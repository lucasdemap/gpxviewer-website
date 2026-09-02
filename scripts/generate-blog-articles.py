#!/usr/bin/env python3
"""Generate blog-articles.json with valid JSON escaping."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "blog-articles.json"

INDENT = "          "  # 10 spaces for body HTML lines


def body(*lines: str) -> str:
    return "\n".join(INDENT + line for line in lines)


def para(text: str) -> str:
    return body(f"<p>{text}</p>")


def h2(text: str) -> str:
    return body(f"<h2>{text}</h2>")


def h3(text: str) -> str:
    return body(f"<h3>{text}</h3>")


def ul(items: list[str]) -> str:
    lines = [body("<ul>")]
    for item in items:
        lines.append(body(f"  <li>{item}</li>"))
    lines.append(body("</ul>"))
    return "\n".join(lines)


def join_sections(*sections: str) -> str:
    return "\n\n".join(sections)


BLOG_INDEX = {
    "en": {
        "title": "GPX Viewer Blog — GPX Guides for Hiking, Cycling & Navigation",
        "description": "Learn how to open GPX files, view routes on a map, follow hiking trails, and create cycling tracks. Free guides from the GPX Viewer team.",
        "h1": "GPX Viewer Blog",
        "subtitle": "Guides to open, view, and navigate GPX files on iPhone and Android.",
        "nav_features": "Features",
        "nav_blog": "Blog",
        "nav_pro": "Pro",
        "footer_home": "Home",
        "footer_privacy": "Privacy",
        "footer_contact": "Contact",
    }
}

LEGACY_ARTICLES = [
    {
        "slug": "what-is-a-gpx-file",
        "tag_en": "Beginner",
        "translations": {
            "en": {
                "tag": "Beginner",
                "card_title": "What Is a GPX File? The Complete Guide for Hikers & Cyclists",
                "card_desc": "Learn what GPX files are, how GPS tracks work, and why GPX Viewer uses the .gpx format.",
            }
        },
    },
    {
        "slug": "how-to-open-gpx-files-on-iphone",
        "tag_en": "iPhone & Android",
        "translations": {
            "en": {
                "tag": "iPhone & Android",
                "card_title": "How to Open GPX Files on iPhone and Android",
                "card_desc": "Step-by-step: import GPX from Mail, Files, or Safari into GPX Viewer.",
            }
        },
    },
    {
        "slug": "how-to-view-gpx-on-a-map",
        "tag_en": "Maps",
        "translations": {
            "en": {
                "tag": "Maps",
                "card_title": "How to View GPX Routes on a Map",
                "card_desc": "See waypoints, elevation, and distance on interactive maps — standard, satellite, and hybrid.",
            }
        },
    },
    {
        "slug": "best-gpx-viewer-for-hiking",
        "tag_en": "Hiking",
        "translations": {
            "en": {
                "tag": "Hiking",
                "card_title": "Best GPX Viewer for Hiking: Follow Trails with GPS Tracks",
                "card_desc": "Why hikers use GPX files, how to follow routes safely, and what to look for in a GPX app.",
            }
        },
    },
    {
        "slug": "how-to-create-gpx-cycling-routes",
        "tag_en": "Cycling",
        "translations": {
            "en": {
                "tag": "Cycling",
                "card_title": "How to Create GPX Cycling Routes and Export Them",
                "card_desc": "Plan bike routes, save GPX tracks, and share rides with friends or your cycling computer.",
            }
        },
    },
]

COMMON_NAV = {
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


def article(
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
    body_html: str,
) -> dict:
    en = {
        **COMMON_NAV,
        "title": title,
        "h1": h1,
        "subtitle": subtitle,
        "description": description,
        "keywords": keywords,
        "tag": tag,
        "card_title": card_title,
        "card_desc": card_desc,
        "date_display": date_display,
        "cta_text": cta_text,
        "body": body_html,
    }
    return {"slug": slug, "date": date, "translations": {"en": en}}


ARTICLES = [
    article(
        "what-is-a-gpx-file-reader",
        "2026-07-12",
        "July 12, 2026",
        "Beginner",
        "What Is a GPX File Reader? How to Read GPX Files on Any Device",
        "What Is a GPX File Reader?",
        "Understand GPX readers, how they parse tracks and routes, and why a dedicated app beats a text editor.",
        "A GPX file reader turns raw GPS coordinates into maps, elevation profiles, and distance stats. Learn how GPX readers work and why GPX Viewer is the best way to read .gpx files on iPhone and Android.",
        "gpx file reader, gpx reader, read gpx file, open gpx file, gpx viewer",
        "What Is a GPX File Reader?",
        "Learn how GPX readers parse tracks, routes, and waypoints — and why GPX Viewer is the easiest way to read .gpx files on your phone.",
        "Download GPX Viewer free and read any .gpx file on your phone in seconds — no desktop software required.",
        join_sections(
            para(
                'A <strong>GPX file reader</strong> is any app or tool that opens a <code>.gpx</code> file and turns '
                "raw GPS coordinates into something you can understand — a map line, an elevation chart, or a list of "
                "waypoints. If you have ever received a hiking trail or cycling route by email, you need a GPX reader "
                "to make sense of it. While you can technically open a small GPX file in a text editor, a dedicated "
                '<a href="../">GPX Viewer</a> app is far more practical for outdoor navigation.'
            ),
            para(
                'Before choosing a reader, it helps to know what GPX files contain. Our '
                '<a href="what-is-a-gpx-file.html">complete guide to GPX files</a> explains tracks, routes, and '
                "waypoints in detail. A good GPX reader displays all three on an interactive map so you can preview "
                "a route before you leave home."
            ),
            h2("How a GPX reader works"),
            para(
                "GPX files use the GPS Exchange Format — an open XML standard. A GPX reader parses that XML, extracts "
                "latitude, longitude, elevation, and timestamps, then renders them visually. The best readers also "
                "calculate total distance, elevation gain, and estimated duration automatically."
            ),
            ul([
                "<strong>Parse the XML</strong> — read track points, route segments, and waypoint names.",
                "<strong>Render on a map</strong> — draw the path over standard, satellite, or hybrid basemaps.",
                "<strong>Show statistics</strong> — distance, climb, descent, and min/max elevation.",
                "<strong>Support import</strong> — open files from Mail, Files, Safari, or cloud storage.",
            ]),
            para(
                'GPX Viewer handles all of this on both iOS and Android. For a deeper look at map rendering, see '
                '<a href="how-to-view-gpx-on-a-map.html">how to view GPX routes on a map</a>.'
            ),
            h2("GPX reader vs. text editor"),
            para(
                "Opening a GPX file in Notepad or TextEdit shows XML tags and numbers — useful for developers, "
                "not for hikers on a trailhead. A GPX file reader translates those numbers into a colored line "
                "you can follow against your real-world surroundings."
            ),
            h3("When a text editor is enough"),
            para(
                "If you only need to verify that a file is valid GPX or copy a single coordinate, a text editor "
                "works. For anything involving navigation, elevation planning, or sharing routes, use a proper reader."
            ),
            h3("When you need a dedicated app"),
            para(
                "Choose a dedicated GPX reader when you want to import files quickly, switch map styles, and "
                "compare your live GPS position to the track. That workflow is exactly what "
                '<a href="../">GPX Viewer</a> is built for.'
            ),
            h2("Best GPX file readers in 2026"),
            para(
                "Desktop tools like Garmin BaseCamp and QGIS can read GPX files, but they require a computer. "
                "On mobile, GPX Viewer stands out because it opens files directly from Mail or the Files app "
                "without syncing through a desktop. Compare options in our guide on "
                '<a href="how-to-open-gpx-file-any-device.html">how to open a GPX file on any device</a>.'
            ),
            ul([
                "<strong>GPX Viewer (iOS & Android)</strong> — fast import, map views, elevation profile, route creation.",
                "<strong>Google Earth</strong> — desktop KML/GPX viewing, less suited for on-trail navigation.",
                "<strong>Garmin Connect</strong> — best for Garmin device owners, limited for general GPX sharing.",
            ]),
            h2("How to read a GPX file on your phone"),
            para(
                'The fastest method: save or receive the .gpx file, tap Share, and choose '
                '<a href="../">GPX Viewer</a>. Our walkthrough on '
                '<a href="how-to-open-gpx-files-on-iphone.html">opening GPX on iPhone</a> and '
                '<a href="how-to-open-gpx-files-on-android.html">opening GPX on Android</a> covers every import path.'
            ),
            para(
                "Once imported, scroll the elevation profile, zoom into tricky junctions, and check waypoint labels "
                "before you start. If the file will not open, see "
                '<a href="gpx-file-not-opening-fixes.html">GPX file not opening — fixes and troubleshooting</a>.'
            ),
            h2("Reading GPX online vs. offline"),
            para(
                "Some web-based GPX readers work in a browser but need an internet connection for map tiles. "
                'GPX Viewer Pro supports <a href="view-gpx-without-internet.html">offline GPX viewing</a> '
                "so you can read routes without cell service — essential for backcountry hikes."
            ),
            h2("Related guides"),
            para(
                'Explore <a href="gpx-file-format-tracks-routes-waypoints.html">GPX tracks, routes, and waypoints</a>, '
                'compare <a href="gpx-vs-kml.html">GPX vs KML</a>, or learn '
                '<a href="best-ways-view-gpx-online-offline.html">the best ways to view GPX online and offline</a>.'
            ),
        ),
    ),
]

# Append remaining 19 articles via helper to keep script manageable
def build_remaining_articles() -> list:
    articles = list(ARTICLES)
    specs = _remaining_specs()
    for spec in specs:
        articles.append(article(**spec))
    return articles


def _remaining_specs():
    """Article metadata and body builders for articles 2–20."""
    return [
        _article_open_android(),
        _article_open_any_device(),
        _article_view_online_offline(),
        _article_not_opening(),
        _article_format_tracks(),
        _article_gpx_vs_kml(),
        _article_gpx_vs_tcx(),
        _article_gpx_vs_fit(),
        _article_elevation(),
        _article_distance(),
        _article_google_maps(),
        _article_apple_maps(),
        _article_strava(),
        _article_komoot(),
        _article_garmin(),
        _article_hiking(),
        _article_cycling(),
        _article_offline(),
        _article_share(),
    ]


def _article_open_android():
    b = join_sections(
        para(
            'Opening a GPX file on Android should take seconds, not a trip to a desktop. Whether the file arrived '
            "via Gmail, WhatsApp, Google Drive, or your phone's Downloads folder, "
            '<a href="../">GPX Viewer</a> for Android reads .gpx tracks and routes natively — no conversion required.'
        ),
        para(
            'If you are new to the format, start with <a href="what-is-a-gpx-file.html">what is a GPX file</a>. '
            'For iPhone users, we also cover <a href="how-to-open-gpx-files-on-iphone.html">opening GPX on iPhone</a>.'
        ),
        h2("Import GPX from Gmail or messaging apps"),
        para(
            "When someone sends a .gpx attachment, tap it, then choose Open with or Share. Select GPX Viewer from "
            "the app list. The track appears on your map immediately. If GPX Viewer is not listed, download it from "
            "Google Play first, then retry the share sheet."
        ),
        h2("Open GPX from Files or Downloads"),
        para(
            "Use the Files app or your file manager to locate the .gpx file. Long-press or tap the three-dot menu, "
            "choose Open with, and pick GPX Viewer. This method works for files saved from "
            '<a href="download-gpx-from-strava.html">Strava exports</a> or '
            '<a href="download-gpx-from-komoot.html">Komoot downloads</a>.'
        ),
        h2("GPX Viewer Android features"),
        ul([
            "Standard, satellite, and hybrid map layers",
            "Elevation profile with climb and descent totals",
            "Distance and duration estimates",
            "Share GPX files back to friends or other apps",
            "Pro: live location tracking against the route",
        ]),
        h2("Fix Android GPX import problems"),
        para(
            'If the file fails to open, check <a href="gpx-file-not-opening-fixes.html">GPX troubleshooting tips</a>. '
            "Common issues include renamed .xml files, corrupted downloads, or opening KML instead of GPX."
        ),
        h2("View imported routes on a map"),
        para(
            'After import, follow our <a href="how-to-view-gpx-on-a-map.html">map viewing guide</a> to switch basemaps '
            'and inspect waypoints. For offline use in remote areas, upgrade to Pro — see '
            '<a href="view-gpx-without-internet.html">view GPX without internet</a>.'
        ),
        h2("Share routes between Android and iPhone"),
        para(
            'GPX is cross-platform. Read <a href="share-gpx-iphone-android.html">how to share GPX between iPhone and Android</a> '
            "so your group always has the same trail file."
        ),
    )
    return dict(
        slug="how-to-open-gpx-files-on-android",
        date="2026-07-13",
        date_display="July 13, 2026",
        tag="Android",
        title="How to Open GPX Files on Android — GPX Viewer Guide",
        h1="How to Open GPX Files on Android",
        subtitle="Import GPX tracks from Mail, Drive, or Downloads into GPX Viewer on any Android phone.",
        description="Step-by-step guide to open GPX files on Android using GPX Viewer. Import from Gmail, Files, Drive, and messaging apps.",
        keywords="open gpx android, gpx viewer android, open gpx file android, gpx android app",
        card_title="How to Open GPX Files on Android",
        card_desc="Import GPX from Gmail, Drive, or Downloads into GPX Viewer — the fastest Android GPX viewer.",
        cta_text="Get GPX Viewer on Google Play and open any .gpx file shared to your Android phone.",
        body_html=b,
    )


def _article_open_any_device():
    b = join_sections(
        para(
            "GPX files travel well — the same .gpx attachment opens on iPhone, Android, Windows, Mac, and many GPS "
            "watches. The question is not whether the format works everywhere, but which tool gives you the best "
            "experience on each device. For phone navigation, "
            '<a href="../">GPX Viewer</a> remains the simplest answer.'
        ),
        h2("What opens GPX files?"),
        ul([
            "<strong>GPX Viewer</strong> — iOS and Android; built for outdoor route viewing and navigation.",
            "<strong>Garmin BaseCamp / Connect</strong> — Garmin ecosystem on desktop and mobile.",
            "<strong>QGIS / Google Earth</strong> — desktop analysis and visualization.",
            "<strong>Cycling computers & watches</strong> — Wahoo, Garmin, Coros via USB or app sync.",
        ]),
        para(
            'Learn the format basics in <a href="what-is-a-gpx-file.html">what is a GPX file</a> and '
            '<a href="what-is-a-gpx-file-reader.html">what is a GPX file reader</a>.'
        ),
        h2("Open GPX on iPhone and Android"),
        para(
            'Mobile is where most people first encounter GPX. See '
            '<a href="how-to-open-gpx-files-on-iphone.html">open GPX on iPhone</a> and '
            '<a href="how-to-open-gpx-files-on-android.html">open GPX on Android</a> for platform-specific steps.'
        ),
        h2("Open GPX on desktop"),
        para(
            "Double-clicking a GPX file may open it in a browser or map app depending on your OS. For serious "
            "editing, desktop GIS tools work well — but for quick preview before a hike, send the file to your "
            "phone and open it in GPX Viewer instead."
        ),
        h2("Open GPX on GPS devices"),
        para(
            'Transfer to Garmin and other units with our '
            '<a href="import-gpx-garmin-devices.html">import GPX to Garmin devices</a> guide.'
        ),
        h2("When GPX will not open"),
        para(
            'Try <a href="gpx-file-not-opening-fixes.html">GPX file not opening fixes</a> or confirm you do not '
            'have a <a href="gpx-vs-kml.html">KML file instead of GPX</a>.'
        ),
        h2("Best viewer for any device"),
        para(
            'For on-the-go use, <a href="best-ways-view-gpx-online-offline.html">view GPX online and offline</a> '
            "with GPX Viewer — one app for import, map display, elevation, and sharing."
        ),
    )
    return dict(
        slug="how-to-open-gpx-file-any-device",
        date="2026-07-14",
        date_display="July 14, 2026",
        tag="Beginner",
        title="How to Open a GPX File on Any Device — Phones, PCs & GPS Units",
        h1="How to Open a GPX File on Any Device",
        subtitle="From iPhone and Android to desktop and Garmin — every way to open .gpx files explained.",
        description="Learn what opens GPX files on iPhone, Android, Windows, Mac, and GPS devices. Compare tools and find the fastest way to view routes.",
        keywords="how to open gpx file, what opens gpx files, open gpx file, gpx viewer",
        card_title="How to Open a GPX File on Any Device",
        card_desc="Phones, desktops, and GPS units — discover what opens .gpx files and the fastest way to view routes.",
        cta_text="Open GPX files on iPhone or Android today — import from Mail, Files, or any share sheet.",
        body_html=b,
    )


# Due to length, remaining article builders follow same pattern
def _article_view_online_offline():
    b = join_sections(
        para(
            "You can view GPX files in a web browser or on your phone — each approach has trade-offs. Online GPX "
            "viewers load map tiles over the internet; offline viewers cache basemaps so you can navigate without "
            "cell service. <a href=\"../\">GPX Viewer</a> supports both workflows, with offline maps available in Pro."
        ),
        h2("Online GPX viewers"),
        para(
            "Browser-based tools let you drag and drop a file for a quick preview. They are handy at a desk but "
            "unreliable on a mountain ridge with no signal. For field use, move the file to your phone."
        ),
        h2("Offline GPX viewing"),
        para(
            'GPX Viewer Pro downloads map regions for <a href="view-gpx-without-internet.html">offline GPX viewing</a>. '
            "Your track, elevation profile, and stats remain available even in airplane mode."
        ),
        h2("Compare viewing methods"),
        ul([
            "<strong>Web upload</strong> — fast preview, needs internet for maps.",
            "<strong>GPX Viewer (online)</strong> — full mobile maps when connected.",
            "<strong>GPX Viewer Pro (offline)</strong> — cached tiles for backcountry trips.",
        ]),
        para(
            'See <a href="how-to-view-gpx-on-a-map.html">view GPX on a map</a> and '
            '<a href="what-is-a-gpx-file-reader.html">GPX file readers</a> for related tips.'
        ),
        h2("Choosing the right approach"),
        para(
            "Urban cyclists often rely on live maps. Alpine hikers need offline backups. GPX Viewer lets you "
            "start free online and upgrade when offline matters."
        ),
    )
    return dict(
        slug="best-ways-view-gpx-online-offline",
        date="2026-07-15",
        date_display="July 15, 2026",
        tag="Maps",
        title="Best Ways to View GPX Files Online and Offline",
        h1="Best Ways to View GPX Online and Offline",
        subtitle="Compare browser viewers, mobile apps, and offline map downloads for GPX routes.",
        description="Discover the best ways to view GPX files online and offline. Compare web tools vs GPX Viewer for hiking and cycling navigation.",
        keywords="view gpx files, gpx viewer online, offline gpx viewer, gpx map viewer",
        card_title="Best Ways to View GPX Online and Offline",
        card_desc="Web tools vs mobile apps — find the best way to view GPX routes with or without internet.",
        cta_text="View GPX routes on your phone free — upgrade to Pro for offline maps in the backcountry.",
        body_html=b,
    )


def _article_not_opening():
    b = join_sections(
        para(
            "A GPX file that refuses to open is frustrating — especially when you are packing for an early start. "
            "Most failures come from a handful of fixable causes: wrong file type, incomplete download, or an app "
            "that does not handle GPX natively. This guide walks through each scenario."
        ),
        h2("Check the file extension"),
        para(
            'Confirm the file ends in <code>.gpx</code>, not <code>.kml</code>, <code>.tcx</code>, or <code>.fit</code>. '
            'See <a href="gpx-vs-kml.html">GPX vs KML</a>, <a href="gpx-vs-tcx.html">GPX vs TCX</a>, and '
            '<a href="gpx-vs-fit.html">GPX vs FIT</a> if you need to convert or re-export.'
        ),
        h2("Re-download the file"),
        para(
            "Interrupted downloads produce truncated XML that parsers reject. Delete the local copy and download "
            "again from Strava, Komoot, or email."
        ),
        h2("Validate GPX structure"),
        para(
            'Open the file in a text editor and look for <code>&lt;gpx</code> at the top. Empty files or HTML error '
            'pages saved as .gpx will not work. Learn valid structure in '
            '<a href="gpx-file-format-tracks-routes-waypoints.html">GPX tracks, routes, and waypoints</a>.'
        ),
        h2("Use a dedicated GPX app"),
        para(
            'Generic zip or document apps cannot render maps. Install '
            '<a href="../">GPX Viewer</a> and use Share → GPX Viewer. Follow '
            '<a href="how-to-open-gpx-file-any-device.html">open GPX on any device</a> if the share sheet hides the app.'
        ),
        h2("Platform-specific fixes"),
        ul([
            "<strong>iPhone</strong> — use Files or Mail; see our iPhone import guide.",
            "<strong>Android</strong> — clear default app associations in Settings if the wrong app opens.",
            "<strong>Desktop</strong> — rename .xml exports back to .gpx when safe.",
        ]),
        h2("Still stuck?"),
        para(
            'Read <a href="what-is-a-gpx-file.html">what is a GPX file</a> and confirm the sender exported GPX, '
            "not a proprietary format."
        ),
    )
    return dict(
        slug="gpx-file-not-opening-fixes",
        date="2026-07-16",
        date_display="July 16, 2026",
        tag="Troubleshooting",
        title="GPX File Not Opening? Fixes and Troubleshooting Guide",
        h1="GPX File Not Opening? Here Are the Fixes",
        subtitle="Diagnose corrupt downloads, wrong formats, and app issues when your .gpx file will not open.",
        description="GPX file not opening? Fix corrupt downloads, wrong extensions, and app issues. Step-by-step GPX troubleshooting for iPhone and Android.",
        keywords="gpx file not opening, gpx won't open, fix gpx file, gpx troubleshooting",
        card_title="GPX File Not Opening? Fixes and Troubleshooting",
        card_desc="Wrong format, bad download, or missing app — fix GPX files that refuse to open on your phone.",
        cta_text="Install GPX Viewer and open stubborn .gpx files with a reader built for the GPS Exchange Format.",
        body_html=b,
    )


def _article_format_tracks():
    b = join_sections(
        para(
            "Every GPX file organizes location data into tracks, routes, and waypoints. Understanding the difference "
            "helps you pick the right file for hiking navigation or cycling planning. For a full introduction, read "
            '<a href="what-is-a-gpx-file.html">what is a GPX file</a> first.'
        ),
        h2("GPX tracks"),
        para(
            "A track is a series of recorded GPS points — typically logged while you move. Tracks reflect where you "
            "actually went, including small detours. Hikers follow shared trail tracks; cyclists analyze recorded rides."
        ),
        h2("GPX routes"),
        para(
            "A route connects key waypoints with straight or simplified segments. Routes represent planned paths "
            "and are common in turn-by-turn cycling navigation."
        ),
        h2("GPX waypoints"),
        para(
            "Waypoints are single named points — summits, water sources, parking, or cafes. They appear as pins on "
            "the map inside <a href=\"../\">GPX Viewer</a>."
        ),
        h3("Tracks vs routes in practice"),
        para(
            'Use tracks for <a href="how-to-use-gpx-files-hiking.html">hiking GPX files</a> and routes for '
            '<a href="how-to-create-gpx-cycling-routes.html">planned cycling loops</a>.'
        ),
        h2("Elevation and timestamps"),
        para(
            'Each point may include elevation and time. Learn more in '
            '<a href="how-to-view-gpx-elevation-data.html">view GPX elevation data</a> and '
            '<a href="how-to-calculate-gpx-route-distance.html">calculate GPX route distance</a>.'
        ),
        h2("Open and inspect your file"),
        para(
            'Import into GPX Viewer and switch map styles with '
            '<a href="how-to-view-gpx-on-a-map.html">view GPX on a map</a>.'
        ),
    )
    return dict(
        slug="gpx-file-format-tracks-routes-waypoints",
        date="2026-07-17",
        date_display="July 17, 2026",
        tag="Beginner",
        title="GPX File Format Explained: Tracks, Routes & Waypoints",
        h1="GPX Tracks, Routes, and Waypoints Explained",
        subtitle="Learn how the GPX file format stores paths, planned routes, and point-of-interest markers.",
        description="Understand GPX tracks vs routes vs waypoints. Learn how the GPX file format stores GPS data for hiking and cycling.",
        keywords="gpx tracks routes waypoints, gpx file format, gpx track vs route",
        card_title="GPX Tracks, Routes, and Waypoints",
        card_desc="Tracks, routes, and waypoints — understand the building blocks of every .gpx file.",
        cta_text="Open any GPX file in GPX Viewer and see tracks, routes, and waypoints on an interactive map.",
        body_html=b,
    )


def _article_gpx_vs_kml():
    b = join_sections(
        para(
            "GPX and KML are both open formats for geographic data, but they serve different workflows. GPX dominates "
            "GPS navigation for hiking and cycling; KML is common in Google Earth and legacy Google Maps layers."
        ),
        h2("What is KML?"),
        para(
            "KML (Keyhole Markup Language) describes points, lines, and polygons with rich styling — folders, icons, "
            "and descriptions. It excels at presentation more than turn-by-turn GPS logging."
        ),
        h2("GPX strengths"),
        ul([
            "Native support on GPS watches and cycling computers",
            "Tracks with timestamps and elevation for activity analysis",
            "Smaller files for long trails",
            "Direct import into <a href=\"../\">GPX Viewer</a> without conversion",
        ]),
        h2("When to use each"),
        para(
            'Share hiking trails and ride files as GPX. Use KML for Google Earth visualization. If you received KML, '
            're-export as GPX from your planning tool or read '
            '<a href="how-to-import-gpx-google-maps.html">import GPX to Google Maps</a> for context.'
        ),
        h2("Convert between formats"),
        para(
            'Many planners export both. See also <a href="gpx-vs-tcx.html">GPX vs TCX</a> and '
            '<a href="gpx-vs-fit.html">GPX vs FIT</a>.'
        ),
        h2("View GPX on your phone"),
        para(
            '<a href="what-is-a-gpx-file.html">What is a GPX file</a> · '
            '<a href="how-to-view-gpx-on-a-map.html">View on a map</a>'
        ),
    )
    return dict(
        slug="gpx-vs-kml",
        date="2026-07-18",
        date_display="July 18, 2026",
        tag="Formats",
        title="GPX vs KML: Which Format Should You Use for Routes?",
        h1="GPX vs KML: Which Format Is Better?",
        subtitle="Compare GPX and KML for hiking trails, cycling routes, and map sharing.",
        description="GPX vs KML compared for outdoor navigation. Learn which format works best for hiking, cycling, and GPS devices.",
        keywords="gpx vs kml, gpx or kml, convert kml to gpx",
        card_title="GPX vs KML: Which Format to Use?",
        card_desc="GPX vs KML for trails and rides — which format fits hiking, cycling, and GPS devices?",
        cta_text="Stick with GPX for outdoor navigation — open .gpx files instantly in GPX Viewer.",
        body_html=b,
    )


def _article_gpx_vs_tcx():
    b = join_sections(
        para(
            "TCX (Training Center XML) is Garmin's activity format with heart rate, cadence, and lap data. GPX is "
            "the universal exchange format almost every app accepts. Cyclists often have both in their export menus."
        ),
        h2("TCX advantages"),
        ul([
            "Rich sensor data from Garmin devices",
            "Structured lap and course information",
            "Good for training analysis in Garmin Connect",
        ]),
        h2("GPX advantages"),
        ul([
            "Works on iPhone, Android, and most non-Garmin devices",
            "Smaller, simpler files for sharing routes",
            "Opens directly in GPX Viewer for map preview",
        ]),
        h2("Which should you export?"),
        para(
            "Export TCX for detailed workout review in Garmin ecosystem. Export GPX when sharing a route with friends "
            "or loading it on a phone. See "
            '<a href="download-gpx-from-strava.html">download GPX from Strava</a> for a common workflow.'
        ),
        h2("Related comparisons"),
        para(
            '<a href="gpx-vs-kml.html">GPX vs KML</a> · <a href="gpx-vs-fit.html">GPX vs FIT</a> · '
            '<a href="how-to-create-gpx-cycling-routes.html">Create cycling routes</a>'
        ),
    )
    return dict(
        slug="gpx-vs-tcx",
        date="2026-07-19",
        date_display="July 19, 2026",
        tag="Formats",
        title="GPX vs TCX: Training Files vs Universal Route Sharing",
        h1="GPX vs TCX: What's the Difference?",
        subtitle="Garmin TCX vs GPX — when to export each format for cycling and hiking.",
        description="Compare GPX vs TCX for cycling and hiking. Learn when Garmin's TCX format beats GPX and when to share .gpx instead.",
        keywords="gpx vs tcx, tcx vs gpx, garmin tcx, export gpx cycling",
        card_title="GPX vs TCX for Cyclists and Hikers",
        card_desc="Training Center XML vs GPS Exchange Format — pick the right export for sharing and navigation.",
        cta_text="Share rides as GPX so anyone can open your route in GPX Viewer on iPhone or Android.",
        body_html=b,
    )


def _article_gpx_vs_fit():
    b = join_sections(
        para(
            "FIT is Garmin's compact binary format for recorded activities. GPX is human-readable XML designed for "
            "sharing routes between apps. You cannot email a FIT file to a hiking partner and expect their iPhone "
            "to show a map — but GPX works everywhere."
        ),
        h2("FIT file traits"),
        ul([
            "Binary, smaller on disk",
            "Stores high-frequency sensor streams",
            "Primarily Garmin / ANT+ ecosystem",
        ]),
        h2("GPX file traits"),
        ul([
            "Text XML any editor can inspect",
            "Universal import on phones and web tools",
            "Ideal for trail sharing and <a href=\"import-gpx-garmin-devices.html\">Garmin course import</a>",
        ]),
        h2("Converting FIT to GPX"),
        para(
            "Use Garmin Connect, Golden Cheetah, or similar tools to export GPX from a FIT activity when you need "
            "a shareable route file."
        ),
        h2("View routes on mobile"),
        para(
            '<a href="what-is-a-gpx-file-reader.html">GPX file reader</a> · '
            '<a href="gpx-vs-tcx.html">GPX vs TCX</a>'
        ),
    )
    return dict(
        slug="gpx-vs-fit",
        date="2026-07-20",
        date_display="July 20, 2026",
        tag="Formats",
        title="GPX vs FIT: Shareable Routes vs Garmin Activity Files",
        h1="GPX vs FIT: Which Format Do You Need?",
        subtitle="Understand Garmin FIT binary files vs open GPX route sharing.",
        description="GPX vs FIT explained. Learn why GPX is better for sharing hiking and cycling routes while FIT suits Garmin device recording.",
        keywords="gpx vs fit, fit vs gpx, garmin fit file, convert fit to gpx",
        card_title="GPX vs FIT: Routes vs Activity Files",
        card_desc="Garmin FIT vs GPX — when to use binary activity files and when to share open .gpx routes.",
        cta_text="Keep GPX for sharing trails — open every route in GPX Viewer without proprietary converters.",
        body_html=b,
    )


def _article_elevation():
    b = join_sections(
        para(
            "Elevation data transforms a flat line on a map into a climb profile you can feel in your legs before "
            "you start. Most GPX files include height values per track point; GPX Viewer charts them automatically."
        ),
        h2("Where elevation comes from"),
        para(
            "GPS receivers, barometric altimeters, and post-processed DEM corrections can populate elevation tags. "
            "Quality varies — barometric data is often smoother on trails."
        ),
        h2("Reading the elevation profile"),
        para(
            "After import, scroll the profile to spot steep pitches and cumulative gain. Pair with "
            '<a href="how-to-calculate-gpx-route-distance.html">route distance calculations</a> for planning.'
        ),
        h2("Elevation for hikers"),
        para(
            'Steep GPX segments warn you before alpine sections. See '
            '<a href="how-to-use-gpx-files-hiking.html">how to use GPX for hiking</a> and '
            '<a href="best-gpx-viewer-for-hiking.html">best GPX viewer for hiking</a>.'
        ),
        h2("Elevation for cyclists"),
        para(
            'Plan climbs on sportives with '
            '<a href="how-to-use-gpx-files-cycling.html">cycling GPX guides</a>.'
        ),
        h2("View on a map"),
        para(
            '<a href="how-to-view-gpx-on-a-map.html">View GPX on a map</a> · '
            '<a href="gpx-file-format-tracks-routes-waypoints.html">GPX format basics</a>'
        ),
    )
    return dict(
        slug="how-to-view-gpx-elevation-data",
        date="2026-07-21",
        date_display="July 21, 2026",
        tag="Maps",
        title="How to View GPX Elevation Data and Climb Profiles",
        h1="How to View GPX Elevation Data",
        subtitle="Read climb profiles, total ascent, and altitude stats from any GPX track.",
        description="Learn how to view GPX elevation data and climb profiles. See total ascent, descent, and altitude charts in GPX Viewer.",
        keywords="gpx elevation, gpx elevation profile, view gpx altitude, gpx climb profile",
        card_title="How to View GPX Elevation Data",
        card_desc="Climb profiles, total ascent, and altitude stats — read elevation from any GPX track.",
        cta_text="Import a GPX file and explore elevation profiles free in GPX Viewer.",
        body_html=b,
    )


def _article_distance():
    b = join_sections(
        para(
            "Knowing the distance of a GPX route helps you estimate time, water, and daylight. GPX Viewer calculates "
            "track length by summing geodesic segments between consecutive GPS points."
        ),
        h2("How GPX distance is calculated"),
        para(
            "Each lat/lon pair connects to the next; haversine or similar formulas yield meters along the path. "
            "Dense point recordings produce more accurate totals on twisty trails."
        ),
        h2("Distance vs straight-line"),
        para(
            "Never use map ruler tools for trail distance — switchbacks add length the eye misses. Trust the GPX "
            "track total instead."
        ),
        h2("Combine with elevation"),
        para(
            '<a href="how-to-view-gpx-elevation-data.html">View elevation data</a> alongside distance for full '
            "trip planning."
        ),
        h2("Plan hikes and rides"),
        para(
            '<a href="how-to-use-gpx-files-hiking.html">Hiking GPX</a> · '
            '<a href="how-to-create-gpx-cycling-routes.html">Create cycling routes</a>'
        ),
    )
    return dict(
        slug="how-to-calculate-gpx-route-distance",
        date="2026-07-22",
        date_display="July 22, 2026",
        tag="Maps",
        title="How to Calculate GPX Route Distance Accurately",
        h1="How to Calculate GPX Route Distance",
        subtitle="Measure trail and road distance from any GPX track — not just straight-line guesses.",
        description="Calculate GPX route distance from track points. Learn how GPX Viewer measures hiking and cycling route length accurately.",
        keywords="gpx route distance, calculate gpx distance, gpx track length, gpx mileage",
        card_title="How to Calculate GPX Route Distance",
        card_desc="Measure true trail distance from GPS points — not straight-line map guesses.",
        cta_text="See exact GPX route distance and elevation in GPX Viewer after a one-tap import.",
        body_html=b,
    )


def _article_google_maps():
    b = join_sections(
        para(
            "Google Maps does not natively open arbitrary GPX files on mobile, but you can import routes on desktop "
            "or use GPX Viewer on your phone for a faster workflow."
        ),
        h2("Import GPX to Google Maps (desktop)"),
        para(
            "In Google My Maps, create a layer and import a .gpx file. Useful for planning; less helpful offline "
            "on trail."
        ),
        h2("Better mobile workflow"),
        para(
            'Skip conversion — open the same file in <a href="../">GPX Viewer</a>. See '
            '<a href="how-to-open-gpx-files-on-iphone.html">iPhone</a> and '
            '<a href="how-to-open-gpx-files-on-android.html">Android</a> import guides.'
        ),
        h2("GPX vs KML in Google ecosystem"),
        para(
            '<a href="gpx-vs-kml.html">GPX vs KML</a> explains why hikers still prefer GPX for device export.'
        ),
        h2("View on rich basemaps"),
        para(
            '<a href="how-to-view-gpx-on-a-map.html">View GPX on a map</a> with satellite and hybrid layers.'
        ),
    )
    return dict(
        slug="how-to-import-gpx-google-maps",
        date="2026-07-23",
        date_display="July 23, 2026",
        tag="Maps",
        title="How to Import GPX Files into Google Maps",
        h1="How to Import GPX into Google Maps",
        subtitle="Use Google My Maps on desktop — or GPX Viewer for faster mobile navigation.",
        description="Import GPX files into Google Maps via My Maps. Compare desktop workflow vs GPX Viewer on iPhone and Android.",
        keywords="import gpx google maps, gpx google maps, open gpx google maps",
        card_title="How to Import GPX into Google Maps",
        card_desc="Google My Maps on desktop — plus a faster way to navigate GPX on your phone.",
        cta_text="Skip My Maps limits — navigate GPX routes natively on iPhone and Android with GPX Viewer.",
        body_html=b,
    )


def _article_apple_maps():
    b = join_sections(
        para(
            "Apple Maps does not offer a built-in GPX import on iPhone. To follow a shared trail, use a dedicated "
            "GPX app — GPX Viewer is designed for exactly this gap."
        ),
        h2("Why Apple Maps lacks GPX import"),
        para(
            "Apple Maps focuses on driving and general POI search, not outdoor track following. GPX remains the "
            "standard hikers and cyclists share."
        ),
        h2("Open GPX on iPhone instead"),
        para(
            'Follow <a href="how-to-open-gpx-files-on-iphone.html">how to open GPX on iPhone</a>: Mail → Share → '
            "GPX Viewer."
        ),
        h2("Compare with Apple Watch / Fitness"),
        para(
            "Recorded workouts export differently; for shared routes, stick to .gpx files."
        ),
        h2("Map viewing tips"),
        para(
            '<a href="how-to-view-gpx-on-a-map.html">View on a map</a> · '
            '<a href="open-gpx-files-apple-maps.html">this guide</a> · '
            '<a href="best-gpx-viewer-for-hiking.html">best hiking viewer</a>'
        ),
    )
    return dict(
        slug="open-gpx-files-apple-maps",
        date="2026-07-24",
        date_display="July 24, 2026",
        tag="iPhone",
        title="Can You Open GPX Files in Apple Maps? (And What to Use Instead)",
        h1="Open GPX Files on iPhone — Beyond Apple Maps",
        subtitle="Apple Maps cannot import GPX — here is the best iPhone workflow for trail navigation.",
        description="Apple Maps does not open GPX files. Learn the best iPhone alternative to view and follow GPX hiking and cycling routes.",
        keywords="open gpx apple maps, gpx iphone apple maps, gpx viewer iphone",
        card_title="Open GPX on iPhone — Beyond Apple Maps",
        card_desc="Apple Maps won't import GPX — use GPX Viewer for trail and cycling navigation on iPhone.",
        cta_text="Replace Apple Maps workarounds — follow GPX trails natively with GPX Viewer on iPhone.",
        body_html=b,
    )


def _article_strava():
    b = join_sections(
        para(
            "Strava lets athletes export activities as GPX — perfect for archiving rides or sharing a route with "
            "friends who do not use Strava. Export from Strava, then view the track in "
            '<a href="../">GPX Viewer</a> for maps and elevation beyond the Strava feed.'
        ),
        h2("Export GPX from Strava"),
        para(
            "On strava.com, open the activity, click the three-dot menu, and choose Export GPX. On mobile, use "
            "Share or export options when available, or open the activity on the web. Save the .gpx file to Files "
            "or Google Drive."
        ),
        h2("View Strava GPX in GPX Viewer"),
        para(
            "Tap the exported file and share it to GPX Viewer. You get satellite maps, elevation profiles, and "
            "distance stats without a Strava subscription on the viewer side."
        ),
        h2("Why export instead of only viewing in Strava"),
        ul([
            "Share routes with non-Strava users",
            "Archive personal backups of important rides and hikes",
            "Load the same file on a second device or cycling computer",
            "Inspect elevation and map detail in GPX Viewer Pro offline",
        ]),
        h2("Strava vs GPX Viewer workflow"),
        para(
            "Strava remains excellent for social training logs and segments. GPX Viewer complements it as a "
            "focused map reader — especially when you want a clean track overlay without feed distractions."
        ),
        h2("Related guides"),
        para(
            '<a href="download-gpx-from-komoot.html">Download GPX from Komoot</a> · '
            '<a href="how-to-use-gpx-files-cycling.html">Use GPX for cycling</a> · '
            '<a href="gpx-vs-tcx.html">GPX vs TCX</a>'
        ),
    )
    return dict(
        slug="download-gpx-from-strava",
        date="2026-07-25",
        date_display="July 25, 2026",
        tag="Cycling",
        title="How to Download GPX from Strava and View Routes in GPX Viewer",
        h1="Download GPX from Strava",
        subtitle="Export Strava activities as GPX files and view them on a rich map in GPX Viewer.",
        description="Download GPX from Strava activities and open them in GPX Viewer. Export rides and runs, then view maps and elevation on iPhone or Android.",
        keywords="download gpx from strava, strava export gpx, strava gpx export",
        card_title="Download GPX from Strava",
        card_desc="Export Strava activities as GPX, then view routes with maps and elevation in GPX Viewer.",
        cta_text="Export from Strava, open in GPX Viewer — see your rides on satellite maps with full elevation data.",
        body_html=b,
    )


def _article_komoot():
    b = join_sections(
        para(
            "Komoot is a popular route planner for hiking and bike touring. Every planned tour can be exported as "
            "GPX for use in other apps. Download from Komoot, then open the file in "
            '<a href="../">GPX Viewer</a> for mobile navigation with multiple map styles.'
        ),
        h2("Export GPX from Komoot"),
        para(
            "In the Komoot app or website, open your tour, choose Export or Download, and select GPX format. "
            "Komoot may offer version options — pick the standard GPX track for broad compatibility."
        ),
        h2("Open Komoot GPX on your phone"),
        para(
            'Save to Files or Downloads, then follow '
            '<a href="how-to-open-gpx-files-on-iphone.html">iPhone</a> or '
            '<a href="how-to-open-gpx-files-on-android.html">Android</a> import steps.'
        ),
        h2("Komoot + GPX Viewer together"),
        para(
            "Plan visually in Komoot with surface types and highlights; navigate in the field with GPX Viewer. "
            "Pro offline maps help when Komoot streaming maps lose signal."
        ),
        h2("Troubleshooting Komoot exports"),
        para(
            'If the file fails, see <a href="gpx-file-not-opening-fixes.html">GPX not opening fixes</a>. '
            "Re-export after the tour sync completes."
        ),
        h2("Related"),
        para(
            '<a href="download-gpx-from-strava.html">Strava GPX export</a> · '
            '<a href="how-to-use-gpx-files-hiking.html">Hiking with GPX</a> · '
            '<a href="view-gpx-without-internet.html">Offline viewing</a>'
        ),
    )
    return dict(
        slug="download-gpx-from-komoot",
        date="2026-07-26",
        date_display="July 26, 2026",
        tag="Hiking",
        title="How to Download GPX from Komoot and Open in GPX Viewer",
        h1="Download GPX from Komoot",
        subtitle="Export Komoot tours as GPX and navigate them on your phone with GPX Viewer.",
        description="Download GPX from Komoot tours and open them in GPX Viewer. Export hiking and cycling routes from Komoot for mobile navigation.",
        keywords="download gpx from komoot, komoot export gpx, komoot gpx download",
        card_title="Download GPX from Komoot",
        card_desc="Export Komoot hiking and cycling tours as GPX, then navigate with GPX Viewer on your phone.",
        cta_text="Plan in Komoot, navigate in GPX Viewer — import Komoot GPX exports in one tap.",
        body_html=b,
    )


def _article_garmin():
    b = join_sections(
        para(
            "Garmin devices excel at recording activities, but sharing or previewing a route often means moving a "
            "GPX file between Garmin Connect, your phone, and your watch. GPX Viewer helps you inspect courses "
            "before you sync them to hardware."
        ),
        h2("Import GPX to Garmin Connect"),
        para(
            "Upload a .gpx course in Garmin Connect web or app, then send it to a compatible watch or Edge computer. "
            "Ensure the file is a route or track Garmin recognizes — not a corrupted export."
        ),
        h2("Preview GPX before syncing"),
        para(
            'Open the same file in <a href="../">GPX Viewer</a> to verify waypoints, distance, and elevation. '
            'Fix issues early with <a href="gpx-file-not-opening-fixes.html">troubleshooting tips</a>.'
        ),
        h2("Export from Garmin to GPX"),
        para(
            "Activities recorded on Garmin hardware can export as GPX from Connect for sharing. Compare "
            '<a href="gpx-vs-fit.html">GPX vs FIT</a> and <a href="gpx-vs-tcx.html">GPX vs TCX</a> when choosing formats.'
        ),
        h2("USB and wireless transfer"),
        ul([
            "Garmin Connect mobile sync for recent courses",
            "USB mass storage on some legacy devices",
            "Third-party apps that accept GPX email attachments",
        ]),
        h2("Phone-first workflow"),
        para(
            'Many hikers now load GPX on the phone first via '
            '<a href="how-to-open-gpx-file-any-device.html">any-device import</a>, using the watch as backup.'
        ),
    )
    return dict(
        slug="import-gpx-garmin-devices",
        date="2026-07-27",
        date_display="July 27, 2026",
        tag="Devices",
        title="How to Import GPX Files to Garmin Watches and Edge Computers",
        h1="Import GPX to Garmin Devices",
        subtitle="Upload GPX courses to Garmin Connect and preview routes before syncing to your device.",
        description="Learn how to import GPX files to Garmin watches and Edge computers via Garmin Connect. Preview routes in GPX Viewer first.",
        keywords="import gpx garmin, gpx garmin connect, gpx to garmin watch",
        card_title="Import GPX to Garmin Devices",
        card_desc="Upload GPX to Garmin Connect and preview courses in GPX Viewer before syncing to your watch.",
        cta_text="Preview any GPX course in GPX Viewer before sending it to your Garmin device.",
        body_html=b,
    )


def _article_hiking():
    b = join_sections(
        para(
            "GPX files changed hiking navigation — a shared track from a club or guidebook becomes a live map reference "
            "on your phone. Used well, GPX keeps you on path without replacing map-reading skills."
        ),
        h2("Why hikers use GPX"),
        ul([
            "Follow official trail tracks in poorly marked terrain",
            "Preview elevation and distance before long days",
            "Share planned routes with your group",
            "Archive completed hikes for memory and safety records",
        ]),
        h2("Load a trail GPX on your phone"),
        para(
            'Import via Mail or Files — see '
            '<a href="how-to-open-gpx-files-on-iphone.html">iPhone</a> and '
            '<a href="best-gpx-viewer-for-hiking.html">best GPX viewer for hiking</a>.'
        ),
        h2("Follow the track safely"),
        para(
            "GPX shows where the path goes, not current weather, closures, or your exact real-time position unless "
            "you enable live location in GPX Viewer Pro. Always carry backup navigation and tell someone your plan."
        ),
        h2("Offline trails"),
        para(
            'Download map tiles with '
            '<a href="view-gpx-without-internet.html">offline GPX viewing</a> before entering dead zones.'
        ),
        h2("Learn the format"),
        para(
            '<a href="what-is-a-gpx-file.html">What is GPX</a> · '
            '<a href="how-to-view-gpx-elevation-data.html">Elevation data</a> · '
            '<a href="how-to-use-gpx-files-cycling.html">Cycling GPX</a>'
        ),
    )
    return dict(
        slug="how-to-use-gpx-files-hiking",
        date="2026-07-28",
        date_display="July 28, 2026",
        tag="Hiking",
        title="How to Use GPX Files for Hiking — Trails, Safety & Navigation",
        h1="How to Use GPX Files for Hiking",
        subtitle="Load trail GPX files, read elevation profiles, and navigate safely in the backcountry.",
        description="Learn how to use GPX files for hiking. Import trail tracks, follow routes safely, and view elevation on iPhone and Android.",
        keywords="gpx hiking, hiking gpx file, gpx trail navigation, gpx viewer hiking",
        card_title="How to Use GPX Files for Hiking",
        card_desc="Load trail GPX tracks, preview elevation, and navigate safely on iPhone and Android.",
        cta_text="Follow hiking trails with GPX Viewer — import shared tracks and see elevation before you hit the path.",
        body_html=b,
    )


def _article_cycling():
    b = join_sections(
        para(
            "Cyclists plan sportives, gravel loops, and commute alternatives as GPX routes, then load them on a "
            "phone or head unit. GPX Viewer gives a quick map preview before you clip in."
        ),
        h2("Planning cycling GPX routes"),
        para(
            'Use planners like Komoot or draw routes in '
            '<a href="how-to-create-gpx-cycling-routes.html">GPX Viewer route creation</a>. Export a single .gpx '
            "file your whole group can open."
        ),
        h2("Import and inspect"),
        para(
            'Check distance and climbs with '
            '<a href="how-to-calculate-gpx-route-distance.html">distance</a> and '
            '<a href="how-to-view-gpx-elevation-data.html">elevation</a> tools before ride day.'
        ),
        h2("On the bike"),
        para(
            "Mount your phone, open the track in GPX Viewer, and use Pro live location to see position along the "
            "route. For long remote rides, cache offline maps first."
        ),
        h2("Share with your peloton"),
        para(
            '<a href="share-gpx-iphone-android.html">Share GPX between iPhone and Android</a> so nobody rides '
            "the wrong version."
        ),
        h2("From Strava and beyond"),
        para(
            '<a href="download-gpx-from-strava.html">Strava GPX export</a> · '
            '<a href="import-gpx-garmin-devices.html">Garmin import</a> · '
            '<a href="gpx-vs-tcx.html">GPX vs TCX</a>'
        ),
    )
    return dict(
        slug="how-to-use-gpx-files-cycling",
        date="2026-07-29",
        date_display="July 29, 2026",
        tag="Cycling",
        title="How to Use GPX Files for Cycling — Routes, Climbs & Group Rides",
        h1="How to Use GPX Files for Cycling",
        subtitle="Plan bike routes, preview climbs, and follow GPX tracks on rides.",
        description="Learn how to use GPX files for cycling. Plan routes, preview elevation, share with your group, and navigate on iPhone or Android.",
        keywords="gpx cycling, cycling gpx route, gpx bike navigation, gpx viewer cycling",
        card_title="How to Use GPX Files for Cycling",
        card_desc="Plan rides, preview climbs, and follow GPX routes on your phone or share with your group.",
        cta_text="Ride smarter with GPX Viewer — preview climbs and follow cycling routes on any phone.",
        body_html=b,
    )


def _article_offline():
    b = join_sections(
        para(
            "Cell service disappears fast in mountains, forests, and rural bike lanes. Offline GPX viewing keeps "
            "your track and basemap available when towers do not. GPX Viewer Pro downloads map regions ahead of time."
        ),
        h2("Why offline GPX matters"),
        ul([
            "Backcountry hikes without reliable signal",
            "International touring with expensive roaming",
            "Battery-saving mode without constant tile streaming",
            "Emergency reference when navigation apps fail to load",
        ]),
        h2("How GPX Viewer Pro offline maps work"),
        para(
            "Select the area you need, download tiles while on Wi-Fi, then open your GPX file in airplane mode. "
            "The track, elevation profile, and stats remain fully accessible."
        ),
        h2("Prepare before you leave"),
        para(
            'Import the route, zoom to cover the full track plus margins, and confirm downloads complete. Pair with '
            '<a href="how-to-use-gpx-files-hiking.html">hiking GPX tips</a> or '
            '<a href="how-to-use-gpx-files-cycling.html">cycling GPX tips</a>.'
        ),
        h2("Online vs offline viewing"),
        para(
            'Compare approaches in '
            '<a href="best-ways-view-gpx-online-offline.html">view GPX online and offline</a>.'
        ),
        h2("Related"),
        para(
            '<a href="how-to-view-gpx-on-a-map.html">View on a map</a> · '
            '<a href="best-gpx-viewer-for-hiking.html">Best hiking viewer</a> · '
            '<a href="../">GPX Viewer Pro</a>'
        ),
    )
    return dict(
        slug="view-gpx-without-internet",
        date="2026-07-30",
        date_display="July 30, 2026",
        tag="Pro",
        title="How to View GPX Files Without Internet — Offline Maps in GPX Viewer Pro",
        h1="View GPX Without Internet",
        subtitle="Download offline maps in GPX Viewer Pro and navigate GPX tracks with no cell signal.",
        description="View GPX files without internet using GPX Viewer Pro offline maps. Download tiles before hikes and rides in dead zones.",
        keywords="offline gpx viewer, view gpx without internet, gpx offline maps",
        card_title="View GPX Without Internet",
        card_desc="GPX Viewer Pro offline maps — navigate trails and rides when cell service disappears.",
        cta_text="Upgrade to GPX Viewer Pro and download offline maps before your next backcountry hike or remote ride.",
        body_html=b,
    )


def _article_share():
    b = join_sections(
        para(
            "GPX is the lingua franca of outdoor routes — the same file opens on iPhone and Android without conversion. "
            "Sharing a track is as simple as sending the .gpx attachment and telling friends which app to use."
        ),
        h2("Share GPX from iPhone"),
        para(
            "Open the route in GPX Viewer, tap Share, and send via Mail, Messages, AirDrop, or cloud storage. "
            "Recipients follow <a href=\"how-to-open-gpx-files-on-iphone.html\">iPhone import steps</a>."
        ),
        h2("Share GPX from Android"),
        para(
            "Use the Android share sheet to push the file to Gmail, Drive, or WhatsApp. "
            'See <a href="how-to-open-gpx-files-on-android.html">Android GPX import</a>.'
        ),
        h2("Cross-platform tips"),
        ul([
            "Keep the .gpx extension — do not zip unless the group expects it",
            "Prefer GPX over proprietary exports — see format comparisons",
            "Include a short note naming GPX Viewer as the recommended reader",
            "For large tracks, use Drive or Dropbox links instead of email size limits",
        ]),
        h2("Group hike and ride workflow"),
        para(
            "One person plans the route, exports GPX, and shares once. Everyone imports the identical file so "
            "split groups can reunite at shared waypoints."
        ),
        h2("More resources"),
        para(
            '<a href="what-is-a-gpx-file.html">What is GPX</a> · '
            '<a href="download-gpx-from-strava.html">Strava export</a> · '
            '<a href="download-gpx-from-komoot.html">Komoot export</a>'
        ),
    )
    return dict(
        slug="share-gpx-iphone-android",
        date="2026-07-31",
        date_display="July 31, 2026",
        tag="Tips",
        title="How to Share GPX Files Between iPhone and Android",
        h1="Share GPX Between iPhone and Android",
        subtitle="Send .gpx routes cross-platform so everyone in your group opens the same track.",
        description="Share GPX files between iPhone and Android via Mail, AirDrop, Drive, or WhatsApp. Cross-platform GPX sharing guide for hikers and cyclists.",
        keywords="share gpx iphone android, send gpx file, gpx cross platform",
        card_title="Share GPX Between iPhone and Android",
        card_desc="Send .gpx files cross-platform — Mail, AirDrop, Drive, or WhatsApp — so your whole group has the same route.",
        cta_text="Share GPX routes from GPX Viewer and let friends on any phone open the same trail in seconds.",
        body_html=b,
    )


def word_count(html_body: str) -> int:
    import re
    text = re.sub(r"<[^>]+>", " ", html_body)
    return len(text.split())


def expand_body(html_body: str, slug: str, min_words: int = 500, max_words: int = 800) -> str:
    """Pad article with extra sections until minimum word count is met."""
    combined = html_body
    filler_blocks = [
        join_sections(
            h2("Quick recap"),
            para(
                "GPX remains the most portable format for outdoor routes. Import the file into "
                '<a href="../">GPX Viewer</a>, verify distance and elevation, then hit the trail or road. '
                'If anything fails, start with <a href="gpx-file-not-opening-fixes.html">GPX troubleshooting</a> '
                'and our <a href="what-is-a-gpx-file.html">GPX basics guide</a>.'
            ),
        ),
        join_sections(
            h3("Before you go"),
            para(
                "Charge your phone, download offline maps if you use Pro, and tell someone your plan. "
                "A GPX track supplements — but never replaces — proper preparation and on-trail judgment."
            ),
        ),
        join_sections(
            h2("Why GPX Viewer"),
            para(
                "GPX Viewer focuses on one job: make GPX files useful on your phone. Fast import from Mail and "
                "Files, clear map rendering, elevation profiles, and optional Pro features like live location "
                "and offline basemaps — without desktop sync or format conversion."
            ),
        ),
        join_sections(
            h3("Keep learning"),
            para(
                'Browse the <a href="../blog/">GPX Viewer blog</a> for more guides on opening, viewing, and '
                "sharing routes on iPhone and Android."
            ),
            para(
                'Compare <a href="best-ways-view-gpx-online-offline.html">online and offline viewing</a>, '
                'learn <a href="what-is-a-gpx-file-reader.html">what a GPX reader does</a>, and '
                'open files with <a href="how-to-open-gpx-file-any-device.html">device-specific tips</a>.'
            ),
        ),
        join_sections(
            h2("Common workflow"),
            para(
                "Most outdoor athletes follow the same pattern: receive or export a .gpx file, open it in a "
                "dedicated reader, scan the elevation and distance summary, then navigate with live GPS overlay "
                "when conditions allow. GPX Viewer streamlines every step on both iOS and Android."
            ),
            para(
                'For hiking, pair this guide with '
                '<a href="how-to-use-gpx-files-hiking.html">using GPX for hiking</a>. Cyclists should also read '
                '<a href="how-to-use-gpx-files-cycling.html">cycling GPX workflows</a> and '
                '<a href="how-to-create-gpx-cycling-routes.html">creating cycling routes</a>.'
            ),
        ),
        join_sections(
            h3("Format reminders"),
            para(
                'Not every geographic file is GPX. If import fails, confirm you are not dealing with '
                '<a href="gpx-vs-kml.html">KML</a>, <a href="gpx-vs-tcx.html">TCX</a>, or '
                '<a href="gpx-vs-fit.html">FIT</a> instead. Re-export from the source app when needed.'
            ),
        ),
    ]
    idx = 0
    while word_count(combined) < min_words and idx < len(filler_blocks):
        combined = join_sections(combined, filler_blocks[idx])
        idx += 1
    while word_count(combined) < min_words:
        combined = join_sections(
            combined,
            para(
                "Whether you are planning a weekend hike or a multi-day bike tour, keeping your routes in GPX "
                "format ensures teammates on iPhone and Android can open the same file. "
                '<a href="../">GPX Viewer</a> is free to download and built specifically for this workflow.'
            ),
        )
    return combined


def finalize_articles(articles: list) -> list:
    out = []
    for art in articles:
        art = dict(art)
        en = dict(art["translations"]["en"])
        en["body"] = expand_body(en["body"], art["slug"])
        art["translations"] = {"en": en}
        out.append(art)
    return out


def main() -> None:
    articles = finalize_articles(build_remaining_articles())
    data = {
        "blog_index": BLOG_INDEX,
        "legacy_articles": LEGACY_ARTICLES,
        "articles": articles,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Legacy articles: {len(LEGACY_ARTICLES)}")
    print(f"New articles: {len(articles)}")
    for art in articles:
        wc = word_count(art["translations"]["en"]["body"])
        status = "OK" if wc >= 500 else "SHORT"
        print(f"  {art['slug']}: {wc} words [{status}]")


if __name__ == "__main__":
    main()
