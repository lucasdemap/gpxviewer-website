#!/usr/bin/env python3
"""Regenerate sitemap.xml with all locale URLs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://gpxviewerapp.com"

LOCALES = ["", "de", "fr", "it", "pt", "es", "nl", "pl", "id"]
PAGES = [
    ("", "weekly", "1.0" if True else "0.95"),
    ("privacy.html", "monthly", "0.5"),
    ("blog/", "weekly", "0.9"),
    ("blog/what-is-a-gpx-file.html", "monthly", "0.8"),
    ("blog/how-to-open-gpx-files-on-iphone.html", "monthly", "0.8"),
    ("blog/how-to-view-gpx-on-a-map.html", "monthly", "0.8"),
    ("blog/best-gpx-viewer-for-hiking.html", "monthly", "0.8"),
    ("blog/how-to-create-gpx-cycling-routes.html", "monthly", "0.8"),
]

PRIORITY = {
    "": {"": "1.0", "de": "0.95", "fr": "0.95", "it": "0.95", "pt": "0.95", "es": "0.95", "nl": "0.95", "pl": "0.95", "id": "0.95"},
    "privacy.html": "0.5",
    "blog/": {"": "0.9", "de": "0.85", "fr": "0.85", "it": "0.85", "pt": "0.85", "es": "0.85", "nl": "0.85", "pl": "0.85", "id": "0.85"},
    "blog/what-is-a-gpx-file.html": "0.75",
    "blog/how-to-open-gpx-files-on-iphone.html": "0.75",
    "blog/how-to-view-gpx-on-a-map.html": "0.75",
    "blog/best-gpx-viewer-for-hiking.html": "0.75",
    "blog/how-to-create-gpx-cycling-routes.html": "0.75",
}


def loc(locale: str, page: str) -> str:
    if locale:
        prefix = f"/{locale}/"
    else:
        prefix = "/"
    if page == "":
        return f"{BASE}{prefix}"
    return f"{BASE}{prefix}{page}"


def priority(locale: str, page: str) -> str:
    p = PRIORITY.get(page, "0.75")
    if isinstance(p, dict):
        return p.get(locale, "0.75")
    return p


def main() -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for locale in LOCALES:
        for page, freq, _ in PAGES:
            lines.extend(
                [
                    "  <url>",
                    f"    <loc>{loc(locale, page)}</loc>",
                    f"    <changefreq>{freq}</changefreq>",
                    f"    <priority>{priority(locale, page)}</priority>",
                    "  </url>",
                ]
            )
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(LOCALES) * len(PAGES)} URLs to sitemap.xml")


if __name__ == "__main__":
    main()
