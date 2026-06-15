# Child Status 115

Current stage: ICLR main gate terminal
Last update: 2026-06-15 19:58:38 +0100
PDF: C:/Users/wangz/Downloads/115.pdf
PDF SHA256: D8953A338C245EC65F6103ED57468C873DF2AAB5A9F696870EA0E41142624E93
PDF size: 394835 bytes
Desktop copy present: no
GitHub: https://github.com/Jason-Wang313/115_causal_robot_data_selection
Submission-hardening version: v4.1
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence digest:
- Proposed causal selector beats `invariant_risk_selection` by `0.105 +/- 0.008` combined-stress success with `7/7` paired-seed wins.
- Proposed success is `0.674 +/- 0.008`; strongest baseline success is `0.570 +/- 0.009`.
- Causal recall increases; spurious dependence, tail failure, damage, and selection cost decrease.
- Best ablation trails the full method by `0.036` success.
- Stress sweep now covers `5,880` task/regime/seed rows and `24` aggregate rows.
- Failure-case documentation now covers `8` causal-data-selection boundaries.
- Remaining blocker: no real robot or external high-fidelity benchmark validation.
