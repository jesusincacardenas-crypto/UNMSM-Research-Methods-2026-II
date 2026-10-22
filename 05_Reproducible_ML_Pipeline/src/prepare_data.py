"""Builds the fixed, versionable LEDGAR clause subset for Deliverable 05.

Source: LEDGAR (LexGLUE benchmark), contract provisions from public SEC EDGAR filings,
each labelled with its clause type. No institutional or client data is used.
The Hub revision is pinned (params.yaml), so the same subset is rebuilt byte for byte.

Run: python src/prepare_data.py  (parameters are read from params.yaml)
"""
import argparse, hashlib, json, re
from pathlib import Path
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PARAMS = yaml.safe_load((ROOT / "params.yaml").read_text(encoding="utf-8"))["prepare"]

def load_ledgar_train(revision):
    """Loads the LEDGAR training split at a pinned Hub commit. Fails loudly: a silent
    fallback to another source would produce a different file and a different MD5."""
    from datasets import load_dataset
    ds = load_dataset("coastalcph/lex_glue", "ledgar", split="train", revision=revision)
    names = ds.features["label"].names
    df = ds.to_pandas()
    df["label_name"] = df["label"].map(lambda i: names[i])
    return df, f"datasets.load_dataset('coastalcph/lex_glue', 'ledgar', split='train', revision='{revision}')"

def build_subset(n_classes, per_class, sample_seed, revision):
    df, source = load_ledgar_train(revision)
    df["text"] = df["text"].astype(str).map(lambda t: re.sub(r"\s+", " ", t).strip())
    df = df[df["text"].str.len() > 0]
    # Explicit tie-break (count desc, then name) so the top-k classes never depend on sort stability
    counts = df["label_name"].value_counts().rename_axis("label_name").reset_index(name="n")
    top = counts.sort_values(["n", "label_name"], ascending=[False, True]).head(n_classes)["label_name"].tolist()
    pool = df[df["label_name"].isin(top)]
    if pool["label_name"].value_counts().min() < per_class:
        raise ValueError("A selected clause type has fewer rows than --per-class")
    sub = pool.groupby("label_name").sample(n=per_class, random_state=sample_seed)
    sub = sub.sample(frac=1.0, random_state=sample_seed).reset_index(drop=True)
    sub.insert(0, "clause_id", [f"LEDGAR-{i:05d}" for i in range(len(sub))])
    return sub[["clause_id", "text", "label_name"]], source, top

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-classes", type=int, default=PARAMS["n_classes"])
    ap.add_argument("--per-class", type=int, default=PARAMS["per_class"])
    ap.add_argument("--sample-seed", type=int, default=PARAMS["sample_seed"])
    ap.add_argument("--revision", default=PARAMS["hf_revision"])
    a = ap.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)
    sub, source, top = build_subset(a.n_classes, a.per_class, a.sample_seed, a.revision)
    out = DATA / "ledgar_subset.csv"
    sub.to_csv(out, index=False, lineterminator="\n", encoding="utf-8")
    md5 = hashlib.md5(out.read_bytes()).hexdigest()
    card = {"dataset": "LEDGAR (LexGLUE)", "loader": source, "hf_revision": a.revision, "split": "train",
            "n_classes": a.n_classes, "per_class": a.per_class, "sample_seed": a.sample_seed,
            "n_rows": int(len(sub)), "classes": top,
            "rows_per_class": sub["label_name"].value_counts().sort_index().to_dict(),
            "file": "data/ledgar_subset.csv", "md5": md5}
    (DATA / "dataset_card.json").write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"n_rows": card["n_rows"], "n_classes": a.n_classes, "md5": md5}))
