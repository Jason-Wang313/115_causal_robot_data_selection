# Claims

- Mechanism claim: robot data selection should identify action-critical causal mechanisms, not merely balance labels, maximize uncertainty, diversify embeddings, or mine frequent failures.
- Method claim: `interventional_mechanism_value_selector_v5` selects data by interventional contrast, mechanism coverage, spurious-dependence suppression, tail-failure value, and budgeted deployment utility.
- Evidence claim: on the frozen local hard slice, v5 beats `proposed_causal_mechanism_selector_v4` with success `0.69673` vs `0.60831`, utility `0.63641` vs `0.45486`, causal-recall delta `+0.08002`, spurious-dependence delta `-0.06968`, tail-failure delta `-0.02340`, damage delta `-0.01624`, cost delta `-0.02115`, regret delta `-0.04237`, and `10/10` paired hard-utility seed wins.
- Robustness claim: ablation, stress endpoint, and fixed-risk gates pass; strict fixed-risk coverage is `0.55813` with zero breach and utility margin `0.20267`.
- Scope claim: the work is `STRONG_REVISE`, not ICLR-main ready.
- Unsupported claim explicitly avoided: no claim of real-robot SOTA, deployed data-engine readiness, or universal dataset curation.
