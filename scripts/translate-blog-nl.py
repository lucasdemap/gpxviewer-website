#!/usr/bin/env python3
"""Translate English blog articles to Dutch and update nl/blog/index.html."""

from __future__ import annotations

import html
import re
import time
from pathlib import Path

try:
    from bs4 import BeautifulSoup, NavigableString
    from deep_translator import GoogleTranslator
except ImportError:
    raise SystemExit("Run: pip install beautifulsoup4 deep-translator")

ROOT = Path(__file__).resolve().parent.parent
EN_BLOG = ROOT / "blog"
NL_BLOG = ROOT / "nl" / "blog"

SLUGS = [
    "what-is-a-gpx-file-reader",
    "how-to-open-gpx-files-on-android",
    "how-to-open-gpx-file-any-device",
    "best-ways-view-gpx-online-offline",
    "gpx-file-not-opening-fixes",
    "gpx-file-format-tracks-routes-waypoints",
    "gpx-vs-kml",
    "gpx-vs-tcx",
    "gpx-vs-fit",
    "how-to-view-gpx-elevation-data",
    "how-to-calculate-gpx-route-distance",
    "how-to-import-gpx-google-maps",
    "open-gpx-files-apple-maps",
    "download-gpx-from-strava",
    "download-gpx-from-komoot",
    "import-gpx-garmin-devices",
    "how-to-use-gpx-files-hiking",
    "how-to-use-gpx-files-cycling",
    "view-gpx-without-internet",
    "share-gpx-iphone-android",
]

LANG_CODES = ["en", "de", "fr", "it", "pt", "es", "nl", "pl", "id"]
LANG_LABELS = {
    "en": "English", "de": "Deutsch", "fr": "Français", "it": "Italiano",
    "pt": "Português", "es": "Español", "nl": "Nederlands", "pl": "Polski", "id": "Indonesia",
}

MONTHS_NL = {
    "January": "januari", "February": "februari", "March": "maart", "April": "april",
    "May": "mei", "June": "juni", "July": "juli", "August": "augustus",
    "September": "september", "October": "oktober", "November": "november", "December": "december",
}

SKIP_TAGS = {"script", "style", "code"}

PROTECT = [
    "GPX Viewer", "GPX Viewer Pro", "GPX", "GPS Exchange Format",
    "Garmin Connect", "Garmin BaseCamp", "Google Earth", "Google Maps", "Google My Maps",
    "Google Play", "App Store", "Apple Maps", "Strava", "Komoot", "Garmin", "Wahoo", "Coros",
    "QGIS", "KML", "TCX", "FIT", "XML", "iOS", "Android", "iPhone", "AirDrop", "WhatsApp",
    "Gmail", "Drive", "Mail", "Files", "Safari", "Edge", "lucas@streiv.app",
    ".gpx", ".kml", ".tcx", ".fit", ".xml",
]

tr = GoogleTranslator(source="en", target="nl")
_cache: dict[str, str] = {}


def protect_text(s: str) -> tuple[str, dict[str, str]]:
    repl: dict[str, str] = {}
    for i, token in enumerate(PROTECT):
        if token in s:
            ph = f"__P{i}__"
            repl[ph] = token
            s = s.replace(token, ph)
    return s, repl


def restore_text(s: str, repl: dict[str, str]) -> str:
    for ph, token in repl.items():
        s = s.replace(ph, token)
    return s


def translate(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    if text in _cache:
        return _cache[text]
    protected, repl = protect_text(text)
    for attempt in range(4):
        try:
            out = tr.translate(protected)
            result = restore_text(out, repl)
            _cache[text] = result
            time.sleep(0.15)
            return result
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    _cache[text] = text
    return text


def translate_batch(texts: list[str]) -> list[str]:
    return [translate(t) for t in texts]


def nl_date(en_date: str) -> str:
    m = re.match(r"(\w+)\s+(\d+),\s+(\d{4})", en_date)
    if not m:
        return en_date
    month, day, year = m.group(1), m.group(2), m.group(3)
    return f"{int(day)} {MONTHS_NL.get(month, month.lower())} {year}"


def fix_nl_links(fragment: str) -> str:
    fragment = fragment.replace('href="../blog/"', 'href="/nl/blog/"')
    fragment = fragment.replace('href="../"', 'href="/nl/"')
    fragment = fragment.replace('href="../#features"', 'href="/nl/#features"')
    fragment = fragment.replace('href="../#pricing"', 'href="/nl/#pricing"')
    fragment = fragment.replace('href="../privacy.html"', 'href="/nl/privacy.html"')
    return fragment


def translate_html_body(fragment: str) -> str:
    soup = BeautifulSoup(fragment, "html.parser")
    strings = []
    nodes = []
    for node in soup.descendants:
        if isinstance(node, NavigableString):
            parent = node.parent.name if node.parent else ""
            if parent in SKIP_TAGS:
                continue
            text = str(node)
            if text.strip():
                strings.append(text)
                nodes.append(node)
    if strings:
        translated = translate_batch(strings)
        for node, new_text in zip(nodes, translated):
            if new_text is None:
                continue
            node.replace_with(new_text)
    return fix_nl_links(str(soup))


def hreflang_block(slug: str) -> str:
    lines = []
    for code in LANG_CODES:
        if code == "en":
            href = f"https://gpxviewerapp.com/blog/{slug}.html"
        else:
            href = f"https://gpxviewerapp.com/{code}/blog/{slug}.html"
        lines.append(f'    <link rel="alternate" hreflang="{code}" href="{href}" />')
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/{slug}.html" />')
    return "\n".join(lines)


def lang_dropdown(slug: str) -> str:
    links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "nl" else ""
        if code == "en":
            href = f"/blog/{slug}.html"
        else:
            href = f"/{code}/blog/{slug}.html"
        links.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    return (
        '          <details class="lang-dropdown">\n'
        '            <summary aria-label="Taal">NL</summary>\n'
        '            <div class="lang-dropdown-menu" role="navigation" aria-label="Taal">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        "          </details>"
    )


def parse_en_article(slug: str) -> dict:
    raw = (EN_BLOG / f"{slug}.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.string.strip() if soup.title else slug
    desc = ""
    keywords = ""
    for meta in soup.find_all("meta"):
        name = meta.get("name", "")
        if name == "description":
            desc = meta.get("content", "")
        elif name == "keywords":
            keywords = meta.get("content", "")
    h1 = soup.select_one(".page-header h1")
    subtitle = soup.select_one(".page-header p")
    h1_text = h1.get_text(strip=True) if h1 else title
    sub_text = subtitle.get_text(strip=True) if subtitle else ""
    time_el = soup.select_one(".article-meta time")
    date_iso = time_el.get("datetime", "2026-07-11") if time_el else "2026-07-11"
    date_display = time_el.get_text(strip=True) if time_el else "July 11, 2026"
    article = soup.select_one("article.article-content")
    body_parts = []
    cta_title = "Try GPX Viewer free"
    cta_text = ""
    if article:
        for child in article.children:
            if getattr(child, "name", None) == "div" and "article-cta" in child.get("class", []):
                h2 = child.find("h2")
                p = child.find("p")
                if h2:
                    cta_title = h2.get_text(strip=True)
                if p:
                    cta_text = p.get_text(strip=True)
                break
            if getattr(child, "name", None) == "nav":
                break
            if getattr(child, "name", None):
                body_parts.append(str(child))
    body_html = "\n          ".join(body_parts).strip()
    ld = soup.find("script", type="application/ld+json")
    ld_headline = h1_text
    if ld and ld.string:
        m = re.search(r'"headline":\s*"([^"]+)"', ld.string)
        if m:
            ld_headline = m.group(1)
    return {
        "slug": slug,
        "title": title,
        "description": desc,
        "keywords": keywords,
        "h1": h1_text,
        "subtitle": sub_text,
        "date_iso": date_iso,
        "date_display": date_display,
        "body_html": body_html,
        "cta_title": cta_title,
        "cta_text": cta_text,
        "ld_headline": ld_headline,
    }


def render_nl_article(data: dict) -> str:
    slug = data["slug"]
    title = html.escape(translate(data["title"]))
    desc = html.escape(translate(data["description"]))
    keywords = html.escape(translate(data["keywords"]))
    h1 = html.escape(translate(data["h1"]))
    subtitle = html.escape(translate(data["subtitle"]))
    ld_headline = html.escape(translate(data["ld_headline"]))
    date_iso = data["date_iso"]
    date_nl = nl_date(data["date_display"])
    body = translate_html_body(data["body_html"])
    cta_title = html.escape(translate(data["cta_title"]))
    cta_text = html.escape(translate(data["cta_text"]))
    canonical = f"https://gpxviewerapp.com/nl/blog/{slug}.html"

    return f"""<!DOCTYPE html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta name="keywords" content="{keywords}" />
    <link rel="canonical" href="{canonical}" />
{hreflang_block(slug)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="nl_NL" />
    <link rel="icon" href="../../images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="../../css/style.css?v=3" />
    <link rel="stylesheet" href="../../css/lang.css?v=5" />
<link rel="stylesheet" href="../../css/blog.css" />
    <script src="../../js/config.js"></script>
    <script src="../../js/seo.js"></script>
    <script src="../../js/analytics.js"></script>
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{ld_headline}",
        "datePublished": "{date_iso}",
        "inLanguage": "nl",
        "author": {{
          "@type": "Person",
          "name": "GPX Viewer"
        }},
        "image": "https://gpxviewerapp.com/images/og-image.jpg",
        "publisher": {{
          "@type": "Organization",
          "name": "GPX Viewer",
          "logo": {{
            "@type": "ImageObject",
            "url": "https://gpxviewerapp.com/images/app-icon.png"
          }}
        }}
      }}
    </script>
  </head>
  <body>
    <header class="site-header">
      <div class="container">
        <a class="brand" href="/nl/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/nl/#features">Functies</a>
          <a href="/nl/blog/">Blog</a>
          <a href="/nl/#pricing">Pro</a>
          {lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Download in de App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Downloaden via Google Play" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>{h1}</h1>
        <p>{subtitle}</p>
      </div>
    </div>

    <main class="article-page">
      <div class="container article-layout">
        <article class="article-content">
          <p class="article-meta"><time datetime="{date_iso}">{date_nl}</time></p>

          {body}

          <div class="article-cta">
            <h2>{cta_title}</h2>
            <p>{cta_text}</p>
            <div class="store-badges">
              <a class="store-badge app-store-link" href="#" data-location="article_cta">
                <img src="../../images/app-store-badge-white.svg" alt="Download in de App Store" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="Downloaden via Google Play" />
              </a>
            </div>
          </div>

          <nav class="article-nav">
            <a href="/nl/blog/">← Terug naar alle gidsen</a>
          </nav>
        </article>
      </div>
    </main>

    <footer class="site-footer">
      <div class="container">
        <span class="footer-brand">
          <img src="../../images/app-icon.png" alt="" width="28" height="28" />
          © <span id="year"></span> GPX Viewer
        </span>
        <div class="footer-links">
          <a href="/nl/">Startpagina</a>
          <a href="/nl/privacy.html">Privacy</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Contact</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
    <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


# Existing 5 Dutch cards (keep as-is)
EXISTING_CARDS = """          <article class="blog-card">
            <span class="blog-tag">Beginner</span>
            <h2><a href="what-is-a-gpx-file.html">Wat is een GPX-bestand? De complete gids voor wandelaars &amp; fietsers</a></h2>
            <p>Leer wat GPX-bestanden zijn, hoe GPS-tracks werken en waarom GPX Viewer het .gpx-formaat gebruikt.</p>
            <a class="blog-read-more" href="what-is-a-gpx-file.html">Lees gids →</a>
          </article>
          <article class="blog-card">
            <span class="blog-tag">iPhone &amp; Android</span>
            <h2><a href="how-to-open-gpx-files-on-iphone.html">GPX-bestanden openen op iPhone en Android</a></h2>
            <p>Stap voor stap: GPX importeren vanuit Mail, Bestanden of Safari in GPX Viewer.</p>
            <a class="blog-read-more" href="how-to-open-gpx-files-on-iphone.html">Lees gids →</a>
          </article>
          <article class="blog-card">
            <span class="blog-tag">Kaarten</span>
            <h2><a href="how-to-view-gpx-on-a-map.html">GPX-routes bekijken op een kaart</a></h2>
            <p>Bekijk waypoints, hoogte en afstand op interactieve kaarten — standaard, satelliet en hybride.</p>
            <a class="blog-read-more" href="how-to-view-gpx-on-a-map.html">Lees gids →</a>
          </article>
          <article class="blog-card">
            <span class="blog-tag">Wandelen</span>
            <h2><a href="best-gpx-viewer-for-hiking.html">Beste GPX-viewer voor wandelen: wandelpaden volgen met GPS-tracks</a></h2>
            <p>Waarom wandelaars GPX-bestanden gebruiken, hoe je routes veilig volgt en waar je op moet letten in een GPX-app.</p>
            <a class="blog-read-more" href="best-gpx-viewer-for-hiking.html">Lees gids →</a>
          </article>
          <article class="blog-card">
            <span class="blog-tag">Fietsen</span>
            <h2><a href="how-to-create-gpx-cycling-routes.html">GPX-fietsroutes maken en exporteren</a></h2>
            <p>Plan fietsroutes, sla GPX-tracks op en deel ritten met vrienden of je fietscomputer.</p>
            <a class="blog-read-more" href="how-to-create-gpx-cycling-routes.html">Lees gids →</a>
          </article>"""

NEW_CARD_SPECS = [
    ("Beginner", "What Is a GPX File Reader?", "Learn how GPX readers parse tracks, routes, and waypoints — and why GPX Viewer is the easiest way to read .gpx files on your phone.", "what-is-a-gpx-file-reader"),
    ("Android", "How to Open GPX Files on Android", "Import GPX from Gmail, Drive, or Downloads into GPX Viewer — the fastest Android GPX viewer.", "how-to-open-gpx-files-on-android"),
    ("Beginner", "How to Open a GPX File on Any Device", "Phones, desktops, and GPS units — discover what opens .gpx files and the fastest way to view routes.", "how-to-open-gpx-file-any-device"),
    ("Maps", "Best Ways to View GPX Online and Offline", "Web tools vs mobile apps — find the best way to view GPX routes with or without internet.", "best-ways-view-gpx-online-offline"),
    ("Troubleshooting", "GPX File Not Opening? Fixes and Troubleshooting", "Wrong format, bad download, or missing app — fix GPX files that refuse to open on your phone.", "gpx-file-not-opening-fixes"),
    ("Beginner", "GPX Tracks, Routes, and Waypoints", "Tracks, routes, and waypoints — understand the building blocks of every .gpx file.", "gpx-file-format-tracks-routes-waypoints"),
    ("Formats", "GPX vs KML: Which Format to Use?", "GPX vs KML for trails and rides — which format fits hiking, cycling, and GPS devices?", "gpx-vs-kml"),
    ("Formats", "GPX vs TCX for Cyclists and Hikers", "Training Center XML vs GPS Exchange Format — pick the right export for sharing and navigation.", "gpx-vs-tcx"),
    ("Formats", "GPX vs FIT: Routes vs Activity Files", "Garmin FIT vs GPX — when to use binary activity files and when to share open .gpx routes.", "gpx-vs-fit"),
    ("Maps", "How to View GPX Elevation Data", "Climb profiles, total ascent, and altitude stats — read elevation from any GPX track.", "how-to-view-gpx-elevation-data"),
    ("Maps", "How to Calculate GPX Route Distance", "Measure true trail distance from GPS points — not straight-line map guesses.", "how-to-calculate-gpx-route-distance"),
    ("Maps", "How to Import GPX into Google Maps", "Google My Maps on desktop — plus a faster way to navigate GPX on your phone.", "how-to-import-gpx-google-maps"),
    ("iPhone", "Open GPX on iPhone — Beyond Apple Maps", "Apple Maps won't import GPX — use GPX Viewer for trail and cycling navigation on iPhone.", "open-gpx-files-apple-maps"),
    ("Cycling", "Download GPX from Strava", "Export Strava activities as GPX, then view routes with maps and elevation in GPX Viewer.", "download-gpx-from-strava"),
    ("Hiking", "Download GPX from Komoot", "Export Komoot hiking and cycling tours as GPX, then navigate with GPX Viewer on your phone.", "download-gpx-from-komoot"),
    ("Devices", "Import GPX to Garmin Devices", "Upload GPX to Garmin Connect and preview courses in GPX Viewer before syncing to your watch.", "import-gpx-garmin-devices"),
    ("Hiking", "How to Use GPX Files for Hiking", "Load trail GPX tracks, preview elevation, and navigate safely on iPhone and Android.", "how-to-use-gpx-files-hiking"),
    ("Cycling", "How to Use GPX Files for Cycling", "Plan rides, preview climbs, and follow GPX routes on your phone or share with your group.", "how-to-use-gpx-files-cycling"),
    ("Pro", "View GPX Without Internet", "GPX Viewer Pro offline maps — navigate trails and rides when cell service disappears.", "view-gpx-without-internet"),
    ("Tips", "Share GPX Between iPhone and Android", "Send .gpx files cross-platform — Mail, AirDrop, Drive, or WhatsApp — so your whole group has the same route.", "share-gpx-iphone-android"),
]

TAG_MAP = {
    "Beginner": "Beginner",
    "Android": "Android",
    "Maps": "Kaarten",
    "Troubleshooting": "Probleemoplossing",
    "Formats": "Formaten",
    "iPhone": "iPhone",
    "Cycling": "Fietsen",
    "Hiking": "Wandelen",
    "Devices": "Apparaten",
    "Pro": "Pro",
    "Tips": "Tips",
}


def build_new_cards() -> str:
    cards = []
    for tag_en, title, desc, slug in NEW_CARD_SPECS:
        tag_nl = TAG_MAP.get(tag_en, translate(tag_en))
        title_nl = translate(title)
        desc_nl = translate(desc)
        cards.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{html.escape(tag_nl)}</span>
            <h2><a href="{slug}.html">{html.escape(title_nl)}</a></h2>
            <p>{html.escape(desc_nl)}</p>
            <a class="blog-read-more" href="{slug}.html">Lees gids →</a>
          </article>"""
        )
    return "\n".join(cards)


def render_index(new_cards: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GPX Viewer Blog — GPX-gidsen voor wandelen, fietsen &amp; navigatie</title>
    <meta
      name="description"
      content="Leer hoe je GPX-bestanden opent, routes op een kaart bekijkt, wandelpaden volgt en fiets-tracks maakt. Gratis gidsen van het GPX Viewer-team."
    />
    <meta
      name="keywords"
      content="GPX-bestand gids, GPX openen iPhone, GPX-kaartviewer, wandelen GPX, fietsroutes GPX"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/nl/blog/" />
    <link rel="alternate" hreflang="en" href="https://gpxviewerapp.com/blog/index.html" />
    <link rel="alternate" hreflang="de" href="https://gpxviewerapp.com/de/blog/index.html" />
    <link rel="alternate" hreflang="fr" href="https://gpxviewerapp.com/fr/blog/index.html" />
    <link rel="alternate" hreflang="it" href="https://gpxviewerapp.com/it/blog/index.html" />
    <link rel="alternate" hreflang="pt" href="https://gpxviewerapp.com/pt/blog/index.html" />
    <link rel="alternate" hreflang="es" href="https://gpxviewerapp.com/es/blog/index.html" />
    <link rel="alternate" hreflang="nl" href="https://gpxviewerapp.com/nl/blog/index.html" />
    <link rel="alternate" hreflang="pl" href="https://gpxviewerapp.com/pl/blog/index.html" />
    <link rel="alternate" hreflang="id" href="https://gpxviewerapp.com/id/blog/index.html" />
    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/index.html" />
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/nl/blog/" />
    <meta property="og:title" content="GPX Viewer Blog — Gidsen &amp; tips" />
    <meta property="og:description" content="Leer hoe je GPX-bestanden opent, routes op een kaart bekijkt en wandelpaden volgt." />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="nl_NL" />
    <link rel="icon" href="../../images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="../../css/style.css?v=3" />
    <link rel="stylesheet" href="../../css/lang.css?v=5" />
<link rel="stylesheet" href="../../css/blog.css" />
    <script src="../../js/config.js"></script>
    <script src="../../js/seo.js"></script>
    <script src="../../js/analytics.js"></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container">
        <a class="brand" href="/nl/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/nl/#features">Functies</a>
          <a href="/nl/blog/">Blog</a>
          <a href="/nl/#pricing">Pro</a>
          <details class="lang-dropdown">
            <summary aria-label="Taal">NL</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="Taal">
              <a href="/blog/index.html" hreflang="en" title="English">EN</a>
              <a href="/de/blog/index.html" hreflang="de" title="Deutsch">DE</a>
              <a href="/fr/blog/index.html" hreflang="fr" title="Français">FR</a>
              <a href="/it/blog/index.html" hreflang="it" title="Italiano">IT</a>
              <a href="/pt/blog/index.html" hreflang="pt" title="Português">PT</a>
              <a href="/es/blog/index.html" hreflang="es" title="Español">ES</a>
              <a href="/nl/blog/index.html" hreflang="nl" title="Nederlands" class="is-active">NL</a>
              <a href="/pl/blog/index.html" hreflang="pl" title="Polski">PL</a>
              <a href="/id/blog/index.html" hreflang="id" title="Indonesia">ID</a>
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Download in de App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Downloaden via Google Play" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>GPX Viewer Blog</h1>
        <p>Gidsen om GPX-bestanden te openen, bekijken en navigeren op iPhone en Android.</p>
      </div>
    </div>

    <main class="blog-index">
      <div class="container">
        <div class="blog-grid">
{EXISTING_CARDS}
{new_cards}
        </div>
      </div>
    </main>

    <footer class="site-footer">
      <div class="container">
        <span class="footer-brand">
          <img src="../../images/app-icon.png" alt="" width="28" height="28" />
          © <span id="year"></span> GPX Viewer
        </span>
        <div class="footer-links">
          <a href="/nl/">Startpagina</a>
          <a href="/nl/privacy.html">Privacy</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Contact</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def main() -> None:
    NL_BLOG.mkdir(parents=True, exist_ok=True)
    written = 0
    for i, slug in enumerate(SLUGS, 1):
        print(f"[{i}/{len(SLUGS)}] {slug}", flush=True)
        data = parse_en_article(slug)
        out = NL_BLOG / f"{slug}.html"
        out.write_text(render_nl_article(data), encoding="utf-8")
        written += 1
        print(f"  wrote {out.relative_to(ROOT)}", flush=True)

    new_cards = build_new_cards()
    index_path = NL_BLOG / "index.html"
    index_path.write_text(render_index(new_cards), encoding="utf-8")
    written += 1
    print(f"Wrote {index_path.relative_to(ROOT)} (25 cards)")
    print(f"Total files written: {written}")


if __name__ == "__main__":
    main()
