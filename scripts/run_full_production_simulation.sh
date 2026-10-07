#!/usr/bin/env bash
# Shell adapter; all configuration, preflight and stage routing live in Python.
# Set NKM_PYTHON to select an interpreter; otherwise use python3 from PATH.
set -euo pipefail
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
exec "${NKM_PYTHON:-python3}" -B "${REPO_ROOT}/scripts/run_production_simulation.py" "$@"
