# Milestone 290 — R5-BTS-07: consolidation of article and supplement

Completed: 2026-10-31. Round-5 task R5-BTS-07 (Reviewer 2 R2D-05, R2D-11; Reviewer 1 R1D-BTS-07).

**Article.**
- **First fresh test.** The round-3 test table (former Table 6) and its paragraph moved to the new supplement
  Section 5. A three-sentence summary in Section 4.3 keeps the tracked gain of 3.3, the unresolved low-beta change,
  and the 13 % angle-jitter cost. References to the moved table now point to Tables 6 and 8, or were dropped.
- **Figure 4.** Replaced by `figures/round5_jitter_transfer.pdf`, which has only the jitter-transfer panel, the
  label "found range" in place of "reachable", and no "Refined low beta". The loss panel duplicated Figure 5.
- **Sampled roll and energy-jitter table** (former Table 8). It moved to the supplement with its paragraph, keeping
  its sampled-prediction definition. A short summary remains in Section 4.5: rolls change the loss by less than
  0.001 percentage points, and halving the energy jitter by at most 0.04.
- **Four-station material.** Repeated text in Sections 2.1 and 3.1 is compressed to point to the supplement.
- **Float order.** The residual table follows the jitter table.
- **Final numbering:** Tables 1–8 and Figures 1–6.

**Supplement.**
- **New Section 5,** "Earlier fresh test and roll and energy-jitter sensitivity": the moved tables and paragraphs,
  with cross-references pointing to the article and the reading-error difference stated.
- **Shorter audit.** The four-station accuracy paragraph in Section 3 is cut from 12 lines to 6, with its
  provenance numbers kept.
- **Introduction.** It lists six sections.

**Length.** The article is 19 pages (20 before the four-station compression), with a 10-page supplement. The text
before the references is about 9,900 whitespace-separated tokens, including captions, tables and mathematics; this
is not a formal word count. JKPS recommends about 4,000 words and up to six figures, without a strict limit, and
the article has six figures. The 12–14-page target was not reached, because the round-5 additions were required.
Further shortening would mean choosing among material the author asked for, such as the baseline Figures 2–3 and
the expanded literature review. That is left as an author decision; no assumption or unfavourable result was
removed.

The prose follows the humanizer rules. The isolated builds are clean. Protected files are unchanged.
