#!/usr/bin/env python3
"""Update hreflang blocks and language switchers site-wide."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOCALE_PREFIXES = ("de", "fr", "it", "pt", "es", "nl", "pl", "id")

LANGS = [
    ("en", "/", "EN", "English"),
    ("de", "/de/", "DE", "Deutsch"),
    ("fr", "/fr/", "FR", "Français"),
    ("it", "/it/", "IT", "Italiano"),
    ("pt", "/pt/", "PT", "Português"),
    ("es", "/es/", "ES", "Español"),
    ("nl", "/nl/", "NL", "Nederlands"),
    ("pl", "/pl/", "PL", "Polski"),
    ("id", "/id/", "ID", "Indonesia"),
]

LABELS = {
    "en": "Language",
    "de": "Sprache",
    "fr": "Langue",
    "it": "Lingua",
    "pt": "Idioma",
    "es": "Idioma",
    "nl": "Taal",
    "pl": "Język",
    "id": "Bahasa",
}

BLOG_ARTICLES = [
    "what-is-a-gpx-file.html",
    "how-to-open-gpx-files-on-iphone.html",
    "how-to-view-gpx-on-a-map.html",
    "best-gpx-viewer-for-hiking.html",
    "how-to-create-gpx-cycling-routes.html",
]


def page_suffix(rel: Path) -> str:
    parts = rel.parts
    if parts[0] in LOCALE_PREFIXES:
        rest = Path(*parts[1:])
    else:
        rest = rel
    if rest.as_posix() == "index.html":
        return "/"
    return "/" + rest.as_posix()


def href_for(lang_path: str, suffix: str) -> str:
    if lang_path == "/":
        return suffix
    if suffix == "/":
        return lang_path
    return lang_path.rstrip("/") + suffix


def build_hreflang(suffix: str) -> str:
    lines = [
        f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com{href_for(path, suffix)}" />'
        for code, path, _, _ in LANGS
    ]
    default = suffix if suffix != "/" else "/"
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com{default}" />'
    )
    return "\n".join(lines)


def build_switcher(page_lang: str, suffix: str) -> str:
    aria = LABELS.get(page_lang, "Language")
    current_short = next(short for code, _, short, _ in LANGS if code == page_lang)
    links = []
    for code, path, short, name in LANGS:
        active = ' class="is-active"' if code == page_lang else ""
        links.append(
            f'              <a href="{href_for(path, suffix)}" hreflang="{code}" title="{name}"{active}>{short}</a>'
        )
    return (
        f'          <details class="lang-dropdown">\n'
        f'            <summary aria-label="{aria}">{current_short}</summary>\n'
        f'            <div class="lang-dropdown-menu" role="navigation" aria-label="{aria}">\n'
        + "\n".join(links)
        + "\n            </div>\n"
        f"          </details>"
    )


def extract_lang(html: str) -> str:
    match = re.search(r'<html lang="([a-z]{2})"', html)
    return match.group(1) if match else "en"


def replace_hreflang(html: str, suffix: str) -> str:
    block = build_hreflang(suffix)
    if re.search(r'<link rel="alternate" hreflang="en"', html):
        return re.sub(
            r'    <link rel="alternate" hreflang="en" href="[^"]+" />\n(?:    <link rel="alternate" hreflang="[^"]+" href="[^"]+" />\n)*    <link rel="alternate" hreflang="x-default" href="[^"]+" />',
            block,
            html,
            count=1,
        )
    return re.sub(
        r'(<link rel="canonical" href="[^"]+" />)',
        r"\1\n" + block,
        html,
        count=1,
    )


def patch_switcher(html: str, switcher: str) -> str:
    html = re.sub(
        r"\s*<details class=\"lang-dropdown\">.*?</details>\s*",
        "\n",
        html,
        flags=re.DOTALL,
    )
    if '<div class="store-badges' in html:
        return html.replace(
            '<div class="store-badges',
            switcher + "\n          <div class=\"store-badges",
            1,
        )
    if '<div class="header-right">' in html:
        return re.sub(
            r'(<div class="header-right">\s*)',
            r"\1" + switcher + "\n",
            html,
            count=1,
        )
    return html


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts or path.name == "streiv-credits.html":
            continue
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] not in (".",) and rel.suffix != ".html":
            continue

        html = path.read_text(encoding="utf-8")
        if "site-header" not in html and "canonical" not in html:
            continue

        suffix = page_suffix(rel)
        page_lang = extract_lang(html)
        updated = replace_hreflang(html, suffix)
        if "lang-dropdown" in html or "header-right" in html:
            updated = patch_switcher(updated, build_switcher(page_lang, suffix))
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {rel}")
            changed += 1
    print(f"Done. {changed} files updated.")


if __name__ == "__main__":
    main()
