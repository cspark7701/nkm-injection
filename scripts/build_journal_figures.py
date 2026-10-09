#!/usr/bin/env python3
"""Task 009 — Build journal figures, tables and LaTeX macros from an explicit campaign manifest.

Every figure/table is computed from the artifacts named in the manifest (no hard-coded results).
Outputs go to a new --output-dir; with --install-dir the PDF figures, tables and macros are also
copied there (e.g. docs/jinst-paper/generated) together with figure_provenance.csv, which records
for each manuscript asset the generator, the consumed artifacts and their SHA-256 digests.

Units in figures: mm, mrad (explicitly converted from m, rad). Capture fractions in percent.
"""
import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.optics import compute_twiss_propagation
from nkm_injection.optimization_handoff import load_optimization_handoff, reference_handoff

# Validated light-mode categorical slots (dataviz reference palette) + neutral reference ink.
COL = {"fieldmap": "#2a78d6", "dipole": "#eb6834", "linear": "#1baf7a", "off": "#52514e"}
MARK = {"fieldmap": "o", "dipole": "s", "linear": "^", "off": "x"}
LABEL = {"fieldmap": "NKM field map", "dipole": "uniform dipole (calibrated)", "linear": "linearised NKM (calibrated)",
         "off": "kicker off"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
BLUES = LinearSegmentedColormap.from_list("seq_blue", ["#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"])


def tex_sci(v, digits=1):
    """LaTeX scientific notation, e.g. 5\\times10^{-6} inside math mode."""
    m, e = f"{v:.{digits - 1}e}".split("e")
    return f"${m}\\times10^{{{int(e)}}}$"


def sci_label(v):
    if v >= 100:
        return f"{v:.0f}"
    if v >= 0.01:
        return f"{v:.2g}"
    m, e = f"{v:.0e}".split("e")
    return f"{m}e{int(e)}"


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9,
                         "legend.fontsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True,
                         "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True, "lines.linewidth": 2.0,
                         "lines.markersize": 5, "savefig.dpi": 300, "figure.dpi": 150, "savefig.bbox": "tight", "savefig.pad_inches": 0.03, "axes.spines.top": False,
                         "axes.spines.right": False, "legend.frameon": False})


class Builder:
    def __init__(self, manifest_path, repo_root, out):
        self.manifest_path = Path(manifest_path).resolve()
        self.m = json.loads(self.manifest_path.read_text())
        self.root, self.out = Path(repo_root).resolve(), Path(out).resolve()
        self.used, self.provenance, self.macros = {}, [], {}

    def _rel(self, p):
        p = Path(p).resolve()
        return p.relative_to(self.root).as_posix() if p.is_relative_to(self.root) else str(p)

    def path(self, key):
        p = Path(self.m["artifacts"][key])
        return p if p.is_absolute() else self.root / p

    def load(self, key):
        p = self.path(key)
        raw = p.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        expected = self.m.get("sha256", {}).get(key)
        if expected and expected != digest:
            raise SystemExit(f"SHA-256 mismatch for {key}: {p}")
        self.used[key] = (str(p), digest)
        return json.loads(raw)

    def save(self, fig, name, keys, caption_data):
        for ext in ("pdf", "png"):
            fig.savefig(self.out / "figures" / f"{name}.{ext}")
        plt.close(fig)
        self.provenance.append({"asset": f"figures/{name}.pdf", "kind": "figure", "inputs": ";".join(keys),
                                "sha256": ";".join(self.used[k][1] for k in keys), "data": caption_data})

    def macro(self, name, value, fmt="{:.3g}"):
        self.macros[name] = fmt.format(value) if not isinstance(value, str) else value

    # ------------------------------------------------------------------
    def fig_kick_geometry(self):
        """Kick-map profile, angle-matching condition and on-momentum DA band."""
        s6 = self.load("operating_region_grid")
        s5 = self.load("backend_validation")
        cfg = InjectionStudyConfig.from_dict(s6["study_config"])
        kmap = NKMKickMap2D(self.root / cfg.kickmap_path)
        x = np.linspace(-20e-3, 20e-3, 801)
        k = cfg.kicker_polarity * kmap.evaluate_kicks(x, np.zeros_like(x))[0]
        da = s5["dynamic_aperture"]["da_x_delta"]["+0.00"]
        lever = cfg.septum_to_nkm_drift_m + 0.2625
        fig, ax = plt.subplots(figsize=(6.2, 3.4), layout="constrained")
        ax.axvspan(da["x_min_stable_mm"], da["x_max_stable_mm"], color="#cde2fb", alpha=0.6, lw=0)
        ax.text(0.5 * (da["x_min_stable_mm"] + da["x_max_stable_mm"]), 6.4, "on-momentum DA (500 turns)",
                ha="center", color=INK2, fontsize=8)
        for scale, ls in ((0.9, ":"), (1.0, "-"), (1.1, "--")):
            ax.plot(x * 1e3, scale * k * 1e3, color=COL["fieldmap"], ls=ls, lw=2, label=f"NKM kick, S = {scale:g}")
        for x_inj, sh in ((-20.0, INK), (-21.0, INK2)):
            xc = np.linspace(x_inj, 0, 50)
            ax.plot(xc, -(xc - x_inj) / lever, color=sh, lw=1.2, ls="-." if sh == INK2 else "-",
                    label=f"required kick $-x'_{{in}}$, $x_{{inj}}$ = {x_inj:g} mm")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_xlabel("horizontal position at NKM centre $x$ [mm]")
        ax.set_ylabel("horizontal kick $\\Delta x'$ [mrad]")
        ax.set_xlim(-20, 20); ax.set_ylim(-7, 7)
        ax.legend(loc="lower right", ncol=1)
        self.macro("DAxMinMm", da["x_min_stable_mm"], "{:.0f}")
        self.macro("DAxMaxMm", da["x_max_stable_mm"], "{:.0f}")
        self.macro("KickPeakMrad", abs(k.min()) * 1e3, "{:.2f}")
        self.macro("KickPeakXmm", x[np.argmin(k)] * 1e3, "{:.1f}")
        self.save(fig, "fig1_kick_geometry", ["operating_region_grid", "backend_validation"],
                  "kick map at y=0 (P=+1) for S=0.9/1.0/1.1; incoming-angle lines; on-momentum DA band")

    def fig_dynamic_aperture(self):
        s5 = self.load("backend_validation")
        raw = json.loads(self.path("backend_validation_raw").read_bytes())
        self.used["backend_validation_raw"] = (str(self.path("backend_validation_raw")),
                                               hashlib.sha256(self.path("backend_validation_raw").read_bytes()).hexdigest())
        turns = s5["cli"]["da_turns"]
        fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), layout="constrained")
        for ax, kind, ylab, ysc in ((axes[0], "da_x_delta", "momentum deviation $\\delta$ [%]", 100),
                                    (axes[1], "da_x_xp", "angle $x'$ [mrad]", 1e3)):
            pts, lt = [], []
            for r in raw:
                if r["kind"] == kind:
                    pts += r["points"]; lt += [t if t >= 0 else turns for t in r["loss_turn"]]
            pts, lt = np.asarray(pts), np.asarray(lt, float)
            ycol = 2 if kind == "da_x_delta" else 1
            xs, ys = np.unique(pts[:, 0]), np.unique(pts[:, ycol])
            grid = np.full((len(ys), len(xs)), np.nan)
            for (px, py), t in zip(pts[:, [0, ycol]], lt):
                grid[np.searchsorted(ys, py), np.searchsorted(xs, px)] = t
            dx, dy = (xs[1] - xs[0]) * 1e3 / 2, (ys[1] - ys[0]) * ysc / 2
            im = ax.imshow(grid, origin="lower", aspect="auto", cmap=BLUES, vmin=0, vmax=turns,
                           extent=[xs[0] * 1e3 - dx, xs[-1] * 1e3 + dx, ys[0] * ysc - dy, ys[-1] * ysc + dy])
            ax.set_xlabel("$x$ at NKM centre [mm]"); ax.set_ylabel(ylab); ax.grid(False)
        cb = fig.colorbar(im, ax=axes, shrink=0.9, pad=0.02)
        cb.set_label("turns survived (max %d)" % turns)
        self.save(fig, "fig2_dynamic_aperture", ["backend_validation", "backend_validation_raw"],
                  f"native AT tracking, single particles, {turns} turns, 1 mm x grid")

    def fig_model_validation(self):
        s5 = self.load("backend_validation")
        pairs = s5["paired_backend_comparison"]
        fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw={"width_ratios": [1.2, 1]}, layout="constrained")
        ax = axes[0]
        models = ["fieldmap", "dipole", "linear"]
        for i, m in enumerate(models):
            rows = [p for p in pairs if p["model"] == m]
            e = np.mean([p["element_capture"] for p in rows]) * 100
            mp = np.mean([p["map_capture"] for p in rows]) * 100
            ax.bar(i - 0.18, e, 0.34, color=COL[m], edgecolor="white", linewidth=1)
            ax.bar(i + 0.18, mp, 0.34, color="white", edgecolor=COL[m], hatch="///", linewidth=1.2)
            ax.text(i - 0.18, e + 1.5, f"{e:.0f}", ha="center", color=INK, fontsize=8)
            ax.text(i + 0.18, mp + 1.5, f"{mp:.0f}", ha="center", color=INK, fontsize=8)
        ax.set_xticks(range(3)); ax.set_xticklabels(["field map", "dipole", "linearised"])
        ax.set_ylabel("capture after 500 turns [%]"); ax.set_ylim(0, 100)
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(facecolor=INK2, label="native element tracking"),
                           Patch(facecolor="white", edgecolor=INK2, hatch="///", label="linear one-turn map")],
                  loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7.5)
        ax2 = axes[1]
        tc = s5["turn_convergence_capture"]
        t = np.array(sorted(map(int, tc))); c = np.array([tc[str(v)] for v in t]) * 100
        ax2.plot(t, c, color=COL["fieldmap"], marker="o")
        ax2.set_xscale("log"); ax2.set_xlabel("turns"); ax2.set_ylabel("field-map capture [%]")
        ax2.set_ylim(0, 100)
        self.macro("ProvCaptureNative", np.mean([p["element_capture"] for p in pairs if p["model"] == "fieldmap"]) * 100, "{:.0f}")
        self.macro("ProvCaptureMap", np.mean([p["map_capture"] for p in pairs if p["model"] == "fieldmap"]) * 100, "{:.0f}")
        self.save(fig, "fig3_model_validation", ["backend_validation"],
                  "provisional point x_inj=-20 mm, x'=5.75 mrad; 200 particles; seeds 42/123/777 (field map), 42 (controls)")

    def fig_operating_region(self):
        s6 = self.load("operating_region_grid")
        rows = [r for r in s6["rows"] if r["group"] == "map" and r["model"] == "fieldmap"]
        xs = sorted({round(r["x_inj_m"] * 1e3, 3) for r in rows}); ss = sorted({r["field_scale"] for r in rows})
        offs = sorted({round(r["xp_offset_rad"] * 1e3, 3) for r in rows})
        fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1.15, 1]}, layout="constrained")
        grid = np.full((len(xs), len(ss)), np.nan)
        for r in rows:
            if abs(r["xp_offset_rad"]) < 1e-12:
                grid[xs.index(round(r["x_inj_m"] * 1e3, 3)), ss.index(r["field_scale"])] = r["capture"] * 100
        ax = axes[0]
        im = ax.imshow(grid, origin="lower", aspect="auto", cmap=BLUES, vmin=0, vmax=100)
        for i in range(len(xs)):
            for j in range(len(ss)):
                v = grid[i, j]
                ax.text(j, i, "—" if np.isnan(v) else f"{v:.0f}", ha="center", va="center", fontsize=7.5,
                        color="white" if (not np.isnan(v) and v > 55) else INK)
        ax.set_xticks(range(len(ss))); ax.set_xticklabels([f"{s:g}" for s in ss])
        ax.set_yticks(range(len(xs))); ax.set_yticklabels([f"{x:g}" for x in xs])
        ax.set_xlabel("NKM field scale $S$"); ax.set_ylabel("$x_{inj}$ at septum [mm]"); ax.grid(False)
        fig.colorbar(im, ax=ax, shrink=0.9, pad=0.02).set_label("capture [%]")
        fig.get_layout_engine().set(wspace=0.12)
        ax2 = axes[1]
        best = max(rows, key=lambda r: (r["ci95"][0], -abs(r["xp_offset_rad"])))
        bx, bs = best["x_inj_m"], best["field_scale"]
        for sc, ls in ((bs, "-"),):
            sel = sorted([r for r in rows if r["x_inj_m"] == bx and r["field_scale"] == sc], key=lambda r: r["xp_offset_rad"])
            o = np.array([r["xp_offset_rad"] for r in sel]) * 1e3
            c = np.array([r["capture"] for r in sel]) * 100
            lo = np.array([r["ci95"][0] for r in sel]) * 100; hi = np.array([r["ci95"][1] for r in sel]) * 100
            ax2.errorbar(o, c, yerr=[c - lo, hi - c], color=COL["fieldmap"], marker="o", capsize=3, ls=ls,
                         label=f"$x_{{inj}}$ = {bx*1e3:g} mm, S = {sc:g}")
        ax2.set_xlabel("angle offset from matched $x'_{inj}$ [mrad]"); ax2.set_ylabel("capture [%]")
        ax2.set_ylim(0, 105); ax2.legend(loc="lower center")
        self.best = best
        self.save(fig, "fig4_operating_region", ["operating_region_grid"],
                  "native tracking, 200 particles, 500 turns, coupled optimised BTS beam, seed 42; 95% Wilson bars")

    def fig_controls(self):
        """Paired capture at the operating point and the bicubic stored-beam response (computed here)."""
        import tempfile
        from dataclasses import replace
        from nkm_injection.injection_study import KickModelEvaluator, prepare_ring, stored_beam_response
        s6r = self.load("operating_region_replicate")
        op = self.load("operating_point_config")
        cfg = InjectionStudyConfig.from_dict(op)
        rows = [r for r in s6r["rows"] if r["group"] == "replicate"]
        models = [m for m in ("fieldmap", "linear", "dipole", "off") if any(r["model"] == m for r in rows)]
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), layout="constrained")
        for i, m in enumerate(models):
            frac = np.array([r["capture"] for r in rows if r["model"] == m])
            caps, mean = frac * 100, np.mean(frac) * 100  # same arithmetic as the text macros
            axes[0].scatter(np.full(len(caps), i), caps, color=COL[m], marker=MARK[m], s=28, zorder=3)
            axes[0].plot([i - 0.25, i + 0.25], [mean] * 2, color=INK, lw=1.5)
            axes[0].text(i + 0.3, mean, f"{mean:.1f}", va="center", fontsize=8, color=INK)
        names = {"fieldmap": "field map", "linear": "linearised", "dipole": "dipole", "off": "off"}
        axes[0].set_xticks(range(len(models))); axes[0].set_xticklabels([names[m] for m in models])
        axes[0].set_ylabel("capture, 500 turns [%]"); axes[0].set_ylim(-3, 105); axes[0].set_xlim(-0.5, len(models) - 0.2)
        kmap = NKMKickMap2D(self.root / cfg.kickmap_path)
        ring = prepare_ring(cfg, self.root, Path(tempfile.mkdtemp()))
        bars = []
        for label, m, off in (("field map\naligned", "fieldmap", 0.0), ("field map\n0.2 mm", "fieldmap", 2e-4),
                              ("field map\n0.5 mm", "fieldmap", 5e-4), ("linearised", "linear", 0.0), ("dipole", "dipole", 0.0)):
            c = replace(cfg, closed_orbit_x_m=off)
            r = stored_beam_response(c, ring, KickModelEvaluator(m, c, kmap, cfg.nkm_entry_x_m), n=100000)
            bars.append((label, m, r["amplitude_over_sigma"], r["filamented_emittance_growth"]))
            self.stored_rows = bars
        for i, (label, m, a, _) in enumerate(bars):
            axes[1].bar(i, a, 0.6, color=COL[m], edgecolor="white")
            axes[1].text(i, a * 2.0, sci_label(a), ha="center", fontsize=7.5, color=INK)
        axes[1].set_yscale("log"); axes[1].set_ylim(1e-6, 1e5)
        axes[1].set_xticks(range(len(bars))); axes[1].set_xticklabels([b[0] for b in bars], fontsize=7)
        axes[1].set_ylabel("stored centroid amplitude / $\\sigma_x$")
        self.macro("StoredAlignedAmp", tex_sci(bars[0][2]))
        self.macro("StoredTwoTenthAmp", bars[1][2], "{:.2f}")
        self.macro("StoredHalfMmAmp", bars[2][2], "{:.1f}")
        self.macro("StoredDipoleAmp", bars[4][2], "{:.0f}")
        self.macro("StoredLinearAmp", bars[3][2], "{:.0f}")
        self.macro("StoredAlignedEmit", tex_sci(bars[0][3]))
        self.save(fig, "fig5_controls", ["operating_region_replicate", "operating_point_config"],
                  "operating point; 4 independent 500-particle bunches; stored response from 1e5-particle equilibrium sample, bicubic map")

    def fig_capture_robustness(self):
        an = self.load("capture_analysis")
        raws = {}
        for key in ("capture_raw_42", "capture_raw_123", "capture_raw_777", "capture_raw_nojitter", "capture_raw_corrected"):
            p = self.path(key); b = p.read_bytes(); self.used[key] = (str(p), hashlib.sha256(b).hexdigest())
            raws[key] = json.loads(b)
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), layout="constrained")
        def ecdf(vals, color, label, ls="-"):
            v = np.sort(np.asarray(vals) * 100)
            axes[0].step(v, np.arange(1, len(v) + 1) / len(v), where="post", color=color, ls=ls, label=label)
        pooled = [r["models"]["fieldmap"]["capture_fraction"] for k in ("capture_raw_42", "capture_raw_123", "capture_raw_777")
                  for r in raws[k]["realizations"] if r["sample_id"] >= 0]
        dip = [r["models"]["dipole"]["capture_fraction"] for r in raws["capture_raw_42"]["realizations"] if r["sample_id"] >= 0]
        noj = [r["models"]["fieldmap"]["capture_fraction"] for r in raws["capture_raw_nojitter"]["realizations"] if r["sample_id"] >= 0]
        cor = [r["models"]["fieldmap"]["capture_fraction"] for r in raws["capture_raw_corrected"]["realizations"] if r["sample_id"] >= 0]
        ecdf(pooled, COL["fieldmap"], f"NKM, all errors ({len(pooled)})")
        ecdf(cor, COL["fieldmap"], f"NKM, static orbit corrected ({len(cor)})", ls="--")
        ecdf(noj, COL["fieldmap"], f"NKM, no booster jitter ({len(noj)})", ls=":")
        ecdf(dip, COL["dipole"], f"dipole control, all errors ({len(dip)})")
        axes[0].set_xlabel("capture per error realization [%]"); axes[0].set_ylabel("cumulative fraction")
        axes[0].legend(loc="lower right", fontsize=7)
        xs, cs = [], []
        for k in ("capture_raw_42", "capture_raw_123", "capture_raw_777"):
            z = None
            for r in raws[k]["realizations"]:
                if r["sample_id"] >= 0:
                    xs.append(abs(r["bts_exit"]["centroid_xp_rad"]) * 1e3); cs.append(r["models"]["fieldmap"]["capture_fraction"] * 100)
        ex, exp_ = [], []
        for k in ("capture_raw_42", "capture_raw_123", "capture_raw_777"):
            for r in raws[k]["realizations"]:
                if r["sample_id"] >= 0:
                    ex.append(r["bts_exit"]["centroid_x_m"]); exp_.append(r["bts_exit"]["centroid_xp_rad"])
        cx = [r["bts_exit"]["centroid_x_m"] for r in raws["capture_raw_corrected"]["realizations"] if r["sample_id"] >= 0]
        cxp = [r["bts_exit"]["centroid_xp_rad"] for r in raws["capture_raw_corrected"]["realizations"] if r["sample_id"] >= 0]
        self.macro("RobExitRmsXmm", float(np.std(cx)) * 1e3, "{:.2f}")      # jitter only (static orbit corrected)
        self.macro("RobExitRmsXpMrad", float(np.std(cxp)) * 1e3, "{:.2f}")
        self.macro("RobExitRmsXmmAll", float(np.std(ex)) * 1e3, "{:.2f}")   # all errors, uncorrected
        sx = [r["bts_exit"]["centroid_x_m"] for r in raws["capture_raw_nojitter"]["realizations"] if r["sample_id"] >= 0]
        self.macro("RobStaticRmsXmm", float(np.sqrt(np.mean(np.square(sx)))) * 1e3, "{:.1f}")  # static only (no jitter)
        axes[1].scatter(xs, cs, s=14, color=COL["fieldmap"], alpha=0.8, edgecolors="none")
        axes[1].set_xlabel("|injected-orbit angle error at septum| [mrad]"); axes[1].set_ylabel("NKM capture [%]")
        axes[1].set_ylim(-3, 103)
        self.robust = {"pooled": pooled, "dipole": dip, "nojitter": noj, "corrected": cor}
        self.save(fig, "fig6_capture_robustness", ["capture_analysis", "capture_raw_42", "capture_raw_123", "capture_raw_777",
                                                   "capture_raw_nojitter", "capture_raw_corrected"],
                  "combined errors; coupled BTS tracking; native ring tracking 500 turns; 200 particles per realization")

    def fig_bts_and_tolerance(self):
        tol = self.load("tolerance_replicates")
        sel = load_optimization_handoff(self.path("optimization_summary"))
        b = self.path("optimization_summary").read_bytes()
        self.used["optimization_summary"] = (str(self.path("optimization_summary")), hashlib.sha256(b).hexdigest())
        ref = reference_handoff()
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1.6, 1]}, layout="constrained")
        for h, lab, ls in ((ref, "baseline", "--"), (sel, "matched", "-")):
            p = compute_twiss_propagation(create_bts_lattice(h.bts), h.initial_twiss)
            s = np.asarray(p["s_pos"]); beta = np.asarray(p["beta"])
            axes[0].plot(s, beta[:, 0], color=COL["fieldmap"], ls=ls, lw=1.6, label=f"$\\beta_x$ {lab}")
            axes[0].plot(s, beta[:, 1], color=COL["dipole"], ls=ls, lw=1.6, label=f"$\\beta_y$ {lab}")
        axes[0].axhline(60, color=INK2, lw=0.8); axes[0].text(0.3, 63, "60 m limit", fontsize=7.5, color=INK2)
        axes[0].set_yscale("log"); axes[0].set_xlabel("$s$ along BTS [m]"); axes[0].set_ylabel("$\\beta$ [m]")
        axes[0].legend(ncol=2, loc="upper left", fontsize=7)
        runs = tol["runs"]
        for i, (lab, r) in enumerate(runs.items()):
            q = r["quantiles"]["mismatch_x"]
            axes[1].errorbar([i], [q["p50"] * 1e3], yerr=[[q["p50"] * 1e3 - q["p50_ci"][0] * 1e3], [q["p50_ci"][1] * 1e3 - q["p50"] * 1e3]],
                             color=COL["fieldmap"], marker="o", capsize=3)
        pooled = tol["pooled"]["quantiles"]["mismatch_x"]
        axes[1].axhspan(pooled["p50_ci"][0] * 1e3, pooled["p50_ci"][1] * 1e3, color="#cde2fb", lw=0)
        axes[1].set_xticks(range(len(runs))); axes[1].set_xticklabels([k.replace("seed", "seed ") for k in runs])
        axes[1].set_ylabel("median $\\mathcal{M}_x$ [$10^{-3}$]")
        self.save(fig, "fig7_bts_tolerance", ["tolerance_replicates", "optimization_summary"],
                  "linear BTS optics; tolerance medians with order-statistic 95% CIs per seed (50,000 samples) and pooled band")

    # ------------------------------------------------------------------
    def tables_and_macros(self):
        tol = self.load("tolerance_replicates")
        s6r = self.load("operating_region_replicate")
        b = self.best
        self.macro("OpXinjMm", b["x_inj_m"] * 1e3, "{:g}")
        self.macro("OpXpMrad", b["xp_inj_rad"] * 1e3, "{:.2f}")
        self.macro("OpScale", b["field_scale"], "{:g}")
        self.macro("OpCaptureGrid", b["capture"] * 100, "{:.1f}")
        rep = [r for r in s6r["rows"] if r["group"] == "replicate"]
        for m in ("fieldmap", "dipole", "linear", "off"):
            caps = [r["capture"] for r in rep if r["model"] == m]
            if caps:
                self.macro(f"Rep{m.capitalize()}Capture", np.mean(caps) * 100, "{:.1f}")
            amps = [r["stored_amp_over_sigma"] for r in rep if r["model"] == m and r["stored_amp_over_sigma"] is not None]
            if amps:
                self.macro(f"Rep{m.capitalize()}AmpSigma", np.mean(amps), "{:.2g}")
        base = [r["capture"] for r in s6r["rows"] if r["group"] == "bts"]
        self.macro("BaselineBTSCapture", np.mean(base) * 100, "{:.1f}")
        an = self.load("capture_analysis")
        pl = an["pooled"]
        self.macro("RobMeanCapture", pl["mean"] * 100, "{:.1f}")
        self.macro("RobMeanCaptureLo", pl["mean_ci95"][0] * 100, "{:.1f}")
        self.macro("RobMeanCaptureHi", pl["mean_ci95"][1] * 100, "{:.1f}")
        self.macro("RobMedianCapture", pl["median"] * 100, "{:.1f}")
        self.macro("RobPFive", pl["p05"] * 100, "{:.1f}")
        self.macro("RobFracAbove", pl["fraction_above_threshold"] * 100, "{:.0f}")
        self.macro("RobNReal", an["n_realizations"], "{:d}")
        self.macro("RobThreshold", pl["threshold"] * 100, "{:.0f}")
        self.macro("RobDipoleMean", np.mean(self.robust["dipole"]) * 100, "{:.1f}")
        self.macro("RobNoJitterMean", np.mean(self.robust["nojitter"]) * 100, "{:.1f}")
        self.macro("RobNoJitterN", len(self.robust["nojitter"]), "{:d}")
        self.macro("RobCorrectedMean", np.mean(self.robust["corrected"]) * 100, "{:.1f}")
        self.macro("RobCorrectedN", len(self.robust["corrected"]), "{:d}")
        self.macro("RobCorrectedFracAbove", np.mean(np.asarray(self.robust["corrected"]) >= 0.9) * 100, "{:.0f}")
        self.macro("RobCorrectedMedian", np.median(self.robust["corrected"]) * 100, "{:.1f}")
        sb = an["stored_beam_cubic"]["amplitude_over_sigma"]
        self.macro("RobStoredMedian", sb["median"], "{:.2f}")
        self.macro("RobStoredPNinetyFive", sb["p95"], "{:.1f}")
        self.macro("RobStoredMax", sb["max"], "{:.1f}")
        top = an["spearman_ranking"][0]
        self.macro("RobTopRho", top["spearman_rho"], "{:.2f}")
        s7 = self.load("capture_robustness")
        self.macro("RobPairedDiff", abs(s7["paired_difference"]["mean_difference_fieldmap_minus_dipole"]) * 100, "{:.1f}")
        self.macro("RobZeroError", s7["zero_error_realization"]["fieldmap"] * 100, "{:.0f}")
        p = tol["pooled"]
        self.macro("TolMedianMx", p["quantiles"]["mismatch_x"]["p50"] * 1e3, "{:.3f}")
        self.macro("TolMedianMxLo", p["quantiles"]["mismatch_x"]["p50_ci"][0] * 1e3, "{:.3f}")
        self.macro("TolMedianMxHi", p["quantiles"]["mismatch_x"]["p50_ci"][1] * 1e3, "{:.3f}")
        self.macro("TolFailures", p["failures"]["k"], "{:d}")
        self.macro("TolN", f"{p['failures']['n']:,d}".replace(",", "\\,"))
        self.macro("TolFailUpper", tex_sci(p["failures"]["clopper_pearson"][1], 2))
        lines = ["% Generated by scripts/build_journal_figures.py; do not edit."]
        for k, v in sorted(self.macros.items()):
            lines.append(f"\\newcommand{{\\{k}}}{{{v}}}")
        (self.out / "tables" / "journal_macros.tex").write_text("\n".join(lines) + "\n")
        self.provenance.append({"asset": "tables/journal_macros.tex", "kind": "macros",
                                "inputs": ";".join(sorted(self.used)), "sha256": ";".join(self.used[k][1] for k in sorted(self.used)),
                                "data": "scalar results quoted in text"})

    def write_provenance(self):
        with open(self.out / "figure_provenance.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["asset", "kind", "inputs", "sha256", "data"])
            w.writeheader(); w.writerows(self.provenance)
        (self.out / "consumed_artifacts.json").write_text(json.dumps(
            {"manifest": self._rel(self.manifest_path), "artifacts": {k: {"path": self._rel(v[0]), "sha256": v[1]} for k, v in self.used.items()}},
            indent=2) + "\n")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--install-dir", type=Path, default=None)
    a = p.parse_args(argv)
    if a.output_dir.exists() and any(a.output_dir.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    (a.output_dir / "figures").mkdir(parents=True, exist_ok=True)
    (a.output_dir / "tables").mkdir(exist_ok=True)
    style()
    b = Builder(a.manifest, a.repo_root, a.output_dir)
    for fn in (b.fig_kick_geometry, b.fig_dynamic_aperture, b.fig_model_validation, b.fig_operating_region,
               b.fig_controls, b.fig_capture_robustness, b.fig_bts_and_tolerance, b.tables_and_macros):
        fn()
    b.write_provenance()
    if a.install_dir:
        dst = a.install_dir.resolve()
        (dst / "figures").mkdir(parents=True, exist_ok=True)
        for f in (a.output_dir / "figures").glob("*.pdf"):
            shutil.copy2(f, dst / "figures" / f.name)
        shutil.copy2(a.output_dir / "tables" / "journal_macros.tex", dst / "journal_macros.tex")
        shutil.copy2(a.output_dir / "figure_provenance.csv", dst / "figure_provenance.csv")
        shutil.copy2(a.output_dir / "consumed_artifacts.json", dst / "consumed_artifacts.json")
    print(json.dumps(b.macros, indent=1))


if __name__ == "__main__":
    main()
