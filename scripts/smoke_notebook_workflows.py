#!/usr/bin/env python3
"""Execute maintained notebooks in separate clean kernels with reduced study counts."""
import argparse
import json
import os
from pathlib import Path
import sys

from nkm_injection.notebook_workflows import notebook_repository_root


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=None)
    parser.add_argument('--output-dir', type=Path, required=True, help='Fresh directory for all smoke artifacts')
    args = parser.parse_args(argv)
    root = notebook_repository_root(args.repo_root)
    output = args.output_dir.resolve()
    if output == root or root.is_relative_to(output) or (output.is_relative_to(root) and not output.is_relative_to(root/'results')):
        raise ValueError('Smoke outputs must be outside sources or inside results/')
    output.mkdir(parents=True, exist_ok=False)
    import nbformat
    from nbclient import NotebookClient
    from jupyter_client import KernelManager
    reports = []
    for name in ('01_bts_main_simulation', '02_multiturn_injection_validation',
                 '03_bts_moga_pareto', '04_full_production_simulation'):
        case = output/name
        case.mkdir()
        environment = dict(os.environ, NKM_NOTEBOOK_REPO_ROOT=str(root),
            NKM_NOTEBOOK_RUN_DIR=str(case/'study'), NKM_NOTEBOOK_SMOKE='1',
            MPLBACKEND='Agg', MPLCONFIGDIR=str(case/'matplotlib'), IPYTHONDIR=str(case/'ipython'),
            OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
        notebook = nbformat.read(root/'notebooks'/f'{name}.ipynb', as_version=4)
        # Discard saved outputs before execution; every notebook gets its own interpreter.
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        manager = KernelManager(kernel_name='python3', connection_file=str(case/'kernel.json'),
                                transport='ipc', ip=str(case/'kernel-ipc'))
        manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
        report = {'notebook': name, 'status': 'failed', 'study_dir': str(case/'study'),
                  'python_executable': sys.executable}
        try:
            NotebookClient(notebook, km=manager, timeout=120,
                resources={'metadata': {'path': str(root/'notebooks')}}).execute(env=environment)
            report['status'] = 'completed'
        except Exception as error:
            report['error'] = str(error)
            raise
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
            nbformat.write(notebook, case/'executed.ipynb')
            reports.append(report)
            (output/'smoke_report.json').write_text(json.dumps(reports, indent=2)+'\n')
        print(f'{name}: completed (notebook 04 remains a read-only production preview)', flush=True)


if __name__ == '__main__':
    main()
