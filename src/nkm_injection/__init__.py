"""NKM public API; subsystems load only when their exports are requested."""
from importlib import import_module

if __name__ != 'nkm_injection':
    raise ImportError('Use nkm_injection, not src.nkm_injection; install the package first.')

__version__ = "0.2.0"

_EXPORTS = {
    'parallel_map': 'concurrency',
    'resolve_workers': 'concurrency',
    'generate_worker_seeds': 'concurrency',
    'SerializableConfigMixin': 'results_schema',
    'PublicationManifest': 'results_schema',
    'PaperResultSchema': 'results_schema',
    'validate_publication_manifest': 'results_schema',
    'initialize_publication_manifest': 'results_schema',
    'compute_input_data_hashes': 'results_schema',
    'BTSConfig': 'bts_lattice',
    'create_bts_lattice': 'bts_lattice',
    'ErrorBudgetConfig': 'errors',
    'sample_error_ensemble': 'errors',
    'OpticsTargetConfig': 'objectives',
    'BTSNormalizedObjectives': 'objectives',
    'BTSConstraintConfig': 'constraints',
    'QuadrupoleHardwareBounds': 'constraints',
    'BTSHardwareConstraints': 'constraints',
    'BTSMOGAConfig': 'moga',
    'BTSMOGAProblem': 'moga',
    'BTSMOGAResult': 'moga',
    'run_bts_moga': 'moga',
    'save_moga_results': 'moga',
    'plot_moga_summary': 'moga',
    'generate_paper_tables': 'paper',
    'generate_paper_figures': 'paper',
    'run_paper_pipeline': 'paper',
    'set_publication_style': 'paper',
    'PUBLICATION_COLORS': 'paper',
    'escape_latex': 'paper',
    'format_scientific': 'paper',
    'format_uncertainty': 'paper',
    'LaTeXTableBuilder': 'paper',
    'LaTeXMacroBuilder': 'paper',
    'BaseFieldMap': 'fieldmap',
    'NKMFieldMap1D': 'fieldmap',
    'NKMFieldMap3D': 'fieldmap',
    'OutOfDomainError': 'fieldmap',
    'integrate_longitudinal_field': 'fieldmap',
    'interpolate_3d_field_vectorized': 'fieldmap',
    'NKMKickMap2D': 'kickmap',
    'TrackingResult': 'tracking',
    'Meters': 'units',
    'Millimeters': 'units',
    'Radians': 'units',
    'Milliradians': 'units',
    'Tesla': 'units',
    'TeslaMeters': 'units',
    'GigaelectronVolts': 'units',
    'ElectronVolts': 'units',
    'validate_positive': 'units',
    'validate_non_zero': 'units',
    'validate_finite': 'units',
    'compute_rigidity': 'units',
    'integrated_field_to_transverse_kicks': 'units',
    'transverse_kicks_to_integrated_field': 'units',
    'FieldMap3DProtocol': 'units',
    'KickerEvaluatorProtocol': 'units',
    'ZeroFieldMap3D': 'units',
    'UniformFieldMap3D': 'units',
    'LinearGradientFieldMap3D': 'units',
    'BaseOpticsObjective': 'optimization',
    'DeterministicObjective': 'optimization',
    'OpticsOptimizer': 'optimization',
    'BTSOptimizationEvaluator': 'optimization',
    'RobustMonteCarloObjective': 'robust_optimization',
    'SeptumModel': 'storage_ring_injection',
    'ElementAperture': 'storage_ring_injection',
    'track_element_resolved_injection': 'storage_ring_injection',
    'StorageRingInjectionConfig': 'storage_ring_injection',
    'OffKickerEvaluator': 'storage_ring_injection',
    'IdealKickerEvaluator': 'storage_ring_injection',
    'LinearKickerEvaluator': 'storage_ring_injection',
    'get_kicker_evaluator': 'storage_ring_injection',
    'BoosterExtractionConfig': 'end_to_end',
    'generate_booster_extraction_distribution': 'end_to_end',
    'run_end_to_end_pipeline': 'end_to_end',
    'InjectionStudyTierConfig': 'convergence_study',
    'ConvergenceScanResult': 'convergence_study',
    'AcceptanceResult': 'convergence_study',
    'EnsembleStudyResult': 'convergence_study',
    'smoke_config': 'convergence_study',
    'pilot_config': 'convergence_study',
    'production_config': 'convergence_study',
    'bootstrap_capture_ci': 'convergence_study',
    'particle_count_convergence_scan': 'convergence_study',
    'turn_count_convergence_scan': 'convergence_study',
    'compute_first_loss_turn_distribution': 'convergence_study',
    'compute_stored_beam_perturbation': 'convergence_study',
    'compute_injection_acceptance': 'convergence_study',
    'run_ensemble_study': 'convergence_study',
}

__all__ = list(_EXPORTS)


def __getattr__(name):
    """Resolve and cache a public export from its canonical module."""
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module('.' + _EXPORTS[name], __name__), name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
