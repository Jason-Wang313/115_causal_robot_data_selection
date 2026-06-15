# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

Reason: The v4 rebuild adds a paper-specific causal robot data-selection benchmark with strong local evidence. The proposed selector beats `invariant_risk_selection` by `0.105 +/- 0.008` combined-stress success, wins `7/7` paired seeds, improves causal recall, lowers spurious dependence, tail failure, damage, and selection cost, and survives ablations.

Honest terminal action: keep and revise aggressively. Do not submit as final ICLR main paper until external validation is added.

Revival-to-ready condition: add real robot or accepted high-fidelity simulator experiments, release selected datasets/trained policies, compare to external data-curation baselines, and deepen related work through manual full-paper reading.
