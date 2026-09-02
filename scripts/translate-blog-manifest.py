#!/usr/bin/env python3
"""Batch-translate blog-articles.json from English to all site locales."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from deep_translator import GoogleTranslator

MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"
TARGETS = ["de", "fr", "it", "pt", "es", "nl", "pl", "id"]
SKIP_TAGS = {"script", "style", "code", "pre"}
TEXT_KEYS = [
    "title", "h1", "subtitle", "description", "keywords", "tag",
    "card_title", "card_desc", "date_display", "cta_text", "cta_title",
    "nav_features", "nav_blog", "nav_pro", "footer_home", "footer_privacy",
    "footer_contact", "back_link", "read_more", "app_store_alt", "play_store_alt",
]
_cache: dict[tuple[str, str], str] = {}


def tr(text: str, lang: str) -> str:
    text = text.strip()
    if not text:
        return text
    key = (lang, text)
    if key in _cache:
        return _cache[key]
    for attempt in range(3):
        try:
            out = GoogleTranslator(source="en", target=lang).translate(text)
            _cache[key] = out
            time.sleep(0.04)
            return out
        except Exception:
            time.sleep(0.8)
    _cache[key] = text
    return text


def batch_tr(texts: list[str], lang: str) -> list[str]:
    todo_idx = []
    todo_text = []
    results = list(texts)
    for i, t in enumerate(texts):
        k = (lang, t.strip())
        if k in _cache:
            results[i] = _cache[k]
        elif t.strip():
            todo_idx.append(i)
            todo_text.append(t)
    for start in range(0, len(todo_text), 40):
        chunk = todo_text[start : start + 40]
        idx_chunk = todo_idx[start : start + 40]
        try:
            outs = GoogleTranslator(source="en", target=lang).translate_batch(chunk)
        except Exception:
            outs = [tr(x, lang) for x in chunk]
        for i, out in zip(idx_chunk, outs):
            out = out if out else texts[i]
            results[i] = out
            _cache[(lang, texts[i].strip())] = out
        time.sleep(0.15)
    return results


def translate_html(html: str, lang: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    segments: list[str] = []
    nodes: list = []

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
    translated = batch_tr(segments, lang)
    for node, new in zip(nodes, translated):
        if new:
            node.replace_with(new)
    return str(soup)


def translate_dict(en: dict, lang: str) -> dict:
    out = {}
    for k, v in en.items():
        if k == "body":
            out[k] = translate_html(v, lang)
        elif isinstance(v, str) and k in TEXT_KEYS:
            out[k] = tr(v, lang)
        else:
            out[k] = v
    return out


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for lang in TARGETS:
        print(f"Translating to {lang}...")
        data["blog_index"][lang] = translate_dict(data["blog_index"]["en"], lang)

        for leg in data["legacy_articles"]:
            leg.setdefault("translations", {})
            leg["translations"][lang] = translate_dict(leg["translations"]["en"], lang)

        for art in data["articles"]:
            art.setdefault("translations", {})
            art["translations"][lang] = translate_dict(art["translations"]["en"], lang)

        MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  saved {lang} ({len(_cache)} cache entries)")

    print("Done.")


if __name__ == "__main__":
    main()
