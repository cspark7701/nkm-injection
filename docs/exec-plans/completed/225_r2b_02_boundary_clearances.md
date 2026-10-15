# Milestone 225 — R2B-02: Boundary-fixed end-station clearances

Completed: 2026-10-15. Reviewer 2 BTS task R2B-02 (M1 of `reviewer2_bts_20261015_main_report.md`).

**Change.** `src/nkm_injection/bts_round3.py` (new) provides `boundary_clearances`. It gives the nominal five-sigma
clearance at the entrance and exit stations from the boundary Twiss, dispersion, emittance and energy spread alone.
Both stations lie where the optics are fixed: the entrance is an input and the exit is matched. Their clearances are
therefore identical for every matched quadrupole setting:
- entrance: 17.455/18.865 mm;
- exit: 18.555/19.064 mm.

**Manuscript.**
- Section 3.1 now states this analytic result and explains that the minimum's "saturation" follows from placing
  restrictions only at the line's ends.
- The abstract no longer headlines the baseline ensemble result.
- Section 4.1 refers to the analytic value.

**Tests.** `tests/test_bts_round3.py`: the reference and low-beta settings reproduce the analytic values (entrance
1e-9 m, exit 2e-7 m), and the values equal Table 2 (3 tests pass). The article builds without warnings.
