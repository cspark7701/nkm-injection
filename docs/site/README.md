# NKM GitHub Pages Static Site Bundle (`docs/site/`)

This directory contains the self-contained static website bundle for the **Nonlinear Kicker Magnet (NKM) & BTS Simulation Framework** designed for deployment to GitHub Pages (`https://nkm-injection.github.io` under the `nkm-injection` GitHub organization).

---

## Directory Contents

| File | Description |
| :--- | :--- |
| [`index.html`](index.html) | Sphinx/Read-the-Docs styled documentation and interactive overview. |
| [`style.css`](style.css) | Custom CSS theme, layout styling, MathJax rendering, and typography. |
| [`nkm_consolidated_report.pdf`](nkm_consolidated_report.pdf) | Consolidated technical simulation and physics report PDF. |
| [`paper_results.pdf`](paper_results.pdf) | Production simulation result summary and metrics PDF. |
| [`.nojekyll`](.nojekyll) | Bypasses Jekyll processing on GitHub Pages to serve static files as-is. |

---

## Deployment & Syncing to Standalone `nkm-injection.github.io` Repository

When creating the standalone `nkm-injection.github.io` repository on GitHub:

### Option A: Using the Automated Sync Script
```bash
# From the root of the 'nkm' repository:
./scripts/sync_site.sh ../nkm-injection.github.io
```

If no target directory is passed, the script automatically defaults to `../nkm-injection.github.io`.

### Option B: Manual Sync via `rsync`
```bash
rsync -av --delete docs/site/ /path/to/nkm-injection.github.io/
```

### Option C: Direct Git Worktree / Branch
If serving GitHub Pages from the `gh-pages` branch within this repository:
```bash
git subtree push --prefix docs/site origin gh-pages
```
