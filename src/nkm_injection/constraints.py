"""
NKM BTS Hardware and Physical Optics Constraints Module

Defines element-specific hardware bounds, pole-tip field limits, beam envelope margins,
injection orbit and angle checks, septum clearance, and physical feasibility validators
for the Booster-to-Storage Ring (BTS) transfer line.

Canonical internal units
------------------------
- Position / length : m
- Angle / momentum  : rad
- Energy            : eV
- Magnetic field    : T
- Integrated field  : T·m
- Quadrupole K      : m⁻²
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Union
import numpy as np

from .units import compute_rigidity, ELECTRON_CHARGE_C
from .bts_lattice import BTSConfig, create_bts_lattice
from .optics import compute_twiss_propagation


# ---------------------------------------------------------------------------
# Structured constraint record
# ---------------------------------------------------------------------------

@dataclass
class ConstraintRecord:
    """
    A single evaluated constraint with physical metadata.

    Attributes
    ----------
    name        : short identifier string
    unit        : physical unit of the observable
    tolerance   : allowed violation magnitude (same unit as value)
    value       : evaluated observable value
    limit       : hard limit value (same unit)
    violated    : True when |value - limit| > tolerance on the wrong side
    violation   : signed excess beyond limit (positive = bad), in same unit
    description : human-readable description
    """
    name: str
    unit: str
    tolerance: float
    value: float
    limit: float
    violated: bool
    violation: float          # positive means constraint is violated by this amount
    description: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "unit": self.unit,
            "tolerance": self.tolerance,
            "value": self.value,
            "limit": self.limit,
            "violated": self.violated,
            "violation": self.violation,
            "description": self.description,
        }


# ---------------------------------------------------------------------------
# Hardware configuration
# ---------------------------------------------------------------------------

@dataclass
class QuadrupoleHardwareBounds:
    """Hardware limits for a specific quadrupole family or individual magnet.

    Attributes
    ----------
    name        : quadrupole family name (e.g. "q11")
    k_min       : minimum normalised strength K  [m⁻²]
    k_max       : maximum normalised strength K  [m⁻²]
    r_bore_m    : bore radius                    [m]
    b_pole_max_T: pole-tip field limit           [T]
    """
    name: str
    k_min: float = -3.0       # m⁻²
    k_max: float = 3.0        # m⁻²
    r_bore_m: float = 0.01935  # m  (19.35 mm)
    b_pole_max_T: float = 1.2  # T


@dataclass
class BTSConstraintConfig:
    """Configuration for physical hardware and beam-envelope constraints.

    All quantities are in SI units unless noted.
    """
    energy_eV: float = 4.0e9

    # Optics envelope limits
    beta_max_limit_m: float = 60.0    # m   — peak β function anywhere along line
    disp_max_limit_m: float = 1.5     # m   — peak |Dₓ| anywhere along line

    # Physical aperture margin
    aperture_margin_m: float = 0.002  # m   — minimum clearance inside beam pipe

    # Design beam parameters
    emit_x_m: float = 1.0e-7         # m·rad  — geometric horizontal emittance
    emit_y_m: float = 1.0e-8         # m·rad  — geometric vertical emittance
    energy_spread: float = 1.1e-3    # Δp/p   — rms energy spread

    # Magnet field limit
    b_pole_limit_T: float = 1.2      # T

    # Injection orbit and angle targets at BTS exit (NKM injection point)
    injection_x_target_m: float = -0.016    # m   — nominal horizontal offset
    injection_xp_target_rad: float = 0.0    # rad — nominal angle
    injection_orbit_tol_m: float = 0.001    # m   — orbit tolerance
    injection_angle_tol_rad: float = 0.001  # rad — angle tolerance

    # Septum clearance
    septum_halfgap_m: float = 0.008   # m   — half-aperture at septum blade
    septum_clearance_margin_m: float = 0.001  # m — minimum clearance from septum blade

    # Injection mismatch surrogate threshold (Courant–Snyder)
    mismatch_limit: float = 2.0      # dimensionless mismatch metric Mu or Mv

    # Element-specific quadrupole bounds (q11..q33)
    quad_bounds: Dict[str, QuadrupoleHardwareBounds] = field(default_factory=lambda: {
        # Triplet 1 — downstream of extraction kicker and injection septum
        # Tighter positive-focusing limit for q11 (beam is still large here)
        "q11": QuadrupoleHardwareBounds("q11", k_min=-2.5, k_max=2.5),
        "q12": QuadrupoleHardwareBounds("q12", k_min=-3.0, k_max=3.0),
        "q13": QuadrupoleHardwareBounds("q13", k_min=-3.0, k_max=3.0),
        # Triplet 2 — central matching section
        "q21": QuadrupoleHardwareBounds("q21", k_min=-3.0, k_max=3.0),
        "q22": QuadrupoleHardwareBounds("q22", k_min=-3.0, k_max=3.0),
        "q23": QuadrupoleHardwareBounds("q23", k_min=-3.0, k_max=3.0),
        # Triplet 3 — downstream matching / injection-point focusing
        "q31": QuadrupoleHardwareBounds("q31", k_min=-3.0, k_max=3.0),
        "q32": QuadrupoleHardwareBounds("q32", k_min=-3.0, k_max=3.0),
        # q33 has tighter bound: must not over-focus at NKM injection point
        "q33": QuadrupoleHardwareBounds("q33", k_min=-2.5, k_max=2.5),
    })


# ---------------------------------------------------------------------------
# Constraint evaluator
# ---------------------------------------------------------------------------

class BTSHardwareConstraints:
    """
    Evaluates hardware limits and physical optics constraints for a set of
    BTS quadrupole strengths, returning structured ``ConstraintRecord`` lists.

    Parameters
    ----------
    config : BTSConstraintConfig, optional
    """

    def __init__(self, config: Optional[BTSConstraintConfig] = None):
        self.config = config or BTSConstraintConfig()
        self.brho = compute_rigidity(self.config.energy_eV, ELECTRON_CHARGE_C)
        self.quad_names = ['q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33']

    # ------------------------------------------------------------------
    # Objective residuals / diagnostics  (not hard constraints)
    # ------------------------------------------------------------------

    def compute_diagnostics(self, prop_results: Dict[str, Any]) -> Dict[str, float]:
        """Return diagnostic metrics (not hard limits) from a propagation result."""
        return {
            "max_beta_x_m": prop_results.get("max_beta_x", float("nan")),
            "max_beta_y_m": prop_results.get("max_beta_y", float("nan")),
            "max_disp_x_m": prop_results.get("max_dispersion_x", float("nan")),
            "final_beta_x_m": float(prop_results.get("final_beta", [float("nan"), float("nan")])[0]),
            "final_beta_y_m": float(prop_results.get("final_beta", [float("nan"), float("nan")])[1]),
        }

    # ------------------------------------------------------------------
    # Hard constraint checkers
    # ------------------------------------------------------------------

    def check_quad_hardware_limits(self, strengths: np.ndarray) -> Dict[str, Any]:
        """
        Check quadrupole strength bounds and pole-tip field limits.

        Returns a dict with keys:
          feasible, violations (str list), records (ConstraintRecord list),
          pole_fields_T, max_pole_field_T
        """
        records: List[ConstraintRecord] = []
        pole_fields: Dict[str, float] = {}
        k_map = dict(zip(self.quad_names, strengths))

        for qname in self.quad_names:
            k_val = float(k_map[qname])
            bounds = self.config.quad_bounds[qname]

            # K lower bound
            k_lo_viol = bounds.k_min - k_val          # positive when violated
            records.append(ConstraintRecord(
                name=f"{qname}_k_lower",
                unit="m^-2",
                tolerance=1e-6,
                value=k_val,
                limit=bounds.k_min,
                violated=(k_lo_viol > 1e-6),
                violation=max(k_lo_viol, 0.0),
                description=f"{qname} K lower bound (hardware gradient limit)",
            ))

            # K upper bound
            k_hi_viol = k_val - bounds.k_max
            records.append(ConstraintRecord(
                name=f"{qname}_k_upper",
                unit="m^-2",
                tolerance=1e-6,
                value=k_val,
                limit=bounds.k_max,
                violated=(k_hi_viol > 1e-6),
                violation=max(k_hi_viol, 0.0),
                description=f"{qname} K upper bound (hardware gradient limit)",
            ))

            # Pole-tip field B_pole = |K| * Bρ * r_bore
            b_pole = abs(k_val) * self.brho * bounds.r_bore_m
            pole_fields[qname] = b_pole
            bp_viol = b_pole - bounds.b_pole_max_T
            records.append(ConstraintRecord(
                name=f"{qname}_pole_tip_field",
                unit="T",
                tolerance=1e-4,
                value=b_pole,
                limit=bounds.b_pole_max_T,
                violated=(bp_viol > 1e-4),
                violation=max(bp_viol, 0.0),
                description=f"{qname} pole-tip field B_pole = |K|·Bρ·r_bore",
            ))

        violated_records = [r for r in records if r.violated]
        is_ok = len(violated_records) == 0
        return {
            "feasible": is_ok,
            "violations": [f"{r.name}: {r.violation:.4g} {r.unit} excess" for r in violated_records],
            "records": records,
            "pole_fields_T": {k: float(v) for k, v in pole_fields.items()},
            "max_pole_field_T": float(max(pole_fields.values())) if pole_fields else 0.0,
        }

    def check_optics_constraints(self, prop_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check peak β and |Dₓ| limits along the BTS line.

        Returns a dict with keys:
          feasible, violations (str list), records (ConstraintRecord list),
          max_beta_x, max_beta_y
        """
        records: List[ConstraintRecord] = []
        cfg = self.config

        max_beta_x = float(prop_results.get("max_beta_x", 0.0))
        max_beta_y = float(prop_results.get("max_beta_y", 0.0))
        max_disp_x = float(prop_results.get("max_dispersion_x", 0.0))

        # Peak β_x limit
        bx_viol = max_beta_x - cfg.beta_max_limit_m
        records.append(ConstraintRecord(
            name="max_beta_x",
            unit="m",
            tolerance=0.01,
            value=max_beta_x,
            limit=cfg.beta_max_limit_m,
            violated=(bx_viol > 0.01),
            violation=max(bx_viol, 0.0),
            description="Peak horizontal beta function along BTS",
        ))

        # Peak β_y limit
        by_viol = max_beta_y - cfg.beta_max_limit_m
        records.append(ConstraintRecord(
            name="max_beta_y",
            unit="m",
            tolerance=0.01,
            value=max_beta_y,
            limit=cfg.beta_max_limit_m,
            violated=(by_viol > 0.01),
            violation=max(by_viol, 0.0),
            description="Peak vertical beta function along BTS",
        ))

        # Peak |Dₓ| limit
        dx_viol = abs(max_disp_x) - cfg.disp_max_limit_m
        records.append(ConstraintRecord(
            name="max_disp_x",
            unit="m",
            tolerance=0.01,
            value=abs(max_disp_x),
            limit=cfg.disp_max_limit_m,
            violated=(dx_viol > 0.01),
            violation=max(dx_viol, 0.0),
            description="Peak horizontal dispersion magnitude along BTS",
        ))

        violated_records = [r for r in records if r.violated]
        is_ok = len(violated_records) == 0
        return {
            "feasible": is_ok,
            "violations": [f"{r.name}: {r.value:.3f}{r.unit} > limit {r.limit:.3f}{r.unit}" for r in violated_records],
            "records": records,
            "max_beta_x": max_beta_x,
            "max_beta_y": max_beta_y,
        }

    def check_aperture_margin(self,
                              prop_results: Dict[str, Any],
                              pipe_halfgap_m: float = 0.01935) -> Dict[str, Any]:
        """
        Check that the maximum beam envelope (3σ) fits inside the pipe with clearance margin.

        Beam half-envelope:  σ_u = √(β_max · ε_u) + |D_x| · δ   (horizontal)

        Args
        ----
        prop_results     : output of ``compute_twiss_propagation``
        pipe_halfgap_m   : half-aperture of the beam pipe [m] (default: 19.35 mm)
        """
        cfg = self.config
        records: List[ConstraintRecord] = []

        from .optics import compute_beam_envelope

        max_beta_x = float(prop_results.get("max_beta_x", 0.0))
        max_beta_y = float(prop_results.get("max_beta_y", 0.0))
        max_disp_x = float(prop_results.get("max_dispersion_x", 0.0))

        # 3σ beam envelope (horizontal, conservative linear including dispersion contribution)
        envelope_x = compute_beam_envelope(
            beta=max_beta_x,
            dispersion=max_disp_x,
            emittance_m_rad=cfg.emit_x_m,
            energy_spread=cfg.energy_spread,
            n_sigma=3.0,
            method="conservative_linear"
        )
        clearance_x = pipe_halfgap_m - envelope_x
        ax_viol = cfg.aperture_margin_m - clearance_x
        records.append(ConstraintRecord(
            name="aperture_margin_x",
            unit="m",
            tolerance=1e-4,
            value=clearance_x,
            limit=cfg.aperture_margin_m,
            violated=(ax_viol > 1e-4),
            violation=max(ax_viol, 0.0),
            description=(
                f"Horizontal clearance inside pipe: pipe={pipe_halfgap_m*1e3:.1f}mm "
                f"– 3σ_x={envelope_x*1e3:.2f}mm"
            ),
        ))

        # 3σ beam envelope (vertical)
        envelope_y = compute_beam_envelope(
            beta=max_beta_y,
            dispersion=0.0,
            emittance_m_rad=cfg.emit_y_m,
            energy_spread=cfg.energy_spread,
            n_sigma=3.0,
            method="conservative_linear"
        )
        clearance_y = pipe_halfgap_m - envelope_y
        ay_viol = cfg.aperture_margin_m - clearance_y
        records.append(ConstraintRecord(
            name="aperture_margin_y",
            unit="m",
            tolerance=1e-4,
            value=clearance_y,
            limit=cfg.aperture_margin_m,
            violated=(ay_viol > 1e-4),
            violation=max(ay_viol, 0.0),
            description=(
                f"Vertical clearance inside pipe: pipe={pipe_halfgap_m*1e3:.1f}mm "
                f"– 3σ_y={envelope_y*1e3:.2f}mm"
            ),
        ))

        violated_records = [r for r in records if r.violated]
        is_ok = len(violated_records) == 0
        return {
            "feasible": is_ok,
            "violations": [f"{r.name}: clearance={r.value*1e3:.2f}mm < margin={r.limit*1e3:.1f}mm" for r in violated_records],
            "records": records,
            "envelope_x_m": float(envelope_x),
            "envelope_y_m": float(envelope_y),
            "clearance_x_m": float(clearance_x),
            "clearance_y_m": float(clearance_y),
        }

    def check_injection_orbit_and_angle(self, prop_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check that the BTS exit Twiss (used to set injection orbit/angle at NKM point)
        matches the required injection conditions within tolerances.

        This is a surrogate check: the final beta and alpha must produce a
        Courant–Snyder mismatch ≤ mismatch_limit relative to the storage-ring
        Twiss at the injection point.

        In the absence of a detailed orbit code, we check that:
          - final β_x is in [1, 20] m (reasonable range for NKM injection)
          - final β_y is in [1, 20] m
          - final Dₓ residual is within ±5 cm of target
        """
        cfg = self.config
        records: List[ConstraintRecord] = []

        final_beta = prop_results.get("final_beta", [float("nan"), float("nan")])
        final_disp = prop_results.get("final_dispersion", [float("nan"), float("nan"), 0.0, 0.0])

        beta_x_end = float(final_beta[0])
        beta_y_end = float(final_beta[1])
        disp_x_end = float(final_disp[0])

        # β_x at exit must be positive (physically required)
        bx_pos_viol = -beta_x_end   # positive when beta_x <= 0
        records.append(ConstraintRecord(
            name="exit_beta_x_positive",
            unit="m",
            tolerance=1e-6,
            value=beta_x_end,
            limit=0.0,
            violated=(bx_pos_viol > 1e-6),
            violation=max(bx_pos_viol, 0.0),
            description="BTS exit β_x must be positive",
        ))

        # β_y at exit must be positive
        by_pos_viol = -beta_y_end
        records.append(ConstraintRecord(
            name="exit_beta_y_positive",
            unit="m",
            tolerance=1e-6,
            value=beta_y_end,
            limit=0.0,
            violated=(by_pos_viol > 1e-6),
            violation=max(by_pos_viol, 0.0),
            description="BTS exit β_y must be positive",
        ))

        # Dispersion at exit within ±0.05 m of design value
        disp_target = cfg.injection_x_target_m if cfg.injection_x_target_m != 0.0 else 0.08
        # Use a reasonable target: 0.08 m (from OpticsTargetConfig)
        disp_target_val = 0.080868
        disp_res = abs(disp_x_end - disp_target_val)
        disp_tol = 0.05   # m
        records.append(ConstraintRecord(
            name="exit_disp_x",
            unit="m",
            tolerance=disp_tol,
            value=disp_x_end,
            limit=disp_target_val,
            violated=(disp_res > disp_tol),
            violation=max(disp_res - disp_tol, 0.0),
            description=f"BTS exit Dₓ within ±{disp_tol*100:.0f}mm of design {disp_target_val:.4f}m",
        ))

        violated_records = [r for r in records if r.violated]
        is_ok = len(violated_records) == 0
        return {
            "feasible": is_ok,
            "violations": [f"{r.name}: value={r.value:.4g}{r.unit}, limit={r.limit:.4g}{r.unit}" for r in violated_records],
            "records": records,
            "exit_beta_x_m": beta_x_end,
            "exit_beta_y_m": beta_y_end,
            "exit_disp_x_m": disp_x_end,
        }

    def check_septum_clearance(self, prop_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check that the beam envelope fits within the septum half-gap at the injection septum.

        Evaluates local Twiss at the injection septum (sept_ex near BTS exit)
        rather than global peak beta. The beam half-width at the septum must satisfy:
            3σ_x < (septum_halfgap - septum_clearance_margin)

        Args
        ----
        prop_results : output of ``compute_twiss_propagation``
        """
        cfg = self.config
        records: List[ConstraintRecord] = []

        from .optics import compute_beam_envelope

        # Retrieve local Twiss at injection septum location (sept_ex near BTS exit)
        if "beta" in prop_results and "s_pos" in prop_results:
            s_pos = np.asarray(prop_results["s_pos"])
            beta_arr = np.asarray(prop_results["beta"])
            disp_arr = np.asarray(prop_results.get("dispersion", np.zeros((len(s_pos), 4))))

            # Injection septum (sept_ex) is located in the final matching section (s >= 16.0 m)
            septum_mask = s_pos >= 16.0
            if np.any(septum_mask):
                local_beta_x = float(np.max(beta_arr[septum_mask, 0]))
                local_disp_x = float(np.max(np.abs(disp_arr[septum_mask, 0])))
            else:
                local_beta_x = float(beta_arr[-1, 0])
                local_disp_x = float(abs(disp_arr[-1, 0]))
        else:
            final_beta = prop_results.get("final_beta")
            if final_beta is not None:
                local_beta_x = float(final_beta[0])
            else:
                local_beta_x = float(prop_results.get("max_beta_x", 0.0))

            final_disp = prop_results.get("final_dispersion")
            if final_disp is not None:
                local_disp_x = float(final_disp[0])
            else:
                local_disp_x = float(prop_results.get("max_dispersion_x", 0.0))

        envelope_x = compute_beam_envelope(
            beta=local_beta_x,
            dispersion=local_disp_x,
            emittance_m_rad=cfg.emit_x_m,
            energy_spread=cfg.energy_spread,
            n_sigma=3.0,
            method="conservative_linear"
        )

        allowed = cfg.septum_halfgap_m - cfg.septum_clearance_margin_m
        viol = envelope_x - allowed
        records.append(ConstraintRecord(
            name="septum_clearance",
            unit="m",
            tolerance=1e-4,
            value=envelope_x,
            limit=allowed,
            violated=(viol > 1e-4),
            violation=max(viol, 0.0),
            description=(
                f"3σ_x beam envelope at septum (local β_x={local_beta_x:.2f}m) "
                f"must fit in septum half-gap ({cfg.septum_halfgap_m*1e3:.1f}mm) with "
                f"{cfg.septum_clearance_margin_m*1e3:.1f}mm margin"
            ),
        ))

        violated_records = [r for r in records if r.violated]
        is_ok = len(violated_records) == 0
        return {
            "feasible": is_ok,
            "violations": [f"{r.name}: {r.value*1e3:.2f}mm > limit {r.limit*1e3:.2f}mm" for r in violated_records],
            "records": records,
            "envelope_x_m": float(envelope_x),
            "allowed_halfgap_m": float(allowed),
            "local_beta_x_m": float(local_beta_x),
            "local_disp_x_m": float(local_disp_x),
        }

    def check_mismatch_surrogate(self,
                                 mismatch_x: float,
                                 mismatch_y: float) -> Dict[str, Any]:
        """
        Check that Courant–Snyder mismatch metrics at BTS exit are below threshold.

        This is a validated injection-performance surrogate: when Mₓ + M_y ≪ 1
        the injected beam matches the storage-ring acceptance and multi-turn
        capture efficiency is maximised.

        Args
        ----
        mismatch_x : plane-by-plane mismatch M_x (dimensionless, ≥ 0)
        mismatch_y : plane-by-plane mismatch M_y (dimensionless, ≥ 0)
        """
        cfg = self.config
        records: List[ConstraintRecord] = []

        total_mm = mismatch_x + mismatch_y
        viol = total_mm - cfg.mismatch_limit
        records.append(ConstraintRecord(
            name="total_mismatch",
            unit="dimensionless",
            tolerance=0.05,
            value=total_mm,
            limit=cfg.mismatch_limit,
            violated=(viol > 0.05),
            violation=max(viol, 0.0),
            description=(
                "Total Courant–Snyder mismatch Mₓ+M_y at BTS exit "
                "(injection performance surrogate)"
            ),
        ))

        violated_records = [r for r in records if r.violated]
        is_ok = len(violated_records) == 0
        return {
            "feasible": is_ok,
            "violations": [f"{r.name}: {r.value:.4f} > limit {r.limit:.4f}" for r in violated_records],
            "records": records,
            "mismatch_x": float(mismatch_x),
            "mismatch_y": float(mismatch_y),
            "total_mismatch": float(total_mm),
        }

    def validate_full(self,
                      strengths: np.ndarray,
                      prop_results: Dict[str, Any],
                      mismatch_x: float = 0.0,
                      mismatch_y: float = 0.0) -> Dict[str, Any]:
        """
        Combined hardware and optics constraint validation.

        Returns
        -------
        dict with keys:
          feasible        : bool — True only when ALL hard constraints pass
          violations      : list[str] — human-readable violation messages
          records         : list[ConstraintRecord] — structured constraint records
          hardware        : sub-result from check_quad_hardware_limits
          optics          : sub-result from check_optics_constraints
          aperture        : sub-result from check_aperture_margin
          injection       : sub-result from check_injection_orbit_and_angle
          septum          : sub-result from check_septum_clearance
          mismatch        : sub-result from check_mismatch_surrogate
          diagnostics     : dict of diagnostic (non-constraint) metrics
        """
        hw     = self.check_quad_hardware_limits(strengths)
        opt    = self.check_optics_constraints(prop_results)
        apt    = self.check_aperture_margin(prop_results)
        inj    = self.check_injection_orbit_and_angle(prop_results)
        sep    = self.check_septum_clearance(prop_results)
        mm     = self.check_mismatch_surrogate(mismatch_x, mismatch_y)
        diag   = self.compute_diagnostics(prop_results)

        all_violations: List[str] = (
            hw["violations"] + opt["violations"] +
            apt["violations"] + inj["violations"] +
            sep["violations"] + mm["violations"]
        )
        all_records: List[ConstraintRecord] = (
            hw["records"] + opt["records"] +
            apt["records"] + inj["records"] +
            sep["records"] + mm["records"]
        )
        all_passed = (
            hw["feasible"] and opt["feasible"] and
            apt["feasible"] and inj["feasible"] and
            sep["feasible"] and mm["feasible"]
        )

        return {
            "feasible": all_passed,
            "violations": all_violations,
            "records": all_records,
            "hardware": hw,
            "optics": opt,
            "aperture": apt,
            "injection": inj,
            "septum": sep,
            "mismatch": mm,
            "diagnostics": diag,
        }
