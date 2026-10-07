"""Installed production CLI; source data and scripts come from --repo-root.

This adapter preserves the production runner's SI interfaces and seed policy.
"""
import argparse
from pathlib import Path
import sys

from .production import ProductionRunConfig, run_production


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Run or preview the NKM production pipeline')
    parser.add_argument('--repo-root', type=Path, default=None,
                        help='Source checkout (default: current directory)')
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-w', '--workers', type=int, default=None,
                        help='Injection/tolerance worker count (default: 90%% of CPU cores)')
    parser.add_argument('-o', '--output-dir', type=Path, default=None,
                        help='Exact new production run directory')
    parser.add_argument('--tier', choices=['smoke', 'pilot', 'production'], default='production')
    parser.add_argument('--samples', type=int, default=100, help='Tolerance sample count')
    parser.add_argument('--seed', type=int, default=42, help='Slicing, optimizer and tolerance seed')
    parser.add_argument('--compile-pdf', action='store_true', help='Compile in a run-local build directory')
    parser.add_argument('-q', '--quiet', dest='verbose', action='store_false', default=True)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    colors = parser.add_mutually_exclusive_group()
    colors.add_argument('--color', dest='color', action='store_const', const='always')
    colors.add_argument('--no-color', dest='color', action='store_const', const='never')
    parser.set_defaults(color='auto')
    return parser.parse_args(argv)


def main(argv=None, *, repo_root=None):
    args = parse_args(argv)
    config = ProductionRunConfig(repo_root=args.repo_root or repo_root or Path.cwd(), output_dir=args.output_dir,
        workers=args.workers, seed=args.seed, tier=args.tier, tolerance_samples=args.samples,
        compile_pdf=args.compile_pdf, verbose=args.verbose, color=args.color)
    try:
        report = run_production(config, dry_run=args.dry_run)
    except (ValueError, FileNotFoundError, SyntaxError, RuntimeError) as exc:
        print(f'[ERROR] {exc}', file=sys.stderr)
        return 1
    print(f'Production {report["status"]}: {report["output_dir"]}')
    return 0


