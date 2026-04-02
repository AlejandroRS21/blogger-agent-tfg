# Quickstart

```bash
cd backend
source .venv/bin/activate
uv pip install -e ".[dev]"  # ensure pytest is ready

# Unit tests only
pytest -m "not integration"
# OR using the new runner:
python tests/run_tests.py --suite unit
```
