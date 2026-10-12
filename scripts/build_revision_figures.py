#!/usr/bin/env python3
"""C10 — Figures, tables and LaTeX macros of the revised manuscript (journal campaign 02).

Extends ``build_journal_figures.Builder`` (hash-verified artifact loading, macros, provenance). Every number quoted in
the revised manuscript is written to ``journal_macros.tex`` from the artifacts named in the manifest. The principal
kicker model is the exact 3-D filament field (``kicker_model_validation.md``). Figures:

1. NKM geometry and kick profile (computed from the filament geometry and the kick map);
2. dynamic aperture (campaign 01);  3. tracking-backend validation (campaign 01);
4. finite-length mechanism (C2);    5. operating window: grid, angle and position scans (C3);
6. septum phase-space acceptance (C3) and long-term survival (C4);
7. paired controls and stored-beam transparency (C3, C7);
8. combined-error robustness and tolerance curves (C5, C6).

Units in figures: mm, mrad; capture in percent.
"""
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_spec = importlib.util.spec_from_file_location("build_journal_figures",
                                               Path(__file__).resolve().parent / "build_journal_figures.py")
bj = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bj)
BLUES, COL, INK, INK2, MARK, tex_sci = bj.BLUES, bj.COL, bj.INK, bj.INK2, bj.MARK, bj.tex_sci

from nkm_injection.injection_study import InjectionStudyConfig, KickModelEvaluator, wilson_interval  # noqa: E402
from nkm_injection.kickmap import NKMKickMap2D  # noqa: E402
from nkm_injection.wire_field import FilamentNKMField  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
COL3 = {"fieldmap_3d": COL["fieldmap"], "dipole": COL["dipole"], "linear": COL["linear"], "off": COL["off"]}
LEVER = 2.2625
TUNE_X_FRAC = 0.17913  # fractional horizontal tune of the KLS lattice (4D linear model, run_survival_validation ring_diagnostics)
THRESHOLD = 0.80  # declared capture threshold defining the operating window (before the scans were analysed)


def wilson(k, n):
    lo, hi = wilson_interval(int(k), int(n))
    return lo, hi


def crossings(x, y, level):
    """Linear-interpolated crossings of y = level (x sorted)."""
    out = []
    for i in range(len(x) - 1):
        if (y[i] - level) * (y[i + 1] - level) < 0:
            out.append(x[i] + (level - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i]))
    return out


class RevisionBuilder(bj.Builder):
    def _json(self, key):
        return self.load(key)

    def transparency_sensitivities(self):
        if not self.has("round2_transparency"):return
        d=self.load("round2_transparency");rows=[]
        for r in d["wire_sensitivity"]:
            k=r["dipole_derivative_rad_per_m"];j=r["quadrupole_derivative_rad_per_m2"]
            tolerance=["--" if v is None else f"{v*1e6:.2f}" for v in r["tolerance_x_y_m"]]
            rows.append(f"{r['wire']+1} & ${r['axis']}$ & {k[0]:+.3f} & {k[1]:+.3f} & "
                        f"{j[0][0]:+.1f} & {j[0][1]:+.1f} & {tolerance[0]} & {tolerance[1]} \\\\")
        self.macro("WireSensitivityRows","\n".join(rows))
        current=d["independent_loop_current_sensitivity"];rows=[]
        for r in current:
            k=r["dipole_derivative_rad_per_relative_current"];j=r["quadrupole_derivative_rad_per_m_per_relative_current"]
            rows.append(f"{r['loop']+1} & {k[0]:+.4f} & {k[1]:+.4f} & {j[0][0]:+.3f} & "
                        f"{j[0][1]:+.3f} & {r['single_loop_tolerance_relative']*1e4:.2f} \\\\")
        self.macro("LoopSensitivityRows","\n".join(rows))
        self.macro("WireTolMin",min(r["joint_single_error_tolerance_m"] for r in d["wire_sensitivity"])*1e6,"{:.2f}")
        self.macro("WireTolMax",max(r["joint_single_error_tolerance_m"] for r in d["wire_sensitivity"])*1e6,"{:.2f}")
        self.macro("LoopTolerance",tex_sci(min(r["single_loop_tolerance_relative"] for r in current),2))
        for i,plane in enumerate(("X","Y")):
            moment=d["beam_moments"][-1]["planes"][i]
            self.macro(f"AlignedMoment{plane}",tex_sci(moment["emittance_ratio_after_single_pass"]-1,2))
        self.macro("MomentGHOrder",d["beam_moments"][-1]["gh_order_per_axis"],"{:d}")

    def fig_generality(self):
        if "round2_generality" not in self.m["artifacts"]:
            return
        d=self.load("round2_generality")
        fig,axes=plt.subplots(1,2,figsize=(7.4,2.9),layout="constrained")
        for family,marker in ((1.,"o"),(1.25,"s")):
            selected=[r for r in d["rows"] if r["transverse_family_scale"]==family]
            for ax,key in zip(axes,("thin_minus_3d","sliced_minus_3d")):
                ax.scatter([r["eta"] for r in selected],[r[key][1]*1e3 for r in selected],marker=marker,
                           label=f"wire scale {family:g}")
                ax.set_xlabel(r"$\eta=|K|L/(8w)$");ax.set_ylabel("momentum difference [mrad]")
                ax.axhline(0,color=INK2,lw=.5)
        axes[0].set_title("Thin map minus 3-D");axes[1].set_title("Sliced vector map minus 3-D");axes[0].legend()
        self.save(fig,"fig9_generality",["round2_generality"],
                  "deterministic centroids; length/strength scaling and 1.25 transverse wire family; w=kick-lobe FWHM")

    def fig_corrected_ring(self):
        if "round2_ring_scenario" not in self.m["artifacts"]:
            return
        d=self.load("round2_ring_scenario");rows=d["rows"]
        fig,axes=plt.subplots(1,2,figsize=(7.4,2.8),layout="constrained")
        for r in rows:
            xs=np.array(r["da_x_m"])*1e3
            axes[0].plot(xs,np.asarray(r["da_alive"],float),alpha=.4,lw=.8)
        axes[0].set_xlabel("horizontal launch x [mm]");axes[0].set_ylabel("500-turn survival (single particle)")
        x=[r["correction_after_tune"]["history"][-1]["rms_x_m"]*1e6 for r in rows]
        y=[r["correction_after_tune"]["history"][-1]["rms_y_m"]*1e6 for r in rows]
        axes[1].plot(range(1,len(rows)+1),x,"o-",label="horizontal");axes[1].plot(range(1,len(rows)+1),y,"s-",label="vertical")
        axes[1].set_xlabel("ring-error seed index");axes[1].set_ylabel("BPM residual RMS [um]");axes[1].legend()
        self.macro("ScenOrbitXmax",max(x),"{:.1f}");self.macro("ScenOrbitYmax",max(y),"{:.1f}")
        self.macro("ScenTuneMax",tex_sci(max(abs(v) for r in rows for v in r["tune_residual"]),2))
        self.macro("ScenSeeds",len(rows),"{:d}")
        self.save(fig,"fig10_corrected_ring",["round2_ring_scenario"],
                  "10 declared corrected-error seeds; deterministic DA particles and BPM residuals; no sampling interval")

    # ------------------------------------------------------------------ figure 1
    def fig_geometry(self):
        op = InjectionStudyConfig.from_dict(self.load("operating_point_3d"))
        f = FilamentNKMField()
        w = f.geometry.wire_positions() * 1e3
        fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw={"width_ratios": [1, 1.35]}, layout="constrained")
        ax = axes[0]
        g = np.linspace(-14, 14, 57) * 1e-3
        X, Y = np.meshgrid(g, g)
        bx, by, _ = f(X.ravel(), Y.ravel(), 0.0)
        bx, by = bx.reshape(X.shape), by.reshape(X.shape)
        bm = np.hypot(bx, by)
        im = ax.contourf(X * 1e3, Y * 1e3, bm, levels=np.linspace(0, 0.3, 13), cmap=BLUES, extend="max")
        ax.streamplot(X * 1e3, Y * 1e3, bx, by, color=INK2, linewidth=0.5, density=0.9, arrowsize=0.6)
        ax.plot(w[:, 0], w[:, 1], "o", color=INK, ms=4)
        ax.set_aspect("equal"); ax.set_xlim(-14, 14); ax.set_ylim(-14, 14); ax.grid(False)
        ax.set_xlabel("$x$ [mm]"); ax.set_ylabel("$y$ [mm]")
        fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02, ticks=[0, 0.1, 0.2, 0.3]).set_label("$|B|$ at $s=0$ [T]")
        ax = axes[1]
        km = NKMKickMap2D(self.root / op.kickmap_path)
        ev = KickModelEvaluator("fieldmap", op, km, op.nkm_entry_x_m, interpolation="cubic")
        xs = np.linspace(-14, 14, 561) * 1e-3
        k = ev.kicks(xs, np.zeros_like(xs))[0]
        ax.plot(xs * 1e3, k * 1e3, color=COL["fieldmap"], label=f"NKM kick, $S={op.field_scale:g}$ (straight line)")
        xp = np.linspace(4.0, 6.0, 41) * 1e-3
        ax.plot((op.injection_x_m + LEVER * xp) * 1e3, -xp * 1e3, color=INK, ls="--", lw=1.2,
                label=f"required $-x'_{{\\rm in}}$, $x_{{\\rm inj}}={op.injection_x_m*1e3:g}$ mm")
        xc = op.injection_x_m + LEVER * op.injection_xp_rad
        ax.axvline(xc * 1e3, color=INK2, lw=0.8, ls=":")
        ax.set_xlabel("horizontal position at NKM centre $x$ [mm]"); ax.set_ylabel("horizontal kick [mrad]")
        ax.legend(loc="lower right", fontsize=7)
        self.macro("PeakKickMrad", float(np.max(np.abs(k))) * 1e3, "{:.2f}")
        self.macro("PeakKickXmm", float(xs[np.argmax(np.abs(k))]) * 1e3, "{:.1f}")
        self.macro("WireInnerMm", f.geometry.x1_m * 1e3, "{:.2f}")
        self.macro("WireOuterMm", f.geometry.x2_m * 1e3, "{:.2f}")
        self.macro("NKMLengthMm", 2 * f.geometry.half_length_m * 1e3, "{:.0f}")
        self.macro("NKMCurrentA", abs(f.geometry.current_A), "{:.0f}")
        self.save(fig, "fig1_nkm_geometry", ["operating_point_3d"],
                  "exact filament field at s=0 (left); kick map at y=0, bicubic (right); required kick for the selected x_inj")

    # ------------------------------------------------------------------ figure 4
    def fig_mechanism(self):
        d = self.load("mechanism")
        v = self.load("kicker_validation")
        dg = self.load("vertical_diagnostic")
        fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7), gridspec_kw={"width_ratios": [1.2, 1.1, 1]}, layout="constrained")
        ax = axes[0]
        e = np.asarray(d["angle_error_rad"]) * 1e3
        sty = {"thin": (COL["dipole"], "-", "thin kick"), "straight": (COL["linear"], "--", "straight path"),
               "bent": (INK2, "-", "bent path"), "3d": (COL["fieldmap"], ":", "exact 3-D")}
        for k, (c, ls, lab) in sty.items():
            ax.plot(e, np.asarray(d["amplitude_vs_angle_m"][k]) * 1e3, color=c, ls=ls, lw=2.2 if k == "3d" else 1.6, label=lab)
        ax.set_xlabel("septum angle error [mrad]"); ax.set_ylabel("amplitude after kick [mm]")
        ax.legend(fontsize=6.8, loc="upper center")
        ax = axes[1]
        prof = d["kick_profile"]
        xext = prof["x_m"][int(np.argmin(prof["kick_rad"]))] * 1e3
        ax.axhline(xext, color=INK2, lw=0.8, ls=":")
        ax.text(-0.26, xext + 0.04, "kick extremum", fontsize=6.5, color=INK2)
        for off, c in (("-0.3", COL["linear"]), ("+0.0", INK), ("+0.3", COL["dipole"])):
            for kind, ls, lw in (("straight", "--", 1.0), ("bent", "-", 1.8)):
                tr = np.asarray(d["trajectories_s_x_kickdensity"][f"{kind}_{off}mrad"])
                ax.plot(tr[:, 0], tr[:, 1] * 1e3, color=c, ls=ls, lw=lw,
                        label=f"{off} mrad" if kind == "bent" else None)
        ax.set_xlabel("$s$ in magnet [m]"); ax.set_ylabel("$x$ along path [mm]")
        ax.legend(fontsize=6.5, loc="lower right", title="bent (solid) / straight (dashed)", title_fontsize=6)
        ax = axes[2]
        sc = d["length_scan_bent_fixed_integral"]
        L = [float(k) for k in sc if sc[k]["matched_angle_rad"] is not None]
        for key, c, lab in (("amp_minus03_m", COL["linear"], "$-0.3$ mrad"), ("amp_nominal_m", INK, "nominal"),
                            ("amp_plus03_m", COL["dipole"], "$+0.3$ mrad")):
            ax.plot(L, [sc[f"{l:.3f}"][key] * 1e3 for l in L], marker="o", color=c, label=lab)
        ax.set_xlabel("magnet length $L$ [m]"); ax.set_ylabel("amplitude after kick [mm]")
        ax.legend(fontsize=6.8)
        m = d["matched_angle_rad"]
        self.macro("MatchThinMrad", m["thin"] * 1e3, "{:.3f}")
        self.macro("MatchStraightMrad", m["straight"] * 1e3, "{:.3f}")
        self.macro("MatchBentMrad", m["bent"] * 1e3, "{:.4f}")
        self.macro("MatchThreeDMrad", m["3d"] * 1e3, "{:.4f}")
        self.macro("SagittaMm", d["sagitta_m"]["value"] * 1e3, "{:.2f}")
        i0 = int(np.argmin(np.abs(e))); ip = int(np.argmin(np.abs(e - 0.3))); im_ = int(np.argmin(np.abs(e + 0.3)))
        for k, nm in (("thin", "Thin"), ("3d", "ThreeD")):
            a = d["amplitude_vs_angle_m"][k]
            self.macro(f"Amp{nm}Nom", a[i0] * 1e3, "{:.2f}")
            self.macro(f"Amp{nm}Plus", (a[ip] - a[i0]) * 1e3, "{:+.2f}")
            self.macro(f"Amp{nm}Minus", (a[im_] - a[i0]) * 1e3, "{:+.2f}")
        nomatch = [float(k) for k in sc if sc[k]["matched_angle_rad"] is None]
        self.macro("LengthNoMatchM", min(nomatch) if nomatch else float("nan"), "{:.2f}")
        # kicker-model validation numbers (C1)
        ma = v["map_agreement"]
        self.macro("MapAgreeRad", tex_sci(max(ma["kx_vs_int_By"]["max_abs_rad"], ma["ky_vs_int_Bx"]["max_abs_rad"]), 1))
        self.macro("MapAgreeRel", tex_sci(max(ma["kx_vs_int_By"]["max_rel"], ma["ky_vs_int_Bx"]["max_rel"]), 1))
        self.macro("MapNodes", f"{ma['n_nodes']:,d}".replace(",", "\\,"))
        conv = {(c["n_slices"], c["s_span_m"]): c["dpx_vs_finest_rad"] for c in v["convergence"]}
        self.macro("SliceConvRad", tex_sci(abs(conv[(640, 0.45)]), 1))
        ds = v["delta_sensitivity"]
        self.macro("DeltaSensUrad", abs(ds["+3e-03"]["px_rad"] - ds["-3e-03"]["px_rad"]) / 6e-3 * 1e-3 * 1e6, "{:.2f}")
        cm = v["capture_means"]
        for k, nm in (("thin_legacy", "CapThinLegacy"), ("thin", "CapThinPhys"), ("fieldmap_3d", "CapThreeDSame"),
                      ("fieldmap_3d_rematched", "CapThreeDRematch")):
            self.macro(nm, cm[k] * 100, "{:.1f}")
        cr = dg["capture_means"]
        self.macro("CapThreeDNoVert", cr["fieldmap_3d_rematched_novert"] * 100, "{:.1f}")
        self.macro("CapThreeDVertDiag", cr["fieldmap_3d_rematched"] * 100, "{:.1f}")
        self.macro("CapThickOneD", cr["thick1d"] * 100, "{:.1f}")
        vy = v["centroid_response"]
        self.macro("VertKickThreeD", vy["fieldmap_3d"]["y+1mm"]["py_rad"] * 1e3, "{:.2f}")
        self.macro("VertKickThin", vy["thin"]["y+1mm"]["py_rad"] * 1e3, "{:.2f}")
        self.save(fig, "fig4_mechanism", ["mechanism", "kicker_validation", "vertical_diagnostic"],
                  "single-centroid models at their own matched angles (left), centroid path inside the magnet (centre), "
                  "bent-path model vs magnet length at fixed integrated kick (right)")

    # ------------------------------------------------------------------ figure 5
    def fig_window(self):
        grid = self.load("c3_grid")
        ang = self.load("c3_angle")
        pos = self.load("c3_position")
        fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.8), gridspec_kw={"width_ratios": [1.25, 1, 1]}, layout="constrained")
        ax = axes[0]
        xs = sorted({r["x_inj_m"] for r in grid["rows"]} | {s["x_inj_mm"] * 1e-3 for s in grid["skipped"]})
        ss = sorted({r["field_scale"] for r in grid["rows"]} | {s["S"] for s in grid["skipped"]})
        Z = np.full((len(xs), len(ss)), np.nan)
        for r in grid["rows"]:
            Z[xs.index(r["x_inj_m"]), ss.index(r["field_scale"])] = r["models"]["fieldmap_3d"]["capture"] * 100
        im = ax.imshow(Z, origin="upper", cmap=BLUES, vmin=0, vmax=100, aspect="auto")
        for i in range(len(xs)):
            for j in range(len(ss)):
                ax.text(j, i, "—" if np.isnan(Z[i, j]) else f"{Z[i, j]:.0f}", ha="center", va="center", fontsize=6.5,
                        color="white" if (not np.isnan(Z[i, j]) and Z[i, j] > 60) else INK)
        ax.set_xticks(range(len(ss))); ax.set_xticklabels([f"{s:g}" for s in ss], fontsize=7)
        ax.set_yticks(range(len(xs))); ax.set_yticklabels([f"{x*1e3:g}" for x in xs], fontsize=7)
        ax.set_xlabel("field scale $S$"); ax.set_ylabel("$x_{\\rm inj}$ [mm]"); ax.grid(False)
        best = max(grid["rows"], key=lambda r: r["models"]["fieldmap_3d"]["ci95"][0])
        from matplotlib.patches import Rectangle
        bi, bj_ = xs.index(best["x_inj_m"]), ss.index(best["field_scale"])
        ax.add_patch(Rectangle((bj_ - 0.5, bi - 0.5), 1, 1, fill=False, ec=COL["dipole"], lw=2))
        ax.set_title("capture [%] at the matched angle", fontsize=8)
        for ax, data, key, lab, nm in ((axes[1], ang, "xp_offset_rad", "angle offset [mrad]", "Angle"),
                                       (axes[2], pos, "dx_offset_m", "position offset [mm]", "Pos")):
            groups = {}
            for r in data["rows"]:
                m = r["models"]["fieldmap_3d"]
                g = groups.setdefault(round(r[key] * 1e3, 4), [0, 0])
                g[0] += m["captured"]; g[1] += m["n"]
            o = np.array(sorted(groups)); k = np.array([groups[v][0] for v in o]); n = np.array([groups[v][1] for v in o])
            c = k / n; ci = np.array([wilson(a, b) for a, b in zip(k, n)])
            ax.fill_between(o, ci[:, 0] * 100, ci[:, 1] * 100, color="#cde2fb", lw=0)
            ax.plot(o, c * 100, color=COL["fieldmap"], marker="o", ms=3)
            ax.axhline(THRESHOLD * 100, color=INK2, lw=0.8, ls="--")
            ax.set_xlabel(lab); ax.set_ylim(0, 100)
            if nm == "Angle":
                ax.set_ylabel("capture [%]")
            else:
                ax.tick_params(labelleft=False)
            cr = crossings(o, c, THRESHOLD)
            lo_c = crossings(o, ci[:, 1], THRESHOLD); hi_c = crossings(o, ci[:, 0], THRESHOLD)
            if len(cr) >= 2:
                self.macro(f"Win{nm}Lo", cr[0], "{:+.2f}"); self.macro(f"Win{nm}Hi", cr[-1], "{:+.2f}")
                self.macro(f"Win{nm}Width", cr[-1] - cr[0], "{:.2f}")
                self.macro(f"Win{nm}LoUnc", max(abs(x - cr[0]) for x in (lo_c[0] if lo_c else cr[0], hi_c[0] if hi_c else cr[0])), "{:.2f}")
                self.macro(f"Win{nm}HiUnc", max(abs(x - cr[-1]) for x in (lo_c[-1] if lo_c else cr[-1], hi_c[-1] if hi_c else cr[-1])), "{:.2f}")
            imax = int(np.argmax(c))
            self.macro(f"Win{nm}BestOffset", o[imax] + 0.0, "{:+.2f}")
            self.macro(f"Win{nm}BestCapture", c[imax] * 100, "{:.1f}")
            self.macro(f"Win{nm}Step", float(np.min(np.diff(o))), "{:.2f}")
            self.macro(f"Win{nm}N", int(n[0]), "{:d}")
        self.macro("WinThreshold", THRESHOLD * 100, "{:.0f}")
        self.macro("OpXinjMm", best["x_inj_m"] * 1e3, "{:.1f}")
        self.macro("OpScale", best["field_scale"], "{:.2f}")
        self.macro("OpXpMrad", best["xp_inj_rad"] * 1e3, "{:.3f}")
        self.macro("OpCentroidMm", (best["x_inj_m"] + LEVER * best["xp_inj_rad"]) * 1e3, "{:.2f}")
        bm = best["models"]["fieldmap_3d"]
        self.macro("OpGridCapture", bm["capture"] * 100, "{:.1f}")
        self.macro("OpGridLo", bm["ci95"][0] * 100, "{:.1f}")
        self.macro("GridPoints", len(grid["rows"]), "{:d}")
        self.macro("GridSkipped", len(grid["skipped"]), "{:d}")
        self.macro("GridParticles", bm["n"], "{:d}")
        self.save(fig, "fig5_operating_window", ["c3_grid", "c3_angle", "c3_position"],
                  "exact 3-D NKM; matched-point grid (200 particles, seed 42); angle and position scans at the selected point "
                  "(2 x 500 particles per value; band: 95 % Wilson); dashed: declared 80 % threshold")

    # ------------------------------------------------------------------ figure 6
    def fig_acceptance(self):
        acc = self.load("c3_acceptance")
        val = self.load("c3_validate")
        lt = self.load("c4_longturn")
        op = InjectionStudyConfig.from_dict(acc["point_config"])
        fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1.3, 1]}, layout="constrained")
        ax = axes[0]
        P = np.asarray(acc["points"]); alive = np.asarray(acc["alive"], bool)
        xs, ps = np.unique(P[:, 0]), np.unique(P[:, 1])
        Z = np.zeros((len(ps), len(xs)))
        for (x, p), a in zip(P, alive):
            Z[np.searchsorted(ps, p), np.searchsorted(xs, x)] = a
        dx, dp = (xs[1] - xs[0]) * 1e3 / 2, (ps[1] - ps[0]) * 1e3 / 2
        ax.imshow(Z, origin="lower", aspect="auto", cmap=BLUES, vmin=0, vmax=1.6, extent=[xs[0] * 1e3 - dx, xs[-1] * 1e3 + dx,
                                                                                      ps[0] * 1e3 - dp, ps[-1] * 1e3 + dp])
        mom = val["rows"][0]["injected_moments"]
        th = np.linspace(0, 2 * np.pi, 200)
        # beam covariance at the septum exit: betatron part from the Twiss moments plus the dispersive part
        e, b, a = mom["emit_x_m_rad"], mom["beta_x_m"], mom["alpha_x"]
        D, Dp, sd = mom["disp_x_m"], mom["disp_px"], mom["delta_rms"]
        cov = e * np.array([[b, -a], [-a, (1 + a * a) / b]]) + sd ** 2 * np.array([[D * D, D * Dp], [D * Dp, Dp * Dp]])
        self.macro("InjSigmaXmm", np.sqrt(cov[0, 0]) * 1e3, "{:.2f}")
        self.macro("InjSigmaXpMrad", np.sqrt(cov[1, 1]) * 1e3, "{:.2f}")
        L = np.linalg.cholesky(cov + 1e-30 * np.eye(2))
        for nsig, ls in ((1, "-"), (2, "--")):
            e = (L @ np.vstack([np.cos(th), np.sin(th)])) * nsig
            ax.plot((op.injection_x_m + e[0]) * 1e3, (op.injection_xp_rad + e[1]) * 1e3, color=COL["dipole"], ls=ls, lw=1.4)
        blade = op.septum_edge_x_m - op.septum_thickness_m
        ax.axvspan(blade * 1e3, xs[-1] * 1e3 + dx, color=INK2, alpha=0.35, lw=0)
        ax.annotate("septum blade\n($x\geq%.0f$ mm lost)" % (blade * 1e3), xy=(blade * 1e3, ps[-1] * 1e3 - 0.4),
                    xytext=(blade * 1e3 - 1.9, ps[-1] * 1e3 - 0.45), fontsize=7, color=INK2, va="center",
                    arrowprops=dict(arrowstyle="->", color=INK2, lw=0.8))
        ax.set_xlabel("$x$ at septum exit [mm]"); ax.set_ylabel("$x'$ at septum exit [mrad]"); ax.grid(False)
        ax = axes[1]
        turns = lt["rows"][0]["turns"]
        flt = np.concatenate([np.asarray(r["first_loss_turn"]) for r in lt["rows"]])
        n = sum(r["n"] for r in lt["rows"])
        t = np.arange(0, turns + 1)
        lost_by = np.array([np.sum((flt >= 0) & (flt < tt)) for tt in t])
        pre = sum(r["loss_causes"].get("septum_creation", 0) + r["loss_causes"].get("outside_field_map", 0) for r in lt["rows"])
        surv = (n - pre - lost_by) / n
        ax.plot(t, surv * 100, color=COL["fieldmap"])
        ax.axvline(500, color=INK2, lw=0.8, ls=":"); ax.text(520, 99, "500 turns", fontsize=7, color=INK2)
        ax.set_xscale("symlog", linthresh=10); ax.set_xlabel("turn"); ax.set_ylabel("surviving fraction [%]")
        ax.set_ylim(80, 100); ax.set_xlim(0, turns * 1.1)
        for tt, nm in ((500, "Short"), (2000, "Mid"), (turns, "Long")):
            self.macro(f"Surv{nm}", surv[min(tt, turns)] * 100, "{:.1f}")
        self.macro("SurvTurns", turns, "{:d}")
        self.macro("SurvN", n, "{:d}")
        k = sum(r["captured"] for r in lt["rows"])
        lo, hi = wilson(k, n)
        self.macro("SurvLongLo", lo * 100, "{:.1f}")
        self.macro("SurvLongHi", hi * 100, "{:.1f}")
        self.macro("SurvSeeds", ", ".join(str(s) for s in sorted({r["seed"] for r in lt["rows"]})))
        late = np.sum(flt >= 500) / n * 100
        self.macro("SurvLateLossPct", late, "{:.1f}")
        self.macro("AccPoints", len(P), "{:d}")
        self.save(fig, "fig6_acceptance_survival", ["c3_acceptance", "c3_validate", "c4_longturn"],
                  "single-particle survival (500 turns, delta=0) in septum phase space with the injected-beam 1/2-sigma ellipses "
                  "and the septum blade (left); surviving fraction of the injected bunch vs turn (right)")

    # ------------------------------------------------------------------ figure 7
    def fig_controls_transparency(self):
        val = self.load("c3_validate")
        tr = self.load("c7_analytic")
        tracked_key="round2_stored_tracked" if self.has("round2_stored_tracked") else "c7_tracked"
        fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1, 1.2]}, layout="constrained")
        ax = axes[0]
        models = ["fieldmap_3d", "linear", "dipole", "off"]
        labels = {"fieldmap_3d": "NKM (3-D)", "linear": "linearised", "dipole": "dipole", "off": "off"}
        caps = {m: np.array([r["models"][m]["capture"] for r in val["rows"]]) for m in models}
        for i, m in enumerate(models):
            ax.scatter(np.full(len(caps[m]), i), caps[m] * 100, color=COL3[m], marker=MARK.get(m, "o") if m != "fieldmap_3d" else "o", s=26, zorder=3)
            mean = caps[m].mean() * 100
            ax.plot([i - 0.25, i + 0.25], [mean] * 2, color=INK, lw=1.4)
            ax.text(i + 0.3, mean, f"{mean:.1f}", va="center", fontsize=7.5)
        ax.set_xticks(range(len(models))); ax.set_xticklabels([labels[m] for m in models], fontsize=7.5)
        ax.set_ylabel("capture, 500 turns [%]"); ax.set_ylim(-3, 103); ax.set_xlim(-0.5, 3.9)
        for m, nm in (("fieldmap_3d", "ValThreeD"), ("linear", "ValLinear"), ("dipole", "ValDipole"), ("off", "ValOff")):
            k = sum(r["models"][m]["captured"] for r in val["rows"]); n = sum(r["models"][m]["n"] for r in val["rows"])
            lo, hi = wilson(k, n)
            self.macro(nm, k / n * 100, "{:.1f}"); self.macro(nm + "Lo", lo * 100, "{:.1f}"); self.macro(nm + "Hi", hi * 100, "{:.1f}")
        for m, nm in (("dipole", "Dipole"), ("linear", "Linear")):
            d = caps["fieldmap_3d"] - caps[m]
            self.macro(f"ValDiff{nm}", d.mean() * 100, "{:+.1f}")
            self.macro(f"ValDiff{nm}Se", d.std(ddof=1) / np.sqrt(len(d)) * 100, "{:.1f}")
        self.macro("ValBunches", len(val["rows"]), "{:d}")
        self.macro("ValParticles", val["rows"][0]["models"]["fieldmap_3d"]["n"], "{:d}")
        ax = axes[1]
        rows = [r for r in tr["offset_response"] if r["dy_m"] == 0.0]
        dx = np.array([r["dx_m"] for r in rows]) * 1e3
        ax.plot(dx[1:], [r["exact"]["x"]["amplitude_over_sigma"] for r in rows[1:]], color=COL["fieldmap"], marker="o", label="horizontal offset: $A_x/\\sigma_x$")
        ax.plot(dx[1:], [r["exact"]["x"]["filamented_emittance_growth"] for r in rows[1:]], color=COL["fieldmap"], ls="--", label="$\\Delta\\varepsilon_x/\\varepsilon_x$ from the kick spread")
        rowsy = [r for r in tr["offset_response"] if r["dy_m"] > 0]
        ax.plot([r["dy_m"] * 1e3 for r in rowsy], [r["exact"]["y"]["amplitude_over_sigma"] for r in rowsy], color=COL["linear"], marker="^", label="vertical offset: $A_y/\\sigma_y$")
        if self.has(tracked_key):
            tk = self.load(tracked_key)
            td = sorted({r["dx_m"] for r in tk["rows"] if r["dx_m"] > 0})
            ax.scatter([d * 1e3 for d in td], [np.mean([r["centroid_x_amplitude_over_sigma"] for r in tk["rows"] if r["dx_m"] == d])
                                               for d in td], marker="s", s=36, facecolors="none", edgecolors=INK, zorder=3,
                       label="tracked $A_x/\\sigma_x$ (turns 1--50)")
        ax.axhline(0.1, color=INK2, lw=0.8, ls=":")
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("NKM–orbit offset [mm]"); ax.set_ylabel("stored-beam response")
        from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
        ax.xaxis.set_major_locator(FixedLocator([0.05, 0.1, 0.2, 0.3, 0.5]))
        ax.xaxis.set_major_formatter(FixedFormatter(["0.05", "0.1", "0.2", "0.3", "0.5"]))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.legend(fontsize=6.8, loc="upper left")
        for r in rows:
            d = r["dx_m"] * 1e3
            if d in (0.1, 0.2, 0.5):
                nm = {0.1: "One", 0.2: "Two", 0.5: "Five"}[d]
                self.macro(f"Transp{nm}Amp", r["exact"]["x"]["amplitude_over_sigma"], "{:.3f}" if d < 0.2 else "{:.2f}")
                self.macro(f"Transp{nm}Emit", tex_sci(r["exact"]["x"]["filamented_emittance_growth"], 2))
                # total rms emittance once the centroid oscillation has also filamented: 1 + A^2/2 + growth
                e = r["exact"]["x"]
                self.macro(f"Transp{nm}Total", 1 + e["amplitude_over_sigma"] ** 2 / 2 + e["filamented_emittance_growth"],
                           "{:.3f}" if d < 0.5 else "{:.2f}")
            if d == 0.1:
                self.macro("TranspBilinOne", r["map_linear"]["x"]["amplitude_over_sigma"], "{:.2f}")
        r0 = rows[0]["exact"]["x"]
        self.macro("TranspAlignedAmp", r0["amplitude_over_sigma"], "{:.0e}" if r0["amplitude_over_sigma"] > 0 else "{:.0f}")
        self.macro("TranspAlignedEmit", tex_sci(r0["filamented_emittance_growth"], 1))
        for r in rowsy:
            if abs(r["dy_m"] - 2e-4) < 1e-9:
                self.macro("TranspVertTwoAmp", r["exact"]["y"]["amplitude_over_sigma"], "{:.2f}")
        self.macro("TranspMCsem", tex_sci(tr["monte_carlo_standard_error_1e5"]["sem_amplitude_over_sigma"], 1))
        self.macro("CubicCoeff", tex_sci(tr["near_axis_fit"]["coefficients_rad_per_m^k"][3], 2))
        self.macro("BicubicErr", tex_sci(tr["map_interpolation_error_near_axis"]["cubic"], 1))
        self.macro("BilinearErr", tex_sci(tr["map_interpolation_error_near_axis"]["linear"], 1))
        self.macro("SigmaXum", tr["optics"]["sigma_x"] * 1e6, "{:.1f}")
        self.macro("EmitYRatio", float(tr["emit_y_assumption"].split("=")[1].split("emit_x")[0]), "{:g}")
        self.macro("CtrlDipoleAmp", abs(val["calibration_k0_k1_xref"][0]) * tr["optics"]["beta_x"] / tr["optics"]["sigma_x"], "{:.0f}")
        if self.has(tracked_key):
            tk = self.load(tracked_key)
            for d, nm in ((0.2, "Two"), (0.5, "Five")):
                rr = [r for r in tk["rows"] if abs(r["dx_m"] - d * 1e-3) < 1e-12]
                if rr:
                    self.macro(f"Tracked{nm}Amp", np.mean([r["centroid_x_amplitude_over_sigma"] for r in rr]), "{:.2f}")
                    self.macro(f"Tracked{nm}EmitRatio", np.mean([r["emit_x_ratio_last"] for r in rr]), "{:.2f}")
            self.macro("TrackedTurns", tk["rows"][0]["turns"], "{:d}")
        self.save(fig, "fig7_controls_transparency", ["c3_validate", "c7_analytic"] + ([tracked_key] if self.has(tracked_key) else []),
                  "fresh bunches (4 x 500) at the selected point for the 3-D NKM and calibrated controls (left); stored-beam "
                  "response from the exact field with deterministic Gauss-Hermite averaging (right)")

    # ------------------------------------------------------------------ figure 8
    def fig_robustness(self):
        """Combined errors without (prefix c5/c6) and with ideal static orbit correction (c5c/c6c) at the septum exit."""
        seeds = (42, 123, 777)
        levels = (("0", 0.0), ("0.25", 0.25), ("0.5", 0.5), ("0.75", 0.75))
        sets = {}
        for tag, c5, c6 in (("U", "c5", "c6"), ("C", "c5c", "c6c")):
            nkm = self._caps([f"{c5}_raw_{s}" for s in seeds], "fieldmap_3d")
            dip = self._caps([f"{c5}_raw_{s}" for s in seeds], "dipole")
            jit = {f: self._caps([f"{c6}_raw_{lab}"], "fieldmap_3d") for lab, f in levels}
            jit[1.0] = {k: v for k, v in nkm.items() if k[0] == 42}
            xo = self._caps([f"{c6}_raw_x_only"], "fieldmap_3d"); po = self._caps([f"{c6}_raw_xp_only"], "fieldmap_3d")
            fs = sorted(jit)
            mean = np.array([np.mean([x[0] for x in jit[f].values()]) * 100 for f in fs])
            p10 = np.array([np.quantile([x[0] for x in jit[f].values()], 0.1) * 100 for f in fs])
            boot = []
            for f in fs:
                v = np.array([x[0] for x in jit[f].values()])
                b = v[np.random.default_rng(1729).integers(0, len(v), (5000, len(v)))].mean(axis=1)
                boot.append(np.quantile(b, [0.025, 0.975]) * 100)
            sets[tag] = dict(nkm=nkm, dip=dip, jit=jit, xo=xo, po=po, fs=fs, mean=mean, p10=p10, boot=np.array(boot),
                             c5=c5)
        off = self.load("c3_nkm_offset"); emi = self.load("c3_emittance")
        fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [1.15, 1.1, 1]}, layout="constrained")
        ax = axes[0]
        for tag, ls, nm in (("C", "-", "corrected"), ("U", "--", "uncorrected")):
            for key, c, lab in (("nkm", COL["fieldmap"], "NKM"), ("dip", COL["dipole"], "dipole")):
                v = np.sort([x[0] for x in sets[tag][key].values()]) * 100
                ax.step(v, np.arange(1, len(v) + 1) / len(v), where="post", color=c, ls=ls, label=f"{lab}, {nm}")
        ax.set_xlabel("capture per realization [%]"); ax.set_ylabel("cumulative fraction")
        ax.legend(fontsize=6.3, loc="upper left")
        ax = axes[1]
        c = sets["C"]
        ax.fill_between(c["fs"], c["boot"][:, 0], c["boot"][:, 1], color="#cde2fb", lw=0)
        ax.plot(c["fs"], c["mean"], color=COL["fieldmap"], marker="o", label="mean (corr.)")
        ax.plot(c["fs"], c["p10"], color=COL["fieldmap"], ls="--", marker="v", ms=4, label="p10 (corr.)")
        u = sets["U"]
        ax.plot(u["fs"], u["mean"], color=INK2, ls=":", marker="o", ms=3, label="mean (uncorr.)")
        ax.scatter([1.0], [np.mean([x[0] for x in c["xo"].values()]) * 100], marker="s", color=INK, s=22, zorder=3,
                   label="x only (corr.)")
        ax.scatter([1.0], [np.mean([x[0] for x in c["po"].values()]) * 100], marker="D", color=INK2, s=22, zorder=3,
                   label="x$'$ only (corr.)")
        ax.axhline(THRESHOLD * 100, color=INK2, lw=0.6, ls="-.")
        ax.set_xlabel("booster jitter / assumed (0.5 mm, 0.2 mrad)"); ax.set_ylabel("capture [%]")
        ax.set_ylim(0, 100)
        ax.legend(fontsize=5.8, loc="upper center", ncol=3, columnspacing=0.6, handlelength=1.6, handletextpad=0.4,
                  borderaxespad=0.2)
        ax = axes[2]
        g = {}
        for r in off["rows"]:
            m = r["models"]["fieldmap_3d"]; t = g.setdefault(round(r["nkm_offset_m"] * 1e3, 3), [0, 0]); t[0] += m["captured"]; t[1] += m["n"]
        o = np.array(sorted(g)); cc = np.array([g[v][0] / g[v][1] for v in o]) * 100
        ax.plot(o, cc, color=COL["fieldmap"], marker="o")
        ax.set_xlabel("NKM–orbit offset [mm]"); ax.set_ylabel("capture, no other errors [%]"); ax.set_ylim(0, 100)
        axt = ax.twiny(); axt.grid(False)
        emig = {}
        for r in emi["rows"]:
            m = r["models"]["fieldmap_3d"]; t = emig.setdefault(round(r["emit_x_m_rad"] * 1e9, 1), [0, 0]); t[0] += m["captured"]; t[1] += m["n"]
        o = np.array(sorted(emig)); ce = np.array([emig[v][0] / emig[v][1] for v in o]) * 100
        axt.plot(o, ce, color=COL["dipole"], marker="s", ms=4)
        axt.set_xlabel("injected emittance $\\varepsilon_x$ [nm rad]", color=COL["dipole"]); axt.tick_params(axis="x", colors=COL["dipole"])
        for tag, prefix in (("U", ""), ("C", "C")):
            self._robust_macros(prefix, sets[tag])
        self._offset_emittance_macros(emig, off)
        keys = []
        for c5, c6 in (("c5", "c6"), ("c5c", "c6c")):
            keys += [f"{c5}_raw_{s}" for s in seeds] + [f"{c6}_raw_{l}" for l, _ in levels] + [f"{c6}_raw_x_only", f"{c6}_raw_xp_only"]
        self.save(fig, "fig8_robustness", keys + ["c3_nkm_offset", "c3_emittance"],
                  "combined errors with the 3-D NKM and the 3-D-calibrated dipole, with (solid) and without (dashed) ideal "
                  "static orbit correction at the septum exit (left); capture vs booster jitter scale (50 paired "
                  "realizations per level, seed 42; band: bootstrap 95 % of the corrected mean) (centre); capture vs "
                  "NKM-orbit offset and injected emittance without other errors (right)")

    def _robust_macros(self, p, s):
        """Macros Rob<p>*, Jit<p>* for one ensemble set; p = '' (uncorrected) or 'C' (ideal static correction)."""
        nkm, dip, jit = s["nkm"], s["dip"], s["jit"]
        v = np.array([x[0] for x in nkm.values()])
        b = v[np.random.default_rng(1729).integers(0, len(v), (10000, len(v)))].mean(axis=1)
        self.macro(f"Rob{p}Mean", v.mean() * 100, "{:.1f}")
        self.macro(f"Rob{p}MeanLo", np.quantile(b, 0.025) * 100, "{:.1f}")
        self.macro(f"Rob{p}MeanHi", np.quantile(b, 0.975) * 100, "{:.1f}")
        self.macro(f"Rob{p}Median", np.median(v) * 100, "{:.1f}")
        self.macro(f"Rob{p}Pten", np.quantile(v, 0.1) * 100, "{:.1f}")
        self.macro(f"Rob{p}N", len(v), "{:d}")
        k = int(np.sum(v >= THRESHOLD)); lo, hi = wilson(k, len(v))
        self.macro(f"Rob{p}FracEighty", k / len(v) * 100, "{:.0f}")
        self.macro(f"Rob{p}FracEightyLo", lo * 100, "{:.0f}"); self.macro(f"Rob{p}FracEightyHi", hi * 100, "{:.0f}")
        k = int(np.sum(v >= 0.9)); lo, hi = wilson(k, len(v))
        self.macro(f"Rob{p}FracNinety", k / len(v) * 100, "{:.0f}")
        self.macro(f"Rob{p}FracNinetyLo", lo * 100, "{:.0f}"); self.macro(f"Rob{p}FracNinetyHi", hi * 100, "{:.0f}")
        vd = np.array([x[0] for x in dip.values()])
        self.macro(f"Rob{p}DipMean", vd.mean() * 100, "{:.1f}")
        m, lo, hi, n = self._paired(nkm, dip)
        self.macro(f"Rob{p}NkmMinusDip", m * 100, "{:+.1f}"); self.macro(f"Rob{p}NkmMinusDipLo", lo * 100, "{:+.1f}")
        self.macro(f"Rob{p}NkmMinusDipHi", hi * 100, "{:+.1f}"); self.macro(f"Rob{p}PairN", n, "{:d}")
        z = self.load(f"{s['c5']}_summary_42")["zero_error_realization"]
        self.macro(f"Rob{p}ZeroErr", z["fieldmap_3d"] * 100, "{:.1f}")
        self.macro(f"Rob{p}ZeroErrDip", z["dipole"] * 100, "{:.1f}")
        names = {0.0: "Zero", 0.25: "Quarter", 0.5: "Half", 0.75: "ThreeQ", 1.0: "Full"}
        for f, mm, pp, bb in zip(s["fs"], s["mean"], s["p10"], s["boot"]):
            self.macro(f"Jit{p}{names[f]}Mean", mm, "{:.1f}"); self.macro(f"Jit{p}{names[f]}Pten", pp, "{:.1f}")
            self.macro(f"Jit{p}{names[f]}Lo", bb[0], "{:.1f}"); self.macro(f"Jit{p}{names[f]}Hi", bb[1], "{:.1f}")
            vv = np.array([x[0] for x in jit[f].values()])
            self.macro(f"Jit{p}{names[f]}Median", np.median(vv) * 100, "{:.1f}")
            self.macro(f"Jit{p}{names[f]}FracEighty", np.mean(vv >= THRESHOLD) * 100, "{:.0f}")
        # jitter scale for a mean capture at the threshold (linear interpolation of the paired curve); the curve
        # may stay below the threshold even without jitter, then the macro reads "none"
        for arr, nm in ((s["mean"], "Eighty"), (s["boot"][:, 0], "EightyLo"), (s["boot"][:, 1], "EightyHi")):
            cr = crossings(np.array(s["fs"]), np.asarray(arr), THRESHOLD * 100)
            self.macro(f"Jit{p}ScaleFor{nm}", f"{cr[0]:.2f}" if cr else "none", "{}")
        self.macro(f"Jit{p}XOnlyMean", np.mean([x[0] for x in s["xo"].values()]) * 100, "{:.1f}")
        self.macro(f"Jit{p}XpOnlyMean", np.mean([x[0] for x in s["po"].values()]) * 100, "{:.1f}")
        mm, lo2, hi2, _ = self._paired(jit[0.0], jit[1.0])
        self.macro(f"Jit{p}RemovalGain", mm * 100, "{:.1f}"); self.macro(f"Jit{p}RemovalGainLo", lo2 * 100, "{:.1f}")
        self.macro(f"Jit{p}RemovalGainHi", hi2 * 100, "{:.1f}")

    def _offset_emittance_macros(self, emig, off):
        words = {25: "TwentyFive", 50: "Fifty", 100: "Hundred", 150: "OneFifty", 200: "TwoHundred"}
        for e in sorted(emig):
            if int(round(e)) in words:
                self.macro(f"Emit{words[int(round(e))]}Cap", emig[e][0] / emig[e][1] * 100, "{:.1f}")
        g = {}
        for r in off["rows"]:
            m = r["models"]["fieldmap_3d"]; t = g.setdefault(round(r["nkm_offset_m"] * 1e3, 2), [0, 0]); t[0] += m["captured"]; t[1] += m["n"]
        caps = [g[d][0] / g[d][1] * 100 for d in sorted(g)]
        self.macro("OffCapMin", min(caps), "{:.1f}"); self.macro("OffCapMax", max(caps), "{:.1f}")
        self.macro("OffRangeMm", max(abs(d) for d in g), "{:.1f}")

    # ------------------------------------------------------------------ survival / sensitivity tables
    def survival_tables(self):
        if "round2_statistics" in self.m["artifacts"]:
            d2 = self.load("round2_statistics")
            q = d2["paired_jitter"]["c6c_0.25"]
            for key, name in (("mean_difference", "QuarterPairedDiff"), ("mean", "QuarterMean"),
                              ("median", "QuarterMedian"), ("p10", "QuarterPten"),
                              ("fraction_ge_80pct", "QuarterAboveEighty")):
                self.macro(name, q[key] * 100, "{:.2f}")
            self.macro("QuarterPairedLo", q["ci95"][0] * 100, "{:.2f}")
            self.macro("QuarterPairedHi", q["ci95"][1] * 100, "{:.2f}")
            self.macro("QuarterPairs", q["n_pairs"], "{:d}")
        pr = self.load("c4_particles"); ap = self.load("c4_aperture"); re = self.load("c4_ring_errors")
        s = next(iter(pr["summary"].values()))
        self.macro("BigN", s["n"], "{:d}"); self.macro("BigCap", s["capture"] * 100, "{:.1f}")
        self.macro("BigLo", s["ci95"][0] * 100, "{:.1f}"); self.macro("BigHi", s["ci95"][1] * 100, "{:.1f}")
        lc = s["loss_causes"]
        self.macro("BigLossSeptumReturn", lc.get("ring_septum_return", 0), "{:d}")
        self.macro("BigLossElsewhere", lc.get("ring_elsewhere", 0), "{:d}")
        self.macro("BigLossCreation", lc.get("septum_creation", 0), "{:d}")
        self.macro("BigLossMagnet", lc.get("outside_field_map", 0), "{:d}")
        rows = []
        words = {"15": "Fifteen", "12": "Twelve", "11": "Eleven", "10": "Ten"}
        for lab, v in sorted(ap["summary"].items(), key=lambda kv: -float(kv[0].rstrip("mm"))):
            nm = words.get(lab.rstrip("mm"), lab.rstrip("mm").replace(".", "p"))
            self.macro(f"Aper{nm}Cap", v["capture"] * 100, "{:.1f}")
            rows.append((lab, v["capture"]))
        for key, nm in (("c4_aper_y10", "AperDiagYten"), ("c4_aper_xopen", "AperDiagXopen"), ("c4_aper_xopen_novert", "AperDiagNoVert"),
                        ("c4_aper_open_novert", "AperDiagOpenNoVert")):
            v = next(iter(self.load(key)["summary"].values()))
            self.macro(nm, v["capture"] * 100, "{:.1f}")
        seeds = {r["seed"] for r in self.load("c4_aper_open_novert")["rows"]}
        ref = [r["models"]["fieldmap_3d"] for r in self.load("c3_validate")["rows"] if r["seed"] in seeds]
        self.macro("AperDiagRef", sum(m["captured"] for m in ref) / sum(m["n"] for m in ref) * 100, "{:.1f}")
        caps = {}
        tunes = {}
        das = {}
        for r in re["rows"]:
            q = r["quad_rel"]
            caps.setdefault(q, []).append(r["captured"] / r["n"])
            tunes.setdefault(q, []).append(r["ring"]["tunes"][0])
            das.setdefault(q, []).append(r["ring"]["first_unstable_x_neg_m"] or np.nan)
        for q, c in sorted(caps.items()):
            nm = {5e-4: "Low", 1e-3: "High"}.get(q, f"{q:g}")
            c = np.array(c)
            self.macro(f"RingErr{nm}Mean", c.mean() * 100, "{:.1f}")
            self.macro(f"RingErr{nm}Min", c.min() * 100, "{:.1f}")
            self.macro(f"RingErr{nm}Max", c.max() * 100, "{:.1f}")
            self.macro(f"RingErr{nm}Rel", q * 100, "{:.2f}")
            self.macro(f"RingErr{nm}DAmin", np.nanmax(das[q]) * 1e3, "{:.1f}")  # smallest |DA| (least negative edge)
            self.macro(f"RingErr{nm}DAmax", np.nanmin(das[q]) * 1e3, "{:.1f}")
            self.macro(f"RingErr{nm}Seeds", len(c), "{:d}")
        self.macro("RingErrSextRel", re["rows"][0]["sext_rel"] * 100, "{:.1f}")
        self.provenance.append({"asset": "tables/journal_macros.tex#survival", "kind": "macros",
                                "inputs": "c4_particles;c4_aperture;c4_ring_errors", "sha256": "", "data": "survival and sensitivity"})

    # ------------------------------------------------------------------ pulsed-magnet requirements (C8)
    def pulse_macros(self):
        """Parameterised pulse requirements; needs the angle window (fig_window) to have run."""
        from nkm_injection.wire_field import FilamentNKMKicker, centroid_exit
        op = InjectionStudyConfig.from_dict(self.load("operating_point_3d"))
        tr = self.load("c7_analytic")
        circ = 799.30
        t0 = circ / 299792458.0
        self.macro("RevPeriodUs", t0 * 1e6, "{:.3f}")
        km = NKMKickMap2D(self.root / op.kickmap_path)
        ev = KickModelEvaluator("fieldmap", op, km, op.nkm_entry_x_m, interpolation="cubic")
        K = lambda x: float(ev.kicks(np.array([x]), np.array([0.0]))[0][0])
        x1, p1 = centroid_exit(op, FilamentNKMKicker(op, n_slices=640), op.injection_xp_rad)
        bx, ax_ = tr["optics"]["beta_x"], tr["optics"]["alpha_x"]
        g = (1 + ax_ ** 2) / bx
        mu = 2 * np.pi * TUNE_X_FRAC  # linear one-turn rotation at the NKM centre (centroid estimate only)
        M = np.array([[np.cos(mu) + ax_ * np.sin(mu), bx * np.sin(mu)], [-g * np.sin(mu), np.cos(mu) - ax_ * np.sin(mu)]])
        v = np.array([x1, p1])
        width = float(self.macros["WinAngleWidth"]) * 1e-3
        allow = 0.1 * width
        for t, nm in ((1, "One"), (2, "Two"), (3, "Three")):
            v = M @ v
            k = abs(K(v[0]))
            self.macro(f"Turn{nm}Xmm", v[0] * 1e3, "{:.1f}")
            self.macro(f"Turn{nm}KickMrad", k * 1e3, "{:.2f}")
            if nm in ("One", "Two"):
                self.macro(f"Residual{'TurnOne' if nm == 'One' else 'TurnTwo'}", allow / k, "{:.2f}" if allow / k < 1 else "{:.1f}")
        self.macro("ResidualAllowMrad", allow * 1e3, "{:.3f}")
        xs = np.linspace(-0.012, 0.012, 2401)
        kk = np.array([K(x) for x in xs])
        peak = np.max(np.abs(kk)); grad = np.max(np.abs(np.gradient(kk, xs)))
        sig = tr["optics"]["sigma_x"]
        self.macro("DipoleResidualRel", tex_sci(0.1 * sig / bx / peak, 1))
        self.macro("GradResidualRel", tex_sci(4 * np.pi * 1e-4 / bx / grad, 1))
        if "round2_pulse" in self.m["artifacts"]:
            d=self.load("round2_pulse")
            self.macro("RevPeriodUs",d["revolution_period_s"]*1e6,"{:.3f}")
            self.macro("ResidualAllowMrad",d["residual_kick_allowance_rad"]*1e3,"{:.3f}")
            for row,name in zip(d["native_turns"],("One","Two","Three")):
                self.macro(f"Turn{name}Xmm",row["coordinate"][0]*1e3,"{:.1f}")
                self.macro(f"Turn{name}KickMrad",abs(row["straight_line_full_kick_rad"])*1e3,"{:.2f}")
                if name in ("One","Two"):self.macro(f"ResidualTurn{name}",row["allowed_fraction"],"{:.2f}")
            self.macro("PeakPhaseMaxPulseUs",d["peak_phase_maximum_duration_s"]*1e6,"{:.2f}")
            self.macro("NoReturnMaxPulseUs",d["no_return_field_maximum_duration_s"]*1e6,"{:.2f}")
            self.macro("EightUsResidual",d["eight_us_first_return_fraction"],"{:.2f}")
            self.macro("TimingLossMin",tex_sci(min(r["relative_loss"] for r in d["timing"]),2))
            self.macro("TimingLossMax",tex_sci(max(r["relative_loss"] for r in d["timing"]),2))

    # ------------------------------------------------------------------ campaign-01 quantities still quoted
    def legacy_macros(self):
        s5 = self.load("backend_validation")
        da = s5["dynamic_aperture"]["da_x_delta"]["+0.00"]
        self.macro("DAxMinMm", da["x_min_stable_mm"], "{:.0f}")
        self.macro("DAxMaxMm", da["x_max_stable_mm"], "{:.0f}")
        tc = s5["turn_convergence_capture"]
        t = sorted(map(int, tc))
        self.macro("TurnConvShort", tc[str(500)] * 100 if "500" in tc else tc[str(t[0])] * 100, "{:.0f}")
        self.macro("TurnConvLong", tc[str(t[-1])] * 100, "{:.0f}")
        self.macro("TurnConvLongTurns", t[-1], "{:d}")
        tol = self.load("tolerance_replicates")
        p = tol["pooled"]
        self.macro("TolMedianMx", p["quantiles"]["mismatch_x"]["p50"] * 1e3, "{:.3f}")
        self.macro("TolMedianMxLo", p["quantiles"]["mismatch_x"]["p50_ci"][0] * 1e3, "{:.3f}")
        self.macro("TolMedianMxHi", p["quantiles"]["mismatch_x"]["p50_ci"][1] * 1e3, "{:.3f}")
        self.macro("TolFailures", p["failures"]["k"], "{:d}")
        self.macro("TolN", f"{p['failures']['n']:,d}".replace(",", "\\,"))
        self.macro("TolFailUpper", tex_sci(p["failures"]["clopper_pearson"][1], 2))
        big = tol["runs"]["seed2026_400k"]["prefix"]
        self.macro("TolPrefixChangeBig", tex_sci(big["absolute_change"], 2))
        eb = self.load("error_budget")
        for k, nm, sc, fmt in (("booster_x_jitter_std_m", "BudJitX", 1e3, "{:.1f}"), ("booster_xp_jitter_std_rad", "BudJitXp", 1e3, "{:.1f}"),
                               ("quad_k_rel_std", "BudQuadK", 100, "{:.1f}"), ("quad_dx_std_m", "BudQuadDx", 1e6, "{:.0f}"),
                               ("quad_roll_std_rad", "BudQuadRoll", 1e3, "{:.1f}"), ("dipole_b_rel_std", "BudDipB", 100, "{:.2f}"),
                               ("beta_mismatch_rel_std", "BudBetaMis", 100, "{:.0f}"), ("energy_dp_p_std", "BudEnergy", 100, "{:.1f}"),
                               ("emittance_rel_std", "BudEmit", 100, "{:.0f}"), ("espread_std", "BudEspread", 1e4, "{:.0f}"),
                               ("nkm_scale_std", "BudNkmScale", 100, "{:.1f}"), ("nkm_timing_std_mrad", "BudNkmTiming", 1e3, "{:.1f}"),
                               ("nkm_dx_std_m", "BudNkmDx", 1e3, "{:.1f}"), ("ring_co_x_std_m", "BudRingCo", 1e3, "{:.1f}"),
                               ("septum_x_std_m", "BudSeptum", 1e3, "{:.1f}")):
            self.macro(nm, eb[k] * sc, fmt)

    # ------------------------------------------------------------------ helpers reused from the campaign-01 builder
    def has(self, key):
        return key in self.m["artifacts"]

    def _caps(self, keys, model):
        out = {}
        for k in keys:
            d = self.load(k)
            for r in d["realizations"]:
                if r["sample_id"] >= 0:
                    out[(d["cli"]["seed"], r["sample_id"])] = (r["models"][model]["capture_fraction"],
                                                              r["bts_exit"]["centroid_x_m"], r["bts_exit"]["centroid_xp_rad"])
        return out

    _paired = staticmethod(bj.Builder._paired) if hasattr(bj.Builder, "_paired") else None

    def write_macros(self):
        lines = ["% Generated by scripts/build_revision_figures.py; do not edit."]
        for k, v in sorted(self.macros.items()):
            lines.append(f"\\newcommand{{\\{k}}}{{{v}}}")
        (self.out / "tables" / "journal_macros.tex").write_text("\n".join(lines) + "\n")
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
        fixed = {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest() for p in ("By.txt", "kickmap_file.txt", "K4GSR_HBIv4-1.mat")
                 if (self.root / p).exists()}
        self.provenance.append({"asset": "tables/journal_macros.tex", "kind": "macros",
                                "inputs": ";".join(sorted(self.used)) + ";" + ";".join(sorted(fixed)),
                                "sha256": ";".join(self.used[k][1] for k in sorted(self.used)) + ";" + ";".join(fixed[k] for k in sorted(fixed)),
                                "data": f"scalar results quoted in text; generator scripts/build_revision_figures.py at commit {commit}"})


def paired(a, b, seed=1729, count=10000):
    ids = sorted(set(a) & set(b))
    d = np.array([a[i][0] - b[i][0] for i in ids])
    boot = d[np.random.default_rng(seed).integers(0, len(d), size=(count, len(d)))].mean(axis=1)
    return float(d.mean()), float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975)), len(d)


RevisionBuilder._paired = staticmethod(paired)
STEPS = {"legacy": "legacy_macros", "geometry": "fig_geometry", "dynamic_aperture": "fig_dynamic_aperture", "validation": "fig_model_validation",
         "mechanism": "fig_mechanism", "window": "fig_window", "acceptance": "fig_acceptance",
         "controls": "fig_controls_transparency", "robustness": "fig_robustness", "survival": "survival_tables",
         "pulse": "pulse_macros", "generality": "fig_generality", "corrected_ring": "fig_corrected_ring",
         "transparency_sensitivities": "transparency_sensitivities"}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--install-dir", type=Path, default=None)
    p.add_argument("--only", nargs="+", choices=list(STEPS), default=None, help="Build a subset (testing)")
    a = p.parse_args(argv)
    if a.output_dir.exists() and any(a.output_dir.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    (a.output_dir / "figures").mkdir(parents=True, exist_ok=True)
    (a.output_dir / "tables").mkdir(exist_ok=True)
    bj.style()
    b = RevisionBuilder(a.manifest, a.repo_root, a.output_dir)
    for step in (a.only or list(STEPS)):
        getattr(b, STEPS[step])()
    b.write_macros()
    b.write_provenance()
    if a.install_dir:
        if a.only:
            raise SystemExit("--install-dir requires a full build")
        dst = a.install_dir.resolve()
        if dst.exists():
            shutil.rmtree(dst)
        (dst / "figures").mkdir(parents=True)
        for f in (a.output_dir / "figures").glob("*.pdf"):
            shutil.copy2(f, dst / "figures" / f.name)
        for name in ("tables/journal_macros.tex", "figure_provenance.csv", "consumed_artifacts.json"):
            shutil.copy2(a.output_dir / name, dst / Path(name).name)
    print(json.dumps(b.macros, indent=1))


if __name__ == "__main__":
    main()
