# Milestone 103 — Campaign S1–S3 and Step 1 physics checks

Completed: 2026-10-09. Scope: reproduce existing studies S1–S3 and audit kick sign/units and
injection acceptance before any large campaign. No source code, manuscript or protected input changed.

## Execution
Campaign `results/journal_campaign_01/` (git-ignored) at commit 8b62bcd, pyat-dev Python 3.11.9.
Source run read from `backups_20261009/production_statistical_01`. Commands follow
[023 §3–4](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md); S3 used `--workers 6` and base seeds 42/123/777.
Full numbers and diagnostic scripts: `results/journal_campaign_01/FINDINGS.md` and `step1_checks/`.

## Results
- S1, S2 and S3 (seed 42) reproduce the archived run exactly; S3 seeds 123/777 agree (field-map capture 0.9978–0.9979).
- The S3 seed lists overlap (123, 777, 858 reused), contrary to 023; they are not independent replicates.
- `kickmap_file.txt` stores kick angles in mrad without charge sign (header "Tm" is wrong). On the midplane it
  equals `By.txt`·L/Bρ to ~1e-10, and `By.txt` is a transverse By(x) at the magnet centre.
- Kick-map tracking uses +∫By/Bρ while thick tracking uses the electron sign −∫By/Bρ; the frame mapping is undocumented.
- The ring lattice has max β_x 16.4 m and no aperture elements. With native nonlinear tracking, a particle with x'=0
  survives 500 turns at ±12 mm but is lost at −16 mm (turn 31) and −20 mm (turn 4). The linear-map model keeps
  −20 mm stable, so the reported ~99.8 % capture and off-kicker 100 % capture come from the linearization.
  In that model any NKM kick increases the betatron amplitude.

## Verification and limits
Protected-file hashes matched before and after; git status showed only this document and README changes
(plus the user's untracked backup folder). Dynamic-aperture result is single-particle, on-momentum, 500 turns,
without physical apertures; a full DA/momentum-aperture study belongs to Tasks 003–004.

## Next
Tasks 002–004: define injection geometry and kick sign, adopt nonlinear element-by-element tracking with apertures,
then rerun controls. Defer S4 and new large budgets.
