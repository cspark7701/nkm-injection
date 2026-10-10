#!/usr/bin/env python3
"""C11 — Frozen evidence bundle for review (reviewer tasks R1-10, R2-19).

Creates a self-contained directory (and a .tar.gz) that lets a referee inspect every artifact behind the manuscript
and rebuild its figures and numbers without the author's ignored ``results/`` and ``backups_*`` directories:

* ``evidence/``       every artifact selected by the campaign manifest, at its manifest-relative path, plus the
                      scientific input files (copied byte-for-byte; the originals are untouched);
* ``code.tar.gz``     ``git archive`` of the committed source (src, scripts, config, tests, docs/jinst-paper, packaging);
* ``campaign_manifest.json``, ``SHA256SUMS``, ``environment.json`` and ``REBUILD.md``.

With ``--verify`` the bundle is rebuilt in a temporary directory with the committed builder and the regenerated
``journal_macros.tex`` is compared with the installed manuscript macros. No upload, release or DOI is created.
"""
import argparse
import hashlib
import importlib.metadata as md
import json
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INPUTS = ("By.txt", "kickmap_file.txt", "K4GSR_HBIv4-1.mat")
CODE_PATHS = ("src", "scripts", "config", "tests", "docs/jinst-paper", "pyproject.toml", "README.md", "environment.yml",
              "requirements-lock.txt")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--manifest", type=Path, default=REPO / "docs/jinst-paper/campaign_manifest.json")
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--verify", action="store_true")
    a = p.parse_args(argv)
    out = a.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    (out / "evidence").mkdir(parents=True)
    m = json.loads(a.manifest.read_text())
    copied = {}
    for key, rel in m["artifacts"].items():
        src = Path(rel) if Path(rel).is_absolute() else REPO / rel
        if Path(rel).is_absolute():
            raise SystemExit(f"manifest path for {key} is absolute; bundle requires repository-relative paths")
        digest = sha256(src)
        if m.get("sha256", {}).get(key) not in (None, digest):
            raise SystemExit(f"hash mismatch for {key}")
        dst = out / "evidence" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied[rel] = digest
    for rel in INPUTS:
        shutil.copy2(REPO / rel, out / "evidence" / rel)
        copied[rel] = sha256(REPO / rel)
    shutil.copy2(a.manifest, out / "campaign_manifest.json")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *CODE_PATHS], cwd=REPO, capture_output=True, text=True).stdout
    subprocess.run(["git", "archive", "--format=tar.gz", "-o", str(out / "code.tar.gz"), "HEAD", *CODE_PATHS], cwd=REPO, check=True)
    pkgs = {}
    for n in ("accelerator-toolbox", "numpy", "scipy", "matplotlib"):
        try:
            pkgs[n] = md.version(n)
        except md.PackageNotFoundError:
            pkgs[n] = None
    (out / "environment.json").write_text(json.dumps({"git_commit": commit, "uncommitted_code_changes": bool(dirty),
                                                      "python": platform.python_version(), "platform": platform.platform(),
                                                      "packages": pkgs}, indent=2) + "\n")
    (out / "REBUILD.md").write_text(f"""# Rebuilding the manuscript evidence

Code: `code.tar.gz` = `git archive` of commit `{commit}`. Evidence: `evidence/` (manifest artifacts at their
repository-relative paths and the scientific inputs {", ".join(INPUTS)}). Hashes: `SHA256SUMS`.

```bash
mkdir code && tar -xzf code.tar.gz -C code
python -m pip install -e "code[dev]"
sha256sum -c SHA256SUMS
OMP_NUM_THREADS=1 MPLBACKEND=Agg python code/scripts/build_journal_figures.py \\
    --manifest campaign_manifest.json --repo-root evidence --output-dir rebuilt
diff rebuilt/tables/journal_macros.tex code/docs/jinst-paper/generated/journal_macros.tex
```

The builder verifies the SHA-256 digest of every artifact it reads. Raw simulation drivers and their command lines are
recorded inside each artifact (`cli` fields) and in `code/docs/exec-plans/completed/`.
""")
    lines = []
    for f in sorted(out.rglob("*")):
        if f.is_file() and f.name != "SHA256SUMS":
            lines.append(f"{sha256(f)}  {f.relative_to(out).as_posix()}")
    (out / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    with tarfile.open(out.with_suffix(".tar.gz"), "w:gz") as tar:
        tar.add(out, arcname=out.name)
    result = {"artifacts": len(m["artifacts"]), "files": len(lines), "commit": commit, "uncommitted": bool(dirty),
              "archive": str(out.with_suffix(".tar.gz"))}
    if a.verify:
        with tempfile.TemporaryDirectory() as tmp:
            code = Path(tmp) / "code"; code.mkdir()
            subprocess.run(["tar", "-xzf", str(out / "code.tar.gz"), "-C", str(code)], check=True)
            env = {"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MPLBACKEND": "Agg", "PATH": "/usr/bin:/bin",
                   "PYTHONPATH": str(code / "src")}
            r = subprocess.run([sys.executable, "-B", str(code / "scripts/build_journal_figures.py"), "--manifest",
                                str(out / "campaign_manifest.json"), "--repo-root", str(out / "evidence"), "--output-dir",
                                str(Path(tmp) / "rebuilt")], cwd=tmp, env=env, capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit("rebuild failed:\n" + r.stderr[-3000:])
            new = (Path(tmp) / "rebuilt/tables/journal_macros.tex").read_text()
            ref = (code / "docs/jinst-paper/generated/journal_macros.tex").read_text()
            result["rebuild_macros_identical"] = new == ref
    (out / "bundle_summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
