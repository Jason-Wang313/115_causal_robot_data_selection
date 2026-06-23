# Paper 115 Expanded v5 Submission Plan

Date: 2026-06-23

Paper: `causal_robot_data_selection`

Goal: rebuild Paper 115 into a 25+ page ICLR-style submission package that maximizes honest acceptance odds under CPU-only, RAM-light constraints. The target is not pretty results. The target is evidence that survives hostile review.

## Frozen Decision Policy

- Primary terminal labels: `STRONG_REVISE` if all frozen local empirical gates pass but external scope evidence is missing; `KILL_ARCHIVE` if any key local empirical gate fails.
- ICLR-main readiness can be `yes` only with real robot or accepted high-fidelity retrieval of downstream policy evidence, selected dataset release, trained policy checkpoints, calibrated deployment logs, and rollout/video artifacts. The current run is expected to fail this scope gate unless such evidence already exists locally.
- Do not optimize after seeing final test rows. Method development is allowed only before the v5 protocol is frozen in this file.
- Report all predefined results: main, hard aggregate, paired seeds, ablations, stress endpoints, fixed-risk budgets, failure cases, and scope gates.

## Method Being Tested

Proposed v5 method: `interventional_mechanism_value_selector_v5`.

The method scores candidate robot data by four theory-motivated terms:

- Interventional contrast: whether selected data separates action effects from observed correlations.
- Mechanism coverage: whether rare contact, compliance, occlusion, and recovery mechanisms are covered under the budget.
- Spurious suppression: whether selected data avoids shortcuts such as color, operator, camera, morphology, and success-frequency proxies.
- Deployment value: whether the selected subset improves downstream success and utility while controlling tail failures, damage, cost, regret, and calibration.

The old v4 method, `proposed_causal_mechanism_selector_v4`, remains in the baseline suite. It is not renamed away; it must be beaten.

## Main Experiment

- 16 selectors.
- 5 robot skill families.
- 8 causal/spurious shift regimes.
- 4 data budgets.
- 4 evaluation splits.
- 10 paired seeds.
- 102,400 main rollout-cell rows.
- 10,240 main group rows.
- 1,280 seed metric rows.
- 128 method metric rows.

Metrics:

- Downstream success.
- Causal mechanism recall.
- Spurious dependence.
- Tail failure.
- Damage rate.
- Selection cost.
- Regret.
- Calibration error.
- Safety utility.

## Hostile Baselines

- `random_uniform_selector`
- `label_balanced_selector`
- `diversity_coreset_selector`
- `failure_mining_selector`
- `uncertainty_active_selector`
- `influence_function_selector`
- `invariant_risk_selector`
- `domain_adversarial_selector`
- `counterfactual_pair_selector`
- `tail_risk_reweighting_selector`
- `conformal_shift_guard_selector`
- `offline_rl_value_selector`
- `foundation_embedding_filter`
- `proposed_causal_mechanism_selector_v4`
- `interventional_mechanism_value_selector_v5`
- `oracle_interventional_selector`

## Frozen Local Gates

- v5 must beat the strongest non-oracle baseline on hard-aggregate success by at least 0.030.
- v5 must beat the strongest non-oracle baseline on hard-aggregate utility by at least 0.050.
- v5 must improve causal mechanism recall by at least 0.040.
- v5 must reduce spurious dependence by at least 0.020.
- v5 must not increase tail failure, damage, selection cost, regret, or calibration error.
- v5 must win at least 8 of 10 paired hard-utility seeds.
- Full v5 must beat the best ablation by at least 0.020 success and 0.040 utility.
- The maximum-stress endpoint must preserve positive success and utility margins.
- Fixed-risk deployment at budget 0.10 must show positive coverage, zero predefined budget breach, and positive utility margin against the strongest non-oracle baseline.
- PDF must be 25+ pages, compile cleanly, use bright boxed clickable citations, and exist as `C:/Users/wangz/Downloads/115.pdf` only.

## Stress And Fixed-Risk Protocols

- Stress sweep: 48,000 rollout-cell rows over six stress axes and ten stress levels.
- Ablations: 8,000 rollout-cell rows over ten component removals/variants.
- Fixed-risk audit: 51,200 rollout-cell rows over two risk budgets.
- Failure cases: 24 manually named boundary cases generated from the frozen run configuration.

## Manuscript Requirements

- 25+ pages without filler.
- Expanded theory section defining mechanism value, spurious risk, utility, and gate rationale.
- Related work must cite real active learning, influence, invariant learning, causal confusion, offline RL datasets, and robot data-scale references.
- Results must include main table, hard aggregate, ablations, stress sweep, fixed-risk table, failure taxonomy, and final submission-readiness checklist.
- Cite links must appear as evident bright boxes in the PDF and route to references.

## Artifact Policy

- Canonical PDF: `C:/Users/wangz/Downloads/115.pdf`.
- Do not copy `115.pdf` to the visible Desktop.
- Do not leave numbered PDFs in the factory root or child repo root.
- Push the public GitHub repository only after code, results, manuscript, validator, and artifact-location checks pass.
