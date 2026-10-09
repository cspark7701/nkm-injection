import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

from scripts.inventory_protected_hashes import create_hash_manifest, verify_hash_manifest


@pytest.fixture(scope="module")
def baseline_metrics(tmp_path_factory):
    """Compute the reference metrics without requiring or writing repository results."""
    import scripts.record_baseline_metrics as producer
    output = tmp_path_factory.mktemp('baseline_metrics')
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(producer, 'OUTPUT_DIR', output)
        patch.setattr(producer, 'OUTPUT_JSON', output / 'baseline_metrics.json')
        patch.setattr(producer, 'OUTPUT_MD', output / 'baseline_metrics.md')
        producer.record_baseline()
    return json.loads((output / 'baseline_metrics.json').read_text())


def test_protected_files_manifest(tmp_path):
    """Verify versioned scientific digests and a complete temporary inventory."""
    inventory = create_hash_manifest(REPO_ROOT)
    reference = json.loads((REPO_ROOT / 'config/publication_input_hashes.json').read_text())
    assert all(inventory[name] == digest for name, digest in reference.items())
    manifest = tmp_path / 'protected_files_manifest.json'
    manifest.write_text(json.dumps(inventory))
    assert verify_hash_manifest(manifest)


def test_baseline_lattice_parameters(baseline_metrics):
    """Verify core BTS lattice baseline parameters."""
    bts = baseline_metrics["bts_lattice"]
    assert pytest.approx(bts["total_length_m"], abs=1e-3) == 21.789
    assert bts["element_count"] == 36
    assert bts["beam_energy_GeV"] == 4.0
    assert "sept_in" in bts["unique_families"]
    assert "sept_ex" in bts["unique_families"]


def test_baseline_optics_parameters(baseline_metrics):
    """Verify linear optics and maximum beta values."""
    optics = baseline_metrics["optics"]
    initial = optics["initial_twiss"]
    final = optics["final_twiss"]
    maxima = optics["maximums"]

    # Initial Twiss
    assert pytest.approx(initial["beta_x_m"], abs=1e-4) == 7.560
    assert pytest.approx(initial["beta_y_m"], abs=1e-4) == 12.269
    assert pytest.approx(initial["alpha_x"], abs=1e-4) == 1.5231
    assert pytest.approx(initial["alpha_y"], abs=1e-4) == -1.6547

    # Final optics
    assert pytest.approx(final["beta_x_m"], abs=1e-2) == 44.98
    assert pytest.approx(final["beta_y_m"], abs=1e-1) == 242.61

    # Maximums
    assert maxima["beta_x_max_m"] <= 60.0
    assert maxima["beta_y_max_m"] > 200.0


def test_baseline_tracking_survival(baseline_metrics):
    """Verify baseline beam tracking survival."""
    tracking = baseline_metrics["tracking"]
    assert tracking["initial_particle_count"] == 1000
    assert tracking["survived_particle_count"] == 1000
    assert pytest.approx(tracking["survival_fraction"]) == 1.0


def test_nkm_field_and_kick(baseline_metrics):
    """Verify NKM integrated field and nominal kick angle."""
    nkm = baseline_metrics["nkm"]
    assert nkm["length_m"] == 0.525
    assert pytest.approx(nkm["peak_field_T"], abs=1e-3) == 0.146
    assert pytest.approx(nkm["nominal_kick_mrad"], abs=1e-2) == 5.75
