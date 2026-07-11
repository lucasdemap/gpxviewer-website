#!/usr/bin/env python3
"""Replace cycling feature icon and remove Streiv branding site-wide."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_BIKE_ICON = (
    '<svg viewBox="0 0 24 24"><path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm14.5 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM12 5.5c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3zM8.5 12c-.83 0-1.5.67-1.5 1.5S7.67 15 8.5 15 10 14.33 10 13.5 9.33 12 8.5 12zm7 0c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zM12 16c-1.5 0-2.85.75-3.66 1.91l1.43 1.43A3.98 3.98 0 0112 18c1.05 0 2.01.4 2.73 1.05l1.43-1.43A5.978 5.978 0 0012 16z"/></svg>'
)

NEW_BIKE_ICON = (
    '<svg viewBox="0 0 24 24"><path d="M18.29 5.71a2 2 0 0 0-2.83 0L14 7.17V7H9.5L8 3H4v2h3.06l1.5 4.5H7v2h2.36l1.06 3.19-.47.47A3.994 3.994 0 0 0 7 19a4 4 0 0 0 8 0c0-.64-.15-1.24-.42-1.78l2.07-2.07a2 2 0 0 0 0-2.83zM7 19a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm10 0a2 2 0 1 1 0-4 2 2 0 0 1 0 4zM6.29 7.29 7.5 6.08 8.29 7H6.29z"/></svg>'
)

CONTACT_EMAIL = "lucas@streiv.app"

REPLACEMENTS = [
    (OLD_BIKE_ICON, NEW_BIKE_ICON),
    ('content="Streiv"', 'content="GPX Viewer"'),
    ('"name": "Streiv"', '"name": "GPX Viewer"'),
    ("Streiv · GPX Viewer", "GPX Viewer"),
    (" · Streiv</p>", "</p>"),
    ("lucas@streiv.app", CONTACT_EMAIL),
    # English privacy
    ("Privacy policy for GPX Viewer by Streiv.", "Privacy policy for GPX Viewer."),
    (
        'GPX Viewer (“the app”) is developed by Streiv.',
        "GPX Viewer (“the app”) is developed by the GPX Viewer team.",
    ),
    # German privacy
    ("Datenschutzerklärung für GPX Viewer von Streiv.", "Datenschutzerklärung für GPX Viewer."),
    (
        "GPX Viewer („die App“) wird von Streiv entwickelt.",
        "GPX Viewer („die App“) wird vom GPX Viewer-Team entwickelt.",
    ),
    # French privacy
    (
        "Politique de confidentialité de GPX Viewer par Streiv.",
        "Politique de confidentialité de GPX Viewer.",
    ),
    (
        "GPX Viewer (« l'application ») est développée par Streiv.",
        "GPX Viewer (« l'application ») est développée par l'équipe GPX Viewer.",
    ),
    # Italian privacy
    (
        "Informativa sulla privacy di GPX Viewer di Streiv.",
        "Informativa sulla privacy di GPX Viewer.",
    ),
    (
        "GPX Viewer («l'app») è sviluppata da Streiv.",
        "GPX Viewer («l'app») è sviluppata dal team GPX Viewer.",
    ),
    # Portuguese privacy
    (
        "Política de privacidade do GPX Viewer da Streiv.",
        "Política de privacidade do GPX Viewer.",
    ),
    (
        "O GPX Viewer («a app») é desenvolvido pela Streiv.",
        "O GPX Viewer («a app») é desenvolvido pela equipa GPX Viewer.",
    ),
    # Spanish privacy
    (
        "Política de privacidad de GPX Viewer de Streiv.",
        "Política de privacidad de GPX Viewer.",
    ),
    (
        'GPX Viewer ("la app") es desarrollada por Streiv.',
        'GPX Viewer ("la app") es desarrollada por el equipo de GPX Viewer.',
    ),
    (
        "GPX Viewer (« la app ») es desarrollada por Streiv.",
        "GPX Viewer (« la app ») es desarrollada por el equipo de GPX Viewer.",
    ),
]


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    patterns = ("*.html", "*.js")
    changed = 0
    for pattern in patterns:
        for path in ROOT.rglob(pattern):
            if ".git" in path.parts:
                continue
            if patch_file(path):
                print(f"Updated {path.relative_to(ROOT)}")
                changed += 1
    print(f"Done. {changed} files updated.")


if __name__ == "__main__":
    main()
