"""Resolve the NKM directory rename without rewriting frozen evidence records."""
from pathlib import Path


def manuscript_path(root: Path, value: str | Path) -> Path:
    """Resolve a repository path, accepting the historical NKM directory name.

    Existing paths always win. Only the exact ``docs/paper`` / ``docs/paper_nkm``
    prefix is interchangeable, so old extracted attachments and current checkouts
    can use the same readers. This resolves locations; callers still verify hashes.
    No physical quantities or units are involved.
    """
    root = Path(root).resolve()
    value = Path(value)
    candidate = value if value.is_absolute() else root / value
    if candidate.exists():
        return candidate
    try:
        parts = candidate.relative_to(root).parts
    except ValueError:
        return candidate
    if len(parts) >= 2 and parts[0] == "docs" and parts[1] in ("paper", "paper_nkm"):
        other = "paper_nkm" if parts[1] == "paper" else "paper"
        alternate = root / "docs" / other / Path(*parts[2:])
        if alternate.exists():
            return alternate
    return candidate
