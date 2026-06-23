# Submission Readiness Audit v5

Paper: 115 `causal_robot_data_selection`

Date: 2026-06-23

Terminal decision: `STRONG_REVISE`

ICLR-main ready: `no`

## Integrity

- `dataset_summary.csv`: 80 rows.
- `cell_metrics.csv`: 102,400 rows.
- `main_group_metrics.csv`: 10,240 rows.
- `seed_metrics.csv`: 1,280 rows.
- `metrics.csv`: 128 rows.
- `hard_seed_metrics.csv`: 160 rows.
- `hard_aggregate_metrics.csv`: 16 rows.
- `hard_pairwise_stats.csv`: 15 rows.
- `ablation_cell_metrics.csv`: 8,000 rows.
- `ablation_seed_metrics.csv`: 100 rows.
- `ablation_metrics.csv`: 10 rows.
- `stress_sweep_cell_metrics.csv`: 48,000 rows.
- `stress_sweep_seed_metrics.csv`: 600 rows.
- `stress_sweep.csv`: 60 rows.
- `fixed_risk_cell_metrics.csv`: 51,200 rows.
- `fixed_risk_seed_metrics.csv`: 320 rows.
- `fixed_risk_metrics.csv`: 32 rows.
- `fixed_risk_pairwise_stats.csv`: 28 rows.
- `failure_cases.csv`: 24 rows.

## Result Gates

- Strongest non-oracle baseline: `proposed_causal_mechanism_selector_v4`.
- Hard success: `0.69673` v5 vs `0.60831` baseline.
- Hard utility: `0.63641` v5 vs `0.45486` baseline.
- Causal-recall delta: `+0.08002`.
- Spurious-dependence delta: `-0.06968`.
- Tail-failure delta: `-0.02340`.
- Damage delta: `-0.01624`.
- Selection-cost delta: `-0.02115`.
- Regret delta: `-0.04237`.
- Paired hard utility wins: `10/10`.
- Ablation success margin: `0.02132`.
- Ablation utility margin: `0.05251`.
- Stress endpoint utility margin: `0.23837`.
- Strict fixed-risk coverage: `0.55813`.
- Strict fixed-risk breach: `0.00000`.
- Strict fixed-risk utility margin: `0.20267`.

## Artifact

- PDF: `C:/Users/wangz/Downloads/115.pdf`
- SHA256: `718DE79DFE5AE2991958D6C2C43EE6CD3273C5BE34EFC4331C1E721E2AB3B4C4`
- Pages: 25
- Validator: passed.

## Scope Failures

- No real robot data-selection rollouts.
- No accepted high-fidelity data-selection simulation.
- No released selected dataset or indices.
- No trained downstream policy checkpoint.
- No calibrated collection or deployment logs.
- No rollout videos.
- Manual full-paper related-work synthesis remains incomplete.
