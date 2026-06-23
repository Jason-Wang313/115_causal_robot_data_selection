# 115 Causal Robot Data Selection

Submission-hardening version: `v5_expanded`

Terminal decision: `STRONG_REVISE`

ICLR-main ready: `no`

Paper 115 has been rebuilt as a 25-page expanded local audit for causal robot data selection. The v5 method, `interventional_mechanism_value_selector_v5`, selects robot data by intervention contrast, action-critical mechanism coverage, spurious-dependence suppression, tail-failure value, and budgeted deployment utility.

The result is strong local evidence, not final submission readiness. The scope gate fails because there are no real robot data-selection rollouts, no accepted high-fidelity external validation, no released selected dataset or indices, no trained downstream policy checkpoint, no calibrated deployment logs, no rollout videos, and manual full-paper related-work synthesis remains incomplete.

## Evidence Snapshot

- Main evidence: 102,400 rollout-cell rows, 10,240 group rows, 1,280 seed-metric rows, 128 metric rows.
- Hard audit: 160 hard seed rows, 16 hard aggregate rows, 15 paired comparisons.
- Ablations: 8,000 rollout-cell rows, 100 ablation seed rows, 10 ablation metrics.
- Stress sweep: 48,000 rollout-cell rows, 600 stress seed rows, 60 stress metrics.
- Fixed risk: 51,200 rollout-cell rows, 320 fixed-risk seed rows, 32 fixed-risk metrics, 28 pairwise rows.
- Failure cases: 24 named boundary cases.
- Strongest non-oracle baseline: `proposed_causal_mechanism_selector_v4`.
- Hard success: v5 `0.69673` vs strongest baseline `0.60831`.
- Hard utility: v5 `0.63641` vs strongest baseline `0.45486`.
- Causal-recall delta: `+0.08002`.
- Spurious-dependence delta: `-0.06968`.
- Tail-failure delta: `-0.02340`.
- Damage delta: `-0.01624`.
- Selection-cost delta: `-0.02115`.
- Regret delta: `-0.04237`.
- Paired hard utility wins: `10/10`.
- Strict fixed-risk coverage: `0.55813`; breach: `0.00000`; utility margin: `0.20267`.

## Canonical Artifact

- PDF: `C:/Users/wangz/Downloads/115.pdf`
- SHA256: `718DE79DFE5AE2991958D6C2C43EE6CD3273C5BE34EFC4331C1E721E2AB3B4C4`
- Pages: 25
- Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.

## Reproduce

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item -LiteralPath paper\main.pdf -Destination "$HOME\Downloads\115.pdf" -Force
python scripts\validate_submission_artifacts.py
```
