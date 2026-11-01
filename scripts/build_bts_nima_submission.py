#!/usr/bin/env python3
"""Build a flat NIM A source archive and PDFs without running simulations."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs/paper_bts"
INPUT = re.compile(r"\\input\{([^}]+)\}")
FIGURE = re.compile(r"(\\includegraphics(?:\[[^]]*\])?)\{([^}]+)\}")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(output, install_pdfs=False, two_column=False):
    """Create a new output directory; retain logs and exact source identities."""
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / "source"
    source.mkdir()
    identities = {}
    copied = {}

    def copy(path):
        path = path.resolve()
        path.relative_to(PAPER.resolve())
        name = path.name
        if name in copied:
            if copied[name] != path:
                raise ValueError(f"Flat source name collision: {name}")
            return name
        copied[name] = path
        identities[str(path.relative_to(ROOT))] = digest(path)
        if path.suffix == ".tex":
            text = path.read_text()

            def include(match):
                target = PAPER / match[1]
                if not target.suffix:
                    target = target.with_suffix(".tex")
                return "\\input{" + copy(target) + "}"

            def figure(match):
                target = PAPER / match[2]
                if not target.suffix:
                    target = target.with_suffix(".pdf")
                return match[1] + "{" + copy(target) + "}"

            text = INPUT.sub(include, text)
            text = FIGURE.sub(figure, text)
            (source / name).write_text(text)
        else:
            shutil.copy2(path, source / name)
        return name

    documents = ("paper", "supplement", "paper_twocolumn") if two_column else ("paper", "supplement")
    for name in (*[stem + ".tex" for stem in documents], "paper.bib", "highlights.txt"):
        copy(PAPER / name)
    # Include the numbered style used by both documents for EM processing.
    bst = Path(subprocess.check_output(
        ["kpsewhich", "elsarticle-num.bst"], text=True).strip())
    shutil.copy2(bst, source / bst.name)
    logs = output / "build"
    logs.mkdir()
    for stem in documents:
        command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                   f"-outdir={logs}", stem + ".tex"]
        result = subprocess.run(command, cwd=source, text=True, capture_output=True)
        (logs / f"{stem}_command.txt").write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f"{stem} build failed; see {logs}")
        log = (logs / f"{stem}.log").read_text()
        problems = [line for line in log.splitlines() if any(word in line for word in
                    ("LaTeX Warning", "Warning:", "Overfull", "Underfull",
                     "Missing character", "undefined references", "undefined citations"))]
        if problems:
            raise ValueError(f"{stem} layout/reference problems: {problems}")
        shutil.copy2(logs / f"{stem}.pdf", output / f"{stem}.pdf")
        shutil.copy2(logs / f"{stem}.bbl", source / f"{stem}.bbl")
    archive = output / "bts_nima_sources.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(source.iterdir()):
            bundle.write(path, arcname=path.name)
    record = {
        "journal": "Nuclear Instruments and Methods in Physics Research Section A",
        "source_sha256": identities,
        "builder_sha256": digest(Path(__file__)),
        "outputs_sha256": {p.name: digest(p) for p in
                           (*[output / (stem + ".pdf") for stem in documents], archive)},
        "flat_source_sha256": {p.name: digest(p) for p in sorted(source.iterdir())},
        "scientific_campaign_rerun": False,
        "submission_performed": False,
    }
    (output / "build_manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    if install_pdfs:
        for stem in documents:
            shutil.copy2(output / f"{stem}.pdf", PAPER / f"{stem}.pdf")
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--install-pdfs", action="store_true")
    parser.add_argument("--two-column", action="store_true",
                        help="Also build and package the shared-source two-column NIM A preview")
    args = parser.parse_args()
    build(args.output_dir, args.install_pdfs, args.two_column)
