# Deliverable 07 — Model Card + Dataset Datasheet

**Course:** Research Methods and Scientific Integrity in AI and Advanced Technologies  
**Doctoral Program:** Deep Tech, Artificial Intelligence & Emerging Technologies — UNMSM  
**Student:** Jesús Vicente Inca Cárdenas  
**Instructor:** Dr. Loveleen Gaur  
**Semester:** 2026-II

## Deliverable
Session 7 deliverable: a **Model Card** (Mitchell et al., 2019) for the doctoral research artefact and a **Datasheet** (Gebru et al., 2021) for its planned evaluation dataset.

### Research artefact
**VeriClause-HITL v0.0** — a verifiable, human-in-the-loop clause-recommendation assistant for one clause family in one SBS-supervised fiduciary institution. Every candidate clause is cited to precedent clauses and normative provisions in force; unsupported candidates are withheld; a legal analyst decides.

## Evidence status
**Pre-implementation specification.** The artefact has not been built or evaluated and no thesis result is claimed. Unresolved fields are marked `UNKNOWN — to investigate`.

## Files
- `model_card.md` — 9 Model Card sections.
- `datasheet.md` — 7 Datasheet sections.
- `documentation_scorecard.md` — self-audit, 8/8.
- `regulatory_crosswalk.md` — educational gap analysis against EU AI Act Annex IV and Peru's Supreme Decree No. 115-2025-PCM.
- `REPRODUCIBILITY_REPORT.md` — environment, evidence status and integrity boundary.
- `results_summary.json` and `fig_*.png` — results of the proxy exercises.
- `Notebook_HandsOn_Inca.ipynb` / `Notebook_HandsOn_Executed_Inca.ipynb` — customised Session 7 notebook, clean and executed.
- `D7_Model_Card_Datasheet_Jesus_Inca.pdf` / `.docx` — report.

## Data used by the notebook
Exercises 1–3 and 7–10 run on the public **LEDGAR clause subset** versioned in Deliverable 05 (MD5 `bc995ef9bacb814a07d06dbecad47ad0`). Retrieve it first:

```bash
cd ../05_Reproducible_ML_Pipeline && python -m dvc pull && cd ../07_Model_Card_Datasheet
jupyter nbconvert --to notebook --execute Notebook_HandsOn_Inca.ipynb
```

## Integrity boundary
LEDGAR results are **course demonstrations on a public English-language proxy**, not evidence about the attribution, hallucination or legal correctness of the artefact.
