#!/usr/bin/env python3
"""Generate dropdown language switchers for all site pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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


def page_suffix(rel: Path) -> str:
    parts = rel.parts
    if parts[0] in {"de", "fr", "it", "pt", "es", "nl", "pl", "id"}:
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


def depth_for(rel: Path) -> str:
    return "../" * (len(rel.parts) - 1)


def ensure_assets(html: str, depth: str) -> str:
    lang_css = f"{depth}css/lang.css?v=3"
    html = re.sub(r'\s*<link rel="stylesheet" href="[^"]*css/lang\.css(?:\?v=\d+)?" />\s*', "\n", html)
    html = re.sub(
        r'(<link rel="stylesheet" href="[^"]*style\.css[^"]*" />)',
        rf'\1\n    <link rel="stylesheet" href="{lang_css}" />',
        html,
        count=1,
    )

    dropdown_js = f"{depth}js/lang-dropdown.js"
    html = re.sub(r'\s*<script src="[^"]*lang-switcher\.js"></script>\s*', "\n", html)
    html = re.sub(r'\s*<script src="[^"]*languages\.js"></script>\s*', "\n", html)
    if dropdown_js not in html:
        html = html.replace("</body>", f'    <script src="{dropdown_js}"></script>\n  </body>', 1)
    return html


def patch_html(html: str, switcher: str) -> str:
    html = re.sub(r"\s*<div data-lang-switcher></div>\s*", "\n", html)
    html = re.sub(
        r"\s*<details class=\"lang-dropdown\">.*?</details>\s*",
        "\n",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"\s*<nav class=\"lang-switcher\"[^>]*>.*?</nav>\s*",
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

    if '<nav class="nav-links">' in html:
        return html.replace(
            '<nav class="nav-links">',
            "<nav class=\"nav-links\">\n" + switcher + "\n",
            1,
        )

    if '<div class="header-right">' in html:
        return re.sub(
            r'(<div class="header-right">\s*)',
            r"\1" + switcher + "\n",
            html,
            count=1,
        )

    return re.sub(
        r'(<header class="site-header">\s*<div class="container">\s*<a class="brand"[^>]*>.*?</a>\s*)',
        r"\1<div class=\"header-right\">\n" + switcher + "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts or "site-header" not in path.read_text(encoding="utf-8"):
            continue

        rel = path.relative_to(ROOT)
        html = path.read_text(encoding="utf-8")
        if "header-right" not in html and "lang-switcher" not in html and "lang-dropdown" not in html:
            continue

        page_lang = extract_lang(html)
        suffix = page_suffix(rel)
        switcher = build_switcher(page_lang, suffix)
        updated = patch_html(html, switcher)
        updated = ensure_assets(updated, depth_for(rel))
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {rel}")
            changed += 1

    print(f"Done. {changed} files updated.")


if __name__ == "__main__":
    main()
