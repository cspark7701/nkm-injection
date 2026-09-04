#!/usr/bin/env bash
# ==============================================================================
# cleanup.sh — Clean simulation outputs and temporary generated artifacts
# NKM & BTS Transfer Line Physics Simulation Framework (4GSR)
#
# Usage:
#   ./scripts/cleanup.sh [OPTIONS]
#
# Options:
#   -a, --all         Clean all simulation outputs including results/ runs,
#                     caches, root generated files, and LaTeX aux files.
#   -r, --results     Clean simulation run directories under results/ (preserves baseline/).
#   -c, --cache       Clean Python bytecodes (__pycache__, *.pyc) and .pytest_cache.
#   -d, --dry-run     Show what files/directories would be deleted without deleting.
#   -y, --yes         Skip interactive confirmation prompt.
#   -h, --help        Show this help message.
# ==============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

DRY_RUN=false
ASSUME_YES=false
CLEAN_ALL=false
CLEAN_RESULTS=false
CLEAN_CACHE=false

# Immutable and protected scientific source data files that must NEVER be deleted
PROTECTED_FILES=(
    "By.txt"
    "kickmap_file.txt"
    "K4GSR_HBIv4-1.mat"
    "nkm_field.xlsx"
    "nkm_field_expanded.xlsx"
    "nlk.py"
    "NKM_radia.ipynb"
    "NKM_radia_y=0.ipynb"
    "storage_ring.ipynb"
)

# Parse command line flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        -a|--all)
            CLEAN_ALL=true
            shift
            ;;
        -r|--results)
            CLEAN_RESULTS=true
            shift
            ;;
        -c|--cache)
            CLEAN_CACHE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -y|--yes)
            ASSUME_YES=true
            shift
            ;;
        -h|--help)
            cat << 'HLP'
Usage: ./scripts/cleanup.sh [OPTIONS]

Clean simulation outputs, caches, and temporary artifacts while strictly
preserving protected scientific source data (By.txt, kickmap_file.txt,
K4GSR_HBIv4-1.mat, etc.) and baseline validation manifests.

Options:
  -a, --all        Clean all generated simulation outputs, caches, root
                   temporary files, and LaTeX build artifacts.
  -r, --results    Clean simulation runs under results/ (preserves results/baseline/).
  -c, --cache      Clean __pycache__, *.pyc, *.pyo, and .pytest_cache/.
  -d, --dry-run    Show files and directories to be removed without deleting.
  -y, --yes        Execute without prompting for confirmation.
  -h, --help       Show this help message.

Default (no flags): Equivalent to --results.
HLP
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Run './scripts/cleanup.sh --help' for usage details." >&2
            exit 1
            ;;
    esac
done

# Default behavior if neither --all, --results, nor --cache is explicitly passed
if [ "${CLEAN_ALL}" = false ] && [ "${CLEAN_RESULTS}" = false ] && [ "${CLEAN_CACHE}" = false ]; then
    CLEAN_RESULTS=true
fi

# If --all is passed, enable both results and cache cleanup
if [ "${CLEAN_ALL}" = true ]; then
    CLEAN_RESULTS=true
    CLEAN_CACHE=true
fi

echo "======================================================================"
echo "                   NKM Output Cleanup Utility                         "
echo "======================================================================"
echo " Repository Root : ${REPO_ROOT}"
echo " Dry Run Mode    : ${DRY_RUN}"
echo " Clean Results   : ${CLEAN_RESULTS}"
echo " Clean Caches    : ${CLEAN_CACHE}"
echo " Clean All       : ${CLEAN_ALL}"
echo "======================================================================"

TARGET_PATHS=()

# 1. Gather simulation outputs under results/ (preserving results/baseline)
if [ "${CLEAN_RESULTS}" = true ] && [ -d "results" ]; then
    while IFS= read -r dir_entry; do
        bname="$(basename "${dir_entry}")"
        # Protect baseline/ reference directory
        if [ "${bname}" != "baseline" ]; then
            TARGET_PATHS+=("${dir_entry}")
        fi
    done < <(find results -mindepth 1 -maxdepth 1 -type d)
fi

# 2. Gather untracked simulation outputs in repo root if --all or --results is selected
UNTRACKED_ROOT_OUTPUTS=(
    "storage_ring_lattice_nkm.mat"
    "storage_ring_lattice_after_nkm.mat"
    "acceptance.npy"
    "field_map.npy"
)

for f in "${UNTRACKED_ROOT_OUTPUTS[@]}"; do
    if [ -e "${f}" ]; then
        TARGET_PATHS+=("${f}")
    fi
done

# Also find any *.pkl in repo root (optimizer temporary files)
while IFS= read -r pkl_file; do
    if [ -e "${pkl_file}" ]; then
        TARGET_PATHS+=("${pkl_file}")
    fi
done < <(find . -maxdepth 1 -name "*.pkl")

# 3. Gather caches if --cache or --all is requested
if [ "${CLEAN_CACHE}" = true ]; then
    while IFS= read -r cache_entry; do
        TARGET_PATHS+=("${cache_entry}")
    done < <(find . -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".ipynb_checkpoints" \))
fi

# 4. Gather LaTeX auxiliary build artifacts if --all is requested
if [ "${CLEAN_ALL}" = true ] && [ -d "docs/jinst-paper" ]; then
    while IFS= read -r aux_file; do
        TARGET_PATHS+=("${aux_file}")
    done < <(find docs/jinst-paper -type f \( -name "*.aux" -o -name "*.log" -o -name "*.bbl" -o -name "*.blg" -o -name "*.out" -o -name "*.toc" \))
fi

# Deduplicate and filter targets
UNIQUE_TARGETS=()
if [ ${#TARGET_PATHS[@]} -gt 0 ]; then
    while IFS= read -r line; do
        [ -n "${line}" ] && UNIQUE_TARGETS+=("${line}")
    done < <(printf '%s\n' "${TARGET_PATHS[@]}" | sort -u)
fi

if [ ${#UNIQUE_TARGETS[@]} -eq 0 ]; then
    echo "No matching output folders or temporary files found to clean."
    exit 0
fi

# Integrity Guard: Assert that NO protected scientific file is in deletion list
for target in "${UNIQUE_TARGETS[@]}"; do
    target_rel="${target#./}"
    for protected in "${PROTECTED_FILES[@]}"; do
        if [ "${target_rel}" = "${protected}" ]; then
            echo "[CRITICAL ERROR] Protected scientific file matched for deletion: ${target_rel}" >&2
            echo "Aborting cleanup immediately." >&2
            exit 1
        fi
    done
    if [ "${target_rel}" = "results/baseline" ] || [[ "${target_rel}" =~ ^results/baseline/.* ]]; then
        echo "[CRITICAL ERROR] results/baseline matched for deletion: ${target_rel}" >&2
        echo "Aborting cleanup immediately." >&2
        exit 1
    fi
done

echo ""
echo "Identified ${#UNIQUE_TARGETS[@]} target path(s) for cleanup:"
for t in "${UNIQUE_TARGETS[@]}"; do
    if [ -d "${t}" ]; then
        echo "  [DIR]  ${t}"
    else
        echo "  [FILE] ${t}"
    fi
done
echo ""

if [ "${DRY_RUN}" = true ]; then
    echo "[DRY-RUN] No files or directories were deleted."
    exit 0
fi

# Prompt confirmation unless -y/--yes is provided
if [ "${ASSUME_YES}" = false ]; then
    read -r -p "Are you sure you want to delete these output paths? [y/N] " response
    case "${response}" in
        [yY][eE][sS]|[yY])
            ;;
        *)
            echo "Cleanup aborted by user."
            exit 0
            ;;
    esac
fi

# Perform deletion
for t in "${UNIQUE_TARGETS[@]}"; do
    if [ -e "${t}" ]; then
        rm -rf "${t}"
        echo "Removed: ${t}"
    fi
done

echo ""
echo "Cleanup completed successfully."
