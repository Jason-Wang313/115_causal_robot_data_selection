# Paper 115 Expanded Submission Plan - 2026-06-23

This is the frozen v5 plan for Paper 115, `causal_robot_data_selection`.

## Reviewer-Hostile Objective

The work is rebuilt as an action-critical causal robot data-selection paper. The acceptance strategy is to expose weaknesses with strong baselines and stress tests, improve the method before freezing, and then report every predefined outcome honestly.

## Evidence Standard

The run must produce:

- A deterministic CPU-only experiment.
- 102,400 main rollout-cell rows.
- 8,000 ablation rollout-cell rows.
- 48,000 stress rollout-cell rows.
- 51,200 fixed-risk rollout-cell rows.
- 24 failure cases.
- 25+ page ICLR-style PDF with bright boxed citations.
- Downloads-only numbered PDF artifact.
- Public GitHub commit.

## Frozen Empirical Gates

The local evidence passes only if:

- The v5 selector beats the strongest non-oracle baseline in hard success by at least 0.030.
- The v5 selector beats the strongest non-oracle baseline in hard utility by at least 0.050.
- Causal-mechanism recall improves by at least 0.040.
- Spurious dependence decreases by at least 0.020.
- Tail failure, damage, cost, regret, and calibration do not regress.
- v5 wins at least 8/10 paired hard-utility seeds.
- Full v5 beats every ablation by at least 0.020 success and 0.040 utility.
- The maximum-stress endpoint preserves positive success and utility margins.
- Fixed-risk deployment at risk budget 0.10 has positive coverage, zero breach, and positive utility margin.

## Scope Gate

ICLR-main readiness remains `no` unless all of the following exist:

- Real robot data-selection/downstream-policy rollouts or accepted high-fidelity external simulator validation.
- Released selected datasets or selection indices.
- Trained downstream policy checkpoints.
- Calibrated data-collection/deployment logs.
- Rollout videos or qualitative hardware artifacts.
- Manual full-paper related-work synthesis.

## Reporting Rule

If local gates pass but scope evidence is missing, the terminal decision is `STRONG_REVISE`, not `ICLR_MAIN_READY`. If any local gate fails, the paper is marked `KILL_ARCHIVE` or `REVIVE_ONLY_WITH_NEW_EVIDENCE`.
