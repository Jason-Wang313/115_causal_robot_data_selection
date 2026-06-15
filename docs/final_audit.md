# Final Audit

Paper: 115 causal_robot_data_selection

Submission-hardening version: v4

Terminal decision: STRONG_REVISE

## Evidence

The archive scaffold was replaced with a causal robot data-selection benchmark. The benchmark evaluates 5 skill families, 7 causal/spurious regimes, 5 budgets/splits, 9 selectors, 7 seeds, and 84 rollout episodes per group. The proposed causal mechanism selector beats the strongest non-oracle baseline, `invariant_risk_selection`, under combined stress.

Key results:
- Success: `0.674 +/- 0.008` proposed vs `0.570 +/- 0.009` strongest baseline.
- Paired difference: `0.105 +/- 0.008`; wins `7/7`.
- Causal-recall delta: `+0.087`.
- Spurious-dependence delta: `-0.117`.
- Tail-failure delta: `-0.037`.
- Damage delta: `-0.026`.
- Selection-cost delta: `-0.026`.
- Best ablation gap: `0.036`.

## Remaining Risk

The result is local benchmark evidence. It lacks real robot experiments, external high-fidelity simulator transfer, released selected datasets, trained policies, and hardware videos. The correct terminal action is strong revise, not ICLR-main-ready submission.
