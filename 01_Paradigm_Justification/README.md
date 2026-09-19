# 01 · Paradigm Justification (Deliverable No. 1)

**File:** `Epistemological_Statement.pdf`

## Summary

Statement of epistemological paradigm justification for the doctoral thesis *"A Verifiable Generative Artificial Intelligence Model for Contractual Clause Recommendation in Regulated Fiduciary Institutions"*.

### Adopted paradigm
- **Design Science Research (DSR)**, philosophically grounded in **critical realism** (Bhaskar), rather than the pragmatism commonly paired with DSR.
- Distinguishes the domains of the *real* (generative mechanisms: the SBS regulatory framework, the legal logic of clauses, model behaviour), the *actual* (events such as clause generation or the emergence of a hallucination), and the *empirical* (what the researcher can observe/measure).

### Why critical realism rather than pragmatism
1. The object of study is genuinely stratified (causal mechanisms are real even when not observed).
2. Verifiability presupposes a mind-independent foundation (the source norm or clause must exist with content of its own).
3. Fallibilism fits a stochastic artefact evaluated against a contestable legal standard ("modified objectivity").

### Preliminary research question
- **Main question:** How can a verifiable generative AI artefact be designed to recommend contractual clauses so that every recommendation is traceable to a contrastable normative/contractual source, and does it outperform a standard RAG baseline in verifiability and hallucination control without loss of quality?
- **RQ1 (design):** design principles for a verifiable clause-recommendation artefact in an SBS-supervised fiduciary setting.
- **RQ2 (evaluation):** does the artefact achieve higher attribution quality and lower hallucination rates than (a) a no-retrieval baseline, (b) standard RAG, and (c) current institutional practice, while maintaining recommendation quality?

### Data, methods, and contribution
- **Data:** anonymised corpus of fiduciary contracts/clauses, regulatory corpus (SBS norms, Ley 26702), and an annotated gold standard.
- **Methods:** DSR cycle after Peffers et al. (2007), with quantitative evaluation via controlled comparison and human annotation.
- **Dual contribution** (Gregor & Hevner, 2013): prescriptive design principles + empirical evidence of the effect of an explicit verifiability layer.
- **Target venues:** MIS Quarterly, JAIS, EJIS, DESRIST; Artificial Intelligence and Law, ICAIL/JURIX; NLP venues on attribution and factuality.

### Operationalising verifiability
- Grounded in the concept of *attribution* (Rashkin et al., 2023): a proposition is attributable to a source if a reasonable reader would affirm "According to P, s."
- Metrics: citation precision/recall (Gao et al., 2023) and human span-level attributability judgments.
- Hallucination defined as: (i) unsupported, (ii) misattributed, or (iii) contradicting the governing regulatory framework.

### Gold standard and statistical analysis
- Built by at least 2–3 lawyers with fiduciary/financial-regulation expertise, with inter-annotator agreement (Cohen's κ or Krippendorff's α ≥ 0.67, ≥ 0.80 preferred).
- Comparison of 4 conditions: B0 (no retrieval), B1 (standard RAG), B2 (proposed artefact), B3 (current institutional practice).
- Paired statistical tests (McNemar's test, paired bootstrap), multiple-comparison correction (Holm–Bonferroni / Benjamini–Hochberg), effect sizes and confidence intervals reported.

### Legal risk and human oversight
- Applicable legal framework: banking secrecy (Ley 26702, art. 140) and personal data protection (Ley 29733).
- Design implications: de-identification/pseudonymisation of contract data, preference for on-premise deployment, and a data-protection impact assessment if any external processing occurs.
- The artefact is **explicitly advisory**: final authority over any adopted clause remains with a qualified legal officer.

### Transferability and novelty
- Transferability claimed as analytical generalisation (design principles), not statistical generalisation, validated by an expert panel and, if possible, a second-site instantiation.
- The claim that no comparable model exists in the literature or the Peruvian State will be supported by a PRISMA-style systematic review (Scopus, Web of Science, IEEE Xplore, ACL Anthology, SSRN).

### Open tension
Verifiability ≠ correctness: a clause can be perfectly attributable to an outdated or legally mistaken source. The thesis will treat correctness as a dimension distinct from attribution, and will state verifiability as a necessary but not sufficient condition for trustworthiness.
