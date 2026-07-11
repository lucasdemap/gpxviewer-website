#!/usr/bin/env python3
"""Add hreflang tags and language switcher to English pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HREFLANG_HOME = """
    <link rel="alternate" hreflang="en" href="https://gpxviewerapp.com/" />
    <link rel="alternate" hreflang="de" href="https://gpxviewerapp.com/de/" />
    <link rel="alternate" hreflang="fr" href="https://gpxviewerapp.com/fr/" />
    <link rel="alternate" hreflang="it" href="https://gpxviewerapp.com/it/" />
    <link rel="alternate" hreflang="pt" href="https://gpxviewerapp.com/pt/" />
    <link rel="alternate" hreflang="es" href="https://gpxviewerapp.com/es/" />
    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/" />"""

HREFLANG_PRIVACY = """
    <link rel="alternate" hreflang="en" href="https://gpxviewerapp.com/privacy.html" />
    <link rel="alternate" hreflang="de" href="https://gpxviewerapp.com/de/privacy.html" />
    <link rel="alternate" hreflang="fr" href="https://gpxviewerapp.com/fr/privacy.html" />
    <link rel="alternate" hreflang="it" href="https://gpxviewerapp.com/it/privacy.html" />
    <link rel="alternate" hreflang="pt" href="https://gpxviewerapp.com/pt/privacy.html" />
    <link rel="alternate" hreflang="es" href="https://gpxviewerapp.com/es/privacy.html" />
    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/privacy.html" />"""

HREFLANG_BLOG_INDEX = """
    <link rel="alternate" hreflang="en" href="https://gpxviewerapp.com/blog/" />
    <link rel="alternate" hreflang="de" href="https://gpxviewerapp.com/de/blog/" />
    <link rel="alternate" hreflang="fr" href="https://gpxviewerapp.com/fr/blog/" />
    <link rel="alternate" hreflang="it" href="https://gpxviewerapp.com/it/blog/" />
    <link rel="alternate" hreflang="pt" href="https://gpxviewerapp.com/pt/blog/" />
    <link rel="alternate" hreflang="es" href="https://gpxviewerapp.com/es/blog/" />
    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/" />"""

BLOG_ARTICLES = [
    "what-is-a-gpx-file.html",
    "how-to-open-gpx-files-on-iphone.html",
    "how-to-view-gpx-on-a-map.html",
    "best-gpx-viewer-for-hiking.html",
    "how-to-create-gpx-cycling-routes.html",
]

LANG_SWITCHER = '          <div data-lang-switcher></div>\n'

LANG_SCRIPTS_ROOT = """    <script src="js/languages.js"></script>
    <script src="js/lang-switcher.js"></script>"""

LANG_SCRIPTS_BLOG = """    <script src="../js/languages.js"></script>
    <script src="../js/lang-switcher.js"></script>"""


def hreflang_blog(article: str) -> str:
    lines = [
        f'    <link rel="alternate" hreflang="en" href="https://gpxviewerapp.com/blog/{article}" />',
    ]
    for code in ("de", "fr", "it", "pt", "es"):
        lines.append(
            f'    <link rel="alternate" hreflang="{code}" href="https://gpxviewerapp.com/{code}/blog/{article}" />'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://gpxviewerapp.com/blog/{article}" />'
    )
    return "\n" + "\n".join(lines)


def insert_after_canonical(content: str, block: str) -> str:
    if "hreflang=" in content:
        return content
    return re.sub(
        r'(<link rel="canonical" href="[^"]+" />)',
        r"\1" + block,
        content,
        count=1,
    )


def add_lang_css(content: str, depth: str) -> str:
    css_href = f"{depth}css/lang.css"
    if css_href in content:
        return content
    return re.sub(
        r'(<link rel="stylesheet" href="[^"]*style\.css[^"]*" />)',
        r'\1\n    <link rel="stylesheet" href="' + css_href + '" />',
        content,
        count=1,
    )


def add_switcher_to_nav(content: str) -> str:
    if "data-lang-switcher" in content:
        return content
    return content.replace(
        '        <nav class="nav-links">\n',
        '        <nav class="nav-links">\n' + LANG_SWITCHER,
        1,
    )


def add_scripts_before_body_end(content: str, scripts: str) -> str:
    if "lang-switcher.js" in content:
        return content
    return content.replace("  </body>", scripts + "\n  </body>", 1)


def patch_file(path: Path, hreflang: str, css_depth: str, scripts: str, nav: bool = True) -> None:
    text = path.read_text(encoding="utf-8")
    text = insert_after_canonical(text, hreflang)
    text = add_lang_css(text, css_depth)
    if nav:
        text = add_switcher_to_nav(text)
    text = add_scripts_before_body_end(text, scripts)
    path.write_text(text, encoding="utf-8")
    print(f"Patched {path.relative_to(ROOT)}")


def patch_privacy(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = insert_after_canonical(text, HREFLANG_PRIVACY)
    text = add_lang_css(text, "")
    if "data-lang-switcher" not in text:
        text = text.replace(
            "        </a>\n      </div>\n    </header>",
            "        </a>\n        <div data-lang-switcher></div>\n      </div>\n    </header>",
            1,
        )
    text = add_scripts_before_body_end(text, LANG_SCRIPTS_ROOT)
    path.write_text(text, encoding="utf-8")
    print(f"Patched {path.relative_to(ROOT)}")


def main() -> None:
    patch_file(ROOT / "index.html", HREFLANG_HOME, "", LANG_SCRIPTS_ROOT)
    patch_privacy(ROOT / "privacy.html")
    patch_file(ROOT / "blog/index.html", HREFLANG_BLOG_INDEX, "../", LANG_SCRIPTS_BLOG)
    for article in BLOG_ARTICLES:
        patch_file(
            ROOT / "blog" / article,
            hreflang_blog(article),
            "../",
            LANG_SCRIPTS_BLOG,
        )


if __name__ == "__main__":
    main()
