#!/usr/bin/env python3
"""Translate English blog articles to Indonesian (id/blog/)."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
EN_BLOG = ROOT / "blog"
ID_BLOG = ROOT / "id" / "blog"

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

TAG_MAP = {
    "Beginner": "Pemula",
    "iPhone & Android": "iPhone & Android",
    "Android": "Android",
    "Maps": "Peta",
    "Hiking": "Hiking",
    "Cycling": "Bersepeda",
    "Formats": "Format",
    "Troubleshooting": "Pemecahan Masalah",
    "iPhone": "iPhone",
    "Devices": "Perangkat",
    "Pro": "Pro",
    "Tips": "Tips",
}

MONTHS_ID = {
    "January": "Januari", "February": "Februari", "March": "Maret", "April": "April",
    "May": "Mei", "June": "Juni", "July": "Juli", "August": "Agustus",
    "September": "September", "October": "Oktober", "November": "November", "December": "Desember",
}

tr = GoogleTranslator(source="en", target="id")
cache: dict[str, str] = {}


def translate(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    if text in cache:
        return cache[text]
    # Preserve brand / tech tokens
    protected = {}
    tokens = [
        "GPX Viewer Pro", "GPX Viewer", "GPX", "GPS Exchange Format",
        "Google Play", "App Store", "Google Maps", "Apple Maps", "Google Earth",
        "Garmin Connect", "Garmin BaseCamp", "Garmin FIT", "Garmin",
        "Strava", "Komoot", "QGIS", "KML", "TCX", "FIT", "iOS", "Android",
        "iPhone", "WhatsApp", "AirDrop", "Mail", "Files", "Safari", "Drive",
        "Wahoo", "Coros", "Edge", "XML", "ANT+", "DEM",
    ]
    work = text
    for i, tok in enumerate(tokens):
        if tok in work:
            ph = f"__TOK{i}__"
            protected[ph] = tok
            work = work.replace(tok, ph)
    out = work
    for attempt in range(4):
        try:
            result = tr.translate(work)
            if result:
                out = result
                break
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    for ph, tok in protected.items():
        out = out.replace(ph, tok)
    cache[text] = out
    time.sleep(0.15)
    return out


def translate_batch(texts: list[str]) -> list[str]:
    return [translate(t) for t in texts]


def hreflang_block(slug: str) -> str:
    lines = []
    for code in LANG_CODES:
        if code == "en":
            href = f"https://gpxviewerapp.com/blog/{slug}.html"
        else:
            href = f"https://gpxviewerapp.com/{code}/blog/{slug}.html"
        lines.append(f'    <link rel="alternate" hreflang="{code}" href="{href}" />')
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/{slug}.html" />'
    )
    return "\n".join(lines)


def lang_dropdown(slug: str) -> str:
    links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "id" else ""
        if code == "en":
            href = f"/blog/{slug}.html"
        else:
            href = f"/{code}/blog/{slug}.html"
        links.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    return (
        '          <details class="lang-dropdown">\n'
        '            <summary aria-label="Bahasa">ID</summary>\n'
        '            <div class="lang-dropdown-menu" role="navigation" aria-label="Bahasa">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        "          </details>"
    )


def fix_body_html(html: str) -> str:
    html = html.replace('href="../"', 'href="/id/"')
    html = html.replace('href="../blog/"', 'href="/id/blog/"')
    return html


def translate_soup(node: Tag) -> None:
    """Translate text nodes in-place, skip script/style."""
    to_translate: list[NavigableString] = []
    for el in node.descendants:
        if isinstance(el, NavigableString) and el.parent.name not in ("script", "style"):
            txt = str(el)
            if txt.strip():
                to_translate.append(el)
    texts = [str(el).strip() for el in to_translate]
    if not texts:
        return
    translated = translate_batch(texts)
    for el, new in zip(to_translate, translated):
        if not new:
            new = str(el).strip()
        leading = str(el)[: len(str(el)) - len(str(el).lstrip())]
        trailing = str(el)[len(str(el).rstrip()) :]
        el.replace_with(NavigableString(leading + new + trailing))


def parse_en_article(slug: str) -> dict:
    soup = BeautifulSoup((EN_BLOG / f"{slug}.html").read_text(encoding="utf-8"), "html.parser")
    title = soup.title.string.strip() if soup.title else slug
    desc = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        desc = meta_desc.get("content", "")
    keywords = ""
    meta_kw = soup.find("meta", attrs={"name": "keywords"})
    if meta_kw:
        keywords = meta_kw.get("content", "")
    h1 = soup.select_one(".page-header h1")
    h1_text = h1.get_text(strip=True) if h1 else title
    subtitle_el = soup.select_one(".page-header p")
    subtitle = subtitle_el.get_text(strip=True) if subtitle_el else ""
    time_el = soup.select_one("time")
    date_iso = time_el.get("datetime", "2026-07-11") if time_el else "2026-07-11"
    date_display = time_el.get_text(strip=True) if time_el else "11 Juli 2026"
    article = soup.select_one("article.article-content")
    body_parts = []
    cta_title = "Coba GPX Viewer gratis"
    cta_text = ""
    if article:
        for child in article.children:
            if not isinstance(child, Tag):
                continue
            if child.name == "div" and "article-cta" in child.get("class", []):
                h2 = child.find("h2")
                p = child.find("p")
                if h2:
                    cta_title = h2.get_text(strip=True)
                if p:
                    cta_text = p.get_text(strip=True)
                continue
            if child.name == "nav":
                continue
            body_parts.append(str(child))
    body_html = "\n\n          ".join(body_parts)
    return {
        "slug": slug,
        "title": title,
        "description": desc,
        "keywords": keywords,
        "h1": h1_text,
        "subtitle": subtitle,
        "date_iso": date_iso,
        "date_display": date_display,
        "body_html": body_html,
        "cta_title": cta_title,
        "cta_text": cta_text,
    }


def localize_date(display: str) -> str:
    m = re.match(r"(\w+)\s+(\d+),\s+(\d{4})", display)
    if m:
        month, day, year = m.groups()
        return f"{day} {MONTHS_ID.get(month, month)} {year}"
    return display


def render_article(data: dict) -> str:
    slug = data["slug"]
    title = data["title"]
    desc = data["description"]
    keywords = data["keywords"]
    h1 = data["h1"]
    subtitle = data["subtitle"]
    date_iso = data["date_iso"]
    date_display = data["date_display"]
    body = data["body_html"]
    cta_title = data["cta_title"]
    cta_text = data["cta_text"]
    canonical = f"https://gpxviewerapp.com/id/blog/{slug}.html"

    return f"""<!DOCTYPE html>
<html lang="id">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta
      name="description"
      content="{desc}"
    />
    <meta
      name="keywords"
      content="{keywords}"
    />
    <link rel="canonical" href="{canonical}" />
{hreflang_block(slug)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:title" content="{title}" />
    <meta
      property="og:description"
      content="{desc}"
    />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="id_ID" />
    <link rel="icon" href="../../images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="../../css/style.css?v=2" />
    <link rel="stylesheet" href="../../css/lang.css?v=5" />
<link rel="stylesheet" href="../../css/blog.css" />
    <script src="../../js/config.js"></script>
    <script src="../../js/seo.js"></script>
    <script src="../../js/analytics.js"></script>
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": {json.dumps(h1)},
        "datePublished": "{date_iso}",
        "inLanguage": "id",
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
        <a class="brand" href="/id/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/id/#features">Fitur</a>
          <a href="/id/blog/">Blog</a>
          <a href="/id/#pricing">Pro</a>
          {lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Unduh di App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Dapatkan di Google Play" />
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
          <p class="article-meta"><time datetime="{date_iso}">{date_display}</time></p>

          {body}

          <div class="article-cta">
            <h2>{cta_title}</h2>
            <p>{cta_text}</p>
            <div class="store-badges">
              <a class="store-badge app-store-link" href="#" data-location="article_cta">
                <img src="../../images/app-store-badge-white.svg" alt="Unduh di App Store" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="Dapatkan di Google Play" />
              </a>
            </div>
          </div>

          <nav class="article-nav">
            <a href="/id/blog/">← Kembali ke semua panduan</a>
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
          <a href="/id/">Beranda</a>
          <a href="/id/privacy.html">Privasi</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Kontak</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def translate_article(slug: str) -> dict:
    raw = parse_en_article(slug)
    fields = ["title", "description", "keywords", "h1", "subtitle", "cta_title", "cta_text"]
    for f in fields:
        raw[f] = translate(raw[f])
    raw["date_display"] = localize_date(raw["date_display"])
    body_soup = BeautifulSoup(raw["body_html"], "html.parser")
    translate_soup(body_soup)
    raw["body_html"] = fix_body_html(str(body_soup))
    return raw


def parse_en_index_cards() -> list[dict]:
    soup = BeautifulSoup((EN_BLOG / "index.html").read_text(encoding="utf-8"), "html.parser")
    cards = []
    for art in soup.select("article.blog-card"):
        tag = art.select_one(".blog-tag").get_text(strip=True)
        title = art.select_one("h2 a").get_text(strip=True)
        desc = art.select_one("p").get_text(strip=True)
        href = art.select_one("h2 a").get("href", "")
        slug = href.replace(".html", "")
        cards.append({"slug": slug, "tag_en": tag, "title": title, "desc": desc})
    return cards


def render_index(all_cards: list[dict]) -> str:
    existing_slugs = {
        "what-is-a-gpx-file",
        "how-to-open-gpx-files-on-iphone",
        "how-to-view-gpx-on-a-map",
        "best-gpx-viewer-for-hiking",
        "how-to-create-gpx-cycling-routes",
    }
    # Keep existing 5 card text from current id index
    id_index = BeautifulSoup((ID_BLOG / "index.html").read_text(encoding="utf-8"), "html.parser")
    kept = {}
    for art in id_index.select("article.blog-card"):
        href = art.select_one("h2 a").get("href", "")
        slug = href.replace(".html", "")
        kept[slug] = {
            "tag": art.select_one(".blog-tag").get_text(strip=True),
            "title": art.select_one("h2 a").get_text(strip=True),
            "desc": art.select_one("p").get_text(strip=True),
        }

    card_html = []
    for card in all_cards:
        slug = card["slug"]
        if slug in kept:
            t = kept[slug]
        else:
            t = {
                "tag": TAG_MAP.get(card["tag_en"], translate(card["tag_en"])),
                "title": translate(card["title"]),
                "desc": translate(card["desc"]),
            }
        card_html.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{t['tag']}</span>
            <h2><a href="{slug}.html">{t['title']}</a></h2>
            <p>{t['desc']}</p>
            <a class="blog-read-more" href="{slug}.html">Baca panduan →</a>
          </article>"""
        )

    hreflang = "\n".join(
        [
            '    <link rel="alternate" hreflang="en" href="https://gpxviewerapp.com/blog/index.html" />',
            '    <link rel="alternate" hreflang="de" href="https://gpxviewerapp.com/de/blog/index.html" />',
            '    <link rel="alternate" hreflang="fr" href="https://gpxviewerapp.com/fr/blog/index.html" />',
            '    <link rel="alternate" hreflang="it" href="https://gpxviewerapp.com/it/blog/index.html" />',
            '    <link rel="alternate" hreflang="pt" href="https://gpxviewerapp.com/pt/blog/index.html" />',
            '    <link rel="alternate" hreflang="es" href="https://gpxviewerapp.com/es/blog/index.html" />',
            '    <link rel="alternate" hreflang="nl" href="https://gpxviewerapp.com/nl/blog/index.html" />',
            '    <link rel="alternate" hreflang="pl" href="https://gpxviewerapp.com/pl/blog/index.html" />',
            '    <link rel="alternate" hreflang="id" href="https://gpxviewerapp.com/id/blog/index.html" />',
            '    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/index.html" />',
        ]
    )

    dropdown = "\n".join(
        [
            '              <a href="/blog/index.html" hreflang="en" title="English">EN</a>',
            '              <a href="/de/blog/index.html" hreflang="de" title="Deutsch">DE</a>',
            '              <a href="/fr/blog/index.html" hreflang="fr" title="Français">FR</a>',
            '              <a href="/it/blog/index.html" hreflang="it" title="Italiano">IT</a>',
            '              <a href="/pt/blog/index.html" hreflang="pt" title="Português">PT</a>',
            '              <a href="/es/blog/index.html" hreflang="es" title="Español">ES</a>',
            '              <a href="/nl/blog/index.html" hreflang="nl" title="Nederlands">NL</a>',
            '              <a href="/pl/blog/index.html" hreflang="pl" title="Polski">PL</a>',
            '              <a href="/id/blog/index.html" hreflang="id" title="Indonesia" class="is-active">ID</a>',
        ]
    )

    return f"""<!DOCTYPE html>
<html lang="id">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GPX Viewer Blog — Panduan GPX untuk Hiking, Bersepeda & Navigasi</title>
    <meta
      name="description"
      content="Pelajari cara membuka file GPX, melihat rute di peta, mengikuti jalur hiking, dan membuat track bersepeda. Panduan gratis dari tim GPX Viewer."
    />
    <meta
      name="keywords"
      content="panduan file GPX, buka GPX iPhone, penampil peta GPX, hiking GPX, rute bersepeda GPX"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/id/blog/" />
{hreflang}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/id/blog/" />
    <meta property="og:title" content="GPX Viewer Blog — Panduan & Tips" />
    <meta property="og:description" content="Pelajari cara membuka file GPX, melihat rute di peta, dan mengikuti jalur hiking." />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="id_ID" />
    <link rel="icon" href="../../images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="../../css/style.css?v=2" />
    <link rel="stylesheet" href="../../css/lang.css?v=5" />
<link rel="stylesheet" href="../../css/blog.css" />
    <script src="../../js/config.js"></script>
    <script src="../../js/seo.js"></script>
    <script src="../../js/analytics.js"></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container">
        <a class="brand" href="/id/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/id/#features">Fitur</a>
          <a href="/id/blog/">Blog</a>
          <a href="/id/#pricing">Pro</a>
          <details class="lang-dropdown">
            <summary aria-label="Bahasa">ID</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="Bahasa">
{dropdown}
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Unduh di App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Dapatkan di Google Play" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>GPX Viewer Blog</h1>
        <p>Panduan untuk membuka, melihat, dan menavigasi file GPX di iPhone dan Android.</p>
      </div>
    </div>

    <main class="blog-index">
      <div class="container">
        <div class="blog-grid">
{chr(10).join(card_html)}
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
          <a href="/id/">Beranda</a>
          <a href="/id/privacy.html">Privasi</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Kontak</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def main() -> None:
    written = 0
    for slug in SLUGS:
        print(f"Translating {slug}...", flush=True)
        data = translate_article(slug)
        out = ID_BLOG / f"{slug}.html"
        out.write_text(render_article(data), encoding="utf-8")
        written += 1
        print(f"  Wrote {out.name}")

    cards = parse_en_index_cards()
    index_path = ID_BLOG / "index.html"
    index_path.write_text(render_index(cards), encoding="utf-8")
    written += 1
    print(f"Wrote index.html with {len(cards)} cards")
    print(f"Total files written: {written}")


if __name__ == "__main__":
    main()
