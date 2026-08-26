# Task 57: Centralize Canonical Twiss Parameters and Enforce DRY (Task 05)

## Summary
- **Single Source of Truth for Optical Parameters**:
  - Implemented immutable, frozen dataclass [`TwissParameters`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/optics.py#L14) in `src/nkm/optics.py` with `.to_dict()` conversion.
  - Defined authoritative single-source-of-truth constants:
    - **`DEFAULT_BTS_ENTRANCE_TWISS`**:
      $$\beta_x = 7.5600\text{ m}, \quad \beta_y = 12.2690\text{ m}, \quad \alpha_x = 1.5231, \quad \alpha_y = -1.6547, \quad D_x = 0.2762\text{ m}, \quad D_x' = -0.0657\text{ rad}$$
    - **`DEFAULT_BTS_TARGET_TWISS`**:
      $$\beta_x = 2.3365\text{ m}, \quad \beta_y = 4.2562\text{ m}, \quad \alpha_x = -0.0163, \quad \alpha_y = 0.0178, \quad D_x = 0.0809\text{ m}, \quad D_x' = 0.0475\text{ rad}$$
- **Eliminated Duplicate Dictionaries Across Codebase**:
  - Refactored [`OpticsTargetConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/objectives.py#L17) in `src/nkm/objectives.py` to default directly to `DEFAULT_BTS_ENTRANCE_TWISS` and `DEFAULT_BTS_TARGET_TWISS`.
  - Refactored [`src/nkm/errors.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/errors.py#L142) to scale `DEFAULT_BTS_ENTRANCE_TWISS` attributes.
  - Refactored [`src/nkm/robust_optimization.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/robust_optimization.py#L230) to reference `DEFAULT_BTS_ENTRANCE_TWISS.to_dict()`.
  - Refactored [`src/nkm/paper.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/paper.py#L89) in table and figure generation to use `DEFAULT_BTS_ENTRANCE_TWISS.to_dict()`.
  - Refactored [`scripts/validate_bts_optics.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/validate_bts_optics.py#L39) to reference both canonical constants.
- **Verification & Testing**:
  - Added [`test_canonical_twiss_parameters_and_dry_structure`](file:///home/cspark/Work/projects/nkm-injection/tests/test_bts_lattice.py#L105) and [`test_canonical_optics_metrics_with_constants`](file:///home/cspark/Work/projects/nkm-injection/tests/test_bts_lattice.py#L119) in `tests/test_bts_lattice.py`.
  - Ran `pytest tests/test_bts_lattice.py tests/test_optimization.py tests/test_paper_pipeline.py -v`: all 18 tests passed.
  - Verified protected source data files remain clean and untampered.
