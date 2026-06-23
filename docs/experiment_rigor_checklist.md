# Experiment Rigor Checklist

- [x] Frozen plan written before final v5 reporting.
- [x] Strongest old method retained as `proposed_causal_mechanism_selector_v4`.
- [x] Multiple strong baselines included: active, core-set, influence, invariant, domain-adversarial, counterfactual, conformal, offline-RL value, foundation embedding, v4, and oracle.
- [x] Hard aggregate separated from easy source-matched rows.
- [x] Paired seed testing over 10 hard seeds.
- [x] Ablations over 10 method variants.
- [x] Stress sweep over six stress axes and ten levels.
- [x] Fixed-risk audit with strict risk budget `0.10`.
- [x] Failure-case ledger with 24 named boundaries.
- [x] All predefined local gates reported honestly.
- [x] Scope gate reported as failed.
- [x] Validator checks row counts, gates, page count, PDF hash, citation settings, logs, and artifact placement.
