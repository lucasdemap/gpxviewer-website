#!/usr/bin/env python3
"""Generate concise blog-articles.json (~150 words per article, no filler)."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "blog-articles.json"
INDENT = "          "


def body(*lines: str) -> str:
    return "\n".join(INDENT + line for line in lines)


def para(text: str) -> str:
    return body(f"<p>{text}</p>")


def h2(text: str) -> str:
    return body(f"<h2>{text}</h2>")


def ul(items: list[str]) -> str:
    lines = [body("<ul>")]
    for item in items:
        lines.append(body(f"  <li>{item}</li>"))
    lines.append(body("</ul>"))
    return "\n".join(lines)


def join_sections(*sections: str) -> str:
    return "\n\n".join(sections)


def related(*links: str) -> str:
    return para("Related: " + " · ".join(links))


COMMON = {
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


def art(
    slug: str,
    date: str,
    date_display: str,
    tag: str,
    title: str,
    h1: str,
    subtitle: str,
    description: str,
    keywords: str,
    card_title: str,
    card_desc: str,
    cta_text: str,
    sections: str,
) -> dict:
    en = {**COMMON, "title": title, "h1": h1, "subtitle": subtitle, "description": description,
          "keywords": keywords, "tag": tag, "card_title": card_title, "card_desc": card_desc,
          "date_display": date_display, "cta_text": cta_text, "body": sections}
    return {"slug": slug, "date": date, "tag_en": tag, "translations": {"en": en}}


BLOG_INDEX = {
    "en": {
        "title": "GPX Viewer Blog — GPX Guides for Hiking, Cycling & Navigation",
        "description": "Short guides to open, view, and navigate GPX files on iPhone and Android.",
        "h1": "GPX Viewer Blog",
        "subtitle": "Quick guides for GPX files on iPhone and Android.",
        **{k: COMMON[k] for k in ("nav_features", "nav_blog", "nav_pro", "footer_home", "footer_privacy", "footer_contact")},
    }
}

LEGACY = [
    ("what-is-a-gpx-file", "Beginner", "What Is a GPX File?", "Learn what GPX files are and how GPS tracks work."),
    ("how-to-open-gpx-files-on-iphone", "iPhone & Android", "How to Open GPX Files on iPhone and Android", "Import GPX from Mail, Files, or Safari into GPX Viewer."),
    ("how-to-view-gpx-on-a-map", "Maps", "How to View GPX Routes on a Map", "See waypoints, elevation, and distance on interactive maps."),
    ("best-gpx-viewer-for-hiking", "Hiking", "Best GPX Viewer for Hiking", "Follow trail GPX tracks safely on your phone."),
    ("how-to-create-gpx-cycling-routes", "Cycling", "How to Create GPX Cycling Routes", "Plan bike routes and export GPX files to share."),
]

LEGACY_ARTICLES = [
    {"slug": s, "tag_en": t, "translations": {"en": {"tag": t, "card_title": ct, "card_desc": cd, "read_more": "Read guide →"}}}
    for s, t, ct, cd in LEGACY
]

ARTICLES = [
    art(
        "what-is-a-gpx-file-reader", "2026-07-12", "July 12, 2026", "Beginner",
        "What Is a GPX File Reader?",
        "What Is a GPX File Reader?",
        "How GPX readers turn GPS data into maps you can follow.",
        "A GPX file reader opens .gpx files and shows tracks on a map with distance and elevation. Learn how readers work and try GPX Viewer on iPhone and Android.",
        "gpx file reader, gpx reader, read gpx file",
        "What Is a GPX File Reader?",
        "How GPX readers parse tracks and show them on a map.",
        "Open any .gpx file in GPX Viewer — free on iPhone and Android.",
        join_sections(
            para('A <strong>GPX file reader</strong> opens <code>.gpx</code> files and draws the route on a map with distance, elevation, and waypoints. Text editors show raw XML — a reader like <a href="../">GPX Viewer</a> is what hikers and cyclists actually need.'),
            h2("What a good reader does"),
            ul([
                "Parses track points and waypoints from the GPX file",
                "Shows the route on standard, satellite, or hybrid maps",
                "Calculates distance and elevation gain automatically",
            ]),
            para('New to the format? Read <a href="what-is-a-gpx-file.html">what is a GPX file</a>, then <a href="how-to-open-gpx-file-any-device.html">open GPX on any device</a>.'),
        ),
    ),
    art(
        "how-to-open-gpx-files-on-android", "2026-07-13", "July 13, 2026", "Android",
        "How to Open GPX Files on Android",
        "How to Open GPX Files on Android",
        "Import GPX from Gmail, Drive, or Downloads in seconds.",
        "Open GPX files on Android with GPX Viewer. Import from Gmail, WhatsApp, Drive, or the Files app.",
        "open gpx android, gpx viewer android",
        "How to Open GPX Files on Android",
        "Import GPX from Gmail, Drive, or Downloads into GPX Viewer.",
        "Get GPX Viewer on Google Play and open any shared .gpx file.",
        join_sections(
            para('To open a GPX file on Android, tap the attachment or file, choose <strong>Share</strong> or <strong>Open with</strong>, and pick <a href="../">GPX Viewer</a>. Works with Gmail, WhatsApp, Google Drive, and the Files app.'),
            h2("Step by step"),
            ul([
                "Receive or download the .gpx file",
                "Tap it → Open with → GPX Viewer",
                "Review the map, distance, and elevation profile",
            ]),
            para('Problems? See <a href="gpx-file-not-opening-fixes.html">GPX not opening fixes</a>. iPhone users: <a href="how-to-open-gpx-files-on-iphone.html">open GPX on iPhone</a>.'),
        ),
    ),
    art(
        "how-to-open-gpx-file-any-device", "2026-07-14", "July 14, 2026", "Beginner",
        "How to Open a GPX File on Any Device",
        "How to Open a GPX File on Any Device",
        "Phones, computers, and GPS units — what opens .gpx files.",
        "Learn how to open GPX files on iPhone, Android, Mac, Windows, and GPS devices. GPX Viewer is the fastest option on mobile.",
        "how to open gpx file, what opens gpx files",
        "How to Open a GPX File on Any Device",
        "What opens .gpx files on phones, computers, and GPS units.",
        "Download GPX Viewer and open GPX files on your phone in one tap.",
        join_sections(
            para('GPX is an open standard — many apps read it. On <strong>iPhone and Android</strong>, <a href="../">GPX Viewer</a> is the quickest way: share the file to the app and the route appears instantly.'),
            h2("By device"),
            ul([
                "<strong>iPhone / Android</strong> — GPX Viewer (recommended), or share sheet import",
                "<strong>Mac / Windows</strong> — Garmin BaseCamp, QGIS, or Google Earth",
                "<strong>GPS watches</strong> — import via Garmin Connect or manufacturer app",
            ]),
            para('See <a href="how-to-open-gpx-files-on-android.html">Android</a> and <a href="how-to-open-gpx-files-on-iphone.html">iPhone</a> guides for mobile steps.'),
        ),
    ),
    art(
        "best-ways-view-gpx-online-offline", "2026-07-15", "July 15, 2026", "Maps",
        "Best Ways to View GPX Files Online and Offline",
        "Best Ways to View GPX Online and Offline",
        "Web tools vs mobile apps — and when you need offline maps.",
        "Compare online and offline GPX viewers. GPX Viewer works on mobile with optional offline maps in Pro.",
        "view gpx files, gpx viewer online, offline gpx viewer",
        "Best Ways to View GPX Online and Offline",
        "Web viewers vs mobile apps for GPX routes.",
        "View GPX routes on your phone — with offline maps in GPX Viewer Pro.",
        join_sections(
            para('<strong>Online:</strong> browser tools like GPSVisualizer or Google My Maps work for quick previews but need internet for map tiles. <strong>Offline:</strong> a mobile app with cached maps is essential for backcountry hikes.'),
            h2("Our recommendation"),
            para('Use <a href="../">GPX Viewer</a> on iPhone or Android for daily GPX viewing. Upgrade to Pro for <a href="view-gpx-without-internet.html">offline maps</a> when cell service is unreliable.'),
            related('<a href="how-to-view-gpx-on-a-map.html">View GPX on a map</a>', '<a href="what-is-a-gpx-file-reader.html">GPX file reader</a>'),
        ),
    ),
    art(
        "gpx-file-not-opening-fixes", "2026-07-16", "July 16, 2026", "Troubleshooting",
        "GPX File Not Opening? Common Fixes",
        "GPX File Not Opening?",
        "Fix corrupted downloads, wrong formats, and import errors.",
        "GPX file won't open? Try these fixes: check the file extension, re-download, convert KML to GPX, or open in GPX Viewer.",
        "gpx file not opening, gpx won't open",
        "GPX File Not Opening? Fixes",
        "Fix GPX files that refuse to open on your phone.",
        "Open your GPX file in GPX Viewer — free import on iPhone and Android.",
        join_sections(
            para('If a GPX file will not open, the cause is usually a bad download, wrong file type, or no app assigned to .gpx.'),
            h2("Quick fixes"),
            ul([
                "Confirm the file ends in <code>.gpx</code> (not .xml or .kml)",
                "Re-download or re-export from Strava, Komoot, or the source",
                "Open with <a href=\"../\">GPX Viewer</a> via Share → Open with",
                "Check the file is not empty (0 KB)",
            ]),
            para('Wrong format? Compare <a href="gpx-vs-kml.html">GPX vs KML</a> and <a href="gpx-vs-tcx.html">GPX vs TCX</a>.'),
        ),
    ),
    art(
        "gpx-file-format-tracks-routes-waypoints", "2026-07-17", "July 17, 2026", "Beginner",
        "GPX Format: Tracks, Routes and Waypoints",
        "GPX Tracks, Routes and Waypoints",
        "The three building blocks inside every .gpx file.",
        "Understand GPX tracks, routes, and waypoints. Learn what each element means and how GPX Viewer displays them.",
        "gpx tracks routes waypoints, gpx format",
        "GPX Tracks, Routes and Waypoints",
        "Tracks, routes, and waypoints explained simply.",
        "Open any GPX file in GPX Viewer and see tracks and waypoints on a map.",
        join_sections(
            para('Every GPX file can contain <strong>tracks</strong> (GPS breadcrumb trails), <strong>routes</strong> (planned paths), and <strong>waypoints</strong> (named points like summits or parking).'),
            h2("What each one means"),
            ul([
                "<strong>Track</strong> — recorded GPS path, most common for shared hikes and rides",
                "<strong>Route</strong> — planned sequence of points, may lack elevation detail",
                "<strong>Waypoint</strong> — a single labeled location on the map",
            ]),
            para('<a href="../">GPX Viewer</a> displays all three. Start with <a href="what-is-a-gpx-file.html">what is a GPX file</a>.'),
        ),
    ),
    art(
        "gpx-vs-kml", "2026-07-18", "July 18, 2026", "Formats",
        "GPX vs KML: What's the Difference?",
        "GPX vs KML",
        "Which format to use for hiking, cycling, and GPS devices.",
        "GPX vs KML compared. GPX is best for GPS tracks and navigation apps. KML is better for Google Earth visualizations.",
        "gpx vs kml",
        "GPX vs KML",
        "Which format for trails, bikes, and GPS apps?",
        "GPX Viewer opens .gpx files natively on iPhone and Android.",
        join_sections(
            para('<strong>GPX</strong> (GPS Exchange Format) stores tracks, routes, and elevation — ideal for hiking apps and GPS devices. <strong>KML</strong> (Keyhole Markup Language) is Google\'s format, great for Earth visualizations but less universal for navigation.'),
            h2("Which to choose"),
            ul([
                "Sharing trail or bike routes → GPX",
                "Google Earth overlays → KML",
                "Garmin / phone navigation → GPX",
            ]),
            para('Open GPX files in <a href="../">GPX Viewer</a>. Also see <a href="gpx-vs-tcx.html">GPX vs TCX</a>.'),
        ),
    ),
    art(
        "gpx-vs-tcx", "2026-07-19", "July 19, 2026", "Formats",
        "GPX vs TCX: Which Should You Use?",
        "GPX vs TCX",
        "Open route sharing vs Garmin training data.",
        "GPX vs TCX: GPX is better for sharing routes. TCX adds heart-rate and cadence data for Garmin training.",
        "gpx vs tcx",
        "GPX vs TCX",
        "Route sharing vs Garmin training exports.",
        "Open shared GPX routes in GPX Viewer on any phone.",
        join_sections(
            para('<strong>GPX</strong> is the standard for sharing hike and bike routes — any app can open it. <strong>TCX</strong> (Training Center XML) is Garmin\'s format with extra workout fields like heart rate and cadence.'),
            h2("When to use each"),
            ul([
                "Share a route with friends → GPX",
                "Upload a structured workout to Garmin → TCX",
                "View a route on iPhone/Android → GPX",
            ]),
            para('Import GPX into <a href="../">GPX Viewer</a>. Compare <a href="gpx-vs-fit.html">GPX vs FIT</a>.'),
        ),
    ),
    art(
        "gpx-vs-fit", "2026-07-20", "July 20, 2026", "Formats",
        "GPX vs FIT: What's the Difference?",
        "GPX vs FIT",
        "Open route files vs Garmin's binary activity format.",
        "GPX vs FIT explained. GPX is for sharing routes. FIT is Garmin's binary format for recorded activities.",
        "gpx vs fit",
        "GPX vs FIT",
        "Route files vs Garmin activity recordings.",
        "View and share GPX routes with GPX Viewer on mobile.",
        join_sections(
            para('<strong>GPX</strong> is text-based and widely shareable — perfect for routes. <strong>FIT</strong> is Garmin\'s binary format for recorded activities with rich sensor data, but harder to open outside Garmin ecosystem.'),
            h2("Rule of thumb"),
            ul([
                "Share a planned route → export GPX",
                "Archive a recorded ride with power/HR → FIT",
                "Preview before a group ride → GPX in GPX Viewer",
            ]),
            para('Open GPX in <a href="../">GPX Viewer</a>. <a href="import-gpx-garmin-devices.html">Import GPX to Garmin</a>.'),
        ),
    ),
    art(
        "how-to-view-gpx-elevation-data", "2026-07-21", "July 21, 2026", "Maps",
        "How to View Elevation Data from a GPX File",
        "View GPX Elevation Data",
        "Read climb, descent, and elevation profiles from any track.",
        "View elevation data from GPX files. See total climb, descent, and an elevation profile in GPX Viewer.",
        "gpx elevation, gpx elevation profile",
        "How to View GPX Elevation Data",
        "Climb, descent, and elevation profiles from GPX.",
        "See elevation profiles for any GPX route in GPX Viewer.",
        join_sections(
            para('GPX files store elevation at each GPS point. A good viewer plots an elevation profile so you can preview climbs before you start.'),
            h2("In GPX Viewer"),
            ul([
                "Import the .gpx file",
                "Scroll the elevation chart below the map",
                "Check total ascent, descent, and min/max elevation",
            ]),
            para('Plan hikes with <a href="how-to-use-gpx-files-hiking.html">GPX for hiking</a> and <a href="how-to-calculate-gpx-route-distance.html">route distance</a>.'),
        ),
    ),
    art(
        "how-to-calculate-gpx-route-distance", "2026-07-22", "July 22, 2026", "Maps",
        "How to Calculate GPX Route Distance",
        "Calculate GPX Route Distance",
        "Measure real trail distance from GPS points — not map guesses.",
        "Calculate the distance of a GPX route from its GPS track points. GPX Viewer shows accurate trail distance automatically.",
        "gpx distance, calculate gpx route distance",
        "How to Calculate GPX Route Distance",
        "Measure trail distance from GPS track points.",
        "Import a GPX file and see accurate distance in GPX Viewer.",
        join_sections(
            para('Straight-line map distance underestimates trails. GPX distance sums every GPS point along the actual path.'),
            h2("Automatic in GPX Viewer"),
            para('Open the file in <a href="../">GPX Viewer</a> — total distance appears as soon as the track loads. Pair with <a href="how-to-view-gpx-elevation-data.html">elevation data</a> to plan your day.'),
            related('<a href="how-to-view-gpx-on-a-map.html">View on a map</a>', '<a href="what-is-a-gpx-file-reader.html">GPX reader</a>'),
        ),
    ),
    art(
        "how-to-import-gpx-google-maps", "2026-07-23", "July 23, 2026", "Maps",
        "How to Import GPX Files into Google Maps",
        "Import GPX into Google Maps",
        "Use Google My Maps on desktop — or GPX Viewer on your phone.",
        "Import GPX into Google Maps via My Maps on desktop. For mobile navigation, GPX Viewer is faster.",
        "import gpx google maps, gpx google maps",
        "Import GPX into Google Maps",
        "Google My Maps on desktop, GPX Viewer on mobile.",
        "Navigate GPX routes on your phone with GPX Viewer.",
        join_sections(
            para('Google Maps on mobile does not import GPX directly. On desktop, use <strong>Google My Maps</strong>: create a map → import → upload your .gpx file.'),
            h2("Better on mobile"),
            para('For on-trail navigation, skip the desktop workaround — open the file in <a href="../">GPX Viewer</a> on iPhone or Android. See <a href="how-to-open-gpx-file-any-device.html">open GPX on any device</a>.'),
        ),
    ),
    art(
        "open-gpx-files-apple-maps", "2026-07-24", "July 24, 2026", "iPhone",
        "Can You Open GPX Files in Apple Maps?",
        "Open GPX on iPhone",
        "Apple Maps can't import GPX — use GPX Viewer instead.",
        "Apple Maps does not open GPX files. Use GPX Viewer on iPhone to view and navigate GPX routes.",
        "open gpx apple maps, gpx iphone",
        "Open GPX on iPhone",
        "Apple Maps won't import GPX — GPX Viewer will.",
        "Download GPX Viewer and open any GPX route on iPhone.",
        join_sections(
            para('<strong>Apple Maps cannot import GPX files.</strong> To view a trail or bike route on iPhone, use a dedicated GPX app.'),
            h2("What to use instead"),
            para('Share the .gpx file to <a href="../">GPX Viewer</a> from Mail, Files, or Safari. Full steps: <a href="how-to-open-gpx-files-on-iphone.html">open GPX on iPhone</a>.'),
            related('<a href="how-to-view-gpx-on-a-map.html">View on a map</a>', '<a href="view-gpx-without-internet.html">Offline viewing</a>'),
        ),
    ),
    art(
        "download-gpx-from-strava", "2026-07-25", "July 25, 2026", "Cycling",
        "How to Download GPX from Strava",
        "Download GPX from Strava",
        "Export activities and open them in GPX Viewer.",
        "Download GPX files from Strava activities and view them in GPX Viewer with maps and elevation.",
        "download gpx from strava, strava gpx export",
        "Download GPX from Strava",
        "Export Strava activities as GPX files.",
        "Export from Strava, then open in GPX Viewer on your phone.",
        join_sections(
            para('On Strava web: open an activity → <strong>⋮</strong> menu → <strong>Export GPX</strong>. Save the file, then open it in <a href="../">GPX Viewer</a> on your phone.'),
            h2("Tips"),
            ul([
                "Some activities may be export-restricted by the owner",
                "GPX includes the route track — open and check elevation before you ride",
                "Share the same file with your group via <a href=\"share-gpx-iphone-android.html\">cross-platform sharing</a>",
            ]),
        ),
    ),
    art(
        "download-gpx-from-komoot", "2026-07-26", "July 26, 2026", "Hiking",
        "How to Download GPX from Komoot",
        "Download GPX from Komoot",
        "Export Komoot tours and navigate with GPX Viewer.",
        "Download GPX from Komoot tours and open them in GPX Viewer on iPhone or Android.",
        "download gpx from komoot, komoot gpx export",
        "Download GPX from Komoot",
        "Export Komoot hiking and cycling tours as GPX.",
        "Plan in Komoot, navigate in GPX Viewer on your phone.",
        join_sections(
            para('In Komoot, open your tour → <strong>Export</strong> → choose <strong>GPX</strong>. Save the file and open it in <a href="../">GPX Viewer</a> for map preview, distance, and elevation.'),
            h2("Why both apps"),
            para('Komoot is great for planning; GPX Viewer is built for quick mobile viewing and navigation. Offline maps available with Pro — see <a href="view-gpx-without-internet.html">offline GPX</a>.'),
        ),
    ),
    art(
        "import-gpx-garmin-devices", "2026-07-27", "July 27, 2026", "Devices",
        "How to Import GPX to Garmin Devices",
        "Import GPX to Garmin",
        "Upload courses via Garmin Connect — preview in GPX Viewer first.",
        "Import GPX files to Garmin watches and Edge computers via Garmin Connect. Preview routes in GPX Viewer before syncing.",
        "import gpx garmin, gpx garmin connect",
        "Import GPX to Garmin Devices",
        "Upload GPX to Garmin Connect and sync to your watch.",
        "Preview GPX routes in GPX Viewer before syncing to Garmin.",
        join_sections(
            para('Upload a .gpx course in <strong>Garmin Connect</strong> (web or app), then send it to your watch or Edge computer.'),
            h2("Preview first"),
            para('Open the same file in <a href="../">GPX Viewer</a> to verify waypoints, distance, and elevation before syncing. Compare <a href="gpx-vs-fit.html">GPX vs FIT</a>.'),
        ),
    ),
    art(
        "how-to-use-gpx-files-hiking", "2026-07-28", "July 28, 2026", "Hiking",
        "How to Use GPX Files for Hiking",
        "Use GPX for Hiking",
        "Load trail tracks, check elevation, and navigate safely.",
        "Use GPX files for hiking. Import trail tracks, preview elevation, and follow routes on iPhone or Android.",
        "gpx hiking, hiking gpx file",
        "How to Use GPX for Hiking",
        "Load trail GPX tracks and navigate on your phone.",
        "Follow hiking GPX tracks with GPX Viewer on iPhone and Android.",
        join_sections(
            para('A shared GPX track turns a club route or guidebook path into a live map on your phone. Import it into <a href="../">GPX Viewer</a>, check distance and elevation, then follow the line on the trail.'),
            h2("Hiking tips"),
            ul([
                "Download offline maps before remote trails (GPX Viewer Pro)",
                "Always carry a paper map or backup navigation",
                "Tell someone your plan before you go",
            ]),
            para('See <a href="best-gpx-viewer-for-hiking.html">best GPX viewer for hiking</a> and <a href="view-gpx-without-internet.html">offline viewing</a>.'),
        ),
    ),
    art(
        "how-to-use-gpx-files-cycling", "2026-07-29", "July 29, 2026", "Cycling",
        "How to Use GPX Files for Cycling",
        "Use GPX for Cycling",
        "Plan rides, preview climbs, and share routes with your group.",
        "Use GPX files for cycling. Plan routes, preview elevation, and navigate on iPhone or Android with GPX Viewer.",
        "gpx cycling, cycling gpx route",
        "How to Use GPX for Cycling",
        "Plan bike routes and follow GPX tracks on rides.",
        "Preview cycling GPX routes and navigate with GPX Viewer.",
        join_sections(
            para('Export a ride from Komoot or Strava as GPX, open it in <a href="../">GPX Viewer</a>, and review distance and climbs before ride day.'),
            h2("On the bike"),
            ul([
                "Mount your phone and open the track in GPX Viewer",
                "Use Pro live location to see your position on the route",
                "Share the same GPX with your group — <a href=\"share-gpx-iphone-android.html\">iPhone and Android</a>",
            ]),
            para('<a href="how-to-create-gpx-cycling-routes.html">Create cycling routes</a> · <a href="download-gpx-from-strava.html">Strava export</a>'),
        ),
    ),
    art(
        "view-gpx-without-internet", "2026-07-30", "July 30, 2026", "Pro",
        "View GPX Without Internet",
        "View GPX Without Internet",
        "Offline maps in GPX Viewer Pro for dead zones.",
        "View GPX files without internet using GPX Viewer Pro offline maps. Download tiles before hikes and rides.",
        "offline gpx viewer, gpx offline",
        "View GPX Without Internet",
        "Offline GPX maps when cell service drops.",
        "Get GPX Viewer Pro and download offline maps before your next hike.",
        join_sections(
            para('Cell service disappears in mountains and forests. <strong>GPX Viewer Pro</strong> lets you download map tiles over Wi-Fi and view your GPX track with no connection.'),
            h2("Before you leave"),
            ul([
                "Import your GPX route",
                "Download the map area covering the track",
                "Test in airplane mode at home",
            ]),
            para('Compare <a href="best-ways-view-gpx-online-offline.html">online vs offline viewing</a>.'),
        ),
    ),
    art(
        "share-gpx-iphone-android", "2026-07-31", "July 31, 2026", "Tips",
        "Share GPX Between iPhone and Android",
        "Share GPX Between iPhone and Android",
        "Send .gpx files so everyone in your group has the same route.",
        "Share GPX files between iPhone and Android via Mail, AirDrop, Drive, or WhatsApp. Cross-platform GPX sharing guide.",
        "share gpx iphone android",
        "Share GPX Between iPhone and Android",
        "Send .gpx routes cross-platform to your group.",
        "Share GPX routes from GPX Viewer — friends open them on any phone.",
        join_sections(
            para('GPX works on both iPhone and Android — no conversion needed. Send the .gpx file via Mail, WhatsApp, AirDrop, or Google Drive.'),
            h2("How to share"),
            ul([
                "<strong>iPhone</strong> — open in GPX Viewer → Share → Mail or AirDrop",
                "<strong>Android</strong> — Share → Gmail, Drive, or WhatsApp",
                "Recipients open with GPX Viewer — see <a href=\"how-to-open-gpx-files-on-android.html\">Android</a> and <a href=\"how-to-open-gpx-files-on-iphone.html\">iPhone</a> guides",
            ]),
            para('Keep the <code>.gpx</code> extension. See <a href="what-is-a-gpx-file.html">what is GPX</a>.'),
        ),
    ),
]


def main() -> None:
    data = {"blog_index": BLOG_INDEX, "legacy_articles": LEGACY_ARTICLES, "articles": ARTICLES}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(ARTICLES)} short articles to {OUT}")


if __name__ == "__main__":
    main()
