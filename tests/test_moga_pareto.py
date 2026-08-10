import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm.moga import (
    BTSMOGAConfig,
    run_bts_moga,
    reevaluate_pareto_finalists,
    plot_moga_summary,
    compute_true_aperture_margin
)

def test_moga_nondominated_sorting():
    from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
    # Test NonDominatedSorting logic directly on a known non-dominated matrix
    pareto_f = np.array([
        [1.0, 10.0, 0.5],
        [2.0, 5.0, 0.2],
        [3.0, 2.0, 0.1]
    ])
    nds = NonDominatedSorting().do(pareto_f, only_non_dominated_front=True)
    assert len(nds) == len(pareto_f)
    assert np.allclose(np.sort(nds), np.arange(len(pareto_f)))

def test_reevaluate_pareto_finalists():
    cfg = BTSMOGAConfig(pop_size=10, n_gen=3, seed=42)
    res = run_bts_moga(cfg)
    assert res.success
    reevaluate_pareto_finalists(res, n_particles=100, n_mc_seeds=2)
    assert len(res.finalist_evaluations) > 0
    for key, eval_data in res.finalist_evaluations.items():
        assert "mean_transmission" in eval_data
        assert "min_clearance" in eval_data
        assert "tracking_std" in eval_data

def test_aperture_margin_computation():
    cfg = BTSMOGAConfig(aperture_radius_m=0.01935, emittance_x_mrad=1.0e-7, energy_spread=1.1e-3)
    margin = compute_true_aperture_margin(beta_m=30.0, disp_m=0.1, config=cfg)
    envelope = 3.0 * np.sqrt(1.0e-7 * 30.0) + abs(0.1 * 1.1e-3)
    expected = 0.01935 - envelope
    assert np.isclose(margin, expected)
    
def test_plot_moga_summary(tmp_path):
    cfg = BTSMOGAConfig(pop_size=10, n_gen=3, seed=42)
    res = run_bts_moga(cfg)
    plot_moga_summary(res, save_dir=tmp_path)
    # Check if a figure is saved
    assert any(tmp_path.glob("*.png"))

