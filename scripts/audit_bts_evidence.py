#!/usr/bin/env python3
"""Verify selected BTS artifact digests and exact claim JSON pointers (SI units)."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def resolve(document, pointer):
    """Resolve an RFC 6901 JSON pointer; absent keys/indices raise."""
    value = document
    if pointer and not pointer.startswith('/'):
        raise ValueError('JSON pointer must start with /')
    for token in pointer.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def audit(root, manifest):
    cache, checked = {}, []
    for artifact in manifest['artifacts']:
        path = root / artifact['path']
        if sha256(path) != artifact['sha256'] or path.stat().st_size != artifact['bytes']:
            raise ValueError(f'Artifact identity mismatch: {artifact["path"]}')
    for claim in manifest['claims']:
        name = claim['artifact']
        if name not in cache:
            cache[name] = json.loads((root / name).read_text())
        actual = resolve(cache[name], claim['pointer'])
        if actual != claim['expected']:
            raise ValueError(f'Claim mismatch: {claim["id"]}')
        checked.append(claim['id'])
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--manifest', type=Path, default=Path('docs/paper_bts/evidence_manifest.json'))
    args = parser.parse_args()
    manifest = args.manifest if args.manifest.is_absolute() else args.root / args.manifest
    print('Verified claims:', ', '.join(audit(args.root, json.loads(manifest.read_text()))))


if __name__ == '__main__':
    main()
