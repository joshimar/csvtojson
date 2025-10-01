cat > README.md <<'EOF'
# csvtojson

Tiny, production-ready Python tool that converts a CSV (with headers) into JSON (list of records).
- Library API (importable functions)
- Simple CLI: `csv2json input.csv [-o out.json] [--no-infer] [--indent 0] [--ascii]`
- Tests + coverage, Docker image, and GitHub Actions CI

## Quick start (local)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[test]"
pytest -q
