# Milestone 321 — NKM G2 scan driver and paired analysis

Completed implementation: 2026-11-01. The simulation/analysis task G2 remains running, not complete.

Added `run_round5_campaign.py` to generate only the three missing paired two-plane jitter scales, with eight workers, fixed inputs and strict checkpoint resumption. Existing zero/full endpoints are reused after verifying their tracking sources/configurations. Their only changed recorded module is the separate BTS `bts_round3.py`, which the NKM tracker does not import; this exclusion is explicitly recorded rather than claiming every old source hash matches.

Added `analyze_round5_jitter.py` to verify complete job/particle/ring identities, preserve all non-jitter draws, reconcile particle losses and report pointwise paired jitter costs separately from model gaps. Added round-5 reporting and manifest selection, and optional supporting records in the submission packager. Portable analysis supports an explicit evidence root.

Meaningful tests check pairing rejection, non-jitter invariance, the distinction between jitter-cost noninferiority and a negative model gap, and numerical reporting. Sixteen initial scan/protocol tests pass, and 15 reporting/packaging tests pass after the reporting addition. Prepared 0.1-scale and existing zero-scale jobs match all 50 full-endpoint identities. No core physics code changed. New outputs remain in `results/journal_campaign_06/`; G2 will close only after all scales and final analyses are verified.
