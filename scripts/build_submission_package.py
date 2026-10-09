#!/usr/bin/env python3
"""Task 012 — build the JINST submission package in an isolated directory.

Copies only the files the manuscript needs (paper.tex, paper.bib, jinstpub.sty, generated macros and referenced
figures), compiles pdflatex -> bibtex -> pdflatex x2, rejects LaTeX errors, undefined references/citations, BibTeX
warnings and overfull boxes, and writes a source archive (with the compiled paper.bbl), the PDF, the supplement
(provenance, manifest, claim table, review), SHA-256 hashes and the software environment to a new output directory.
"""
import argparse
import hashlib
import importlib.metadata as md
import json
import platform
import re
import shutil
import subprocess
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAPER = REPO / "docs" / "jinst-paper"
SUPPLEMENT = ["campaign_manifest.json", "claim_evidence.csv", "scientific_review.md", "bibliography_audit.md",
              "cover_letter.md", "generated/figure_provenance.csv", "generated/consumed_artifacts.json"]
BAD_LOG = re.compile(r"^!|undefined|Overfull|Rerun to get", re.I | re.M)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def referenced_figures(tex: str):
    return sorted(set(re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex)))


def stage_sources(dest: Path):
    tex = (PAPER / "paper.tex").read_text()
    files = ["paper.tex", "paper.bib", "jinstpub.sty", "generated/journal_macros.tex"] + referenced_figures(tex)
    for rel in files:
        src = PAPER / rel
        if not src.is_file():
            raise SystemExit(f"missing manuscript input: {rel}")
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest / rel)
    return files


def compile_paper(src: Path):
    run = lambda *c: subprocess.run(c, cwd=src, capture_output=True, text=True)
    run("pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex")
    bib = run("bibtex", "paper")
    if bib.returncode != 0 or "Warning" in bib.stdout:
        raise SystemExit("bibtex failed:\n" + bib.stdout)
    for _ in range(2):
        r = run("pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex")
    log = (src / "paper.log").read_text(errors="replace")
    bad = BAD_LOG.findall(log)
    if r.returncode != 0 or bad:
        raise SystemExit(f"LaTeX build not clean: {sorted(set(bad))}")
    pages = re.search(r"Output written on paper.pdf \((\d+) pages", log)
    return int(pages.group(1)) if pages else None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--install-pdf", action="store_true", help="copy the compiled PDF to docs/jinst-paper/paper.pdf")
    a = p.parse_args(argv)
    out = a.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    src = out / "source"
    src.mkdir(parents=True)
    files = stage_sources(src)
    pages = compile_paper(src)
    files.append("paper.bbl")
    archive = out / "nkm_jinst_submission_source.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for rel in files:
            tar.add(src / rel, arcname=f"nkm_jinst_submission/{rel}")
    shutil.copy2(src / "paper.pdf", out / "paper.pdf")
    sup = out / "supplement"
    for rel in SUPPLEMENT:
        (sup / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PAPER / rel, sup / rel)
    git = lambda *c: subprocess.run(["git", *c], cwd=REPO, capture_output=True, text=True).stdout.strip()
    pkgs = {}
    for name in ("accelerator-toolbox", "numpy", "scipy", "matplotlib"):
        try:
            pkgs[name] = md.version(name)
        except md.PackageNotFoundError:
            pkgs[name] = None
    record = {
        "git_commit": git("rev-parse", "HEAD"), "git_dirty": bool(git("status", "--porcelain", "--", "docs/jinst-paper", "scripts", "src")),
        "pages": pages, "sources": {r: sha256(src / r) for r in files},
        "outputs": {f.name: sha256(f) for f in (archive, out / "paper.pdf")},
        "supplement": {r: sha256(sup / r) for r in SUPPLEMENT},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "packages": pkgs,
                        "tex": subprocess.run(["pdflatex", "--version"], capture_output=True, text=True).stdout.splitlines()[0]},
        "commands": ["python scripts/build_journal_figures.py --manifest docs/jinst-paper/campaign_manifest.json "
                     "--output-dir <new> --install-dir docs/jinst-paper/generated",
                     f"python scripts/build_submission_package.py --output-dir <new>{' --install-pdf' if a.install_pdf else ''}"],
    }
    (out / "package_manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    if a.install_pdf:
        shutil.copy2(src / "paper.pdf", PAPER / "paper.pdf")
    print(json.dumps({"pages": pages, "files": len(files), "archive": str(archive), "pdf_sha256": record["outputs"]["paper.pdf"]}, indent=1))


if __name__ == "__main__":
    main()
