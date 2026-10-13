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
    if a.require_all and missing:
        raise SystemExit(f"missing round-3 artifacts: {missing}")
    out = {"description": "Round-3 evidence: round-2 selection (campaign 03, unchanged) plus campaign-04 artifacts "
                          "(in-magnet NKM chamber, corrected ring population, re-selected operating point, final "
                          "robustness rerun)", "artifacts": artifacts, "sha256": digests}
    a.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"recorded": len(artifacts), "round3_missing": missing}))


if __name__ == "__main__":
    main()
