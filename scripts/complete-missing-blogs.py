#!/usr/bin/env python3
"""Generate missing localized blog articles and index pages from English sources."""

from __future__ import annotations

import html
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
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
OG_LOCALE = {
    "pt": "pt_PT",
    "es": "es_ES",
    "nl": "nl_NL",
    "pl": "pl_PL",
    "id": "id_ID",
}

UI = {
    "pt": {
        "label": "Idioma",
        "nav_features": "Funcionalidades",
        "nav_blog": "Blog",
        "nav_pro": "Pro",
        "footer_home": "Início",
        "footer_privacy": "Privacidade",
        "footer_contact": "Contacto",
        "back": "← Voltar a todos os guias",
        "read_more": "Ler guia →",
        "app_store": "Descarregar na App Store",
        "play_store": "Disponível no Google Play",
        "index_title": "Blog GPX Viewer — Guias GPX para caminhadas, ciclismo e navegação",
        "index_desc": "Aprenda a abrir ficheiros GPX, ver rotas num mapa, seguir trilhos e criar percursos de ciclismo. Guias gratuitos da equipa GPX Viewer.",
        "index_h1": "Blog GPX Viewer",
        "index_sub": "Guias para abrir, ver e navegar ficheiros GPX no iPhone e Android.",
    },
    "es": {
        "label": "Idioma",
        "nav_features": "Funciones",
        "nav_blog": "Blog",
        "nav_pro": "Pro",
        "footer_home": "Inicio",
        "footer_privacy": "Privacidad",
        "footer_contact": "Contacto",
        "back": "← Volver a todas las guías",
        "read_more": "Leer guía →",
        "app_store": "Descargar en App Store",
        "play_store": "Disponible en Google Play",
        "index_title": "Blog GPX Viewer — Guías GPX para senderismo, ciclismo y navegación",
        "index_desc": "Aprende a abrir archivos GPX, ver rutas en un mapa, seguir senderos y crear rutas en bici. Guías gratuitas del equipo GPX Viewer.",
        "index_h1": "Blog GPX Viewer",
        "index_sub": "Guías para abrir, ver y navegar archivos GPX en iPhone y Android.",
    },
    "nl": {
        "label": "Taal",
        "nav_features": "Functies",
        "nav_blog": "Blog",
        "nav_pro": "Pro",
        "footer_home": "Home",
        "footer_privacy": "Privacy",
        "footer_contact": "Contact",
        "back": "← Terug naar alle gidsen",
        "read_more": "Gids lezen →",
        "app_store": "Download in de App Store",
        "play_store": "Downloaden via Google Play",
        "index_title": "GPX Viewer Blog — GPX-gidsen voor wandelen, fietsen en navigatie",
        "index_desc": "Leer GPX-bestanden openen, routes op een kaart bekijken, wandelpaden volgen en fietsroutes maken. Gratis gidsen van het GPX Viewer-team.",
        "index_h1": "GPX Viewer Blog",
        "index_sub": "Gidsen om GPX-bestanden te openen, bekijken en navigeren op iPhone en Android.",
    },
    "pl": {
        "label": "Język",
        "nav_features": "Funkcje",
        "nav_blog": "Blog",
        "nav_pro": "Pro",
        "footer_home": "Strona główna",
        "footer_privacy": "Prywatność",
        "footer_contact": "Kontakt",
        "back": "← Wróć do wszystkich poradników",
        "read_more": "Czytaj poradnik →",
        "app_store": "Pobierz z App Store",
        "play_store": "Pobierz z Google Play",
        "index_title": "Blog GPX Viewer — przewodniki GPX na wędrówki, rower i nawigację",
        "index_desc": "Dowiedz się, jak otwierać pliki GPX, oglądać trasy na mapie, podążać szlakami i tworzyć trasy rowerowe. Darmowe poradniki zespołu GPX Viewer.",
        "index_h1": "Blog GPX Viewer",
        "index_sub": "Poradniki o otwieraniu, przeglądaniu i nawigacji plików GPX na iPhone i Android.",
    },
    "id": {
        "label": "Bahasa",
        "nav_features": "Fitur",
        "nav_blog": "Blog",
        "nav_pro": "Pro",
        "footer_home": "Beranda",
        "footer_privacy": "Privasi",
        "footer_contact": "Kontak",
        "back": "← Kembali ke semua panduan",
        "read_more": "Baca panduan →",
        "app_store": "Unduh di App Store",
        "play_store": "Dapatkan di Google Play",
        "index_title": "Blog GPX Viewer — Panduan GPX untuk hiking, bersepeda & navigasi",
        "index_desc": "Pelajari cara membuka file GPX, melihat rute di peta, mengikuti jalur hiking, dan membuat rute bersepeda. Panduan gratis dari tim GPX Viewer.",
        "index_h1": "Blog GPX Viewer",
        "index_sub": "Panduan untuk membuka, melihat, dan menavigasi file GPX di iPhone dan Android.",
    },
}

MISSING = {
    "pt": [
        "download-gpx-from-komoot",
        "import-gpx-garmin-devices",
        "how-to-use-gpx-files-hiking",
        "how-to-use-gpx-files-cycling",
        "view-gpx-without-internet",
        "share-gpx-iphone-android",
    ],
    "es": [
        "how-to-use-gpx-files-cycling",
        "view-gpx-without-internet",
        "share-gpx-iphone-android",
    ],
    "nl": ["view-gpx-without-internet", "share-gpx-iphone-android"],
    "pl": ["view-gpx-without-internet", "share-gpx-iphone-android"],
    "id": [
        "download-gpx-from-komoot",
        "import-gpx-garmin-devices",
        "how-to-use-gpx-files-hiking",
        "how-to-use-gpx-files-cycling",
        "view-gpx-without-internet",
        "share-gpx-iphone-android",
    ],
}

INDEX_LOCALES = ["pt", "es", "nl", "pl", "id"]
SKIP_TAGS = {"script", "style", "code", "pre"}
_cache: dict[tuple[str, str], str] = {}


def translate(text: str, target: str) -> str:
    text = text.strip()
    if not text or re.fullmatch(r"[\W\d_]+", text):
        return text
    key = (target, text)
    if key in _cache:
        return _cache[key]
    try:
        out = GoogleTranslator(source="en", target=target).translate(text)
    except Exception:
        time.sleep(0.5)
        out = GoogleTranslator(source="en", target=target).translate(text)
    _cache[key] = out
    time.sleep(0.05)
    return out


def translate_node(node, target: str) -> None:
    if isinstance(node, NavigableString):
        if isinstance(node.parent, Tag) and node.parent.name in SKIP_TAGS:
            return
        raw = str(node)
        if raw.strip():
            node.replace_with(translate(raw, target))
    elif isinstance(node, Tag):
        if node.name in SKIP_TAGS:
            return
        for child in list(node.children):
            translate_node(child, target)


def lang_dropdown(slug: str | None, locale: str, index: bool = False) -> str:
    links = []
    for code in LANG_CODES:
        active = ' class="is-active"' if code == locale else ""
        if index:
            href = "/blog/" if code == "en" else f"/{code}/blog/"
        else:
            href = f"/blog/{slug}.html" if code == "en" else f"/{code}/blog/{slug}.html"
        links.append(
            f'              <a href="{href}" hreflang="{code}" title="{LANG_LABELS[code]}"{active}>{code.upper()}</a>'
        )
    ui = UI[locale]
    return (
        f'          <details class="lang-dropdown">\n'
        f'            <summary aria-label="{ui["label"]}">{locale.upper()}</summary>\n'
        f'            <div class="lang-dropdown-menu" role="navigation" aria-label="{ui["label"]}">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        f"          </details>"
    )


def localize_article(locale: str, slug: str) -> None:
    src = ROOT / "blog" / f"{slug}.html"
    soup = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")
    ui = UI[locale]

    soup.html["lang"] = locale
    canonical = f"https://gpxviewerapp.com/{locale}/blog/{slug}.html"
    soup.find("link", rel="canonical")["href"] = canonical
    og_url = soup.find("meta", property="og:url")
    if og_url:
        og_url["content"] = canonical
    og_locale = soup.find("meta", property="og:locale")
    if og_locale:
        og_locale["content"] = OG_LOCALE[locale]
    elif soup.find("meta", property="og:title"):
        soup.find("meta", property="og:title").insert_after(
            soup.new_tag("meta", attrs={"property": "og:locale", "content": OG_LOCALE[locale]})
        )

    for tag in soup.find_all("link", rel="stylesheet"):
        if "style.css" in tag.get("href", ""):
            tag["href"] = "../../css/style.css"

    for tag in soup.find_all(["title", "meta"]):
        if tag.name == "title" or tag.get("name") in {"description", "keywords"} or tag.get("property") in {
            "og:title",
            "og:description",
        }:
            if tag.string:
                tag.string.replace_with(translate(tag.string, locale))
            elif tag.get("content"):
                tag["content"] = translate(tag["content"], locale)

    ld = soup.find("script", type="application/ld+json")
    if ld and ld.string and '"headline"' in ld.string:
        m = re.search(r'"headline":\s*"([^"]+)"', ld.string)
        if m:
            ld.string = ld.string.replace(m.group(1), translate(m.group(1), locale))
        ld.string = ld.string.replace('"inLanguage": "en"', f'"inLanguage": "{locale}"')

    brand = soup.select_one("a.brand")
    if brand:
        brand["href"] = "../"

    for a in soup.select("nav.nav-links a[href*='#features']"):
        a.string = ui["nav_features"]
    for a in soup.select("nav.nav-links a[href*='blog']"):
        if a.get("href") in {"../blog/", "/blog/"} or a.get("href", "").endswith("/blog/"):
            a.string = ui["nav_blog"]
    for a in soup.select("nav.nav-links a[href*='#pricing']"):
        a.string = ui["nav_pro"]

    dropdown = soup.select_one("details.lang-dropdown")
    if dropdown:
        dropdown.replace_with(BeautifulSoup(lang_dropdown(slug, locale), "html.parser"))

    for img in soup.select(".store-badges img"):
        alt = img.get("alt", "")
        if "App Store" in alt or "App" in alt:
            img["alt"] = ui["app_store"]
        elif "Google Play" in alt or "Play" in alt:
            img["alt"] = ui["play_store"]

    for tag in soup.select(".page-header h1, .page-header p, .article-content"):
        translate_node(tag, locale)

    cta = soup.select_one(".article-cta")
    if cta:
        for img in cta.select("img"):
            if "white" in img.get("src", ""):
                img["alt"] = ui["app_store"]
            else:
                img["alt"] = ui["play_store"]

    back = soup.select_one(".article-nav a")
    if back:
        back.string = ui["back"]
        back["href"] = "../blog/"

    for a, text in [
        (soup.select_one(".footer-links a[href='../']"), ui["footer_home"]),
        (soup.select_one(".footer-links a[href*='privacy']"), ui["footer_privacy"]),
        (soup.select_one("#footer-contact"), ui["footer_contact"]),
    ]:
        if a:
            a.string = text

    for a in soup.select(".footer-links a[href='../']"):
        a["href"] = "../"
    for a in soup.select(".footer-links a[href*='privacy']"):
        a["href"] = "../privacy.html"

    for tag in soup.find_all(["link", "script", "img"], src=True):
        if tag["src"].startswith("../"):
            tag["src"] = "../../" + tag["src"][3:]
    for tag in soup.find_all(["link", "a"], href=True):
        href = tag["href"]
        if href.startswith("../images/") or href.startswith("../css/") or href.startswith("../js/"):
            tag["href"] = "../" + href

    out = ROOT / locale / "blog" / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(str(soup), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")


def localize_index(locale: str) -> None:
    src = ROOT / "blog" / "index.html"
    soup = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")
    ui = UI[locale]

    soup.html["lang"] = locale
    canonical = f"https://gpxviewerapp.com/{locale}/blog/"
    soup.find("link", rel="canonical")["href"] = canonical

    soup.find("title").string = ui["index_title"]
    soup.find("meta", attrs={"name": "description"})["content"] = ui["index_desc"]
    soup.select_one(".page-header h1").string = ui["index_h1"]
    soup.select_one(".page-header p").string = ui["index_sub"]

    brand = soup.select_one("a.brand")
    brand["href"] = "../"

    for a in soup.select("nav.nav-links a[href*='#features']"):
        a.string = ui["nav_features"]
    for a in soup.select("nav.nav-links a[href*='blog']"):
        a.string = ui["nav_blog"]
    for a in soup.select("nav.nav-links a[href*='#pricing']"):
        a.string = ui["nav_pro"]

    dropdown = soup.select_one("details.lang-dropdown")
    if dropdown:
        dropdown.replace_with(BeautifulSoup(lang_dropdown(None, locale, index=True), "html.parser"))

    for card in soup.select(".blog-card"):
        for tag in card.select(".blog-tag, h2 a, p, .blog-read-more"):
            translate_node(tag, locale)
        link = card.select_one("h2 a")
        if link:
            slug = link["href"]
            link["href"] = slug
            card.select_one(".blog-read-more")["href"] = slug

    for a, text in [
        (soup.select_one(".footer-links a[href='../']"), ui["footer_home"]),
        (soup.select_one(".footer-links a[href*='privacy']"), ui["footer_privacy"]),
        (soup.select_one("#footer-contact"), ui["footer_contact"]),
    ]:
        if a:
            a.string = text

    for tag in soup.find_all(["link", "script", "img"], src=True):
        if tag["src"].startswith("../"):
            tag["src"] = "../../" + tag["src"][3:]
    for a in soup.select(".footer-links a[href*='privacy']"):
        a["href"] = "../privacy.html"

    out = ROOT / locale / "blog" / "index.html"
    out.write_text(str(soup), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")


def main() -> None:
    for locale, slugs in MISSING.items():
        for slug in slugs:
            localize_article(locale, slug)
    for locale in INDEX_LOCALES:
        localize_index(locale)
    print(f"Translation cache entries: {len(_cache)}")


if __name__ == "__main__":
    main()
