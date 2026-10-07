# Milestone 88 — Task 03: Strict shared field-map validation

Completed: 2026-10-07  
Task: [Enforce shared field-map shape and domain validation](../../05_refactor_tasks/03_strict_fieldmap_domain_validation.md)

## Problem and outcome

The 3-D interpolation paths silently clamped coordinates outside map coverage and ignored the class's extrapolation setting, including along z. The 2-D parser discarded the second section's axes. Map construction now validates shapes, finite values and axes before interpolation; all evaluators reject outside queries by default and accept NumPy broadcast coordinates.

## Implementation

- Added NumPy-only axis, value, bounds, coordinate and uniform-grid contracts, plus shared trilinear interpolation. Grid axes require at least two nodes and strictly increasing finite coordinates without duplicates; fields require exactly three components.
- Validated kick-map length, integer dimensions, exact section/token counts, finite component data and identical axes in both sections. Preserved existing component assignments, metadata conversions and kick signs.
- Added finite query checks to 1-D/2-D evaluation and explicit broadcasting to 2-D/3-D evaluation. Shape errors remain ValueError; finite outside coordinates raise OutOfDomainError. The 3-D class exposes z bounds and evaluates in meters directly.
- Made 3-D raise/extrapolate/clip policies explicit. The class's allow_extrapolation flag now selects linear edge-cell continuation instead of implicit clipping. Closed endpoints are accepted; immediately outside floating-point neighbors are rejected without tolerance.
- Retained sorting in the 1-D file loader, validated its output, repaired CSV delimiter handling, and validated quadrature inputs. Two-node linear maps work; cubic requests require at least four nodes. Symmetry diagnostics handle sparse positive-side samples safely.
- Reused the shared NumPy-only source in the pyAT installer and patch artifact. Tracking validates the map once before slicing and leaves already-lost particles unchanged. The external pyAT installation was not modified.
- Documented units, layouts, boundary migration, broadcasting, numerical tolerances and extension installation in [field-map contracts](../../013_FIELDMAP_CONTRACTS.md); updated README and the ignored backlog status/manifest.

## Verification

- Focused existing and new field-map tests: **71 passed** in 1.63 s.
- Full suite: **306 passed** in 47.98 s in the existing pyat-dev Python 3.11 environment with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1.
- Tests exercise every lower/upper face and immediately outside neighbor in 1-D/2-D/3-D, nonfinite fields/coordinates, duplicate/reversed axes, malformed dimensions/token counts, section disagreements, scalar/array broadcasting, explicit boundary policies, and a standalone copied pyAT helper. Patch source synchronization is checked.
- Existing tabulated interpolation checks retain absolute tolerance below 1e-12. Affine-field checks use absolute tolerance 1e-12 with zero relative tolerance; existing batch/scalar interpolation and tracking use 1e-14.
- Field-validation CLI executed in a fresh process and wrote only to `/tmp/nkm-task03-fieldmap-20261007/`: 1-D valid, peak By 0.146109 T, 2-D tabulated interpolation error 0, and existing x=-10 mm kick -5.4341 mrad.
- By.txt and kickmap_file.txt SHA-256 values match existing regression hashes. Final git status/diff and whitespace checks confirm no protected source/input changes. Installer shell syntax and patch syntax checks pass.

## Compatibility and scope

Outside queries that previously returned clipped 3-D fields now raise. Explicit low-level boundary_policy="clip" reproduces the old behavior when deliberately needed; allow_extrapolation=True selects actual extrapolation. In-domain physics, kick signs, saved schemas and source maps are unchanged. The installed pyAT copy needs reinstallation to receive this update. No full production study, source regeneration, remote GitHub interaction or push was performed.
