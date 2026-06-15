# Paper 115 Terminal Audit - 2026-06-15

Paper: `causal_robot_data_selection`

Terminal state: STRONG_REVISE

ICLR main ready: no

## What Passed

- Code compiled with `python -m py_compile src\run_experiment.py`.
- Experiment reran successfully under low-RAM thread caps.
- All expected CSV row counts passed.
- Numeric audit found no NaN or infinite values.
- Proposed method beats the strongest non-oracle baseline under combined stress.
- Proposed method wins 7/7 paired seeds over the strongest non-oracle baseline.
- Causal-mechanism recall improves.
- Spurious dependence, tail failure, damage, and selection cost decrease.
- Core ablations remain below the full method.
- Stress evidence now includes 5,880 task/regime/seed rows.
- Failure-case documentation now includes 8 concrete boundaries.
- Canonical PDF exists at `C:/Users/wangz/Downloads/115.pdf`.
- PDF SHA256 is `D8953A338C245EC65F6103ED57468C873DF2AAB5A9F696870EA0E41142624E93`.
- PDF size is `394835` bytes.
- No copy exists at `C:/Users/wangz/Desktop/115.pdf`.
- LaTeX/BibTeX scan is clean except benign `rerunfilecheck`; BibTeX reports `warning$ -- 0`.

## What Did Not Pass

- No real robot validation.
- No external high-fidelity simulator benchmark.
- No selected dataset or trained policy checkpoint release.
- No hardware videos or qualitative rollouts.
- Related work still needs manual full-paper synthesis.

## Decision

Mark as `STRONG_REVISE`. Do not claim ICLR-main submission readiness until real robot or independent high-fidelity validation gates are satisfied.
