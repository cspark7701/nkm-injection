#!/usr/bin/env bash
# ==============================================================================
# Shell environment loader for nkm-injection (source it)
# ==============================================================================
# Usage:
#   source setup.sh                     Activate the conda environment 'pyat-dev'
#   NKM_INJECTION_ENV=NAME source setup.sh
#
# Exports PROJECT_ROOT and activates the conda environment when conda is available and
# the environment exists. The package itself is imported from the editable install
# (pip install -e .); this script does not modify the Python module search path.
# ==============================================================================

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "setup.sh must be sourced so its settings stay in your shell: source setup.sh" >&2
  exit 1
fi

_nkm_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PROJECT_ROOT="${_nkm_root}"

_nkm_env="${NKM_INJECTION_ENV:-pyat-dev}"
if command -v conda >/dev/null 2>&1; then
  if ! type conda 2>/dev/null | grep -q "function"; then
    eval "$(conda shell.bash hook 2>/dev/null)"  # enable 'conda activate' in this shell
  fi
  if conda env list 2>/dev/null | awk '{print $1}' | grep -qx "${_nkm_env}"; then
    conda activate "${_nkm_env}" || echo "[nkm-injection] WARNING: could not activate conda environment '${_nkm_env}'." >&2
  else
    echo "[nkm-injection] WARNING: conda environment '${_nkm_env}' not found; create it with" \
         "conda env create -f environment.yml -n ${_nkm_env} and install the package with pip install -e ." >&2
  fi
else
  echo "[nkm-injection] conda not found; using the current Python environment." >&2
fi

echo "[nkm-injection] Environment configured:"
echo "  PROJECT_ROOT:  ${PROJECT_ROOT}"
echo "  Python:        $(command -v python || echo 'not found')"
_nkm_pkg="$(python -c 'import nkm_injection, os; print(os.path.dirname(nkm_injection.__file__))' 2>/dev/null)"
if [[ -z "${_nkm_pkg}" ]]; then
  echo "[nkm-injection] WARNING: nkm_injection is not importable; install it with pip install -e ${_nkm_root}" >&2
elif [[ "${_nkm_pkg}" != "${_nkm_root}/src/nkm_injection" ]]; then
  echo "[nkm-injection] WARNING: nkm_injection is imported from ${_nkm_pkg}, not this checkout;" \
       "reinstall it with pip install -e ${_nkm_root}" >&2
else
  echo "  Package:       ${_nkm_pkg}"
fi
if [[ ":${PYTHONPATH:-}:" == *":${_nkm_root}/src:"* ]]; then
  echo "[nkm-injection] WARNING: PYTHONPATH contains ${_nkm_root}/src; remove it" \
       "so the installed package is the one imported." >&2
fi
unset _nkm_root _nkm_env _nkm_pkg
