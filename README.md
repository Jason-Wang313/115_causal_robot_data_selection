# 115 Causal Robot Data Selection

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild replaces the archive/template scaffold with a paper-specific local benchmark for causal robot data selection. The evidence supports a strong-revise direction: selecting data by action-critical causal mechanism improves downstream policy robustness under spurious-correlation and mechanism-shift stress. The paper is not yet ICLR-main ready because it lacks real robot or external high-fidelity validation.

## Evidence Snapshot

- Design: 5 robot skill families x 7 causal/spurious regimes x 5 budgets/splits x 9 selectors, 7 paired seeds, 84 rollout episodes per group.
- Strongest non-oracle baseline: `invariant_risk_selection`.
- Combined-stress success: proposed `0.674 +/- 0.008` vs baseline `0.570 +/- 0.009`.
- Paired difference: `0.105 +/- 0.008`, wins `7/7` seeds.
- Causal-mechanism recall delta: `+0.087`.
- Spurious-dependence delta: `-0.117`.
- Tail-failure delta: `-0.037`; damage delta: `-0.026`; selection-cost delta: `-0.026`.
- Best ablation gap: `0.036`.

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
