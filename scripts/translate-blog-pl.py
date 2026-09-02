#!/usr/bin/env python3
"""Translate English blog articles to Polish."""

from __future__ import annotations

import html
import json
import re
import sys
import time
from pathlib import Path

try:
    from bs4 import BeautifulSoup, NavigableString
    from deep_translator import GoogleTranslator
except ImportError:
    print("Run: pip install beautifulsoup4 deep-translator")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
BLOG_EN = ROOT / "blog"
BLOG_PL = ROOT / "pl" / "blog"

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

MONTHS_PL = {
    "January": "stycznia", "February": "lutego", "March": "marca", "April": "kwietnia",
    "May": "maja", "June": "czerwca", "July": "lipca", "August": "sierpnia",
    "September": "września", "October": "października", "November": "listopada", "December": "grudnia",
}

PROTECT = [
    "GPX Viewer Pro", "GPX Viewer", "GPS Exchange Format",
    "Garmin Connect", "Garmin BaseCamp", "Google Earth", "Google Maps", "Google My Maps",
    "Google Play", "App Store", "Apple Maps", "Komoot", "Strava", "Garmin", "QGIS",
    "WhatsApp", "AirDrop", "Mail", "Files", "Safari", "Drive", "Gmail", "Downloads",
    "Notepad", "TextEdit", "iOS", "Android", "iPhone", "XML", "KML", "TCX", "FIT",
    "Training Center XML", "lucas@streiv.app",
]

tr = GoogleTranslator(source="en", target="pl")
_cache: dict[str, str] = {}


def protect_text(s: str) -> tuple[str, dict[str, str]]:
    repl: dict[str, str] = {}
    out = s
    for i, token in enumerate(PROTECT):
        if token in out:
            ph = f"__PROT{i}__"
            repl[ph] = token
            out = out.replace(token, ph)
    if ".gpx" in out:
        out = out.replace(".gpx", "__DOTGPX__")
        repl["__DOTGPX__"] = ".gpx"
    if ".xml" in out:
        out = out.replace(".xml", "__DOTXML__")
        repl["__DOTXML__"] = ".xml"
    return out, repl


def restore_text(s: str, repl: dict[str, str]) -> str:
    for ph, token in repl.items():
        s = s.replace(ph, token)
    return s


def translate(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    if s in _cache:
        return _cache[s]
    protected, repl = protect_text(s)
    stripped = protected
    for ph in repl:
        stripped = stripped.replace(ph, "")
    if not stripped.strip() or re.fullmatch(r"[\W\d_]+", stripped.strip()):
        _cache[s] = s
        return s
    for attempt in range(4):
        try:
            out = tr.translate(protected)
            result = restore_text(out, repl)
            _cache[s] = result
            time.sleep(0.15)
            return result
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    _cache[s] = s
    return s


def translate_batch(texts: list[str]) -> list[str]:
    return [translate(t) for t in texts]


def pl_date(en_display: str, iso: str) -> str:
    m = re.match(r"(\w+)\s+(\d{1,2}),\s+(\d{4})", en_display.strip())
    if m:
        month, day, year = m.group(1), m.group(2), m.group(3)
        pl_month = MONTHS_PL.get(month, month.lower())
        return f"{day} {pl_month} {year}"
    return en_display


def translate_node(node) -> None:
    if isinstance(node, NavigableString):
        text = str(node)
        if text.strip():
            node.replace_with(translate(text))
        return
    if node.name in ("script", "style"):
        return
    for child in list(node.children):
        translate_node(child)


def fix_pl_links(soup: BeautifulSoup) -> None:
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href in ("../", "/"):
            a["href"] = "/pl/"
        elif href == "../blog/":
            a["href"] = "/pl/blog/"


def extract_article(en_path: Path) -> dict:
    raw = en_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    desc = ""
    keywords = ""
    for meta in soup.find_all("meta"):
        name = meta.get("name", "")
        prop = meta.get("property", "")
        if name == "description":
            desc = meta.get("content", "")
        elif name == "keywords":
            keywords = meta.get("content", "")

    og_title = ""
    og_desc = ""
    for meta in soup.find_all("meta"):
        if meta.get("property") == "og:title":
            og_title = meta.get("content", "")
        elif meta.get("property") == "og:description":
            og_desc = meta.get("content", "")

    ld = soup.find("script", type="application/ld+json")
    headline = ""
    date_iso = "2026-07-11"
    if ld and ld.string:
        try:
            data = json.loads(ld.string)
            headline = data.get("headline", "")
            date_iso = data.get("datePublished", date_iso)
        except json.JSONDecodeError:
            pass

    h1_el = soup.select_one(".page-header h1")
    h1 = h1_el.get_text(strip=True) if h1_el else headline
    sub_el = soup.select_one(".page-header p")
    subtitle = sub_el.get_text(strip=True) if sub_el else ""

    time_el = soup.select_one(".article-meta time")
    date_display = time_el.get_text(strip=True) if time_el else "July 11, 2026"
    if time_el and time_el.get("datetime"):
        date_iso = time_el["datetime"]

    article = soup.select_one(".article-content")
    body_parts = []
    cta_title = "Wypróbuj GPX Viewer za darmo"
    cta_text = ""
    back_link = "← Wróć do wszystkich poradników"

    if article:
        for child in list(article.children):
            if getattr(child, "name", None) == "div" and "article-cta" in child.get("class", []):
                h2 = child.find("h2")
                p = child.find("p")
                if h2:
                    cta_title = h2.get_text(strip=True)
                if p:
                    cta_text = p.get_text(strip=True)
                continue
            if getattr(child, "name", None) == "nav" and "article-nav" in child.get("class", []):
                a = child.find("a")
                if a:
                    back_link = a.get_text(strip=True)
                continue
            body_parts.append(str(child))

    body_html = "".join(body_parts).strip()
    body_soup = BeautifulSoup(body_html, "html.parser")
    translate_node(body_soup)
    fix_pl_links(body_soup)

    fields = [title, desc, keywords, og_title or title, og_desc or desc, h1, subtitle, cta_title, cta_text, back_link]
    translated = translate_batch(fields)
    pl_date_display = pl_date(date_display, date_iso)

    return {
        "title": translated[0],
        "description": translated[1],
        "keywords": translated[2],
        "og_title": translated[3],
        "og_description": translated[4],
        "h1": translated[5],
        "subtitle": translated[6],
        "cta_title": translated[7],
        "cta_text": translated[8],
        "back_link": translated[9],
        "headline": translated[5],
        "date_iso": date_iso,
        "date_display": pl_date_display,
        "body": str(body_soup),
    }


def hreflang_block(slug: str) -> str:
    lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{"/blog/" if code == "en" else f"/{code}/blog/"}{slug}.html" />'
        for code in LANG_CODES
    ]
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/{slug}.html" />')
    return "\n".join(lines)


def lang_dropdown(slug: str) -> str:
    links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "pl" else ""
        href = f"/blog/{slug}.html" if code == "en" else f"/{code}/blog/{slug}.html"
        links.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    return (
        '          <details class="lang-dropdown">\n'
        '            <summary aria-label="Język">PL</summary>\n'
        '            <div class="lang-dropdown-menu" role="navigation" aria-label="Język">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        "          </details>"
    )


def render_pl_article(slug: str, t: dict) -> str:
    canonical = f"https://gpxviewerapp.com/pl/blog/{slug}.html"
    title = html.escape(t["title"])
    desc = html.escape(t["description"])
    keywords = html.escape(t["keywords"])
    og_title = html.escape(t["og_title"])
    og_desc = html.escape(t["og_description"])
    h1 = html.escape(t["h1"])
    subtitle = html.escape(t["subtitle"])
    headline_json = json.dumps(t["headline"], ensure_ascii=False)
    cta_title = html.escape(t["cta_title"])
    cta_text = html.escape(t["cta_text"])
    back = html.escape(t["back_link"])

    body = t["body"]
    # Normalize body indentation to match existing pl articles
    body_lines = []
    for line in body.split("\n"):
        stripped = line.strip()
        if stripped:
            body_lines.append("          " + stripped)
    body_block = "\n".join(body_lines)

    return f"""<!DOCTYPE html>
<html lang="pl">
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
    <meta property="og:title" content="{og_title}" />
    <meta
      property="og:description"
      content="{og_desc}"
    />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="pl_PL" />
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
        "headline": {headline_json},
        "datePublished": "{t['date_iso']}",
        "inLanguage": "pl",
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
        <a class="brand" href="/pl/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/pl/#features">Funkcje</a>
          <a href="/pl/blog/">Blog</a>
          <a href="/pl/#pricing">Pro</a>
          {lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Pobierz z App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Pobierz z Google Play" />
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
          <p class="article-meta"><time datetime="{t['date_iso']}">{html.escape(t['date_display'])}</time></p>

{body_block}

          <div class="article-cta">
            <h2>{cta_title}</h2>
            <p>{cta_text}</p>
            <div class="store-badges">
              <a class="store-badge app-store-link" href="#" data-location="article_cta">
                <img src="../../images/app-store-badge-white.svg" alt="Pobierz z App Store" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="Pobierz z Google Play" />
              </a>
            </div>
          </div>

          <nav class="article-nav">
            <a href="../">{back}</a>
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
          <a href="/pl/">Strona główna</a>
          <a href="/pl/privacy.html">Prywatność</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Kontakt</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def card_from_en_index(slug: str) -> dict:
    index = (BLOG_EN / "index.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(index, "html.parser")
    for card in soup.select(".blog-card"):
        a = card.find("h2")
        if not a:
            continue
        link = a.find("a")
        if not link or slug not in link.get("href", ""):
            continue
        tag = card.find("span", class_="blog-tag")
        desc_p = card.find("p")
        return {
            "tag": tag.get_text(strip=True) if tag else "Poradnik",
            "title": link.get_text(strip=True),
            "desc": desc_p.get_text(strip=True) if desc_p else "",
        }
    return {"tag": "Poradnik", "title": slug, "desc": ""}


def render_pl_index(cards: list[dict]) -> str:
    card_html = []
    for c in cards:
        card_html.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{html.escape(c['tag'])}</span>
            <h2><a href="{html.escape(c['slug'])}.html">{html.escape(c['title'])}</a></h2>
            <p>{html.escape(c['desc'])}</p>
            <a class="blog-read-more" href="{html.escape(c['slug'])}.html">Czytaj poradnik →</a>
          </article>"""
        )

    hreflang = "\n".join(
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{"/blog/index.html" if code == "en" else f"/{code}/blog/index.html"}" />'
        for code in LANG_CODES
    )
    dropdown = "\n".join(
        f'              <a href="{"/blog/index.html" if code == "en" else f"/{code}/blog/index.html"}" hreflang="{code}" title="{LANG_LABELS[code]}"{" class=\"is-active\"" if code == "pl" else ""}>{code.upper()}</a>'
        for code in LANG_CODES
    )

    return f"""<!DOCTYPE html>
<html lang="pl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GPX Viewer Blog — Poradniki GPX dla turystyki, kolarstwa i nawigacji</title>
    <meta
      name="description"
      content="Dowiedz się, jak otwierać pliki GPX, wyświetlać trasy na mapie, podążać szlakami pieszymi i tworzyć trasy rowerowe. Darmowe poradniki od zespołu GPX Viewer."
    />
    <meta
      name="keywords"
      content="poradnik plik GPX, otwórz GPX iPhone, przeglądarka map GPX, GPX turystyka, trasy rowerowe GPX"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/pl/blog/" />
{hreflang}
    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/index.html" />
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/pl/blog/" />
    <meta property="og:title" content="GPX Viewer Blog — Poradniki i wskazówki" />
    <meta property="og:description" content="Dowiedz się, jak otwierać pliki GPX, wyświetlać trasy na mapie i podążać szlakami pieszymi." />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="pl_PL" />
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
        <a class="brand" href="/pl/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/pl/#features">Funkcje</a>
          <a href="/pl/blog/">Blog</a>
          <a href="/pl/#pricing">Pro</a>
          <details class="lang-dropdown">
            <summary aria-label="Język">PL</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="Język">
{dropdown}
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Pobierz z App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Pobierz z Google Play" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>GPX Viewer Blog</h1>
        <p>Poradniki dotyczące otwierania, wyświetlania i nawigacji plików GPX na iPhone i Android.</p>
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
          <a href="/pl/">Strona główna</a>
          <a href="/pl/privacy.html">Prywatność</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Kontakt</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def existing_pl_cards() -> list[dict]:
    index = (BLOG_PL / "index.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(index, "html.parser")
    cards = []
    for card in soup.select(".blog-card"):
        a = card.find("h2").find("a")
        href = a.get("href", "")
        slug = href.replace(".html", "")
        tag = card.find("span", class_="blog-tag").get_text(strip=True)
        cards.append({"slug": slug, "tag": tag, "title": a.get_text(strip=True), "desc": card.find("p").get_text(strip=True)})
    return cards


def main() -> None:
    BLOG_PL.mkdir(parents=True, exist_ok=True)
    written = 0
    card_meta: dict[str, dict] = {}

    for slug in SLUGS:
        en_path = BLOG_EN / f"{slug}.html"
        if not en_path.exists():
            print(f"Missing: {en_path}")
            continue
        print(f"Translating {slug}...", flush=True)
        data = extract_article(en_path)
        out = BLOG_PL / f"{slug}.html"
        out.write_text(render_pl_article(slug, data), encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")
        written += 1

        en_card = card_from_en_index(slug)
        tag, title, desc = translate_batch([en_card["tag"], en_card["title"], en_card["desc"]])
        card_meta[slug] = {"slug": slug, "tag": tag, "title": title, "desc": desc}

    # Build index: 5 existing + 20 new in English order
    en_index = BeautifulSoup((BLOG_EN / "index.html").read_text(encoding="utf-8"), "html.parser")
    existing = {c["slug"]: c for c in existing_pl_cards()}
    all_cards = []
    for card in en_index.select(".blog-card"):
        a = card.find("h2").find("a")
        slug = a.get("href", "").replace(".html", "")
        if slug in existing:
            all_cards.append(existing[slug])
        elif slug in card_meta:
            all_cards.append(card_meta[slug])

    index_path = BLOG_PL / "index.html"
    index_path.write_text(render_pl_index(all_cards), encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)} ({len(all_cards)} cards)")
    print(f"Done: {written} articles written")


if __name__ == "__main__":
    main()
