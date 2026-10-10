#!/usr/bin/env python3
"""Write the revision campaign manifest (key -> repository-relative path, SHA-256) for build_revision_figures.py.

Only artifacts that exist are recorded unless --require-all is given. Paths are repository-relative.
"""
import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
C1, C2 = "results/journal_campaign_01", "results/journal_campaign_02"
ARTIFACTS = {
    "backend_validation": f"{C1}/backend_validation/backend_validation_summary.json",
    "backend_validation_raw": f"{C1}/backend_validation/backend_validation_raw.json",
    "operating_point_3d": f"{C2}/operating_point_3d.json",
    "kicker_validation": f"{C2}/c1_kicker_validation/kicker_model_validation.json",
    "vertical_diagnostic": f"{C2}/c1_vertical_diagnostic/kicker_model_validation.json",
    "mechanism": f"{C2}/c2_mechanism/finite_length_mechanism.json",
    "c3_grid": f"{C2}/c3_operating_window/grid_raw.json",
    "c3_validate": f"{C2}/c3_operating_window/validate_raw.json",
    "c3_angle": f"{C2}/c3_operating_window/angle_raw.json",
    "c3_position": f"{C2}/c3_operating_window/position_raw.json",
    "c3_acceptance": f"{C2}/c3_operating_window/acceptance_raw.json",
    "c3_nkm_offset": f"{C2}/c3_operating_window/nkm_offset_raw.json",
    "c3_emittance": f"{C2}/c3_operating_window/emittance_raw.json",
    "c4_particles": f"{C2}/c4_survival/particles_raw.json",
    "c4_longturn": f"{C2}/c4_survival/longturn_raw.json",
    "c4_aperture": f"{C2}/c4_survival/aperture_raw.json",
    "c4_ring_errors": f"{C2}/c4_survival/ring_errors_raw.json",
    "c4_aper_y10": f"{C2}/c4_aperture_diag_y10/aperture_raw.json",
    "c4_aper_xopen": f"{C2}/c4_aperture_diag_xopen/aperture_raw.json",
    "c4_aper_xopen_novert": f"{C2}/c4_aperture_diag_xopen_novert/aperture_raw.json",
    "c4_aper_open_novert": f"{C2}/c4_aperture_diag_open_novert/aperture_raw.json",
    "c5_raw_42": f"{C2}/c5_errors_seed42/capture_robustness_raw.json",
    "c5_raw_123": f"{C2}/c5_errors_seed123/capture_robustness_raw.json",
    "c5_raw_777": f"{C2}/c5_errors_seed777/capture_robustness_raw.json",
    "c5_summary_42": f"{C2}/c5_errors_seed42/capture_robustness_summary.json",
    "c6_raw_0": f"{C2}/c6_jitter_0/capture_robustness_raw.json",
    "c6_raw_0.25": f"{C2}/c6_jitter_0.25/capture_robustness_raw.json",
    "c6_raw_0.5": f"{C2}/c6_jitter_0.5/capture_robustness_raw.json",
    "c6_raw_0.75": f"{C2}/c6_jitter_0.75/capture_robustness_raw.json",
    "c6_raw_x_only": f"{C2}/c6_jitter_x_only/capture_robustness_raw.json",
    "c6_raw_xp_only": f"{C2}/c6_jitter_xp_only/capture_robustness_raw.json",
    "c7_analytic": f"{C2}/c7_transparency/transparency_analytic.json",
    "c7_tracked": f"{C2}/c7_transparency/stored_beam_tracked.json",
    "tolerance_replicates": f"{C1}/followup_analysis/tolerance_replicates_with_400k.json",
    "error_budget": f"{C1}/error_budget.json",
    "optimization_summary": "backups_20261009/production_statistical_01/optimization/bts_optimization_summary.json",
}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--require-all", action="store_true")
    a = p.parse_args(argv)
    art, sha, missing = {}, {}, []
    for k, rel in ARTIFACTS.items():
        f = REPO / rel
        if not f.exists():
            missing.append(k)
            continue
        art[k] = rel
        sha[k] = hashlib.sha256(f.read_bytes()).hexdigest()
    if missing and a.require_all:
        raise SystemExit(f"missing artifacts: {missing}")
    a.output.write_text(json.dumps({"description": "Revision campaign 02 evidence selected for the revised manuscript",
                                    "artifacts": art, "sha256": sha}, indent=2) + "\n")
    print(json.dumps({"recorded": len(art), "missing": missing}))


if __name__ == "__main__":
    main()
