# Round 3: physical synthesis of the robustness hierarchy (E8)

> Review-status annotation, 2026-10-16: these are the executed E7/E8 records. Their attribution of the
> NKM-specific deficit chiefly to booster angle jitter is challenged by both round-4 reviews: the paired
> NKM–dipole gap is already 28.33 points without jitter and 28.79 points with full jitter (seed 42).
> No individual non-jitter cause is established by this annotation. The original numerical records and
> interpretation below are retained pending [F2/F8](reviews/consolidated_revision_plan_round4.md);
> neither scientific revision has been executed.

**Hierarchy at the selected point** (manuscript Table V; rows use different samples and are not paired):

| Condition | NKM | Dipole |
| :--- | ---: | ---: |
| Ideal ring, no errors, 500 / 4000 turns | 98.4 / 97.8 % | 100 % |
| Ten corrected rings, no injection errors | 78.0 % | 82.2 % |
| Joint errors, no booster jitter (50 draws) | 40.1 % | 68.5 % |
| Joint errors, quarter jitter | 34.4 % | 66.9 % |
| Joint errors, full budget (150 draws) | 16.1 % | 44.1 % |
| Joint errors, no booster jitter, tuned | 52.1 % | — |

**What organizes the losses** (`scripts/analyze_round3_synthesis.py`, `e8_synthesis.json`):

1. **Ring errors are a ring property.** Without injection errors, both kickers lose about equally on the corrected
   rings. Across the ten rings both models correlate with the residual horizontal chromaticity (ρ = −0.68 NKM,
   −0.65 dipole) and β-beat (−0.58, −0.54). These are weak associations with only ten rings.
2. **The on-axis DA margin does not organize capture.** Over 400 candidate–ring pairs (E6 selection bunches), the
   margin between the first unstable launch and the injected centroid amplitude gives ρ = −0.23, and the logistic fit
   does not converge to a meaningful width:
   - capture peaks at an intermediate amplitude (about 7.5–7.7 mm);
   - the weakest ring (5501) has one of the largest margins.

   This rejects the single-parameter "DA margin" hypothesis raised by Reviewer 2 (round 3).
3. **The NKM-specific loss comes from injection errors.**
   - Booster angle jitter is the only Holm-significant driver (ρ = −0.38).
   - Angle-only jitter costs 16.8 points; position-only costs 8.9.
   - The NKM's angular window at the selected point (0.44 mrad) is comparable to the budget's angle errors; a uniform
     kick does not narrow the window.

   The E6 objective excluded injection errors and so favoured a point with a narrow angular window. The earlier point
   had 0.76 mrad. Selecting with injection errors in the objective is the evident next step and is not tested here.

**Statistical wording (R1C-06).** The jitter margin test is a one-sided noninferiority test against the declared
1-point analysis margin. Quarter jitter fails it with a resolved loss (−5.7 [−9.4, −2.5] points). The manuscript,
the Supplemental Material (S4) and the method notes use the same terms; "predeclared" is no longer used.
