# Interior beta extrema — R2-BTS-04

[Exported results](generated/round2_spatial.json); reproduce `python scripts/run_bts_round2.py --stage spatial --output-dir results/<new>/spatial`. Exact nominal hard-edge maps are sampled inside each finite element at8/16/32/64 subdivisions, with bend edges applied only once. The endpoint map remains unchanged; this is spatial observation refinement, not integrator-step convergence.

Reference boundary peaks31.4368/50.7459 m become31.6290/51.2699 m at64 subdivisions. The old alternative's33.5795/28.1800 m become33.7652/28.4955 m. These finite meshes approximate continuous maxima and expose the boundary sampling bias. They are not analytical proof of exact extrema.

Refining the low-beta objective on16 subdivisions converges in34 SLSQP iterations with exit residual equalities, horizontal beta<=60 m and unchanged family bounds. The new64-subdivision peaks are33.7945/28.4371 m.32-to64 changes are below0.00035 m, well below the declared0.02 m check. The active lower bound remains q32=-3 m^-2. Normalized independent-map exit residuals are below3e-10; the new setting and original setting are both retained in the campaign. No global optimum is asserted. New comparison uses the refined setting, not the old alternative relabelled as spatially converged.
