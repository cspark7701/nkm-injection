# Local normalized response and correction-claim withdrawal — R1-BTS-07

[Selected response and finite checks](generated/normalized_response.json). Raw results in `results/bts_journal_campaign_r1_20261013/response/`; reproduce with `python scripts/run_bts_journal_revision.py --stage response --output-dir results/<new>/response`.

Rows are beta_x, beta_y, alpha_x, alpha_y, Dx, Dpx, divided by [.05 m,.05 m,.01,.01,.002 m,.001]. Columns multiply derivatives by .01 m^-2, an assumed tuning increment common to all nine independent quadrupoles. The dimensionless matrix is A_ij=(dO_i/dK_j) DeltaK_j / sigma_i. This convention differs from the archived mixed-unit matrix and its condition number1421.636.

Central steps1e-4,1e-5,1e-6 m^-2 have relative convergence [5.281912109751257e-09, 4.600365419889125e-09, 0.0]. The normalized condition number is 57.7807; six singular values [18.12498428076684, 7.156357882167073, 2.1440243979156204, 0.975662224208595, 0.476934526126971, 0.3136855601090855] are above the relative1e-10 rank threshold. Full Vt has a three-dimensional local null space with arbitrary vector signs. Right-vector Euclidean orthogonality uses the declared actuator scales and does not establish decoupled finite optical corrections.

All six small finite response perturbations remain in bounds and differ from linear predictions by less than1%. Raw vectors, actual changes and saturation checks are recorded. These are local diagnostic checks, not an operational correction demonstration.

**Withdrawn claims:** achieved commissioning knobs, measured optical observability, independently decoupled dispersion control, shot-by-shot retuning, and correction gains under alignment errors. No measurement system or optical-estimation uncertainty is assumed to be available. Implementing correction would require diagnosed optical errors, calibration and constrained finite reevaluation; it is outside the final scope. The physical contribution is instead the frozen nominal/margin design comparison of R1-BTS-08.
