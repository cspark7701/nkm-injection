# Milestone 116 — Repair failing GitHub CI test collection

Completed: 2026-10-09.

**Failure.** CI Workflow runs 37903432176 and 37906103392 (main, 2026-10-09) failed in "Run Pytest Suite" on Python
3.10 and 3.11 with 5 collection errors (`ModuleNotFoundError: scripts`, `patches`, `nlk`) in test_baseline,
test_fieldmap, test_fieldmap_contracts, test_nkm_cross_validation and test_optimization_handoff. The baseline step passed
because it used `python -m pytest`, which puts the working directory on `sys.path`; the suite step used the bare
`pytest` entry point, which does not. Local checks always used `python -m pytest`, so they did not reproduce it.

**Fix.** `pyproject.toml` `[tool.pytest.ini_options] pythonpath = ["."]`; all workflows call `python -m pytest`;
`actions/checkout@v5` and `actions/setup-python@v6` (Node 24, removes the Node 20 deprecation warning). Paper
Regression already passed and is unchanged except for the same command/action updates.

**Verification** (clean clone, fresh conda Python 3.10.x and 3.11.x, `pip install -e .[dev,moga]` from PyPI, mirroring
the workflow steps): baseline 5 passed; bare `pytest` 651 passed on both versions; paper pipeline 3 passed; paper
regression 8 passed. Reverting only `pyproject.toml` reproduces the 5 collection errors. Not pushed; CI will rerun on the
author's next push.
