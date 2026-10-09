# Milestone 105 — Journal Task 002: canonical physics model and claim audit

Completed: 2026-10-09. Task: [002](../../jinst-paper/tasks/002_canonical_physics_and_claim_audit.md).

## Deliverables
- [`claim_evidence.csv`](../../jinst-paper/claim_evidence.csv): 29 audited manuscript claims (all abstract and
  conclusion numbers) with artifact, key, actual value/units, model and decision. Disputed numbers resolved:
  kick at −16 mm (−2.105, not −5.749 mrad), grid ±50 mm/0.5 mm, NKM length 0.525 m (0.31 m is the BTS
  extraction kicker), BTS length 21.789 m, emittances 100/10 nm used in all studies, quad bounds, selected-run
  optimisation/tolerance values, linear-map capture and 430× ratio removed, unverifiable references removed.
- [`physics_model.md`](../../jinst-paper/physics_model.md): source contents, ring parameters derived from the
  lattice (ε_x 61.6 pm, σ_δ 1.264e−3, tunes, chromaticity, damping), injection geometry (septum −16 mm edge,
  2 mm blade, 2.0 m drift to NKM, single-turn thin kick at NKM centre), polarity convention, calibrated
  controls, beams, observables, error coverage table and objective normalisation.
- `src/nkm_injection/injection_study.py`: versioned `InjectionStudyConfig` (schema 1), kick models
  (`off`, `fieldmap`, `dipole`, `linear` calibrated at the injected centroid), ring re-ordered at the NKM
  centre with septum aperture, native and linear backends, stored-beam response. Example
  `config/injection_study_v1.json`. `tests/test_injection_study.py` (10 tests).
- `scripts/audit_error_coverage.py`: effective coverage audit; 5 sampled fields have no effect on the
  tolerance observables and 4 are never sampled; capture is not computed by the tolerance study.

## Verification
Full suite 634 passed (271 s, single-thread BLAS/OMP). Audit CLI reproduced the campaign audit exactly.
Protected hashes unchanged; outputs only under `results/journal_campaign_01/task002/`.
Assumptions: vertical stored emittance 10 % of ε_x; booster emittances from the optimisation configuration;
tolerance σ values carried without design justification.
