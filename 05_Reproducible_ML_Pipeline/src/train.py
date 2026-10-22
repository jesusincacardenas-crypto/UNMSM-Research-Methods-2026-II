"""Leakage-free, seed-controlled clause-type classification for Deliverable 05.

Task: predict the clause type of a contract provision (LEDGAR subset), a first step
toward clause recommendation in the doctoral thesis.
Run: python src/train.py --seed 42  (re-launches itself with PYTHONHASHSEED=0)

Note on randomness: LogisticRegression(lbfgs) is deterministic, so the seed changes the
StratifiedKFold partition. Seed variance is therefore variance due to the data split.
"""
import argparse, hashlib, json, os, random, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
N_SPLITS = yaml.safe_load((ROOT / "params.yaml").read_text(encoding="utf-8"))["train"]["n_splits"]
# zero_division=0 keeps the majority baseline from emitting UndefinedMetricWarning
SCORING = {
    "accuracy": "accuracy",
    "balanced_accuracy": "balanced_accuracy",
    "f1_macro": make_scorer(f1_score, average="macro", zero_division=0),
    "f1_weighted": make_scorer(f1_score, average="weighted", zero_division=0),
    "precision_macro": make_scorer(precision_score, average="macro", zero_division=0),
    "recall_macro": make_scorer(recall_score, average="macro", zero_division=0),
}
DEFAULT_DATA = ROOT / "data" / "ledgar_subset.csv"
MODEL_DESC = {
    "tfidf_logreg": {"features": "TF-IDF word 1-2 grams, min_df=2, max_features=50000, sublinear_tf",
                     "classifier": "LogisticRegression lbfgs C=4 max_iter=3000"},
    "majority_baseline": {"features": "none", "classifier": "DummyClassifier most_frequent"},
}

def ensure_hash_seed():
    """Re-launches the current script with PYTHONHASHSEED=0 if it is not already set,
    so `python src/...` behaves the same on every shell (including Windows cmd)."""
    if os.environ.get("PYTHONHASHSEED") != "0":
        env = {**os.environ, "PYTHONHASHSEED": "0"}
        sys.exit(subprocess.run([sys.executable, *sys.argv], env=env).returncode)

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)

def build_pipeline(seed, model="tfidf_logreg"):
    """TF-IDF is fitted inside each training fold, so no vocabulary or IDF weight
    is learned from validation clauses (no preprocessing leakage)."""
    if model == "majority_baseline":
        return Pipeline([("model", DummyClassifier(strategy="most_frequent"))])
    return Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2,
                                  max_features=50000, sublinear_tf=True)),
        ("model", LogisticRegression(max_iter=3000, C=4.0, random_state=seed)),
    ])

def evaluate(seed=42, data_path=None, model="tfidf_logreg"):
    set_seed(seed)
    data_path = Path(data_path or DEFAULT_DATA)
    df = pd.read_csv(data_path, encoding="utf-8")
    X, y = df["text"], df["label_name"]
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
    raw = cross_validate(build_pipeline(seed, model), X, y, cv=cv, scoring=SCORING,
                         n_jobs=1, return_train_score=False)
    summary = {"seed": seed, "model": model,
               "data_md5": hashlib.md5(data_path.read_bytes()).hexdigest(),
               "n_rows": int(len(df)), "n_classes": int(y.nunique())}
    folds = []
    for k in range(N_SPLITS):
        row = {"seed": seed, "model": model, "fold": k + 1}
        for m in SCORING:
            row[m] = float(raw[f"test_{m}"][k])
        folds.append(row)
    for m in SCORING:
        vals = raw[f"test_{m}"]
        summary[f"{m}_mean"] = float(vals.mean())
        summary[f"{m}_sd"] = float(vals.std(ddof=1))
    return summary, pd.DataFrame(folds)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--model", default="tfidf_logreg", choices=list(MODEL_DESC))
    ap.add_argument("--data", default=None)
    ap.add_argument("--exact", action="store_true", help="print full-precision floats (used by the repeatability check)")
    a = ap.parse_args()
    ensure_hash_seed()
    s, _ = evaluate(a.seed, a.data, a.model)
    if not a.exact:
        s = {k: (round(v, 5) if isinstance(v, float) else v) for k, v in s.items()}
    print(json.dumps(s, sort_keys=True))
