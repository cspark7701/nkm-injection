#!/usr/bin/env python3
"""Task 012 — build a PRAB submission package in an isolated directory.

Copies only the files the manuscript needs (paper.tex, paper.bib, generated macros and referenced
figures), compiles pdflatex -> bibtex -> pdflatex x2 (up to x4 while labels settle), rejects LaTeX errors, undefined references/citations, BibTeX
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
PAPER = REPO / "docs" / "paper"
SUPPLEMENT = ["revision_manifest_round2.json", "revision_manifest.json", "claim_evidence.csv",
              "round2_final_checks.md", "round2_reproduction.md", "round2_comparison_audit.md",
              "bibliography_audit.md", "cover_letter.md", "generated/figure_provenance.csv",
              "generated/consumed_artifacts.json", "prab_submission.md", "submission_checklist.md"]
if (PAPER / "reviews/author_response_round2.md").is_file():
    SUPPLEMENT.append("reviews/author_response_round2.md")

BAD_LOG = re.compile(r"^!|undefined|Overfull|Rerun to get|A float is stuck|Float too large", re.I | re.M)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def referenced_figures(tex: str):
    return sorted(set(re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex)))


def stage_sources(dest: Path):
    tex = (PAPER / "paper.tex").read_text()
    files = ["paper.tex", "paper_twocolumn.tex", "paper.bib", "generated/journal_macros.tex"] + referenced_figures(tex)
    for rel in files:
        src = PAPER / rel
        if not src.is_file():
            raise SystemExit(f"missing manuscript input: {rel}")
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest / rel)
    return files


def bibliography_warnings(output: str):
    # apsrev4-2 emits this control-setting notice for REVTeX's author="08".
    # It is not a missing citation/field; retain every other BibTeX warning.
    control_notice = "Warning--jnrlst (dependency: not reversed) set 1"
    return [line for line in output.splitlines()
            if "Warning" in line and line.strip() != control_notice]


def compile_paper(src: Path, tex_name: str = "paper.tex"):
    stem = Path(tex_name).stem
    run = lambda *c: subprocess.run(c, cwd=src, capture_output=True, text=True)
    first = run("pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_name)
    if first.returncode != 0:
        raise SystemExit("initial LaTeX build failed:\n" + first.stdout[-4000:])
    bib = run("bibtex", stem)
    if bib.returncode != 0 or bibliography_warnings(bib.stdout):
        raise SystemExit("bibtex failed:\n" + bib.stdout)
    for _ in range(4):  # at least two passes; repeat while labels are still settling
        r = run("pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_name)
        log = (src / f"{stem}.log").read_text(errors="replace")
        if _ >= 1 and "Rerun to get" not in log:
            break
    bad = BAD_LOG.findall(log)
    if r.returncode != 0 or bad:
        raise SystemExit(f"LaTeX build not clean: {sorted(set(bad))}")
    pages = re.search(rf"Output written on {re.escape(stem)}\.pdf \((\d+) pages", log)
    return int(pages.group(1)) if pages else None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--layout", choices=("one-column", "two-column"), default="one-column",
                   help="one-column PRAB review draft (default) or two-column journal-style preview")
    p.add_argument("--install-pdf", action="store_true", help="install paper.pdf or paper_twocolumn.pdf according to --layout")
    a = p.parse_args(argv)
    out = a.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    src = out / "source"
    src.mkdir(parents=True)
    files = stage_sources(src)
    tex_name = "paper.tex" if a.layout == "one-column" else "paper_twocolumn.tex"
    stem = Path(tex_name).stem
    pdf_name = f"{stem}.pdf"
    pages = compile_paper(src, tex_name)
    files.append(f"{stem}.bbl")
    archive = out / "nkm_article_submission_source.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for rel in files:
            tar.add(src / rel, arcname=f"nkm_article_submission/{rel}")
    shutil.copy2(src / pdf_name, out / pdf_name)
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
        "git_commit": git("rev-parse", "HEAD"), "git_dirty": bool(git("status", "--porcelain", "--", "docs/paper", "scripts", "src")),
        "journal": "PRAB", "layout": a.layout, "entry_point": tex_name,
        "pages": pages, "sources": {r: sha256(src / r) for r in files},
        "outputs": {f.name: sha256(f) for f in (archive, out / pdf_name)},
        "supplement": {r: sha256(sup / r) for r in SUPPLEMENT},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "packages": pkgs,
                        "tex": subprocess.run(["pdflatex", "--version"], capture_output=True, text=True).stdout.splitlines()[0]},
        "commands": ["python scripts/build_revision_figures.py --manifest docs/paper/revision_manifest_round2.json "
                     "--output-dir <new> --install-dir docs/paper/generated",
                     f"python scripts/build_submission_package.py --layout {a.layout} --output-dir <new>{' --install-pdf' if a.install_pdf else ''}"],
    }
    (out / "package_manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    if a.install_pdf:
        shutil.copy2(src / pdf_name, PAPER / pdf_name)
    print(json.dumps({"pages": pages, "files": len(files), "archive": str(archive), "pdf_sha256": record["outputs"][pdf_name]}, indent=1))


if __name__ == "__main__":
    main()
