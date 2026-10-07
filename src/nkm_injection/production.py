"""Production configuration and stage orchestration shared by shell and notebook.

This module routes artifacts; it does not alter physics algorithms or units.
Stage quantities retain SI interfaces (m, rad, eV, T, T m), with explicit legacy
conversions inside the existing producers. Only injection/tolerance use workers.
"""
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Callable, Optional, Tuple, Dict, Any

from .publication_inputs import load_publication_inputs
from .results_schema import SerializableConfigMixin, PublicationManifest, validate_publication_manifest

REQUIRED_INPUTS = ('By.txt', 'kickmap_file.txt', 'K4GSR_HBIv4-1.mat',
                   'nkm_field.xlsx', 'nkm_field_expanded.xlsx',
                   'NKM_radia.ipynb', 'NKM_radia_y=0.ipynb', 'nlk.py', 'storage_ring.ipynb')


def _positive_integer(value, name, minimum=1):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')


@dataclass
class ProductionRunConfig(SerializableConfigMixin):
    """Job settings; seed controls slicing, optimization and tolerance sampling.

    Injection and MOGA retain their existing fixed tier/multi-seed presets,
    which are saved by their producers. workers=None selects 90% of CPU cores.
    output_dir is an exact new run directory; existing directories are rejected.
    """
    repo_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    output_dir: Optional[Path] = None
    workers: Optional[int] = None
    seed: int = 42
    tier: str = 'production'
    tolerance_samples: int = 100
    compile_pdf: bool = False
    verbose: bool = True
    color: str = 'auto'
    python_executable: str = field(default_factory=lambda: sys.executable)

    def __post_init__(self):
        self.repo_root = Path(self.repo_root).resolve()
        self.output_dir = (Path(self.output_dir).resolve() if self.output_dir is not None else
                           self.repo_root / 'results' / f'production_run_{datetime.now():%Y%m%d_%H%M%S_%f}')

    @property
    def resolved_workers(self) -> int:
        return self.workers if self.workers is not None else max(1, int((os.cpu_count() or 1) * 0.9))

    def validate(self):
        if self.workers is not None:
            _positive_integer(self.workers, 'workers')
        _positive_integer(self.seed, 'seed', 0)
        _positive_integer(self.tolerance_samples, 'tolerance_samples')
        if self.tier not in ('smoke', 'pilot', 'production'):
            raise ValueError('tier must be smoke, pilot or production')
        if self.color not in ('auto', 'always', 'never'):
            raise ValueError('color must be auto, always or never')
        if not isinstance(self.compile_pdf, bool) or not isinstance(self.verbose, bool):
            raise ValueError('compile_pdf and verbose must be boolean')
        if not Path(self.python_executable).is_file() or not os.access(self.python_executable, os.X_OK):
            raise ValueError(f'Python executable unavailable: {self.python_executable}')
        if not self.repo_root.is_dir():
            raise ValueError(f'repository root unavailable: {self.repo_root}')
        if self.output_dir.exists():
            raise ValueError(f'output directory already exists; choose a new run: {self.output_dir}')
        for name in REQUIRED_INPUTS:
            if not (self.repo_root / name).is_file():
                raise FileNotFoundError(f'required scientific input missing: {name}')


@dataclass(frozen=True)
class ProductionStage:
    """Explicit argv, exact output directory and expected artifacts for one stage."""
    name: str
    label: str
    command: Tuple[str, ...]
    output_dir: Path
    expected_artifacts: Tuple[str, ...]
    workers: int = 1

    @property
    def execution_mode(self):
        return 'parallel' if self.name in ('multiturn', 'tolerances') and self.workers > 1 else 'sequential'


def production_stages(config: ProductionRunConfig) -> Tuple[ProductionStage, ...]:
    """Build the ordered stage commands; no execution, directories or other writes."""
    root, out = config.repo_root, config.output_dir
    manifest_path = out / 'publication_manifest.json'
    stages = []
    specs = (
        ('baseline', 'Protected input hash inventory', 'inventory_protected_hashes.py',
         ('protected_files_manifest.json',), ()),
        ('fieldmap', 'NKM field validation', 'validate_nkm_fieldmap.py',
         ('fieldmap_validation_metrics.json',), ()),
        ('convergence', 'Symplectic slicing convergence', 'run_tracking_convergence.py',
         ('tracking_convergence_summary.json',), ('--seed', str(config.seed))),
        ('multiturn', 'Multi-turn injection', 'run_multiturn_injection.py',
         ('config.json', 'injection_metrics_summary.json'),
         ('--tier', config.tier, '--workers', str(config.resolved_workers))),
        ('optimization', 'Deterministic BTS matching', 'optimize_bts_publication.py',
         ('config.json', 'bts_optimization_summary.json'), ('--seed', str(config.seed))),
        ('tolerances', 'Monte Carlo tolerance study', 'run_publication_tolerances.py',
         ('publication_tolerances_summary.json',),
         ('--samples', str(config.tolerance_samples), '--seed', str(config.seed),
          '--workers', str(config.resolved_workers), '--optimization-summary',
          str(out / 'optimization' / 'bts_optimization_summary.json'))),
        ('moga', 'Multi-seed MOGA study', 'run_publication_moga.py',
         ('multi_seed_moga_summary.json',), ()),
        ('summary', 'Selected-run publication generation', 'reproduce_paper.py',
         ('metrics.json', 'upstream_artifacts.json', 'figures/figure_data.json'),
         ('--manifest', str(manifest_path)) + (() if config.compile_pdf else ('--no-pdf',))),
    )
    for name, label, script, artifacts, args in specs:
        command = (config.python_executable, '-B', str(root / 'scripts' / script),
                   '--output-dir', str(out / name)) + args
        stages.append(ProductionStage(name, label, command, out / name, artifacts,
                       config.resolved_workers if name in ('multiturn', 'tolerances') else 1))
    return tuple(stages)


def _manifest(config: ProductionRunConfig) -> PublicationManifest:
    out = config.output_dir
    return PublicationManifest(field_validation_run=str(out / 'fieldmap'),
        tracking_convergence_run=str(out / 'convergence'),
        bts_optimization_run=str(out / 'optimization'), injection_run=str(out / 'multiturn'),
        tolerance_run=str(out / 'tolerances'), moga_run=str(out / 'moga'),
        input_hash_manifest=str(out / 'baseline' / 'protected_files_manifest.json'))


def _status(message: str, config: ProductionRunConfig):
    colored = (config.color == 'always' or
               config.color == 'auto' and sys.stdout.isatty() and not os.environ.get('NO_COLOR'))
    print('\033[36m' + message + '\033[0m' if colored else message, flush=True)


def _execute(stage: ProductionStage, config: ProductionRunConfig):
    """Execute with argv (no shell) and preserve stdout/stderr in a per-stage log."""
    log_path = config.output_dir / 'logs' / f'{stage.name}.log'
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['MPLBACKEND'] = 'Agg'
    with log_path.open('w', encoding='utf-8') as log:
        log.write(shlex.join(stage.command) + '\n')
        log.flush()
        if config.verbose:
            with subprocess.Popen(stage.command, cwd=config.repo_root, env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
                for line in process.stdout:
                    print(line, end='', flush=True)
                    log.write(line)
                code = process.wait()
        else:
            code = subprocess.run(stage.command, cwd=config.repo_root, env=env,
                                  stdout=log, stderr=subprocess.STDOUT).returncode
    if code:
        raise RuntimeError(f'{stage.name} exited with status {code}; log: {log_path}')


def run_production(config: Optional[ProductionRunConfig] = None, *, dry_run: bool = False,
                   executor: Optional[Callable[[ProductionStage], None]] = None) -> Dict[str, Any]:
    """Validate and run all stages, or return a read-only plan.

    executor(stage) is an injectable stage executor for tests; it must raise on
    failure and produce the declared artifacts. A failure stops later stages.
    A publication manifest is written only after all selected inputs validate.
    Dry runs compile script source in memory; no child process, simulation,
    directory, log, hash baseline or bytecode is created by this function.
    """
    config = config or ProductionRunConfig()
    config.validate()
    stages = production_stages(config)
    for stage in stages:
        script = Path(stage.command[2])
        # Syntax validation does not write .pyc files or import stage modules.
        compile(script.read_bytes(), str(script), 'exec')
    report = {'status': 'planned' if dry_run else 'running',
              'output_dir': str(config.output_dir), 'workers': config.resolved_workers,
              'stages': []}
    for i, stage in enumerate(stages, 1):
        report['stages'].append({'name': stage.name, 'command': list(stage.command),
            'output_dir': str(stage.output_dir), 'execution_mode': stage.execution_mode,
            'workers': stage.workers, 'status': 'planned'})
        _status(f'{i}. {stage.label} [{stage.execution_mode}; workers={stage.workers}]', config)
        if dry_run:
            print('   ' + shlex.join(stage.command), flush=True)
    if dry_run:
        return report

    config.output_dir.mkdir(parents=True, exist_ok=False)
    (config.output_dir / 'logs').mkdir()
    saved = config.to_dict()
    saved['resolved_workers'] = config.resolved_workers
    (config.output_dir / 'production_config.json').write_text(json.dumps(saved, indent=2) + '\n')
    status_path = config.output_dir / 'production_status.json'
    execute = executor or (lambda stage: _execute(stage, config))
    current = None
    try:
        for stage, record in zip(stages, report['stages']):
            current = record
            _status(f'\n[RUNNING] {stage.label}', config)
            if stage.name == 'summary':
                manifest = _manifest(config)
                validation = validate_publication_manifest(manifest, config.repo_root, create_if_missing=False)
                if not validation['valid']:
                    raise ValueError(f'production manifest invalid: {validation["errors"]}')
                load_publication_inputs(manifest, config.repo_root)
                manifest.save(config.output_dir / 'publication_manifest.json')
            stage.output_dir.mkdir()
            execute(stage)
            for artifact in stage.expected_artifacts:
                path = stage.output_dir / artifact
                if not path.is_file():
                    raise FileNotFoundError(f'{stage.name} did not produce required artifact: {path}')
            record['status'] = 'completed'
            status_path.write_text(json.dumps(report, indent=2) + '\n')
            _status(f'[COMPLETED] {stage.label}', config)
        report['status'] = 'completed'
    except Exception as exc:
        report['status'] = 'failed'
        if current is not None:
            current['status'] = 'failed'
            report['failed_stage'] = current['name']
        report['error'] = str(exc)
        status_path.write_text(json.dumps(report, indent=2) + '\n')
        raise RuntimeError(f'Production stopped at {report.get("failed_stage")}: {exc}') from exc
    status_path.write_text(json.dumps(report, indent=2) + '\n')
    return report
