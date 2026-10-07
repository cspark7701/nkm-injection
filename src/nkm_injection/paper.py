"""
Data-Driven Publication Paper Pipeline & Figure/Table Generation Module

Provides dynamic compilation of publication-quality tables (LaTeX & Markdown) and 300 DPI figures
derived exclusively from validated simulation models and results.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import numpy as np
import matplotlib.pyplot as plt

from .bts_lattice import BTSConfig, create_bts_lattice
from .optics import compute_twiss_propagation, compute_mismatch_metric, DEFAULT_BTS_ENTRANCE_TWISS
from .fieldmap import load_1d_fieldmap, NKMFieldMap1D
from .kickmap import NKMKickMap2D
from .optimization import BTSOptimizationConfig, BTSOptimizationEvaluator
from .constraints import BTSHardwareConstraints, BTSConstraintConfig
from .objectives import OpticsTargetConfig
from .publication_inputs import PublicationInputs, load_publication_inputs
from .results_schema import (
    PaperResultSchema,
    compute_input_data_hashes,
    record_environment_metadata,
    compute_rms_envelope
)


PUBLICATION_COLORS = {
    "beta_x": "#1f77b4",        # Blue
    "beta_y": "#d62728",        # Red
    "dispersion": "#2ca02c",    # Green
    "aperture": "#333333",      # Dark Charcoal
    "injected": "#ff7f0e",      # Orange
    "stored": "#9467bd",        # Purple
    "ideal": "#2ca02c",         # Green
    "fieldmap": "#d62728",      # Red
}


def set_publication_style(font_size: int = 10,
                          dpi: int = 300,
                          use_latex_fonts: bool = False) -> Dict[str, Any]:
    """
    Centralized Publication Plotting Theme Configurator.
    
    Enforces consistent font sizes, DPI, line widths, grid opacity, and color palettes
    across all publication figures generated in the project.
    """
    params = {
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'Lato'],
        'font.size': font_size,
        'axes.labelsize': font_size + 1,
        'axes.titlesize': font_size + 2,
        'xtick.labelsize': font_size,
        'ytick.labelsize': font_size,
        'legend.fontsize': font_size - 1,
        'figure.titlesize': font_size + 3,
        'figure.dpi': dpi,
        'savefig.dpi': dpi,
        'figure.autolayout': True,
        'axes.grid': True,
        'grid.linestyle': ':',
        'grid.alpha': 0.6,
        'lines.linewidth': 1.8,
        'lines.markersize': 5,
    }

    if use_latex_fonts:
        params.update({
            'text.usetex': True,
            'font.family': 'serif',
        })

    plt.rcParams.update(params)
    return params


# ---------------------------------------------------------------------------
# LaTeX Table and Macro Publication Builders (Task 16)
# ---------------------------------------------------------------------------

def escape_latex(text: str) -> str:
    """
    Escape special LaTeX characters (%, _, &, #) in plain text, preserving math mode spans ($...$).
    """
    if not isinstance(text, str):
        return str(text)

    parts = text.split("$")
    escaped_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Non-math part
            p = part
            p = p.replace("\\", "\\textbackslash{}")
            p = p.replace("%", "\\%")
            p = p.replace("_", "\\_")
            p = p.replace("&", "\\&")
            p = p.replace("#", "\\#")
            escaped_parts.append(p)
        else:  # Math part
            escaped_parts.append(f"${part}$")
    return "".join(escaped_parts)


def format_scientific(value: Union[float, int, str], precision: int = 4, sci_threshold: float = 1e-4) -> str:
    """Format a numerical value into clean LaTeX scientific notation if needed."""
    if isinstance(value, (int, np.integer)):
        return str(value)
    if isinstance(value, (float, np.floating)):
        if abs(value) == 0.0:
            return "0"
        if abs(value) < sci_threshold or abs(value) >= 1e5:
            formatted = f"{value:.{precision}e}"
            mantissa, exp = formatted.split("e")
            exp_int = int(exp)
            return f"{float(mantissa):.{precision}f} \\times 10^{{{exp_int}}}"
        return f"{value:.{precision}f}"
    return str(value)


def format_uncertainty(mean: float, std: float, precision: int = 2) -> str:
    """Format value with uncertainty as $mean \\pm std$."""
    return f"${mean:.{precision}f} \\pm {std:.{precision}f}$"


class LaTeXTableBuilder:
    """
    Modular builder for booktabs-formatted LaTeX tables and Markdown tables.
    """
    def __init__(self,
                 caption: str,
                 label: str,
                 columns: List[str],
                 alignment: Optional[str] = None):
        self.caption = caption
        self.label = label
        self.columns = columns
        self.alignment = alignment or ("l" + "c" * (len(columns) - 1))
        self.rows: List[List[Any]] = []

    def add_row(self, *values: Any) -> "LaTeXTableBuilder":
        """Add a row of cell values to the table."""
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            row = list(values[0])
        else:
            row = list(values)
        if len(row) != len(self.columns):
            raise ValueError(f"Row length {len(row)} does not match column count {len(self.columns)}")
        self.rows.append(row)
        return self

    def render_latex(self) -> str:
        """Render complete booktabs-formatted LaTeX table."""
        header_escaped = " & ".join(escape_latex(str(c)) for c in self.columns)
        lines = [
            "\\begin{table}[htbp]",
            "\\centering",
            f"\\caption{{{escape_latex(self.caption)}}}",
            f"\\label{{{self.label}}}",
            f"\\begin{{tabular}}{{{self.alignment}}}",
            "\\toprule",
            f"{header_escaped} \\\\",
            "\\midrule"
        ]
        for row in self.rows:
            row_str = " & ".join(escape_latex(str(v)) for v in row)
            lines.append(f"{row_str} \\\\")
        lines.extend([
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}"
        ])
        return "\n".join(lines) + "\n"

    def render_markdown(self) -> str:
        """Render clean GitHub-flavored Markdown table."""
        lines = [
            f"# {self.caption}\n",
            "| " + " | ".join(str(c) for c in self.columns) + " |",
            "| " + " | ".join([":---" if i == 0 else ":---:" for i in range(len(self.columns))]) + " |"
        ]
        for row in self.rows:
            lines.append("| " + " | ".join(str(v) for v in row) + " |")
        return "\n".join(lines) + "\n"

    def render(self) -> str:
        """Default render method returning LaTeX string."""
        return self.render_latex()

    def save(self, filepath: Union[str, Path]) -> Path:
        """Save table to file (.tex or .md based on extension)."""
        fp = Path(filepath)
        fp.parent.mkdir(parents=True, exist_ok=True)
        content = self.render_markdown() if fp.suffix == ".md" else self.render_latex()
        with open(fp, "w") as f:
            f.write(content)
        return fp


class LaTeXMacroBuilder:
    """
    Builder for LaTeX macros (\\newcommand{\\macroName}{value}).
    """
    def __init__(self):
        self.macros: Dict[str, str] = {}

    def add(self,
            name: str,
            value: Union[str, float, int],
            precision: int = 3,
            unit: Optional[str] = None) -> "LaTeXMacroBuilder":
        """Add a macro definition."""
        macro_name = name.lstrip("\\").replace("_", "").replace("-", "")
        if isinstance(value, (float, np.floating)):
            val_str = f"{value:.{precision}f}"
        else:
            val_str = str(value)

        if unit:
            formatted_val = f"{val_str}\\,\\text{{{unit}}}"
        else:
            formatted_val = val_str

        self.macros[macro_name] = formatted_val
        return self

    def render(self) -> str:
        """Render macro declarations string."""
        lines = [
            "% Auto-generated publication LaTeX macros",
            "% Generated by nkm_injection.paper.LaTeXMacroBuilder",
            ""
        ]
        for name, val in self.macros.items():
            lines.append(f"\\newcommand{{\\{name}}}{{{val}}}")
        return "\n".join(lines) + "\n"

    def save(self, filepath: Union[str, Path]) -> Path:
        """Save macros to a .tex file."""
        fp = Path(filepath)
        fp.parent.mkdir(parents=True, exist_ok=True)
        with open(fp, "w") as f:
            f.write(self.render())
        return fp


def _publication_optics(inputs: Optional[PublicationInputs]):
    """Recompute optics from the selected saved configuration or labelled reference."""
    if inputs is None:
        bts = BTSConfig()
        twiss = DEFAULT_BTS_ENTRANCE_TWISS.to_dict()
        target = OpticsTargetConfig()
        constraints = BTSConstraintConfig()
        bounds = tuple((constraints.quad_bounds[q].k_min, constraints.quad_bounds[q].k_max)
                       for q in ('q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33'))
    else:
        opt = inputs.optimization
        bts, twiss = opt.selected_bts, opt.entrance_twiss
        target, constraints, bounds = opt.target, opt.constraints, opt.strength_bounds_m_inv2
    prop = compute_twiss_propagation(create_bts_lattice(bts), twiss)
    return bts, twiss, prop, target, constraints, bounds


def generate_paper_tables(repo_root: Path, output_dir: Path,
                          inputs: Optional[PublicationInputs] = None) -> Dict[str, str]:
    """
    Generate tables from selected inputs (SI); without inputs, label nominal references.

    Existing two-argument callers retain nominal reference generation. The pipeline
    always supplies validated inputs and never falls back to reference calculations.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {}

    nominal_config, twiss_init, prop, target, constraints, bounds = _publication_optics(inputs)
    source_label = "Selected optimized run" if inputs is not None else "Nominal reference"

    # Table 1: BTS Line & Storage Ring Reference Parameters
    t1_builder = LaTeXTableBuilder(
        caption=f"Table 1: BTS Parameters — {source_label}",
        label="tab:bts_parameters",
        columns=["Parameter", "Symbol", "Value", "Unit"],
        alignment="llcl"
    )
    t1_builder.add_row("Beam Energy", "$E_0$", f"{nominal_config.energy_eV * 1e-9:.1f}", "GeV")
    t1_builder.add_row("Relativistic Gamma", "$\\gamma$", f"{nominal_config.energy_eV / 0.51099895e6:.2f}", "-")
    t1_builder.add_row("Entrance Beta ($\\beta_x, \\beta_y$)", "$(\\beta_{x0}, \\beta_{y0})$", f"({twiss_init['beta'][0]:.4f}, {twiss_init['beta'][1]:.4f})", "m")
    t1_builder.add_row("Entrance Alpha ($\\alpha_x, \\alpha_y$)", "$(\\alpha_{x0}, \\alpha_{y0})$", f"({twiss_init['alpha'][0]:.4f}, {twiss_init['alpha'][1]:.4f})", "-")
    t1_builder.add_row("Entrance Dispersion ($D_x, D_x'$)", "$(D_{x0}, D_{x0}')$", f"({twiss_init['dispersion'][0]:.4f}, {twiss_init['dispersion'][1]:.4f})", "m, rad")
    t1_builder.add_row("Exit Beta ($\\beta_x, \\beta_y$)", "$(\\beta_{xExit}, \\beta_{yExit})$", f"({prop['final_beta'][0]:.4f}, {prop['final_beta'][1]:.4f})", "m")
    t1_builder.add_row("Exit Dispersion ($D_x, D_x'$)", "$(D_{xExit}, D_{xExit}')$", f"({prop['final_dispersion'][0]:.4f}, {prop['final_dispersion'][1]:.4f})", "m, rad")

    t1_builder.save(output_dir / "table1_bts_parameters.tex")
    t1_builder.save(output_dir / "table1_bts_parameters.md")
    tables["table1"] = t1_builder.render_markdown()

    # Table 2: Quadrupole Strengths & Hardware Limits
    t2_builder = LaTeXTableBuilder(
        caption=f"Table 2: Quadrupole Strengths & Hardware Limits — {source_label}",
        label="tab:quad_strengths",
        columns=["Quadrupole", "$K$ [$\\text{m}^{-2}$]", "Hardware Bounds [$\\text{m}^{-2}$]"],
        alignment="lcc"
    )
    quad_names = ['q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33']
    k_list = nominal_config.quad_strengths_list
    for qname, k_val, (lo, hi) in zip(quad_names, k_list, bounds):
        t2_builder.add_row(qname, f"{k_val:+.4f}", f"[{lo:+.4f}, {hi:+.4f}]")

    t2_builder.save(output_dir / "table2_quad_strengths.tex")
    t2_builder.save(output_dir / "table2_quad_strengths.md")
    tables["table2"] = t2_builder.render_markdown()

    # Table 3: Optics Comparison Summary
    t3_builder = LaTeXTableBuilder(
        caption=f"Table 3: Optical Functions & Matching Summary — {source_label}",
        label="tab:optics_summary",
        columns=["Parameter", "Entrance Value", "Exit Value", "Design Target", "Unit"],
        alignment="lcccc"
    )
    t3_builder.add_row("$\\beta_x$", f"{twiss_init['beta'][0]:.4f}", f"{prop['final_beta'][0]:.4f}", f"{target.target_beta_x:.4f}", "m")
    t3_builder.add_row("$\\beta_y$", f"{twiss_init['beta'][1]:.4f}", f"{prop['final_beta'][1]:.4f}", f"{target.target_beta_y:.4f}", "m")
    t3_builder.add_row("$\\alpha_x$", f"{twiss_init['alpha'][0]:.4f}", f"{prop['final_alpha'][0]:.4f}", f"{target.target_alpha_x:.4f}", "-")
    t3_builder.add_row("$\\alpha_y$", f"{twiss_init['alpha'][1]:.4f}", f"{prop['final_alpha'][1]:.4f}", f"{target.target_alpha_y:.4f}", "-")
    t3_builder.add_row("$D_x$", f"{twiss_init['dispersion'][0]:.4f}", f"{prop['final_dispersion'][0]:.4f}", f"{target.target_disp_x:.4f}", "m")

    t3_builder.save(output_dir / "table3_optics_comparison.tex")
    t3_builder.save(output_dir / "table3_optics_comparison.md")
    tables["table3"] = t3_builder.render_markdown()

    # Paper Macros
    macro_builder = LaTeXMacroBuilder()
    macro_builder.add("beamEnergyGeV", nominal_config.energy_eV * 1e-9, precision=1, unit="GeV")
    macro_builder.add("btsLengthM", prop['s_pos'][-1], precision=3, unit="m")
    macro_builder.add("peakBetaXM", float(np.max(prop['beta'][:, 0])), precision=2, unit="m")
    macro_builder.add("peakBetaYM", float(np.max(prop['beta'][:, 1])), precision=2, unit="m")
    macro_builder.save(output_dir / "paper_macros.tex")

    if inputs is not None:
        def save_table(number, name, caption, columns, rows):
            builder = LaTeXTableBuilder(caption, "tab:" + name, columns)
            for row in rows:
                builder.add_row(row)
            for suffix in ("tex", "md"):
                builder.save(output_dir / f"table{number}_{name}.{suffix}")
            tables[f"table{number}"] = builder.render_markdown()

        save_table(4, "injection", "Selected injection model results",
                   ["Model", "Particles", "Turns", "Seeds", "Capture", "CI level", "CI", "Stored oscillation [m]"],
                   [(r.model, r.n_particles, r.n_turns, r.n_seeds, f"{r.capture:.6f}",
                     f"{r.ci_level:.3f}", f"[{r.ci_lo:.6f}, {r.ci_hi:.6f}]",
                     "Unavailable (no survivors)" if r.stored_oscillation_m is None
                     else f"{r.stored_oscillation_m:.8g}") for r in inputs.injection])
        t = inputs.tolerance
        save_table(5, "tolerances", "Selected tolerance study (dimensionless metrics)",
                   ["Samples", "Failure probability", "Median mismatch x", "Median mismatch y"],
                   [(t.n_samples, f"{t.failure_probability:.6f}",
                     f"{t.mismatch_x_median:.6g}", f"{t.mismatch_y_median:.6g}")])
        save_table(6, "moga", "Selected MOGA seed results",
                   ["Seed", "Success", "Feasible fraction", "Pareto count"],
                   [(r.seed, r.success, f"{r.feasible_fraction:.6f}", r.pareto_count) for r in inputs.moga])
        f = inputs.field
        save_table(7, "validation", "Selected field validation and tracking convergence",
                   ["Metric", "Value", "Unit"],
                   [("Peak By", f"{f.peak_by_T:.8g}", "T"),
                    ("Odd symmetry residual", f"{f.odd_symmetry_residual_T:.8g}", "T"),
                    ("Grid interpolation error", f"{f.grid_interpolation_error_mrad:.8g}", "mrad"),
                    ("Recommended slices", inputs.convergence.recommended_slices, "count"),
                    ("Selected mismatch x", f"{inputs.optimization.mismatch_x:.8g}", "1"),
                    ("Selected mismatch y", f"{inputs.optimization.mismatch_y:.8g}", "1")])

    return tables


def generate_paper_figures(repo_root: Path, output_dir: Path,
                           inputs: Optional[PublicationInputs] = None) -> List[Path]:
    """
    Generate figures from selected inputs, with SI figure data saved alongside plots.

    Two-argument callers generate labelled nominal references. Selected-run optics
    are recomputed from saved strengths/Twiss; study metrics are read, not rerun.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    set_publication_style(font_size=10, dpi=300)

    # 1. BTS Optics Propagation
    nominal_config, twiss_init, prop, target, constraints, bounds = _publication_optics(inputs)
    source_label = "Selected optimized run" if inputs is not None else "Nominal reference"

    s = prop["s_pos"]
    beta_x, beta_y = prop["beta"][:, 0], prop["beta"][:, 1]
    dx = prop["dispersion"][:, 0]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(s, beta_x, color=PUBLICATION_COLORS["beta_x"], linestyle='-', label=r'$\beta_x$ (m)')
    ax1.plot(s, beta_y, color=PUBLICATION_COLORS["beta_y"], linestyle='--', label=r'$\beta_y$ (m)')
    ax1.set_ylabel(r'$\beta$ [m]')
    ax1.set_title(f'BTS Optical Functions — {source_label}')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')

    ax2.plot(s, dx, color=PUBLICATION_COLORS["dispersion"], linestyle='-', label=r'$D_x$ (m)')
    ax2.set_xlabel('s [m]')
    ax2.set_ylabel(r'$D_x$ [m]')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right')

    fig_path1 = output_dir / "fig1_bts_optics.png"
    fig.savefig(fig_path1, dpi=300)
    plt.close(fig)
    generated_files.append(fig_path1)

    # 2. Statistically Consistent Beam Envelope (3-sigma)
    fig, ax = plt.subplots(figsize=(10, 4.5))

    env_x_mm = compute_rms_envelope(beta_x, dx, emit_mrad=constraints.emit_x_m, espread=constraints.energy_spread, n_sigma=3.0) * 1e3
    env_y_mm = compute_rms_envelope(beta_y, prop["dispersion"][:, 2], emit_mrad=constraints.emit_y_m, espread=constraints.energy_spread, n_sigma=3.0) * 1e3

    ax.plot(s, env_x_mm, color=PUBLICATION_COLORS["beta_y"], linestyle='-', label=r'Horizontal Total Envelope ($3\sigma_x$)')
    ax.plot(s, -env_x_mm, color=PUBLICATION_COLORS["beta_y"], linestyle='-')
    ax.plot(s, env_y_mm, color=PUBLICATION_COLORS["beta_x"], linestyle='-', label=r'Vertical Total Envelope ($3\sigma_y$)')
    ax.plot(s, -env_y_mm, color=PUBLICATION_COLORS["beta_x"], linestyle='-')
    ax.axhline(nominal_config.ap1_limit * 1e3, color=PUBLICATION_COLORS["aperture"],
               linestyle=':', label='AP1 half-aperture')
    ax.axhline(-nominal_config.ap1_limit * 1e3, color=PUBLICATION_COLORS["aperture"], linestyle=':')

    ax.set_xlabel(r'Longitudinal Coordinate $s$ [m]')
    ax.set_ylabel(r'Beam Envelope [mm]')
    ax.set_title(f'RMS beam envelopes (3 sigma) — {source_label}')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')

    fig_path2 = output_dir / "fig2_beam_envelopes.png"
    fig.savefig(fig_path2, dpi=300)
    plt.close(fig)
    generated_files.append(fig_path2)

    figure_data = {
        "source": source_label,
        "units": {"s": "m", "beta": "m", "dispersion": "m", "envelope": "m"},
        "strengths_m_inv2": nominal_config.quad_strengths_list,
        "s_m": s.tolist(), "beta_m": prop["beta"].tolist(),
        "dispersion_m": prop["dispersion"].tolist(),
        "envelope_x_m": (env_x_mm * 1e-3).tolist(),
        "envelope_y_m": (env_y_mm * 1e-3).tolist(),
        "ap1_half_aperture_m": nominal_config.ap1_limit,
    }
    if inputs is not None:
        fig, axes = plt.subplots(1, 3, figsize=(13, 4))
        inj = inputs.injection
        axes[0].bar([r.model for r in inj], [r.capture for r in inj],
                    yerr=np.array([[r.capture - r.ci_lo for r in inj],
                                   [r.ci_hi - r.capture for r in inj]]), capsize=4)
        axes[0].set_ylabel("Capture fraction (reported CI)")
        axes[0].set_ylim(0, 1.1)
        t = inputs.tolerance
        axes[1].bar(["x", "y"], [t.mismatch_x_median, t.mismatch_y_median])
        axes[1].set_ylabel("Median mismatch")
        axes[1].set_title(f"Tolerance study: {t.n_samples} samples")
        axes[2].bar([str(r.seed) for r in inputs.moga], [r.pareto_count for r in inputs.moga])
        axes[2].set_ylabel("Pareto count")
        axes[2].set_xlabel("MOGA seed (including failed runs)")
        fig.suptitle("Selected simulation runs")
        path = output_dir / "fig3_selected_studies.png"
        fig.savefig(path, dpi=300)
        plt.close(fig)
        generated_files.append(path)

        points = inputs.convergence.points
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot([r.n_slices for r in points], [r.reference_xp_rad for r in points], "o-")
        ax.set_xlabel("NKM slice count")
        ax.set_ylabel("Reference exit angle [rad]")
        ax.set_title("Selected thick-tracking convergence scan")
        path = output_dir / "fig4_tracking_convergence.png"
        fig.savefig(path, dpi=300)
        plt.close(fig)
        generated_files.append(path)
        figure_data.update({
            "injection": [{"model": r.model, "capture": r.capture,
                           "ci_lo": r.ci_lo, "ci_hi": r.ci_hi, "ci_level": r.ci_level}
                          for r in inj],
            "tolerance": {"n_samples": t.n_samples, "mismatch_x_median": t.mismatch_x_median,
                          "mismatch_y_median": t.mismatch_y_median},
            "moga": [{"seed": r.seed, "pareto_count": r.pareto_count} for r in inputs.moga],
            "convergence": [{"n_slices": r.n_slices, "reference_xp_rad": r.reference_xp_rad}
                            for r in points]})
    with open(output_dir / "figure_data.json", "w", encoding="utf-8") as handle:
        json.dump(figure_data, handle, indent=2, allow_nan=False)
    return generated_files


def run_paper_pipeline(repo_root: Optional[Path] = None,
                       run_id: str = "paper_run",
                       manifest: Optional[Union[str, Path, "PublicationManifest"]] = None,
                       create_if_missing: bool = True,
                       compile_pdf: bool = False,
                       workers: Optional[int] = None) -> Dict[str, Any]:
    """
    Execute full data-driven paper pipeline consuming a validated PublicationManifest.
    Fails if manifest validation fails, required files are missing, or input hashes differ.
    """
    from .results_schema import PublicationManifest, validate_publication_manifest

    if repo_root is None:
        repo_root = Path(__file__).resolve().parent.parent.parent

    # Resolve or create default manifest
    if manifest is None:
        default_manifest_path = repo_root / "config" / "publication_manifest.json"
        if default_manifest_path.is_file():
            pub_manifest = PublicationManifest.load(default_manifest_path)
        else:
            pub_manifest = PublicationManifest()
    elif isinstance(manifest, (str, Path)):
        pub_manifest = PublicationManifest.load(manifest)
    else:
        pub_manifest = manifest

    # Validate manifest & upstream runs
    val_status = validate_publication_manifest(pub_manifest, repo_root, create_if_missing=create_if_missing)
    if not val_status["valid"]:
        raise ValueError(f"Publication manifest validation failed with errors: {val_status['errors']}")

    # Require every selected stage artifact before creating publication outputs.
    inputs = load_publication_inputs(pub_manifest, repo_root)

    # Verify input data hashes
    input_hashes = compute_input_data_hashes(repo_root)
    if "MISSING" in input_hashes.values():
        raise FileNotFoundError(f"Missing scientific input data files: {input_hashes}")

    schema = PaperResultSchema(run_id=run_id, base_dir=repo_root / "results" / "paper")
    schema.initialize_directories()

    record_environment_metadata(schema.run_dir)

    with open(schema.run_dir / "input_hashes.json", "w") as f:
        json.dump(input_hashes, f, indent=2)

    pub_manifest.save(schema.run_dir / "publication_manifest.json")

    with open(schema.run_dir / "upstream_artifacts.json", "w", encoding="utf-8") as handle:
        json.dump(inputs.provenance(), handle, indent=2, allow_nan=False)

    tables = generate_paper_tables(repo_root, schema.tables_dir, inputs=inputs)
    figures = generate_paper_figures(repo_root, schema.figures_dir, inputs=inputs)

    pdf_compiled = False
    pdf_path = None
    if compile_pdf:
        jinst_dir = repo_root / "docs" / "jinst-paper"
        tex_file = jinst_dir / "paper.tex"
        if tex_file.is_file():
            import shutil
            import subprocess

            # Copy generated figures into jinst-paper figures directory if present
            jinst_fig_dir = jinst_dir / "figures"
            jinst_fig_dir.mkdir(parents=True, exist_ok=True)
            for fig_p in figures:
                shutil.copy(fig_p, jinst_fig_dir / fig_p.name)

            # Check if pdflatex is available
            if shutil.which("pdflatex"):
                try:
                    cmd_pdf = ["pdflatex", "-interaction=nonstopmode", "paper.tex"]
                    cmd_bib = ["bibtex", "paper"]
                    subprocess.run(cmd_pdf, cwd=jinst_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                    subprocess.run(cmd_bib, cwd=jinst_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                    subprocess.run(cmd_pdf, cwd=jinst_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                    subprocess.run(cmd_pdf, cwd=jinst_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

                    compiled_file = jinst_dir / "paper.pdf"
                    if compiled_file.is_file():
                        pdf_compiled = True
                        pdf_path = str(compiled_file)
                        # Copy generated PDF to run_dir for archival
                        shutil.copy(compiled_file, schema.run_dir / "paper.pdf")
                except Exception as e:
                    print(f"Warning: PDF compilation failed: {e}")

    metrics_summary = {
        "run_id": run_id,
        "manifest_valid": val_status["valid"],
        "input_hashes_verified": True,
        "tables_count": len(tables),
        "figures_count": len(figures),
        "pdf_compiled": pdf_compiled,
        "pdf_path": pdf_path,
        "verified_runs": val_status["verified_runs"],
        "upstream_artifacts": inputs.artifacts,
        "publication_input_schema_version": 1
    }

    with open(schema.run_dir / "metrics.json", "w") as f:
        json.dump(metrics_summary, f, indent=2)

    return metrics_summary
