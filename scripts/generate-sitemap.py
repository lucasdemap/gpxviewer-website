#!/usr/bin/env python3
"""Regenerate sitemap.xml with all blog URLs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://gpxviewerapp.com"
LOCALES = ["", "de", "fr", "it", "pt", "es", "nl", "pl", "id"]

BLOG_SLUGS = [
    "what-is-a-gpx-file.html",
    "how-to-open-gpx-files-on-iphone.html",
    "how-to-view-gpx-on-a-map.html",
    "gpx-for-hiking-and-cycling.html",
]

PAGES = [("", "weekly", "1.0"), ("privacy.html", "monthly", "0.5"), ("blog/", "weekly", "0.9")]
PAGES += [(f"blog/{s}", "monthly", "0.75") for s in BLOG_SLUGS]


def loc(locale: str, page: str) -> str:
    prefix = f"/{locale}/" if locale else "/"
    return f"{BASE}{prefix}{page}" if page else f"{BASE}{prefix}"


def priority(locale: str, page: str) -> str:
    if page == "":
        return "1.0" if not locale else "0.95"
    if page == "privacy.html":
        return "0.5"
    if page == "blog/":
        return "0.9" if not locale else "0.85"
    return "0.75"


def main() -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    count = 0
    for locale in LOCALES:
        for page, freq, _ in PAGES:
            lines += ["  <url>", f"    <loc>{loc(locale, page)}</loc>", f"    <changefreq>{freq}</changefreq>",
                      f"    <priority>{priority(locale, page)}</priority>", "  </url>"]
            count += 1
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {count} URLs to sitemap.xml")


if __name__ == "__main__":
    main()
