#!/usr/bin/env python3
"""Translate blog articles to Italian and render HTML matching it/blog/what-is-a-gpx-file.html."""

from __future__ import annotations

import html
import json
import re
import sys
import time
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Run: pip install deep-translator")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"
OUT_DIR = ROOT / "it" / "blog"

LANG_CODES = ["en", "de", "fr", "it", "pt", "es", "nl", "pl", "id"]
LANG_LABELS = {
    "en": "English", "de": "Deutsch", "fr": "Français", "it": "Italiano",
    "pt": "Português", "es": "Español", "nl": "Nederlands", "pl": "Polski", "id": "Indonesia",
}

UI = {
    "nav_features": "Funzionalità",
    "nav_blog": "Blog",
    "nav_pro": "Pro",
    "footer_home": "Home",
    "footer_privacy": "Privacy",
    "footer_contact": "Contatti",
    "back_link": "← Torna a tutte le guide",
    "read_more": "Leggi la guida →",
    "app_store_alt": "Scarica su App Store",
    "play_store_alt": "Disponibile su Google Play",
    "cta_title": "Prova GPX Viewer gratis",
}

LEGACY_CARDS_IT = {
    "what-is-a-gpx-file": {
        "tag": "Principianti",
        "card_title": "Cos'è un file GPX? La guida completa per escursionisti e ciclisti",
        "card_desc": "Scopri cosa sono i file GPX, come funzionano le tracce GPS e perché GPX Viewer usa il formato .gpx.",
    },
    "how-to-open-gpx-files-on-iphone": {
        "tag": "iPhone e Android",
        "card_title": "Come aprire file GPX su iPhone e Android",
        "card_desc": "Passo dopo passo: importa GPX da Mail, File o Safari in GPX Viewer.",
    },
    "how-to-view-gpx-on-a-map": {
        "tag": "Mappe",
        "card_title": "Come visualizzare percorsi GPX su una mappa",
        "card_desc": "Visualizza waypoint, altitudine e distanza su mappe interattive — standard, satellitare e ibrida.",
    },
    "best-gpx-viewer-for-hiking": {
        "tag": "Escursionismo",
        "card_title": "Il miglior visualizzatore GPX per escursionismo: segui i sentieri con tracce GPS",
        "card_desc": "Perché gli escursionisti usano i file GPX, come seguire i percorsi in sicurezza e cosa cercare in un'app GPX.",
    },
    "how-to-create-gpx-cycling-routes": {
        "tag": "Ciclismo",
        "card_title": "Come creare percorsi ciclistici GPX ed esportarli",
        "card_desc": "Pianifica percorsi in bici, salva tracce GPX e condividi le pedalate con amici o il ciclocomputer.",
    },
}

INDEX_IT = {
    "title": "Blog GPX Viewer — Guide GPX per escursionismo, ciclismo e navigazione",
    "description": "Scopri come aprire file GPX, visualizzare percorsi su una mappa, seguire sentieri escursionistici e creare tracce ciclistiche. Guide gratuite dal team GPX Viewer.",
    "keywords": "guida file GPX, aprire GPX iPhone, visualizzatore mappa GPX, GPX escursionismo, percorsi ciclistici GPX",
    "h1": "Blog GPX Viewer",
    "subtitle": "Guide per aprire, visualizzare e navigare file GPX su iPhone e Android.",
}

TAG_MAP = {
    "Beginner": "Principianti",
    "iPhone & Android": "iPhone e Android",
    "Android": "Android",
    "iPhone": "iPhone",
    "Maps": "Mappe",
    "Hiking": "Escursionismo",
    "Cycling": "Ciclismo",
    "Troubleshooting": "Risoluzione problemi",
    "Formats": "Formati",
    "Devices": "Dispositivi",
    "Pro": "Pro",
    "Tips": "Consigli",
}

PROTECT = sorted([
    "GPX Viewer Pro", "GPX Viewer", "GPX file reader", "GPX files", "GPX file",
    "GPS Exchange Format", "Garmin Connect", "Garmin BaseCamp", "Google Earth",
    "Google Maps", "Google My Maps", "Apple Maps", "Strava", "Komoot", "QGIS",
    "WhatsApp", "AirDrop", "Mail", "Files", "Safari", "Drive", "Gmail",
    "Downloads", "iOS", "Android", "iPhone", "XML", "KML", "TCX", "FIT",
    ".gpx", "GPX", "lucas@streiv.app",
], key=len, reverse=True)

tr = GoogleTranslator(source="en", target="it")


def protect_text(s: str) -> tuple[str, dict[str, str]]:
    repl: dict[str, str] = {}
    for i, token in enumerate(PROTECT):
        if token in s:
            ph = f"__P{i}__"
            repl[ph] = token
            s = s.replace(token, ph)
    return s, repl


def restore_text(s: str, repl: dict[str, str]) -> str:
    for ph, token in sorted(repl.items(), key=lambda x: len(x[0]), reverse=True):
        s = s.replace(ph, token)
    return s


def translate_html_body(body: str) -> str:
    tokens: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        tokens.append(match.group(0))
        return f"__HTML{len(tokens) - 1}__"

    protected = re.sub(r"<[^>]+>", replacer, body)
    translated = translate(protected)
    for i, tok in enumerate(tokens):
        translated = translated.replace(f"__HTML{i}__", tok)
    return localize_body(translated)


def translate(s: str) -> str:
    if not s or not s.strip():
        return s
    p, repl = protect_text(s)
    for attempt in range(4):
        try:
            out = tr.translate(p)
            if out:
                return restore_text(out, repl)
        except Exception:
            time.sleep(1 + attempt)
    return restore_text(p, repl)


def translate_batch(texts: list[str]) -> list[str]:
    protected = [protect_text(t) for t in texts]
    try:
        outs = tr.translate_batch([p for p, _ in protected])
        return [restore_text(o, r) for o, (_, r) in zip(outs, protected)]
    except Exception:
        return [translate(t) for t in texts]


def localize_body(body: str) -> str:
    body = body.replace('href="../"', 'href="/it/"')
    body = body.replace('href="../blog/"', 'href="/it/blog/"')
    return body


def article_path(locale: str, slug: str) -> str:
    if locale == "en":
        return f"/blog/{slug}.html"
    return f"/{locale}/blog/{slug}.html"


def hreflang_block(slug: str) -> str:
    lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{article_path(code, slug)}" />'
        for code in LANG_CODES
    ]
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/{slug}.html" />')
    return "\n".join(lines)


def lang_dropdown(slug: str) -> str:
    links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "it" else ""
        links.append(
            f'              <a href="{article_path(code, slug)}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    return (
        '          <details class="lang-dropdown">\n'
        '            <summary aria-label="Lingua">IT</summary>\n'
        '            <div class="lang-dropdown-menu" role="navigation" aria-label="Lingua">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        "          </details>"
    )


def render_article(article: dict, t: dict) -> str:
    slug = article["slug"]
    date = article.get("date", "2026-07-11")
    title = html.escape(t["title"])
    desc = html.escape(t["description"])
    keywords = html.escape(t.get("keywords", ""))
    h1 = html.escape(t["h1"])
    subtitle = html.escape(t["subtitle"])
    canonical = f"https://gpxviewerapp.com/it/blog/{slug}.html"
    body = localize_body(t["body"])

    return f"""<!DOCTYPE html>
<html lang="it">
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
    <meta property="og:locale" content="it_IT" />
    <link rel="icon" href="../../images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="../../css/style.css" />
    <link rel="stylesheet" href="../../css/lang.css?v=5" />
<link rel="stylesheet" href="../../css/blog.css" />
<script src="../../js/config.js"></script>
    <script src="../../js/seo.js"></script>
    <script src="../../js/analytics.js"></script>
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": {json.dumps(t['h1'])},
        "datePublished": "{date}",
        "inLanguage": "it",
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
        <a class="brand" href="/it/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
          <a href="/it/#features">{UI['nav_features']}</a>
          <a href="/it/blog/">{UI['nav_blog']}</a>
          <a href="/it/#pricing">{UI['nav_pro']}</a>
{lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="{UI['app_store_alt']}" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="{UI['play_store_alt']}" />
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
          <p class="article-meta"><time datetime="{date}">{html.escape(t['date_display'])}</time></p>
{body}
          <div class="article-cta">
            <h2>{html.escape(t['cta_title'])}</h2>
            <p>{html.escape(t['cta_text'])}</p>
            <div class="store-badges">
              <a class="store-badge app-store-link" href="#" data-location="article_cta">
                <img src="../../images/app-store-badge-white.svg" alt="{UI['app_store_alt']}" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="{UI['play_store_alt']}" />
              </a>
            </div>
          </div>

          <nav class="article-nav">
            <a href="/it/blog/">{UI['back_link']}</a>
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
          <a href="/it/">{UI['footer_home']}</a>
          <a href="/it/privacy.html">{UI['footer_privacy']}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{UI['footer_contact']}</a>
        </div>
      </div>
    </footer>
<script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def render_index(cards: list[dict]) -> str:
    hreflang_lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{"/blog/" if code == "en" else f"/{code}/blog/"}" />'
        for code in LANG_CODES
    ]
    hreflang_lines.append('    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/" />')

    dropdown_links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "it" else ""
        href = "/blog/" if code == "en" else f"/{code}/blog/"
        dropdown_links.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )

    card_html = []
    for c in cards:
        card_html.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{html.escape(c['tag'])}</span>
            <h2><a href="{c['slug']}.html">{html.escape(c['card_title'])}</a></h2>
            <p>{html.escape(c['card_desc'])}</p>
            <a class="blog-read-more" href="{c['slug']}.html">{UI['read_more']}</a>
          </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="it">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(INDEX_IT['title'])}</title>
    <meta
      name="description"
      content="{html.escape(INDEX_IT['description'])}"
    />
    <meta
      name="keywords"
      content="{html.escape(INDEX_IT['keywords'])}"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/it/blog/" />
{chr(10).join(hreflang_lines)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/it/blog/" />
    <meta property="og:title" content="Blog GPX Viewer — Guide e consigli" />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="it_IT" />
    <link rel="icon" href="../../images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="../../css/style.css" />
    <link rel="stylesheet" href="../../css/lang.css?v=5" />
<link rel="stylesheet" href="../../css/blog.css" />
<script src="../../js/config.js"></script>
    <script src="../../js/seo.js"></script>
    <script src="../../js/analytics.js"></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container">
        <a class="brand" href="/it/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
          <a href="/it/#features">{UI['nav_features']}</a>
          <a href="/it/blog/">{UI['nav_blog']}</a>
          <a href="/it/#pricing">{UI['nav_pro']}</a>
          <details class="lang-dropdown">
            <summary aria-label="Lingua">IT</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="Lingua">
{chr(10).join(dropdown_links)}
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="{UI['app_store_alt']}" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="{UI['play_store_alt']}" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>{html.escape(INDEX_IT['h1'])}</h1>
        <p>{html.escape(INDEX_IT['subtitle'])}</p>
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
          <a href="/it/">{UI['footer_home']}</a>
          <a href="/it/privacy.html">{UI['footer_privacy']}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{UI['footer_contact']}</a>
        </div>
      </div>
    </footer>
<script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


CARD_TITLE_FIXES = {
    "GPX Il file non si apre? Correzioni e risoluzione dei problemi": "Il file GPX non si apre? Correzioni e risoluzione dei problemi",
    "GPX Tracce, percorsi e waypoint": "Tracce, percorsi e waypoint GPX",
    "GPX vs FIT: Percorsi vs Attività Files": "GPX vs FIT: percorsi vs file attività",
    "Apri GPX il iPhone — Oltre Apple Maps": "Apri GPX su iPhone — oltre Apple Maps",
    "Visualizza GPX Senza Internet": "Visualizza GPX senza internet",
    "Condividi GPX Tra iPhone e Android": "Condividi GPX tra iPhone e Android",
}


def polish_it(t: dict) -> dict:
    for field in ("title", "h1", "subtitle", "description", "card_title", "card_desc", "cta_text"):
        if field in t and t[field]:
            t[field] = t[field].replace("A file GPX reader", "Un lettore di file GPX")
            t[field] = t[field].replace("file GPX reader", "lettore di file GPX")
            t[field] = t[field].replace("GPX Files", "file GPX")
    if t.get("card_title") in CARD_TITLE_FIXES:
        t["card_title"] = CARD_TITLE_FIXES[t["card_title"]]
    body = t.get("body", "")
    body = body.replace("file GPX reader", "lettore di file GPX")
    body = body.replace("file GPX readers", "lettori di file GPX")
    body = body.replace("cos'è-un-gpx-file-reader.html", "what-is-a-gpx-file-reader.html")
    body = body.replace("cosa contiene file GPX", "cosa contengono i file GPX")
    body = body.replace("guida completa a file GPX", "guida completa ai file GPX")
    t["body"] = body
    return t


def italian_date(en_date: str) -> str:
    months = {
        "January": "gennaio", "February": "febbraio", "March": "marzo",
        "April": "aprile", "May": "maggio", "June": "giugno",
        "July": "luglio", "August": "agosto", "September": "settembre",
        "October": "ottobre", "November": "novembre", "December": "dicembre",
    }
    m = re.match(r"(\w+)\s+(\d+),\s+(\d+)", en_date)
    if m:
        month, day, year = m.groups()
        return f"{int(day)} {months.get(month, month.lower())} {year}"
    return en_date


def translate_article_fields(en: dict) -> dict:
    fields = [
        "title", "h1", "subtitle", "description", "keywords",
        "card_title", "card_desc", "cta_text",
    ]
    texts = [en.get(f, "") for f in fields]
    outs = translate_batch(texts)
    result = dict(zip(fields, outs))
    result["body"] = translate_html_body(en["body"])
    result["date_display"] = italian_date(en.get("date_display", "July 11, 2026"))
    result["cta_title"] = UI["cta_title"]
    tag_en = en.get("tag", "Guide")
    result["tag"] = TAG_MAP.get(tag_en, translate(tag_en))
    return result


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    articles = data["articles"]
    written = 0
    cards: list[dict] = []

    for legacy_slug, legacy_card in LEGACY_CARDS_IT.items():
        cards.append({"slug": legacy_slug, **legacy_card})

    for i, article in enumerate(articles):
        slug = article["slug"]
        en = article["translations"]["en"]
        print(f"Translating {slug} ({i + 1}/{len(articles)})...", flush=True)
        it = polish_it(translate_article_fields(en))
        out = OUT_DIR / f"{slug}.html"
        out.write_text(render_article(article, it), encoding="utf-8")
        written += 1
        cards.append({
            "slug": slug,
            "tag": it["tag"],
            "card_title": it["card_title"],
            "card_desc": it["card_desc"],
        })
        time.sleep(0.15)

    index_path = OUT_DIR / "index.html"
    index_path.write_text(render_index(cards), encoding="utf-8")
    written += 1

    print(f"Done: {written} files written ({len(articles)} articles + index)")


if __name__ == "__main__":
    main()
