#!/usr/bin/env python3
"""
Task 08 — Dynamic Paper Figure and Table Reproduction Script

Single-command script to verify input data hashes, execute the data-driven paper pipeline,
generate publication figures/tables, and log environment/git provenance under
results/paper/paper_run_<timestamp>/.
"""
import argparse
import sys
import json
import datetime
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

from nkm_injection.paper import run_paper_pipeline
from nkm_injection.results_schema import (PublicationManifest, validate_publication_manifest,
                                         initialize_publication_manifest)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Manifest-driven Paper Reproduction Pipeline")
    parser.add_argument("-w", "--workers", type=int, default=None,
                        help="Number of parallel CPU worker cores.")
    parser.add_argument("--manifest", type=str, default=None, help="Path to publication manifest JSON file")
    parser.add_argument("--no-pdf", action="store_true", help="Skip LaTeX PDF compilation")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Exact publication output directory")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--validate-only', action='store_true', help='Read-only validation of hashes and selected stage artifacts')
    mode.add_argument('--initialize', action='store_true', help='Explicitly create missing run directories and source hash baseline')
    return parser.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    if args.validate_only or args.initialize:
        path = Path(args.manifest) if args.manifest else repo_root / 'config/publication_manifest.json'
        manifest = PublicationManifest.load(path) if args.manifest or path.is_file() else PublicationManifest()
        report = (initialize_publication_manifest(manifest, repo_root) if args.initialize else
                  validate_publication_manifest(manifest, repo_root))
        print(json.dumps(report, indent=2))
        if args.validate_only and not report['valid']:
            raise SystemExit(1)
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"paper_run_{timestamp}"

    print("=== Fully Manifest-Driven Paper Pipeline Reproduction ===")
    print(f"Run ID: {run_id}")

    try:
        summary = run_paper_pipeline(repo_root=repo_root, run_id=run_id, manifest=args.manifest, compile_pdf=not args.no_pdf, workers=args.workers,
                                     output_dir=args.output_dir, create_if_missing=False)
        if not args.no_pdf and not summary['pdf_compiled']:
            raise RuntimeError(f"Requested PDF build failed: {summary['pdf_build']['error']}")
        print("\n--- Reproduction Pipeline Completed Successfully ---\n")
        print(f"Manifest Verified: {summary['manifest_valid']}")
        print(f"Input Hashes Verified: {summary['input_hashes_verified']}")
        print(f"Tables Generated: {summary['tables_count']}")
        print(f"Figures Generated: {summary['figures_count']}")
        print(f"PDF Compiled: {summary.get('pdf_compiled', False)}")
        if summary.get('pdf_path'):
            print(f"PDF Path: {summary['pdf_path']}")
        print(f"Output Directory: {args.output_dir or repo_root / 'results' / 'paper' / run_id}")
    except Exception as e:
        print(f"\n[ERROR] Paper reproduction pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
