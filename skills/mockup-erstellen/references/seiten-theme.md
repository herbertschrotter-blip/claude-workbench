# Seiten mit Theme und Seitenliste

Gilt für mockup-erstellen, wenn das Skill-Profil `Mockup.Theme` **und** `Mockup.Seitenliste` nennt. Steht eines davon auf
`none` oder fehlt es, bleibt es bei Mockups je Thema (`../SKILL.md`). Dateien und Befehle kommen immer aus dem Profil.

## Inhalt

- Eine Datei je Seite
- Theme
- Interaktiv
- Vorschau
- Abnahme und Version
- Ältere Mockups

## Eine Datei je Seite

- Je Seite oder Formular eine Datei in der Ablage (`Mockup.Ablage`). Sie enthält nur Inhalt und Zustände; Bausteine
  kommen aus dem Theme.
- Vor dem Mockup die Seitenliste lesen (Quelldatei aus `Mockup.Seitenliste`). Gibt es die Seite schon, wird nur ihre
  Datei geändert, kein neues Mockup angelegt, und die Auswahlfrage Archivieren/Überschreiben entfällt.
- Eine neue Seite kommt vor der Vorschau in die Quelldatei, danach läuft der Befehl aus `Mockup.Seitenliste`; so steht sie
  in der Liste und hat eine Version.
- Jede Seite zeigt ihre Version und hat die Pflichtansichten aus `Mockup.Ansichten` umschaltbar.

## Theme

- Ein Baustein, den mehrere Seiten nutzen, wird im Theme geändert, nie in einer Seite kopiert.
- Erzeugte Theme-Dateien nie von Hand ändern. Stile werden in der App geändert (code-erstellen), danach läuft der Befehl
  aus `Mockup.Theme`.
- Seiten brauchen die Theme-Dateien und sind deshalb nicht allein öffenbar (`../SKILL.md#Standalone-fähig`).
- Der Token-Abgleich entfällt für erzeugte Theme-Dateien. Er gilt für alles, was in der Seite oder im von Hand
  gepflegten Theme-Teil steht.

## Interaktiv

Seiten, Zustände und Hauptknöpfe sind klickbar, Knöpfe führen zur nächsten Seite. Keine echte Logik.

## Vorschau

Nicht als einzelne Datei senden: Eine Seite ohne Theme zeigt nichts Richtiges. Die Seitenliste samt Seiten und Theme mit
dem Werkzeug der Umgebung veröffentlichen (die Seitenliste als Seite, Seiten und Theme als ihre Dateien, die relativen
Pfade bleiben gleich) und den Link nennen. Cowork:
[cowork.md](cowork.md#vorschau).

## Abnahme und Version

Nach einer Abnahme, zusätzlich zu `../SKILL.md#Abnahme festhalten`:

1. Verlaufseintrag in der Quelldatei: Version, Datum, was, Ticket, Mockup.
2. Version der Seite setzen: kleine Änderung +0.1, Neugestaltung +1.0.
3. Befehl aus `Mockup.Seitenliste` ausführen.
4. Abnahme am Abnahme-Ort festhalten, nur für die geänderte Seite.

Quelldatei, erzeugte Dateien und Abnahme kommen in denselben Commit. Damit steht die Version fest; code-erstellen zählt
sie für dieselbe Änderung nicht noch einmal.

## Ältere Mockups

Ältere Mockups bleiben liegen. Eine Seite wandert erst um, wenn sie überarbeitet wird; das alte Mockup wird dann am
Abnahme-Ort als abgelöst vermerkt.
