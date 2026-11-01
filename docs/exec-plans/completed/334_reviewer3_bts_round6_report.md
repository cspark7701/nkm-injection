# Milestone 334 — Reviewer 3 round-6 report on the BTS manuscript

Completed: 2026-11-01. Reviewer 3 independent assessment of the BTS transfer line manuscript (`docs/paper_bts/paper.tex`, `paper.pdf` [19-page NIM A Elsevier layout], `supplement.tex`, `supplement.pdf` [10 pages]) at checkpoint `fd16b2a` / latest `main`, after auditing all historical and current author responses across Rounds 1–6.

**Output.**
- `docs/paper_bts/reviews/review_round_06_reviewer_03_report.md` (comprehensive evaluation report);
- `docs/paper_bts/reviews/review_round_06_reviewer_03_tasks.md` (optional camera-ready editorial checklist R3-BTS-01 to 05);
- updated review index in `docs/paper_bts/reviews/README.md` and current status in `docs/paper_bts/README.md`.

No earlier review, author response, or historical register was modified or overwritten.

**Recommendation.** Accept for publication in Nuclear Instruments and Methods in Physics Research Section A (NIM A). No mandatory scientific revisions or tracking reruns required.

**Key Evaluated Findings.**
- **Blade Clearance Invariance:** Proved that matching declared boundary Twiss parameters fixes the nominal beam size at the limiting injection-septum blade, meaning interior peak beta reduction produces negligible clearance headroom where beam scraping actually occurs.
- **Phase-Advance Mechanism:** Formulated the transfer matrix mapping from extraction to septum exit, demonstrating that horizontal phase advance $\mu_x$ acts as the decisive physical knob partitioning incoming booster jitter between spatial excursion and angular deviation at the blade.
- **Active Dispersion Constraint:** Identified that the non-zero dispersion slope target ($D'_x = 0.0475$) sets a physical lower bound on accessible phase advance ($\mu_x \ge 0.69 \times 2\pi$), directly constraining the achievable loss reduction.
- **Shared-Reading Benchmark:** Audited Table 5's 200-machine, 3-shot, 2000-particle evaluation with frozen monitor errors. The true low-beta contrast is a modest $-0.13$ percentage points ($[-0.24, -0.04]$), whereas the loss-based phase-edge setting delivers a 4.48-fold reduction in mean jitter-integrated loss.
- **Surrogate Tracking Discrepancy Localization:** Verified the 880.5 expected vs 942 observed losses, localized predominantly to Machine 116, Shot 2 (454 observed vs 410.9 expected across 16 loss-bearing shots) due to near-blade grazing ($< 1\sigma_x$).
- **Dual Operating Regimes:** Contrasted the stress-jitter regime (where $\mu_x$ governs blade scraping) with the realistic small-jitter regime (where blade losses vanish and beam delivery is dominated by $0.18\text{ mrad}$ dipole steering residuals and $1.1\text{ mm}$ uncorrected vertical orbit).

Optional tasks R3-BTS-01 to 05 provide non-blocking editorial suggestions for submission formatting.
