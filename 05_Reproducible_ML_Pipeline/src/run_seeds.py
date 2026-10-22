"""Runs the seven-seed study, the same-seed repeatability checks and MLflow logging.
Run: python src/run_seeds.py  (or `dvc repro`; re-launches itself with PYTHONHASHSEED=0)

Outputs: results/ (per-seed and per-fold metrics, mean ± SD table, metrics.json for DVC,
manifest.json with code/data/environment fingerprints) and figures/.
The seed-42 reference in reference/expected_seed42.json (Git-tracked, outside the DVC outputs)
is compared, never silently overwritten.
"""
import argparse, hashlib, json, os, platform, subprocess, sys
from importlib.metadata import version
from pathlib import Path
import pandas as pd
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train import evaluate, ensure_hash_seed, SCORING, DEFAULT_DATA, MODEL_DESC, N_SPLITS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES, FIG, REF = ROOT / "results", ROOT / "figures", ROOT / "reference"
PARAMS = yaml.safe_load((ROOT / "params.yaml").read_text(encoding="utf-8"))
SEEDS = PARAMS["train"]["seeds"]
EXPERIMENT = "UNMSM-D5-clause-reproducibility"
LIBS = ["scikit-learn", "numpy", "scipy", "pandas", "matplotlib", "mlflow", "datasets", "dvc", "PyYAML"]
REF_KEYS = ("accuracy_mean", "f1_macro_mean")

def git(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None

def environment():
    return {"python": platform.python_version(), "platform": platform.platform(),
            "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
            "libraries": {lib: version(lib) for lib in LIBS}}

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

def repeatability_check(seed=42):
    """Same seed twice in this process, and twice in fresh processes (full-precision JSON)."""
    s1, f1 = evaluate(seed)
    s2, f2 = evaluate(seed)
    in_process = (s1 == s2) and f1.equals(f2)
    cmd = [sys.executable, str(ROOT / "src" / "train.py"), "--seed", str(seed), "--exact"]
    outs = [json.loads(subprocess.check_output(cmd, cwd=ROOT, text=True)) for _ in range(2)]
    cross_process = outs[0] == outs[1] == s1
    rep = {"seed": seed, "identical_in_process": in_process, "identical_across_processes": cross_process,
           "run_a": {k: s1[k] for k in REF_KEYS}, "run_b": {k: s2[k] for k in REF_KEYS},
           "subprocess_runs": [{k: o[k] for k in REF_KEYS} for o in outs],
           "fold_accuracy": [round(v, 8) for v in f1["accuracy"].tolist()]}
    if not (in_process and cross_process):
        write_json(RES / "repeatability_seed42.json", rep)
        raise RuntimeError("Same-seed repeatability FAILED: results differ (see results/repeatability_seed42.json)")
    return rep

def check_reference(ref, update):
    """Compares the seed-42 result with the committed reference; writes it only if absent or --update-reference."""
    REF.mkdir(exist_ok=True)
    path = REF / "expected_seed42.json"
    if path.exists() and not update:
        expected = json.loads(path.read_text(encoding="utf-8"))
        diffs = {k: (expected[k], ref[k]) for k in expected if expected[k] != ref.get(k)}
        if diffs:
            raise RuntimeError(f"Seed-42 result differs from reference/expected_seed42.json: {diffs}")
        return "matched existing reference"
    write_json(path, ref)
    return "reference written"

def mean_sd_table(overall):
    lines = ["| Model | Metric | Mean ± SD across 7 seeds (%) | Min–Max (%) | Range (pp) |",
             "|---|---|---|---|---|"]
    for r in overall.itertuples():
        lines.append(f"| {r.model} | {r.metric} | {r.mean*100:.2f} ± {r.sd*100:.2f} | "
                     f"{r.min*100:.2f}–{r.max*100:.2f} | {r.range_pp:.2f} |")
    return "\n".join(lines) + "\n"

def main(use_mlflow=True, update_reference=False):
    RES.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
    rep = repeatability_check(42)
    write_json(RES / "repeatability_seed42.json", rep)
    print("Repeatability seed 42: PASSED (in-process and across processes)")

    commit, dirty = git("rev-parse", "HEAD"), bool(git("status", "--porcelain", "--untracked-files=no"))
    env = environment()
    if use_mlflow:
        import mlflow
        mlflow.set_tracking_uri(f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}")
        if mlflow.get_experiment_by_name(EXPERIMENT) is None:
            mlflow.create_experiment(EXPERIMENT, artifact_location=(ROOT / "mlartifacts").as_uri())
        mlflow.set_experiment(EXPERIMENT)
        parent = mlflow.start_run(run_name="seed-study")
        mlflow.set_tags({"git_commit": str(commit), "git_dirty": str(dirty), "python": env["python"]})
        mlflow.log_params({"seeds": str(SEEDS), **{f"lib_{k}": v for k, v in env["libraries"].items()}})

    summaries, folds = [], []
    for model in MODEL_DESC:
        for seed in SEEDS:
            s, f = evaluate(seed, model=model)
            summaries.append(s); folds.append(f)
            fpath = RES / f"fold_metrics_{model}_seed_{seed}.csv"
            f.to_csv(fpath, index=False, lineterminator="\n")
            if use_mlflow:
                with mlflow.start_run(run_name=f"{model}-seed-{seed}", nested=True):
                    mlflow.set_tags({"git_commit": str(commit), "git_dirty": str(dirty)})
                    mlflow.log_params({"seed": seed, "model": model, **MODEL_DESC[model],
                                       "cv": f"StratifiedKFold({N_SPLITS}, shuffle=True, random_state=seed)",
                                       "data_md5": s["data_md5"], "n_rows": s["n_rows"], "n_classes": s["n_classes"],
                                       "sklearn": env["libraries"]["scikit-learn"]})
                    mlflow.log_metrics({k: v for k, v in s.items() if k.endswith(("_mean", "_sd"))})
                    mlflow.log_artifact(str(fpath))
    seed_df = pd.DataFrame(summaries)
    seed_df.to_csv(RES / "seed_summary.csv", index=False, lineterminator="\n")
    pd.concat(folds).to_csv(RES / "fold_metrics_all.csv", index=False, lineterminator="\n")

    rows = []
    for model, g in seed_df.groupby("model"):
        for m in SCORING:
            v = g[f"{m}_mean"]
            rows.append({"model": model, "metric": m, "mean": v.mean(), "sd": v.std(ddof=1),
                         "min": v.min(), "max": v.max(), "range_pp": (v.max() - v.min()) * 100})
    overall = pd.DataFrame(rows)
    overall.to_csv(RES / "overall_stability.csv", index=False, lineterminator="\n")
    (RES / "stability_table.md").write_text(mean_sd_table(overall), encoding="utf-8", newline="\n")
    metrics = {model: {m: {"mean": round(float(r["mean"]), 6), "sd": round(float(r["sd"]), 6)}
                       for m, r in g.set_index("metric").iterrows()}
               for model, g in overall.groupby("model")}
    write_json(RES / "metrics.json", metrics)

    main_df = seed_df[seed_df.model == "tfidf_logreg"].set_index("seed").loc[SEEDS]
    x = [str(s) for s in SEEDS]
    # Figure 1: accuracy and macro-F1 by seed with fold SD; dashed line = mean across seeds
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for m, lab in [("accuracy", "Accuracy"), ("f1_macro", "Macro-F1")]:
        bars = ax.errorbar(x, main_df[f"{m}_mean"] * 100, yerr=main_df[f"{m}_sd"] * 100, marker="o", capsize=4, label=lab)
        ax.axhline(main_df[f"{m}_mean"].mean() * 100, ls="--", lw=1, color=bars[0].get_color())
    ax.set_xlabel("Random seed"); ax.set_ylabel("Mean 5-fold score (%)")
    ax.set_title("Clause-type classification: stability across seven seeds"); ax.legend()
    fig.tight_layout(); fig.savefig(FIG / "fig1_accuracy_f1_by_seed.png", dpi=200); plt.close(fig)
    # Figure 2: all metrics by seed
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for m in SCORING:
        ax.plot(x, main_df[f"{m}_mean"] * 100, marker="o", label=m)
    ax.set_xlabel("Random seed"); ax.set_ylabel("Mean 5-fold score (%)")
    ax.set_title("Multi-metric stability across seven seeds"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "fig2_multimetric_by_seed.png", dpi=200); plt.close(fig)
    # Figure 3: fold-level macro-F1 distribution per seed
    fa = pd.concat(folds); fa = fa[fa.model == "tfidf_logreg"]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.boxplot([fa[fa.seed == s]["f1_macro"] * 100 for s in SEEDS])
    ax.set_xticks(range(1, len(SEEDS) + 1), x)
    ax.set_xlabel("Random seed"); ax.set_ylabel("Fold macro-F1 (%)")
    ax.set_title("Within-seed fold variability (5 folds per seed)")
    fig.tight_layout(); fig.savefig(FIG / "fig3_fold_f1_boxplot.png", dpi=200); plt.close(fig)

    ref = main_df.loc[42]
    expected = {"seed": 42, "model": "tfidf_logreg", "data_md5": ref["data_md5"],
                **{k: round(float(ref[k]), 5) for k in REF_KEYS}}
    ref_status = check_reference(expected, update_reference)

    manifest = {"experiment": EXPERIMENT, "git_commit": commit, "git_dirty": dirty,
                "data": {"file": "data/ledgar_subset.csv",
                         "md5": hashlib.md5(DEFAULT_DATA.read_bytes()).hexdigest(),
                         "hf_revision": PARAMS["prepare"]["hf_revision"]},
                "params": PARAMS, "models": MODEL_DESC, "environment": env,
                "repeatability_seed42": "passed", "reference_seed42": ref_status,
                "outputs_md5": {p.relative_to(ROOT).as_posix(): hashlib.md5(p.read_bytes()).hexdigest()
                                for p in sorted(RES.glob("*.csv"))}}
    write_json(RES / "manifest.json", manifest)

    if use_mlflow:
        mlflow.log_metrics({f"{m}_{stat}": v for m, d in metrics["tfidf_logreg"].items() for stat, v in d.items()})
        for p in [RES / "stability_table.md", RES / "manifest.json", RES / "repeatability_seed42.json", *FIG.glob("*.png")]:
            mlflow.log_artifact(str(p))
        mlflow.end_run()
    print(overall.round(5).to_string(index=False))
    print("Seed-42 reference:", expected, f"({ref_status})")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-mlflow", action="store_true", help="local smoke test only")
    ap.add_argument("--update-reference", action="store_true", help="overwrite reference/expected_seed42.json")
    a = ap.parse_args()
    ensure_hash_seed()
    main(use_mlflow=not a.no_mlflow, update_reference=a.update_reference)
