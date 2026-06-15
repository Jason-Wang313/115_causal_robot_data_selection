# 115 Causal Robot Data Selection

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild replaces the archive/template scaffold with a paper-specific local benchmark for causal robot data selection. The v4.1 continuation audit expands stress and failure coverage while preserving the honest strong-revise direction: selecting data by action-critical causal mechanism improves downstream policy robustness under spurious-correlation and mechanism-shift stress. The paper is not yet ICLR-main ready because it lacks real robot or external high-fidelity validation.

## Evidence Snapshot

- Design: 5 robot skill families x 7 causal/spurious regimes x 5 budgets/splits x 9 selectors, 7 paired seeds, 84 rollout episodes per group.
- Strongest non-oracle baseline: `invariant_risk_selection`.
- Combined-stress success: proposed `0.674 +/- 0.008` vs baseline `0.570 +/- 0.009`.
- Paired difference: `0.105 +/- 0.008`, wins `7/7` seeds.
- Causal-mechanism recall delta: `+0.087`.
- Spurious-dependence delta: `-0.117`.
- Tail-failure delta: `-0.037`; damage delta: `-0.026`; selection-cost delta: `-0.026`.
- Best ablation gap: `0.036`.
- Stress sweep coverage: `5,880` task/regime/seed rows plus `24` aggregate rows.
- Failure cases: `8` documented causal-data-selection boundaries.
- Latest rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/115_causal_robot_data_selection_continuation_rerun_20260615.log`.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/115.pdf`

PDF SHA256: `D8953A338C245EC65F6103ED57468C873DF2AAB5A9F696870EA0E41142624E93`

PDF size: `394835` bytes.

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
