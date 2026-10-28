---
name: mockup-erstellen
description: >
  Erstellt UI-Mockups als HTML-Entwürfe für neue Screens, Dialoge und
  Layoutvarianten – nach dem Mockup-Profil des Projekts (Ablage, Designquelle,
  Ansichten). Use when users want to mocken, entwerfen, skizzieren,
  zeigen, visualisieren, layouten, or want to clarify how a screen should
  look before coding — including mockups, screen designs, UI proposals,
  layout drafts, dialog sketches, tab/panel arrangements, and changes to an
  existing project mockup ("erst ins Mockup einbauen", "im Mockup ändern"),
  also in the middle of a ticket or code task, including the mockup's generator
  sources in the mockup folder and recording its approval (Abnahme). For
  sequential intents like "mock and then implement": triggers as the first
  step (mockup), then defers to code-erstellen. Do not trigger for direct
  XAML or Lit component implementation, small UI fixes in existing code, or
  non-UI design topics like database design.
---

# Mockup-Erstellen — UI-Entwürfe als HTML

## Zweck

Erstellt HTML-Mockups für die Screens des aktiven Projekts. Stellt sicher dass:
- Die Namenskonvention und Ablage des Projekts eingehalten wird (Skill-Profil, Bereich Mockup)
- Die richtigen Docs und Design-Tokens des Projekts geladen werden
- Der Workflow (Vorschau → Bestätigung → Speichern → Abnahme festhalten) befolgt wird
- Bestehende Mockups nicht überschrieben werden
- Der Stil konsistent über alle Screens bleibt (Token-Abgleich mit der Designquelle)

Was projektspezifisch ist, steht im Skill-Profil des Projekts (Abschnitt „Voraussetzung: Skill-Profil“). Wie zwei
Projekte die Werte füllen (Ordner je Fenster mit Sitemap; eine Datei mit Tabs und CSS-Variablen aus einer Token-Datei):
[references/beispiele.md](references/beispiele.md). Was nur im Cowork-Chat gilt (Visualizer, Desktop Commander):
[references/cowork.md](references/cowork.md).

---

## Vorrang / Delegation an andere Skills

**mockup-erstellen ist für UI-Entwürfe als HTML-Mockup. Wenn die Hauptabsicht
echte Code-Implementierung ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| View/Komponente schreiben oder ändern (XAML, Lit-Komponente, Dialog) | **code-erstellen** |
| ViewModel, Commands, Bindings, Selektoren implementieren | **code-erstellen** |
| Kleiner UI-Fix in bestehendem Code (Farbe, Größe, Binding) | **code-erstellen** |
| Code-Struktur oder Logik der UI | **code-erstellen** |

Nur wenn die Hauptabsicht **ein neuer UI-Entwurf als HTML-Mockup** ist
(Screen-Vorschlag, Layout-Klärung vor dem Code, Dialog-Skizze),
bleibt mockup-erstellen zuständig. Das gilt auch für eine Änderung an einem bestehenden Projekt-Mockup, auch mitten in
einem Ticket- oder Code-Ablauf („erst ins Mockup einbauen“). Dazu gehören die Quellen, aus denen das Mockup erzeugt
wird (z. B. Generator-Skripte im Mockup-Ordner), und der Abnahme-Eintrag am Abnahme-Ort des Profils, auch wenn er in
einer README steht.

**Wichtig:** Mockup-erstellen liefert HTML in die Mockup-Ablage des Profils. Sobald es um
echten Code (XAML/C#, TypeScript/Lit) geht, gehört die Arbeit in code-erstellen. Umgekehrt
ruft code-erstellen diesen Skill über den **Mockup-Hook** (Deep + UI + `Code.Mockup-Policy` im Skill-Profil)
auf und wartet auf die festgehaltene Abnahme (Abschnitt „Abnahme festhalten“).

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist –,
  dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Token-Abgleich zeigt Abweichungen | Mockup an Tokens anpassen, Tokens-Datei ändern (→ code-erstellen), Abweichung begründet lassen |
  | Pflichtansicht fehlt (`Mockup.Ansichten`) | Ansicht ergänzen, Ohne speichern (Begründung), Abbrechen |
  | Abnahme | Abgenommen, Änderungen nötig, Später |
  | Bestehendes Mockup gefunden: Archiv vs. Überschreiben | Archivieren (_ARCHIV suffix), Überschreiben, Abbrechen |
  | NN-Nummer belegt | Nächste freie Nummer, Andere Nummer wählen, Abbrechen |
  | Mehrere Stil-Referenzen möglich | Referenz-Dateinamen als Optionen |
  | Fenster-Ordner existiert bereits (neue Variante) | Variante hinzufügen, Bestehende ersetzen, Abbrechen |
  | Eingehende Links unklar beim neuen Fenster | Liste vorhandener Fenster aus Sitemap als Optionen + "Keine eingehenden Links" |

  Prosa-Fragen NUR wenn:
  - Offene Frage ohne feste Optionen (z.B. "Welche Daten/Felder soll der Screen zeigen?")
  - User hat Präferenz signalisiert
  - Freitext-Input nötig
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle muss dieser sein, sonst Auswahlfrage (wechseln /
  abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: Branch aus Chat-Kontext verwenden; mit Shell (Claude Code: Bash/PowerShell, Cowork: DC)
  `git branch --show-current`, Pflicht-Branch aus dem älteren Code-Profil beachten; ohne Shell und unbekannt: Auswahlfrage mit
  den Branch-Namen aus `git branch -a`. NIE automatisch einen Branch annehmen.

---

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Cowork: für Schreiboperationen Arbeitsverzeichnis nach **cc-steuerung**, Abschnitt „Arbeitsverzeichnis“, ermitteln.

---

## Voraussetzung: Skill-Profil

1. `CLAUDE.md` des Repos, Abschnitt `## Skill-Profil` (Spezifikation `docs/skill-profile-v1.md` im Skill-Repo; Claude
   Code liest sie automatisch, Cowork per DC). Pflichtfelder für mockup-erstellen: die Grundfelder, `Mockup.Ablage`,
   `Mockup.Designquelle`, `Mockup.Ansichten`, `Mockup.Abnahme-Ort`; für den Commit `Commit.Format` und `Commit.Module`.
   Fehlt ein Pflichtfeld oder steht es auf `fehlt`: genau dieses Feld nennen und nach `docs/skill-profile-v1.md`,
   Abschnitt „Fehlende Werte“, fragen.
2. Fehlt der Abschnitt: das ältere `## Mockup-Profil` der `CLAUDE.md` mit den Feldern unten. Die Spalte „Skill-Profil“
   nennt, wo der Wert dort steht.
3. **Fehlt beides:** die BPM-Werte aus [references/beispiele.md](references/beispiele.md) und `references/sitemap.md`
   annehmen – nur wenn das Repo tatsächlich `Docs/Mockups/` hat; sonst Auswahlfrage „Profil anlegen (Vorschlag aus dem
   Repo)“.

| Feld | Skill-Profil | Bedeutung |
|------|--------------|-----------|
| Ablage | `Mockup.Ablage` | Ordner für Mockups |
| Namensschema | `Mockup.Ablage` (Konvention der Ablage) | Datei- und Ordnernamen |
| Design-Quelle | `Mockup.Designquelle` | Datei mit den gültigen Tokens |
| Referenz-Mockup | `Mockup.Designquelle` | Stilvorlage für neue Mockups |
| Token-Form im HTML | `Mockup.Designquelle` | wie Tokens im Mockup stehen (Hex-Werte oder CSS-Variablen mit den Werten der Quelle) |
| Ansichten | `Mockup.Ansichten` | Pflichtansichten je Mockup |
| Sitemap / Klick-Navigation | `Mockup.Ablage` (gibt es dort `_SITEMAP.md`, gilt „ja“) | `references/sitemap.md` anwenden? |
| Vorschau | – (Umgebung) | wie der User das Mockup sieht |
| Abnahme-Ort | `Mockup.Abnahme-Ort` | wo die Abnahme festgehalten wird |
| Commit-Modul | `Commit.Module` | Modulname für den Commit |

Werte von BPM und Heidi als Beispiel: [references/beispiele.md](references/beispiele.md#profilwerte-bpm-und-heidi).

---

## Sitemap und Klick-Navigation (Profil „Sitemap: ja“)

Hat das Profil „Sitemap / Klick-Navigation: ja“, gelten zusätzlich die Regeln in
[references/sitemap.md](references/sitemap.md): Namenskonvention mit Ordner je Fenster, Klick-Navigation zwischen den
Mockups, `_SITEMAP.md` mit Selbstcheck und die Abläufe für ein neues oder nachträglich eingefügtes Fenster. Vor jedem
Mockup in einem solchen Projekt lesen. Ohne „Sitemap: ja“ wird die Reference nicht geladen.

---

## Docs laden

Pflicht vor der Mockup-Erstellung.

Der Skill speichert KEINE Farbwerte, Spacing, Token-Namen.
Stattdessen werden die **Designquelle** und das **Referenz-Mockup** aus dem Profil gelesen (Datei lesen).

- Designquelle vollständig (alle Tokens), vom Referenz-Mockup den Kopf (Token-Block, Layout-Regeln, Navigationsformen)
- die Seitenübersicht der Doku, falls das Projekt eine führt, und die Aufgabe, für die das Mockup entsteht
- Regeln des Projekts für Mockups (z. B. System-Schriftstapel, keine externen Ressourcen) gelten auch im Mockup
- führt das Projekt eine Ladereihenfolge der Doku (Quickload, Router), die Docs der Designquelle danach laden

Wie BPM und Heidi das füllen: [references/beispiele.md](references/beispiele.md#docs-laden-bpm-und-heidi).

### Bestehende Mockups prüfen

Vor Erstellung eines neuen Mockups die Ablage des Profils listen (`<Ablage>/**/*.html`):
- Prüfe ob `NN_Fenster/`-Ordner schon existiert (dann ist es eine neue Variante, kein neues Fenster — siehe `references/sitemap.md#Neues Fenster anlegen`)
- Bei Update einer bestehenden Mockup-Datei: Per Auswahlfrage fragen (Archivieren, Überschreiben, Abbrechen).
  Abgelöste Mockups bleiben liegen, wenn das Projekt es so führt, und werden am Abnahme-Ort als „abgelöst durch
  <Datei>“ vermerkt

### Sitemap laden (zusätzlich, nur bei Profil „Sitemap: ja“)

Vor jedem neuen Mockup `<Ablage>/<Modul>/_SITEMAP.md` lesen:
- Bestehende Navigationskanten kennen (welche Fenster gibt es schon? wer ruft was auf?)
- Bei totem Pfad (`alert('Mockup folgt: X')`): prüfen ob X jetzt existiert → Cleanup (siehe `references/sitemap.md#Sitemap und Selbstcheck`)

### Design-Referenz aus bestehenden Screens

Wenn ein neuer Screen im gleichen Modul/Stil wie ein bestehender sein soll:
- Bestehenden UI-Code laden (die View oder Komponente des Screens und ihre Styles) als Stil-Referenz
- ODER Screenshot vom User anfragen
- Ziel: Konsistenz über alle Screens

---

## Workflow

Verbindlich, in dieser Reihenfolge.

### Kontext sammeln
- Welches Modul? Welcher Screen?
- Gibt es schon ein Mockup das aktualisiert werden soll?
- Welche Daten/Felder soll der Screen zeigen?
- Gibt es einen bestehenden Screen als Stil-Referenz?

### Docs laden (im Ablauf)
- Designquelle und Referenz-Mockup des Profils (Abschnitt „Docs laden“), dazu die Ladereihenfolge des Projekts
- `_SITEMAP.md` des betroffenen Moduls (nur bei Profil „Sitemap: ja“)
- Aufgabenquelle des Schritts (`Code.Aufgabenquelle`; die Akzeptanz sagt, was das Mockup zeigen muss)
- Memory und Entscheidungs-Ort (`Doku.Entscheidungs-Ort`) auf Design-Entscheidungen prüfen

### Vorschau
- **Claude Code:** Datei in die Ablage schreiben (Speichern ist hier dieselbe Datei) und im
  **Browser-Bereich** öffnen (`file://`-Pfad bzw. `preview_start`), Screenshot prüfen, zusätzlich
  per `SendUserFile` (render) an den User; Ansichten aus dem Profil im Browser nachstellen
  (`resize_window` auf die Breite der Ansicht)
- **Cowork:** [references/cowork.md](references/cowork.md#vorschau)
- User bestätigt oder gibt Änderungswünsche
- Iterieren bis User zufrieden ist

### Token-Abgleich (Pflicht vor dem Speichern)
- Alle Token-Werte im Mockup (Token-Block bzw. Hex-Werte) gegen die **Designquelle** des Profils vergleichen
- Abweichungen als Liste (Token, Mockup-Wert, Quell-Wert) → Auswahlfrage: Mockup anpassen /
  Tokens-Datei ändern (Aufgabe für code-erstellen) / begründet lassen (Begründung ins Mockup als Kommentar)
- Neue Tokens, die es in der Quelle nicht gibt, gelten als Abweichung
- Mockup darf keine Werte enthalten, die später „aus Versehen“ Standard der App werden

### Ansichten prüfen (`Mockup.Ansichten`)
- Jede Pflichtansicht ist im Mockup vorhanden (z. B. Desktop und Smartphone-Breite nebeneinander)
- Fehlt eine → Auswahlfrage: ergänzen / ohne speichern (Begründung) / abbrechen

### Auf Platte speichern
- Erst nach User-Bestätigung
- **Claude Code:** Write in die Ablage des Profils (Repo-Wurzel + Ablage); kein zusätzlicher Trigger nötig
- **Cowork:** [references/cowork.md](references/cowork.md#speichern)
- Dateiname nach Namensschema des Profils (bei Sitemap: `references/sitemap.md#Namenskonvention`)
- Nur bei Profil „Sitemap: ja“: Sitemap aktualisieren (`references/sitemap.md#Sitemap und Selbstcheck`), Aufrufer-HTMLs patchen (`references/sitemap.md#Interaktivität und Klick-Navigation`, `references/sitemap.md#Neues Fenster anlegen`), tote Pfade scannen (`references/sitemap.md#Neues Fenster anlegen`)

### Abnahme festhalten
Pflicht, sobald der User abnimmt.
- Auswahlfrage „Abgenommen / Änderungen nötig / Später“ – erst nach der Vorschau der finalen Datei
- Bei „Abgenommen“ an den **Abnahme-Ort des Profils** (`Mockup.Abnahme-Ort`) schreiben: Datum, Datei, Umfang (welche
  Seiten/Zustände), bewusst weggelassene Extras. Führt das Projekt ein Register für gewollte Abweichungen, kommt eine
  Abweichung zum bisherigen Verhalten dort hinein. Beispiele: [references/beispiele.md](references/beispiele.md#abnahme-ort)
- Ohne festgehaltene Abnahme gilt das Mockup für code-erstellen (Mockup-Hook) als **nicht** abgenommen.
- Bei „Später“: Hinweis, dass der Bau des Schritts blockiert bleibt.

### Commit-Vorschlag
- Format: `Commit.Format` mit dem Doku-Modul aus `Commit.Module`, Typ `Docs`: `[vX.Y.Z] <Modul>, Docs: Mockup <Datei> – <Kurztitel>`
- Version: `Commit.Versionsregel` (reine Doku-Commits behalten oft die aktuelle Nummer)
- Abnahme-Eintrag (Abschnitt „Abnahme festhalten“) im selben Commit
- Falls Sitemap mitgeändert oder Aufrufer-Mockups gepatcht: in Commit-Message erwähnen

---

## HTML-Regeln für Mockups

### Standalone-fähig
- Mockup-HTML muss im Browser allein öffenbar sein
- Eigenes `<style>` Block mit den Tokens der Designquelle des Profils (geladen, nicht im Skill gespeichert)
- Kein Framework, keine externen Dependencies (keine Web-Fonts, keine CDN-Skripte), wenn das Projekt sie verbietet

### Tokens in der Form des Profils
- Tokens in der Form der Designquelle: Hex-Werte aus der Quelle, oder CSS-Variablen in einem `:root`-Block mit
  **denselben Werten wie die Quelle** (Token-Abgleich); Komponenten-Klassen wie im Referenz-Mockup
- Werte aus der Designquelle laden, nicht hardcoden im Skill
- Variablen einer Vorschau-Umgebung dürfen nie ins gespeicherte Mockup ([references/cowork.md](references/cowork.md#visualizer-variablen))

### Struktur
```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title><Projekt> <Modul/Seite> — <Blatt></title>
<style>
/* Tokens aus der Designquelle des Profils (Hex-Werte oder :root { --… } wie die Quelle) */
</style>
</head>
<body>
<!-- Mockup Content -->
</body>
</html>
```

### Interaktivität
- Hover-Effekte über `onmouseover`/`onmouseout` erlaubt
- Tab-Wechsel via einfaches JS erlaubt
- **Klick-Navigation zwischen Mockups: PFLICHT bei Profil „Sitemap: ja“** — siehe `references/sitemap.md#Interaktivität und Klick-Navigation`; ohne Sitemap: Tabs innerhalb der Datei, Zustände (z. B. Leerlauf/Lauf/Fehler) als umschaltbare Varianten
- Keine komplexe Logik — es ist ein Mockup, kein Prototyp

---


## VERBOTEN

- Farbwerte, Spacing-Werte, Token-Namen im Skill hardcoden
- Mockup erstellen ohne Docs zu laden
- Mockup auf Platte schreiben ohne User-Bestätigung im Chat
- Mockup auf Platte schreiben ohne expliziten DC-Trigger vom User (Cowork, [references/cowork.md](references/cowork.md#speichern))
- NN-Nummer doppelt vergeben (Profil „Sitemap: ja“)
- Umlaute oder Leerzeichen in Dateinamen oder Ordnernamen
- Mockup im Visualizer anzeigen und direkt das Visualizer-HTML speichern
  (Visualizer nutzt andere CSS-Variablen als das Projekt)
- Branch automatisch annehmen (Branch-Policy des Skill-Profils, Shell fragen oder Auswahlfrage)
- **Speichern ohne Token-Abgleich** gegen die Designquelle (Abschnitt „Token-Abgleich“) oder mit Tokens, die es dort nicht gibt
- **Speichern ohne die Pflichtansichten des Profils** (`Mockup.Ansichten`) ohne Auswahlfrage
- **Abnahme nur im Chat** – ohne Eintrag am Abnahme-Ort gilt das Mockup als nicht abgenommen (Abschnitt „Abnahme festhalten“)
- **BPM-Ablage oder -Namensschema für ein anderes Projekt annehmen** – alles aus dem Skill-Profil
- **Externe Ressourcen im Mockup** (Web-Fonts, CDN), wenn das Projekt sie verbietet
- Prosa-Fragen bei festen Entscheidungsoptionen (z.B. Archiv-vs-Überschreiben-Entscheidung)
- **Mockup ohne Klick-Navigation auf interaktive Elemente speichern** (Profil „Sitemap: ja“) — alle Buttons/Tabs/Karten brauchen `onclick` (`references/sitemap.md#Interaktivität und Klick-Navigation`)
- **Sitemap-Update vergessen nach Mockup-Erstellung** (Profil „Sitemap: ja“) — `_SITEMAP.md` ist Single Source of Truth (`references/sitemap.md#Sitemap und Selbstcheck`)
- **Tote Pfade nicht prüfen vor Mockup-Erstellung** — `alert('Mockup folgt: X')` muss ersetzt werden wenn X jetzt existiert
- **Aufrufer-HTMLs nicht patchen** beim Anlegen eines neuen Fensters — `references/sitemap.md#Neues Fenster anlegen`, Abschnitt „Aufrufer-HTMLs patchen“ ist Pflicht
- **Pfade in onclick ohne Selbstcheck speichern** — Datei-Existenz und Sitemap-Konsistenz prüfen (`references/sitemap.md#Sitemap und Selbstcheck`)
