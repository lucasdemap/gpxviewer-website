#!/usr/bin/env python3
"""Translate blog-articles.json to one locale from English, then render HTML."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"
TEXT_KEYS = [
    "title", "h1", "subtitle", "description", "keywords", "tag",
    "card_title", "card_desc", "date_display", "cta_text", "cta_title",
    "nav_features", "nav_blog", "nav_pro", "footer_home", "footer_privacy",
    "footer_contact", "back_link", "read_more", "app_store_alt", "play_store_alt",
]
SKIP_TAGS = {"script", "style", "code", "pre"}

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


def tr(text: str, lang: str, cache: dict) -> str:
    text = text.strip()
    if not text:
        return text
    key = (lang, text)
    if key in cache:
        return cache[key]
    for _ in range(3):
        try:
            out = GoogleTranslator(source="en", target=lang).translate(text) or text
            cache[key] = out
            time.sleep(0.03)
            return out
        except Exception:
            time.sleep(0.5)
    cache[key] = text
    return text


def batch_tr(texts: list[str], lang: str, cache: dict) -> list[str]:
    results = list(texts)
    todo_i, todo_t = [], []
    for i, t in enumerate(texts):
        k = (lang, t.strip())
        if k in cache:
            results[i] = cache[k]
        elif t.strip():
            todo_i.append(i)
            todo_t.append(t)
    for start in range(0, len(todo_t), 50):
        chunk = todo_t[start : start + 50]
        idx = todo_i[start : start + 50]
        try:
            outs = GoogleTranslator(source="en", target=lang).translate_batch(chunk)
        except Exception:
            outs = [tr(x, lang, cache) for x in chunk]
        for i, out in zip(idx, outs):
            results[i] = out or texts[i]
            cache[(lang, texts[i].strip())] = results[i]
        time.sleep(0.1)
    return results


def translate_html(html: str, lang: str, cache: dict) -> str:
    soup = BeautifulSoup(html, "html.parser")
    segments, nodes = [], []

    def walk(node):
        if isinstance(node, NavigableString):
            if isinstance(node.parent, Tag) and node.parent.name in SKIP_TAGS:
                return
            s = str(node)
            if s.strip():
                segments.append(s)
                nodes.append(node)
        elif isinstance(node, Tag):
            if node.name in SKIP_TAGS:
                return
            for child in list(node.children):
                walk(child)

    walk(soup)
    if not segments:
        return html
    for node, new in zip(nodes, batch_tr(segments, lang, cache)):
        if new:
            node.replace_with(new)
    return str(soup)


def translate_entry(en: dict, lang: str, cache: dict, ui: dict) -> dict:
    out = dict(ui)
    for k, v in en.items():
        if k in out:
            continue
        if k == "body":
            out[k] = translate_html(v, lang, cache)
        elif isinstance(v, str) and k in TEXT_KEYS:
            out[k] = tr(v, lang, cache)
        else:
            out[k] = v
    return out


def translate_locale(lang: str) -> None:
    if lang == "de":
        print("Use add-de-translations.py for German.")
        return
    if lang not in LOCALE_UI:
        raise SystemExit(f"Unknown locale: {lang}")

    ui = LOCALE_UI[lang]
    cache: dict = {}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    index_en = data["blog_index"]["en"]
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

    ui_keys = {
        k: ui[k]
        for k in TEXT_KEYS
        if k in ui and k not in {"title", "h1", "subtitle", "description", "keywords", "tag",
                                  "card_title", "card_desc", "date_display", "cta_text"}
    }

    for leg in data["legacy_articles"]:
        en = leg["translations"]["en"]
        leg.setdefault("translations", {})[lang] = translate_entry(en, lang, cache, {
            "read_more": ui["read_more"],
        })

    for i, art in enumerate(data["articles"], 1):
        en = art["translations"]["en"]
        art.setdefault("translations", {})[lang] = translate_entry(en, lang, cache, ui_keys)
        print(f"  [{lang}] article {i}/20: {art['slug']}", flush=True)

    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved manifest for {lang}")

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "render-blog.py"), "--locales", lang],
        check=True,
        cwd=ROOT,
    )
    print(f"Rendered {lang} blog HTML")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: translate-one-locale.py <fr|it|pt|es|nl|pl|id|all>")
    arg = sys.argv[1]
    langs = ["fr", "it", "pt", "es", "nl", "pl", "id"] if arg == "all" else [arg]
    for lang in langs:
        print(f"\n=== {lang.upper()} ===", flush=True)
        translate_locale(lang)
    print("\nDone.")


if __name__ == "__main__":
    main()
