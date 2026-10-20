# Round 4 (F7): pulse and transparency at the current point

**Scope.** All quantities are recomputed at the point retained by F3: x_inj −19.478 mm, S = 0.95, with the round-3
chamber. Outputs are in `results/journal_campaign_05/f7/`.

**Manifest.** `scripts/make_round4_manifest.py` writes `docs/paper/revision_manifest_round4.json`:
- the round-3 manifest, plus the round-4 artifacts;
- the builder keys `round2_pulse`, `round2_transparency`, `round2_stored_tracked`, `round3_transparency_mc` and
  `c7_analytic`, re-pointed to the recomputations below;
- each S = 0.85 original kept under a `historical_` key.

The manifest builder rechecks every recorded hash. A test confirms that every re-pointed artifact is at S = 0.95 and
that the pulse allowance is one tenth of the current window.

## Pulse (`analyze_round2_pulse.py`)

**One allowance convention.** The allowance is one tenth of the current point's 80 % angular window, the same
convention as the thin-map accuracy allowance (section 3):
- window −0.319 to +0.124 mrad, width 0.443 mrad, so the allowance is 0.044 mrad;
- the round-2 pulse used the earlier window, 0.758 mrad, giving 0.076 mrad.

| Quantity | Round 2 (earlier point, S 0.85) | Current point (S 0.95) |
| :--- | ---: | ---: |
| Turn 1/2/3 position at NKM centre | −2.87 / 6.20 / 9.00 mm | −2.45 / 5.49 / 7.75 mm |
| Turn 1/2/3 straight-line full kick | 0.54 / 3.71 / 4.87 mrad | 0.38 / 3.32 / 5.30 mrad |
| Allowed first/second-return fraction | 0.14 / 0.02 | 0.12 / 0.01 |
| Peak-phase maximum pulse length | 5.85 µs | 5.76 µs |
| No-return maximum (2 T₀) | 5.33 µs | 5.33 µs |

**The conclusion is unchanged.** The 5.3 µs peak-phase example satisfies both limits. The margin to the no-return
limit (0.03 µs) is set by the revolution period and is independent of the point. An 8 µs pulse still retains 0.50
of the peak field on the first return.

## Transparency at S = 0.95

| Quantity | S 0.85 (history) | S 0.95 (current) |
| :--- | ---: | ---: |
| A_x/σ_x at 0.1 / 0.2 / 0.5 mm offset (exact field, quadrature) | 0.016 / 0.10 / 1.54 | 0.018 / 0.12 / 1.72 |
| A_y/σ_y at 0.2 mm vertical offset | 0.17 | 0.19 |
| Tracked A_x/σ_x at 0.2 / 0.5 mm (turns 1–50) | 0.10 / 1.47 | 0.11 / 1.65 |
| Tracked emittance ratio at 0.2 / 0.5 mm (turn 1000) | 1.01 / 2.24 | 1.01 / 2.55 |
| Single-error wire limits | 0.29–2.04 µm | 0.26–1.82 µm |
| Independent-loop current balance | 1.15 × 10⁻⁴ | 1.03 × 10⁻⁴ |
| Wire MC median A_x/σ, A_y/σ, 10 µm | 2.6, 4.8 | 2.9, 5.4 |
| Wire MC median A_x/σ, A_y/σ, 25 µm | 6.4, 11.9 | 7.2, 13.3 |
| Wire MC median A_x/σ, A_y/σ, 50 µm | 13.2, 23.2 | 14.8, 25.9 |
| Septum-leakage requirement | 0.066 G | 0.066 G (independent of S) |

**Reading.**
- The single-pass quantities scale linearly with S (factor 0.95/0.85 = 1.118), as expected.
- The tracked emittance ratio at 0.5 mm grows faster than linearly.
- At the selected strength a 0.2 mm offset gives 0.11–0.12 σ, slightly above the 0.1 σ criterion. The manuscript
  now states this instead of "about a tenth".

**Manuscript changes.**
- Pulse section: names the selected point and the window it uses.
- Transparency paragraph: evaluated at the selected S; S = 0.85 values scale down by 1/1.12.
- The cubic coefficient is labelled with the selected S.
- The remaining `\OpScale` (0.85) labels on the field table and on Fig. 2 are historical diagnostics; F8 labels them.

**Build environment.**
- The pinned `requirements-lock.txt` environment is not available on this machine. The builds and simulations use the
  conda env `pyat-dev` (numpy 2.4.6, matplotlib 3.11.1, accelerator-toolbox 0.7.2.dev).
- Only Fig. 7, whose inputs changed, is regenerated. Figures with unchanged inputs keep their matplotlib 3.8.3 files.
- F9 decides the final rebuild.
