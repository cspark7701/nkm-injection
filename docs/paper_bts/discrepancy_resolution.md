# Reviewer discrepancy resolutions

- **BC01**: Matched reference: peaks 31.4368/50.7459 m; matching precision is numerical. Exact pointer: `/final_max_beta_y_m`.
- **BC02**: Nominal plus two random starts: feasible success, infeasible success, evaluation-budget failure; no volume estimate. Exact pointer: `/1/optimizer_success`.
- **BC03**: Median interval uses order statistics, not pooled bootstrap. Exact pointer: `/pooled/quantiles/mismatch_x/p50_ci`.
- **BC04**: Five optical-rule exceedances; exact asymmetric interval, not physical losses. Exact pointer: `/pooled/failures/clopper_pearson`.
- **BC05**: 1421.636 is a mixed-unit raw sensitivity condition number; achieved correction claims withdrawn until validated. Exact pointer: `/sensitivity/condition_number`.
- **BC06**: OAT mean absolute change of Mx+My: beta-only entrance error, gradient, energy; alpha fixed. Exact pointer: `/sensitivity_ranking`.
- **BC07**: Three main bends plus kicker and two septa; 36 elements, 21.789 m from model. Exact pointer: `/bts_config/ang_b3`.
- **BC08**: Configured entrance at m1; physical source unresolved. Exact pointer: `/target_config/init_beta_x`.
- **BC09**: Configured parametric target at m4; not derived from ring NKM centre. Exact pointer: `/target_config/target_beta_x`.
- **BC10**: 50k prefixes missed 1e-5 target; 400k passed; not tail convergence. Exact pointer: `/runs/seed42/prefix`.
- **BC11**: Family bounds and bore are modelling assumptions, not verified hardware. Exact pointer: `/constraint_config/quad_bounds`.
- **BC12**: Archived raw strengths retained; rounded settings require reevaluation. Exact pointer: `/optimized_strengths_by_name_m_minus2`.

Historical feasibility uses beta >60.01 m or Mx+My >2.05. All five records exceed vertical beta only. Wilson 95% limits are [3.8831e-6, 2.1283e-5]; exact limits are asymmetric [2.95e-6, 2.12e-5]. No symmetric ± approximation is retained. Source limitations are not resolved by hash verification.
