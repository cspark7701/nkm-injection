# Task 55: Parameterize Matched Twiss in Convergence Studies (Task 03)

## Summary
- **Config Twiss Parameterization**:
  - Extended [`StorageRingInjectionConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/storage_ring_injection.py#L33) in `src/nkm/storage_ring_injection.py` with matched injection beam and circulating stored beam parameters:
    - **Injected Beam** (matched to BTS exit target optics):
      $$\beta_x = 2.3365\text{ m}, \quad \alpha_x = -0.016335, \quad \epsilon_x = 10^{-7}\text{ m}\cdot\text{rad}$$
      $$\beta_y = 4.2562\text{ m}, \quad \alpha_y = 0.017772, \quad \epsilon_y = 10^{-8}\text{ m}\cdot\text{rad}$$
      $$\sigma_\delta = 1.1 \times 10^{-3}, \quad \sigma_z = 13.4\text{ mm}$$
    - **Stored Circulating Beam** (ring injection point $s=0$ optics):
      $$\beta_x = 16.197\text{ m}, \quad \alpha_x = -0.1285, \quad \epsilon_x = 10^{-9}\text{ m}\cdot\text{rad}$$
      $$\beta_y = 5.0\text{ m}, \quad \alpha_y = 0.0, \quad \epsilon_y = 10^{-11}\text{ m}\cdot\text{rad}$$
- **Refactored Beam Generation Across Studies**:
  - Refactored [`particle_count_convergence_scan`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/convergence_study.py#L154) and [`turn_count_convergence_scan`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/convergence_study.py#L194) in `src/nkm/convergence_study.py` to pull Twiss parameters directly from `config`.
  - Refactored [`compute_injection_acceptance`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/convergence_study.py#L307) and [`run_ensemble_study`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/convergence_study.py#L352) to eliminate arbitrary hardcoded numbers (`beta_x=10.0, beta_y=5.0`).
  - Updated [`scripts/run_multiturn_injection.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_multiturn_injection.py#L316) survival curve plotting distribution to use `config.inj_beta_x_m` and `config.inj_alpha_x`.
- **Verification & Testing**:
  - Added [`TestMatchedTwissParameterization`](file:///home/cspark/Work/projects/nkm-injection/tests/test_convergence_study.py#L235) in `tests/test_convergence_study.py` to verify configuration propagation and custom Twiss injection scans.
  - Ran `pytest tests/test_convergence_study.py tests/test_storage_ring_injection.py -v`: all 22 tests passed in 4.79s.
  - Verified protected files remain clean and untampered.
