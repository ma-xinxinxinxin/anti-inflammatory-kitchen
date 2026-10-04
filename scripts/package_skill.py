#!/usr/bin/env python3
"""Build a clean, deterministic skill archive without personal state or caches."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def package(destination=None):
    destination = Path(destination or ROOT / 'dist/kitchen.zip')
    destination.parent.mkdir(parents=True, exist_ok=True)
    paths = [ROOT / 'kitchen/SKILL.md']
    for folder in ('references', 'scripts', 'agents'):
        paths.extend(p for p in (ROOT / 'kitchen' / folder).rglob('*')
                     if p.is_file() and p.suffix in ('.md', '.py', '.yaml')
                     and '__pycache__' not in p.parts)
    with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(paths):
            entry = ZipInfo(path.relative_to(ROOT).as_posix(), (2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, path.read_bytes())
    return destination


if __name__ == '__main__':
    print(package())
