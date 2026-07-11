#!/usr/bin/env python3
"""Render blog article HTML from manifest data."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"

LOCALES = {
    "en": {"code": "en", "prefix": "", "label": "Language", "home": "/", "blog": "/blog/"},
    "de": {"code": "de", "prefix": "de", "label": "Sprache", "home": "/de/", "blog": "/de/blog/"},
    "fr": {"code": "fr", "prefix": "fr", "label": "Langue", "home": "/fr/", "blog": "/fr/blog/"},
    "it": {"code": "it", "prefix": "it", "label": "Lingua", "home": "/it/", "blog": "/it/blog/"},
    "pt": {"code": "pt", "prefix": "pt", "label": "Idioma", "home": "/pt/", "blog": "/pt/blog/"},
    "es": {"code": "es", "prefix": "es", "label": "Idioma", "home": "/es/", "blog": "/es/blog/"},
    "nl": {"code": "nl", "prefix": "nl", "label": "Taal", "home": "/nl/", "blog": "/nl/blog/"},
    "pl": {"code": "pl", "prefix": "pl", "label": "Język", "home": "/pl/", "blog": "/pl/blog/"},
    "id": {"code": "id", "prefix": "id", "label": "Bahasa", "home": "/id/", "blog": "/id/blog/"},
}

LANG_CODES = ["en", "de", "fr", "it", "pt", "es", "nl", "pl", "id"]
LANG_LABELS = {
    "en": "English", "de": "Deutsch", "fr": "Français", "it": "Italiano",
    "pt": "Português", "es": "Español", "nl": "Nederlands", "pl": "Polski", "id": "Indonesia",
}


def article_path(locale: str, slug: str) -> str:
    if locale == "en":
        return f"/blog/{slug}.html"
    return f"/{locale}/blog/{slug}.html"


def hreflang_block(slug: str) -> str:
    lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{article_path(code, slug)}" />'
        for code in LANG_CODES
    ]
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/{slug}.html" />'
    )
    return "\n".join(lines)


def lang_dropdown(locale: str, slug: str) -> str:
    loc = LOCALES[locale]
    links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == locale else ""
        links.append(
            f'              <a href="{article_path(code, slug)}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    return (
        f'          <details class="lang-dropdown">\n'
        f'            <summary aria-label="{loc["label"]}">{locale.upper()}</summary>\n'
        f'            <div class="lang-dropdown-menu" role="navigation" aria-label="{loc["label"]}">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        f"          </details>"
    )


def render_article(locale: str, article: dict) -> str:
    loc = LOCALES[locale]
    slug = article["slug"]
    t = article["translations"][locale]
    prefix = loc["prefix"]
    if prefix:
        asset = "../" if locale else ""
        depth = "../../"
        home = f"/{prefix}/"
        blog_home = f"/{prefix}/blog/"
        features = f"/{prefix}/#features"
        pricing = f"/{prefix}/#pricing"
    else:
        asset = "../"
        depth = "../"
        home = "../"
        blog_home = "../blog/"
        features = "../#features"
        pricing = "../#pricing"

    canonical = f"https://gpxviewerapp.com{article_path(locale, slug)}"
    body = t["body"]
    cta_title = html.escape(t["cta_title"])
    cta_text = html.escape(t["cta_text"])
    title = html.escape(t["title"])
    h1 = html.escape(t["h1"])
    subtitle = html.escape(t["subtitle"])
    desc = html.escape(t["description"])
    keywords = html.escape(t.get("keywords", ""))
    date = article.get("date", "2026-07-11")
    date_display = t.get("date_display", "July 11, 2026")
    back = html.escape(t.get("back_link", "← Back to all guides"))
    privacy_href = f"/{prefix}/privacy.html" if prefix else "../privacy.html"

    return f"""<!DOCTYPE html>
<html lang="{loc['code']}">
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
    <link rel="icon" href="{depth}images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="{depth}css/style.css" />
    <link rel="stylesheet" href="{depth}css/lang.css?v=5" />
    <link rel="stylesheet" href="{depth}css/blog.css" />
    <script src="{depth}js/config.js"></script>
    <script src="{depth}js/seo.js"></script>
    <script src="{depth}js/analytics.js"></script>
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": {json.dumps(t['h1'])},
        "datePublished": "{date}",
        "inLanguage": "{loc['code']}",
        "author": {{ "@type": "Person", "name": "GPX Viewer" }},
        "image": "https://gpxviewerapp.com/images/og-image.jpg",
        "publisher": {{
          "@type": "Organization",
          "name": "GPX Viewer",
          "logo": {{ "@type": "ImageObject", "url": "https://gpxviewerapp.com/images/app-icon.png" }}
        }}
      }}
    </script>
  </head>
  <body>
    <header class="site-header">
      <div class="container">
        <a class="brand" href="{home}">
          <img class="brand-logo" src="{depth}images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
          <nav class="nav-links">
            <a href="{features}">{html.escape(t.get('nav_features', 'Features'))}</a>
            <a href="{blog_home}">{html.escape(t.get('nav_blog', 'Blog'))}</a>
            <a href="{pricing}">{html.escape(t.get('nav_pro', 'Pro'))}</a>
            {lang_dropdown(locale, slug)}
            <div class="store-badges store-badges--header">
              <a class="store-badge app-store-link" href="#" data-location="header">
                <img src="{depth}images/app-store-badge.svg" alt="{html.escape(t.get('app_store_alt', 'Download on the App Store'))}" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="header">
                <img src="{depth}images/google-play-badge.png" alt="{html.escape(t.get('play_store_alt', 'Get it on Google Play'))}" />
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
                <img src="{depth}images/app-store-badge-white.svg" alt="{html.escape(t.get('app_store_alt', 'Download on the App Store'))}" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="{depth}images/google-play-badge.png" alt="{html.escape(t.get('play_store_alt', 'Get it on Google Play'))}" />
              </a>
            </div>
          </div>
          <nav class="article-nav">
            <a href="{blog_home}">{back}</a>
          </nav>
        </article>
      </div>
    </main>

    <footer class="site-footer">
      <div class="container">
        <span class="footer-brand">
          <img src="{depth}images/app-icon.png" alt="" width="28" height="28" />
          © <span id="year"></span> GPX Viewer
        </span>
        <div class="footer-links">
          <a href="{home}">{html.escape(t.get('footer_home', 'Home'))}</a>
          <a href="{privacy_href}">{html.escape(t.get('footer_privacy', 'Privacy'))}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{html.escape(t.get('footer_contact', 'Contact'))}</a>
        </div>
      </div>
    </footer>

    <script src="{depth}js/site.js"></script>
    <script src="{depth}js/lang-dropdown.js"></script>
  </body>
</html>
"""


def render_blog_index(locale: str, articles: list, index_t: dict) -> str:
    loc = LOCALES[locale]
    prefix = loc["prefix"]
    depth = "../" if not prefix else "../../"
    home = f"/{prefix}/" if prefix else "../"
    features = f"/{prefix}/#features" if prefix else "../#features"
    pricing = f"/{prefix}/#pricing" if prefix else "../#pricing"
    if locale == "en":
        blog_path = "/blog/"
        canonical = "https://gpxviewerapp.com/blog/"
        privacy = "../privacy.html"
    else:
        blog_path = f"/{prefix}/blog/"
        canonical = f"https://gpxviewerapp.com/{prefix}/blog/"
        privacy = f"/{prefix}/privacy.html"

    cards = []
    for art in articles:
        if locale not in art["translations"]:
            continue
        t = art["translations"][locale]
        slug = art["slug"]
        link = f"{slug}.html" if locale == "en" else f"/{prefix}/blog/{slug}.html"
        cards.append(
            f"""          <article class="blog-card">
            <span class="blog-tag">{html.escape(t.get('tag', art.get('tag_en', 'Guide')))}</span>
            <h2><a href="{link}">{html.escape(t['card_title'])}</a></h2>
            <p>{html.escape(t['card_desc'])}</p>
            <a class="blog-read-more" href="{link}">{html.escape(t.get('read_more', 'Read guide →'))}</a>
          </article>"""
        )

    hreflang_lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{"/blog/" if code == "en" else f"/{code}/blog/"}" />'
        for code in LANG_CODES
    ]
    hreflang_lines.append('    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/" />')

    dropdown_links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == locale else ""
        href = "/blog/" if code == "en" else f"/{code}/blog/"
        dropdown_links.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )

    return f"""<!DOCTYPE html>
<html lang="{loc['code']}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(index_t['title'])}</title>
    <meta name="description" content="{html.escape(index_t['description'])}" />
    <link rel="canonical" href="{canonical}" />
{chr(10).join(hreflang_lines)}
    <meta name="theme-color" content="#14388c" />
    <link rel="icon" href="{depth}images/app-icon.png" type="image/png" />
    <link rel="stylesheet" href="{depth}css/style.css" />
    <link rel="stylesheet" href="{depth}css/lang.css?v=5" />
    <link rel="stylesheet" href="{depth}css/blog.css" />
    <script src="{depth}js/config.js"></script>
    <script src="{depth}js/seo.js"></script>
    <script src="{depth}js/analytics.js"></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container">
        <a class="brand" href="{home}">
          <img class="brand-logo" src="{depth}images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
          <nav class="nav-links">
            <a href="{features}">{html.escape(index_t.get('nav_features', 'Features'))}</a>
            <a href="{blog_path}">{html.escape(index_t.get('nav_blog', 'Blog'))}</a>
            <a href="{pricing}">{html.escape(index_t.get('nav_pro', 'Pro'))}</a>
            <details class="lang-dropdown">
              <summary aria-label="{loc['label']}">{locale.upper()}</summary>
              <div class="lang-dropdown-menu" role="navigation" aria-label="{loc['label']}">
{chr(10).join(dropdown_links)}
              </div>
            </details>
            <div class="store-badges store-badges--header">
              <a class="store-badge app-store-link" href="#" data-location="header">
                <img src="{depth}images/app-store-badge.svg" alt="App Store" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="header">
                <img src="{depth}images/google-play-badge.png" alt="Google Play" />
              </a>
            </div>
          </nav>
        </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>{html.escape(index_t['h1'])}</h1>
        <p>{html.escape(index_t['subtitle'])}</p>
      </div>
    </div>

    <main class="blog-index">
      <div class="container">
        <div class="blog-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </main>

    <footer class="site-footer">
      <div class="container">
        <span class="footer-brand">
          <img src="{depth}images/app-icon.png" alt="" width="28" height="28" />
          © <span id="year"></span> GPX Viewer
        </span>
        <div class="footer-links">
          <a href="{home}">{html.escape(index_t.get('footer_home', 'Home'))}</a>
          <a href="{privacy}">{html.escape(index_t.get('footer_privacy', 'Privacy'))}</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">{html.escape(index_t.get('footer_contact', 'Contact'))}</a>
        </div>
      </div>
    </footer>

    <script src="{depth}js/site.js"></script>
    <script src="{depth}js/lang-dropdown.js"></script>
  </body>
</html>
"""


def output_path(locale: str, slug: str) -> Path:
    if locale == "en":
        return ROOT / "blog" / f"{slug}.html"
    return ROOT / locale / "blog" / f"{slug}.html"


def main() -> None:
    import sys

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    articles = data["articles"]
    legacy = data.get("legacy_articles", [])
    index_articles = legacy + articles

    locales = LANG_CODES
    if len(sys.argv) > 1 and sys.argv[1] == "--locales":
        locales = [x.strip() for x in sys.argv[2].split(",") if x.strip()]

    for locale in locales:
        if locale not in data["blog_index"]:
            continue
        for article in articles:
            if locale not in article["translations"]:
                continue
            path = output_path(locale, article["slug"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render_article(locale, article), encoding="utf-8")
            print(f"Wrote {path.relative_to(ROOT)}")

        index_path = ROOT / "blog" / "index.html" if locale == "en" else ROOT / locale / "blog" / "index.html"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(
            render_blog_index(locale, index_articles, data["blog_index"][locale]),
            encoding="utf-8",
        )
        print(f"Wrote {index_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
