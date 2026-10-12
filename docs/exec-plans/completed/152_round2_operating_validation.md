# Milestone 152 — Validate chamber operating point and long-turn boundaries (D11)

Completed: 2026-10-12.

Replace provisional validation with native and affine backend comparisons, refine the connected operating window, and track the nominal point, two interpolated edge candidates and a degraded corrected ring for 4000 turns. Nominal survival falls from 97.0% at 500 turns to 96.1%; fresh edge samples qualify the interpolated 80% boundaries. Reconcile the pulse allowance and independent trajectory checks with the final window.

Validation: Ten focused tests and three submission tests pass; the gated 17-page PDF builds. The nominal 500-turn masks exactly match D6, the affine tangent agrees within 1.37e-14, and all eight independent ODE cases pass. Figures 3, 5 and 7 inspected.

Protected input hashes match the initial campaign-03 inventory. Generated results remain uncommitted under `results/journal_campaign_03/`.
