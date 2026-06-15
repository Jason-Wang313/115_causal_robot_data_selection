# Submission Readiness Audit v4.1

Paper: 115 `causal_robot_data_selection`

Date: 2026-06-15

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

Command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\115_causal_robot_data_selection_continuation_rerun_20260615.log
```

## Integrity Gates

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1,575 rows.
- `seed_task_regime_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 24 rows.
- `stress_sweep_seed_metrics.csv`: 5,880 task/regime/seed rows.
- `failure_cases.csv`: 8 rows.
- Numeric sanity: no NaN or infinite values found.

## Result Gates

- Strongest non-oracle baseline: `invariant_risk_selection`.
- Combined-stress success: `0.674 +/- 0.008` proposed vs `0.570 +/- 0.009` baseline.
- Paired success gain: `0.105 +/- 0.008`, 7/7 seed wins.
- Causal-mechanism recall: `0.633` proposed vs `0.545` baseline.
- Spurious dependence: `0.130` proposed vs `0.247` baseline.
- Tail failure: `0.076` proposed vs `0.113` baseline.
- Damage rate: `0.042` proposed vs `0.068` baseline.
- Selection cost: `0.222` proposed vs `0.248` baseline.
- Ablation margin over best removed component: `0.036`.
- Max stress success: `0.623 +/- 0.010` proposed vs `0.478 +/- 0.004` invariant risk and `0.749 +/- 0.003` oracle.

## Artifact Gate

- Canonical PDF: `C:/Users/wangz/Downloads/115.pdf`.
- PDF SHA256: `D8953A338C245EC65F6103ED57468C873DF2AAB5A9F696870EA0E41142624E93`.
- PDF size: `394835` bytes.
- Desktop PDF copy: absent.
- LaTeX/BibTeX scan: clean except benign `rerunfilecheck`; BibTeX reports `warning$ -- 0`.

## Submission Decision

The local evidence clears the strong-revise gate: strongest-baseline margin, causal-recall gain, spurious-dependence reduction, tail-failure/damage/cost non-regression, paired-seed wins, ablation margin, expanded stress detail, and failure-case documentation all pass.

The paper is not ICLR-main ready. It still needs real robot or independent high-fidelity validation, selected dataset and trained policy release, hardware/video artifacts, and deeper manual related-work synthesis before submission.
