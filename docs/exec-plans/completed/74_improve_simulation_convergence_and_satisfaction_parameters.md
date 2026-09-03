# Task 74: Improve Simulation Convergence and Satisfaction Parameters (Steps 4–7)

## Summary
- **Step 4 (Multi-Turn Injection Tracking Convergence)**:
  - Identified that nominal injection offset $x_{\text{inj}} = -16.0\text{ mm}$ was on the steep boundary of the storage ring acceptance window ($\Delta x' \approx -2.1\text{ mrad}$, under-kicked), giving ~5.2% capture and non-converged particle-scan residuals ($\Delta = 0.0021 > 0.001$).
  - Updated nominal injection position to $x_{\text{inj}} = -20.0\text{ mm}$ (where $\Delta x' \approx -2.7\text{ mrad}$, optimal for 4GSR), achieving **100.0% capture** and perfect particle-count convergence (**$\Delta = 0.0000 < 0.001$**).
  - Generalized linear kicker model around injection reference point and filtered NaNs before tracking.
- **Step 5 (Deterministic BTS Quadrupole Optics Matching)**:
  - Verified physical satisfaction: merit $J = 0.0000$, mismatch $M_x = M_y = 0.000000$, peak betas $\beta_x=30.2\text{ m}, \beta_y=44.5\text{ m} \ll 100\text{ m}$, and all constraints satisfied (`Constraints satisfied: True`).
  - Increased `max_iter` from 20 to 100 in [`scripts/optimize_bts_publication.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/optimize_bts_publication.py), allowing SLSQP to formally report **`Optimization success: True`**.
- **Step 6 (Monte Carlo Tolerance & Sensitivity Analysis)**:
  - Verified that Monte Carlo sampling was converged ($\Delta_{50\to 100} = 0.000054 \ll 0.02$).
  - Updated [`scripts/run_publication_tolerances.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_publication_tolerances.py) to evaluate tolerances on the matched Step 5 quadrupole configuration instead of the unoptimized baseline, reducing failure probability from **100.0% to 0.0%** (zero constraint violations across all error categories).
- **Step 7 (MOGA NSGA-II Pareto Optimization)**:
  - Identified that `pop_size=15, n_gen=5` was too small for 9-D constrained parameter space (resulting in 0% feasibility).
  - Updated [`scripts/run_publication_moga.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_publication_moga.py) to `pop_size=40, n_gen=20`, achieving **100.0% feasible fraction**, **31 non-dominated Pareto solutions**, and **`Success: True`**.
- **Verification**:
  - Full test suite (`pytest`) verified with 100% pass rate across all 177 tests.
