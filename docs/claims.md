# Claims

- Mechanism claim: robot data selection should identify action-critical causal mechanisms, not merely balance labels or mine high-loss failures.
- Method claim: selecting examples by intervention score, mechanism coverage, spurious-confound penalty, tail-failure risk, and cost constraint improves downstream robustness.
- Evidence claim: the local benchmark shows the proposed selector beats the strongest non-oracle baseline by `0.105 +/- 0.008` combined-stress success, wins `7/7` paired seeds, improves causal recall by `0.087`, reduces spurious dependence by `0.117`, and survives ablations.
- Scope claim: results support a strong local submission rebuild, not final ICLR-main readiness.
- Unsupported claim explicitly avoided: no claim of real-robot SOTA or universal dataset curation.
