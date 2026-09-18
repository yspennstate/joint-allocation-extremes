#!/usr/bin/env python3
"""Create a deterministic source archive without build debris or third-party PDFs."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def package(output: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    files = [root / name for name in ('README.md', 'Makefile', 'CITATION.cff', '.gitignore')]
    for pattern in ('paper/*.tex', 'code/*.py', 'code/*.json', 'docs/*.md', '.github/workflows/*.yml'):
        files.extend(root.glob(pattern))
    files = sorted(set(files), key=lambda p: p.relative_to(root).as_posix())
    if not (root / 'paper/main.tex').is_file():
        raise FileNotFoundError('paper/main.tex is required')
    manifest = {}
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            if not path.is_file():
                raise FileNotFoundError(path)
            name = path.relative_to(root).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
            manifest[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        info = zipfile.ZipInfo('SOURCE_MANIFEST.json', date_time=(2026, 9, 18, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(f'Wrote {len(files)} source files to {output}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('source-package.zip'))
    args = parser.parse_args()
    package(args.output)


if __name__ == '__main__':
    main()
