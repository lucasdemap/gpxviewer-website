#!/usr/bin/env python3
"""Translate 20 English blog articles to Portuguese (pt-PT style) and update pt/blog/index.html."""

from __future__ import annotations

import html
import json
import re
import time
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    raise SystemExit("Run: pip install deep-translator")

ROOT = Path(__file__).resolve().parent.parent
EN_BLOG = ROOT / "blog"
PT_BLOG = ROOT / "pt" / "blog"

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

# UI strings (European Portuguese, matching existing pt/blog pages)
UI = {
    "nav_features": "Funcionalidades",
    "nav_blog": "Blog",
    "nav_pro": "Pro",
    "footer_home": "Início",
    "footer_privacy": "Privacidade",
    "footer_contact": "Contacto",
    "back_link": "← Voltar a todos os guias",
    "read_more": "Ler guia →",
    "app_store_alt": "Descarregar na App Store",
    "play_store_alt": "Disponível no Google Play",
    "cta_title": "Experimente o GPX Viewer gratuitamente",
    "lang_label": "Idioma",
    "index_title": "Blog GPX Viewer — Guias GPX para Caminhada, Ciclismo e Navegação",
    "index_desc": "Aprenda a abrir ficheiros GPX, ver rotas num mapa, seguir trilhos de caminhada e criar percursos de ciclismo. Guias gratuitos da equipa GPX Viewer.",
    "index_h1": "Blog GPX Viewer",
    "index_subtitle": "Guias para abrir, ver e navegar ficheiros GPX no iPhone e Android.",
}

TAG_MAP = {
    "Beginner": "Iniciante",
    "Android": "Android",
    "Maps": "Mapas",
    "Troubleshooting": "Resolução de problemas",
    "Formats": "Formatos",
    "Comparison": "Comparação",
    "Integration": "Integração",
    "iPhone": "iPhone",
    "Cycling": "Ciclismo",
    "Hiking": "Caminhada",
    "Devices": "Dispositivos",
    "Pro": "Pro",
    "Tips": "Dicas",
}

# BR → PT-EU normalisation after machine translation
PT_EU = [
    (r"\barquivo\b", "ficheiro"),
    (r"\barquivos\b", "ficheiros"),
    (r"\bBaixar\b", "Descarregar"),
    (r"\bbaixar\b", "descarregar"),
    (r"\bBaixe\b", "Descarregue"),
    (r"\bcelular\b", "telemóvel"),
    (r"\bcelulares\b", "telemóveis"),
    (r"\bContato\b", "Contacto"),
    (r"\bcontato\b", "contacto"),
    (r"\bAplicativo\b", "App"),
    (r"\baplicativo\b", "app"),
    (r"\bAplicativos\b", "Apps"),
    (r"\baplicativos\b", "apps"),
    (r"\bCompartilhar\b", "Partilhar"),
    (r"\bcompartilhar\b", "partilhar"),
    (r"\bCompartilhe\b", "Partilhe"),
    (r"\bcompartilhe\b", "partilhe"),
    (r"\bCompartilhamento\b", "Partilha"),
    (r"\bcompartilhamento\b", "partilha"),
    (r"\bVocê\b", "Si"),
    (r"\bvocê\b", "si"),
    (r"\bseu\b", "seu"),
    (r"\bsua\b", "sua"),
    (r"\bseus\b", "seus"),
    (r"\bsuas\b", "suas"),
    (r"\bE-mail\b", "Mail"),
    (r"\be-mail\b", "mail"),
    (r"\bEmail\b", "Mail"),
    (r"\bemail\b", "mail"),
    (r"\bArquivos\b", "Ficheiros"),
    (r"\barquivos\b", "ficheiros"),
    (r"\bArquivo\b", "Ficheiro"),
    (r"\btrilha\b", "trilho"),
    (r"\btrilhas\b", "trilhos"),
    (r"\bcaminhada\b", "caminhada"),
    (r"\bCaminhada\b", "Caminhada"),
]

MONTHS_PT = {
    "January": "janeiro", "February": "fevereiro", "March": "março",
    "April": "abril", "May": "maio", "June": "junho", "July": "julho",
    "August": "agosto", "September": "setembro", "October": "outubro",
    "November": "novembro", "December": "dezembro",
}

tr = GoogleTranslator(source="en", target="pt")


def pt_eu(text: str) -> str:
    for pat, repl in PT_EU:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text


def protect(text: str) -> tuple[str, dict[str, str]]:
    repl: dict[str, str] = {}
    idx = 0

    def sub(m: re.Match) -> str:
        nonlocal idx
        key = f"__PH{idx}__"
        repl[key] = m.group(0)
        idx += 1
        return key

    for pat in [
        r"GPX Viewer Pro",
        r"GPX Viewer",
        r"Google Play",
        r"App Store",
        r"Google Maps",
        r"Apple Maps",
        r"Google Earth",
        r"Garmin Connect",
        r"Garmin BaseCamp",
        r"Google My Maps",
        r"Training Center XML",
        r"GPS Exchange Format",
        r"Keyhole Markup Language",
        r"Strava",
        r"Komoot",
        r"Garmin",
        r"QGIS",
        r"WhatsApp",
        r"AirDrop",
        r"Google Drive",
        r"Gmail",
        r"Mail",
        r"Files",
        r"Safari",
        r"Notepad",
        r"TextEdit",
        r"Wahoo",
        r"Coros",
        r"Edge",
        r"Golden Cheetah",
        r"ANT\+",
        r"iPhone",
        r"Android",
        r"iOS",
        r"XML",
        r"TCX",
        r"FIT",
        r"KML",
        r"GPX",
        r"\.gpx",
        r"\.kml",
        r"\.tcx",
        r"\.fit",
        r"\.xml",
        r"lucas@streiv\.app",
    ]:
        text = re.sub(pat, sub, text, flags=re.IGNORECASE)

    return text, repl


def restore(text: str, repl: dict[str, str]) -> str:
    for k, v in repl.items():
        text = text.replace(k, v)
    return text


def translate(text: str) -> str:
    if not text.strip():
        return text
    p, repl = protect(text)
    try:
        out = tr.translate(p)
    except Exception:
        time.sleep(1)
        out = tr.translate(p)
    out = restore(out or text, repl)
    return pt_eu(out)


def translate_batch(texts: list[str]) -> list[str]:
    protected = [protect(t) for t in texts]
    try:
        outs = tr.translate_batch([p for p, _ in protected])
    except Exception:
        outs = []
        for p, repl in protected:
            try:
                outs.append(restore(tr.translate(p), repl))
            except Exception:
                outs.append(restore(p, repl))
            time.sleep(0.3)
        return [pt_eu(o) for o in outs]
    result = []
    for (p, repl), out in zip(protected, outs):
        result.append(pt_eu(restore(out or p, repl)))
    return result


def extract_meta(content: str, name: str) -> str:
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', content)
    if m:
        return html.unescape(m.group(1))
    m = re.search(rf'<meta\s+content="([^"]*)"\s+name="{name}"', content)
    return html.unescape(m.group(1)) if m else ""


def extract_title(content: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", content)
    return html.unescape(m.group(1)) if m else ""


def extract_h1_subtitle(content: str) -> tuple[str, str]:
    m = re.search(
        r'<div class="page-header">\s*<div class="container">\s*<h1>([^<]+)</h1>\s*<p>([^<]+)</p>',
        content,
        re.S,
    )
    if m:
        return html.unescape(m.group(1)), html.unescape(m.group(2))
    return "", ""


def extract_date(content: str) -> tuple[str, str]:
    m = re.search(r'<time datetime="([^"]+)">([^<]+)</time>', content)
    if m:
        return m.group(1), m.group(2)
    return "2026-07-12", "12 de julho de 2026"


def format_date_pt(en_display: str) -> str:
    m = re.match(r"(\w+)\s+(\d+),\s+(\d{4})", en_display.strip())
    if not m:
        return en_display
    month, day, year = m.group(1), m.group(2), m.group(3)
    pt_month = MONTHS_PT.get(month, month.lower())
    return f"{day} de {pt_month} de {year}"


def extract_body_and_cta(content: str) -> tuple[str, str, str]:
    m = re.search(
        r'<article class="article-content">\s*<p class="article-meta">.*?</p>\s*(.*?)\s*<div class="article-cta">',
        content,
        re.S,
    )
    body = m.group(1).strip() if m else ""
    cta_m = re.search(
        r'<div class="article-cta">\s*<h2>([^<]+)</h2>\s*<p>([^<]+)</p>',
        content,
        re.S,
    )
    cta_title = html.unescape(cta_m.group(1)) if cta_m else UI["cta_title"]
    cta_text = html.unescape(cta_m.group(2)) if cta_m else ""
    return body, cta_title, cta_text


def translate_html_fragment(fragment: str) -> str:
    """Translate text nodes inside HTML, preserving tags and hrefs."""
    parts = re.split(r"(<[^>]+>)", fragment)
    text_indices = [i for i, p in enumerate(parts) if p and not p.startswith("<")]
    if not text_indices:
        return fragment
    texts = [parts[i] for i in text_indices]
    translated = translate_batch(texts)
    for idx, t in zip(text_indices, translated):
        parts[idx] = t
    return "".join(parts)


def hreflang_block(slug: str) -> str:
    lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{article_path(code, slug)}" />'
        for code in LANG_CODES
    ]
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/{slug}.html" />'
    )
    return "\n".join(lines)


def article_path(locale: str, slug: str) -> str:
    if locale == "en":
        return f"/blog/{slug}.html"
    return f"/{locale}/blog/{slug}.html"


def lang_dropdown(slug: str) -> str:
    links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "pt" else ""
        links.append(
            f'              <a href="{article_path(code, slug)}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    return (
        f'          <details class="lang-dropdown">\n'
        f'            <summary aria-label="{UI["lang_label"]}">PT</summary>\n'
        f'            <div class="lang-dropdown-menu" role="navigation" aria-label="{UI["lang_label"]}">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        f"          </details>"
    )


def render_article(slug: str, meta: dict) -> str:
    esc = html.escape
    title = esc(meta["title"])
    desc = esc(meta["description"])
    keywords = esc(meta["keywords"])
    h1 = esc(meta["h1"])
    subtitle = esc(meta["subtitle"])
    date = meta["date"]
    date_display = esc(meta["date_display"])
    body = meta["body"]
    cta_title = esc(meta.get("cta_title", UI["cta_title"]))
    cta_text = esc(meta["cta_text"])
    headline_json = json.dumps(meta["h1"], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="pt">
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
    <link rel="canonical" href="https://gpxviewerapp.com/pt/blog/{slug}.html" />
{hreflang_block(slug)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="https://gpxviewerapp.com/pt/blog/{slug}.html" />
    <meta property="og:title" content="{title}" />
    <meta
      property="og:description"
      content="{desc}"
    />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
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
        "headline": {headline_json},
        "datePublished": "{date}",
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
        }},
        "inLanguage": "pt"
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
          <a href="../#features">{UI["nav_features"]}</a>
          <a href="../blog/">{UI["nav_blog"]}</a>
          <a href="../#pricing">{UI["nav_pro"]}</a>
          {lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="{UI["app_store_alt"]}" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="{UI["play_store_alt"]}" />
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
                <img src="../../images/app-store-badge-white.svg" alt="{UI["app_store_alt"]}" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="{UI["play_store_alt"]}" />
              </a>
            </div>
          </div>

          <nav class="article-nav">
            <a href="../blog/">{UI["back_link"]}</a>
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
          <a href="../">{UI["footer_home"]}</a>
          <a href="../privacy.html">{UI["footer_privacy"]}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{UI["footer_contact"]}</a>
        </div>
      </div>
    </footer>
<script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def extract_card_from_en(content: str) -> tuple[str, str, str]:
    m = re.search(
        r'<article class="blog-card">\s*<span class="blog-tag">([^<]+)</span>\s*<h2><a href="[^"]+">([^<]+)</a></h2>\s*<p>([^<]+)</p>',
        content,
        re.S,
    )
    if not m:
        return "Guia", "Título", "Descrição"
    return m.group(1), html.unescape(m.group(2)), html.unescape(m.group(3))


def render_index(cards: list[dict]) -> str:
    card_html = []
    for c in cards:
        card_html.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{html.escape(c["tag"])}</span>
            <h2><a href="{c["href"]}">{html.escape(c["title"])}</a></h2>
            <p>{html.escape(c["desc"])}</p>
            <a class="blog-read-more" href="{c["href"]}">{UI["read_more"]}</a>
          </article>"""
        )

    dropdown = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "pt" else ""
        href = "/blog/index.html" if code == "en" else f"/{code}/blog/index.html"
        dropdown.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )

    hreflang = []
    for code in LANG_CODES:
        href = "https://gpxviewerapp.com/blog/index.html" if code == "en" else f"https://gpxviewerapp.com/{code}/blog/index.html"
        hreflang.append(f'    <link rel="alternate" hreflang="{code}" href="{href}" />')
    hreflang.append('    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/index.html" />')

    return f"""<!DOCTYPE html>
<html lang="pt">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{UI["index_title"]}</title>
    <meta
      name="description"
      content="{UI["index_desc"]}"
    />
    <meta
      name="keywords"
      content="guia ficheiro GPX, abrir GPX iPhone, visualizador mapa GPX, GPX caminhada, rotas ciclismo GPX"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/pt/blog/" />
{chr(10).join(hreflang)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/pt/blog/" />
    <meta property="og:title" content="Blog GPX Viewer — Guias e Dicas" />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
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
          <a href="../#features">{UI["nav_features"]}</a>
          <a href="../blog/">{UI["nav_blog"]}</a>
          <a href="../#pricing">{UI["nav_pro"]}</a>
          <details class="lang-dropdown">
            <summary aria-label="{UI["lang_label"]}">PT</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="{UI["lang_label"]}">
{chr(10).join(dropdown)}
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="{UI["app_store_alt"]}" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="{UI["play_store_alt"]}" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>{UI["index_h1"]}</h1>
        <p>{UI["index_subtitle"]}</p>
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
          <a href="../">{UI["footer_home"]}</a>
          <a href="../privacy.html">{UI["footer_privacy"]}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{UI["footer_contact"]}</a>
        </div>
      </div>
    </footer>
<script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def main() -> None:
    PT_BLOG.mkdir(parents=True, exist_ok=True)
    written = 0
    card_data: list[dict] = []

    # Legacy 5 cards from existing pt index
    legacy_cards = [
        ("what-is-a-gpx-file", "Iniciante",
         "O que é um ficheiro GPX? Guia completo para caminhantes e ciclistas",
         "Saiba o que são ficheiros GPX, como funcionam os trilhos GPS e porque o GPX Viewer usa o formato .gpx."),
        ("how-to-open-gpx-files-on-iphone", "iPhone e Android",
         "Como abrir ficheiros GPX no iPhone e Android",
         "Passo a passo: importe GPX a partir de Mail, Ficheiros ou Safari para o GPX Viewer."),
        ("how-to-view-gpx-on-a-map", "Mapas",
         "Como ver rotas GPX num mapa",
         "Veja pontos de passagem, elevação e distância em mapas interativos — standard, satélite e híbrido."),
        ("best-gpx-viewer-for-hiking", "Caminhada",
         "Melhor visualizador GPX para caminhada: siga trilhos com trilhos GPS",
         "Porque os caminhantes usam ficheiros GPX, como seguir rotas em segurança e o que procurar numa app GPX."),
        ("how-to-create-gpx-cycling-routes", "Ciclismo",
         "Como criar rotas GPX de ciclismo e exportá-las",
         "Planeie percursos de bicicleta, guarde trilhos GPX e partilhe passeios com amigos ou o seu ciclocomputador."),
    ]
    for slug, tag, title, desc in legacy_cards:
        card_data.append({"href": f"{slug}.html", "tag": tag, "title": title, "desc": desc})

    en_index = (EN_BLOG / "index.html").read_text(encoding="utf-8")

    for i, slug in enumerate(SLUGS):
        print(f"Translating {slug} ({i+1}/{len(SLUGS)})...", flush=True)
        en_path = EN_BLOG / f"{slug}.html"
        content = en_path.read_text(encoding="utf-8")

        title = translate(extract_title(content))
        desc = translate(extract_meta(content, "description"))
        keywords = extract_meta(content, "keywords")  # keep English keywords for SEO
        h1, subtitle = extract_h1_subtitle(content)
        h1 = translate(h1)
        subtitle = translate(subtitle)
        date, date_en = extract_date(content)
        date_display = format_date_pt(date_en)
        body_en, cta_title_en, cta_text = extract_body_and_cta(content)
        cta_title = translate(cta_title_en) if cta_title_en != "Try GPX Viewer free" else UI["cta_title"]
        cta_text = translate(cta_text)
        body = translate_html_fragment(body_en)

        meta = {
            "title": title,
            "description": desc,
            "keywords": keywords,
            "h1": h1,
            "subtitle": subtitle,
            "date": date,
            "date_display": date_display,
            "body": body,
            "cta_title": cta_title,
            "cta_text": cta_text,
        }

        out_path = PT_BLOG / f"{slug}.html"
        out_path.write_text(render_article(slug, meta), encoding="utf-8")
        written += 1
        time.sleep(0.15)

        # Card from English index
        slug_block = re.search(
            rf'<article class="blog-card">.*?href="{re.escape(slug)}\.html".*?</article>',
            en_index,
            re.S,
        )
        if slug_block:
            tag_en, card_title, card_desc = extract_card_from_en(slug_block.group(0))
            tag = TAG_MAP.get(tag_en, translate(tag_en))
            card_data.append({
                "href": f"{slug}.html",
                "tag": tag,
                "title": translate(card_title),
                "desc": translate(card_desc),
            })

    index_path = PT_BLOG / "index.html"
    index_path.write_text(render_index(card_data), encoding="utf-8")
    written += 1

    print(f"\nDone: {written} files written ({len(SLUGS)} articles + index)")
    print(f"Index cards: {len(card_data)}")


if __name__ == "__main__":
    main()
