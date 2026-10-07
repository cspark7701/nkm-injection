"""Isolated publication PDF builds; inputs, command logs and return codes persist."""
from pathlib import Path
import json
import shutil
import subprocess


def build_publication_pdf(source_dir, run_dir, figures, tables_dir):
    """Copy manuscript inputs to a fresh build/ and report actual command success.

    No scientific units/conversions or source manuscript contents are changed.
    Failure is reported with logs; a stale source PDF is never an output.
    """
    source, run_dir = Path(source_dir), Path(run_dir)
    build = run_dir / 'build'
    report = {'status': 'failed', 'build_dir': str(build), 'commands': [],
              'pdf_path': None, 'error': None}
    def finish(error=None):
        report['error'] = error
        (run_dir / 'pdf_build.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        return report
    if build.exists() or (run_dir / 'paper.pdf').exists():
        return finish('Build directory and archived PDF must not already exist')
    if not (source / 'paper.tex').is_file():
        return finish('Manuscript paper.tex is missing')
    try:
        shutil.copytree(source, build, ignore=shutil.ignore_patterns(
            'paper.pdf', '*.aux', '*.log', '*.bbl', '*.blg', '*.out', '*.toc', '*.fls', '*.fdb_latexmk'))
        (build / 'figures').mkdir(exist_ok=True)
        for figure in figures:
            shutil.copy2(figure, build / 'figures' / Path(figure).name)
        shutil.copytree(tables_dir, build / 'tables', dirs_exist_ok=True)
        # Manuscript input paths are local to build; generated tables/macros live here.
        for table in Path(tables_dir).glob('*.tex'):
            shutil.copy2(table, build / table.name)
        import hashlib
        report['input_sha256'] = {str(path.relative_to(build)): hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in sorted(build.rglob('*')) if path.is_file()}
        commands = [['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'paper.tex'],
                    ['bibtex', 'paper'],
                    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'paper.tex'],
                    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'paper.tex']]
        for index, command in enumerate(commands, 1):
            log = build / f'{index:02d}_{command[0]}.stdout.log'
            record = {'command': command, 'returncode': None, 'log_path': str(log)}
            report['commands'].append(record)
            with log.open('w', encoding='utf-8') as handle:
                try:
                    completed = subprocess.run(command, cwd=build, stdout=handle,
                                               stderr=subprocess.STDOUT, check=False)
                    record['returncode'] = completed.returncode
                except OSError as error:
                    handle.write(str(error) + '\n')
                    return finish(f'{command[0]} could not run: {error}')
            if completed.returncode != 0:
                return finish(f'{command[0]} exited with code {completed.returncode}')
        pdf = build / 'paper.pdf'
        if not pdf.is_file() or pdf.stat().st_size == 0:
            return finish('Successful commands did not produce a nonempty new paper.pdf')
        shutil.copy2(pdf, run_dir / 'paper.pdf')
        report.update(status='completed', pdf_path=str(run_dir / 'paper.pdf'))
        return finish()
    except OSError as error:
        return finish(f'PDF build input/output failed: {error}')
