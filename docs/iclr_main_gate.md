# ICLR Main Gate

Paper: 115 causal_robot_data_selection

Existing v3 decision: KILL_ARCHIVE

v4 gate verdict: STRONG_REVISE

Evidence digest: causal-data-selection-local-v4

## Passed Local Gates

- Success margin over strongest non-oracle baseline: `0.105 >= 0.030`.
- Causal-recall delta: `0.087 >= 0.030`.
- Spurious-dependence delta: `-0.117 <= -0.020`.
- Tail-failure delta: `-0.037 <= 0`.
- Damage delta: `-0.026 <= 0`.
- Selection-cost delta: `-0.026 <= 0`.
- Paired-seed wins: `7/7 >= 5/7`.
- Ablation margin: `0.036 >= 0.020`.

## Remaining Main-Conference Blockers

- No real robot validation.
- No external high-fidelity simulator benchmark.
- No released selected datasets or policy checkpoints.
- Related work still needs manual full-paper synthesis.

The only honest main-conference-safe terminal state is STRONG_REVISE.
