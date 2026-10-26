# Milestone 259 — Use the original BTS setting as the optimization reference

Completed: 2026-10-26 at the author's request to replace the earlier matched reference in Figures 2 and 3 with the original setting, and to frame the study around optimizing the BTS line.

## Original-to-optimized comparison

Both figures now obtain the reference strengths directly from `BTSConfig().quad_strengths_list`, with exact identity checked against the retained initial-setting record. The optimized curve is the existing refined low-beta setting. Figure 2 re-evaluates both lattices on the same observation mesh, checks native AT optics against independent maps and records strengths, peaks, exit functions and normalized residuals.

Figure 3 re-evaluates the original aperture profile rather than substituting the matched-baseline data. It uses a symmetric logarithmic scale with a linear region near zero so that the negative original clearance is visible. Its difference panel is optimized minus original; the shared BTS layout is retained. All optimized aperture-family minima still agree with their frozen summary. The original exit RMS sizes are checked independently against the retained initial-setting record.

The new nominal comparison table reports:

| Quantity | Original setting | Optimized low beta |
| :--- | ---: | ---: |
| Peak horizontal beta [m] | 52.2506 | 33.7945 |
| Peak vertical beta [m] | 242.6069 | 28.4371 |
| Exit horizontal beta [m] | 44.9808 | 2.3365 |
| Exit vertical beta [m] | 242.6069 | 4.2562 |
| Minimum five-sigma clearance [mm] | -1.5170 | 0.6484 |
| Maximum normalized exit residual | 4.77e3 | 2.88e-10 |

The original setting is unmatched; the optimized setting meets the prescribed target. Negative five-sigma clearance means envelope overlap, not loss of every particle.

## Manuscript and provenance

Reframed the qualitative abstract, study goal, results and conclusions around optimization of the original line followed by loss-sensitivity refinement within matched solutions. Added the nominal table and replaced misleading statements that the two plotted settings share an exit match or coincide at the injection septum. Updated legends, captions, README and reproduction instructions.

Existing error ensembles retain their actual matched intermediate baseline. Their table display labels now say Matched, and the narrative distinguishes these matched-only results from the original-setting figure reference. Their numerical JSON summaries and all numerical table entries are verified unchanged; no original-setting error ensemble is claimed. The later jitter plot's matched-only scope is explicit. Previous reviews and historical records are preserved.

## Validation

The new reference-identity regression verifies that the original configuration is plotted, the frozen campaign record is not mutated, the original fails matching/nominal clearance, and the optimized setting passes both checks. It and the relevant aperture/import checks pass: 15 tests.

Both figure exporters complete their independent checks. Confirmed the same original strength vector in both validation records, the qualitative abstract, citations/equation references, units, whitespace and changed paths. Visually inspected both new figures and the rendered comparison table and Figure 3 page. Final isolated builds under `results/bts_original_reference_20261026/` pass the layout/reference gate: 15-page main paper and 8-page supporting document. Installed PDFs and refreshed asset hashes; asset verification passes.

Protected inputs, scientific code under `src/`, old campaign summaries and the historical attachment remain unchanged. This task re-evaluates deterministic nominal settings; no optimizer or random error campaign was rerun. No push or external submission performed.
