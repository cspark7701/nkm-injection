"""Exact 3-D field of the four-loop filament NKM and a sliced tracker in AT canonical coordinates.

Geometry (from the RADIA model in ``NKM_radia.ipynb``, read only): four closed rectangular filament loops, one per
quadrant. Each loop has an inner wire at (±x1, ±y1) and an outer wire at (±x2, ±y2) running along s from −Lh to +Lh,
joined by straight end connectors at s = ±Lh; every loop carries the same current I in the RADIA point order
(x1,+Lh)→(x2,+Lh)→(x2,−Lh)→(x1,−Lh)→(x1,+Lh). Default values: x1 = y1 = 5.3 mm, x2 = y2 = 10.25 mm,
Lh = 262.5 mm. RADIA uses the axis order (x, s, y), which is left-handed relative to the beam frame (x, y, s) used
here, so the RADIA current of −3000 A corresponds to I = +3000 A in this frame; with that value the line integrals
reproduce both components of ``kickmap_file.txt`` to ~1e-10 relative (tests/test_wire_field.py). The field of straight filaments in vacuum is evaluated in closed form (Biot–Savart),
including fringe and end-connector fields; there is no iron, no chamber and no time dependence.

Units: positions m, field T, current A, rigidity T m, kicks rad (AT canonical p_x/p0, p_y/p0).

Kick convention: with polarity P the horizontal electron kick on a straight line equals P ∫B_y ds / (Bρ), which
reproduces the stored kick-map value for P = +1 (the map stores ∫B_y ds/Bρ). The vertical kick is the curl-free
partner −P ∫B_x ds / (Bρ). Inside the field the canonical equations are
    dp_x/ds = P S (B_y − y' B_s)/Bρ,   dp_y/ds = P S (−B_x + x' B_s)/Bρ,   x' = p_x/(1+δ), y' = p_y/(1+δ),
with S the field scale. The kick is applied to canonical momentum and carries no 1/(1+δ) factor; the drift uses
the slope p/(1+δ).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

MU0_OVER_4PI = 1e-7  # T m / A


@dataclass(frozen=True)
class FilamentGeometry:
    x1_m: float = 5.3e-3
    y1_m: float = 5.3e-3
    x2_m: float = 10.25e-3
    y2_m: float = 10.25e-3
    half_length_m: float = 0.2625
    current_A: float = 3000.0

    def segments(self) -> np.ndarray:
        """(16, 2, 3) array of segment end points (x, y, s) in m, in RADIA loop order (current flows A→B)."""
        segs = []
        lh = self.half_length_m
        for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            p1 = (sx * self.x1_m, sy * self.y1_m, lh)
            p2 = (sx * self.x2_m, sy * self.y2_m, lh)
            p3 = (sx * self.x2_m, sy * self.y2_m, -lh)
            p4 = (sx * self.x1_m, sy * self.y1_m, -lh)
            for a, b in ((p1, p2), (p2, p3), (p3, p4), (p4, p1)):
                segs.append((a, b))
        return np.asarray(segs, dtype=float)

    def wire_positions(self) -> np.ndarray:
        """(8, 2) transverse positions of the longitudinal wires (m)."""
        pts = []
        for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            pts += [(sx * self.x1_m, sy * self.y1_m), (sx * self.x2_m, sy * self.y2_m)]
        return np.asarray(pts)


def segment_field(points: np.ndarray, seg_a: np.ndarray, seg_b: np.ndarray, current_A: float) -> np.ndarray:
    """Biot–Savart field (T) at points (N, 3) of straight segments A→B (M, 3) with common current; returns (N, 3).

    B = μ0 I/(4π) (|a|+|b|) (a × b) / (|a||b| (|a||b| + a·b)), a = A − P, b = B − P; points on a segment's line give 0.
    """
    p = np.asarray(points, float)[:, None, :]
    a = seg_a[None, :, :] - p
    b = seg_b[None, :, :] - p
    na = np.linalg.norm(a, axis=-1)
    nb = np.linalg.norm(b, axis=-1)
    cross = np.cross(a, b)
    ab = np.einsum("nmk,nmk->nm", a, b)
    c2 = np.einsum("nmk,nmk->nm", cross, cross)
    # |a||b| + a·b = |a×b|² / (|a||b| − a·b): use the cancellation-free form when the point lies between the ends
    with np.errstate(divide="ignore", invalid="ignore"):
        f_out = (na + nb) / (na * nb * (na * nb + ab))
        f_in = (na + nb) * (na * nb - ab) / (na * nb * c2)
        f = np.where(ab < 0, f_in, f_out)
        f = np.where(np.isfinite(f) & (c2 > 0), f, 0.0)
    return MU0_OVER_4PI * current_A * np.einsum("nm,nmk->nk", f, cross)


class FilamentNKMField:
    """Callable 3-D field B(x, y, s) of the filament NKM (centred at s = 0)."""

    def __init__(self, geometry: FilamentGeometry = FilamentGeometry()):
        self.geometry = geometry
        segs = geometry.segments()
        self._a, self._b = segs[:, 0, :], segs[:, 1, :]

    def __call__(self, x, y, s) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        x = np.atleast_1d(np.asarray(x, float))
        y = np.broadcast_to(np.asarray(y, float), x.shape)
        s = np.broadcast_to(np.asarray(s, float), x.shape)
        b = segment_field(np.stack([x, y, s], axis=-1).reshape(-1, 3), self._a, self._b, self.geometry.current_A)
        b = b.reshape(x.shape + (3,))
        return b[..., 0], b[..., 1], b[..., 2]

    def line_integrals(self, x, y, s_max_m: float = 2.0, n_nodes: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        """∫B_x ds and ∫B_y ds (T m) along straight lines parallel to s over [−s_max, s_max] (Gauss–Legendre,
        nodes clustered at the magnet ends). The neglected tail beyond s_max falls off as r²/s² of the end field."""
        x = np.atleast_1d(np.asarray(x, float)); y = np.broadcast_to(np.asarray(y, float), x.shape)
        lh = self.geometry.half_length_m
        edges = np.unique(np.concatenate([np.linspace(-s_max_m, -lh - 0.05, 3), np.linspace(-lh - 0.05, -lh + 0.05, 9),
                                          np.linspace(-lh + 0.05, lh - 0.05, 5), np.linspace(lh - 0.05, lh + 0.05, 9),
                                          np.linspace(lh + 0.05, s_max_m, 3)]))
        g, w = np.polynomial.legendre.leggauss(max(4, n_nodes // (len(edges) - 1)))
        ibx = np.zeros(x.shape); iby = np.zeros(x.shape)
        for lo, hi in zip(edges[:-1], edges[1:]):
            s = 0.5 * (hi - lo) * g + 0.5 * (hi + lo)
            ww = 0.5 * (hi - lo) * w
            for si, wi in zip(s, ww):
                bx, by, _ = self(x, y, si)
                ibx += wi * bx; iby += wi * by
        return ibx, iby


def brho_T_m(energy_eV: float) -> float:
    """Magnetic rigidity (T m) of an ultra-relativistic electron, Bρ = E/(c e) for E in eV (β ≈ 1)."""
    return energy_eV / 299792458.0


class FilamentNKMKicker:
    """Sliced finite-length NKM through the exact 3-D filament field (``_apply_kick`` compatible).

    The beam is given at the NKM centre in AT coordinates. It is drifted back to s = −s_span (exact drift in
    canonical coordinates), integrated to +s_span with n_slices drift–kick–drift steps, and drifted back to the
    centre. Field scale S = config.field_scale, polarity P = config.kicker_polarity, magnet-frame offset
    config.nkm_dx_m − closed_orbit_x; an additive config.kick_offset_rad is added to p_x (kept for backward
    compatibility with the error model). Particles closer than ``conductor_radius_m`` to a wire, or outside
    |x|, |y| ≤ ``domain_half_m`` at any slice, are lost (no extrapolation beyond the physical model).
    """
    model = "fieldmap_3d"
    interpolation = "exact"

    def __init__(self, config, n_slices: int = 320, s_span_m: float = 0.45, conductor_radius_m: float = 1.0e-3,
                 domain_half_m: float = 0.05, geometry: FilamentGeometry = FilamentGeometry(),
                 vertical_kick: bool = True):
        self.config = config
        self.vertical_kick = bool(vertical_kick)  # False: diagnostic only (suppresses dp_y inside the magnet)
        self.field = FilamentNKMField(geometry)
        self.n_slices = int(n_slices)
        self.s_span_m = float(s_span_m)
        self.conductor_radius_m = float(conductor_radius_m)
        self.domain_half_m = float(domain_half_m)
        self.wires = geometry.wire_positions()
        self.brho = brho_T_m(config.energy_eV)

    @staticmethod
    def _drift(b, length):
        pn = 1.0 / (1.0 + b[4])
        xp, yp = b[1] * pn, b[3] * pn
        b[0] += length * xp
        b[2] += length * yp
        b[5] += length * 0.5 * (xp ** 2 + yp ** 2)

    def apply(self, beam: np.ndarray, closed_orbit_x: float) -> np.ndarray:
        """Kick live particles in place; return the mask of particles lost inside the magnet."""
        live = np.flatnonzero(np.isfinite(beam[0]))
        b = beam[:, live].copy()
        dx = self.config.nkm_dx_m - closed_orbit_x
        gain = self.config.kicker_polarity * self.config.field_scale / self.brho
        lost = np.zeros(b.shape[1], bool)
        self._drift(b, -self.s_span_m)
        ds = 2 * self.s_span_m / self.n_slices
        for i in range(self.n_slices):
            s = -self.s_span_m + (i + 0.5) * ds
            self._drift(b, 0.5 * ds)
            xm, ym = b[0] - dx, b[2]
            rmin = np.min(np.hypot(xm[:, None] - self.wires[None, :, 0], ym[:, None] - self.wires[None, :, 1]), axis=1)
            lost |= (rmin < self.conductor_radius_m) | (np.abs(xm) > self.domain_half_m) | (np.abs(ym) > self.domain_half_m)
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
        return out

    def kicks(self, x, y):
        """Straight-line integrated kicks (rad) at magnet-frame-free positions x, y (for stored-beam estimates)."""
        ibx, iby = self.field.line_integrals(np.asarray(x, float) - self.config.nkm_dx_m, y)
        g = self.config.kicker_polarity * self.config.field_scale / self.brho
        return g * iby + self.config.kick_offset_rad, -g * ibx
