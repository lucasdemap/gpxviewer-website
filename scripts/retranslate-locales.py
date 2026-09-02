#!/usr/bin/env python3
"""Re-translate blog articles with HTML-safe block translation (fixes broken h2/strong tags)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"
LOCALES = ["fr", "it", "pt", "es", "nl", "pl", "id"]
TEXT_KEYS = [
    "title", "h1", "subtitle", "description", "keywords", "tag",
    "card_title", "card_desc", "date_display", "cta_text",
]
BRAND = "GPX Viewer"

LOCALE_UI = {
    "fr": {
        "nav_features": "Fonctionnalités", "nav_blog": "Blog", "nav_pro": "Pro",
        "footer_home": "Accueil", "footer_privacy": "Confidentialité", "footer_contact": "Contact",
        "back_link": "← Retour à tous les guides", "read_more": "Lire le guide →",
        "app_store_alt": "Télécharger sur l'App Store", "play_store_alt": "Disponible sur Google Play",
        "cta_title": "Essayez GPX Viewer gratuitement",
        "index_title": "Blog GPX Viewer — Guides GPX pour randonnée, vélo et navigation",
        "index_desc": "Courts guides pour ouvrir, afficher et naviguer des fichiers GPX sur iPhone et Android.",
        "index_h1": "Blog GPX Viewer", "index_subtitle": "Guides GPX courts pour iPhone et Android.",
    },
    "it": {
        "nav_features": "Funzionalità", "nav_blog": "Blog", "nav_pro": "Pro",
        "footer_home": "Home", "footer_privacy": "Privacy", "footer_contact": "Contatto",
        "back_link": "← Torna a tutte le guide", "read_more": "Leggi la guida →",
        "app_store_alt": "Scarica su App Store", "play_store_alt": "Disponibile su Google Play",
        "cta_title": "Prova GPX Viewer gratis",
        "index_title": "Blog GPX Viewer — Guide GPX per escursionismo, ciclismo e navigazione",
        "index_desc": "Brevi guide per aprire, visualizzare e navigare file GPX su iPhone e Android.",
        "index_h1": "Blog GPX Viewer", "index_subtitle": "Guide GPX brevi per iPhone e Android.",
    },
    "pt": {
        "nav_features": "Funcionalidades", "nav_blog": "Blog", "nav_pro": "Pro",
        "footer_home": "Início", "footer_privacy": "Privacidade", "footer_contact": "Contacto",
        "back_link": "← Voltar a todos os guias", "read_more": "Ler guia →",
        "app_store_alt": "Descarregar na App Store", "play_store_alt": "Disponível no Google Play",
        "cta_title": "Experimente GPX Viewer grátis",
        "index_title": "Blog GPX Viewer — Guias GPX para caminhadas, ciclismo e navegação",
        "index_desc": "Guias curtos para abrir, ver e navegar ficheiros GPX no iPhone e Android.",
        "index_h1": "Blog GPX Viewer", "index_subtitle": "Guias GPX curtos para iPhone e Android.",
    },
    "es": {
        "nav_features": "Funciones", "nav_blog": "Blog", "nav_pro": "Pro",
        "footer_home": "Inicio", "footer_privacy": "Privacidad", "footer_contact": "Contacto",
        "back_link": "← Volver a todas las guías", "read_more": "Leer guía →",
        "app_store_alt": "Descargar en App Store", "play_store_alt": "Disponible en Google Play",
        "cta_title": "Prueba GPX Viewer gratis",
        "index_title": "Blog GPX Viewer — Guías GPX para senderismo, ciclismo y navegación",
        "index_desc": "Guías breves para abrir, ver y navegar archivos GPX en iPhone y Android.",
        "index_h1": "Blog GPX Viewer", "index_subtitle": "Guías GPX breves para iPhone y Android.",
    },
    "nl": {
        "nav_features": "Functies", "nav_blog": "Blog", "nav_pro": "Pro",
        "footer_home": "Home", "footer_privacy": "Privacy", "footer_contact": "Contact",
        "back_link": "← Terug naar alle gidsen", "read_more": "Gids lezen →",
        "app_store_alt": "Download in de App Store", "play_store_alt": "Downloaden via Google Play",
        "cta_title": "Probeer GPX Viewer gratis",
        "index_title": "GPX Viewer Blog — GPX-gidsen voor wandelen, fietsen en navigatie",
        "index_desc": "Korte gidsen om GPX-bestanden te openen, bekijken en navigeren op iPhone en Android.",
        "index_h1": "GPX Viewer Blog", "index_subtitle": "Korte GPX-gidsen voor iPhone en Android.",
    },
    "pl": {
        "nav_features": "Funkcje", "nav_blog": "Blog", "nav_pro": "Pro",
        "footer_home": "Strona główna", "footer_privacy": "Prywatność", "footer_contact": "Kontakt",
        "back_link": "← Wróć do wszystkich poradników", "read_more": "Czytaj poradnik →",
        "app_store_alt": "Pobierz z App Store", "play_store_alt": "Pobierz z Google Play",
        "cta_title": "Wypróbuj GPX Viewer za darmo",
        "index_title": "Blog GPX Viewer — poradniki GPX na wędrówki, rower i nawigację",
        "index_desc": "Krótkie poradniki o otwieraniu, przeglądaniu i nawigacji plików GPX na iPhone i Android.",
        "index_h1": "Blog GPX Viewer", "index_subtitle": "Krótkie poradniki GPX na iPhone i Android.",
    },
    "id": {
        "nav_features": "Fitur", "nav_blog": "Blog", "nav_pro": "Pro",
        "footer_home": "Beranda", "footer_privacy": "Privasi", "footer_contact": "Kontak",
        "back_link": "← Kembali ke semua panduan", "read_more": "Baca panduan →",
        "app_store_alt": "Unduh di App Store", "play_store_alt": "Dapatkan di Google Play",
        "cta_title": "Coba GPX Viewer gratis",
        "index_title": "Blog GPX Viewer — Panduan GPX untuk hiking, bersepeda & navigasi",
        "index_desc": "Panduan singkat untuk membuka, melihat, dan menavigasi file GPX di iPhone dan Android.",
        "index_h1": "Blog GPX Viewer", "index_subtitle": "Panduan GPX singkat untuk iPhone dan Android.",
    },
}

_cache: dict[tuple[str, str], str] = {}
_PH = "\uE000{}\uE001"


def tr(text: str, lang: str) -> str:
    text = text.strip()
    if not text:
        return text
    key = (lang, text)
    if key in _cache:
        return _cache[key]
    for _ in range(4):
        try:
            out = GoogleTranslator(source="en", target=lang).translate(text) or text
            _cache[key] = out
            time.sleep(0.04)
            return out
        except Exception:
            time.sleep(0.6)
    _cache[key] = text
    return text


def protect_tags(html: str) -> tuple[str, list[str]]:
    tags: list[str] = []

    def repl(m: re.Match) -> str:
        tags.append(m.group(0))
        return _PH.format(len(tags) - 1)

    return re.sub(r"<[^>]+>", repl, html), tags


def restore_tags(text: str, tags: list[str]) -> str:
    for i, tag in enumerate(tags):
        text = text.replace(_PH.format(i), tag)
        text = text.replace(f" {i} ", tag)
        text = text.replace(f"({i})", tag)
    return text


def normalize_html(html: str) -> str:
    html = re.sub(r"Visionneuse GPX|Visualiseur GPX|Visualizador GPX|GPX-viewer", BRAND, html, flags=re.I)
    html = re.sub(r"([^\s>])(<(?!/)(?:a|strong|code|em)\b)", r"\1 \2", html)
    html = re.sub(r"(</(?:a|strong|code|em)>)([^\s<,.;:!?\)])", r"\1 \2", html)
    html = re.sub(r"\s{2,}", " ", html)
    return html.strip()


def translate_block(html: str, lang: str) -> str:
    protected, tags = protect_tags(html.strip())
    translated = tr(protected, lang)
    restored = restore_tags(translated, tags)
    return normalize_html(restored)


def translate_body(en_body: str, lang: str) -> str:
    soup = BeautifulSoup(en_body, "html.parser")
    parts: list[str] = []
    for el in soup.children:
        if not isinstance(el, Tag):
            continue
        if el.name == "ul":
            lis = []
            for li in el.find_all("li", recursive=False):
                lis.append(f"  <li>{translate_block(li.decode_contents(), lang)}</li>")
            parts.append("          <ul>\n" + "\n".join(lis) + "\n          </ul>")
        else:
            inner = translate_block(el.decode_contents(), lang)
            parts.append(f"          <{el.name}>{inner}</{el.name}>")
    return "\n\n".join(parts)


def translate_entry(en: dict, lang: str, ui: dict) -> dict:
    out = {**ui}
    for key in TEXT_KEYS:
        if key in en:
            out[key] = tr(en[key], lang)
    out["body"] = translate_body(en["body"], lang)
    return out


def retranslate_locale(data: dict, lang: str) -> None:
    ui = LOCALE_UI[lang]
    data["blog_index"][lang] = {
        **ui,
        "title": ui["index_title"],
        "description": ui["index_desc"],
        "h1": ui["index_h1"],
        "subtitle": ui["index_subtitle"],
        "nav_features": ui["nav_features"],
        "nav_blog": ui["nav_blog"],
        "nav_pro": ui["nav_pro"],
        "footer_home": ui["footer_home"],
        "footer_privacy": ui["footer_privacy"],
        "footer_contact": ui["footer_contact"],
    }
    for leg in data["legacy_articles"]:
        en = leg["translations"]["en"]
        leg["translations"][lang] = {
            "tag": tr(en["tag"], lang),
            "card_title": tr(en["card_title"], lang),
            "card_desc": tr(en["card_desc"], lang),
            "read_more": ui["read_more"],
        }
    for i, art in enumerate(data["articles"], 1):
        en = art["translations"]["en"]
        art["translations"][lang] = translate_entry(en, lang, {
            k: ui[k] for k in ui if k.startswith(("nav_", "footer_", "back_", "read_", "app_", "play_", "cta_"))
        })
        print(f"  [{lang}] {i}/20 {art['slug']}", flush=True)


def main() -> None:
    langs = LOCALES if len(sys.argv) < 2 else [a for a in sys.argv[1:] if a in LOCALES]
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for lang in langs:
        print(f"\n=== {lang.upper()} ===", flush=True)
        retranslate_locale(data, lang)
        MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "render-blog.py"), "--locales", lang],
            check=True,
            cwd=ROOT,
        )
    print("\nDone.")


if __name__ == "__main__":
    main()
