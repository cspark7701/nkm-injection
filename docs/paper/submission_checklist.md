# PRAB submission checklist — current status

Updated: 2026-11-01. Target: Physical Review Accelerators and Beams, Research Article.

[Reviewer 1's round-6 assessment](reviews/review_round_06_reviewer_01_report.md) recommends scientific acceptance with no mandatory scientific revision and [two optional copyedits](reviews/review_round_06_reviewer_01_tasks.md). The separately written [Reviewer 2 round-6 report](reviews/review_round_06_reviewer_02_report_and_tasks.md) also recommends acceptance. The [G1–G7 register](reviews/revision_round_05_plan_for_review_round_05.md) and [joint response](reviews/review_round_05_author_response_to_reviewers_01_02.md) record G1–G6 complete; G7 remains deferred. This internal review recommendation does not supply final author approval or perform submission.

## Completed preparation

- [x] D1–D15 round-2 work and PRAB conversion; E1–E11 round-3 work.
- [x] F1–F9 round-4 execution (milestones 236–246): paired attribution, point decision, loss/domain diagnostics and current-point pulse/transparency reconciliation.
- [x] [Round-4 response](reviews/review_round_04_author_response_to_reviewers_01_02.md), selected manifest and frozen evidence attachment.
- [x] REVTeX one-column primary, shared-source two-column preview and supplement; current lengths 36/18/7 pages after the round-5 revision.
- [x] Fifth-round evidence checks: 250 artifact-key hashes, exact fresh post-processing and macro reproduction, 258 frozen inventory entries and 26 relevant tests.

These are execution and evidence checks. Their detailed limits are in the fifth-round report; they do not establish operational performance or replace author approval.

## Consolidated revision work

- [x] G1: freeze the paired protocol and verify shared BTS settings, populations and jitter units.
- [x] G2: run the targeted two-plane jitter scan and report paired loss/gap estimands.
- [x] G3: reconcile headline populations, recovery budgets and abstract wording.
- [x] G4: correct physical chamber-interception wording from existing F5 records.
- [x] G5: reconcile selected-point labels, date, ideal-correction scope and tuning conditions.
- [x] G6: rebuild, verify evidence/packaging, update current status and respond to both reviewers.

The current simulated headline remains 98.4% ideal-ring capture at 500 turns, 97.8% at 4000, 78.0% corrected-ring mean and 16.1/44.1% NKM/dipole joint-error means. The seed-42 steering sensitivities use their own paired 50-draw population and budget labels. The current pulse uses the adopted point and a 0.044 mrad allowance; earlier pending-F and old-pulse statements are superseded.

## Author and delivery gates (G7, deferred)

- [ ] Approve final scientific interpretation, title, authorship/contact details, declarations and AI disclosure.
- [ ] Confirm retained funding information and other declarations in the submission interface.
- [ ] Choose final PhySH headings and confirm exclusive submission/history in the portal.
- [ ] Confirm availability wording and actual access to the ignored scientific evidence attachment.
- [ ] Approve and perform external submission/delivery separately. No DOI is required by this local checklist.

Build commands: [PRAB formats](prab_submission.md). Scientific snapshot and reproduction commands: [round-5 evidence guide](round5_reproduction.md). Earlier reports, responses and frozen packages are preserved and must remain identifiable as historical versions.

Round-5 evidence: 272 selected keys and 280 verified attachment inventory entries. Archived macros and portable scan reanalysis reproduce byte for byte. See the [verification receipt](round5_final_identity.json).
