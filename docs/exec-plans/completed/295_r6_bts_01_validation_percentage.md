# Milestone 295: R6-BTS-01 validation percentage

Completed: 2026-10-31. The exporter now names the discrepancy as a prediction
shortfall relative to observation: (942 - 880.4533242328341) / 942 = 6.533617385%.
Generated macros and manuscript Results/Discussion use 6.5% below observation.
The 2.1-standard-deviation value is explicitly a diagnostic Poisson approximation
without model-systematic uncertainty; the discrepancy remains unresolved.

Applied the humanizer skill to changed manuscript prose, preserving numerical
claims and technical notation. No simulation output was overwritten. Counts,
headline gain/interval and all original validation fields match the reviewed snapshot.
The exporter executes and the isolated article build in
`results/bts_round6_revision_20261031/task01_article` passes without warnings;
PDF text confirms the corrected wording. Final installed PDFs and selected hashes
will be reconciled in R6-BTS-04. Protected inputs are unchanged.
