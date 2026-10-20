#!/usr/bin/env python3
"""Round-4 evidence manifest: the round-3 manifest plus the campaign-05 artifacts (key -> path, SHA-256).

Round-3 entries are carried over unchanged, except for the builder keys re-pointed to the current-point (S = 0.95)
recomputations of F7. Each re-pointed artifact stays recorded under a ``historical_`` key, so its S = 0.85 values
remain citable as labelled history. With ``--require-all`` every declared round-4 artifact must exist. Paths are
repository relative.
"""
import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROUND3 = REPO / "docs/paper/revision_manifest_round3.json"
C5 = "results/journal_campaign_05"

ROUND4 = {
    "round4_protocol": "docs/paper/round4_protocol.json",
    "round4_reproduction": f"{C5}/f1_reproduction.json",
    "round4_points": f"{C5}/points/points.json",
    "round4_ablation": f"{C5}/f2_ablation.json",
    "round4_points_test": f"{C5}/f3_points.json",
    "round4_associations": f"{C5}/f4_associations.json",
    "round4_loss_locations": f"{C5}/f5_loss_locations.json",
    "round4_ring5501_chamber": f"{C5}/f5_ring5501_chamber_check.json",
    "round4_dispersion_scope": f"{C5}/f6_dispersion_scope.json",
    "round4_vertical_steering": f"{C5}/f2v_vertical_sensitivity.json",
}

# F7: builder keys re-pointed to the current point (x_inj -19.478 mm, S = 0.95, window 0.443 mrad).
OVERRIDES = {
    "round2_pulse": f"{C5}/f7/f7_pulse.json",
    "round2_transparency": f"{C5}/f7/f7_transparency_resolved.json",
    "round2_stored_tracked": f"{C5}/f7/f7_stored_beam_end_turns.json",
    "round3_transparency_mc": f"{C5}/f7/f7_transparency_mc.json",
    "c7_analytic": f"{C5}/f7/f7_transparency_analytic.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def point_identity(artifacts):
    """Operating-point identity check: every current-point artifact must carry the selected point's injection
    position and field scale (round3_operating_point), not only a matching hash. Returns the checked keys."""
    ref = json.loads((REPO / artifacts["round3_operating_point"]).read_text())
    checked = []
    for key in OVERRIDES:
        cfg = json.loads((REPO / artifacts[key]).read_text())["study_config"]
        for name in ("injection_x_m", "field_scale"):
            if abs(cfg[name] - ref[name]) > 1e-12:
                raise SystemExit(f"point identity: {key} has {name}={cfg[name]}, selected point {ref[name]}")
        checked.append(key)
    return checked


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--require-all", action="store_true")
    a = p.parse_args(argv)
    base = json.loads(ROUND3.read_text())
    artifacts, digests = dict(base["artifacts"]), dict(base["sha256"])
    missing = []
    for key, rel in {**ROUND4, **OVERRIDES}.items():
        if not (REPO / rel).exists():
            missing.append(key)
    if a.require_all and missing:
        raise SystemExit(f"missing round-4 artifacts: {missing}")
    for key, rel in OVERRIDES.items():
        if key in artifacts and key not in missing:
            artifacts[f"historical_{key}"], digests[f"historical_{key}"] = artifacts[key], digests[key]
    for key, rel in {**ROUND4, **OVERRIDES}.items():
        if key not in missing:
            artifacts[key] = rel
            digests[key] = sha256(REPO / rel)
    for key, rel in artifacts.items():  # every recorded file must still match its recorded hash
        if sha256(REPO / rel) != digests[key]:
            raise SystemExit(f"hash mismatch: {key} -> {rel}")
    checked = point_identity(artifacts)
    out = {"description": "Round-4 evidence: round-3 manifest plus campaign-05 artifacts (protocol, ablation, point "
                          "test, associations, loss locations, dispersion scope, two-plane steering sensitivity) and the "
                          "current-point pulse and transparency recomputations; S = 0.85 originals kept as historical_*",
           "artifacts": artifacts, "sha256": digests}
    a.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"recorded": len(artifacts), "round4": len(ROUND4), "overridden": len(OVERRIDES), "missing": missing,
                      "point_identity_checked": checked}))


if __name__ == "__main__":
    main()
