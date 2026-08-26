# Task 11: Publication Regression Tests and Repository Cleanup

## Summary
- **Physics-Level Regression Testing**: Enhanced [`tests/test_paper_regression.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_paper_regression.py) with comprehensive physics checks covering constant 2-plane kicks, thin vs. thick integration agreement ($< 0.1\text{ mm}$ position, $< 0.3\text{ mrad}$ angle), element-resolved physical aperture and septum wall losses, individual Monte Carlo uncertainty responses, and quadrupole hardware bounds.
- **Lattice Symplecticity & Aperture Guards**: Updated `validate_bts_lattice()` in [`src/nkm/bts_lattice.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/bts_lattice.py) so 6D symplecticity (`is_symplectic_m66`) is included in the aggregate pass check `all_checks_passed`. Strengthened aperture validation bounds for shape, finiteness, positive upper limits, and coordinate order.
- **Link & Documentation Sanitization**: Cleaned up [`README.md`](file:///home/cspark/Work/projects/nkm-injection/README.md) by removing local `file:///` URLs and replacing them with relative repository paths.
- **Environment & Dependency Alignment**: Aligned Python version classifiers in [`pyproject.toml`](file:///home/cspark/Work/projects/nkm-injection/pyproject.toml) (`3.9`, `3.10`, `3.11`) matching `environment.yml` and `.github/workflows/ci.yml`.
- **Production Script Fail-Fast Safeguards**: Verified `set -euo pipefail` across [`scripts/run_full_production_simulation.sh`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_full_production_simulation.sh).
- **Test Suite Verification**: **161 tests passed in 573.88s (100% pass rate)**.

## Acceptance Criteria Checklist
- [x] CI runs meaningful physics regressions, not only structural checks.
- [x] README is usable by an external reader (local `file:///` links removed).
- [x] Version and environment declarations are consistent across files.
- [x] Production scripts fail loudly on errors (`set -euo pipefail`).
- [x] Release metadata is complete (`LICENSE`, `CITATION.cff`).
- [x] Protected files remain unchanged.
