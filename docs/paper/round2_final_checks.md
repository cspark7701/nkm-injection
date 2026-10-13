# Round-2 verification record and scope

The completion records in `docs/exec-plans/completed/` report the executed checks
for D1–D15. The [final D14 record](../exec-plans/completed/157_round2_final_reconciliation.md) is authoritative for the full-suite result,
clean manuscript build and protected-input verification. Earlier scientific
reviews and responses are preserved as historical assessments.

[D15](../exec-plans/completed/160_prab_manuscript_formats.md) completed on
2026-10-12 after the author selected PRAB. It records clean REVTeX 4.2 builds
of the 28-page primary draft and 14-page two-column preview, plus 37 passing
relevant tests. These were installed-asset builds; campaign-03 raw evidence was
unavailable locally and the historical evidence-bundle verification was not
repeated. See [current submission status](prab_submission.md).

## Numerical and statistical checks

- The independent trajectory reference compares the stated paraxial equations
  with adaptive DOP853 integration, including off-midplane and momentum-offset
  launches and the final interpolated angular-window edges.
- Native and affine-element ring tracking share initial particles and physical
  aperture checks. The nominal native 500-turn survival masks match the chamber
  study exactly; independent edge/degraded samples extend to 4000 turns.
- Final jitter comparisons verify actual non-jitter draws, scientific settings,
  particle seeds and corrected-ring identities before computing paired intervals.
  Bootstrap uncertainty is conditional on the ten saved corrected rings.
- Tuning uses independent training particles, bounded knobs and a fixed search
  budget. Paired held-out particles quantify recovery without selecting knobs
  from the validation results.
- The manuscript distinguishes particle Wilson intervals, joint-realization
  bootstrap intervals, finite ring-seed variation and deterministic calculations.

## Publication and reproducibility gates

The figure builder checks each consumed artifact against the selected manifest.
`build_submission_package.py` builds in a new directory and rejects LaTeX errors,
undefined references/citations, BibTeX warnings and overfull boxes. Figure
provenance and the consumed-artifact inventory accompany the source package.

`build_evidence_bundle.py --verify` archives committed source and selected
inputs, then rebuilds from that archive and the copied evidence in a temporary
directory. It fails if the regenerated manuscript macros differ. The bundle
contains its verification summary and a SHA-256 inventory. The D13 completion
record identifies the resulting local attachment and archive hash; no public
DOI or external upload is implied. See [reproduction instructions](round2_reproduction.md).

## Scientific limits

These checks establish consistency and reproducibility within the declared
model. They do not establish operational capture, an as-built chamber or ring,
a measured error budget, noisy beam-based feedback, arbitrary kicker-family
universality, or time-dependent pulsed capture. Individual wire/current
sensitivities are distinct from the whole-magnet errors in the joint ensembles.
The incoming-line chamber and the actual IVU assignment remain assumptions or
unavailable inputs. D15 journal conversion is complete; the
[eight third-round scientific tasks](reviews/reviewer1_round3_20261012_revision_tasks.md)
remain pending.
