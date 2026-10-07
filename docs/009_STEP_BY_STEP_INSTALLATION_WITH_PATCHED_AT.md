# Step-by-Step Installation Guide: `nkm-injection` with Patched `accelerator_toolbox`

This guide details how to create an isolated Python environment, install and patch the **Accelerator Toolbox (`accelerator-toolbox` / `pyAT`)** with custom Nonlinear Kicker Magnet (NKM) extensions, and install the **`nkm-injection`** simulation package.

---

## 1. Prerequisites

- **Operating System**: Linux (Ubuntu 20.04+ recommended) or macOS
- **C Compiler**: `gcc` / `g++` (for building pyAT C-extensions and OpenMP tracking)
- **Python**: Version 3.10 or 3.11
- **Package / Environment Manager**: Conda / Miniforge *(Recommended)* or Python `venv`

---

## 2. Step-by-Step Manual Installation

### Step 1: Clone the `nkm-injection` Repository

```bash
git clone https://github.com/cspark7701/nkm-injection.git
cd nkm-injection
```

---

### Step 2: Create & Activate the Python Environment

#### Option A: Using Conda / Miniforge *(Recommended)*
```bash
# Create a Python 3.11 environment
conda create -n nkm-env python=3.11 -y

# Activate the environment
conda activate nkm-env
```

#### Option B: Using Python `venv`
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Core Dependencies & Upgrade `pip`

```bash
python3 -m pip install --upgrade pip setuptools wheel
pip install -r requirements-lock.txt
```

---

### Step 4: Patch & Install `accelerator_toolbox` (`pyAT`)

The `nkm-injection` repository includes the unified patch ([`patches/accelerator_toolbox_nkm.patch`](../patches/accelerator_toolbox_nkm.patch)) and standalone extension files ([`patches/pyat_extensions/`](../patches/pyat_extensions/)) providing:
- `pyNKMPass`: Pure Python 3D/2D field map tracking pass-method
- `NonlinearKicker`: Custom element class inheriting `at.Element`

#### Method A: Automated Installer Script *(Recommended)*
```bash
# Provide the path to your local accelerator_toolbox repository:
./scripts/install_accelerator_toolbox.sh /home/cspark/Work/simulation_codes-working/accelerator_toolbox
```
*(If the folder does not exist, the script offers to clone it automatically).*

#### Method B: Manual Patching & Build
```bash
# 1. Navigate to your accelerator_toolbox source directory
cd /path/to/accelerator_toolbox

# 2. Copy the custom NKM extensions from nkm-injection
cp -r /path/to/nkm-injection/patches/pyat_extensions/* ./

# 3. Ensure imports are registered in pyAT
grep -q "pyNKMPass" pyat/at/integrators/__init__.py || echo "from .pyNKMPass import *" >> pyat/at/integrators/__init__.py
grep -q "nonlinear_kicker" pyat/at/lattice/elements/__init__.py || echo "from .nonlinear_kicker import *" >> pyat/at/lattice/elements/__init__.py

# 4. Build and install with OpenMP multiprocessing
pip install --config-settings openmp=1 --config-settings omp_particle_threshold=4 -e .
```

---

### Step 5: Install `nkm-injection` in Editable Mode

Return to the `nkm-injection` repository and install with development and optimization extras:

```bash
cd /path/to/nkm-injection
pip install -e .[dev,moga]
```

---

### Step 6: Verify the Installation

#### 1. Quick Python Verification
```bash
python3 -c "
import at
from at.integrators import pyNKMPass
from at.lattice.elements import NonlinearKicker
import nkm_injection

print('✓ pyAT version:', at.__version__)
print('✓ NonlinearKicker element loaded:', hasattr(at, 'NonlinearKicker'))
print('✓ nkm-injection version:', nkm_injection.__version__)
"
```

#### 2. Run Full Test Suite
```bash
pytest -v
```
*Expected result: **177 passed in ~1 minute**.*

---

## 3. Automated 1-Command Setup

For a fully automated installation that sets up the environment, patches `accelerator-toolbox`, installs `nkm-injection`, and runs the test suite in a single command:

```bash
./scripts/setup_environment.sh
```

---

## 4. Next Steps & Simulation Workflows

- **Run Single-Command Paper Reproduction**:
  ```bash
  python3 scripts/reproduce_paper.py --manifest config/publication_manifest.json -w 4
  ```

- **Run Jupyter Simulation Notebooks**:
  ```bash
  jupyter notebook notebooks/01_bts_main_simulation.ipynb
  ```
