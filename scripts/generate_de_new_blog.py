#!/usr/bin/env python3
"""Generate German translations for 20 new blog articles + update de/blog/index.html."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "de" / "blog"

LANG_CODES = ["en", "de", "fr", "it", "pt", "es", "nl", "pl", "id"]
LANG_LABELS = {
    "en": "English", "de": "Deutsch", "fr": "Français", "it": "Italiano",
    "pt": "Português", "es": "Español", "nl": "Nederlands", "pl": "Polski", "id": "Indonesia",
}

STANDARD_TAIL = """
          <h2>Kurzfassung</h2>

          <p>GPX bleibt das portabelste Format für Outdoor-Routen. Importieren Sie die Datei in <a href="/de/">GPX Viewer</a>, prüfen Sie Distanz und Höhe, und starten Sie auf den Weg. Wenn etwas nicht funktioniert, beginnen Sie mit <a href="gpx-file-not-opening-fixes.html">GPX-Fehlerbehebung</a> und unserem <a href="what-is-a-gpx-file.html">GPX-Grundlagenratgeber</a>.</p>

          <h3>Vor dem Start</h3>

          <p>Laden Sie Ihr Handy auf, laden Sie Offline-Karten herunter wenn Sie Pro nutzen, und teilen Sie jemandem Ihren Plan mit. Ein GPX-Track ergänzt die Vorbereitung — ersetzt aber nie Eigenverantwortung und Geländeureil vor Ort.</p>

          <h2>Warum GPX Viewer</h2>

          <p>GPX Viewer konzentriert sich auf eine Aufgabe: GPX-Dateien auf dem Handy nutzbar machen. Schneller Import aus Mail und Dateien, klare Kartendarstellung, Höhenprofile und optionale Pro-Funktionen wie Live-Standort und Offline-Basemaps — ohne Desktop-Sync oder Formatkonvertierung.</p>

          <h3>Weiterlesen</h3>

          <p>Durchstöbern Sie den <a href="/de/blog/">GPX Viewer Blog</a> für weitere Ratgeber zum Öffnen, Anzeigen und Teilen von Routen auf iPhone und Android.</p>

          <p>Vergleichen Sie <a href="best-ways-view-gpx-online-offline.html">Online- und Offline-Anzeige</a>, erfahren Sie <a href="what-is-a-gpx-file-reader.html">was ein GPX-Reader macht</a>, und öffnen Sie Dateien mit <a href="how-to-open-gpx-file-any-device.html">gerätespezifischen Tipps</a>.</p>

          <h2>Typischer Ablauf</h2>

          <p>Die meisten Outdoor-Sportler folgen dem gleichen Muster: .gpx-Datei erhalten oder exportieren, in einem Reader öffnen, Höhen- und Distanzübersicht prüfen, dann mit Live-GPS-Overlay navigieren wenn die Bedingungen es erlauben. GPX Viewer vereinfacht jeden Schritt auf iOS und Android.</p>

          <p>Fürs Wandern kombinieren Sie diesen Ratgeber mit <a href="how-to-use-gpx-files-hiking.html">GPX fürs Wandern</a>. Radfahrer sollten auch <a href="how-to-use-gpx-files-cycling.html">Rad-GPX-Workflows</a> und <a href="how-to-create-gpx-cycling-routes.html">Erstellen von Radrouten</a> lesen.</p>

          <h3>Formathinweise</h3>

          <p>Nicht jede Geodatei ist GPX. Wenn der Import fehlschlägt, prüfen Sie ob es <a href="gpx-vs-kml.html">KML</a>, <a href="gpx-vs-tcx.html">TCX</a> oder <a href="gpx-vs-fit.html">FIT</a> ist. Exportieren Sie bei Bedarf erneut aus der Quell-App.</p>

          <p>Ob Wochenendwanderung oder Mehrtagestour — Routen im GPX-Format stellen sicher, dass Teammitglieder auf iPhone und Android dieselbe Datei öffnen können. <a href="/de/">GPX Viewer</a> ist kostenlos und genau für diesen Workflow entwickelt.</p>"""


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
        active = ' class="is-active"' if code == "de" else ""
        href = f"/blog/{slug}.html" if code == "en" else f"/{code}/blog/{slug}.html"
        links.append(f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>')
    return (
        '          <details class="lang-dropdown">\n'
        '            <summary aria-label="Sprache">DE</summary>\n'
        '            <div class="lang-dropdown-menu" role="navigation" aria-label="Sprache">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        "          </details>"
    )


def render_article(a: dict) -> str:
    slug = a["slug"]
    canonical = f"https://gpxviewerapp.com/de/blog/{slug}.html"
    body = a["body"]
    if a.get("append_tail", True):
        body += STANDARD_TAIL
    title = html.escape(a["title"])
    desc = html.escape(a["description"])
    keywords = html.escape(a["keywords"])
    h1 = html.escape(a["h1"])
    subtitle = html.escape(a["subtitle"])
    cta_title = html.escape(a["cta_title"])
    cta_text = html.escape(a["cta_text"])
    date = a["date"]
    date_display = a["date_display"]
    json_headline = json.dumps(a["json_headline"], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="de">
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
    <meta property="og:locale" content="de_DE" />
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
        "headline": {json_headline},
        "datePublished": "{date}",
        "inLanguage": "de",
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
        <a class="brand" href="/de/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/de/#features">Funktionen</a>
          <a href="/de/blog/">Blog</a>
          <a href="/de/#pricing">Pro</a>
{lang_dropdown(slug)}
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Im App Store laden" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Bei Google Play herunterladen" />
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
                <img src="../../images/app-store-badge-white.svg" alt="Im App Store laden" />
              </a>
              <a class="store-badge play-store-link" href="#" data-location="article_cta">
                <img src="../../images/google-play-badge.png" alt="Bei Google Play herunterladen" />
              </a>
            </div>
          </div>
          <nav class="article-nav">
            <a href="/de/blog/">← Zurück zu allen Ratgebern</a>
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
          <a href="/de/">Startseite</a>
          <a href="/de/privacy.html">Datenschutz</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Kontakt</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


from de_blog_data import ARTICLES, INDEX_CARDS_NEW

TRANSLATIONS = {"articles": ARTICLES, "index_cards": INDEX_CARDS_NEW}

INDEX_CARDS = [
    ("Einsteiger", "what-is-a-gpx-file.html", "Was ist eine GPX-Datei? Der komplette Ratgeber für Wanderer & Radfahrer", "Erfahren Sie, was GPX-Dateien sind, wie GPS-Tracks funktionieren und warum GPX Viewer das .gpx-Format nutzt."),
    ("iPhone & Android", "how-to-open-gpx-files-on-iphone.html", "GPX-Dateien auf iPhone und Android öffnen", "Schritt für Schritt: GPX aus Mail, Dateien oder Safari in GPX Viewer importieren."),
    ("Karten", "how-to-view-gpx-on-a-map.html", "GPX-Routen auf einer Karte anzeigen", "Wegpunkte, Höhenprofil und Distanz auf interaktiven Karten — Standard, Satellit und Hybrid."),
    ("Wandern", "best-gpx-viewer-for-hiking.html", "Bester GPX Viewer fürs Wandern: Wanderwege mit GPS-Tracks folgen", "Warum Wanderer GPX-Dateien nutzen, wie Sie Routen sicher folgen und worauf Sie bei einer GPX-App achten sollten."),
    ("Radfahren", "how-to-create-gpx-cycling-routes.html", "GPX-Radrouten erstellen und exportieren", "Radwege planen, GPX-Tracks speichern und Touren mit Freunden oder Ihrem Radcomputer teilen."),
]


def render_index() -> str:
    cards = []
    for tag, slug, title, desc in INDEX_CARDS:
        cards.append(f"""          <article class="blog-card">
            <span class="blog-tag">{tag}</span>
            <h2><a href="{slug}">{html.escape(title)}</a></h2>
            <p>{html.escape(desc)}</p>
            <a class="blog-read-more" href="{slug}">Ratgeber lesen →</a>
          </article>""")
    for card in TRANSLATIONS["index_cards"]:
        cards.append(f"""          <article class="blog-card">
            <span class="blog-tag">{html.escape(card['tag'])}</span>
            <h2><a href="{card['slug']}.html">{html.escape(card['title'])}</a></h2>
            <p>{html.escape(card['desc'])}</p>
            <a class="blog-read-more" href="{card['slug']}.html">Ratgeber lesen →</a>
          </article>""")

    hreflang = "\n".join(
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{"/blog/index.html" if code == "en" else f"/{code}/blog/index.html"}" />'
        for code in LANG_CODES
    )
    dropdown = "\n".join(
        f'              <a href="{"/blog/index.html" if code == "en" else f"/{code}/blog/index.html"}" hreflang="{code}" title="{LANG_LABELS[code]}"{" class=\"is-active\"" if code == "de" else ""}>{code.upper()}</a>'
        for code in LANG_CODES
    )

    return f"""<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GPX Viewer Blog — GPX-Ratgeber für Wandern, Radfahren & Navigation</title>
    <meta
      name="description"
      content="Erfahren Sie, wie Sie GPX-Dateien öffnen, Routen auf einer Karte anzeigen, Wanderwege folgen und Radtracks erstellen. Kostenlose Ratgeber vom GPX Viewer Team."
    />
    <meta
      name="keywords"
      content="GPX-Datei Ratgeber, GPX iPhone öffnen, GPX-Kartenviewer, Wandern GPX, Radrouten GPX"
    />
    <link rel="canonical" href="https://gpxviewerapp.com/de/blog/" />
{hreflang}
    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/index.html" />
    <meta name="theme-color" content="#14388c" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gpxviewerapp.com/de/blog/" />
    <meta property="og:title" content="GPX Viewer Blog — Ratgeber & Tipps" />
    <meta property="og:description" content="Erfahren Sie, wie Sie GPX-Dateien öffnen, Routen auf einer Karte anzeigen und Wanderwege folgen." />
    <meta property="og:image" content="https://gpxviewerapp.com/images/og-image.jpg" />
    <meta property="og:locale" content="de_DE" />
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
        <a class="brand" href="/de/">
          <img class="brand-logo" src="../../images/app-icon.png" alt="GPX Viewer" width="44" height="44" />
          <span>GPX Viewer</span>
        </a>
        <div class="header-right">
<nav class="nav-links">
<a href="/de/#features">Funktionen</a>
          <a href="/de/blog/">Blog</a>
          <a href="/de/#pricing">Pro</a>
          <details class="lang-dropdown">
            <summary aria-label="Sprache">DE</summary>
            <div class="lang-dropdown-menu" role="navigation" aria-label="Sprache">
{dropdown}
            </div>
          </details>
          <div class="store-badges store-badges--header">
            <a class="store-badge app-store-link" href="#" data-location="header">
              <img src="../../images/app-store-badge.svg" alt="Im App Store laden" />
            </a>
            <a class="store-badge play-store-link" href="#" data-location="header">
              <img src="../../images/google-play-badge.png" alt="Bei Google Play herunterladen" />
            </a>
          </div>
        </nav>
              </div>
      </div>
    </header>

    <div class="page-header">
      <div class="container">
        <h1>GPX Viewer Blog</h1>
        <p>Ratgeber zum Öffnen, Anzeigen und Navigieren von GPX-Dateien auf iPhone und Android.</p>
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
          <img src="../../images/app-icon.png" alt="" width="28" height="28" />
          © <span id="year"></span> GPX Viewer
        </span>
        <div class="footer-links">
          <a href="/de/">Startseite</a>
          <a href="/de/privacy.html">Datenschutz</a>
          <a id="footer-contact" href="mailto:lucas@streiv.app">Kontakt</a>
        </div>
      </div>
    </footer>

    <script src="../../js/site.js"></script>
      <script src="../../js/lang-dropdown.js"></script>
  </body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for article in TRANSLATIONS["articles"]:
        path = OUT / f"{article['slug']}.html"
        path.write_text(render_article(article), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
        count += 1
    index_path = OUT / "index.html"
    index_path.write_text(render_index(), encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)}")
    count += 1
    print(f"TOTAL_FILES={count}")


if __name__ == "__main__":
    main()
