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
    "best-gpx-viewer-for-hiking.html",
    "how-to-create-gpx-cycling-routes.html",
    "what-is-a-gpx-file-reader.html",
    "how-to-open-gpx-files-on-android.html",
    "how-to-open-gpx-file-any-device.html",
    "best-ways-view-gpx-online-offline.html",
    "gpx-file-not-opening-fixes.html",
    "gpx-file-format-tracks-routes-waypoints.html",
    "gpx-vs-kml.html",
    "gpx-vs-tcx.html",
    "gpx-vs-fit.html",
    "how-to-view-gpx-elevation-data.html",
    "how-to-calculate-gpx-route-distance.html",
    "how-to-import-gpx-google-maps.html",
    "open-gpx-files-apple-maps.html",
    "download-gpx-from-strava.html",
    "download-gpx-from-komoot.html",
    "import-gpx-garmin-devices.html",
    "how-to-use-gpx-files-hiking.html",
    "how-to-use-gpx-files-cycling.html",
    "view-gpx-without-internet.html",
    "share-gpx-iphone-android.html",
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
