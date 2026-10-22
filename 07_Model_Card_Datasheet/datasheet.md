# Datasheet — Fiduciary Clause Recommendation Evaluation Dataset v0.0

## Motivation
- **Purpose:** Create a traceable evaluation dataset to test whether a verifiable clause-recommendation artefact improves attribution and reduces hallucination relative to B0, B1 and current practice, without loss of legal correctness.
- **Created by / funded by:** Planned doctoral dataset led by Jesús Vicente Inca Cárdenas (UNMSM) in one SBS-supervised fiduciary institution, under written institutional authorisation. Funding: self-funded doctoral research with possible in-kind institutional support; UNKNOWN — to investigate.

## Composition
- **What instances represent:** One instance is a drafting query linked to its candidate clauses from each condition (B0–B3), their citations, and the gold annotations of attribution, hallucination type and legal severity.
- **Linked components:** (A) de-identified precedent clauses; (B) normative provisions with identifiers and validity dates; (C) drafting queries; (D) system outputs and run metadata (seed, model version, snapshot); (E) gold annotations and adjudication records.
- **Sample vs population:** One clause family within one trust type in one institution. NOT representative of all Peruvian fiduciary contracts or institutions. Number of queries: UNKNOWN — to investigate until the power analysis.
- **Current status / missingness:** NO DATA COLLECTED YET. Field dictionary, missing-data rules and corpus size will be reported only in aggregate after de-identification.

## Collection process
- **How collected:** Precedent clauses extracted from the institution’s templates and executed contracts and de-identified on-premise; norms retrieved from the SBS normative portal and SPIJ with consultation dates; queries elicited with the legal area; system outputs logged by the prototype; annotations produced by external lawyers with a written guideline.
- **Experimental structure:** Same queries under B0, B1 and B2 (same base model) with k seeded runs each, plus B3 clauses drafted by legal staff under the usual procedure.
- **Consent / ethics:** Begins only after ethics approval at UNMSM and written institutional authorisation; informed consent and confidentiality agreements for annotators, panel members and participating analysts.
- **Timeframe:** Months 19–24 of the doctoral plan; exact dates: UNKNOWN — to investigate.

## Preprocessing / cleaning / labeling
- **Steps:** De-identification before any processing; separation of identifiers under restricted access; versioning of the normative corpus with validity dates; dated snapshot frozen for evaluation; annotation of attribution spans, hallucination type and severity; agreement reported with Krippendorff’s α; documented adjudication.
- **Leakage control:** Gold passages and queries created without access to the artefact’s segmentation or outputs; annotators blind to condition; no evaluation query used for tuning.
- **Raw data available:** Raw contract text, client data and pre-de-identification records will NOT be released and will not leave the institution’s controlled environment.

## Uses
- **Appropriate uses:** Doctoral evaluation of the artefact; reproducibility audit of the comparison; analysis of attribution, hallucination and correctness failure modes; refinement of design principles.
- **Should NOT be used for:** Training commercial or unrelated models; re-identification of clients, counterparties or trusts; legal advice; assessment or ranking of individual employees (B3 data describe practice, not people); profiling; claims about other institutions or clause families.

## Distribution
- **How distributed:** Shareable after review: schema, annotation guideline, synthetic examples, aggregate results and the public normative corpus with consultation dates. Contract-derived data stay access-controlled inside the institution.
- **License / restrictions:** UNKNOWN — to investigate — to be aligned with the institutional authorisation, banking secrecy, data-protection law and consent terms.

## Maintenance
- **Maintainer:** Doctoral researcher under UNMSM governance and the host institution’s data-protection policies.
- **Versioning:** Snapshots versioned with DVC and MD5 hashes, runs logged in MLflow, normative updates recorded with validity dates (scaffold of Deliverable No. 5).
- **Retention / deletion:** Retention period, storage location, access revocation and deletion schedule: UNKNOWN — to investigate before data collection.
