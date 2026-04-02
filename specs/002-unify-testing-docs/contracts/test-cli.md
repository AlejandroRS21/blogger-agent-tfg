# CLI Contract: run_tests.py

This script acts as the unified facade over `pytest`.

```bash
# Run all unit tests
python backend/tests/run_tests.py --suite unit

# Run all integration tests (requires keys)
python backend/tests/run_tests.py --suite integration

# Run full project tests (default)
python backend/tests/run_tests.py --suite all
```
