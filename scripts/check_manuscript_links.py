#!/usr/bin/env python3
"""Check local NKM manuscript links across repository Markdown and HTML documents."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    root = Path(root).resolve()
    documents = [root/'README.md'] + sorted((root/'docs').rglob('*.md')) + sorted((root/'docs').rglob('*.html'))
    checked, broken, stale = [], [], []
    for path in documents:
        text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        targets = re.findall(r'(?<!!)\[[^\]]*\]\(([^\n]+?)\)', text)
        targets += re.findall(r'(?:href|src)=["\x27]([^"\x27]+)["\x27]', text)
        for value in targets:
            target = value.strip().split(' "', 1)[0].strip('<>')
            parsed = urlparse(target)
            if parsed.scheme not in ('', 'file') or target.startswith('#'):
                continue
            local = unquote(parsed.path)
            actual = Path(local) if local.startswith('/') else path.parent/local
            actual = actual.resolve()
            try:
                relative = actual.relative_to(root).as_posix()
            except ValueError:
                continue
            if not relative.startswith(('docs/paper_nkm/', 'docs/paper/')) and relative not in ('docs/paper_nkm', 'docs/paper'):
                continue
            record = {'document': path.relative_to(root).as_posix(), 'target': target}
            checked.append(record)
            if relative.startswith('docs/paper/') or relative == 'docs/paper':
                stale.append(record)
            if not actual.exists():
                broken.append(record)
    return {'documents_scanned': len(documents), 'nkm_links_checked': len(checked),
            'broken': broken, 'stale': stale}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check(args.repo_root)
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['broken'] or result['stale']))
