# Package imports and entry points

Install the package into the same Python environment used by scripts, pytest and
Jupyter. The canonical import is `nkm_injection`; `src` is a source directory,
not part of the installed package name.

```bash
# From the checkout, using the active environment's interpreter:
python -m pip install -e '.[dev,moga]'
python -m pytest -q
python scripts/run_multiturn_injection.py --help
nkm-production --dry-run --workers 4
```

Base installation does not require the optional MOGA dependency. Install the
`moga` extra when importing or running MOGA components. Use `python -m pip` to
keep installation and execution in the same environment.

```python
from nkm_injection import BTSConfig, SerializableConfigMixin
from nkm_injection.bts_lattice import create_bts_lattice
from nkm_injection.units import compute_rigidity
```

Maintained scripts, tests and notebooks use this name without modifying
`sys.path`. Scripts remain executable by path after installation, including
absolute script paths from outside the checkout. Their source-data location and
output-directory conventions remain those of the existing workflows.

## Installed production command

The installed `nkm-production` command calls the shared production runner. It is
available after either an editable or wheel installation:

```bash
nkm-production --help
nkm-production --repo-root /path/to/nkm-injection --dry-run --workers 4
```

The command defaults to the current directory as the source checkout. Use
`--repo-root` when running elsewhere. The existing checkout adapter,
`python /path/to/nkm-injection/scripts/run_production_simulation.py`, defaults to
its own checkout and accepts the same options. `--dry-run` validates and previews
stages without creating a run directory. Actual execution still requires the
checkout's scientific inputs and scripts; a wheel does not bundle these files.

For wheel installation, build/install in the desired environment and verify
outside the checkout:

```bash
python -m pip wheel --no-deps . --wheel-dir /tmp/nkm-wheels
python -m pip install /tmp/nkm-wheels/nkm_injection-0.2.0-py3-none-any.whl
cd /tmp
python -c 'from nkm_injection import BTSConfig; print(BTSConfig())'
nkm-production --repo-root /path/to/nkm-injection --dry-run
```

## Lazy public exports and compatibility

Existing package-root exports remain available and resolve to the same objects
as direct submodule imports. Importing the package alone loads no subsystems.
Units and configuration serialization can be imported without initializing
tracking, plotting, SciPy or optional MOGA. Requesting a specific physics or
plotting export loads that subsystem and its dependencies. `dir(nkm_injection)`
includes public exports; `from nkm_injection import *` intentionally requests all
exports and therefore needs all their dependencies.

Replace legacy `src.nkm_injection` imports with `nkm_injection` and restart any
existing Python/Jupyter processes. The legacy name raises an explicit import
error before loading submodules, preventing duplicate module and class
identities. Old pickle artifacts referencing the legacy module path are not
migrated by this change; reproduce needed artifacts from verified inputs or
export them in their original environment. Saved JSON structure is unchanged.

Select the installed environment as the Jupyter kernel. Notebook 01 retains its
working-directory setup for relative scientific input paths; notebooks 02–04
retain their existing source-root discovery. Only imports and import-path
bootstrapping changed. Notebook 03 remains independently importable with the
MOGA extra installed. Protected root notebooks are untouched.

This refactor changes no physics algorithms, interface units (m, rad, eV, T and
T m), seeds or numerical tolerances. Existing GeV/mm interfaces retain their
explicit conversions.
