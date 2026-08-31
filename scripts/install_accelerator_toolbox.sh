#!/usr/bin/env bash
# ==============================================================================
# install_accelerator_toolbox.sh
# Build and install accelerator-toolbox (pyAT) with custom NKM extensions.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PATCH_FILE="${REPO_ROOT}/patches/accelerator_toolbox_nkm.patch"
EXTENSIONS_DIR="${REPO_ROOT}/patches/pyat_extensions"

DEFAULT_AT_DIR="/home/cspark/Work/simulation_codes-working/accelerator_toolbox"
AT_DIR="${1:-${DEFAULT_AT_DIR}}"

echo "========================================================================"
echo " Accelerator Toolbox (pyAT) with NKM Custom Extensions Installer"
echo "========================================================================"
echo " Accelerator Toolbox Directory: ${AT_DIR}"
echo " Patch File                   : ${PATCH_FILE}"
echo "------------------------------------------------------------------------"

# 1. Clone repository if missing
if [ ! -d "${AT_DIR}" ]; then
  echo "Target directory '${AT_DIR}' does not exist."
  read -rp "Clone accelerator-toolbox from GitHub? (y/N): " CONFIRM
  if [[ "${CONFIRM}" =~ ^[Yy]$ ]]; then
    mkdir -p "$(dirname "${AT_DIR}")"
    git clone https://github.com/atcollab/accelerator-toolbox.git "${AT_DIR}"
    echo "Cloned accelerator-toolbox."
  else
    echo "Aborted."
    exit 1
  fi
fi

# 2. Apply extensions/patch
cd "${AT_DIR}"
echo "[1/3] Applying custom NKM extensions..."

# Copy extension files directly
if [ -d "${EXTENSIONS_DIR}" ]; then
  cp -r "${EXTENSIONS_DIR}/"* "${AT_DIR}/"
  echo "  Copied standalone extension files to ${AT_DIR}"
fi

# Ensure imports are registered in pyat/at/integrators/__init__.py and pyat/at/lattice/elements/__init__.py
if ! grep -q "pyNKMPass" "${AT_DIR}/pyat/at/integrators/__init__.py"; then
  echo "from .pyNKMPass import *" >> "${AT_DIR}/pyat/at/integrators/__init__.py"
fi

if ! grep -q "nonlinear_kicker" "${AT_DIR}/pyat/at/lattice/elements/__init__.py"; then
  echo "from .nonlinear_kicker import *" >> "${AT_DIR}/pyat/at/lattice/elements/__init__.py"
fi

# 3. Build and install accelerator-toolbox in editable mode
echo "[2/3] Installing accelerator-toolbox in editable mode..."
cd "${AT_DIR}"

python3 -m pip install --upgrade pip setuptools wheel
if pip install --config-settings openmp=1 --config-settings omp_particle_threshold=4 -e . ; then
  echo "  pyAT installed successfully with OpenMP enabled."
else
  echo "  Warning: OpenMP build failed; falling back to standard editable install..."
  pip install -e .
fi

# 4. Verify installation
echo "[3/3] Verifying accelerator-toolbox and NKM extensions..."
python3 -c "
import at
from at.integrators import pyNKMPass
from at.lattice.elements import NonlinearKicker
print('✓ Successfully verified pyAT version:', at.__version__)
print('✓ Custom NonlinearKicker element and pyNKMPass loaded successfully.')
"

echo "========================================================================"
echo " Accelerator Toolbox installation completed successfully."
echo "========================================================================"
