"""Round-three BTS physics tests (Reviewer 2 tasks R2B-01 to R2B-06). SI units."""
import json
from pathlib import Path

import numpy as np
import pytest

from nkm_injection.bts_journal import lattice_for
from nkm_injection.bts_round2 import station_record
from nkm_injection.bts_round3 import boundary_clearances

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = json.loads((ROOT / 'docs/paper_bts/generated/round2_designs.json').read_text())['designs']


@pytest.mark.parametrize('name', ['reference', 'low_beta'])
def test_end_station_clearances_are_fixed_by_boundary_optics(name):
    """Every matched setting has the analytic entrance and exit clearances (R2B-02)."""
    k = np.array(DESIGNS['baseline']['nominal'][name]['strengths_m_minus2'])
    record = station_record(lattice_for(k))
    analytic = boundary_clearances()
    by_station = {(r['s_m'] > 1.0, r['axis']): r['clearance_m'] for r in record['stations']
                  if r['s_m'] in (0.0,) or abs(r['s_m'] - 21.789) < 1e-3}
    for axis in (0, 1):
        assert by_station[(False, axis)] == pytest.approx(analytic['entrance'][axis], abs=1e-9)
        assert by_station[(True, axis)] == pytest.approx(analytic['exit'][axis], abs=2e-7)
    assert record['minimum_m'] == pytest.approx(analytic['entrance'][0], abs=1e-9)


def test_boundary_clearance_values_match_table_2():
    analytic = boundary_clearances()
    assert np.round(np.array(analytic['entrance']) * 1e3, 3).tolist() == [17.455, 18.865]
    assert np.round(np.array(analytic['exit']) * 1e3, 3).tolist() == [18.555, 19.064]
