#!/usr/bin/env python3
"""Generate French blog articles from blog-articles.json English content."""

from __future__ import annotations

import html
import json
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"
OUT_DIR = ROOT / "fr" / "blog"

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
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "it": "Italiano",
    "pt": "Português",
    "es": "Español",
    "nl": "Nederlands",
    "pl": "Polski",
    "id": "Indonesia",
}

TAG_FR = {
    "Beginner": "Débutant",
    "Android": "Android",
    "Maps": "Cartes",
    "Troubleshooting": "Dépannage",
    "Formats": "Formats",
    "Comparison": "Formats",
    "Integration": "Cartes",
    "iPhone": "iPhone",
    "Cycling": "Vélo",
    "Hiking": "Randonnée",
    "Devices": "Appareils",
    "Pro": "Pro",
    "Tips": "Conseils",
    "iPhone & Android": "iPhone et Android",
}

MONTHS_FR = {
    "January": "janvier",
    "February": "février",
    "March": "mars",
    "April": "avril",
    "May": "mai",
    "June": "juin",
    "July": "juillet",
    "August": "août",
    "September": "septembre",
    "October": "octobre",
    "November": "novembre",
    "December": "décembre",
}

FR_UI = {
    "nav_features": "Fonctionnalités",
    "nav_blog": "Blog",
    "nav_pro": "Pro",
    "footer_home": "Accueil",
    "footer_privacy": "Confidentialité",
    "footer_contact": "Contact",
    "back_link": "← Retour à tous les guides",
    "read_more": "Lire le guide →",
    "app_store_alt": "Télécharger sur l'App Store",
    "play_store_alt": "Disponible sur Google Play",
    "cta_title": "Essayez GPX Viewer gratuitement",
    "index_title": "Blog GPX Viewer — Guides GPX pour la randonnée, le vélo et la navigation",
    "index_description": "Apprenez à ouvrir des fichiers GPX, afficher des itinéraires sur une carte, suivre des sentiers de randonnée et créer des parcours vélo. Guides gratuits de l'équipe GPX Viewer.",
    "index_h1": "Blog GPX Viewer",
    "index_subtitle": "Guides pour ouvrir, afficher et naviguer des fichiers GPX sur iPhone et Android.",
}

KEEP = [
    "GPX Viewer",
    "GPX Viewer Pro",
    "Garmin",
    "Strava",
    "Komoot",
    "Google Maps",
    "Google Earth",
    "Google Play",
    "Apple Maps",
    "iPhone",
    "Android",
    "iOS",
    "Garmin Connect",
    "Garmin BaseCamp",
    "QGIS",
    "Wahoo",
    "Coros",
    "WhatsApp",
    "AirDrop",
    "Mail",
    "Files",
    "Safari",
    "XML",
    "KML",
    "TCX",
    "FIT",
    "GPS",
    "DEM",
    "ANT+",
    "Edge",
    "Notepad",
    "TextEdit",
    "Drive",
    "Gmail",
    "Golden Cheetah",
    "My Maps",
]

tr = GoogleTranslator(source="en", target="fr")
_cache: dict[str, str] = {}


def protect(text: str) -> tuple[str, dict[str, str]]:
    repl: dict[str, str] = {}
    out = text

    def add(token: str, original: str) -> None:
        key = f"__KEEP{len(repl)}__"
        repl[key] = original
        nonlocal out
        out = out.replace(token, key, 1)

    for term in sorted(set(KEEP), key=len, reverse=True):
        if term in out:
            add(term, term)

    for m in re.finditer(r"<code>[^<]*</code>", out):
        add(m.group(0), m.group(0))
    for m in re.finditer(r'href="[^"]*"', out):
        add(m.group(0), m.group(0))
    for m in re.finditer(r"datetime=\"[^\"]*\"", out):
        add(m.group(0), m.group(0))
    return out, repl


def restore(text: str, repl: dict[str, str]) -> str:
    for key, val in repl.items():
        text = text.replace(key, val)
    return text


def translate(text: str) -> str:
    if not text or not text.strip():
        return text
    cache_key = text.strip()
    if cache_key in _cache:
        cached = _cache[cache_key]
        if text.endswith(" ") and not cached.endswith(" "):
            return cached + " "
        if text.startswith(" ") and not cached.startswith(" "):
            return " " + cached
        return cached
    protected, repl = protect(text)
    if not re.sub(r"__KEEP\d+__", "", protected).strip():
        _cache[cache_key] = text
        return text
    for attempt in range(4):
        try:
            out = tr.translate(protected)
            if out is None:
                raise ValueError("empty translation")
            out = restore(out, repl)
            _cache[cache_key] = out
            time.sleep(0.12)
            if text.endswith(" ") and not out.endswith(" "):
                out += " "
            if text.startswith(" ") and not out.startswith(" "):
                out = " " + out
            return out
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    _cache[cache_key] = text
    return text


def date_fr(date_display: str) -> str:
    m = re.match(r"(\w+)\s+(\d{1,2}),\s+(\d{4})", date_display)
    if not m:
        return date_display
    month = MONTHS_FR.get(m.group(1), m.group(1).lower())
    return f"{m.group(2)} {month} {m.group(3)}"


def translate_inline_html(inner: str) -> str:
    parts = re.split(r"(<[^>]+>)", inner)
    out: list[str] = []
    for part in parts:
        if part.startswith("<"):
            out.append(part)
        elif part.strip():
            out.append(translate(part))
        else:
            out.append(part)
    return "".join(out)


def fix_html_spacing(text: str) -> str:
    text = re.sub(r"([^\s>])(<[a-z/])", r"\1 \2", text)
    text = re.sub(r"(</[a-z]+>)([^\s,.;:<])", r"\1 \2", text)
    text = re.sub(r"(<code>)([^\s])", r"\1\2", text)
    text = re.sub(r"  +", " ", text)
    return text


def translate_body(body: str) -> str:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
    lines_out: list[str] = []
    for block in blocks:
        if block.startswith("<h2>"):
            inner = re.sub(r"</?h2>", "", block).strip()
            lines_out.append(f"          <h2>{translate(inner)}</h2>")
        elif block.startswith("<h3>"):
            inner = re.sub(r"</?h3>", "", block).strip()
            lines_out.append(f"          <h3>{translate(inner)}</h3>")
        elif block.startswith("<ul>"):
            items = re.findall(r"<li>(.*?)</li>", block, re.DOTALL)
            lis = [f"            <li>{translate_inline_html(item.strip())}</li>" for item in items]
            lines_out.append("          <ul>\n" + "\n".join(lis) + "\n          </ul>")
        elif block.startswith("<p"):
            inner = re.sub(r"^<p[^>]*>|</p>$", "", block, flags=re.DOTALL).strip()
            lines_out.append(f"          <p>{translate_inline_html(inner)}</p>")
        else:
            lines_out.append(f"          {block}")
    return fix_html_spacing("\n\n".join(lines_out))


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
        active = ' class="is-active"' if code == "fr" else ""
        href = f"/blog/{slug}.html" if code == "en" else f"/{code}/blog/{slug}.html"
        links.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    return (
        '          <details class="lang-dropdown">\n'
        '            <summary aria-label="Langue">FR</summary>\n'
        '            <div class="lang-dropdown-menu" role="navigation" aria-label="Langue">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        "          </details>"
    )


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace('"', "&quot;")


def render_article(slug: str, date: str, t: dict) -> str:
    title = esc(t["title"])
    desc = esc(t["description"])
    keywords = esc(t.get("keywords", ""))
    h1 = esc(t["h1"])
    subtitle = esc(t["subtitle"])
    date_display = esc(t["date_display"])
    body = t["body"]
    cta_title = esc(t["cta_title"])
    cta_text = esc(t["cta_text"])
    canonical = f"https://gpxviewerapp.com/fr/blog/{slug}.html"

    return f"""<!DOCTYPE html>
<html lang="fr">
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
    <meta property="og:locale" content="fr_FR" />
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
        "headline": {json.dumps(t["h1"])},
        "datePublished": "{date}",
        "inLanguage": "fr",
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
        <a class="brand" href="../">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="../#features">{FR_UI["nav_features"]}</a>
          <a href="../blog/">{FR_UI["nav_blog"]}</a>
          <a href="../#pricing">{FR_UI["nav_pro"]}</a>
{lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="{FR_UI["app_store_alt"]}" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="{FR_UI["play_store_alt"]}" />
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
          <p class="article-meta"><time datetime="{date}">{date_display}</time></p>

{body}

          <div class="article-cta">
            <h2>{cta_title}</h2>
            <p>{cta_text}</p>
            <div class="store-badges">
              <a class="store-badge app-store-link" href="#" data-location="article_cta">
                <img src="../../images/app-store-badge-white.svg" alt="{FR_UI["app_store_alt"]}" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="{FR_UI["play_store_alt"]}" />
              </a>
            </div>
          </div>

          <nav class="article-nav">
            <a href="../blog/">{FR_UI["back_link"]}</a>
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
          <a href="../">{FR_UI["footer_home"]}</a>
          <a href="../privacy.html">{FR_UI["footer_privacy"]}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{FR_UI["footer_contact"]}</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def translate_article(en: dict) -> dict:
    tag = TAG_FR.get(en.get("tag", ""), translate(en.get("tag", "Guide")))
    return {
        **FR_UI,
        "title": translate(en["title"]),
        "h1": translate(en["h1"]),
        "subtitle": translate(en["subtitle"]),
        "description": translate(en["description"]),
        "keywords": en.get("keywords", ""),  # keep SEO keywords in English/latin
        "tag": tag,
        "card_title": translate(en["card_title"]),
        "card_desc": translate(en["card_desc"]),
        "date_display": date_fr(en["date_display"]),
        "cta_text": translate(en["cta_text"]),
        "body": translate_body(en["body"]),
    }


def render_index(cards: list[dict]) -> str:
    hreflang_lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{"/blog/" if code == "en" else f"/{code}/blog/"}" />'
        for code in LANG_CODES
    ]
    hreflang_lines.append('    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/" />')

    dropdown = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "fr" else ""
        href = "/blog/" if code == "en" else f"/{code}/blog/"
        dropdown.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )

    card_html = []
    for c in cards:
        card_html.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{esc(c["tag"])}</span>
            <h2><a href="{c["slug"]}.html">{esc(c["card_title"])}</a></h2>
            <p>{esc(c["card_desc"])}</p>
            <a class="blog-read-more" href="{c["slug"]}.html">{FR_UI["read_more"]}</a>
          </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{FR_UI["index_title"]}</title>
    <meta
      name="description"
      content="{FR_UI["index_description"]}"
    />
    <meta
      name="keywords"
      content="guide fichier GPX, ouvrir GPX iPhone, visualiseur carte GPX, GPX randonnée, itinéraires vélo GPX"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/fr/blog/" />
{chr(10).join(hreflang_lines)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/fr/blog/" />
    <meta property="og:title" content="Blog GPX Viewer — Guides et conseils" />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="fr_FR" />
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
        <a class="brand" href="../">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="../#features">{FR_UI["nav_features"]}</a>
          <a href="../blog/">{FR_UI["nav_blog"]}</a>
          <a href="../#pricing">{FR_UI["nav_pro"]}</a>
          <details class="lang-dropdown">
            <summary aria-label="Langue">FR</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="Langue">
{chr(10).join(dropdown)}
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="{FR_UI["app_store_alt"]}" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="{FR_UI["play_store_alt"]}" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>{FR_UI["index_h1"]}</h1>
        <p>{FR_UI["index_subtitle"]}</p>
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
          <a href="../">{FR_UI["footer_home"]}</a>
          <a href="../privacy.html">{FR_UI["footer_privacy"]}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{FR_UI["footer_contact"]}</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def main() -> None:
    global _cache
    _cache = {}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_slug = {a["slug"]: a for a in data["articles"]}

    cards: list[dict] = []

    # Legacy cards (already translated in existing index)
    legacy_cards = [
        ("what-is-a-gpx-file", "Débutant", "Qu'est-ce qu'un fichier GPX ? Le guide complet pour randonneurs et cyclistes", "Découvrez ce que sont les fichiers GPX, comment fonctionnent les traces GPS et pourquoi GPX Viewer utilise le format .gpx."),
        ("how-to-open-gpx-files-on-iphone", "iPhone et Android", "Comment ouvrir des fichiers GPX sur iPhone et Android", "Étape par étape : importez des GPX depuis Mail, Fichiers ou Safari dans GPX Viewer."),
        ("how-to-view-gpx-on-a-map", "Cartes", "Comment afficher des itinéraires GPX sur une carte", "Visualisez points de passage, altitude et distance sur des cartes interactives — standard, satellite et hybride."),
        ("best-gpx-viewer-for-hiking", "Randonnée", "Meilleur visualiseur GPX pour la randonnée : suivre les sentiers avec des traces GPS", "Pourquoi les randonneurs utilisent les fichiers GPX, comment suivre les itinéraires en toute sécurité et quoi rechercher dans une application GPX."),
        ("how-to-create-gpx-cycling-routes", "Vélo", "Comment créer des itinéraires vélo GPX et les exporter", "Planifiez des parcours vélo, enregistrez des traces GPX et partagez vos sorties avec vos amis ou votre compteur GPS."),
    ]
    for slug, tag, card_title, card_desc in legacy_cards:
        cards.append({"slug": slug, "tag": tag, "card_title": card_title, "card_desc": card_desc})

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, slug in enumerate(SLUGS, 1):
        art = by_slug[slug]
        en = art["translations"]["en"]
        print(f"[{i}/20] Translating {slug}...", flush=True)
        fr = translate_article(en)
        path = OUT_DIR / f"{slug}.html"
        path.write_text(render_article(slug, art["date"], fr), encoding="utf-8")
        print(f"  Wrote {path.name}", flush=True)
        cards.append(
            {
                "slug": slug,
                "tag": fr["tag"],
                "card_title": fr["card_title"],
                "card_desc": fr["card_desc"],
            }
        )

    index_path = OUT_DIR / "index.html"
    index_path.write_text(render_index(cards), encoding="utf-8")
    print(f"Wrote index.html with {len(cards)} cards")


if __name__ == "__main__":
    main()
