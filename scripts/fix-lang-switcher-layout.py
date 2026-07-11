#!/usr/bin/env python3
"""Embed static language switchers and fix header layout."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LANGS = [
    ("en", "/"),
    ("de", "/de/"),
    ("fr", "/fr/"),
    ("it", "/it/"),
    ("pt", "/pt/"),
    ("es", "/es/"),
]

LABELS = {
    "en": "Language",
    "de": "Sprache",
    "fr": "Langue",
    "it": "Lingua",
    "pt": "Idioma",
    "es": "Idioma",
}


def page_suffix(rel: Path) -> str:
    parts = rel.parts
    if parts[0] in {"de", "fr", "it", "pt", "es"}:
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
    links = []
    for code, path in LANGS:
        active = ' class="is-active"' if code == page_lang else ""
        links.append(
            f'            <a href="{href_for(path, suffix)}" hreflang="{code}"{active}>{code.upper()}</a>'
        )
    return (
        f'          <nav class="lang-switcher" aria-label="{aria}">\n'
        + "\n".join(links)
        + "\n          </nav>"
    )


def extract_lang(html: str) -> str:
    match = re.search(r'<html lang="([a-z]{2})"', html)
    return match.group(1) if match else "en"


def patch_header(html: str, switcher: str) -> str:
    # Remove JS placeholder or existing inline switcher inside nav-links.
    html = re.sub(r"\s*<div data-lang-switcher></div>\s*", "\n", html)
    html = re.sub(
        r"\s*<nav class=\"lang-switcher\"[^>]*>.*?</nav>\s*",
        "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )

    if '<div class="header-right">' in html:
        html = re.sub(
            r'(<div class="header-right">\s*)',
            r"\1" + switcher + "\n",
            html,
            count=1,
        )
        return html

    # Privacy-style header: brand + switcher only.
    privacy_match = re.search(
        r'(<header class="site-header">\s*<div class="container">\s*<a class="brand"[^>]*>.*?</a>\s*)<nav class="nav-links">',
        html,
        flags=re.DOTALL,
    )
    if privacy_match and "nav-links" in html[privacy_match.end() : privacy_match.end() + 200]:
        pass

    if re.search(
        r'<header class="site-header">\s*<div class="container">\s*<a class="brand"[^>]*>.*?</a>\s*(?!<div class="header-right">)',
        html,
        flags=re.DOTALL,
    ):
        html = re.sub(
            r'(<header class="site-header">\s*<div class="container">\s*<a class="brand"[^>]*>.*?</a>\s*)',
            r"\1" + '<div class="header-right">\n' + switcher + "\n",
            html,
            count=1,
            flags=re.DOTALL,
        )
        html = re.sub(
            r"(</nav>\s*)(</div>\s*</header>)",
            r"\1        </div>\n      \2",
            html,
            count=1,
        )
        return html

    return html


def ensure_lang_css(html: str, depth: str) -> str:
    href = f"{depth}css/lang.css"
    if href in html:
        return html
    return re.sub(
        r'(<link rel="stylesheet" href="[^"]*style\.css[^"]*" />)',
        r'\1\n    <link rel="stylesheet" href="' + href + '" />',
        html,
        count=1,
    )


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        html = path.read_text(encoding="utf-8")
        if "site-header" not in html:
            continue
        if "data-lang-switcher" not in html and "lang-switcher" not in html:
            continue

        depth = "../" * (len(rel.parts) - 1)
        page_lang = extract_lang(html)
        suffix = page_suffix(rel)
        switcher = build_switcher(page_lang, suffix)
        updated = patch_header(html, switcher)
        updated = ensure_lang_css(updated, depth)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {rel}")
            changed += 1
    print(f"Done. {changed} files updated.")


if __name__ == "__main__":
    main()
