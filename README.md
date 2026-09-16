# NKM-Injection — Nonlinear Kicker Magnet & BTS Optimization

Repository for studying the Nonlinear Kicker Magnet (NKM), Booster-to-Storage Ring (BTS) transfer line optics matching, off-axis beam injection, and reproducible publication generation.

> **Comprehensive Guide**: See [`docs/SIMULATION_PROCEDURE_AND_PUBLICATION_WORKFLOW.md`](docs/SIMULATION_PROCEDURE_AND_PUBLICATION_WORKFLOW.md) for the single-file complete specification of the simulation procedure and paper reproduction pipeline.

---

## Key Objectives

1. **BTS Optical Matching**: Optimize quad strengths and transport parameters for target injection optics.
2. **NKM Field Integration**: Ingest and validate 3D/2D magnetic field maps from RADIA calculations.
3. **Nonlinear Kick Modeling**: Calculate realistic non-uniform kicks for injected and circulating beams.
4. **Beam Capture & Transmission**: Quantify injected-beam capture efficiency while minimizing stored-beam perturbation.
5. **Robustness & Tolerance Analysis**: Evaluate performance sensitivity against alignment, field map, energy, and quad errors.
6. **Data-Driven Reproduction**: Dynamically generate publication figures and tables without hard-coded numbers.

---

## Visualization

Notebooks `01-03` include rich inline visualization cells, such as phase-space portraits, field maps, Pareto scatter matrices, hypervolume convergence plots, quad strength bars, and radar charts.

---

## Primary Workflows & Scripts

- **Authoritative Simulation Notebooks**: `notebooks/01_bts_main_simulation.ipynb`, `notebooks/02_multiturn_injection_validation.ipynb`, `notebooks/04_full_production_simulation.ipynb`
- **Optional MOGA Pareto Notebook**: `notebooks/03_bts_moga_pareto.ipynb`
- **Single-Command Manifest-Driven Paper Reproduction**: `python3 scripts/reproduce_paper.py --manifest config/publication_manifest.json -w W`

| Workflow Phase | Script Command | Description |
| :--- | :--- | :--- |
| **Field Validation** | `python3 scripts/validate_nkm_kick.py` | 5-way field/kick cross-validation. |
| **Tracking Convergence** | `python3 scripts/run_tracking_convergence.py` | $N_{\text{slices}}$ thick symplectic tracking convergence. |
| **Multi-Turn Injection Validation** | `notebooks/02_multiturn_injection_validation.ipynb` | Multi-Turn Injection Validation. |
| **Multi-Turn Injection** | `python3 scripts/run_multiturn_injection.py -w W` | Turn-by-turn capture efficiency & kicker models. |
| **Deterministic Opt** | `python3 scripts/optimize_bts_publication.py` | 2-stage SLSQP quad matching & SVD Jacobian analysis. |
| **Tolerance Budget** | `python3 scripts/run_publication_tolerances.py` | Monte Carlo robustness & OAT sensitivity rankings. |
| **MOGA Trade-offs** | `python3 scripts/run_bts_moga.py -w W` | Multi-seed NSGA-II Pareto optimization. |
| **Paper Reproduction** | `python3 scripts/reproduce_paper.py --manifest config/publication_manifest.json -w W` | Fully manifest-driven figure and table compilation. |

---

## Production Simulation Results & Key Findings

The complete 8-step production pipeline was executed (`results/production_run_20260915_175049/`), validating numerical convergence, capture performance, and optics feasibility across all physics subsystems:

| Simulation Phase | Key Benchmark & Parameters | Production Finding / Metric |
| :--- | :--- | :--- |
| **Field Validation** | Odd symmetry residual $B_y(z)$ | Residual $< 8.52 \times 10^{-12}\text{ T}$; Lorentz kick sign verified ($\Delta x' = -5.434\text{ mrad}$). |
| **Symplectic Slicing** | Convergence scan $N_{\text{slices}} \in \{10, \dots, 160\}$ | Trajectory converges to $< 10^{-6}\text{ mrad}$; $N_{\text{slices}} = 40$ established as production standard (100% survival). |
| **Multi-Turn Injection** | 1,000-turn tracking, 10,000 macro-particles, 5 seeds | **99.78% capture efficiency** [99.75%, 99.79% 95% CI] with only **$5.78\,\mu\text{m}$** stored beam disturbance ($>440\times$ lower than ideal kicker). |
| **Optics Optimization** | 2-stage deterministic SLSQP quadrupole matching | Exit mismatch $\mathcal{M}_{x,y} < 10^{-15}$; $\beta_{x,\max} = 30.23\text{ m}$, $\beta_{y,\max} = 44.52\text{ m}$ (satisfying $\le 60\text{ m}$ bounds). |
| **Tolerance Budget** | 100-sample Monte Carlo error budget | **100.0% feasible fraction** (0% failure probability); median mismatches $\mathcal{M}_x = 0.0014$, $\mathcal{M}_y = 0.0028$. |
| **MOGA Pareto Study** | 5 independent random seeds (NSGA-II) | 100.0% feasibility across all seeds; 27–40 Pareto front solutions per seed with consistent knee-point dispersion ($\sigma = 1.37\text{ m}^{-2}$). |
| **Paper Pipeline** | Dynamic publication compilation | Verified cryptographic hashes, compiled figures/tables, and generated [`docs/jinst-paper/paper.pdf`](docs/jinst-paper/paper.pdf). |

---

## Protected Scientific Source Data

The following source data and reference files are **immutable** and must not be reformatted, renamed, or modified:

- `NKM_radia.ipynb`, `NKM_radia_y=0.ipynb`
- `nlk.py`, `storage_ring.ipynb`
- Spreadsheet data (`*.xls`, `*.xlsx`, `*.xlsm`)
- Binary array data (`*.npy`, `*.npz`)
- Reference text files (`*.txt`)

All generated simulation outputs are saved under the `results/` directory.

---

## Installation & Setup

> **Detailed Guide**: See [`docs/INSTALLATION.md`](docs/INSTALLATION.md) for full step-by-step installation instructions across Conda and venv.

### Automated Setup (1-Command)

```bash
./scripts/setup_environment.sh
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/cspark7701/nkm-injection.git
cd nkm-injection

# Install locked dependencies and package
pip install -r requirements-lock.txt
pip install -e .[dev,moga]

# Verify installation via pytest suite (177 tests)
pytest -v

# Run single-command paper pipeline
python3 scripts/reproduce_paper.py --manifest config/publication_manifest.json -w 4
```

---

## License & Citation

- **License**: [MIT License](LICENSE)
- **Citation**: See [`CITATION.cff`](CITATION.cff)
