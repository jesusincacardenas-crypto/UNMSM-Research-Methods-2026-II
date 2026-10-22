"""Stranger test: checks that a fresh clone reproduces the committed results exactly.

1. Data:    rebuilds data/ledgar_subset.csv if missing and checks its MD5 against dvc.lock.
2. Seed 42: re-runs train.py in a fresh process and compares with reference/expected_seed42.json.
3. --full:  re-evaluates every model x seed and compares with the committed results/seed_summary.csv.

Run: python src/verify_reproduction.py [--full]   (exit code 0 = reproduced)
Writes nothing to results/; it only reads the committed files and compares.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train import evaluate, ensure_hash_seed, MODEL_DESC  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ledgar_subset.csv"
TOL = 1e-12  # float round-trip through CSV; anything larger is a real difference

def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))
    return ok

def locked_md5():
    lock = yaml.safe_load((ROOT / "dvc.lock").read_text(encoding="utf-8"))
    return next(o["md5"] for o in lock["stages"]["prepare"]["outs"] if o["path"] == "data/ledgar_subset.csv")

def main(full):
    results = []
    if not DATA.exists():
        print("[info] data/ledgar_subset.csv missing; rebuilding it from the pinned Hub revision")
        subprocess.run([sys.executable, str(ROOT / "src" / "prepare_data.py")], cwd=ROOT, check=True)
    md5, expected_md5 = hashlib.md5(DATA.read_bytes()).hexdigest(), locked_md5()
    results.append(check("Data MD5 matches dvc.lock", md5 == expected_md5, f"{md5} vs {expected_md5}"))

    expected = json.loads((ROOT / "reference" / "expected_seed42.json").read_text(encoding="utf-8"))
    out = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / "src" / "train.py"), "--seed", "42"], cwd=ROOT, text=True))
    diffs = {k: (v, out.get(k)) for k, v in expected.items() if out.get(k) != v}
    results.append(check("Seed 42 matches reference/expected_seed42.json", not diffs,
                         f"accuracy={out['accuracy_mean']}, macro-F1={out['f1_macro_mean']}" if not diffs else str(diffs)))

    if full:
        committed = pd.read_csv(ROOT / "results" / "seed_summary.csv")
        metric_cols = [c for c in committed.columns if c.endswith(("_mean", "_sd"))]
        worst = 0.0
        for model in MODEL_DESC:
            for seed in committed.loc[committed.model == model, "seed"]:
                s, _ = evaluate(int(seed), model=model)
                row = committed[(committed.model == model) & (committed.seed == seed)].iloc[0]
                worst = max(worst, max(abs(s[c] - row[c]) for c in metric_cols))
                print(f"  {model:18s} seed {seed:>5}: macro-F1 {s['f1_macro_mean']:.5f}")
        results.append(check(f"All {len(committed)} model x seed runs match results/seed_summary.csv",
                             worst <= TOL, f"max abs diff {worst:.2e}"))
        f1 = committed.loc[committed.model == "tfidf_logreg", "f1_macro_mean"]
        print(f"Macro-F1 across {len(f1)} seeds: {f1.mean():.4f} +/- {np.std(f1, ddof=1):.4f}")

    print("REPRODUCED" if all(results) else "NOT REPRODUCED")
    return 0 if all(results) else 1

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="also re-run all models x seeds (~3 min)")
    a = ap.parse_args()
    ensure_hash_seed()
    sys.exit(main(a.full))
