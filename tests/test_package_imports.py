"""Installed imports share identities and do not initialize unrelated subsystems."""
import ast
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_python(code, cwd):
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    return subprocess.run([sys.executable, '-B', '-c', code], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=60)


def test_lightweight_imports_without_physics_or_optional_dependencies(tmp_path):
    result = run_python('''
import importlib.abc
import sys
class BlockHeavyImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'at', 'scipy', 'matplotlib', 'pymoo'}:
            raise AssertionError('Unexpected dependency: ' + fullname)
sys.meta_path.insert(0, BlockHeavyImports())
import nkm_injection as package
assert not any(name.startswith('nkm_injection.') for name in sys.modules)
from nkm_injection import compute_rigidity, SerializableConfigMixin
from nkm_injection.units import compute_rigidity as direct
from nkm_injection.configuration import SerializableConfigMixin as mixin
assert compute_rigidity is direct
assert SerializableConfigMixin is mixin
assert package.compute_rigidity is direct
assert 'BTSMOGAConfig' in dir(package)
assert compute_rigidity(4.0e9) > 0  # eV, rigidity in T m
try:
    package.unknown_export
except AttributeError:
    pass
else:
    raise AssertionError('Unknown exports must fail')
''', tmp_path)
    assert result.returncode == 0, result.stderr


def test_public_exports_preserve_module_and_class_identity():
    import importlib
    import nkm_injection as package
    for name in package.__all__:
        direct = getattr(importlib.import_module('nkm_injection.' + package._EXPORTS[name]), name)
        assert getattr(package, name) is direct
    from scripts import run_publication_tolerances as cli
    assert cli.ErrorBudgetConfig is package.ErrorBudgetConfig
    from nkm_injection import cli as production_cli
    from nkm_injection.production import ProductionRunConfig
    assert production_cli.ProductionRunConfig is ProductionRunConfig
    assert not any(name.startswith('src.nkm_injection') for name in sys.modules)


def test_legacy_import_rejected_before_creating_duplicate_classes():
    result = run_python('''
try:
    import src.nkm_injection
except ImportError as exc:
    assert 'Use nkm_injection' in str(exc)
else:
    raise AssertionError('Legacy package must not create duplicate identities')
''', ROOT)
    assert result.returncode == 0, result.stderr


def test_maintained_sources_use_installed_imports():
    for folder in ('scripts', 'tests', 'src/nkm_injection'):
        for path in (ROOT / folder).glob('*.py'):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    assert not (node.module or '').startswith('src.nkm_injection'), path
                if isinstance(node, ast.Import):
                    assert not any(n.name.startswith('src.nkm_injection') for n in node.names), path
                if isinstance(node, ast.Call):
                    assert not (isinstance(node.func, ast.Attribute) and
                                ast.unparse(node.func.value) == 'sys.path'), path


@pytest.mark.parametrize('number', ['01', '02', '03', '04'])
def test_notebook_package_imports_in_fresh_process(number, tmp_path):
    path, = (ROOT / 'notebooks').glob(number + '_*.ipynb')
    notebook = json.loads(path.read_text())
    imports = []
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell.get('source', []))
        assert 'src.nkm_injection' not in source
        assert 'sys.path' not in source
        try:
            tree = ast.parse(source)
        except SyntaxError:
            # IPython cells with shell/magic lines still contribute Python imports.
            source = '\n'.join(line for line in source.splitlines()
                               if not line.lstrip().startswith(('!', '%')))
            tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and (node.module or '').startswith('nkm_injection'):
                imports.append(ast.unparse(node))
    assert imports
    result = run_python('\n'.join(imports), tmp_path)
    assert result.returncode == 0, result.stderr
