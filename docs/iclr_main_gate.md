# ICLR Main Gate

Decision: `no`

The v5 local evidence passes all frozen empirical gates, but ICLR-main readiness fails.

## Local Gates

- Hard success margin >= 0.030: pass.
- Hard utility margin >= 0.050: pass.
- Causal recall delta >= 0.040: pass.
- Spurious dependence delta <= -0.020: pass.
- Tail failure, damage, selection cost, and regret non-increase: pass.
- Paired hard utility wins >= 8/10: pass with `10/10`.
- Ablation success and utility margins: pass.
- Stress endpoint success and utility margins: pass.
- Fixed-risk coverage positive, breach zero, utility margin positive: pass.

## Scope Gate Failures

- No real robot data-selection rollouts.
- No accepted high-fidelity data-selection simulation.
- No released selected dataset or indices.
- No trained downstream policy checkpoint.
- No calibrated collection or deployment logs.
- No rollout videos.
- Manual full-paper related-work synthesis remains incomplete.

Terminal state remains `STRONG_REVISE`.
