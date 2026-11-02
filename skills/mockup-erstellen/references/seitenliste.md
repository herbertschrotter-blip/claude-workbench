# Seitenliste

Standard für alle Projekte mit Oberfläche: eine maschinenlesbare Quelldatei mit einer Zeile je Seite oder Formular,
daraus erzeugt eine Doku und eine veröffentlichte Seite. Dateien und Befehle kommen immer aus dem Skill-Profil
(`Mockup.Seitenliste`, `Mockup.Theme`, `Mockup.Beziehungen`, `Mockup.Pruefung`, `Mockup.Datenliste`), Suchmuster aus der Config der Werkzeuge.

## Inhalt

- Wann sie gilt
- Prüfen und nachträglich anlegen
- Quelldatei
- Versionen
- Veröffentlichte Seitenliste
- Mockups und Theme
- Vorschau
- Abnahme
- Datenliste
- Abgleich
- Werkzeuge

## Wann sie gilt

Ein Projekt hat eine Oberfläche, wenn `Mockup.Ablage` nicht `none` ist. Ohne Oberfläche stehen die Felder auf `none`. Steht `Mockup.Seitenliste` bei einem Projekt mit Oberfläche auf `none`, ist
es bewusst ausgenommen: Es gilt die bisherige Arbeitsweise, und es kommt keine Frage.

## Prüfen und nachträglich anlegen

Gilt für mockup-erstellen, code-erstellen, ticket, doc-pflege und projekt-anlegen, sobald sie in einem Projekt mit
Oberfläche arbeiten. audit meldet Fehlendes nur.

1. Stehen die Felder im Profil und gibt es die Dateien, im Format dieser Reference?
2. Fehlt etwas: sagen, was fehlt, und per Auswahlfrage „Jetzt anlegen (Empfehlung)“ / „Nach dieser Aufgabe anlegen“ /
   „Dieses Projekt ausnehmen“ (alle Felder werden im Profil `none`). Eine laufende kleine Aufgabe wird davon nicht
   blockiert. „Nach dieser Aufgabe anlegen“ gilt für die Sitzung: Es kommt am Ende der Aufgabe wieder, nicht in jedem Skill.
3. Anlegen, unter mockup-erstellen (Skill laden, die Dateien liegen in der Ablage):
   - zuerst die Felder ins Profil: Erzeuger, Vorlagen und Check gehören in `Mockup.Seitenliste`, sonst blockt der Skill-Wächter
   - Seiten aus dem Code ermitteln, Nummern vergeben, alle auf Version 0.1, außer der User nennt Überarbeitetes
   - vorhandene Mockups als `mockup_alt` zuordnen
   - Werkzeuge aus `../assets/seitenliste/` übernehmen und an den Stack anpassen (Abschnitt „Werkzeuge“)
   - hat das Projekt einen Datenspeicher: Datenliste anlegen (Abschnitt „Datenliste“), Tabellen und Speicherorte einordnen;
     ohne Datenspeicher `Mockup.Datenliste: none`
   - Check in `Code.Tests` und `Commit.Pre-Commit-Checks`, `Commit.Doku-Check` um „Seite geändert →
     Quelldatei; Schema oder Speicherort geändert → Datenliste“ ergänzen
   - Seitenliste veröffentlichen (Abschnitt „Vorschau“)

Nichts ohne Bestätigung am Code der App ändern.

## Quelldatei

Eine Liste von Bereichen (`nr`, `bereich`, `seiten`). Je Seite:

| Feld | Inhalt |
|---|---|
| `nr` | fester Ort, z. B. `2.3` (Bereich.Seite), nicht die Version. Bleibt für immer; neue Seiten bekommen die nächste freie Nummer im Bereich. Sagt der User „ändere 2.3“, ist diese Seite gemeint |
| `name`, `art` | Name; Seite, Blatt, Formular oder Vollbild |
| `code` | Dateien, mit Komma getrennt, relativ zu `code_wurzel` der Config |
| `schluessel` | Bezug auf das Code-Element, z. B. `blatt:rechnung`; Variante mit `#` |
| `version_mockup`, `version_code` | getrennt geführt; Mockup weiter als Code = abgenommen, aber noch nicht gebaut |
| `mockup`, `mockup_alt` | Mockup je Seite bzw. älteres Mockup je Thema, relativ zur Ablage |
| `verlauf` | je Version `v`, `datum`, `was`, `ticket` |
| `zu` | Verbindungen zu anderen Seiten; „Kommt von“ wird daraus berechnet |
| `nutzt` | gemeinsame Bausteine |
| `code_stand` | Fingerabdruck der Code-Dateien, gesetzt mit `--abnahme <nr>` des Listen-Befehls, wenn der Code gebaut ist |

## Versionen

1.0 = überarbeitet und abgenommen, 0.1 = noch nicht durchgegangen. Kleine Änderung +0.1, Neugestaltung +1.0.

## Veröffentlichte Seitenliste

Erzeugt aus `seitenliste_vorlage.html`:

- Liste mit Nummern, leichter Baumlinie, Chips M und C, Suche nach Nummer, Name oder Baustein, Filter Alle, Offen, Fertig,
  Nicht gebaut
- Reiter Seiten und Daten, wenn es eine Datenliste gibt
- Fokus-Ansicht: gewählte Seite in der Mitte, Kommt von und Geht zu mit Pfeilen, ab 7 Nachbarn „+ n weitere“, der Weg
  bleibt oben stehen; am Desktop neben der Liste, am Handy als eigene Ansicht
- Mockups öffnen in einem eigenen Fenster per fetch und `srcdoc` mit `base`, weil Seitenlinks im Rahmen der
  Veröffentlichung nicht zuverlässig gehen. Wechsel zwischen Mockups per `postMessage` über die Liste.

## Mockups und Theme

- Je Seite oder Formular eine Datei in der Ablage. Sie enthält nur Inhalt und Zustände; Bausteine kommen aus dem Theme.
- Vor dem Mockup die Seitenliste lesen. Gibt es die Seite schon, wird nur ihre Datei geändert, ohne neues Mockup und ohne
  die Auswahlfrage Archivieren/Überschreiben.
- Eine neue Seite kommt vor der Vorschau in die Quelldatei, ohne `code` und `version_code`, danach läuft der Befehl aus
  `Mockup.Seitenliste`. Der Abgleich nimmt sie aus, bis der Code steht.
- Vor einer Änderung an einem Baustein über `nutzt` nennen, welche Seiten sich mitändern.
- Ein Baustein, den mehrere Seiten nutzen, wird im Theme geändert, nie in eine Seite kopiert.
- Das Theme wird, wo möglich, aus den Stilen der App erzeugt und nie von Hand geändert: Stile in der App ändern
  (code-erstellen), dann den Befehl aus `Mockup.Theme` ausführen. Kann ein Stack das nicht, liegt es von Hand gepflegt in
  einer Datei.
- Seiten brauchen die Theme-Dateien und sind deshalb nicht allein öffenbar (`../SKILL.md#Standalone-fähig`).
- Der Token-Abgleich entfällt für erzeugte Theme-Dateien. Er gilt für alles, was in der Seite oder im von Hand gepflegten
  Theme-Teil steht.
- Interaktiv heißt: Seiten, Zustände und Hauptknöpfe sind klickbar, Knöpfe führen zur nächsten Seite. Keine echte Logik.
- Die Pflichtansichten aus `Mockup.Ansichten` sind umschaltbar, Nummer und Version stehen in der Vorführleiste.
- Ältere Mockups bleiben liegen. Eine Seite wandert erst um, wenn sie dran ist; das alte Mockup wird dann am Abnahme-Ort
  als abgelöst vermerkt.

## Vorschau

Nicht als einzelne Datei senden: Eine Seite ohne Theme zeigt nichts Richtiges. Die Seitenliste samt Seiten und Theme mit
dem Werkzeug der Umgebung veröffentlichen (die Seitenliste als Seite, Seiten und Theme als ihre Dateien, die relativen
Pfade bleiben gleich), den Link als `link` in die Config schreiben und nennen. Cowork: [cowork.md](cowork.md#vorschau).

## Abnahme

Zusätzlich zu `../SKILL.md#Abnahme festhalten`:

1. `version_mockup` von der höheren der beiden Versionen aus hochzählen (Abschnitt „Versionen“) und Verlauf ergänzen.
2. Befehl aus `Mockup.Seitenliste` ausführen.
3. Eintrag am Abnahme-Ort, nur für diese Seite.

Quelldatei, erzeugte Dateien und Abnahme kommen in denselben Commit. Damit steht die Version fest; code-erstellen zieht
danach `version_code`, `code_stand` und Verlauf nach.

## Datenliste

Reiter „Daten“ der Seitenliste, eigene Quelldatei und Doku (`Mockup.Datenliste`). Nummern `D1.1` für Tabellen, `S1.1` für
Speicherorte (Einstellungen, Dateien, Browser, Speicher). Je Eintrag Zweck, Felder, Verknüpfungen, genutzt von Seiten.

- Der Aufbau kommt aus einem frisch erzeugten, leeren Schema, nie aus echten Daten; die Liste zeigt nur Aufbau, keine
  Inhalte.
- Zweck, Bereiche, Speicherorte und zugehörige Seiten stehen in der Config unter `daten`. „Genutzt von“ gilt für den
  Bereich; ein Eintrag der Quelldatei kann mit eigenem `seiten` abweichen.
- Bei Projekten ohne Datenspeicher ist das Feld `none`, der Reiter fehlt dann.

## Abgleich

Check des Projekts (`Mockup.Pruefung`), Teil von `Code.Tests`, blockiert den Commit:

- jede Seite im Code steht in der Liste und umgekehrt
- Nummern sind eindeutig
- Verbindungen, Dateien und Mockups sind vorhanden
- Versionen in Liste, Verlauf und Mockup stimmen
- Theme und Liste sind neu erzeugt
- neue Tabelle oder Schema-Änderung ohne Eintrag ist rot; Datenliste und ihre Doku sind neu erzeugt, ihre Seiten gibt es

Ein geänderter Fingerabdruck ohne neue Version ist nur ein Hinweis. Bekannte Grenze: Varianten mit `#` zählen nur als
„Hauptseite gibt es“.

## Werkzeuge

Vorlagen unter `../assets/seitenliste/`; sie kommen nach `tools/` des Projekts bzw. in die Ablage. Bei claude.ai liegen sie
nicht vor; angelegt wird in Claude Code.

| Datei | Zweck | Anpassen |
|---|---|---|
| `seitenliste.config.json` | alle Projektwerte der Werkzeuge: Pfade, `titel`, `start`, `link`, `theme`, `seiten_im_code` (Muster, die Seiten im Code finden), `beziehungen` (Einstieg, Ziele, Handwege, Bausteine), `daten` (Datenliste; fehlt der Schlüssel, gibt es keinen Reiter) | ganz |
| `seitenliste.py` | erzeugt Doku und Seite, `--abnahme <nr>` setzt `code_stand` | nichts |
| `seitenliste_vorlage.html` | veröffentlichte Seite | nichts |
| `seitenbeziehungen.py` | schreibt `zu` und `nutzt` aus dem Code | nichts |
| `seitenliste_check.py` | Abgleich, braucht Python und die Laufzeit des Theme-Befehls | nichts |
| `datenliste.py` | erzeugt Quelldatei und Doku der Datenliste | nichts |
| `schema_leer.py` | gibt das leere Schema als JSON aus, Vorlage für SQLite | `leere_datenbank`; andere Speicher: eigenes Skript mit derselben Ausgabe |
| `theme.js`, `seite.html` | Vorführleiste und Muster einer Seite, für die Ablage | `ANSICHTEN` aus `Mockup.Ansichten`, Pfade |
| `mockup_theme.mjs` | Theme aus den Stilen, Vorlage für Lit | Pfade; andere Stacks: eigener Befehl oder Theme von Hand |

Profilwerte, Beispiel: [beispiele.md](beispiele.md#seitenliste-ha-hausbau).
