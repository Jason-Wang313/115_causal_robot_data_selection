# Paper 115 Rebuild Plan

Started: 2026-06-15 03:02:00 +0100

## Goal

Rebuild `causal_robot_data_selection` from an archive memo into a real local empirical submission package. The paper must test whether selecting robot training data to separate causal mechanisms improves downstream policy robustness compared with label balancing, uncertainty mining, diversity, failure mining, and influence-style selection.

## Claim To Test

Robot data selection should prioritize interventions that identify action-critical causal mechanisms rather than examples that merely balance labels or maximize prediction uncertainty. A causal mechanism selector should improve downstream task success under spurious-correlation and mechanism-shift stress while reducing tail failures and redundant collection cost.

## Evidence Design

- Benchmark dimensions: 5 robot skill families, 7 causal/spurious shift regimes, 5 selection budgets/splits, 9 selectors, 7 paired seeds, 84 rollout episodes per group.
- Methods: random selection, label-balanced selection, diversity core-set, failure mining, uncertainty active selection, influence selection, invariant-risk selection, proposed causal mechanism selector, and oracle interventional selector.
- Metrics: downstream success, causal mechanism recall, spurious-dependence rate, tail failure rate, damage rate, selection cost, calibration error, and paired-seed wins.
- Stress sweep: increasing spurious correlation between observed features and the true causal mechanism.
- Ablations: remove intervention score, remove mechanism coverage, remove spurious-confound penalty, remove tail-failure objective, remove cost constraint, and classifier-only selection.

## Terminal Gates

The paper may become `STRONG_REVISE` only if all gates clear against the strongest non-oracle baseline:

- Combined-stress downstream success margin is at least 0.030.
- Causal mechanism recall increases by at least 0.030.
- Spurious-dependence rate decreases by at least 0.020.
- Tail failure and damage do not increase.
- Selection cost does not increase.
- Paired-seed success wins are at least 5/7.
- Best ablation trails the full method by at least 0.020.

If any gate fails, the terminal decision remains `KILL_ARCHIVE` with the negative result documented.

## Execution Steps

1. Replace the generic branch scaffold with a causal robot data-selection benchmark.
2. Generate raw per-seed/task/regime/split evidence, aggregate metrics, pairwise tests, stress-sweep outputs, ablation tables, and failure cases.
3. Remove stale branch-template artifacts if superseded.
4. Rewrite README, status docs, novelty docs, attack logs, reproducibility docs, and final audit around the v4 evidence.
5. Rewrite the manuscript as an ICLR-style evidence report with honest limitations.
6. Compile the PDF and copy `115.pdf` to Downloads only.
7. Audit Python, LaTeX, CSV finiteness, stale outputs, Git status, Downloads-only PDF placement, and GitHub visibility.
8. Update root reports only after Paper 115 reaches a terminal decision.
