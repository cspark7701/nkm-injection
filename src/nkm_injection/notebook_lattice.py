"""Configured reconstruction of notebook 01's original BTS geometry (SI units)."""
from dataclasses import dataclass, field
from typing import Dict, Tuple
import numpy as np
import at

from .configuration import SerializableConfigMixin
from .tracking_contracts import finite_scalar

QUAD_NAMES = ('q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33')


def _dipoles():
    degree = np.pi / 180
    # length [m], bend [rad], gradient [m^-2], entrance/exit edges [rad]
    return {'kext': (0.31, -0.002, 0., -0.001, -0.001),
            'bm1': (1.42155, 6.07*degree, -0.149, 3.035*degree, 3.035*degree),
            'btsbm': (1.411, 7.8863*degree, 0., 3.94315*degree, 3.94315*degree),
            'sepext': (2.25, -5*degree, 0., -2.5*degree, -2.5*degree),
            'sepsr': (2.25, 5*degree, 0., 2.5*degree, 2.5*degree),
            'sepsr2': (0.9, 0.573*degree, 0., 0.005, 0.005)}


@dataclass
class NotebookBTSConfig(SerializableConfigMixin):
    """Notebook 01 geometry, distinct from the canonical production BTSConfig.

    Lengths/apertures use m, bend/edge angles rad, energy eV, strengths m^-2.
    q34 remains fixed; the nine named matching quadrupoles are decision variables.
    """
    energy_eV: float = 4e9
    quad_length_m: float = 0.2
    strengths_m_minus2: Tuple[float, ...] = (0.738, 0.415, 0.415, -0.9902, 1.288,
                                          1.288, -2.08, 4.13, -2.24)
    q34_strength_m_minus2: float = 2.448
    drifts_m: Dict[str, float] = field(default_factory=lambda: dict(zip(
        ('dr1', 'dr2', 'dr3', 'dr4', 'dr4_1', 'dr4_2', 'dr4_3', 'dr5',
         'dr5_2', 'dr5_3', 'dr5_4', 'dr6', 'dr6_1', 'dr6_2', 'dr6_3',
         'dr6_4', 'dr7', 'dr_nkm_up_bts'),
        (1.845, .875, .3, .485, .8, 5.3, .497, .61224, 4.8, 1.2,
         .6, .6, 1.5, 2.65, 1.25, .2, .15, .25))))
    dipoles: Dict[str, Tuple[float, float, float, float, float]] = field(default_factory=_dipoles)
    element_order: Tuple[str, ...] = (
        'kext', 'dr1', 'bm1', 'dr2', 'sepext', 'dr3', 'sepext', 'dr4',
        'q11', 'dr4_1', 'q12', 'dr4_2', 'q13', 'dr4_3', 'btsbm', 'dr5',
        'q21', 'dr5_2', 'q22', 'dr5_3', 'q23', 'dr5_4', 'btsbm', 'dr6',
        'q31', 'dr6_1', 'q32', 'dr6_2', 'q33', 'dr6_3', 'q34', 'dr6_4',
        'sepsr', 'dr7', 'sepsr2', 'dr_nkm_up_bts')
    with_apertures: bool = True
    drift_aperture_m: float = 0.01935
    quad_aperture_m: float = 0.016
    bend_aperture_m: float = 0.012

    def validate(self):
        for name in ('energy_eV', 'quad_length_m', 'drift_aperture_m',
                     'quad_aperture_m', 'bend_aperture_m'):
            finite_scalar(getattr(self, name), name, minimum=0, nonzero=True)
        if not isinstance(self.with_apertures, bool):
            raise ValueError('with_apertures must be boolean')
        if len(self.strengths_m_minus2) != 9 or not np.isfinite(self.strengths_m_minus2).all():
            raise ValueError('Nine finite matching strengths (m^-2) required')
        finite_scalar(self.q34_strength_m_minus2, 'q34 strength')
        for name, value in self.drifts_m.items():
            finite_scalar(value, name, minimum=0)
        for name, values in self.dipoles.items():
            if len(values) != 5 or not np.isfinite(values).all() or values[0] <= 0:
                raise ValueError(f'Invalid dipole parameters: {name}')
        names = set(self.drifts_m) | set(self.dipoles) | set(QUAD_NAMES) | {'q34'}
        if (set(self.drifts_m) & set(self.dipoles) or
                (set(self.drifts_m) | set(self.dipoles)) & (set(QUAD_NAMES) | {'q34'})):
            raise ValueError('Element family definitions must not overlap')
        if not self.element_order or any(name not in names for name in self.element_order):
            raise ValueError('Unknown or empty element order')
        if any(self.element_order.count(name) != 1 for name in (*QUAD_NAMES, 'q34')):
            raise ValueError('Each matching quadrupole and q34 must appear once')


def create_notebook_bts_lattice(config: NotebookBTSConfig):
    """Build an independent lattice preserving original notebook order/apertures."""
    config.validate()
    elements = {name: at.Drift(name, length) for name, length in config.drifts_m.items()}
    for name, (length, angle, gradient, entrance, exit_) in config.dipoles.items():
        elements[name] = at.Dipole(name, length=length, bending_angle=angle,
                                  PolynomB=[0, gradient], EntranceAngle=entrance, ExitAngle=exit_)
    for name, strength in zip((*QUAD_NAMES, 'q34'),
                              (*config.strengths_m_minus2, config.q34_strength_m_minus2)):
        elements[name] = at.Quadrupole(name, config.quad_length_m, k=strength)
    sequence = []
    for name in config.element_order:
        element = elements[name].deepcopy()
        if config.with_apertures:
            family, radius = ('drift', config.drift_aperture_m) if name in config.drifts_m else (
                ('bend', config.bend_aperture_m) if name in config.dipoles else ('quad', config.quad_aperture_m))
            sequence.extend([at.Aperture('ap_'+family, [-radius, radius, -radius, radius]),
                             element, at.Aperture('ap_'+family, [-radius, radius, -radius, radius])])
        else:
            sequence.append(element)
    return at.Lattice(sequence, name='BTS Lattice', particle='relativistic', energy=config.energy_eV)
