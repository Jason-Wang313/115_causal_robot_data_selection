# Submission Attack Log

Paper: 115 causal_robot_data_selection

This v4.1 pass replaces the v3 archive decision with a local empirical rebuild and expanded continuation audit. The result is `STRONG_REVISE`, not final ICLR-main readiness.

## Attack 1: No real robot validation.

Verdict: Still a blocker for readiness.

Action: Preserve `ICLR main ready: no`.

## Attack 2: Generic active learning novelty.

Verdict: Addressed locally.

Action: Reframed around action-critical causal mechanism selection for robot control.

## Attack 3: Weak baselines.

Verdict: Addressed locally.

Action: Added label balancing, diversity, failure mining, uncertainty active selection, influence selection, invariant-risk selection, and oracle intervention selection.

## Attack 4: Invariant risk may be enough.

Verdict: Addressed locally.

Action: Proposed beats invariant-risk selection by `0.105 +/- 0.008`, wins `7/7` seeds, and improves causal/spurious/tail diagnostics.

## Attack 5: Components may be unnecessary.

Verdict: Addressed locally.

Action: Best ablation trails the full method by `0.036`, clearing the `0.020` gate.

## Attack 6: Missing selected dataset and checkpoints.

Verdict: Still a blocker for readiness.

Action: Document as required next evidence.

## Attack 7: Main-conference decision.

Verdict: STRONG_REVISE.

Action: Keep and expand; do not mark as submission-ready.

## Attack 8: Stress/failure coverage is thin.

Verdict: Addressed locally in v4.1.

Action: Expanded stress evidence to `5,880` task/regime/seed rows and failure documentation to `8` concrete causal-data-selection boundaries.
