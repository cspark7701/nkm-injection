#!/usr/bin/env bash
# ==============================================================================
# check_github_actions.sh — Pre-push GitHub Actions Local Validation Runner
# NKM & BTS Transfer Line Physics Simulation Framework (4GSR)
#
# Usage:
#   ./scripts/check_github_actions.sh [OPTIONS]
#
# Options:
#   -w, --workflow W    Validate specific workflow ('ci', 'paper', 'release', or 'all'; default: 'all').
#   -f, --fast          Fast mode: validate syntax, hashes, and quick paper regression without full 199 tests.
#   -q, --quiet         Quiet mode: minimize output.
#   -d, --dry-run       Dry-run mode: print actions that would be executed without running commands.
#   -h, --help          Show this help message.
# ==============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

WORKFLOW_TARGET="all"
FAST_MODE=false
QUIET=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -w|--workflow)
            WORKFLOW_TARGET="$2"
            shift 2
            ;;
        -f|--fast)
            FAST_MODE=true
            shift
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            cat << 'HLP'
Usage: ./scripts/check_github_actions.sh [OPTIONS]

Locally validates all GitHub Actions workflow requirements and commands
prior to pushing to remote, preventing broken builds and ensuring compliance
with local repository policies (100% local, no remote API calls).

Options:
  -w, --workflow W   Select workflow to simulate/validate:
                     'all'     : Validate all workflows (ci, paper, release) [default]
                     'ci'      : Run steps from .github/workflows/ci.yml
                     'paper'   : Run steps from .github/workflows/paper-regression.yml
                     'release' : Run steps from .github/workflows/release-zenodo.yml
  -f, --fast         Fast mode (skips long full test suite, runs syntax + paper tests).
  -q, --quiet        Quiet mode: suppress detailed progress output.
  -d, --dry-run      Print validation steps without executing commands.
  -h, --help         Show this help message.
HLP
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Run './scripts/check_github_actions.sh --help' for usage details." >&2
            exit 1
            ;;
    esac
done

echo "======================================================================"
echo "          GitHub Actions Pre-Push Local Validation Suite              "
echo "======================================================================"
echo " Repository Root   : ${REPO_ROOT}"
echo " Target Workflow   : ${WORKFLOW_TARGET}"
echo " Fast Mode         : ${FAST_MODE}"
echo " Dry Run Mode      : ${DRY_RUN}"
echo "======================================================================"

run_check() {
    local title="$1"
    shift
    local cmd=("$@")

    echo ""
    echo "----------------------------------------------------------------------"
    echo " [CHECK] ${title}"
    echo " Command: ${cmd[*]}"
    echo "----------------------------------------------------------------------"

    if [ "${DRY_RUN}" = true ]; then
        echo " [DRY-RUN] Command skipped."
        return 0
    fi

    if [ "${QUIET}" = true ]; then
        "${cmd[@]}" > /dev/null 2>&1
    else
        "${cmd[@]}"
    fi
    echo " [PASSED] ${title}"
}

# ------------------------------------------------------------------------------
# STEP 0: Workflow YAML Syntax & Structure Linting
# ------------------------------------------------------------------------------
run_check "YAML Syntax & Schema Validation (.github/workflows/*.yml)" \
    python3 -c "
import yaml
from pathlib import Path
workflows = list(Path('.github/workflows').glob('*.yml'))
assert len(workflows) > 0, 'No workflow files found!'
for wf in workflows:
    with open(wf, 'r') as f:
        data = yaml.safe_load(f)
        assert 'name' in data, f'Workflow {wf} missing name'
        assert 'jobs' in data, f'Workflow {wf} missing jobs'
    print(f'  [OK] Valid YAML: {wf.name} ({len(data[\"jobs\"])} job(s))')
"

# ------------------------------------------------------------------------------
# STEP 1: Protected Scientific Source Data Integrity
# ------------------------------------------------------------------------------
run_check "Protected Input Cryptographic Hashes (inventory_protected_hashes.py)" \
    python3 scripts/inventory_protected_hashes.py

run_check "Cryptographic Hashes Verification via schema" \
    python3 -c "
from pathlib import Path
from src.nkm_injection.results_schema import compute_input_data_hashes
hashes = compute_input_data_hashes(Path('.'))
for name, h in hashes.items():
    assert h != 'MISSING', f'Protected file missing: {name}'
    print(f'  [OK] {name:25s}: {h[:16]}...')
"

# ------------------------------------------------------------------------------
# STEP 2: Baseline Metrics Generation (from ci.yml)
# ------------------------------------------------------------------------------
if [[ "${WORKFLOW_TARGET}" == "all" || "${WORKFLOW_TARGET}" == "ci" ]]; then
    run_check "Generate Baseline Metrics (ci.yml)" \
        python3 scripts/record_baseline_metrics.py
fi

# ------------------------------------------------------------------------------
# STEP 3: Paper Reproduction Pipeline (from paper-regression.yml & release-zenodo.yml)
# ------------------------------------------------------------------------------
if [[ "${WORKFLOW_TARGET}" == "all" || "${WORKFLOW_TARGET}" == "paper" || "${WORKFLOW_TARGET}" == "release" ]]; then
    run_check "Run Paper Reproduction Pipeline (reproduce_paper.py)" \
        python3 scripts/reproduce_paper.py --no-pdf
fi

# ------------------------------------------------------------------------------
# STEP 4: Test Suite Validation
# ------------------------------------------------------------------------------
if [ "${FAST_MODE}" = true ]; then
    run_check "Paper Regression Tests [Fast Mode] (test_paper_regression.py)" \
        pytest -v tests/test_paper_regression.py
else
    if [[ "${WORKFLOW_TARGET}" == "paper" ]]; then
        run_check "Paper Regression Test Suite (test_paper_regression.py)" \
            pytest -v tests/test_paper_regression.py
    else
        run_check "Full Pytest Suite (ci.yml / release-zenodo.yml)" \
            pytest -v
    fi
fi

# ------------------------------------------------------------------------------
# STEP 5: Protected Files Invariant Safeguard
# ------------------------------------------------------------------------------
run_check "Post-Execution Protected Files Immutability Verification" \
    python3 -c "
from pathlib import Path
from src.nkm_injection.results_schema import compute_input_data_hashes
import json

manifest_path = Path('results/baseline/protected_files_manifest.json')
with open(manifest_path, 'r') as f:
    expected = json.load(f)

current = compute_input_data_hashes(Path('.'))
for fname, exp_hash in expected.items():
    if fname in current:
        assert current[fname] == exp_hash, f'Protected file modified: {fname}'
print('  [OK] All protected scientific files remain unmodified and intact.')
"

echo ""
echo "======================================================================"
echo "  All GitHub Actions Pre-Push Local Validations Passed Successfully! "
echo "  Safe to commit and push according to local CI workflow definitions. "
echo "======================================================================"
