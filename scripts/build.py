#!/usr/bin/env python3
"""Build a deterministic Factorio mod ZIP using only the Python standard library."""

import argparse
import json
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
MOD_FILES = ("LICENSE", "README.md", "changelog.txt", "data-final-fixes.lua", "info.json")


def build(output_dir):
    info = json.loads((ROOT / "info.json").read_text(encoding="utf-8"))
    folder = f"{info['name']}_{info['version']}"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{folder}.zip"
    with ZipFile(destination, "w", compression=ZIP_STORED) as archive:
        for filename in MOD_FILES:
            entry = ZipInfo(f"{folder}/{filename}", date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            # Stored entries avoid differences between zlib versions. The mod is tiny.
            entry.compress_type = ZIP_STORED
            archive.writestr(entry, (ROOT / filename).read_bytes())
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    print(build(args.output_dir))
