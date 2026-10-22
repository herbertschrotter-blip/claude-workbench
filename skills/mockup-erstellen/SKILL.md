---
name: mockup-erstellen
description: >
  Erstellt UI-Mockups als HTML-Entwürfe für neue Screens, Dialoge und
  Layoutvarianten – nach dem Mockup-Profil des Projekts (BPM: Docs/Mockups mit
  Sitemap; Heidi: dreame_x60/mockups im Bento-Design mit --dx-Tokens). Use when users want to mocken, entwerfen, skizzieren,
  zeigen, visualisieren, layouten, or want to clarify how a screen should
  look before coding — including mockups, screen designs, UI proposals,
  layout drafts, dialog sketches, tab/panel arrangements, and changes to an
  existing project mockup ("erst ins Mockup einbauen", "im Mockup ändern"),
  also in the middle of a ticket or code task. For
  sequential intents like "mock and then implement": triggers as the first
  step (mockup), then defers to code-erstellen. Do not trigger for direct
  XAML or Lit component implementation, small UI fixes in existing code, or
  non-UI design topics like database design.
---

# Mockup-Erstellen — UI-Entwürfe als HTML

## Zweck

Erstellt HTML-Mockups für die Screens des aktiven Projekts. Stellt sicher dass:
- Die Namenskonvention und Ablage des Projekts eingehalten wird (Mockup-Profil)
- Die richtigen Docs und Design-Tokens des Projekts geladen werden
- Der Workflow (Preview → Bestätigung → Speichern → Abnahme festhalten) befolgt wird
- Bestehende Mockups nicht überschrieben werden
- Der Stil konsistent über alle Screens bleibt (Token-Abgleich mit der Design-Quelle)

Was projektspezifisch ist, steht im **Mockup-Profil** (Abschnitt „Voraussetzung: Mockup-Profil“).
BPM: `Docs/Mockups/<Modul>/NN_Fenster/`, Sitemap, Klick-Navigation, Tokens aus Colors.xaml.
Heidi: `dreame_x60/mockups/*.html`, alle Seiten in einer Datei mit Tabs, Tokens `--dx-*` aus
`tokens.ts`, Referenz `bento.html`, Abnahme im Bauplan.

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
einem Ticket- oder Code-Ablauf („erst ins Mockup einbauen“).

**Wichtig:** Mockup-erstellen liefert HTML in die Mockup-Ablage des Profils. Sobald es um
echten Code (XAML/C#, TypeScript/Lit) geht, gehört die Arbeit in code-erstellen. Umgekehrt
ruft code-erstellen diesen Skill über den **Mockup-Hook** (Deep + UI + Profil „Mockup-Pflicht: ja“)
auf und wartet auf die festgehaltene Abnahme (Abschnitt „Workflow“, Schritt 4b).

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist –,
  dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Token-Abgleich zeigt Abweichungen | Mockup an Tokens anpassen, Tokens-Datei ändern (→ code-erstellen), Abweichung begründet lassen |
  | Pflichtansicht fehlt (Profil „Ansichten“) | Ansicht ergänzen, Ohne speichern (Begründung), Abbrechen |
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
  `git branch --show-current`, Pflicht-Branch aus dem Code-Profil beachten; ohne Shell und unbekannt: Auswahlfrage mit
  den Branch-Namen aus `git branch -a`. NIE automatisch einen Branch annehmen.

---

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Cowork: für Schreiboperationen Arbeitsverzeichnis nach **cc-steuerung**, Abschnitt „Arbeitsverzeichnis“, ermitteln.

---

## Voraussetzung: Mockup-Profil

Abschnitt `## Mockup-Profil` in der `CLAUDE.md` des Repos (Claude Code liest sie automatisch;
Cowork per DC). Felder:

| Feld | Bedeutung | BPM | Heidi |
|------|-----------|-----|-------|
| Ablage | Ordner für Mockups | `Docs/Mockups/<Modul>/NN_Fenster/` | `dreame_x60/mockups/` (flach) |
| Namensschema | Datei- und Ordnernamen | `NN_Fenster/NN_Variante.html` (`references/sitemap.md#Namenskonvention`) | `<thema>.html`, klein, ohne Umlaute; ein Mockup = alle betroffenen Seiten mit Tabs |
| Design-Quelle | Datei mit den gültigen Tokens | `Colors.xaml`, `UI_UX_Guidelines.md`, `WPF_UI_Architecture.md`, `Icons.xaml` | `dreame_x60/card/src/styles/tokens.ts` (`--dx-*`), Designvorgabe „Automotive Dark Bento“ |
| Referenz-Mockup | Stilvorlage für neue Mockups | letztes Mockup im selben Modul | `dreame_x60/mockups/bento.html` |
| Token-Form im HTML | wie Tokens im Mockup stehen | Hex-Werte aus Colors.xaml | CSS-Variablen `--dx-*` mit denselben Werten wie tokens.ts (`:root`-Block) |
| Ansichten | Pflichtansichten je Mockup | Desktop | Desktop **und** 390 px (Smartphone) nebeneinander, Tablet wenn Container-Regeln betroffen |
| Sitemap / Klick-Navigation | `references/sitemap.md` anwenden? | ja | nein (Tabs in der Datei, keine Kanten) |
| Vorschau | wie der User das Mockup sieht | Visualizer (Cowork) | Claude Code: Browser-Bereich (Datei öffnen) oder Datei per SendUserFile; Cowork: Visualizer |
| Abnahme-Ort | wo die Abnahme festgehalten wird | `_SITEMAP.md` (Status ✅) | Bauplan Abschnitt 7 (Seitentabelle: „Abgenommen von Herbert am <Datum> (Mockup <Datei>)“) und Notiz in Abschnitt 10; Abweichung zu v1 → PD-Eintrag 10a |
| Commit-Modul | Modulname für den Commit | `Docs` | `Doku` |

**Fehlt das Profil:** BPM-Werte aus diesem Skill und `references/sitemap.md` annehmen – nur wenn das Repo
tatsächlich `Docs/Mockups/` hat; sonst Auswahlfrage „Profil anlegen (Vorschlag aus dem Repo)“.

---

## Sitemap und Klick-Navigation (Profil „Sitemap: ja“)

Hat das Profil „Sitemap / Klick-Navigation: ja“ (BPM), gelten zusätzlich die Regeln in
[references/sitemap.md](references/sitemap.md): Namenskonvention mit Ordner je Fenster, Klick-Navigation zwischen den
Mockups, `_SITEMAP.md` mit Selbstcheck und die Abläufe für ein neues oder nachträglich eingefügtes Fenster. Vor jedem
Mockup in einem solchen Projekt lesen. Ohne „Sitemap: ja“ wird die Reference nicht geladen.

---

## Docs laden

Pflicht vor der Mockup-Erstellung.

Der Skill speichert KEINE Farbwerte, Spacing, Token-Namen.
Stattdessen werden die **Design-Quelle** und das **Referenz-Mockup** aus dem Profil gelesen
(Claude Code: Read; Cowork: DC `read_file` oder `github:get_file_contents`).

Heidi: `tokens.ts` komplett (alle `--dx-*`), `bento.html` Kopf (`:root`-Block, Layout-Regeln
Bento 12/6/1 Spalten, `dx-nav`-Formen), Bauplan Abschnitt 7 (Seitentabelle) und die
Aufgabenkarte des Schritts, für den das Mockup entsteht. Regel 14 des Bauplans: System-Schriftstapel,
keine externen Ressourcen – gilt auch im Mockup.

### Quickload-First-Pass (BPM)

Folgende Docs laden (Quickload reicht, kein Langform):

| Doc | Zweck | Laden via |
|-----|-------|-----------|
| **UI_UX_Guidelines.md** | Design-Token, Spacing, Komponenten | `github:get_file_contents` → `Docs/Referenz/UI_UX_Guidelines.md` |
| **WPF_UI_Architecture.md** | Token→WPF-Key Mapping, Dialog-Pattern | `github:get_file_contents` → `Docs/Referenz/WPF_UI_Architecture.md` |
| **Colors.xaml** | Aktuelle Farbwerte | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Colors.xaml` |
| **Icons.xaml** | Verfügbare Icon-Keys | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Icons.xaml` |

### Bestehende Mockups prüfen

Vor Erstellung eines neuen Mockups die Ablage des Profils listen:
```
Cowork:      list_directory → Docs/Mockups/<Modul>/
Claude Code: Glob → <Ablage>/*.html   (Heidi: dreame_x60/mockups/)
```
- Prüfe ob `NN_Fenster/`-Ordner schon existiert (dann ist es eine neue Variante, kein neues Fenster — siehe `references/sitemap.md#Neues Fenster anlegen`)
- Bei Update einer bestehenden Mockup-Datei: Per Auswahlfrage fragen (Archivieren, Überschreiben, Abbrechen).
  Heidi: abgelöste Mockups bleiben liegen und werden im Bauplan als „abgelöst durch <Datei>“ vermerkt (wie `seiten.html` → `bento.html`)

### Sitemap laden (zusätzlich, ab 2026-05 – nur bei Profil „Sitemap: ja“)

Vor jedem neuen Mockup:
```
read_file → Docs/Mockups/<Modul>/_SITEMAP.md
```
- Bestehende Navigationskanten kennen (welche Fenster gibt es schon? wer ruft was auf?)
- Bei totem Pfad (`alert('Mockup folgt: X')`): prüfen ob X jetzt existiert → Cleanup (siehe `references/sitemap.md#Sitemap und Selbstcheck`)

### Design-Referenz aus bestehenden Screens

Wenn ein neuer Screen im gleichen Modul/Stil wie ein bestehender sein soll:
- Bestehenden UI-Code laden (BPM: XAML via GitHub/DC; Heidi: Komponente `src/components/dx-*.ts` + `styles/controls.ts`) als Stil-Referenz
- ODER Screenshot vom User anfragen
- Ziel: Konsistenz über alle Screens

---

## Workflow

Verbindlich.

### Schritt 1 — Kontext sammeln
- Welches Modul? Welcher Screen?
- Gibt es schon ein Mockup das aktualisiert werden soll?
- Welche Daten/Felder soll der Screen zeigen?
- Gibt es einen bestehenden Screen als Stil-Referenz?

### Schritt 2 — Docs laden
- Design-Quelle und Referenz-Mockup des Profils (Abschnitt „Docs laden“); BPM zusätzlich Quickload-First-Pass, Colors.xaml
- `_SITEMAP.md` des betroffenen Moduls (nur BPM)
- Aufgabenquelle des Schritts (Heidi: Bauplan-Karte, Akzeptanz = was das Mockup zeigen muss)
- Memory prüfen auf Design-Entscheidungen (z.B. Karten-Design-Regeln; Heidi: Bauplan Abschnitt 10, PD-Register)

### Schritt 3 — Preview
- **Cowork:** Mockup als **Visualizer** (show_widget) im Chat anzeigen
- **Claude Code:** Datei in die Ablage schreiben (Schritt 4 ist hier dieselbe Datei) und im
  **Browser-Bereich** öffnen (`file://`-Pfad bzw. `preview_start`), Screenshot prüfen, zusätzlich
  per `SendUserFile` (render) an den User; Ansichten aus dem Profil im Browser nachstellen
  (`resize_window` 390 px)
- User bestätigt oder gibt Änderungswünsche
- Iterieren bis User zufrieden ist

### Schritt 3b — Token-Abgleich (Pflicht vor dem Speichern)
- Alle Token-Werte im Mockup (`:root`-Block bzw. Hex-Werte) gegen die **Design-Quelle** des Profils
  vergleichen (Heidi: `tokens.ts`; BPM: Colors.xaml)
- Abweichungen als Liste (Token, Mockup-Wert, Quell-Wert) → Auswahlfrage: Mockup anpassen /
  Tokens-Datei ändern (Aufgabe für code-erstellen) / begründet lassen (Begründung ins Mockup als Kommentar)
- Neue Tokens, die es in der Quelle nicht gibt, gelten als Abweichung
- Mockup darf keine Werte enthalten, die später „aus Versehen“ Karten-Standard werden

### Schritt 3c — Ansichten prüfen (Profil „Ansichten“)
- Jede Pflichtansicht ist im Mockup vorhanden (Heidi: Desktop + 390 px; Tablet bei Container-Regeln)
- Fehlt eine → Auswahlfrage: ergänzen / ohne speichern (Begründung) / abbrechen

### Schritt 4 — Auf Platte speichern
- Erst nach User-Bestätigung
- **Claude Code:** Write in die Ablage des Profils (Repo-Wurzel + Ablage); kein zusätzlicher Trigger nötig
- **Cowork:** via DC `write_file` in `<workFolder>/<Ablage>/…`; User muss DC explizit triggern ("dc", "cc", "auf platte", "speichern")
- Dateiname nach Namensschema des Profils (BPM: `references/sitemap.md#Namenskonvention`)
- Nur bei Profil „Sitemap: ja“: Sitemap aktualisieren (`references/sitemap.md#Sitemap und Selbstcheck`), Aufrufer-HTMLs patchen (`references/sitemap.md#Interaktivität und Klick-Navigation`, `references/sitemap.md#Neues Fenster anlegen`), tote Pfade scannen (`references/sitemap.md#Neues Fenster anlegen`)

### Schritt 4b — Abnahme festhalten (Pflicht, sobald der User abnimmt)
- Auswahlfrage „Abgenommen / Änderungen nötig / Später“ – erst nach der Vorschau der finalen Datei
- Bei „Abgenommen“ an den **Abnahme-Ort des Profils** schreiben: Datum, Datei, Umfang (welche Seiten/Zustände),
  bewusst weggelassene Extras. Heidi: Bauplan Abschnitt 7 (Zeile der Seite: „Abgenommen von Herbert am <Datum>
  (Mockup <Datei>)“) + Notiz in Abschnitt 10 (Art `Befund · Info`); Abweichung zum bisherigen Verhalten →
  PD-Eintrag 10a mit Status `freigegeben`. BPM: Sitemap-Status ✅.
- Ohne festgehaltene Abnahme gilt das Mockup für code-erstellen (Mockup-Hook) als **nicht** abgenommen.
- Bei „Später“: Hinweis, dass der Bau des Schritts blockiert bleibt.

### Schritt 5 — Commit-Vorschlag
- Format: `[vX.Y.Z] <Commit-Modul des Profils>, Docs: Mockup <Datei> – <Kurztitel>` (BPM: `Docs`, Heidi: `Doku`)
- Version: Bump-Regel des Commit-Profils (BPM: PATCH; Heidi: reine Doku-Commits behalten die Kartenversion)
- Abnahme-Eintrag (Schritt 4b) im selben Commit
- Falls Sitemap mitgeändert oder Aufrufer-Mockups gepatcht: in Commit-Message erwähnen

---

## HTML-Regeln für Mockups

### Standalone-fähig
- Mockup-HTML muss im Browser allein öffenbar sein
- Eigenes `<style>` Block mit den Tokens der Design-Quelle des Profils (geladen, nicht im Skill gespeichert)
- Kein Framework, keine externen Dependencies (keine Web-Fonts, keine CDN-Skripte – Heidi Regel 14)

### Tokens in der Form des Profils, keine Visualizer-Variablen
- Der Visualizer (Cowork) nutzt eigene CSS-Variablen (--color-background-primary etc.) – die dürfen nie ins gespeicherte Mockup
- BPM: Tokens als Hex-Werte aus Colors.xaml
- Heidi: Tokens als CSS-Variablen `--dx-*` in einem `:root`-Block mit **denselben Werten wie tokens.ts** (Token-Abgleich, Schritt 3b); Komponenten-Klassen wie in `bento.html`
- Werte aus der Design-Quelle laden, nicht hardcoden im Skill

### Struktur
```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title><Projekt> <Modul/Seite> — <Blatt></title>
<style>
/* Tokens aus der Design-Quelle des Profils (BPM: Colors.xaml als Hex; Heidi: :root { --dx-* } wie tokens.ts) */
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
- **Klick-Navigation zwischen Mockups: PFLICHT bei Profil „Sitemap: ja“** — siehe `references/sitemap.md#Interaktivität und Klick-Navigation`; Heidi: Tabs innerhalb der Datei, Zustände (Leerlauf/Lauf/Fehler) als umschaltbare Varianten
- Keine komplexe Logik — es ist ein Mockup, kein Prototyp

---


## VERBOTEN

- Farbwerte, Spacing-Werte, Token-Namen im Skill hardcoden
- Mockup erstellen ohne Docs zu laden
- Mockup auf Platte schreiben ohne User-Bestätigung im Chat
- Mockup auf Platte schreiben ohne expliziten DC-Trigger vom User (Cowork)
- NN-Nummer doppelt vergeben (BPM)
- Umlaute oder Leerzeichen in Dateinamen oder Ordnernamen
- Mockup im Visualizer anzeigen und direkt das Visualizer-HTML speichern
  (Visualizer nutzt andere CSS-Variablen als das Projekt)
- Branch automatisch annehmen (Branch-Policy des Skill-Profils, Shell fragen oder Auswahlfrage)
- **Speichern ohne Token-Abgleich** gegen die Design-Quelle (Schritt 3b) oder mit Tokens, die es dort nicht gibt
- **Speichern ohne die Pflichtansichten des Profils** (Heidi: Desktop + 390 px) ohne Auswahlfrage
- **Abnahme nur im Chat** – ohne Eintrag am Abnahme-Ort gilt das Mockup als nicht abgenommen (Schritt 4b)
- **BPM-Ablage oder -Namensschema für ein anderes Projekt annehmen** – alles aus dem Mockup-Profil
- **Externe Ressourcen im Mockup** (Web-Fonts, CDN), wenn das Projekt sie verbietet
- Prosa-Fragen bei festen Entscheidungsoptionen (z.B. Archiv-vs-Überschreiben-Entscheidung)
- **Mockup ohne Klick-Navigation auf interaktive Elemente speichern** (Profil „Sitemap: ja“) — alle Buttons/Tabs/Karten brauchen `onclick` (`references/sitemap.md#Interaktivität und Klick-Navigation`)
- **Sitemap-Update vergessen nach Mockup-Erstellung** (Profil „Sitemap: ja“) — `_SITEMAP.md` ist Single Source of Truth (`references/sitemap.md#Sitemap und Selbstcheck`)
- **Tote Pfade nicht prüfen vor Mockup-Erstellung** — `alert('Mockup folgt: X')` muss ersetzt werden wenn X jetzt existiert
- **Aufrufer-HTMLs nicht patchen** beim Anlegen eines neuen Fensters — `references/sitemap.md#Neues Fenster anlegen`, Schritt 2 ist Pflicht
- **Pfade in onclick ohne Selbstcheck speichern** — Datei-Existenz und Sitemap-Konsistenz prüfen (`references/sitemap.md#Sitemap und Selbstcheck`)
