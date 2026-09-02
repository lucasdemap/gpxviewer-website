#!/usr/bin/env python3
"""Render Spanish blog articles from English blog-articles.json."""

from __future__ import annotations

import html
import json
import re
import time
from html.parser import HTMLParser
from pathlib import Path

from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"
OUT_DIR = ROOT / "es" / "blog"
CACHE = Path(__file__).resolve().parent / "es-blog-cache.json"

LANG_CODES = ["en", "de", "fr", "it", "pt", "es", "nl", "pl", "id"]
LANG_LABELS = {
    "en": "English", "de": "Deutsch", "fr": "Français", "it": "Italiano",
    "pt": "Português", "es": "Español", "nl": "Nederlands", "pl": "Polski", "id": "Indonesia",
}

MONTHS_ES = {
    "January": "enero", "February": "febrero", "March": "marzo", "April": "abril",
    "May": "mayo", "June": "junio", "July": "julio", "August": "agosto",
    "September": "septiembre", "October": "octubre", "November": "noviembre", "December": "diciembre",
}

LEGACY_CARDS = [
    {"slug": "what-is-a-gpx-file", "tag": "Principiante", "card_title": "¿Qué es un archivo GPX? Guía completa para senderistas y ciclistas", "card_desc": "Descubre qué son los archivos GPX, cómo funcionan los tracks GPS y por qué GPX Viewer usa el formato .gpx."},
    {"slug": "how-to-open-gpx-files-on-iphone", "tag": "iPhone y Android", "card_title": "Cómo abrir archivos GPX en iPhone y Android", "card_desc": "Paso a paso: importa GPX desde Mail, Archivos o Safari a GPX Viewer."},
    {"slug": "how-to-view-gpx-on-a-map", "tag": "Mapas", "card_title": "Cómo ver rutas GPX en un mapa", "card_desc": "Waypoints, elevación y distancia en mapas interactivos — estándar, satélite e híbrido."},
    {"slug": "best-gpx-viewer-for-hiking", "tag": "Senderismo", "card_title": "El mejor visor GPX para senderismo: sigue senderos con tracks GPS", "card_desc": "Por qué los senderistas usan archivos GPX, cómo seguir rutas con seguridad y qué buscar en una app GPX."},
    {"slug": "how-to-create-gpx-cycling-routes", "tag": "Ciclismo", "card_title": "Cómo crear rutas GPX de ciclismo y exportarlas", "card_desc": "Planifica rutas en bici, guarda tracks GPX y comparte salidas con amigos o tu ciclocomputador."},
]

TAG_MAP = {
    "Beginner": "Principiante",
    "Android": "Android",
    "Maps": "Mapas",
    "Troubleshooting": "Solución de problemas",
    "Formats": "Formatos",
    "iPhone": "iPhone",
    "Cycling": "Ciclismo",
    "Hiking": "Senderismo",
    "Devices": "Dispositivos",
    "Pro": "Pro",
    "Tips": "Consejos",
}

translator = GoogleTranslator(source="en", target="es")
_cache: dict[str, str] = {}


def load_cache() -> None:
    global _cache
    if CACHE.exists():
        _cache = json.loads(CACHE.read_text(encoding="utf-8"))


def save_cache() -> None:
    CACHE.write_text(json.dumps(_cache, ensure_ascii=False, indent=2), encoding="utf-8")


def tr(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    if text in _cache:
        return _cache[text]
    for attempt in range(3):
        try:
            result = translator.translate(text)
            if result:
                _cache[text] = result
                time.sleep(0.15)
                return result
        except Exception:
            time.sleep(1 + attempt)
    _cache[text] = text
    return text


def date_display_es(en_display: str) -> str:
    m = re.match(r"(\w+) (\d+), (\d{4})", en_display)
    if not m:
        return en_display
    month, day, year = m.groups()
    return f"{day} de {MONTHS_ES.get(month, month.lower())} de {year}"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self._skip += 1
        attrs_s = "".join(
            f' {k}="{html.escape(v, quote=True)}"' if v is not None else f" {k}"
            for k, v in attrs
        )
        self.parts.append(f"<{tag}{attrs_s}>")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self._skip = max(0, self._skip - 1)
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self._skip:
            self.parts.append(data)
            return
        if data.strip():
            translated = tr(data)
            self.parts.append(translated if translated is not None else data)
        else:
            self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")


def translate_html_body(body: str) -> str:
    parser = TextExtractor()
    parser.feed(body)
    return "".join(parser.parts)


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
        active = ' class="is-active"' if code == "es" else ""
        href = f"/blog/{slug}.html" if code == "en" else f"/{code}/blog/{slug}.html"
        links.append(f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>')
    return (
        '          <details class="lang-dropdown">\n'
        '            <summary aria-label="Idioma">ES</summary>\n'
        '            <div class="lang-dropdown-menu" role="navigation" aria-label="Idioma">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        "          </details>"
    )


def render_article(slug: str, date: str, t: dict) -> str:
    title = html.escape(t["title"])
    desc = html.escape(t["description"])
    keywords = html.escape(t["keywords"])
    h1 = html.escape(t["h1"])
    subtitle = html.escape(t["subtitle"])
    date_display = html.escape(t["date_display"])
    cta_title = html.escape(t["cta_title"])
    cta_text = html.escape(t["cta_text"])
    headline = json.dumps(t["h1"], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="es">
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
    <link rel="canonical" href="https://gpxviewerapp.com/es/blog/{slug}.html" />
{hreflang_block(slug)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="https://gpxviewerapp.com/es/blog/{slug}.html" />
    <meta property="og:title" content="{title}" />
    <meta
      property="og:description"
      content="{desc}"
    />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="es_ES" />
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
        "headline": {headline},
        "datePublished": "{date}",
        "inLanguage": "es",
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
<a href="../#features">Funciones</a>
          <a href="../blog/">Blog</a>
          <a href="../#pricing">Pro</a>
          {lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Descargar en App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Disponible en Google Play" />
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

{t["body"]}
          <div class="article-cta">
            <h2>{cta_title}</h2>
            <p>{cta_text}</p>
            <div class="store-badges">
              <a class="store-badge app-store-link" href="#" data-location="article_cta">
                <img src="../../images/app-store-badge-white.svg" alt="Descargar en App Store" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="Disponible en Google Play" />
              </a>
            </div>
          </div>

          <nav class="article-nav">
            <a href="../blog/">← Volver a todas las guías</a>
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
          <a href="../">Inicio</a>
          <a href="../privacy.html">Privacidad</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Contacto</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def translate_article(en: dict) -> dict:
    return {
        "title": tr(en["title"]),
        "h1": tr(en["h1"]),
        "subtitle": tr(en["subtitle"]),
        "description": tr(en["description"]),
        "keywords": tr(en["keywords"]),
        "tag": TAG_MAP.get(en["tag"], tr(en["tag"])),
        "card_title": tr(en["card_title"]),
        "card_desc": tr(en["card_desc"]),
        "date_display": date_display_es(en["date_display"]),
        "cta_title": "Prueba GPX Viewer gratis",
        "cta_text": tr(en["cta_text"]),
        "body": translate_html_body(en["body"]),
    }


def render_index(cards: list[dict]) -> str:
    card_html = []
    for c in cards:
        slug = c["slug"]
        card_html.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{html.escape(c['tag'])}</span>
            <h2><a href="{slug}.html">{html.escape(c['card_title'])}</a></h2>
            <p>{html.escape(c['card_desc'])}</p>
            <a class="blog-read-more" href="{slug}.html">Leer guía →</a>
          </article>"""
        )

    dropdown = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == "es" else ""
        href = "/blog/index.html" if code == "en" else f"/{code}/blog/index.html"
        dropdown.append(f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>')

    hreflang = []
    for code in LANG_CODES:
        href = "https://gpxviewerapp.com/blog/index.html" if code == "en" else f"https://gpxviewerapp.com/{code}/blog/index.html"
        hreflang.append(f'    <link rel="alternate" hreflang="{code}" href="{href}" />')
    hreflang.append('    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/index.html" />')

    return f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Blog GPX Viewer — Guías GPX para senderismo, ciclismo y navegación</title>
    <meta
      name="description"
      content="Aprende a abrir archivos GPX, ver rutas en un mapa, seguir senderos y crear tracks de ciclismo. Guías gratuitas del equipo de GPX Viewer."
    />
    <meta
      name="keywords"
      content="guía archivo GPX, abrir GPX iPhone, visor mapa GPX, GPX senderismo, rutas GPX ciclismo"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/es/blog/" />
{chr(10).join(hreflang)}
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/es/blog/" />
    <meta property="og:title" content="Blog GPX Viewer — Guías y consejos" />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="es_ES" />
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
<a href="../#features">Funciones</a>
          <a href="../blog/">Blog</a>
          <a href="../#pricing">Pro</a>
          <details class="lang-dropdown">
            <summary aria-label="Idioma">ES</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="Idioma">
{chr(10).join(dropdown)}
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Descargar en App Store" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Disponible en Google Play" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>Blog GPX Viewer</h1>
        <p>Guías para abrir, visualizar y navegar archivos GPX en iPhone y Android.</p>
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
          <a href="../">Inicio</a>
          <a href="../privacy.html">Privacidad</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Contacto</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def main() -> None:
    load_cache()
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = list(LEGACY_CARDS)

    for article in data["articles"]:
        slug = article["slug"]
        en = article["translations"]["en"]
        es = translate_article(en)
        path = OUT_DIR / f"{slug}.html"
        path.write_text(render_article(slug, article["date"], es), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
        cards.append({
            "slug": slug,
            "tag": es["tag"],
            "card_title": es["card_title"],
            "card_desc": es["card_desc"],
        })
        save_cache()

    index_path = OUT_DIR / "index.html"
    index_path.write_text(render_index(cards), encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)} ({len(cards)} cards)")
    save_cache()


if __name__ == "__main__":
    main()
