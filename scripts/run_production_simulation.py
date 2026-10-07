#!/usr/bin/env python3
"""Checkout adapter for the installed production command; --dry-run is read-only."""
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from nkm_injection.cli import main as _main, parse_args


def main(argv=None):
    return _main(argv, repo_root=Path(__file__).resolve().parent.parent)


if __name__ == '__main__':
    raise SystemExit(main())
