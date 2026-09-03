"""
Unit Tests for Task 06 — Converged Multi-Turn Injection Studies
Tests smoke/pilot/production config separation, bootstrap CI, convergence scans.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm_injection.convergence_study import (
    smoke_config,
    pilot_config,
    production_config,
    bootstrap_capture_ci,
    particle_count_convergence_scan,
    turn_count_convergence_scan,
    compute_first_loss_turn_distribution,
    compute_stored_beam_perturbation,
    compute_injection_acceptance,
    run_ensemble_study,
)
from src.nkm_injection.storage_ring_injection import (
    StorageRingInjectionConfig,
    load_storage_ring_injection_lattice,
    track_multiturn_injection,
    TrackingResult,
)
from src.nkm_injection.beam import generate_6d_beam


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def ring_and_config():
    cfg = StorageRingInjectionConfig()
    ring, nkm_idx = load_storage_ring_injection_lattice(cfg)
    return ring, cfg


# ---------------------------------------------------------------------------
# Config Separation Tests
# ---------------------------------------------------------------------------

class TestTierConfigs:
    def test_smoke_tier(self):
        t = smoke_config()
        assert t.n_particles == 100
        assert t.n_turns == 10
        assert t.label == "smoke"

    def test_pilot_tier(self):
        t = pilot_config()
        assert t.n_particles == 1000
        assert t.n_turns == 100
        assert t.label == "pilot"

    def test_production_tier(self):
        t = production_config()
        assert t.n_particles >= 10000
        assert t.n_turns >= 1000
        assert t.label == "production"

    def test_production_has_multiple_seeds(self):
        t = production_config()
        assert len(t.seeds) >= 3, "Production tier should use at least 3 seeds for bootstrap CI."

    def test_tiers_are_strictly_ordered(self):
        s, p, pr = smoke_config(), pilot_config(), production_config()
        assert s.n_particles < p.n_particles < pr.n_particles
        assert s.n_turns < p.n_turns < pr.n_turns


# ---------------------------------------------------------------------------
# Bootstrap CI Tests
# ---------------------------------------------------------------------------

class TestBootstrapCI:
    def test_deterministic_with_fixed_rng(self):
        survived = [95, 90, 88, 92, 85]
        rng = np.random.default_rng(42)
        res = bootstrap_capture_ci(survived, n_particles=100, rng=rng)
        assert "mean" in res and "ci_lo" in res and "ci_hi" in res and "ci_level" in res
        assert 0.0 < res["ci_lo"] <= res["mean"] <= res["ci_hi"] <= 1.0

    def test_ci_width_with_single_seed(self):
        """Bootstrap CI collapses to zero width when only one seed is used."""
        res = bootstrap_capture_ci([80], n_particles=100, rng=np.random.default_rng(0))
        assert res["n_seeds"] == 1
        assert res["std"] == 0.0

    def test_mean_matches_average_efficiency(self):
        survived = [500, 600, 700]
        n_part = 1000
        res = bootstrap_capture_ci(survived, n_particles=n_part, rng=np.random.default_rng(0))
        expected_mean = np.mean([0.5, 0.6, 0.7])
        assert abs(res["mean"] - expected_mean) < 1e-10

    def test_95_percent_ci_level(self):
        survived = [480, 520, 510, 490, 500]
        res = bootstrap_capture_ci(survived, n_particles=1000, ci_level=0.95)
        assert res["ci_level"] == 0.95


# ---------------------------------------------------------------------------
# Convergence Scan Tests
# ---------------------------------------------------------------------------

class TestConvergenceScans:
    def test_particle_count_scan_returns_correct_shape(self, ring_and_config):
        ring, config = ring_and_config
        results = particle_count_convergence_scan(
            n_particle_values=[50, 100],
            n_turns=5,
            ring=ring,
            kicker_model="off",
            kickmap_obj=None,
            config=config,
            seed=42
        )
        assert len(results) == 2
        assert all("n_particles" in r and "capture_efficiency" in r for r in results)

    def test_turn_count_scan_returns_correct_shape(self, ring_and_config):
        ring, config = ring_and_config
        results = turn_count_convergence_scan(
            n_turn_values=[2, 5],
            n_particles=50,
            ring=ring,
            kicker_model="off",
            kickmap_obj=None,
            config=config,
            seed=42
        )
        assert len(results) == 2
        assert all("n_turns" in r and "capture_efficiency" in r for r in results)


# ---------------------------------------------------------------------------
# First-Loss Turn Distribution Tests
# ---------------------------------------------------------------------------

class TestFirstLossTurnDistribution:
    def test_with_no_losses(self):
        res = TrackingResult(
            particles_6d=np.zeros((6, 100)),
            n_particles=100,
            survived_particles=100,
            survival_fraction=1.0,
            centroid=None,
            emittance_x_mrad=0.0,
            emittance_y_mrad=0.0,
            centroid_history=np.zeros((10, 2)),
            emittance_history=np.zeros((10, 2)),
            survival_history=[100] * 10,
            loss_log=[],
            metadata={}
        )
        dist = compute_first_loss_turn_distribution(res, n_turns=10)
        assert dist["n_lost_particles"] == 0
        assert dist["first_loss_turns"] == []

    def test_with_known_losses(self):
        loss_log = [
            {"particle_index": 0, "turn": 1, "cause": "aperture_exceeded"},
            {"particle_index": 1, "turn": 1, "cause": "aperture_exceeded"},
            {"particle_index": 2, "turn": 3, "cause": "aperture_exceeded"},
        ]
        res = TrackingResult(
            particles_6d=np.zeros((6, 100)),
            n_particles=100, survived_particles=97, survival_fraction=0.97,
            centroid=None, emittance_x_mrad=0.0, emittance_y_mrad=0.0,
            centroid_history=np.zeros((5, 2)), emittance_history=np.zeros((5, 2)),
            survival_history=[100, 99, 98, 97, 97], loss_log=loss_log, metadata={}
        )
        dist = compute_first_loss_turn_distribution(res, n_turns=5)
        assert dist["n_lost_particles"] == 3
        assert dist["fraction_lost_on_turn_1"] == pytest.approx(2 / 3)


# ---------------------------------------------------------------------------
# Stored-Beam Perturbation Tests
# ---------------------------------------------------------------------------

class TestStoredBeamPerturbation:
    def test_zero_perturbation_for_constant_centroid(self):
        n_turns = 10
        cent_hist = np.zeros((n_turns, 2))
        emit_hist = np.full((n_turns, 2), 1e-8)
        res = TrackingResult(
            particles_6d=np.zeros((6, 100)),
            n_particles=100, survived_particles=100, survival_fraction=1.0,
            centroid=None, emittance_x_mrad=1e-8, emittance_y_mrad=1e-9,
            centroid_history=cent_hist, emittance_history=emit_hist,
            survival_history=[100] * n_turns, loss_log=[], metadata={}
        )
        pert = compute_stored_beam_perturbation(res)
        assert pert["centroid_oscillation_x_mm"] == pytest.approx(0.0, abs=1e-12)
        assert pert["emittance_growth_x_percent"] == pytest.approx(0.0, abs=1e-10)


# ---------------------------------------------------------------------------
# Ensemble Study Integration Test (smoke tier, off kicker)
# ---------------------------------------------------------------------------

class TestEnsembleStudy:
    def test_smoke_ensemble_off_kicker(self, ring_and_config):
        ring, config = ring_and_config
        tier = smoke_config()
        tier.n_turns = 3  # Minimize runtime for unit tests

        result = run_ensemble_study(
            tier=tier,
            ring=ring,
            kicker_model="off",
            kickmap_obj=None,
            config=config,
            stored_beam_n_particles=50
        )

        assert result["kicker_model"] == "off"
        ci = result["capture_efficiency_ci"]
        assert 0.0 <= ci["mean"] <= 1.0
        assert ci["ci_lo"] <= ci["mean"] <= ci["ci_hi"]
        assert len(result["per_seed_results"]) == len(tier.seeds)


class TestMatchedTwissParameterization:
    def test_injected_beam_twiss_propagation(self, ring_and_config):
        ring, config = ring_and_config
        assert hasattr(config, "inj_beta_x_m")
        assert hasattr(config, "inj_alpha_x")
        assert hasattr(config, "inj_emit_x_m")
        assert hasattr(config, "stored_beta_x_m")
        assert hasattr(config, "stored_alpha_x")

        # Verify defaults match BTS exit target Twiss
        assert pytest.approx(config.inj_beta_x_m, abs=1e-3) == 2.3365
        assert pytest.approx(config.inj_alpha_x, abs=1e-4) == -0.016335
        assert pytest.approx(config.stored_beta_x_m, abs=1e-3) == 16.197

    def test_custom_twiss_in_convergence_scan(self, ring_and_config):
        ring, _ = ring_and_config
        custom_cfg = StorageRingInjectionConfig(
            inj_beta_x_m=5.0,
            inj_alpha_x=0.5,
            inj_emit_x_m=5e-8
        )
        results = particle_count_convergence_scan(
            n_particle_values=[50],
            n_turns=2,
            ring=ring,
            kicker_model="off",
            kickmap_obj=None,
            config=custom_cfg,
            seed=42
        )
        assert len(results) == 1
        assert "capture_efficiency" in results[0]


# ---------------------------------------------------------------------------
# Task 13 — Structured Return Dataclass Tests
# ---------------------------------------------------------------------------

from src.nkm_injection.convergence_study import (
    ConvergenceScanResult,
    AcceptanceResult,
    EnsembleStudyResult,
)
import pandas as pd


class TestStructuredReturnTypes:
    def test_convergence_scan_result_methods_and_df(self):
        res = ConvergenceScanResult(
            scan_parameter="particle_count",
            scan_values=np.array([100, 500, 1000]),
            efficiencies=np.array([0.95, 0.98, 1.0]),
            survived_counts=np.array([95, 490, 1000]),
            cpu_times_s=np.array([0.1, 0.5, 1.0]),
            final_emittance_x=np.array([1.2e-7, 1.1e-7, 1.0e-7]),
            metadata={"n_turns": 10, "kicker_model": "fieldmap"}
        )
        assert len(res) == 3
        assert res.scan_parameter == "particle_count"
        assert pytest.approx(res.mean_efficiency()) == np.mean([0.95, 0.98, 1.0])
        assert res.std_efficiency() > 0.0

        # Dict / sequence access
        assert res[0]["n_particles"] == 100
        assert res[0]["survived"] == 95
        assert np.array_equal(res["n_particles"], [100, 500, 1000])
        assert np.allclose(res["efficiencies"], [0.95, 0.98, 1.0])
        assert res["n_turns"] == 10

        # DataFrame export
        df = res.to_dataframe()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert "n_particles" in df.columns
        assert "capture_efficiency" in df.columns
        assert "cpu_time_s" in df.columns

        # Serialization
        d = res.to_dict()
        assert d["scan_parameter"] == "particle_count"
        loaded = ConvergenceScanResult.from_dict(d)
        assert loaded.scan_parameter == "particle_count"
        assert np.array_equal(loaded.scan_values, res.scan_values)

    def test_acceptance_result_methods_and_df(self, ring_and_config):
        ring, config = ring_and_config
        res = compute_injection_acceptance(
            x_offsets_m=np.array([-0.020, -0.018, -0.016]),
            n_particles=20,
            n_turns=2,
            ring=ring,
            kicker_model="off",
            kickmap_obj=None,
            config=config,
            seed=42
        )
        assert isinstance(res, AcceptanceResult)
        assert len(res) == 3
        assert len(res.x_grid_m) == 3
        assert len(res.survival_fraction_grid) == 3

        # Dict / slice access
        assert "x_offset_mm" in res[0]
        assert "capture_efficiency" in res[0]
        assert len(res["x_offsets_mm"]) == 3

        # Acceptance window
        win_lo, win_hi = res.acceptance_window_mm(threshold=0.0)
        assert not np.isnan(win_lo)
        assert not np.isnan(win_hi)

        # DataFrame export
        df = res.to_dataframe()
        assert isinstance(df, pd.DataFrame)
        assert "x_offset_m" in df.columns
        assert "capture_efficiency" in df.columns

        # Serialization
        d = res.to_dict()
        loaded = AcceptanceResult.from_dict(d)
        assert np.array_equal(loaded.x_grid_m, res.x_grid_m)

    def test_ensemble_study_result_methods_and_df(self, ring_and_config):
        ring, config = ring_and_config
        tier = smoke_config()
        tier.n_turns = 2

        res = run_ensemble_study(
            tier=tier,
            ring=ring,
            kicker_model="off",
            kickmap_obj=None,
            config=config,
            stored_beam_n_particles=20
        )
        assert isinstance(res, EnsembleStudyResult)
        assert res.kicker_model == "off"
        assert "capture_efficiency_ci" in res
        assert "per_seed_results" in res
        assert "mean_stored_perturbation" in res
        assert res["label"] == "smoke"

        # DataFrame export
        df = res.to_dataframe()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(tier.seeds)
        assert "seed" in df.columns
        assert "capture_efficiency" in df.columns

        # Serialization
        d = res.to_dict()
        loaded = EnsembleStudyResult.from_dict(d)
        assert loaded.label == "smoke"
        assert loaded.kicker_model == "off"

