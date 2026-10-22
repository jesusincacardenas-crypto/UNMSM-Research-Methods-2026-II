# Model Card — VeriClause-HITL v0.0

## Model details
- **Name / version:** VeriClause-HITL v0.0 — Verifiable, human-in-the-loop clause recommendation assistant (research specification)
- **Owner / contact:** Jesús Vicente Inca Cárdenas — UNMSM Doctoral Program in Deep Tech, AI & Emerging Technologies
- **Documentation date:** 22 October 2026
- **Development status:** Pre-implementation Design Science Research specification (Deliverable No. 3). Not yet built, evaluated with experts, or deployed.
- **Architecture:** Seven planned components: (i) de-identification pipeline; (ii) knowledge base of de-identified precedent clauses and applicable norms (Law No. 26702, SBS Resolution No. 1010-99, circulars), versioned with the validity dates of each provision; (iii) query autocompletion; (iv) hybrid retrieval of precedents and norms; (v) generation with a self-hosted LLM; (vi) verifiability layer that decomposes each candidate clause into propositions, checks support by the cited span and that the cited provision is in force, and withholds unsupported candidates; (vii) human review interface (accept / edit / reject).
- **Generation model:** Self-hosted open-weight LLM served on-premise; specific model, version and quantisation: UNKNOWN — to investigate before the formative evaluation.
- **License:** UNKNOWN — to investigate — code licence and the licences of the selected LLM and embedding models must be checked before any release.

## Intended use
- **Primary intended uses:** Advisory recommendation of two or three candidate clauses, each with citations to the supporting precedent clauses and normative provisions, for one bounded clause family within one trust type, inside one SBS-supervised fiduciary institution.
- **Intended users:** Qualified legal analysts of the host institution, who retain authority over every adopted clause; researchers evaluating the artefact under an approved protocol.
- **Out-of-scope / misuse:** NOT for autonomous adoption of clauses; legal advice to clients or the public; jurisdictions, clause families or trust types not covered by the knowledge base; credit evaluation or any decision about individuals; regulatory reporting; use as an authoritative source of law; processing identifiable client data on external services; evaluating the performance of individual employees.

## Factors
- **Relevant groups / conditions:** Clause family and trust type; normative tier of the supporting source (law, regulation, circular, precedent); temporal validity of the cited provision at the reference date; query type (adaptation of a precedent vs. norm-driven drafting); Spanish legal register; analyst experience.
- **Evaluation factors:** Results will be disaggregated by condition (B0 no retrieval, B1 standard RAG, B2 proposed artefact, B3 current practice), by hallucination type (unsupported, misattributed, contradictory), by normative tier, and by clause subtype where the sample allows.

## Metrics
- **Primary 1 — Attribution quality:** Citation precision and recall (Gao et al., 2023) plus span-level attributability judged by lawyers under the AIS criterion (Rashkin et al., 2023).
- **Primary 2 — Hallucination rate:** Proportion of generated propositions that are unsupported, misattributed or contradict the governing framework, reported by type.
- **Primary 3 — Legal correctness (non-inferiority):** Expert severity rubric per clause aggregated by maximum severity; share of queries with at least one legally acceptable suggestion, tested against a prespecified margin Δ.
- **Secondary / process:** Citation faithfulness probe; outdated-source rate; abstention rate; review time and edits relative to B3; accepted, edited and rejected suggestions.
- **Variation approach:** Each query run k times per system with fixed seeds; mean ± SD across runs; mixed-effects logistic regression with item and run effects; paired bootstrap 95% CIs; Holm–Bonferroni across metric × baseline contrasts; one-sided CI for the non-inferiority margin.

## Evaluation data
- **Dataset / design:** NOT YET COLLECTED. Drafting queries for one clause family, evaluated under B0–B3 on a dated, frozen snapshot of the knowledge base; number of queries and k fixed by an a priori power analysis recorded in the preregistration.
- **Gold standard:** Two to three external lawyers with at least five years in trust or financial-regulatory practice, written guideline, Krippendorff’s α ≥ 0.67 (≥ 0.80 preferred), adjudication by a senior expert; annotators blind to condition; the researcher does not annotate.
- **Independence rule:** Queries and gold passages are created without access to the artefact’s segmentation, metadata or outputs (lesson from the Deliverable No. 6 audit).
- **Preprocessing:** De-identification or pseudonymisation of all contract text before any processing; exact pipeline and residual re-identification test: UNKNOWN — to investigate before data collection.

## Training data
- **Datasets:** No fine-tuning is planned in v0.0: knowledge enters through retrieval, not training. The pre-training data of the selected LLM are those of its provider: UNKNOWN — to investigate.
- **Knowledge base (non-parametric):** De-identified precedent clauses from the institution’s typology-specific templates and executed contracts, and the applicable normative corpus retrieved from the SBS portal and SPIJ with recorded consultation dates.
- **Leakage control:** Prompts, thresholds and retrieval settings are frozen before the summative evaluation; evaluation queries are never used for tuning. Any later adaptation would be versioned as a new DSR iteration.

## Quantitative analyses
- **Overall results:** NO THESIS RESULTS YET — no claim about attribution, hallucination or legal correctness of the artefact is made in this deliverable.
- **Proxy component evidence:** Deliverable No. 5 evaluated a clause-type recogniser on public LEDGAR contracts (English, 20 types, 3,000 clauses): macro-F1 92.39% ± 0.11% across 7 seeds, against 0.48% for a majority baseline. This is evidence about a candidate component on a public proxy, not about the artefact.
- **Disaggregated results:** Per-class F1 of the proxy recogniser (seed 42): from 0.98+ (Governing Laws, Severability, Counterparts) down to 0.81 (Terminations) and 0.68 (General). For the thesis, results will be reported per condition, per hallucination type and per normative tier, never as a single pooled score.

## Ethical considerations
- **Risks:** Disclosure of information protected by banking secrecy (Law No. 26702, art. 140) or personal data (Law No. 29733; Supreme Decree No. 016-2024-JUS); fluent but unsupported or outdated clauses; automation bias and over-reliance; attributable but legally incorrect clauses; unclear accountability for adopted text; insider bias of a researcher who leads technology in the host institution.
- **Mitigations:** On-premise, self-hosted processing; de-identification and data minimisation; advisory-only design with the analyst’s decision required; verifiability layer with in-force check and abstention; separate legal-correctness rubric; stopping rule for leaks or highest-severity recommendations; external blind annotators; preregistration; voluntary adoption of the high-risk safeguards of Supreme Decree No. 115-2025-PCM (arts. 31.1, 31.4 and 32).
- **Human agency principle:** Outputs are suggestions with visible sources, never decisions. No clause enters a contract without a qualified legal officer’s decision.

## Caveats and recommendations
- **Caveats:** Research-stage specification only. Verifiability is necessary but not sufficient for a trustworthy clause. No accuracy, safety, generalisability or external validity has been established; transfer beyond one institution is analytical, not statistical.
- **Recommendations:** Before the summative evaluation freeze: LLM and model versions, knowledge-base snapshot, prompts, thresholds, clause family, gold-standard guideline, margin Δ, sample size, analysis plan and environment; read every parameter from one configuration file and log it with each run (Deliverable No. 5 scaffold).
