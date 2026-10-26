# Milestone 252 — Clarify BTS methods, add accuracy tables and improve figures

Completed: 2026-10-26 at the author's request to revise the BTS terminology, numerical-method description and figures.

## Manuscript changes

- Defined quadrupole labels by triplet and position: q11 is the first quadrupole of the first triplet; q33 is the last of the third triplet. Also identified q32 in the spatial-resolution discussion.
- Replaced Twiss terminology with Courant–Snyder parameters. Removed supplementary-material references from the main article, the specified subdivision parenthesis, the initialization phrase and displayed seed numbers. Seeds remain in source configurations and archived evidence. The standalone supporting document is retained; its displayed numerical seed identities were also removed.
- Replaced the obsolete integrator sweep narrative with the production choice of 40 steps per magnet and the nominal-map maximum-entry tolerance of 2e-6 in the stated SI coordinate convention.
- Added Kraft's SLSQP reference: *A Software Package for Sequential Quadratic Programming*, DFVLR-FB 88-28 (1988). Checked the primary report and the official SciPy SLSQP reference list. Preserved the companion manuscript's in-preparation status.
- Added two tables to the accuracy subsection: numerical map, symplectic and finite-case convergence checks; and the refined setting's peak beta functions at 8, 16, 32 and 64 observation subdivisions. Exported the tables directly from tracked summaries with input/output hashes. Diagnostic discrepancies are distinguished from acceptance tolerances.
- Added grid lines to Figure 2. Figure 3 now uses blue solid lines/filled circles and orange dashed lines/open squares, with a third panel showing low-beta minus reference clearance in both planes. Its caption identifies the styles and sampled-observation convention.

## Reproduction and verification

`export_bts_accuracy_tables.py` writes the two tables and their hash provenance into a new directory. `export_bts_at_figures.py` validates native optics against exact maps; if ignored campaign profiles are missing, it recomputes deterministic profiles of the frozen settings and checks retained peak summaries first. It handles the installed pyAT 0.8 synoptic return value. `export_bts_round3_assets.py --clearance-figure-dir` regenerates only the two nominal profiles and checks every aperture-family minimum against the tracked summary. The reproduction guide records these commands.

- Figure 2: maximum native/independent beta discrepancies 2.76e-11 m (reference) and 1.59e-11 m (refined low beta), below the 1e-4 m comparison tolerance.
- Figure 3: all aperture-family minima reproduce exactly for both settings; 204 profile rows per setting; 1e-10 m absolute check tolerance. No error campaign or optimization was rerun.
- Tests: `tests/test_bts_round2.py`, `tests/test_bts_round3.py` and `tests/test_package_imports.py`: 26 passed. Reran the maintained-source import-policy check after the final plotting edit: passed.
- Final isolated builds under `results/bts_methods_final_20261026/`: 13-page main paper and 8-page supporting document, passing the existing layout/reference gate. Visually inspected both figures and the rendered accuracy tables. Verified manuscript citation keys, section references, requested removals, whitespace and current asset hashes.

Installed the rebuilt PDFs, figures, numerical-table exports and provenance; updated `revision_selection.json`. Protected inputs, numerical campaign summaries and the historical referee attachment remain unchanged. No push or external submission was performed.

Reference checks: [primary report](https://degenerateconic.com/uploads/2018/03/DFVLR_FB_88_28.pdf), [official SciPy documentation](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html).
