"""Coupled NKM injection study: geometry, kick models, beams and ring tracking backends.

This module defines the frozen journal-campaign injection model (``InjectionStudyConfig``,
schema version 1) documented in ``docs/jinst-paper/physics_model.md``.

Units at every public interface: positions m, angles / canonical momenta rad, energy eV,
relative momentum deviation dimensionless, ct in m, geometric emittance m rad. Kick-map
values are read in mrad (as written by ``NKM_radia.ipynb``) and converted to rad here.

Geometry (AT ring coordinates, observation and kick at the NKM centre):

* The injected beam is created at the septum exit, i.e. the entrance of the ring drift
  ``NKMUPRING`` (length ``septum_to_nkm_drift_m`` = 2.0 m), with centroid
  ``(injection_x_m, injection_xp_rad)`` added to the BTS exit distribution.
* It drifts to the NKM centre (``SectionEnd``, ``SectionStart``, first half of ``NKM``),
  receives one thin kick (single-turn pulse) and is then tracked through the ring,
  which is re-ordered to start and end at the NKM centre.
* The septum blade is a horizontal aperture at the ``NKMUPRING`` entrance:
  circulating particles with ``x < septum_edge_x_m`` are lost there.
* Injected particles are lost at creation if they lie on the stored side of the blade
  outer face (``x >= septum_edge_x_m - septum_thickness_m``).

Kick polarity: the kick-map file stores ``+int(B) dl / (B rho)`` without charge sign.
``kicker_polarity = +1`` means the electron kick equals the stored value; this corresponds
to the coil current opposite to the RADIA notebook sign. The required polarity follows
from the injection geometry (the kick must cancel the incoming positive angle at x < 0).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import numpy as np
import at

from .configuration import SerializableConfigMixin
from .kickmap import NKMKickMap2D
from .storage_ring_injection import StorageRingInjectionConfig, load_storage_ring_injection_lattice

KickModel = Literal["off", "fieldmap", "dipole", "linear"]
Backend = Literal["element", "map"]
KICK_MODELS: Tuple[str, ...] = ("off", "fieldmap", "dipole", "linear")
STUDY_SCHEMA_VERSION = 1


@dataclass
class InjectedBeamConfig(SerializableConfigMixin):
    """Injected bunch at the septum exit (BTS exit), Twiss in m and dimensionless."""
    beta_x_m: float = 2.336495
    alpha_x: float = -0.016335
    beta_y_m: float = 4.256241
    alpha_y: float = 0.017772
    disp_x_m: float = 0.080868
    disp_px: float = 0.047472
    emit_x_m_rad: float = 1.0e-7
    emit_y_m_rad: float = 1.0e-8
    energy_spread: float = 1.1e-3
    bunch_length_m: float = 13.4e-3

    def validate(self) -> None:
        for name in ("beta_x_m", "beta_y_m", "emit_x_m_rad", "emit_y_m_rad", "energy_spread", "bunch_length_m"):
            if not np.isfinite(getattr(self, name)) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be finite and positive")


@dataclass
class InjectionStudyConfig(SerializableConfigMixin):
    """Complete injection-study configuration (schema version 1). See module docstring."""
    schema_version: int = STUDY_SCHEMA_VERSION
    energy_eV: float = 4.0e9
    ring_source: str = "K4GSR_HBIv4-1.mat"
    kickmap_path: str = "kickmap_file.txt"
    kicker_polarity: int = 1
    field_scale: float = 1.0
    nkm_dx_m: float = 0.0
    kick_offset_rad: float = 0.0
    septum_to_nkm_drift_m: float = 2.0
    septum_edge_x_m: float = -0.016
    septum_thickness_m: float = 0.002
    injection_x_m: float = -0.020
    injection_xp_rad: float = 0.00575
    injection_delta: float = 0.0
    closed_orbit_x_m: float = 0.0
    chamber_half_x_m: Optional[float] = None
    chamber_half_y_m: Optional[float] = None
    injected_beam: InjectedBeamConfig = field(default_factory=InjectedBeamConfig)
    stored_vertical_emittance_ratio: float = 0.1
    n_particles: int = 200
    n_turns: int = 500
    seed: int = 42

    def validate(self) -> None:
        if self.schema_version != STUDY_SCHEMA_VERSION:
            raise ValueError(f"Unsupported study schema version {self.schema_version}")
        if self.kicker_polarity not in (-1, 1):
            raise ValueError("kicker_polarity must be +1 or -1")
        if self.energy_eV <= 0 or self.septum_to_nkm_drift_m <= 0 or self.septum_thickness_m <= 0:
            raise ValueError("energy, drift length and septum thickness must be positive")
        if self.n_particles <= 0 or self.n_turns <= 0 or self.seed < 0:
            raise ValueError("particle/turn counts must be positive and seed non-negative")
        if not self.septum_edge_x_m < 0:
            raise ValueError("septum edge must be on the negative-x side")
        for name in ("chamber_half_x_m", "chamber_half_y_m"):
            value = getattr(self, name)
            if value is not None and not value > 0:
                raise ValueError(f"{name} must be positive or None")
        if not 0 < self.stored_vertical_emittance_ratio <= 1:
            raise ValueError("stored_vertical_emittance_ratio must lie in (0, 1]")
        self.injected_beam.validate()

    @property
    def nkm_entry_x_m(self) -> float:
        """Nominal injected centroid at the NKM centre for zero delta (drift + half NKM)."""
        return self.injection_x_m + self.injection_xp_rad * (self.septum_to_nkm_drift_m + 0.5 * 0.525)


# ---------------------------------------------------------------------------
# Kick models
# ---------------------------------------------------------------------------

class KickModelEvaluator:
    """Thin horizontal/vertical kick in rad (canonical momenta) at the NKM centre.

    ``fieldmap``: polarity * scale * map(x - nkm_dx, y) + kick_offset.
    ``dipole``: uniform kick equal to the field-map kick at the reference point x_ref (calibrated control).
    ``linear``: first-order Taylor expansion of the field map about x_ref (calibrated control).
    ``off``: no kick. Coordinates outside the map domain are flagged, never extrapolated.
    """

    def __init__(self, model: str, config: InjectionStudyConfig, kickmap: Optional[NKMKickMap2D], x_ref_m: float):
        if model not in KICK_MODELS:
            raise ValueError(f"Unknown kick model {model!r}; expected one of {KICK_MODELS}")
        if model != "off" and kickmap is None:
            raise ValueError("A kick map is required for fieldmap/dipole/linear models")
        self.model, self.config, self.kickmap, self.x_ref_m = model, config, kickmap, float(x_ref_m)
        self.gain = config.kicker_polarity * config.field_scale
        if model in ("dipole", "linear"):
            k0 = self._map_kx(np.array([x_ref_m]), np.array([0.0]))[0]
            h = 1.0e-4
            kp = self._map_kx(np.array([x_ref_m + h]), np.array([0.0]))[0]
            km = self._map_kx(np.array([x_ref_m - h]), np.array([0.0]))[0]
            self.k0_rad, self.k1_rad_per_m = float(k0), float((kp - km) / (2 * h))
        else:
            self.k0_rad, self.k1_rad_per_m = 0.0, 0.0

    def _map_kx(self, x, y):
        kx, _ = self.kickmap.evaluate_kicks(x - self.config.nkm_dx_m, y)
        return self.gain * np.asarray(kx, dtype=float)

    def in_domain(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        if self.kickmap is None or self.model in ("off", "dipole", "linear"):
            return np.ones_like(x, dtype=bool)
        xs = x - self.config.nkm_dx_m
        return ((xs >= self.kickmap.x_min) & (xs <= self.kickmap.x_max)
                & (y >= self.kickmap.y_min) & (y <= self.kickmap.y_max))

    def kicks(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
        if self.model == "off":
            return np.zeros_like(x), np.zeros_like(y)
        if self.model == "dipole":
            return np.full_like(x, self.k0_rad + self.config.kick_offset_rad), np.zeros_like(y)
        if self.model == "linear":
            return self.k0_rad + self.k1_rad_per_m * (x - self.x_ref_m) + self.config.kick_offset_rad, np.zeros_like(y)
        kx, ky = self.kickmap.evaluate_kicks(x - self.config.nkm_dx_m, y)
        return (self.gain * np.asarray(kx) + self.config.kick_offset_rad, self.gain * np.asarray(ky))


# ---------------------------------------------------------------------------
# Lattice preparation
# ---------------------------------------------------------------------------

@dataclass
class PreparedRing:
    """Ring re-ordered to start/end at the NKM centre, plus the septum->NKM injection segment."""
    ring_c: at.Lattice
    inj_segment: at.Lattice
    orbit6: np.ndarray
    m66: np.ndarray
    twiss_x: Tuple[float, float]
    twiss_y: Tuple[float, float]
    disp_x: Tuple[float, float]
    emit_x_m_rad: float
    energy_spread: float
    bunch_length_m: float
    circumference_m: float
    septum_index: int


def _half_drift(elem, name):
    half = elem.deepcopy()
    half.FamName, half.Length = name, elem.Length / 2.0
    return half


def prepare_ring(config: InjectionStudyConfig, repo_root: Path, work_dir: Path) -> PreparedRing:
    """Build the native ring around the NKM centre. Writes only the generated lattice in work_dir."""
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    rc = StorageRingInjectionConfig(energy_eV=config.energy_eV, mat_filename=str(work_dir / "storage_ring_lattice_nkm.mat"))
    ring, nkm_idx = load_storage_ring_injection_lattice(rc, source_mat_path=Path(repo_root) / config.ring_source)
    names = [e.FamName for e in ring]
    if names[nkm_idx] != "NKM" or names[-2] != "NKMUPRING":
        raise ValueError("Unexpected ring layout: expected NKM after SectionStart and NKMUPRING before SectionEnd")
    nkm = ring[nkm_idx]
    h1, h2 = _half_drift(nkm, "NKM_H1"), _half_drift(nkm, "NKM_H2")
    elems = [h2] + [e.deepcopy() for e in ring[nkm_idx + 1:]] + [e.deepcopy() for e in ring[:nkm_idx]] + [h1]
    sept_idx = 1 + (len(ring) - nkm_idx - 1) - 2  # position of NKMUPRING in the re-ordered list
    if elems[sept_idx].FamName != "NKMUPRING":
        raise ValueError("Septum element index mismatch")
    if config.chamber_half_x_m is not None:
        hy = config.chamber_half_y_m if config.chamber_half_y_m is not None else 1.0
        for e in elems:
            e.RApertures = np.array([-config.chamber_half_x_m, config.chamber_half_x_m, -hy, hy])
    sx_max = config.chamber_half_x_m or 1.0
    sy = config.chamber_half_y_m or 1.0
    elems[sept_idx].RApertures = np.array([config.septum_edge_x_m, sx_max, -sy, sy])
    ring_c = at.Lattice(elems, energy=ring.energy, periodicity=1, name="ring_from_nkm_centre")
    ring_c = ring_c.enable_6d(copy=True) if ring.is_6d else ring_c
    inj = [ring[-2].deepcopy(), ring[-1].deepcopy(), ring[0].deepcopy(), h1.deepcopy()]
    inj[0].Length = config.septum_to_nkm_drift_m
    for e in inj:
        if hasattr(e, "RApertures"):
            del e.RApertures
    inj_segment = at.Lattice(inj, energy=ring.energy, periodicity=1, name="septum_to_nkm_centre")
    orbit6, _ = ring_c.find_orbit6()
    m66, _ = ring_c.find_m66(orbit=orbit6)
    _, _, el = at.get_optics(ring_c, refpts=[0])
    params = ring_c.radiation_parameters()
    return PreparedRing(
        ring_c=ring_c, inj_segment=inj_segment, orbit6=np.asarray(orbit6, float), m66=np.asarray(m66, float),
        twiss_x=(float(el.beta[0, 0]), float(el.alpha[0, 0])), twiss_y=(float(el.beta[0, 1]), float(el.alpha[0, 1])),
        disp_x=(float(el.dispersion[0, 0]), float(el.dispersion[0, 1])),
        emit_x_m_rad=float(params.emittances[0]), energy_spread=float(params.sigma_e),
        bunch_length_m=float(params.sigma_l), circumference_m=float(ring_c.circumference), septum_index=sept_idx)


# ---------------------------------------------------------------------------
# Beams
# ---------------------------------------------------------------------------

def gaussian_beam(n: int, twx, twy, emit_x, emit_y, disp, espread, blength, rng) -> np.ndarray:
    """Uncorrelated-in-planes Gaussian beam (6, n) in AT order; dispersion couples x to delta."""
    def plane(beta, alpha, emit):
        u, v = rng.standard_normal(n), rng.standard_normal(n)
        x = np.sqrt(emit * beta) * u
        xp = np.sqrt(emit / beta) * (v - alpha * u)
        return x, xp
    x, xp = plane(twx[0], twx[1], emit_x)
    y, yp = plane(twy[0], twy[1], emit_y)
    delta = espread * rng.standard_normal(n)
    ct = blength * rng.standard_normal(n)
    return np.vstack([x + disp[0] * delta, xp + disp[1] * delta, y, yp, delta, ct])


def injected_beam_at_septum(config: InjectionStudyConfig, ring: PreparedRing, seed: int,
                            n: Optional[int] = None, bts_exit_beam: Optional[np.ndarray] = None) -> np.ndarray:
    """Injected distribution at the septum exit in ring coordinates.

    ``bts_exit_beam`` (6, N) from coupled BTS tracking is used when supplied; otherwise a Gaussian
    with the configured BTS-exit Twiss. Centroid offsets and the synchronous (delta, ct) are added.
    """
    rng = np.random.default_rng(seed)
    if bts_exit_beam is None:
        b = config.injected_beam
        beam = gaussian_beam(n or config.n_particles, (b.beta_x_m, b.alpha_x), (b.beta_y_m, b.alpha_y),
                             b.emit_x_m_rad, b.emit_y_m_rad, (b.disp_x_m, b.disp_px), b.energy_spread,
                             b.bunch_length_m, rng)
    else:
        beam = np.array(bts_exit_beam, dtype=float, copy=True)
    beam[0] += config.injection_x_m - config.closed_orbit_x_m
    beam[1] += config.injection_xp_rad
    beam[4] += config.injection_delta + ring.orbit6[4]
    beam[5] += ring.orbit6[5]
    return beam


def stored_beam_at_nkm(config: InjectionStudyConfig, ring: PreparedRing, n: int, seed: int) -> np.ndarray:
    """Equilibrium stored beam at the NKM centre around the 6D closed orbit."""
    rng = np.random.default_rng(seed)
    ex = ring.emit_x_m_rad
    beam = gaussian_beam(n, ring.twiss_x, ring.twiss_y, ex, ex * config.stored_vertical_emittance_ratio,
                         ring.disp_x, ring.energy_spread, ring.bunch_length_m, rng)
    return beam + ring.orbit6[:, None]


# ---------------------------------------------------------------------------
# Tracking
# ---------------------------------------------------------------------------

def _apply_kick(beam: np.ndarray, kicker: KickModelEvaluator, closed_orbit_x: float) -> Tuple[np.ndarray, np.ndarray]:
    """Apply the thin kick in place to live particles; return (live mask, outside-map mask)."""
    live = np.isfinite(beam[0])
    x_abs = beam[0, live] + closed_orbit_x  # magnet-frame position includes the closed-orbit offset
    y = beam[2, live]
    inside = kicker.in_domain(x_abs, y)
    kx, ky = np.zeros_like(x_abs), np.zeros_like(y)
    if np.any(inside):
        kx[inside], ky[inside] = kicker.kicks(x_abs[inside], y[inside])
    idx = np.flatnonzero(live)
    beam[1, idx] += kx
    beam[3, idx] += ky
    outside = np.zeros(beam.shape[1], dtype=bool)
    outside[idx[~inside]] = True
    beam[:, outside] = np.nan
    return live, outside


def track_injection(config: InjectionStudyConfig, ring: PreparedRing, kicker: KickModelEvaluator,
                    beam_at_septum: np.ndarray, backend: Backend = "element",
                    n_turns: Optional[int] = None) -> Dict[str, Any]:
    """Track an injected beam from the septum exit for n_turns; capture = alive after the last turn.

    Loss causes: ``septum_creation`` (on stored side of blade at creation), ``outside_field_map``
    (kick map domain), ``ring`` (native AT loss incl. septum aperture, chamber apertures and
    numerical divergence; or, for the map backend, septum/chamber checks at their locations
    evaluated with the linear segment maps).
    """
    n_turns = int(n_turns or config.n_turns)
    beam = np.array(beam_at_septum, dtype=float, copy=True)
    n0 = beam.shape[1]
    causes = {"septum_creation": 0, "outside_field_map": 0, "ring": 0}
    blade_outer = config.septum_edge_x_m - config.septum_thickness_m
    bad = np.isfinite(beam[0]) & (beam[0] >= blade_outer)
    beam[:, bad] = np.nan
    causes["septum_creation"] = int(bad.sum())
    if backend == "element":
        beam = ring.inj_segment.track(beam, nturns=1)[0][:, :, 0, 0]
    else:
        m_inj, _ = ring.inj_segment.find_m66(orbit=np.zeros(6))
        live = np.isfinite(beam[0])
        beam[:, live] = m_inj @ beam[:, live]
    _, outside = _apply_kick(beam, kicker, config.closed_orbit_x_m)
    causes["outside_field_map"] = int(outside.sum())
    first_loss_turn = np.full(n0, -1)
    if backend == "element":
        start_live = np.isfinite(beam[0])
        final = np.array(beam, copy=True)
        _, _, info = ring.ring_c.track(final, nturns=n_turns, refpts=None, losses=True, in_place=True)
        lost = np.asarray(info["loss_map"]["islost"], dtype=bool) & start_live
        first_loss_turn[lost] = np.asarray(info["loss_map"]["turn"])[lost]
        alive = start_live & ~lost & np.isfinite(final[0])
    else:
        alive, first_loss_turn = _track_map(config, ring, beam, n_turns, first_loss_turn)
        final = None
    causes["ring"] = int((np.isfinite(beam[0]) & ~np.asarray(alive)).sum())
    captured = int(alive.sum())
    return {"backend": backend, "kick_model": kicker.model, "n_particles": n0, "n_turns": n_turns,
            "captured": captured, "capture_fraction": captured / n0 if n0 else None,
            "loss_causes": causes, "first_loss_turn": first_loss_turn.tolist(),
            "alive_mask": alive.tolist(), "final_coordinates": None if final is None else np.asarray(final).tolist()}


def _track_map(config, ring, beam, n_turns, first_loss_turn):
    """Linear one-turn-map backend around the 6D closed orbit, with septum/chamber checks."""
    co = ring.orbit6[:, None]
    m_to_sept, _ = at.Lattice(ring.ring_c[:ring.septum_index], energy=ring.ring_c.energy).find_m66(orbit=ring.orbit6)
    m_from_sept, _ = at.Lattice(ring.ring_c[ring.septum_index:], energy=ring.ring_c.energy).find_m66(orbit=ring.orbit6)
    dev = beam - co
    alive = np.isfinite(dev[0])
    hx = config.chamber_half_x_m
    for turn in range(n_turns):
        dev[:, alive] = m_to_sept @ dev[:, alive]
        x = dev[0] + co[0]
        lost = alive & ((x < config.septum_edge_x_m) | ((hx is not None) & (np.abs(x) > (hx or np.inf))))
        first_loss_turn[lost] = turn
        alive &= ~lost
        dev[:, alive] = m_from_sept @ dev[:, alive]
    return alive, first_loss_turn


def stored_beam_response(config: InjectionStudyConfig, ring: PreparedRing, kicker: KickModelEvaluator,
                         n: int = 100000, seed: int = 7) -> Dict[str, Any]:
    """Stored-beam disturbance from one NKM pass, evaluated at the NKM centre (linear optics).

    Returns the centroid kick (rad), the centroid betatron amplitude A = beta |<dx'>| (m) and its
    ratio to the rms beam size, and the filamented horizontal emittance growth (fraction),
    computed from the exact kicks applied to an equilibrium Monte Carlo sample.
    """
    beam = stored_beam_at_nkm(config, ring, n, seed)
    x0 = beam[0] - ring.orbit6[0]
    kx, ky = kicker.kicks(beam[0] + config.closed_orbit_x_m, beam[2])
    beta, alpha = ring.twiss_x
    gamma = (1 + alpha ** 2) / beta
    d, dp = ring.disp_x
    xb, xpb = x0 - d * (beam[4] - ring.orbit6[4]), (beam[1] - ring.orbit6[1]) - dp * (beam[4] - ring.orbit6[4])
    def emit(u, up):
        u, up = u - u.mean(), up - up.mean()
        return float(np.sqrt(np.mean(u * u) * np.mean(up * up) - np.mean(u * up) ** 2))
    e0 = emit(xb, xpb)
    e1 = emit(xb, xpb + kx)
    mean_kick = float(np.mean(kx))
    sigma_x = float(np.sqrt(ring.emit_x_m_rad * beta + (d * ring.energy_spread) ** 2))
    amp = beta * abs(mean_kick)
    # Filamented emittance after decoherence: <J> of the kicked distribution about the new centroid.
    xpk = xpb + kx - mean_kick
    j = gamma * xb ** 2 + 2 * alpha * xb * xpk + beta * xpk ** 2
    eps_fil = float(np.mean(j) / 2)
    return {"kick_model": kicker.model, "n_samples": n, "mean_kick_x_rad": mean_kick,
            "rms_kick_spread_x_rad": float(np.std(kx)), "mean_kick_y_rad": float(np.mean(ky)),
            "centroid_amplitude_m": amp, "rms_beam_size_m": sigma_x, "amplitude_over_sigma": amp / sigma_x,
            "emittance_before_m_rad": e0, "emittance_after_kick_m_rad": e1,
            "filamented_emittance_m_rad": eps_fil, "filamented_emittance_growth": eps_fil / e0 - 1.0,
            "observation": "NKM centre, single pass, linear optics"}


def load_study_config(path: Path) -> InjectionStudyConfig:
    return InjectionStudyConfig.load(path)


def study_provenance(config: InjectionStudyConfig, repo_root: Path) -> Dict[str, Any]:
    from .stage_cli import input_hashes
    return {"schema_version": config.schema_version,
            "input_sha256": input_hashes(Path(repo_root), (config.ring_source, config.kickmap_path))}


# ---------------------------------------------------------------------------
# Coupled BTS handoff and per-process caching
# ---------------------------------------------------------------------------

def booster_beam(initial_twiss: Dict[str, Any], beam: InjectedBeamConfig, n: int, seed: int,
                 centroid: Optional[np.ndarray] = None) -> np.ndarray:
    """Gaussian booster-extraction beam at the BTS entrance (Twiss dict: beta/alpha in m/1, dispersion m/rad)."""
    rng = np.random.default_rng(seed)
    b, a, d = initial_twiss["beta"], initial_twiss["alpha"], initial_twiss["dispersion"]
    out = gaussian_beam(n, (b[0], a[0]), (b[1], a[1]), beam.emit_x_m_rad, beam.emit_y_m_rad,
                        (d[0], d[1]), beam.energy_spread, beam.bunch_length_m, rng)
    if centroid is not None:
        out += np.asarray(centroid, dtype=float)[:, None]
    return out


def track_bts(lattice: at.Lattice, beam: np.ndarray) -> np.ndarray:
    """Single pass through a BTS lattice; lost particles are NaN columns (same column order)."""
    out = np.array(beam, dtype=float, copy=True)
    lattice.track(out, nturns=1, refpts=None, in_place=True)
    return out


def beam_moments(beam: np.ndarray) -> Dict[str, Any]:
    """Centroid (m, rad) and rms Twiss/emittance of live particles in x and y (dispersion removed)."""
    live = np.isfinite(beam[0])
    b = beam[:, live]
    res = {"n_live": int(live.sum())}
    if b.shape[1] < 3:
        return res
    d = b[4] - b[4].mean()
    for name, (i, j) in (("x", (0, 1)), ("y", (2, 3))):
        u, up = b[i] - b[i].mean(), b[j] - b[j].mean()
        var_d = np.mean(d * d)
        if name == "x" and var_d > 0:
            disp, dispp = np.mean(u * d) / var_d, np.mean(up * d) / var_d
            u, up = u - disp * d, up - dispp * d
            res["disp_x_m"], res["disp_px"] = float(disp), float(dispp)
        suu, spp, sup = np.mean(u * u), np.mean(up * up), np.mean(u * up)
        eps = float(np.sqrt(max(suu * spp - sup ** 2, 0.0)))
        res[f"centroid_{name}_m"] = float(b[i].mean())
        res[f"centroid_{name}p_rad"] = float(b[j].mean())
        res[f"emit_{name}_m_rad"] = eps
        res[f"beta_{name}_m"] = float(suu / eps) if eps > 0 else None
        res[f"alpha_{name}"] = float(-sup / eps) if eps > 0 else None
    res["delta_mean"], res["delta_rms"] = float(b[4].mean()), float(b[4].std())
    return res


_RING_CACHE: Dict[str, PreparedRing] = {}


def cached_ring(config: InjectionStudyConfig, repo_root: Path, work_dir: Path) -> PreparedRing:
    """Process-local cache of prepared rings keyed by the lattice-relevant configuration."""
    key = json.dumps([str(Path(repo_root).resolve()), str(Path(work_dir).resolve()), config.ring_source,
                      config.energy_eV, config.septum_edge_x_m, config.septum_to_nkm_drift_m,
                      config.chamber_half_x_m, config.chamber_half_y_m])
    if key not in _RING_CACHE:
        _RING_CACHE[key] = prepare_ring(config, repo_root, work_dir)
    return _RING_CACHE[key]


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> Tuple[Optional[float], Optional[float]]:
    """Wilson score interval for a binomial proportion (default 95 %)."""
    if n <= 0:
        return None, None
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return float(max(0.0, centre - half)), float(min(1.0, centre + half))
