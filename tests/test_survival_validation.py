"""C4 helpers: seeded ring errors and loss-category reconciliation (no long tracking)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sv", ROOT / "scripts" / "run_survival_validation.py")
SV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SV)


def test_summary_reconciles_loss_categories():
    rows = [{"label": "a", "n": 100, "captured": 90, "loss_causes": {"septum_creation": 2, "outside_field_map": 1, "ring": 7,
                                                                      "ring_septum_return": 3, "ring_elsewhere": 4}},
            {"label": "a", "n": 50, "captured": 50, "loss_causes": {"septum_creation": 0, "outside_field_map": 0, "ring": 0}}]
    s = SV.summarise(rows, "label")["a"]
    assert s["n"] == 150 and s["captured"] == 140 and s["reconciles"] and s["loss_causes"]["ring"] == 7
