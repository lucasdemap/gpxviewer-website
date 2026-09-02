#!/usr/bin/env python3
"""Consolidate 25 blog posts into 4 guides, generate redirects, update sitemap."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"
LOCALES = ["de", "fr", "it", "pt", "es", "nl", "pl", "id"]

KEEP_SLUGS = [
    "what-is-a-gpx-file",
    "how-to-open-gpx-files-on-iphone",
    "how-to-view-gpx-on-a-map",
    "gpx-for-hiking-and-cycling",
]

REDIRECTS = {
    "what-is-a-gpx-file-reader": "what-is-a-gpx-file",
    "gpx-file-format-tracks-routes-waypoints": "what-is-a-gpx-file",
    "gpx-vs-kml": "what-is-a-gpx-file",
    "gpx-vs-tcx": "what-is-a-gpx-file",
    "gpx-vs-fit": "what-is-a-gpx-file",
    "how-to-open-gpx-files-on-android": "how-to-open-gpx-files-on-iphone",
    "how-to-open-gpx-file-any-device": "how-to-open-gpx-files-on-iphone",
    "gpx-file-not-opening-fixes": "how-to-open-gpx-files-on-iphone",
    "open-gpx-files-apple-maps": "how-to-open-gpx-files-on-iphone",
    "best-ways-view-gpx-online-offline": "how-to-view-gpx-on-a-map",
    "how-to-view-gpx-elevation-data": "how-to-view-gpx-on-a-map",
    "how-to-calculate-gpx-route-distance": "how-to-view-gpx-on-a-map",
    "how-to-import-gpx-google-maps": "how-to-view-gpx-on-a-map",
    "view-gpx-without-internet": "how-to-view-gpx-on-a-map",
    "best-gpx-viewer-for-hiking": "gpx-for-hiking-and-cycling",
    "how-to-create-gpx-cycling-routes": "gpx-for-hiking-and-cycling",
    "how-to-use-gpx-files-hiking": "gpx-for-hiking-and-cycling",
    "how-to-use-gpx-files-cycling": "gpx-for-hiking-and-cycling",
    "download-gpx-from-strava": "gpx-for-hiking-and-cycling",
    "download-gpx-from-komoot": "gpx-for-hiking-and-cycling",
    "import-gpx-garmin-devices": "gpx-for-hiking-and-cycling",
    "share-gpx-iphone-android": "gpx-for-hiking-and-cycling",
}

EN_UI = {
    "nav_features": "Features",
    "nav_blog": "Blog",
    "nav_pro": "Pro",
    "footer_home": "Home",
    "footer_privacy": "Privacy",
    "footer_contact": "Contact",
    "back_link": "← Back to all guides",
    "read_more": "Read guide →",
    "app_store_alt": "Download on the App Store",
    "play_store_alt": "Get it on Google Play",
    "cta_title": "Try GPX Viewer free",
}

ARTICLES_EN = [
    {
        "slug": "what-is-a-gpx-file",
        "date": "2026-09-02",
        "tag_en": "Beginner",
        "en": {
            **EN_UI,
            "title": "What Is a GPX File? Complete GPS Exchange Format Guide",
            "h1": "What Is a GPX File?",
            "subtitle": "Understand the GPS Exchange Format and why .gpx files power outdoor navigation.",
            "description": "Learn what a GPX file is, how tracks, routes and waypoints work, and how GPX compares to KML, TCX and FIT. For hikers and cyclists on iPhone and Android.",
            "keywords": "what is a gpx file, gpx file format, gps exchange format, gpx vs kml",
            "tag": "Beginner",
            "card_title": "What Is a GPX File?",
            "card_desc": "Tracks, routes, waypoints, and how GPX compares to other formats.",
            "date_display": "September 2, 2026",
            "cta_text": "Import GPX files, view routes on a map, and explore elevation profiles on iPhone and Android.",
            "body": """          <p>
            If you have downloaded a hiking trail, received a cycling route from a friend, or exported
            a GPS recording from a watch, you have almost certainly encountered a <strong>GPX file</strong>.
            The extension <code>.gpx</code> stands for <strong>GPS Exchange Format</strong> — an open
            standard that lets devices and apps share location data in a way any compatible tool can read.
          </p>

          <h2>What does a GPX file contain?</h2>
          <p>Most GPX files include one or more of these elements:</p>
          <ul>
            <li><strong>Tracks</strong> — a path made of GPS points, often recorded during a hike or ride.</li>
            <li><strong>Routes</strong> — a planned path with key turns for navigation.</li>
            <li><strong>Waypoints</strong> — points of interest such as summits, campsites, or parking.</li>
            <li><strong>Elevation data</strong> — height above sea level at each point.</li>
            <li><strong>Timestamps</strong> — when each point was recorded.</li>
          </ul>
          <p>
            A dedicated app like <a href="../">GPX Viewer</a> renders that data as an interactive map.
            See <a href="how-to-view-gpx-on-a-map.html">how to view GPX on a map</a> for the full workflow.
          </p>

          <h2>GPX tracks vs. routes</h2>
          <p>
            A <strong>track</strong> is something you have already traveled — your device logged every GPS fix.
            A <strong>route</strong> is planned in advance, connecting waypoints where you intend to go.
            Both work the same way in GPX Viewer: import the file and follow the line on the map.
          </p>

          <h2>GPX vs. KML, TCX, and FIT</h2>
          <p>Outdoor apps use several GPS file formats. Here is when GPX is the right choice:</p>
          <ul>
            <li><strong>GPX</strong> — best for sharing hiking and cycling routes between apps and phones.</li>
            <li><strong>KML</strong> — common in Google Earth; less ideal for turn-by-turn trail navigation.</li>
            <li><strong>TCX</strong> — Garmin training format with heart-rate and cadence data.</li>
            <li><strong>FIT</strong> — binary activity recordings from Garmin watches; not meant for route sharing.</li>
          </ul>
          <p>
            For trail following and route planning on your phone, GPX is the format to use.
            GPX Viewer opens <code>.gpx</code> files directly — no conversion step.
          </p>

          <h2>How to open a GPX file</h2>
          <p>
            Import a GPX file on iPhone or Android using the share sheet from Mail, Files, or Safari.
            Our guide on <a href="how-to-open-gpx-files-on-iphone.html">opening GPX files on iPhone and Android</a>
            covers every import method step by step.
          </p>""",
        },
    },
    {
        "slug": "how-to-open-gpx-files-on-iphone",
        "date": "2026-09-02",
        "tag_en": "iPhone & Android",
        "en": {
            **EN_UI,
            "title": "How to Open GPX Files on iPhone and Android",
            "h1": "How to Open GPX Files on iPhone and Android",
            "subtitle": "Import GPX routes from Mail, Files, or Safari into GPX Viewer.",
            "description": "Step-by-step guide to open GPX files on iPhone and Android. Import from Mail, Files, Safari, Gmail, or Drive. Fix common import problems.",
            "keywords": "open gpx file iphone, open gpx file android, import gpx, gpx not opening",
            "tag": "iPhone & Android",
            "card_title": "How to Open GPX Files on iPhone and Android",
            "card_desc": "Import GPX from Mail, Files, or Safari — plus troubleshooting tips.",
            "date_display": "September 2, 2026",
            "cta_text": "Open GPX files from Mail, Files, or Safari and view your routes on a map in seconds.",
            "body": """          <p>
            iOS and Android do not include a built-in GPX map viewer. You need an app like
            <a href="../">GPX Viewer</a> that understands the <code>.gpx</code> format. Once installed,
            importing a route takes a few taps through the share sheet.
          </p>

          <h2>Open GPX on iPhone</h2>
          <h3>From Mail or Files</h3>
          <ol>
            <li>Find the <code>.gpx</code> attachment or file.</li>
            <li>Tap <strong>Share</strong>.</li>
            <li>Select <strong>GPX Viewer</strong>.</li>
            <li>The route appears on the map immediately.</li>
          </ol>
          <h3>From Safari</h3>
          <p>
            Tap a GPX download link on a trail website, then share the downloaded file to GPX Viewer
            from Safari's download manager or save it to Files first.
          </p>
          <h3>Apple Maps cannot open GPX</h3>
          <p>
            Apple Maps does not import GPX files. Use GPX Viewer instead — it shows the full track,
            elevation profile, and waypoints on standard, satellite, or hybrid maps.
          </p>

          <h2>Open GPX on Android</h2>
          <ol>
            <li>Open the GPX attachment in Gmail or your file manager.</li>
            <li>Tap <strong>Open with</strong> or <strong>Share</strong>.</li>
            <li>Choose <strong>GPX Viewer</strong>.</li>
            <li>Select <strong>Always</strong> if prompted, for faster imports later.</li>
          </ol>

          <h2>Troubleshooting</h2>
          <ul>
            <li><strong>Wrong file type</strong> — confirm the extension is <code>.gpx</code>, not <code>.kml</code> or <code>.tcx</code>.</li>
            <li><strong>App not in Share menu</strong> — open GPX Viewer once, then retry.</li>
            <li><strong>Empty track</strong> — the file may contain metadata but no GPS points; re-export from the source app.</li>
            <li><strong>File looks wrong on the map</strong> — see <a href="how-to-view-gpx-on-a-map.html">how to view GPX on a map</a>.</li>
          </ul>

          <p>
            New to GPX? Read <a href="what-is-a-gpx-file.html">what is a GPX file</a> first.
          </p>""",
        },
    },
    {
        "slug": "how-to-view-gpx-on-a-map",
        "date": "2026-09-02",
        "tag_en": "Maps",
        "en": {
            **EN_UI,
            "title": "How to View GPX Routes on a Map",
            "h1": "How to View GPX Routes on a Map",
            "subtitle": "Turn GPS coordinates into a clear route map with elevation and waypoints.",
            "description": "View GPX routes on interactive maps with elevation profiles, distance stats, and offline-ready navigation. Works on iPhone and Android with GPX Viewer.",
            "keywords": "view gpx on map, gpx map viewer, gpx elevation profile, gpx offline",
            "tag": "Maps",
            "card_title": "How to View GPX Routes on a Map",
            "card_desc": "Map styles, elevation charts, distance, and offline viewing.",
            "date_display": "September 2, 2026",
            "cta_text": "View GPX routes on interactive maps with elevation profiles on iPhone and Android.",
            "body": """          <p>
            A GPX file is a list of coordinates. To <strong>view GPX on a map</strong>, you need a
            viewer like <a href="../">GPX Viewer</a> that draws the track as a line with distance,
            elevation, and labeled waypoints. If you have not imported your file yet, see
            <a href="how-to-open-gpx-files-on-iphone.html">how to open GPX files on iPhone and Android</a> first.
          </p>

          <h2>What a good GPX map viewer shows</h2>
          <ul>
            <li>The full route as a colored track line</li>
            <li>Start and end markers</li>
            <li>Named waypoints you can tap for details</li>
            <li>Total distance and elevation gain</li>
            <li>An elevation profile chart linked to the map</li>
          </ul>

          <h2>Choosing a map style</h2>
          <p>GPX Viewer offers three layers:</p>
          <ul>
            <li><strong>Standard</strong> — roads, paths, and place names. Best for marked trails and road cycling.</li>
            <li><strong>Satellite</strong> — aerial imagery for forest cover, river crossings, and unmarked paths.</li>
            <li><strong>Hybrid</strong> — satellite with road and trail labels overlaid.</li>
          </ul>

          <h2>Elevation and distance</h2>
          <p>
            The elevation chart shows every climb and descent along the route. Scroll the profile to
            inspect steep sections before you start. Distance is calculated automatically from the
            GPS track points — no manual measurement needed.
          </p>

          <h2>View GPX offline</h2>
          <p>
            Load your route while you still have signal. GPX Viewer keeps the track and map tiles
            available so you can follow the route in areas with weak or no cell coverage.
            GPX Viewer Pro adds a live location dot so you can see your position on the track in real time.
          </p>

          <h2>Google Maps and desktop viewers</h2>
          <p>
            Google My Maps can import GPX on a desktop browser for planning, but it is not practical
            for following a trail on your phone. For mobile navigation,
            <a href="../">GPX Viewer</a> is built specifically for the GPX map experience on iPhone and Android.
          </p>""",
        },
    },
    {
        "slug": "gpx-for-hiking-and-cycling",
        "date": "2026-09-02",
        "tag_en": "Outdoors",
        "en": {
            **EN_UI,
            "title": "GPX for Hiking and Cycling — Routes, Trails & Navigation",
            "h1": "GPX for Hiking and Cycling",
            "subtitle": "Follow trails, plan bike routes, and import GPX from Strava, Komoot, and Garmin.",
            "description": "Use GPX files for hiking trails and cycling routes. Follow tracks on your phone, create routes, import from Strava or Komoot, and share between iPhone and Android.",
            "keywords": "gpx hiking, gpx cycling, gpx strava, gpx komoot, follow gpx trail",
            "tag": "Outdoors",
            "card_title": "GPX for Hiking and Cycling",
            "card_desc": "Follow trails, plan rides, import from Strava/Komoot, and share routes.",
            "date_display": "September 2, 2026",
            "cta_text": "Follow hiking and cycling routes with GPX Viewer on iPhone and Android.",
            "body": """          <p>
            GPX files are the standard way hikers and cyclists share routes. Load a track on your phone,
            see the path on a map, and follow it in the field with
            <a href="../">GPX Viewer</a>. This guide covers hiking, cycling, importing from other apps,
            and sharing routes with your group.
          </p>

          <h2>GPX for hiking</h2>
          <p>
            Trail clubs, guidebooks, and fellow hikers share GPX tracks so you can follow an established
            path even when markers are sparse. Import the file, preview distance and elevation at home,
            then enable live location with GPX Viewer Pro to see your position on the track.
          </p>
          <ul>
            <li>Preview climbs and descents before you start</li>
            <li>Check waypoints at junctions and water sources</li>
            <li>Switch to satellite view in dense forest</li>
            <li>Carry a power bank on longer hikes</li>
          </ul>

          <h2>GPX for cycling</h2>
          <p>
            Plan a road loop, gravel ride, or sportive course in GPX Viewer: tap the map to place
            waypoints, review distance and elevation, then save and export the route as a
            <code>.gpx</code> file to share with riding partners.
          </p>
          <ol>
            <li>Open GPX Viewer and tap <strong>Create Route</strong>.</li>
            <li>Place waypoints along your intended path.</li>
            <li>Review stats and adjust corners.</li>
            <li>Save and export as GPX.</li>
          </ol>

          <h2>Import GPX from Strava, Komoot, and Garmin</h2>
          <p>Most outdoor platforms let you export routes as GPX:</p>
          <ul>
            <li><strong>Strava</strong> — open an activity or route, choose Export GPX.</li>
            <li><strong>Komoot</strong> — open a tour, tap Export, select GPX.</li>
            <li><strong>Garmin</strong> — upload GPX to Garmin Connect, then sync to your watch or open in GPX Viewer on your phone.</li>
          </ul>
          <p>
            Share the exported file via email or messaging, then open it in GPX Viewer using the
            <a href="how-to-open-gpx-files-on-iphone.html">import guide</a>.
            GPX works across iPhone and Android, so mixed groups can use the same route file.
          </p>

          <h2>Following a GPX route safely</h2>
          <p>
            Treat the GPX track as a navigation aid alongside your map and trail knowledge.
            Verify the track source — community routes can be outdated if trails have changed.
            Check which end is the trailhead; some files are recorded in reverse.
          </p>
          <p>
            Read <a href="what-is-a-gpx-file.html">what is a GPX file</a> and
            <a href="how-to-view-gpx-on-a-map.html">how to view GPX on a map</a> for the basics.
          </p>""",
        },
    },
]


def redirect_html(locale: str, old_slug: str, target_slug: str) -> str:
    if locale == "en":
        target = f"/blog/{target_slug}.html"
        canonical = f"https://gpxviewerapp.com/blog/{target_slug}.html"
    else:
        target = f"/{locale}/blog/{target_slug}.html"
        canonical = f"https://gpxviewerapp.com/{locale}/blog/{target_slug}.html"
    return f"""<!DOCTYPE html>
<html lang="{locale or 'en'}">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url={target}" />
    <link rel="canonical" href="{canonical}" />
    <meta name="robots" content="noindex, follow" />
    <title>Redirecting…</title>
  </head>
  <body>
    <p>This page has moved. <a href="{target}">Continue to the updated guide</a>.</p>
  </body>
</html>
"""


def blog_index_en() -> dict:
    return {
        **EN_UI,
        "title": "GPX Viewer Blog — GPX Guides for Hiking, Cycling & Navigation",
        "description": "Four guides to understand, open, view, and navigate GPX files on iPhone and Android.",
        "h1": "GPX Viewer Blog",
        "subtitle": "Essential GPX guides for iPhone and Android.",
    }


def write_manifest() -> None:
    old = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blog_index = {"en": blog_index_en()}
    for loc in LOCALES:
        if loc in old.get("blog_index", {}):
            blog_index[loc] = old["blog_index"][loc]
            blog_index[loc]["subtitle"] = blog_index[loc].get("subtitle", "").replace(
                "Kurze ", "Wesentliche "
            ).replace("Quick ", "Essential ").replace("Courts ", "Essentiels ").replace(
                "Brevi ", "Essenziali "
            ).replace("Guias GPX curtos", "Guias GPX essenciais").replace(
                "Guías GPX breves", "Guías GPX esenciales"
            ).replace("Korte GPX-gidsen", "Essentiële GPX-gidsen").replace(
                "Krótkie poradniki GPX", "Podstawowe poradniki GPX"
            ).replace("Panduan GPX singkat", "Panduan GPX penting")

    articles = []
    for spec in ARTICLES_EN:
        articles.append({
            "slug": spec["slug"],
            "date": spec["date"],
            "tag_en": spec["tag_en"],
            "translations": {"en": spec["en"]},
        })

    data = {"blog_index": blog_index, "articles": articles}
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote manifest with {len(articles)} articles")


def remove_old_html() -> None:
    all_slugs = set(KEEP_SLUGS) | set(REDIRECTS.keys())
    for locale in ["en"] + LOCALES:
        blog_dir = ROOT / "blog" if locale == "en" else ROOT / locale / "blog"
        if not blog_dir.exists():
            continue
        for path in blog_dir.glob("*.html"):
            if path.name == "index.html":
                continue
            slug = path.stem
            if slug not in all_slugs:
                path.unlink()
                print(f"Deleted {path.relative_to(ROOT)}")


def write_redirects() -> None:
    for old_slug, target_slug in REDIRECTS.items():
        for locale in ["en"] + LOCALES:
            if locale == "en":
                path = ROOT / "blog" / f"{old_slug}.html"
            else:
                path = ROOT / locale / "blog" / f"{old_slug}.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(redirect_html(locale if locale != "en" else "en", old_slug, target_slug), encoding="utf-8")
    print(f"Wrote {len(REDIRECTS) * 9} redirect pages")


def update_sitemap_script() -> None:
    sitemap_script = ROOT / "scripts" / "generate-sitemap.py"
    text = sitemap_script.read_text(encoding="utf-8")
    slugs_block = "\n".join(f'    "{s}.html",' for s in KEEP_SLUGS)
    import re
    text = re.sub(
        r"BLOG_SLUGS = \[.*?\]",
        f"BLOG_SLUGS = [\n{slugs_block}\n]",
        text,
        count=1,
        flags=re.DOTALL,
    )
    sitemap_script.write_text(text, encoding="utf-8")
    print("Updated generate-sitemap.py")


def main() -> None:
    write_manifest()
    remove_old_html()
    write_redirects()
    update_sitemap_script()

    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate-sitemap.py")], check=True, cwd=ROOT)

    if "--translate" in sys.argv:
        for loc in ["de", "fr", "it", "pt", "es", "nl", "pl", "id"]:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "translate-one-locale.py"), loc],
                check=True,
                cwd=ROOT,
            )
    else:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "render-blog.py")], check=True, cwd=ROOT)

    print("\nDone. Run with --translate to generate all locale HTML.")


if __name__ == "__main__":
    main()
