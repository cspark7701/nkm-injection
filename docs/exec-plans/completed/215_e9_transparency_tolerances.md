# Milestone 215 — E9: Transparency units, simultaneous construction errors and septum leakage

Completed: 2026-10-13. Round-3 task E9 (R1C-05, R2c-6, R2c-7). Analytic and deterministic: no tracking campaign.

**Units (R1C-05).** The aligned-beam moment changes are fractional single-pass changes of the centred projected
emittance, Δε/ε = 4.5×10⁻⁷ (x) and 1.6×10⁻⁷ (y). They come from the kick spread alone. Section 6 now states this and
keeps them distinct from the filamented coherent growth and the tracked turn-1000 ratio.

**Simultaneous errors (R2c-6).** All eight wires are displaced at once, with independent Gaussian x/y offsets
(4000 draws per case, deterministic seeds). Loop-current errors are 0 (series), 10⁻⁴ or 10⁻³. The stored-beam
centroid amplitude in series powering:

| Wire rms | A_x/σ median (p90) | A_y/σ median (p90) | Both planes ≤ 0.1σ |
| ---: | :--- | :--- | ---: |
| 10 µm | 2.6 (6.2) | 4.8 (11.7) | 0.03 % |
| 25 µm | 6.4 (15.8) | 11.9 (28.9) | 0 % |
| 50 µm | 13.2 (31.9) | 23.2 (57.1) | 0 % |

Loop-current errors change these values by a few percent. Consequence, stated in section 6: geometric symmetry does
not make a realistically built magnet transparent. The static on-axis dipole residual must be measured and
compensated (trim winding or pulsed corrector, as at SOLEIL). No compensation design is attempted.

**Septum leakage (R2c-7).** At the septum β_x = 15.9 m. The allowance for 0.1 σ_x is 197 nrad, i.e. 0.066 G uniform
over the 0.4 m thin septum. That is 50 times below the published 3.3 G at the baseline bumped orbit. Section 6 states
the requirement, of order 0.07 G at the NKM-scheme stored orbit about 16 mm from the blade, and notes that the
thick-septum shielded value would also exceed it if it acts on the stored beam. The published value is not
distance-resolved, so the result is stated as a requirement rather than a prediction.

**Code and evidence.**
- New: `scripts/analyze_round3_transparency.py`.
- `build_revision_figures.py`: step `round3_transparency` (macros `WireMC*`, `Septum*`).
- Artifact: `results/journal_campaign_04/e9_transparency_mc.json` (manifest key `round3_transparency_mc`).
- Method note: `docs/paper/round3_transparency.md`.

**Checks.** The one-column gated build is clean.
