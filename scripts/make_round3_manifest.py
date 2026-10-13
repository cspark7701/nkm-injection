#!/usr/bin/env python3
"""Round-3 evidence manifest: the round-2 selection plus the campaign-04 artifacts (key -> path, SHA-256).

Round-2 entries are carried over unchanged (campaign 03 stays frozen). Campaign-04 entries are added when present;
with ``--require-all`` every declared round-3 artifact must exist. Paths are repository relative.
"""
import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROUND2 = REPO / "docs/paper/revision_manifest_round2.json"
C4 = "results/journal_campaign_04"

ROUND3 = {
    # E4: in-magnet NKM chamber
    "round3_chamber_config": "docs/paper/round3_chamber_config.json",
    "round3_nkm_chamber_scan": f"{C4}/e4_nkm_chamber_scan/nkm_chamber_scan.json",
    "round3_aperture_normalisation": f"{C4}/e4_aperture_normalisation.json",
    # E9: simultaneous wire/current errors and septum leakage allowance
    "round3_transparency_mc": f"{C4}/e9_transparency_mc.json",
    # E5: corrected ring population
    "round3_ring_summary": f"{C4}/e5_corrected_ring/corrected_ring_summary.json",
    **{f"round3_ring_{s}": f"{C4}/e5_corrected_ring/seed{s}.json" for s in range(5501, 5511)},
    **{f"round3_ring_lattice_{s}": f"{C4}/e5_corrected_ring/seed{s}.mat" for s in range(5501, 5511)},
    # E6: operating-point re-selection and the per-point studies at the selected point
    "round3_selection": f"{C4}/e6_operating_point/operating_point_selection.json",
    "round3_operating_point": f"{C4}/e6_operating_point/operating_point_selected_b2.json",
    "round3_operating_point_b1": f"{C4}/e6_operating_point/operating_point_selected_b1.json",
}

# Round-2 builder keys re-pointed to the campaign-04 reruns, so the round-2 reporting code serves round 3. Applied only
# when the campaign-04 file exists; the round-2 artifact otherwise stays selected.
OVERRIDES = {
    "round2_window": f"{C4}/e6_window/window_summary.json",
    "round2_edge_offsets": f"{C4}/e6_edge_offsets.json",
    "round2_trajectory_final": f"{C4}/e6_trajectory.json",
    "round2_validation": f"{C4}/e6_validation/validation_summary.json",
    "round2_backend_contract": f"{C4}/e6_validation/backend_contract.json",
    "round2_chamber_ideal": f"{C4}/e6_chamber_ideal/chamber_summary.json",
    "round2_chamber_corrected": f"{C4}/e6_chamber_corrected/chamber_summary.json",
    "round2_robustness": f"{C4}/e7_final_statistics.json",
    "round2_tuning": f"{C4}/e7_tuning/tuning_summary.json",
    "round2_tuning_inputs": f"{C4}/e7_tuning/tuning_inputs.json",
    **{f"round2_errors_{s}": f"{C4}/e7_seed{s}/capture_robustness_raw.json" for s in (42, 123, 777)},
    **{f"round2_errors_{s}_summary": f"{C4}/e7_seed{s}/capture_robustness_summary.json" for s in (42, 123, 777)},
    **{f"round2_errors_{s}_inputs": f"{C4}/e7_seed{s}/checkpoint_inputs.json" for s in (42, 123, 777)},
    **{f"round2_jitter_{j}{x}": f"{C4}/e7_jitter_{j}/{f}" for j in ("0", "0.25", "0.5", "0.75", "x_only", "xp_only")
       for x, f in (("", "capture_robustness_raw.json"), ("_summary", "capture_robustness_summary.json"),
                    ("_inputs", "checkpoint_inputs.json"))},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--require-all", action="store_true")
    p.add_argument("--extra", nargs="*", default=[], help="additional key=path entries (repository relative)")
    a = p.parse_args(argv)
    base = json.loads(ROUND2.read_text())
    artifacts, digests = dict(base["artifacts"]), dict(base["sha256"])
    declared = dict(ROUND3)
    for item in a.extra:
        key, path = item.split("=", 1)
        declared[key] = path
    missing = []
    for key, rel in declared.items():
        path = REPO / rel
        if not path.exists():
            missing.append(key)
            continue
        artifacts[key] = rel
        digests[key] = sha256(path)
    overridden = []
    for key, rel in OVERRIDES.items():
        path = REPO / rel
        if path.exists():
            artifacts[key] = rel; digests[key] = sha256(path); overridden.append(key)
        else:
            missing.append(key)
    if a.require_all and missing:
        raise SystemExit(f"missing round-3 artifacts: {missing}")
    out = {"description": "Round-3 evidence: round-2 selection (campaign 03, unchanged) plus campaign-04 artifacts "
                          "(in-magnet NKM chamber, corrected ring population, re-selected operating point, final "
                          "robustness rerun)", "artifacts": artifacts, "sha256": digests}
    a.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"recorded": len(artifacts), "overridden": len(overridden), "round3_missing": missing}))


if __name__ == "__main__":
    main()
