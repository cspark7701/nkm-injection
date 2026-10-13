"""Round-3 ring correction helpers on a small FODO ring (units: m, rad, m^-2)."""
import at
import numpy as np
import pytest

from nkm_injection.ring_error_scenario import (bpm_orbit, bpm_reference_offsets, correct_optics,
                                               correct_orbit_converged, response_matrix)


def fodo_ring(cells=8):
    elems = []
    for c in range(cells):
        elems += [at.Marker("BPM"), at.Quadrupole("QF", 0.3, 0.6), at.Drift("D", 0.6),
                  at.Corrector("HVC", 0.0, [0.0, 0.0]), at.Drift("D", 0.6),
                  at.Quadrupole("QD", 0.3, -0.6), at.Drift("D", 0.6), at.Dipole("B", 0.5, 2 * np.pi / cells), at.Drift("D", 0.6)]
    return at.Lattice(elems, energy=3e9)


def test_reference_offsets_follow_nearest_quadrupole_shift():
    r = fodo_ring()
    bpms = [i for i, e in enumerate(r) if e.FamName == "BPM"]
    q0 = next(i for i, e in enumerate(r) if e.FamName == "QF")
    errors = {"magnets": [{"index": i, "dx_m": 1e-4 if i == q0 else 0.0, "dy_m": 0.0}
                          for i, e in enumerate(r) if isinstance(e, at.Quadrupole)]}
    off = bpm_reference_offsets(r, errors, bpms)
    assert off[0] == pytest.approx(1e-4) and np.all(off[1:len(bpms)] == 0.0)


def test_converged_orbit_correction_reduces_rms_and_reports_termination():
    r = fodo_ring()
    bpms = np.array([i for i, e in enumerate(r) if e.FamName == "BPM"])
    cors = np.array([i for i, e in enumerate(r) if isinstance(e, at.Corrector)])
    resp = response_matrix(r, bpms, cors)
    at.set_shift([r[1]], 5e-5, 3e-5)  # displaced QF source
    before = bpm_orbit(r, bpms)
    res = correct_orbit_converged(r, bpms, cors, resp)
    after = bpm_orbit(r, bpms)
    assert np.sqrt(np.mean(after ** 2)) < 0.2 * np.sqrt(np.mean(before ** 2))
    assert res["history"][-1]["rms_x_m"] <= res["history"][0]["rms_x_m"]
    assert "termination" in res and not res["saturated"]


def test_optics_correction_reduces_beta_beat():
    r = fodo_ring()
    bpms = np.array([i for i, e in enumerate(r) if e.FamName == "BPM"])
    quads = np.array([i for i, e in enumerate(r) if isinstance(e, at.Quadrupole)])
    _, _, l0 = r.get_optics(refpts=bpms)
    r[quads[3]].PolynomB[1] *= 1.01
    res = correct_optics(r, bpms, quads, l0.beta.copy(), l0.dispersion[:, 0].copy())
    first, last = res["history"][0]["beta_beat_rms"], res["history"][-1]["beta_beat_rms"]
    assert max(last) < 0.2 * max(first)
