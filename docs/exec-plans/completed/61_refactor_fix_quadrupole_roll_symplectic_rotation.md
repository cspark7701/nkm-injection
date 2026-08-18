# Task 61: Refactor — Fix Quadrupole Roll 6D Symplectic Rotation Matrix

## Summary
- **Refactor Objective (Task 07)**:
  - Fixed a physics defect in quadrupole roll error modeling where coordinate transformations in [`src/nkm/errors.py`](file:///home/cspark/Work/projects/nkm/src/nkm/errors.py#L131-L140) only rotated spatial coordinates $(x, y)$, leaving transverse angle/momentum coordinates $(x', y')$ unrotated.
- **Physics Fix Implemented**:
  - In [`src/nkm/errors.py:apply_sample_errors`](file:///home/cspark/Work/projects/nkm/src/nkm/errors.py#L131-L140), updated the $6\times 6$ roll transformation matrix `r_mat` to rotate both transverse positions and momenta simultaneously:
    ```python
    cos_r, sin_r = np.cos(roll), np.sin(roll)
    r_mat = np.eye(6)
    r_mat[0, 0] = cos_r
    r_mat[0, 2] = sin_r
    r_mat[1, 1] = cos_r
    r_mat[1, 3] = sin_r
    r_mat[2, 0] = -sin_r
    r_mat[2, 2] = cos_r
    r_mat[3, 1] = -sin_r
    r_mat[3, 3] = cos_r

    elem.R1 = r_mat
    elem.R2 = r_mat.T
    ```
- **Verification**:
  - Added [`test_quadrupole_roll_symplectic_structure`](file:///home/cspark/Work/projects/nkm/tests/test_errors.py#L82) in `tests/test_errors.py` checking matrix entries and symplecticity $R_1 J R_1^T = J$ ($< 10^{-14}$ tolerance).
  - Ran `pytest tests/test_errors.py tests/test_error_model.py tests/test_constrained_optimization.py -v`: 100% passed (60/60 tests).
  - Protected scientific source data files remain clean and untampered.
