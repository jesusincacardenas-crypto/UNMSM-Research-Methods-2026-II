# 02 · Method Fit Matrix (Deliverable No. 2)

**File:** `Method_Fit_Matrix_Deliverable_2_(Jesus_Inca).pdf`

## Summary

Method fit matrix comparing four candidate approaches to answer the scoped research question of the project on verifiable contractual clause recommendation.

### Scoped research question
How can a verifiable, human-in-the-loop generative AI artefact be designed and rigorously evaluated to recommend contractual clauses whose every output is traceable to a contrastable normative or contractual source, in one SBS-supervised fiduciary institution and one clearly bounded clause-recommendation task — and does it outperform a standard RAG baseline on verifiability and hallucination control?

### Evaluation criteria (and weights)
| Criterion | Weight | What it measures |
|---|---|---|
| E — Epistemological Fit | 30% | Coherence with the DSR/critical realism paradigm |
| D — Data Feasibility | 20% | Real possibility of obtaining data under banking secrecy |
| F — Feasibility | 15% | Viability within a three-year doctoral timeline |
| C — Contribution | 20% | Delivery of artefact + transferable design knowledge |
| V — Venue Fit | 15% | Publishability in target journals/conferences |

### Comparative results

| Method | Weighted score | Outcome |
|---|---|---|
| Pure Experiment | 2.80/5 (56/100) | Eliminated (fails on data feasibility and feasibility) |
| Pure Case Study | 2.50/5 (50/100) | Eliminated (weak on epistemological fit and contribution) |
| Mixed Methods | 3.65/5 (73/100) | Viable as an evaluation strategy, not as the governing method |
| **Design Science Research** | **4.65/5 (93/100)** | **Selected as the primary method** |

**Gate rule:** any candidate scoring ≤2 on a critical criterion is removed. Under this rule, Pure Experiment and Pure Case Study are eliminated (each scores 2/5 on at least one key criterion: data feasibility/feasibility for the experiment, contribution for the case study).

### Final decision
**Design Science Research (DSR)** is selected as the primary method. Mixed Methods remains a viable evaluation strategy embedded inside the DSR cycle, but not the governing method.

To remain feasible within three years, the DSR study is scoped to:
- **1** functional prototype
- **1** SBS-supervised institution
- **1** clearly bounded clause-recommendation task
- **2–3** primary outcomes: verifiability/attribution quality, hallucination rate, and recommendation quality

A narrowly scoped controlled comparison against a standard RAG baseline is included, along with no-retrieval and current-practice baselines, plus focused expert feedback — all embedded inside the DSR evaluation cycle.

**Additional note:** the simulation/synthetic-data approach is not shortlisted as the primary method (the central claim requires verifiability against real normative sources and real institutional auditability), but it may still be used for pre-deployment stress testing of hallucination and mis-attribution failure modes.

### Data sources for the selected DSR plan
- Prototype interaction logs
- Retrieval traces (retrieved passages per query)
- Generated clauses with their citations
- Citation precision and recall labels
- Span-level attributability judgments
- Hallucination annotations (unsupported, misattributed, or contradictory)
- Annotated legal gold standard
- Focused lawyer/specialist feedback

**Prerequisites:** institutional authorization, banking-secrecy compliance (Ley 26702), data protection (Ley 29733), de-identification of contract text, local/on-premise processing where feasible, and human authority over any adopted clause.
