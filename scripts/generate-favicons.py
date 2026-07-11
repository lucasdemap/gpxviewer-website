#!/usr/bin/env python3
"""Generate favicon assets and update HTML link tags."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "app-icon.png"
IMAGES = ROOT / "images"

FAVICON_BLOCK = """    <link rel="icon" href="/favicon.ico" sizes="48x48" />
    <link rel="icon" href="/images/favicon-48x48.png" type="image/png" sizes="48x48" />
    <link rel="icon" href="/images/favicon-192x192.png" type="image/png" sizes="192x192" />
    <link rel="apple-touch-icon" href="/images/apple-touch-icon.png" sizes="180x180" />"""

ICON_LINE = re.compile(
    r'^\s*<link rel="(?:icon|apple-touch-icon)"[^>]*>\s*$',
    re.MULTILINE,
)


def generate_assets() -> None:
    src = Image.open(SRC).convert("RGBA")
    sizes = {
        IMAGES / "favicon-48x48.png": 48,
        IMAGES / "favicon-192x192.png": 192,
        IMAGES / "apple-touch-icon.png": 180,
    }
    for path, size in sizes.items():
        resized = src.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(path, format="PNG", optimize=True)

    src.resize((48, 48), Image.Resampling.LANCZOS).save(ROOT / "favicon.ico", format="ICO")
    print(f"Generated favicon.ico and {len(sizes)} PNG icons")


def update_html_files() -> int:
    updated = 0
    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if 'rel="icon"' not in text and 'rel="apple-touch-icon"' not in text:
            continue
        cleaned = ICON_LINE.sub("", text)
        if '<link rel="icon" href="/favicon.ico"' in cleaned:
            continue
        anchor = '<meta name="theme-color"'
        if anchor not in cleaned:
            anchor = '<link rel="stylesheet"'
        if anchor not in cleaned:
            continue
        new_text = cleaned.replace(anchor, f"{FAVICON_BLOCK}\n{anchor}", 1)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
    return updated


def main() -> None:
    generate_assets()
    count = update_html_files()
    print(f"Updated {count} HTML files")


if __name__ == "__main__":
    main()
