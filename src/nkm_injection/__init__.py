"""NKM: Nonlinear Kicker Magnet & BTS Line Optimization and Tracking Package."""

__version__ = "0.2.0"

from .concurrency import parallel_map, resolve_workers, generate_worker_seeds
from .results_schema import (
    SerializableConfigMixin,
    PublicationManifest,
    PaperResultSchema,
    validate_publication_manifest,
    compute_input_data_hashes
)
from .bts_lattice import BTSConfig, create_bts_lattice
from .errors import ErrorBudgetConfig, sample_error_ensemble
from .objectives import OpticsTargetConfig, BTSNormalizedObjectives
from .constraints import BTSConstraintConfig, QuadrupoleHardwareBounds, BTSHardwareConstraints
from .moga import (
    BTSMOGAConfig,
    BTSMOGAProblem,
    BTSMOGAResult,
    run_bts_moga,
    save_moga_results,
    plot_moga_summary
)
from .paper import (
    generate_paper_tables,
    generate_paper_figures,
    run_paper_pipeline,
    set_publication_style,
    PUBLICATION_COLORS
)
from .fieldmap import BaseFieldMap, NKMFieldMap1D, OutOfDomainError, integrate_longitudinal_field
from .kickmap import NKMKickMap2D
from .tracking import TrackingResult
from .units import (
    Meters,
    Millimeters,
    Radians,
    Milliradians,
    Tesla,
    TeslaMeters,
    GigaelectronVolts,
    ElectronVolts,
    validate_positive,
    validate_non_zero,
    validate_finite,
    compute_rigidity,
    integrated_field_to_transverse_kicks,
    transverse_kicks_to_integrated_field
)
from .optimization import BaseOpticsObjective, DeterministicObjective, OpticsOptimizer, BTSOptimizationEvaluator
from .robust_optimization import RobustMonteCarloObjective
from .storage_ring_injection import (
    SeptumModel,
    ElementAperture,
    track_element_resolved_injection,
    StorageRingInjectionConfig
)
from .end_to_end import (
    BoosterExtractionConfig,
    generate_booster_extraction_distribution,
    run_end_to_end_pipeline
)
from .convergence_study import (
    InjectionStudyTierConfig,
    ConvergenceScanResult,
    AcceptanceResult,
    EnsembleStudyResult,
    smoke_config,
    pilot_config,
    production_config,
    bootstrap_capture_ci,
    particle_count_convergence_scan,
    turn_count_convergence_scan,
    compute_first_loss_turn_distribution,
    compute_stored_beam_perturbation,
    compute_injection_acceptance,
    run_ensemble_study
)


