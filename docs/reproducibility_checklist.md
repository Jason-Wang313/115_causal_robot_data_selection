# Reproducibility Checklist

## Commands

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py scripts\generate_manuscript.py scripts\validate_submission_artifacts.py
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

## Expected Output

- `results/summary.json` has `version = v5_expanded`.
- `terminal_decision = STRONG_REVISE`.
- `local_gates_pass = true`.
- `scope_gate_pass = false`.
- `paper/main.pdf` and `C:/Users/wangz/Downloads/115.pdf` have identical SHA256 `718DE79DFE5AE2991958D6C2C43EE6CD3273C5BE34EFC4331C1E721E2AB3B4C4`.
- `C:/Users/wangz/Desktop/115.pdf` must be absent.
