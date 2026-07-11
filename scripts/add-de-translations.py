#!/usr/bin/env python3
"""Add German translations to blog-articles.json (no API — instant)."""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent / "blog-articles.json"

DE_UI = {
    "nav_features": "Funktionen",
    "nav_blog": "Blog",
    "nav_pro": "Pro",
    "footer_home": "Startseite",
    "footer_privacy": "Datenschutz",
    "footer_contact": "Kontakt",
    "back_link": "← Zurück zu allen Ratgebern",
    "read_more": "Ratgeber lesen →",
    "app_store_alt": "Im App Store laden",
    "play_store_alt": "Bei Google Play herunterladen",
    "cta_title": "GPX Viewer kostenlos testen",
}

BLOG_INDEX_DE = {
    **DE_UI,
    "title": "GPX Viewer Blog — GPX-Ratgeber für Wandern, Radfahren & Navigation",
    "description": "Kurze Anleitungen zum Öffnen, Anzeigen und Navigieren von GPX-Dateien auf iPhone und Android.",
    "h1": "GPX Viewer Blog",
    "subtitle": "Kurze GPX-Ratgeber für iPhone und Android.",
}

LEGACY_DE = {
    "what-is-a-gpx-file": ("Einsteiger", "Was ist eine GPX-Datei?", "Erfahren Sie, was GPX-Dateien sind und wie GPS-Tracks funktionieren."),
    "how-to-open-gpx-files-on-iphone": ("iPhone & Android", "GPX-Dateien auf iPhone und Android öffnen", "GPX aus Mail, Dateien oder Safari in GPX Viewer importieren."),
    "how-to-view-gpx-on-a-map": ("Karten", "GPX-Routen auf einer Karte anzeigen", "Wegpunkte, Höhe und Distanz auf interaktiven Karten sehen."),
    "best-gpx-viewer-for-hiking": ("Wandern", "Bester GPX Viewer fürs Wandern", "Trail-GPX-Tracks sicher auf dem Handy folgen."),
    "how-to-create-gpx-cycling-routes": ("Radfahren", "GPX-Radrouten erstellen", "Radrouten planen und GPX-Dateien zum Teilen exportieren."),
}

# slug -> German translation dict (metadata + body)
ARTICLES_DE: dict[str, dict] = {
    "what-is-a-gpx-file-reader": {
        "title": "Was ist ein GPX-Datei-Reader?",
        "h1": "Was ist ein GPX-Datei-Reader?",
        "subtitle": "Wie GPX-Reader GPS-Daten in Karten verwandeln.",
        "description": "Ein GPX-Datei-Reader öffnet .gpx-Dateien und zeigt Tracks auf einer Karte mit Distanz und Höhe. So funktionieren Reader — testen Sie GPX Viewer auf iPhone und Android.",
        "keywords": "gpx datei reader, gpx reader, gpx datei lesen",
        "tag": "Einsteiger",
        "card_title": "Was ist ein GPX-Datei-Reader?",
        "card_desc": "Wie GPX-Reader Tracks parsen und auf einer Karte anzeigen.",
        "date_display": "12. Juli 2026",
        "cta_text": "Öffnen Sie jede .gpx-Datei in GPX Viewer — kostenlos auf iPhone und Android.",
        "body": """          <p>Ein <strong>GPX-Datei-Reader</strong> öffnet <code>.gpx</code>-Dateien und zeichnet die Route auf einer Karte mit Distanz, Höhe und Wegpunkten. Texteditoren zeigen rohes XML — ein Reader wie <a href="../">GPX Viewer</a> ist das, was Wanderer und Radfahrer wirklich brauchen.</p>

          <h2>Was ein guter Reader kann</h2>

          <ul>
            <li>Liest Trackpunkte und Wegpunkte aus der GPX-Datei</li>
            <li>Zeigt die Route auf Standard-, Satelliten- oder Hybridkarten</li>
            <li>Berechnet Distanz und Höhenmeter automatisch</li>
          </ul>

          <p>Neu im Format? Lesen Sie <a href="what-is-a-gpx-file.html">was ist eine GPX-Datei</a>, dann <a href="how-to-open-gpx-file-any-device.html">GPX auf jedem Gerät öffnen</a>.</p>""",
    },
    "how-to-open-gpx-files-on-android": {
        "title": "GPX-Dateien auf Android öffnen",
        "h1": "GPX-Dateien auf Android öffnen",
        "subtitle": "GPX aus Gmail, Drive oder Downloads in Sekunden importieren.",
        "description": "GPX-Dateien auf Android mit GPX Viewer öffnen. Import aus Gmail, WhatsApp, Drive oder der Dateien-App.",
        "keywords": "gpx android öffnen, gpx viewer android",
        "tag": "Android",
        "card_title": "GPX-Dateien auf Android öffnen",
        "card_desc": "GPX aus Gmail, Drive oder Downloads in GPX Viewer importieren.",
        "date_display": "13. Juli 2026",
        "cta_text": "GPX Viewer bei Google Play holen und jede geteilte .gpx-Datei öffnen.",
        "body": """          <p>Um eine GPX-Datei auf Android zu öffnen, tippen Sie auf den Anhang, wählen Sie <strong>Teilen</strong> oder <strong>Öffnen mit</strong> und picken Sie <a href="../">GPX Viewer</a>. Funktioniert mit Gmail, WhatsApp, Google Drive und der Dateien-App.</p>

          <h2>Schritt für Schritt</h2>

          <ul>
            <li>.gpx-Datei erhalten oder herunterladen</li>
            <li>Tippen → Öffnen mit → GPX Viewer</li>
            <li>Karte, Distanz und Höhenprofil prüfen</li>
          </ul>

          <p>Probleme? Siehe <a href="gpx-file-not-opening-fixes.html">GPX öffnet nicht — Lösungen</a>. iPhone: <a href="how-to-open-gpx-files-on-iphone.html">GPX auf iPhone öffnen</a>.</p>""",
    },
    "how-to-open-gpx-file-any-device": {
        "title": "GPX-Datei auf jedem Gerät öffnen",
        "h1": "GPX-Datei auf jedem Gerät öffnen",
        "subtitle": "Handy, Computer und GPS-Geräte — was .gpx-Dateien öffnet.",
        "description": "GPX-Dateien auf iPhone, Android, Mac, Windows und GPS-Geräten öffnen. GPX Viewer ist die schnellste Option auf dem Handy.",
        "keywords": "gpx datei öffnen, was öffnet gpx",
        "tag": "Einsteiger",
        "card_title": "GPX-Datei auf jedem Gerät öffnen",
        "card_desc": "Was .gpx-Dateien auf Handys, Computern und GPS-Geräten öffnet.",
        "date_display": "14. Juli 2026",
        "cta_text": "GPX Viewer laden und GPX-Dateien auf dem Handy mit einem Tipp öffnen.",
        "body": """          <p>GPX ist ein offener Standard — viele Apps lesen ihn. Auf <strong>iPhone und Android</strong> ist <a href="../">GPX Viewer</a> am schnellsten: Datei teilen, App wählen, Route erscheint sofort.</p>

          <h2>Nach Gerät</h2>

          <ul>
            <li><strong>iPhone / Android</strong> — GPX Viewer (empfohlen) oder Teilen-Import</li>
            <li><strong>Mac / Windows</strong> — Garmin BaseCamp, QGIS oder Google Earth</li>
            <li><strong>GPS-Uhren</strong> — Import über Garmin Connect oder Hersteller-App</li>
          </ul>

          <p>Siehe <a href="how-to-open-gpx-files-on-android.html">Android</a> und <a href="how-to-open-gpx-files-on-iphone.html">iPhone</a> für mobile Schritte.</p>""",
    },
    "best-ways-view-gpx-online-offline": {
        "title": "GPX online und offline anzeigen",
        "h1": "GPX online und offline anzeigen",
        "subtitle": "Web-Tools vs. Apps — und wann Offline-Karten nötig sind.",
        "description": "Online- und Offline-GPX-Viewer vergleichen. GPX Viewer auf dem Handy, optional mit Offline-Karten in Pro.",
        "keywords": "gpx anzeigen, gpx viewer online, offline gpx",
        "tag": "Karten",
        "card_title": "GPX online und offline anzeigen",
        "card_desc": "Web-Viewer vs. mobile Apps für GPX-Routen.",
        "date_display": "15. Juli 2026",
        "cta_text": "GPX-Routen auf dem Handy ansehen — mit Offline-Karten in GPX Viewer Pro.",
        "body": """          <p><strong>Online:</strong> Browser-Tools wie GPSVisualizer funktionieren für schnelle Vorschauen, brauchen aber Internet für Kartenkacheln. <strong>Offline:</strong> Eine App mit gespeicherten Karten ist in abgelegenen Gebieten unverzichtbar.</p>

          <h2>Unsere Empfehlung</h2>

          <p>Nutzen Sie <a href="../">GPX Viewer</a> auf iPhone oder Android. Pro bietet <a href="view-gpx-without-internet.html">Offline-Karten</a>, wenn der Empfang ausfällt.</p>

          <p>Weiter: <a href="how-to-view-gpx-on-a-map.html">GPX auf Karte anzeigen</a> · <a href="what-is-a-gpx-file-reader.html">GPX-Reader</a></p>""",
    },
    "gpx-file-not-opening-fixes": {
        "title": "GPX-Datei öffnet nicht? Lösungen",
        "h1": "GPX-Datei öffnet nicht?",
        "subtitle": "Fehlerhafte Downloads, falsche Formate und Import-Probleme beheben.",
        "description": "GPX-Datei öffnet nicht? Endung prüfen, neu laden, KML konvertieren oder in GPX Viewer öffnen.",
        "keywords": "gpx öffnet nicht, gpx datei fehler",
        "tag": "Fehlerbehebung",
        "card_title": "GPX-Datei öffnet nicht? Lösungen",
        "card_desc": "GPX-Dateien reparieren, die sich nicht öffnen lassen.",
        "date_display": "16. Juli 2026",
        "cta_text": "GPX-Datei in GPX Viewer öffnen — kostenloser Import auf iPhone und Android.",
        "body": """          <p>Wenn eine GPX-Datei nicht öffnet, liegt es meist an einem fehlerhaften Download, falschem Dateityp oder fehlender App für .gpx.</p>

          <h2>Schnelle Lösungen</h2>

          <ul>
            <li>Endung <code>.gpx</code> prüfen (nicht .xml oder .kml)</li>
            <li>Neu laden oder aus Strava/Komoot neu exportieren</li>
            <li>Mit <a href="../">GPX Viewer</a> über Teilen → Öffnen mit öffnen</li>
            <li>Prüfen, ob die Datei leer ist (0 KB)</li>
          </ul>

          <p>Falsches Format? <a href="gpx-vs-kml.html">GPX vs KML</a> und <a href="gpx-vs-tcx.html">GPX vs TCX</a>.</p>""",
    },
    "gpx-file-format-tracks-routes-waypoints": {
        "title": "GPX-Format: Tracks, Routen, Wegpunkte",
        "h1": "GPX Tracks, Routen und Wegpunkte",
        "subtitle": "Die drei Bausteine jeder .gpx-Datei.",
        "description": "GPX-Tracks, -Routen und -Wegpunkte verstehen. So zeigt GPX Viewer jedes Element an.",
        "keywords": "gpx tracks routen wegpunkte, gpx format",
        "tag": "Einsteiger",
        "card_title": "GPX Tracks, Routen und Wegpunkte",
        "card_desc": "Tracks, Routen und Wegpunkte einfach erklärt.",
        "date_display": "17. Juli 2026",
        "cta_text": "Jede GPX-Datei in GPX Viewer öffnen und Tracks auf der Karte sehen.",
        "body": """          <p>Jede GPX-Datei kann <strong>Tracks</strong> (GPS-Aufzeichnungen), <strong>Routen</strong> (geplante Wege) und <strong>Wegpunkte</strong> (benannte Punkte wie Gipfel oder Parkplätze) enthalten.</p>

          <h2>Was bedeutet was</h2>

          <ul>
            <li><strong>Track</strong> — aufgezeichneter GPS-Pfad, am häufigsten geteilt</li>
            <li><strong>Route</strong> — geplante Punktfolge, evtl. ohne Höhendetails</li>
            <li><strong>Wegpunkt</strong> — ein benannter Ort auf der Karte</li>
          </ul>

          <p><a href="../">GPX Viewer</a> zeigt alle drei. Start: <a href="what-is-a-gpx-file.html">Was ist GPX</a>.</p>""",
    },
    "gpx-vs-kml": {
        "title": "GPX vs KML: Der Unterschied",
        "h1": "GPX vs KML",
        "subtitle": "Welches Format für Wandern, Radfahren und GPS-Geräte.",
        "description": "GPX vs KML im Vergleich. GPX eignet sich für GPS-Tracks und Navigations-Apps. KML für Google Earth.",
        "keywords": "gpx vs kml",
        "tag": "Formate",
        "card_title": "GPX vs KML",
        "card_desc": "Welches Format für Trails, Räder und GPS-Apps?",
        "date_display": "18. Juli 2026",
        "cta_text": "GPX Viewer öffnet .gpx-Dateien nativ auf iPhone und Android.",
        "body": """          <p><strong>GPX</strong> speichert Tracks, Routen und Höhe — ideal für Wander-Apps und GPS-Geräte. <strong>KML</strong> ist Googles Format, gut für Earth-Visualisierungen, weniger universell für Navigation.</p>

          <h2>Wann welches Format</h2>

          <ul>
            <li>Trail- oder Radroute teilen → GPX</li>
            <li>Google-Earth-Overlays → KML</li>
            <li>Garmin / Handy-Navigation → GPX</li>
          </ul>

          <p>GPX in <a href="../">GPX Viewer</a> öffnen. Auch: <a href="gpx-vs-tcx.html">GPX vs TCX</a>.</p>""",
    },
    "gpx-vs-tcx": {
        "title": "GPX vs TCX: Was nutzen?",
        "h1": "GPX vs TCX",
        "subtitle": "Routen teilen vs. Garmin-Trainingsdaten.",
        "description": "GPX vs TCX: GPX zum Routen teilen. TCX mit Herzfrequenz und Trittfrequenz für Garmin-Training.",
        "keywords": "gpx vs tcx",
        "tag": "Formate",
        "card_title": "GPX vs TCX",
        "card_desc": "Routen teilen vs. Garmin-Trainingsexporte.",
        "date_display": "19. Juli 2026",
        "cta_text": "Geteilte GPX-Routen in GPX Viewer auf jedem Handy öffnen.",
        "body": """          <p><strong>GPX</strong> ist der Standard zum Teilen von Wander- und Radrouten. <strong>TCX</strong> ist Garmin-Format mit extra Trainingsfeldern wie Herzfrequenz und Trittfrequenz.</p>

          <h2>Wann welches Format</h2>

          <ul>
            <li>Route mit Freunden teilen → GPX</li>
            <li>Workout zu Garmin hochladen → TCX</li>
            <li>Route auf iPhone/Android ansehen → GPX</li>
          </ul>

          <p>GPX in <a href="../">GPX Viewer</a> importieren. Vergleich: <a href="gpx-vs-fit.html">GPX vs FIT</a>.</p>""",
    },
    "gpx-vs-fit": {
        "title": "GPX vs FIT: Der Unterschied",
        "h1": "GPX vs FIT",
        "subtitle": "Offene Routendateien vs. Garbins Binärformat.",
        "description": "GPX vs FIT erklärt. GPX zum Routen teilen. FIT ist Garbins Binärformat für aufgezeichnete Aktivitäten.",
        "keywords": "gpx vs fit",
        "tag": "Formate",
        "card_title": "GPX vs FIT",
        "card_desc": "Routendateien vs. Garmin-Aktivitätsaufzeichnungen.",
        "date_display": "20. Juli 2026",
        "cta_text": "GPX-Routen mit GPX Viewer auf dem Handy ansehen und teilen.",
        "body": """          <p><strong>GPX</strong> ist textbasiert und weit teilbar — perfekt für Routen. <strong>FIT</strong> ist Garbins Binärformat für Aktivitäten mit Sensordaten, schwerer außerhalb Garmin zu öffnen.</p>

          <h2>Faustregel</h2>

          <ul>
            <li>Geplante Route teilen → GPX exportieren</li>
            <li>Aufzeichnung mit Leistung/HR archivieren → FIT</li>
            <li>Vor Gruppenausfahrt prüfen → GPX in GPX Viewer</li>
          </ul>

          <p>GPX in <a href="../">GPX Viewer</a> öffnen. <a href="import-gpx-garmin-devices.html">GPX zu Garmin importieren</a>.</p>""",
    },
    "how-to-view-gpx-elevation-data": {
        "title": "Höhendaten aus GPX anzeigen",
        "h1": "GPX-Höhendaten anzeigen",
        "subtitle": "Anstieg, Abstieg und Höhenprofil aus jedem Track.",
        "description": "Höhendaten aus GPX-Dateien anzeigen. Gesamtanstieg, Abstieg und Höhenprofil in GPX Viewer.",
        "keywords": "gpx höhe, gpx höhenprofil",
        "tag": "Karten",
        "card_title": "GPX-Höhendaten anzeigen",
        "card_desc": "Anstieg, Abstieg und Höhenprofile aus GPX.",
        "date_display": "21. Juli 2026",
        "cta_text": "Höhenprofile für jede GPX-Route in GPX Viewer sehen.",
        "body": """          <p>GPX-Dateien speichern die Höhe an jedem GPS-Punkt. Ein guter Viewer zeigt ein Höhenprofil, damit Sie Anstiege vorab sehen.</p>

          <h2>In GPX Viewer</h2>

          <ul>
            <li>.gpx-Datei importieren</li>
            <li>Höhendiagramm unter der Karte scrollen</li>
            <li>Gesamtanstieg, Abstieg und Min/Max-Höhe prüfen</li>
          </ul>

          <p>Planen Sie Wanderungen mit <a href="how-to-use-gpx-files-hiking.html">GPX fürs Wandern</a> und <a href="how-to-calculate-gpx-route-distance.html">Routendistanz</a>.</p>""",
    },
    "how-to-calculate-gpx-route-distance": {
        "title": "GPX-Routendistanz berechnen",
        "h1": "GPX-Routendistanz berechnen",
        "subtitle": "Echte Trail-Distanz aus GPS-Punkten — nicht Luftlinie.",
        "description": "Distanz einer GPX-Route aus GPS-Trackpunkten berechnen. GPX Viewer zeigt die genaue Trail-Distanz automatisch.",
        "keywords": "gpx distanz, gpx strecke berechnen",
        "tag": "Karten",
        "card_title": "GPX-Routendistanz berechnen",
        "card_desc": "Trail-Distanz aus GPS-Trackpunkten messen.",
        "date_display": "22. Juli 2026",
        "cta_text": "GPX importieren und die Distanz in GPX Viewer sehen.",
        "body": """          <p>Luftlinie auf der Karte unterschätzt Trails. GPX-Distanz summiert jeden GPS-Punkt entlang des echten Wegs.</p>

          <h2>Automatisch in GPX Viewer</h2>

          <p>Datei in <a href="../">GPX Viewer</a> öffnen — Gesamtdistanz erscheint sofort. Kombinieren Sie mit <a href="how-to-view-gpx-elevation-data.html">Höhendaten</a> zur Tagesplanung.</p>

          <p>Weiter: <a href="how-to-view-gpx-on-a-map.html">Auf Karte anzeigen</a> · <a href="what-is-a-gpx-file-reader.html">GPX-Reader</a></p>""",
    },
    "how-to-import-gpx-google-maps": {
        "title": "GPX in Google Maps importieren",
        "h1": "GPX in Google Maps importieren",
        "subtitle": "Google My Maps am Desktop — oder GPX Viewer auf dem Handy.",
        "description": "GPX über Google My Maps am Desktop importieren. Für mobile Navigation ist GPX Viewer schneller.",
        "keywords": "gpx google maps importieren",
        "tag": "Karten",
        "card_title": "GPX in Google Maps importieren",
        "card_desc": "My Maps am Desktop, GPX Viewer auf dem Handy.",
        "date_display": "23. Juli 2026",
        "cta_text": "GPX-Routen auf dem Handy mit GPX Viewer navigieren.",
        "body": """          <p>Google Maps auf dem Handy importiert GPX nicht direkt. Am Desktop: <strong>Google My Maps</strong> → Karte erstellen → Import → .gpx hochladen.</p>

          <h2>Besser auf dem Handy</h2>

          <p>Für Navigation unterwegs: Datei in <a href="../">GPX Viewer</a> auf iPhone oder Android öffnen. Siehe <a href="how-to-open-gpx-file-any-device.html">GPX auf jedem Gerät öffnen</a>.</p>""",
    },
    "open-gpx-files-apple-maps": {
        "title": "GPX auf iPhone öffnen",
        "h1": "GPX auf iPhone öffnen",
        "subtitle": "Apple Maps kann GPX nicht — GPX Viewer schon.",
        "description": "Apple Maps öffnet keine GPX-Dateien. GPX Viewer auf dem iPhone zum Anzeigen und Navigieren von GPX-Routen.",
        "keywords": "gpx apple maps, gpx iphone",
        "tag": "iPhone",
        "card_title": "GPX auf iPhone öffnen",
        "card_desc": "Apple Maps importiert kein GPX — GPX Viewer schon.",
        "date_display": "24. Juli 2026",
        "cta_text": "GPX Viewer laden und jede GPX-Route auf dem iPhone öffnen.",
        "body": """          <p><strong>Apple Maps kann GPX-Dateien nicht importieren.</strong> Für Trail- oder Radrouten auf dem iPhone brauchen Sie eine GPX-App.</p>

          <h2>Alternative</h2>

          <p>.gpx-Datei an <a href="../">GPX Viewer</a> aus Mail, Dateien oder Safari senden. Schritte: <a href="how-to-open-gpx-files-on-iphone.html">GPX auf iPhone öffnen</a>.</p>

          <p>Weiter: <a href="how-to-view-gpx-on-a-map.html">Auf Karte anzeigen</a> · <a href="view-gpx-without-internet.html">Offline anzeigen</a></p>""",
    },
    "download-gpx-from-strava": {
        "title": "GPX von Strava herunterladen",
        "h1": "GPX von Strava herunterladen",
        "subtitle": "Aktivitäten exportieren und in GPX Viewer öffnen.",
        "description": "GPX-Dateien aus Strava-Aktivitäten laden und in GPX Viewer mit Karte und Höhe ansehen.",
        "keywords": "gpx strava download, strava gpx export",
        "tag": "Radfahren",
        "card_title": "GPX von Strava herunterladen",
        "card_desc": "Strava-Aktivitäten als GPX exportieren.",
        "date_display": "25. Juli 2026",
        "cta_text": "Aus Strava exportieren, dann in GPX Viewer auf dem Handy öffnen.",
        "body": """          <p>Strava Web: Aktivität öffnen → <strong>⋮</strong> → <strong>GPX exportieren</strong>. Datei speichern und in <a href="../">GPX Viewer</a> auf dem Handy öffnen.</p>

          <h2>Tipps</h2>

          <ul>
            <li>Manche Aktivitäten sind vom Besitzer gesperrt</li>
            <li>GPX enthält die Route — Höhe vor der Fahrt prüfen</li>
            <li>Gleiche Datei teilen: <a href="share-gpx-iphone-android.html">plattformübergreifend</a></li>
          </ul>""",
    },
    "download-gpx-from-komoot": {
        "title": "GPX von Komoot herunterladen",
        "h1": "GPX von Komoot herunterladen",
        "subtitle": "Komoot-Touren exportieren und mit GPX Viewer navigieren.",
        "description": "GPX von Komoot-Touren laden und in GPX Viewer auf iPhone oder Android öffnen.",
        "keywords": "gpx komoot download, komoot gpx export",
        "tag": "Wandern",
        "card_title": "GPX von Komoot herunterladen",
        "card_desc": "Komoot-Wander- und Radtouren als GPX exportieren.",
        "date_display": "26. Juli 2026",
        "cta_text": "In Komoot planen, in GPX Viewer auf dem Handy navigieren.",
        "body": """          <p>In Komoot: Tour öffnen → <strong>Exportieren</strong> → <strong>GPX</strong> wählen. Datei in <a href="../">GPX Viewer</a> für Karte, Distanz und Höhe öffnen.</p>

          <h2>Warum beide Apps</h2>

          <p>Komoot plant gut; GPX Viewer ist für schnelle mobile Ansicht und Navigation gebaut. Offline mit Pro — <a href="view-gpx-without-internet.html">Offline-GPX</a>.</p>""",
    },
    "import-gpx-garmin-devices": {
        "title": "GPX auf Garmin-Geräte importieren",
        "h1": "GPX auf Garmin importieren",
        "subtitle": "Kurse über Garmin Connect hochladen — vorher in GPX Viewer prüfen.",
        "description": "GPX auf Garmin-Uhren und Edge über Garmin Connect importieren. Routen vor dem Sync in GPX Viewer prüfen.",
        "keywords": "gpx garmin importieren, garmin connect gpx",
        "tag": "Geräte",
        "card_title": "GPX auf Garmin importieren",
        "card_desc": "GPX in Garmin Connect hochladen und auf die Uhr syncen.",
        "date_display": "27. Juli 2026",
        "cta_text": "GPX-Routen in GPX Viewer prüfen, bevor Sie zu Garmin syncen.",
        "body": """          <p>.gpx-Kurs in <strong>Garmin Connect</strong> (Web oder App) hochladen, dann an Uhr oder Edge senden.</p>

          <h2>Erst prüfen</h2>

          <p>Dieselbe Datei in <a href="../">GPX Viewer</a> öffnen — Wegpunkte, Distanz und Höhe checken. Vergleich: <a href="gpx-vs-fit.html">GPX vs FIT</a>.</p>""",
    },
    "how-to-use-gpx-files-hiking": {
        "title": "GPX-Dateien fürs Wandern nutzen",
        "h1": "GPX fürs Wandern nutzen",
        "subtitle": "Trail-Tracks laden, Höhe prüfen, sicher navigieren.",
        "description": "GPX fürs Wandern nutzen. Trail-Tracks importieren, Höhe prüfen und Routen auf iPhone oder Android folgen.",
        "keywords": "gpx wandern, wandern gpx datei",
        "tag": "Wandern",
        "card_title": "GPX fürs Wandern nutzen",
        "card_desc": "Trail-GPX-Tracks laden und auf dem Handy navigieren.",
        "date_display": "28. Juli 2026",
        "cta_text": "Wander-GPX-Tracks mit GPX Viewer auf iPhone und Android folgen.",
        "body": """          <p>Ein geteilter GPX-Track macht aus einem Vereinsweg oder Guidebook-Pfad eine Live-Karte auf dem Handy. In <a href="../">GPX Viewer</a> importieren, Distanz und Höhe prüfen, der Linie auf dem Trail folgen.</p>

          <h2>Wander-Tipps</h2>

          <ul>
            <li>Offline-Karten vor abgelegenen Trails laden (GPX Viewer Pro)</li>
            <li>Immer Papierkarte oder Backup-Navigation mitführen</li>
            <li>Jemandem den Plan mitteilen</li>
          </ul>

          <p>Siehe <a href="best-gpx-viewer-for-hiking.html">bester GPX Viewer fürs Wandern</a> und <a href="view-gpx-without-internet.html">Offline-Anzeige</a>.</p>""",
    },
    "how-to-use-gpx-files-cycling": {
        "title": "GPX-Dateien fürs Radfahren nutzen",
        "h1": "GPX fürs Radfahren nutzen",
        "subtitle": "Ausfahrten planen, Anstiege prüfen, Routen teilen.",
        "description": "GPX fürs Radfahren. Routen planen, Höhe prüfen und auf iPhone oder Android mit GPX Viewer navigieren.",
        "keywords": "gpx radfahren, radroute gpx",
        "tag": "Radfahren",
        "card_title": "GPX fürs Radfahren nutzen",
        "card_desc": "Radrouten planen und GPX-Tracks auf Ausfahrten folgen.",
        "date_display": "29. Juli 2026",
        "cta_text": "Radsport-GPX-Routen in GPX Viewer prüfen und navigieren.",
        "body": """          <p>Ausfahrt aus Komoot oder Strava als GPX exportieren, in <a href="../">GPX Viewer</a> öffnen und Distanz sowie Anstiege vor dem Tag prüfen.</p>

          <h2>Auf dem Rad</h2>

          <ul>
            <li>Handy montieren, Track in GPX Viewer öffnen</li>
            <li>Pro Live-Standort für Position auf der Route</li>
            <li>Gleiche GPX mit der Gruppe teilen — <a href="share-gpx-iphone-android.html">iPhone und Android</a></li>
          </ul>

          <p><a href="how-to-create-gpx-cycling-routes.html">Radrouten erstellen</a> · <a href="download-gpx-from-strava.html">Strava-Export</a></p>""",
    },
    "view-gpx-without-internet": {
        "title": "GPX ohne Internet anzeigen",
        "h1": "GPX ohne Internet anzeigen",
        "subtitle": "Offline-Karten in GPX Viewer Pro für Funklöcher.",
        "description": "GPX ohne Internet mit GPX Viewer Pro Offline-Karten anzeigen. Kacheln vor Wanderungen und Ausfahrten laden.",
        "keywords": "offline gpx viewer, gpx offline",
        "tag": "Pro",
        "card_title": "GPX ohne Internet anzeigen",
        "card_desc": "Offline-GPX-Karten wenn der Empfang ausfällt.",
        "date_display": "30. Juli 2026",
        "cta_text": "GPX Viewer Pro holen und Offline-Karten vor der nächsten Tour laden.",
        "body": """          <p>In Bergen und Wäldern verschwindet der Empfang. <strong>GPX Viewer Pro</strong> lädt Kartenkacheln per WLAN und zeigt Ihren GPX-Track ohne Verbindung.</p>

          <h2>Vor der Abfahrt</h2>

          <ul>
            <li>GPX-Route importieren</li>
            <li>Kartenbereich entlang des Tracks laden</li>
            <li>Zuhause im Flugmodus testen</li>
          </ul>

          <p>Vergleich: <a href="best-ways-view-gpx-online-offline.html">Online vs. Offline</a>.</p>""",
    },
    "share-gpx-iphone-android": {
        "title": "GPX zwischen iPhone und Android teilen",
        "h1": "GPX zwischen iPhone und Android teilen",
        "subtitle": ".gpx-Dateien senden, damit alle dieselbe Route haben.",
        "description": "GPX zwischen iPhone und Android per Mail, AirDrop, Drive oder WhatsApp teilen.",
        "keywords": "gpx teilen iphone android",
        "tag": "Tipps",
        "card_title": "GPX zwischen iPhone und Android teilen",
        "card_desc": ".gpx-Routen plattformübergreifend an die Gruppe senden.",
        "date_display": "31. Juli 2026",
        "cta_text": "GPX-Routen aus GPX Viewer teilen — Freunde öffnen sie auf jedem Handy.",
        "body": """          <p>GPX funktioniert auf iPhone und Android — keine Konvertierung nötig. .gpx-Datei per Mail, WhatsApp, AirDrop oder Google Drive senden.</p>

          <h2>So teilen</h2>

          <ul>
            <li><strong>iPhone</strong> — in GPX Viewer öffnen → Teilen → Mail oder AirDrop</li>
            <li><strong>Android</strong> — Teilen → Gmail, Drive oder WhatsApp</li>
            <li>Empfänger öffnen mit GPX Viewer — <a href="how-to-open-gpx-files-on-android.html">Android</a> und <a href="how-to-open-gpx-files-on-iphone.html">iPhone</a></li>
          </ul>

          <p>Endung <code>.gpx</code> behalten. Siehe <a href="what-is-a-gpx-file.html">Was ist GPX</a>.</p>""",
    },
}


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["blog_index"]["de"] = BLOG_INDEX_DE

    for leg in data["legacy_articles"]:
        slug = leg["slug"]
        if slug in LEGACY_DE:
            tag, title, desc = LEGACY_DE[slug]
            leg.setdefault("translations", {})["de"] = {
                "tag": tag,
                "card_title": title,
                "card_desc": desc,
                "read_more": DE_UI["read_more"],
            }

    for art in data["articles"]:
        slug = art["slug"]
        if slug not in ARTICLES_DE:
            continue
        de = {**DE_UI, **ARTICLES_DE[slug]}
        art.setdefault("translations", {})["de"] = de

    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added DE translations for {len(ARTICLES_DE)} articles")


if __name__ == "__main__":
    main()
