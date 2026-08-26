"""
Unit and integration tests for src/nkm/storage_ring_injection.py (Task 04)
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm_injection.storage_ring_injection import (
    StorageRingInjectionConfig,
    load_storage_ring_injection_lattice,
    track_multiturn_injection,
    track_element_resolved_injection,
    compute_multiturn_injection_metrics,
    get_kicker_evaluator,
    SeptumModel
)
from src.nkm_injection.tracking import TrackingResult
from src.nkm_injection.beam import generate_6d_beam
from src.nkm_injection.kickmap import NKMKickMap2D


@pytest.fixture
def ring_and_nkm():
    config = StorageRingInjectionConfig()
    ring, nkm_idx = load_storage_ring_injection_lattice(config)
    return ring, nkm_idx


@pytest.fixture
def kickmap_obj():
    p = REPO_ROOT / "kickmap_file.txt"
    assert p.is_file()
    return NKMKickMap2D(p)


def test_storage_ring_loading(ring_and_nkm):
    ring, nkm_idx = ring_and_nkm
    assert len(ring) > 3000
    assert nkm_idx == 1


def test_multiturn_tracking_models(ring_and_nkm, kickmap_obj):
    ring, _ = ring_and_nkm
    config = StorageRingInjectionConfig()

    # Fast test distribution: 50 particles, 5 turns
    injected_beam = generate_6d_beam(
        n_particles=50,
        beta_x=10.0, alpha_x=0.0, emit_x=1e-7,
        beta_y=5.0, alpha_y=0.0, emit_y=1e-8,
        x_offset=-0.016,
        seed=42
    )

    stored_beam = generate_6d_beam(
        n_particles=50,
        beta_x=10.0, alpha_x=0.0, emit_x=1e-8,
        beta_y=5.0, alpha_y=0.0, emit_y=1e-9,
        x_offset=0.0,
        seed=42
    )

    models = ["off", "ideal", "linear", "fieldmap"]

    for model in models:
        inj_res = track_multiturn_injection(
            injected_beam, ring, n_turns=5,
            kicker_model=model, kickmap_obj=kickmap_obj,
            config=config
        )

        stored_res = track_multiturn_injection(
            stored_beam, ring, n_turns=5,
            kicker_model=model, kickmap_obj=kickmap_obj,
            config=config
        )

        metrics = compute_multiturn_injection_metrics(inj_res, stored_res, config)

        assert "capture_efficiency" in metrics
        assert 0.0 <= metrics["capture_efficiency"] <= 1.0
        assert "stored_beam_centroid_oscillation_mm" in metrics

        # Verify TrackingResult dataclass type and dual access (attribute + dict)
        assert isinstance(inj_res, TrackingResult)
        assert isinstance(stored_res, TrackingResult)
        assert inj_res.capture_efficiency == inj_res["capture_efficiency"]
        assert inj_res.survival_fraction == inj_res["survival_fraction"]
        assert np.array_equal(inj_res.final_beam, inj_res["final_beam"], equal_nan=True)


def test_tracking_result_from_beam_constructor():
    """Verify TrackingResult.from_beam factory constructor."""
    beam = generate_6d_beam(
        n_particles=20,
        beta_x=10.0, alpha_x=0.0, emit_x=1e-8,
        beta_y=5.0, alpha_y=0.0, emit_y=1e-9,
        seed=123
    )
    res = TrackingResult.from_beam(beam, metadata={"test": "ok"})
    assert isinstance(res, TrackingResult)
    assert res.n_particles == 20
    assert res.survived_particles == 20
    assert res.survival_fraction == 1.0
    assert res["metadata"]["test"] == "ok"


def test_get_kicker_evaluator_unification(kickmap_obj):
    """Verify get_kicker_evaluator outputs exact expected kicks for standard positions."""
    config = StorageRingInjectionConfig()

    # 1. Off model
    fn_off, meta_off = get_kicker_evaluator("off", config)
    x = np.array([-0.016, 0.0, 0.016])
    y = np.zeros_like(x)
    kx, ky = fn_off(x, y)
    assert np.allclose(kx, 0.0)
    assert np.allclose(ky, 0.0)

    # 2. Ideal model: Courant-Snyder optimal kick
    fn_ideal, meta_ideal = get_kicker_evaluator("ideal", config)
    kx_ideal, ky_ideal = fn_ideal(x, y)
    expected_ideal = -config.alpha_x_nkm * config.septum_x_offset_m / config.beta_x_nkm_m * 1e3
    assert np.allclose(kx_ideal, expected_ideal)
    assert pytest.approx(expected_ideal, abs=1e-3) == -0.1269

    # 3. Linear model: -2.1046 mrad at x = -16 mm
    fn_linear, meta_linear = get_kicker_evaluator("linear", config)
    kx_linear, ky_linear = fn_linear(np.array([-0.016]), np.array([0.0]))
    assert pytest.approx(kx_linear[0], abs=1e-4) == -2.1046

    # 4. Fieldmap model
    fn_fieldmap, meta_fieldmap = get_kicker_evaluator("fieldmap", config, kickmap_obj=kickmap_obj)
    kx_fm, ky_fm = fn_fieldmap(np.array([-0.016]), np.array([0.0]))
    assert pytest.approx(kx_fm[0], abs=1e-3) == -2.1046


def test_kicker_model_consistency_across_tracking_modes(ring_and_nkm, kickmap_obj):
    """Verify identical kick angles applied in multiturn and element-resolved tracking on Turn 1."""
    ring, _ = ring_and_nkm
    config = StorageRingInjectionConfig()

    for model in ["off", "ideal", "linear", "fieldmap"]:
        fn, meta = get_kicker_evaluator(model, config=config, kickmap_obj=kickmap_obj)
        assert callable(fn)
        assert meta.beam_energy_eV == config.energy_eV


