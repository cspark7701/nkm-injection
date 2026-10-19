#!/usr/bin/env python3
"""F5 — where the beam is lost: zero-capture realizations and corrected ring 5501 (round 4).

Reruns selected cases with the unchanged physics and records, per lost particle, the loss category, ring element,
s position, plane and turn (``track_injection``'s loss records), and classifies losses inside the 3-D NKM by the
condition that removed them:
  chamber    the flat in-magnet vacuum chamber (16 x 3.8 mm half-apertures), a physical boundary;
  conductor  within 1 mm of a wire (numerical guard of the filament model);
  domain     outside |x|, |y| <= 50 mm (numerical domain of the field model).
Each rerun must reproduce the stored E7 capture and loss-category counts exactly.

Cases: up to ``--max-cases`` NKM zero-capture realizations of the full-budget seed-42 ensemble (first per ring),
and the selected point on corrected ring 5501 without injection errors (bunch seed 1001, 500 particles).
Units: m, rad; counts.
"""
import argparse
from collections import Counter
import copy
from dataclasses import replace
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_capture_robustness as rc  # noqa: E402
from nkm_injection import injection_study as inj  # noqa: E402
from nkm_injection import wire_field  # noqa: E402

E7 = ROOT / 'results/journal_campaign_04'
RECORDS = []


class ClassifyingKicker(wire_field.FilamentNKMKicker):
    """FilamentNKMKicker with an identical kick and loss rule that also records the removing condition."""

    def apply(self, beam, closed_orbit_x):
        live = np.flatnonzero(np.isfinite(beam[0]))
        b = beam[:, live].copy()
        dx = self.config.nkm_dx_m - closed_orbit_x
        gain = self.config.kicker_polarity * self.config.field_scale / self.brho
        lost = np.zeros(b.shape[1], bool)
        reason = np.array([''] * b.shape[1], dtype=object)
        self._drift(b, -self.s_span_m)
        ds = 2 * self.s_span_m / self.n_slices
        for i in range(self.n_slices):
            s = -self.s_span_m + (i + 0.5) * ds
            self._drift(b, 0.5 * ds)
            xm, ym = b[0] - dx, b[2]
            rmin = np.min(np.hypot(xm[:, None] - self.wires[None, :, 0], ym[:, None] - self.wires[None, :, 1]), axis=1)
            checks = [('conductor', rmin < self.conductor_radius_m),
                      ('domain', (np.abs(xm) > self.domain_half_m) | (np.abs(ym) > self.domain_half_m))]
            if self.chamber_half_y_m is not None and abs(s) <= self.chamber_half_length_m:
                checks.insert(0, ('chamber', (np.abs(xm) > self.chamber_half_x_m) | (np.abs(ym) > self.chamber_half_y_m)))
            for name, mask in checks:
                new = mask & ~lost
                reason[new] = name
                lost |= mask
            if gain != 0.0:
                bx, by, bs = self.field(xm, ym, s)
                pn = 1.0 / (1.0 + b[4])
                b[1] += ds * gain * (by - b[3] * pn * bs)
                if self.vertical_kick:
                    b[3] += ds * gain * (-bx + b[1] * pn * bs)
            self._drift(b, 0.5 * ds)
        self._drift(b, -self.s_span_m)
        b[1] += self.config.kick_offset_rad
        beam[:, live] = b
        out = np.zeros(beam.shape[1], bool)
        out[live[lost]] = True
        beam[:, out] = np.nan
        RECORDS.append({'magnet_reasons': dict(Counter(reason[lost]))})
        return out


_track = inj.track_injection


def recording_track(config, ring, kicker, beam, backend='element', n_turns=None):
    res = _track(config, ring, kicker, beam, backend, n_turns)
    recs = res['ring_loss_records']
    RECORDS.append({'model': kicker.model, 'loss_causes': res['loss_causes'], 'captured': res['captured'],
                    'planes': dict(Counter(r['plane'] for r in recs)),
                    'families': dict(Counter(r['family'] for r in recs).most_common(8)),
                    'turns': {'turn_0': sum(r['turn'] == 0 for r in recs), 'turns_1_9': sum(1 <= r['turn'] < 10 for r in recs),
                              'turns_10_99': sum(10 <= r['turn'] < 100 for r in recs), 'turns_100_plus': sum(r['turn'] >= 100 for r in recs)},
                    'n_records': len(recs)})
    return res


def run_case(job):
    RECORDS.clear()
    rc.track_injection = recording_track
    rc.FilamentNKMKicker = ClassifyingKicker
    job = dict(job, checkpoint=None)
    out = rc.run_realization(job)
    magnet = [r for r in RECORDS if 'magnet_reasons' in r]
    tracks = [r for r in RECORDS if 'model' in r]
    return {'sample_id': job['sample']['sample_id'], 'ring': job.get('ring_error_seed'), 'result': out,
            'magnet_reasons': magnet[0]['magnet_reasons'] if magnet else {}, 'tracks': tracks}


def ring5501_case():
    """Selected point, corrected ring 5501, no injection errors: E6-style nominal bunch."""
    spec = json.loads((E7 / 'e7_jitter_0/checkpoint_inputs.json').read_text())
    job = copy.deepcopy(spec['jobs'][0])
    job['sample'] = {k: ([0.0] * len(v) if isinstance(v, list) else 0.0) for k, v in job['sample'].items()}
    job['sample']['sample_id'] = -5501
    job['extra'] = {'emit_rel': 0.0, 'espread_abs': 0.0}
    job['ring_error_seed'] = 5501
    job['corrected_ring_path'] = str(E7 / 'e5_corrected_ring/seed5501.mat')
    job['particles'] = 500
    job['beam_seed'] = 1001
    return job


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--max-cases', type=int, default=8)
    p.add_argument('--workers', type=int, default=2)
    a = p.parse_args()
    if a.output.exists():
        raise SystemExit('output exists')
    folder = E7 / 'e7_seed42'
    raw = {r['sample_id']: r for r in json.loads((folder / 'capture_robustness_raw.json').read_text())['realizations']}
    jobs = json.loads((folder / 'checkpoint_inputs.json').read_text())['jobs']
    chosen, rings = [], set()
    for job in jobs:
        r = raw[job['sample']['sample_id']]
        if r['models']['fieldmap_3d']['capture_fraction'] == 0 and r['ring_error_seed'] not in rings:
            chosen.append(job)
            rings.add(r['ring_error_seed'])
        if len(chosen) == a.max_cases:
            break
    from nkm_injection.concurrency import parallel_map
    cases = parallel_map(run_case, chosen + [ring5501_case()], n_workers=a.workers, desc='F5 loss locations')
    summary = []
    for case in cases:
        sid = case['sample_id']
        stored = raw.get(sid)
        reproduced = None
        if stored is not None:
            reproduced = all(case['result']['models'][m]['loss_causes'] == stored['models'][m]['loss_causes']
                             and case['result']['models'][m]['captured'] == stored['models'][m]['captured'] for m in stored['models'])
        summary.append({'sample_id': sid, 'ring': case['ring'], 'reproduces_e7': reproduced,
                        'capture': {m: case['result']['models'][m]['capture_fraction'] for m in case['result']['models']},
                        'loss_causes': {m: case['result']['models'][m]['loss_causes'] for m in case['result']['models']},
                        'magnet_reasons_nkm': case['magnet_reasons'], 'ring_losses': case['tracks']})
    totals = Counter()
    for c in summary:
        if c['sample_id'] >= 0:
            for t in c['ring_losses']:
                if t['model'] == 'fieldmap_3d':
                    totals.update({f"plane_{k}": v for k, v in t['planes'].items()})
                    totals.update({f"turns_{k}": v for k, v in t['turns'].items()})
    result = {'scope': 'Selected NKM zero-capture realizations (full budget, seed 42, first per ring) and ring 5501 at the selected '
                       'point without injection errors; unchanged physics with loss classification.',
              'cases': summary, 'zero_capture_nkm_totals': dict(totals),
              'definitions': {'chamber': 'flat in-magnet chamber 16 x 3.8 mm half-apertures over the magnet length (physical)',
                              'conductor': 'within 1 mm of a wire, anywhere in the +/-0.45 m integration span (numerical guard)',
                              'domain': 'outside |x|,|y| <= 50 mm (numerical field-model domain)',
                              'ring planes': 'x/y when outside the element aperture in that plane; dynamical otherwise'}}
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    for c in summary:
        print(c['sample_id'], c['ring'], c['reproduces_e7'], c['capture'], c['magnet_reasons_nkm'],
              [(t['model'], t['planes'], t['turns']) for t in c['ring_losses']])
    print(dict(totals))


if __name__ == '__main__':
    main()
