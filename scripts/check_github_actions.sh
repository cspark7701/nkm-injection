#!/usr/bin/env bash
# Local workflow validation; never contacts GitHub or requires historical results.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"
PYTHON="${NKM_PYTHON:-python3}"
WORKFLOW_TARGET=all
FAST_MODE=false
QUIET=false
DRY_RUN=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        -w|--workflow)
            [[ $# -ge 2 ]] || { echo 'Missing workflow value' >&2; exit 1; }
            WORKFLOW_TARGET="$2"; shift 2 ;;
        -f|--fast) FAST_MODE=true; shift ;;
        -q|--quiet) QUIET=true; shift ;;
        -d|--dry-run) DRY_RUN=true; shift ;;
        -h|--help)
            cat <<'HLP'
Usage: ./scripts/check_github_actions.sh [OPTIONS]
Validate workflow commands locally using temporary test artifacts.
  -w, --workflow W  all, ci, paper or release (default: all)
  -f, --fast        Skip the full suite; keep paper integration and physics regressions
  -q, --quiet       Save command output; print diagnostics on failure
  -d, --dry-run     Print commands without executing or creating artifacts
  -h, --help        Show help
Set NKM_PYTHON to the interpreter with the project and dev/moga dependencies installed.
Publication checks use synthetic complete test bundles, not production evidence.
HLP
            exit 0 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done
case "$WORKFLOW_TARGET" in
    all|ci|paper|release) ;;
    *) echo "Invalid workflow: $WORKFLOW_TARGET" >&2; exit 1 ;;
esac
export PYTHONDONTWRITEBYTECODE=1
export MPLBACKEND=Agg
if [[ "$DRY_RUN" == true ]]; then
    CHECK_DIR="${TMPDIR:-/tmp}/nkm-local-actions-DRY_RUN"
else
    CHECK_DIR=$(mktemp -d "${TMPDIR:-/tmp}/nkm-local-actions.XXXXXXXX")
    cleanup() {
        local code=$?
        if [[ "$code" == 0 ]]; then
            rm -rf -- "$CHECK_DIR"
        else
            echo "[ERROR] Local check failed; diagnostics retained in $CHECK_DIR" >&2
        fi
    }
    trap cleanup EXIT
fi
CHECK_NUMBER=0
run_check() {
    local title="$1"
    shift
    CHECK_NUMBER=$((CHECK_NUMBER + 1))
    echo "[CHECK] $title"
    printf ' Command:'
    printf ' %q' "$@"
    printf '\n'
    if [[ "$DRY_RUN" == true ]]; then
        return
    fi
    local log="$CHECK_DIR/check_${CHECK_NUMBER}.log"
    if "$@" > "$log" 2>&1; then
        if [[ "$QUIET" == false ]]; then cat "$log"; fi
        echo "[PASSED] $title"
    else
        cat "$log" >&2
        return 1
    fi
}
run_check 'Workflow YAML syntax and structure' "$PYTHON" -B -c '
import yaml
from pathlib import Path
workflows = sorted(Path(".github/workflows").glob("*.yml"))
assert workflows, "No workflow files found"
for path in workflows:
    data = yaml.safe_load(path.read_text())
    assert "name" in data and "jobs" in data, f"Invalid workflow: {path}"
    print(f"[OK] {path.name}")
'
run_check 'Temporary protected input inventory' "$PYTHON" -B \
    scripts/inventory_protected_hashes.py --output-dir "$CHECK_DIR/inputs"
run_check 'Versioned scientific hash verification' "$PYTHON" -B -c '
import json
from pathlib import Path
from nkm_injection.results_schema import compute_input_data_hashes
expected = json.loads(Path("config/publication_input_hashes.json").read_text())
assert compute_input_data_hashes(Path.cwd()) == expected, "Scientific input hashes differ"
'
if [[ "$WORKFLOW_TARGET" == all || "$WORKFLOW_TARGET" == ci ]]; then
    run_check 'Isolated baseline metrics and integrity regressions' "$PYTHON" -B -m pytest \
        -q tests/test_baseline.py -o "cache_dir=$CHECK_DIR/pytest_cache" --basetemp "$CHECK_DIR/baseline_tests"
fi
if [[ "$WORKFLOW_TARGET" != ci ]]; then
    run_check 'Paper pipeline and CLI with complete temporary manifests' "$PYTHON" -B -m pytest \
        -q tests/test_publication_inputs.py::test_pipeline_in_fresh_python_process \
        tests/test_publication_validation_build.py::test_explicit_complete_baseline_override_generates_paper \
        -o "cache_dir=$CHECK_DIR/pytest_cache" --basetemp "$CHECK_DIR/paper_tests"
fi
if [[ "$FAST_MODE" == true || "$WORKFLOW_TARGET" == paper ]]; then
    run_check 'Paper physics regression suite' "$PYTHON" -B -m pytest \
        -q tests/test_paper_regression.py -o "cache_dir=$CHECK_DIR/pytest_cache" --basetemp "$CHECK_DIR/regression_tests"
else
    run_check 'Full regression suite' "$PYTHON" -B -m pytest \
        -q -o "cache_dir=$CHECK_DIR/pytest_cache" --basetemp "$CHECK_DIR/full_tests"
fi
run_check 'Post-check protected file immutability' "$PYTHON" -B -c '
import sys
from pathlib import Path
from scripts.inventory_protected_hashes import verify_hash_manifest
assert verify_hash_manifest(Path(sys.argv[1])), "Protected files changed during checks"
' "$CHECK_DIR/inputs/protected_files_manifest.json"
if [[ "$DRY_RUN" == true ]]; then
    echo '[DRY-RUN] All selected checks planned; no commands executed.'
else
    echo '[PASSED] All selected local workflow checks completed.'
fi
