---
name: code-erstellen
description: >
  Plant und erzeugt Codeänderungen im aktiven Projekt nach dessen Skill-Profil
  (Pflicht-Docs, Aufgabenquelle, Stack-Referenzen, Tests, Auslieferung) –
  projektneutral für jedes Repo mit Profil (z. B. C#/WPF, TypeScript/Lit,
  HA-YAML, Python). Use when users want to schreiben, erstellen, bauen,
  implementieren, fixen, refaktorieren, ändern, ergänzen, korrigieren, or
  erweitern application code — views, dialogs, components, services, view
  models, repositories, handlers, validators, models, validation, persistence,
  data flows, schemas, migrations, automations, or any source file (.cs, .xaml,
  .ts, .js, .py, .yaml, .json). Triggers also on bug fixes, UI fixes in existing
  screens/components, implementing logic regardless of domain, and code work
  on a task by its ID ("mach BSM-002", "weiter mit BSM-014"). Do not
  trigger for UI mockups and their sources, git commit
  commands, explicit documentation authoring (ADR / Konzept-Doc / Frontmatter
  / Quickload), ClickUp task actions without code work, or read-only audits.
---

# Code-Erstellen — Orchestrator Skill

## Zweck

Stellt sicher dass vor jeder Code-Erstellung die relevanten Docs
gelesen und geprüft wurden, die Akzeptanz der Aufgabe bekannt ist, Tests
laufen und die Änderung ausgeliefert wird. Welche Docs, Tests und
Auslieferungsschritte das sind, steht im **Skill-Profil** des Projekts
(Abschnitt „Voraussetzung: Skill-Profil“), auch die Ladereihenfolge der Docs
(`Code.Pflichtkontext`).

| Fall | Reference |
|------|-----------|
| Stack `csharp-wpf` (C# / .NET / WPF) | [references/stacks/csharp-wpf.md](references/stacks/csharp-wpf.md) |
| Stack `home-assistant`, `home-assistant-yaml` (Pakete, Automationen, Skripte, Dashboards) | [references/stacks/home-assistant.md](references/stacks/home-assistant.md) |
| Stack `python` | [references/stacks/python.md](references/stacks/python.md) |
| Stack `typescript-lit` (Lit-Komponenten in Home Assistant) | [references/stacks/typescript-lit.md](references/stacks/typescript-lit.md) |
| Wie zwei Projekte (BPM, Heidi) die Werte füllen | [references/beispiele.md](references/beispiele.md) |
| Arbeit im Cowork-Chat (Desktop Commander, Auto-Anker, Ausgabeformat, Tests, Auslieferung) | [references/cowork.md](references/cowork.md) |

---

## Vorrang / Delegation an andere Skills

**code-erstellen ist der größte Catch-all und würde sonst auch bei verwandten
Themen anspringen. Deshalb gilt lokal: wenn die Hauptabsicht einer dieser
Punkte ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| UI-Entwurf, Layout-Klärung, Screen-Vorschlag, neues HTML-Mockup | **mockup-erstellen** |
| Großer UI-Umbau (Modus Deep) und `Code.Mockup-Policy` greift → zuerst Mockup, Abnahme abwarten, dann hier weiter | **mockup-erstellen** (Mockup-Hook) |
| Commit-Befehl, Commit-Message, Version-Bump | **git-commit-helper** |
| ADR, Konzept, Frontmatter, Quickload, Doku-Refactor | **doc-pflege** |
| Tracker-Aktion ohne Code-Arbeit (neu, done, update, split, …); eine Aufgabe per ID umsetzen („mach <PRÄFIX>-NNN“, „weiter mit <PRÄFIX>-NNN“) bleibt hier, tracker setzt nur den Status | **tracker** |
| Read-only Konsistenzprüfung zwischen Code und Docs | **audit** |

Nur wenn die Hauptabsicht **echte Code-Implementierung** ist
(Services, ViewModels, Dialoge, Persistenzlogik, Validierung, etc.),
bleibt code-erstellen zuständig.

**Wichtig:** Das ist kein globales Regelsystem, sondern lokaler Vorrang
für den größten Catch-all. Die Delegation wird hier explizit genannt, weil
code-erstellen sonst unbeabsichtigt die genannten Nachbarskills überschreibt.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen
  ist –, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Modus unklar | Lite, Standard, Deep |
  | Zielschicht mehrdeutig | die Schichten der Stack-Referenz |
  | Mehrere Referenz-Implementierungen | Dateinamen als Optionen |
  | Fachliche Invariante würde verletzt | "Trotzdem fortsetzen", "Abbrechen", "Andere Lösung" |
  | Aufgaben-Zuordnung nach Commit | Aufgaben-Kandidaten als Optionen + "Keine Aufgabe" + "Neue Aufgabe anlegen" |
  | Mehrere Blocking Conditions | Welche Datei zuerst laden (Kandidaten) |
  | Commit-Version unklar (Major/Minor/Patch) | MAJOR (Breaking), MINOR (Feature), PATCH (Fix); `Commit.Versionsregel` hat Vorrang (z.B. Vorabversion: jede Änderung zählt hoch) |
  | User muss Referenzdatei angeben | Kandidaten aus Projektstruktur |
  | Bestehende Daten/Configs betroffen | "Daten löschen, neu anlegen lassen", "Migration bauen", "Abbrechen" |
  | Tests rot nach dem Bau | "Fix jetzt", "Test anpassen (Begründung)", "Abbrechen" |
  | `Code.Mockup-Policy` greift (Deep + UI) | "Mockup zuerst", "Ohne Mockup weiter (User-Entscheid)" |

  Prosa-Fragen nur, wenn:
  - Offene Frage ohne feste Optionen (Beispiel: "Welcher Kurztitel für den Commit?")
  - User hat gerade eine klare Präferenz signalisiert
  - Es ist Erklärung/Kontext, keine echte Entscheidung
  - Freitext-Input nötig (z.B. neuer Klassenname, neue Commit-Message)
- **Branch** (PFLICHT vor dem ersten Schreibzugriff) nach der Branch-Policy im Skill-Profil der `CLAUDE.md`:
  `current` → der aktuelle Branch aus der Shell (`git branch --show-current`); `fixed:<branch>` → der aktuelle muss
  dieser sein, sonst Auswahlfrage (wechseln / abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil:
  1. Prüfe ob Branch bereits in dieser Session bekannt ist → verwenden
  2. **Shell verfügbar:** `git branch --show-current`
     liefert den Branch – das ist eine Tatsache, keine Frage. Nennt das ältere Code-Profil einen
     Pflicht-Branch und der aktuelle weicht ab → Auswahlfrage
     (wechseln / trotzdem / abbrechen), nie stumm weiterarbeiten.
  3. **Keine Shell** (reiner Chat, GitHub API): Branches auflisten und **per Auswahlfrage**
     den aktiven wählen lassen (Optionen = alle Branch-Namen, z.B. aus `git branch -a`)
  4. Gewählten Branch für die gesamte Session merken

  NIE automatisch einen Branch annehmen (weder `main` noch einen anderen).

---

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

**Claude Code:** Arbeitsverzeichnis = Repo-Wurzel der Sitzung
(`git rev-parse --show-toplevel`); bei Worktrees gilt der Worktree, nie das
Haupt-Checkout.

**Cowork-Chat:** [references/cowork.md](references/cowork.md#profil-und-dateien-lesen).

**Keine hardcodierten absoluten Pfade** – in keiner Umgebung.

---

## Voraussetzung: Skill-Profil

Die Werte kommen aus dem Skill-Profil der `CLAUDE.md` im Repo (`docs/skill-profile-v1.md` im Skill-Repo):

| Feld | Wofür |
|------|-------|
| `Code.Stacks` | Schlüssel der Stack-Referenzen in `references/stacks/<key>.md` (Schichten, Kopplung, Impact-Zeilen, Tests, typische Fehler je Sprache); mehrere erlaubt |
| `Code.Pflichtkontext` | Docs und ihre Ladereihenfolge vor dem Code |
| `Code.Aufgabenquelle` | wo Ziel und Akzeptanz stehen (Pflicht, wenn das Projekt Aufgaben führt) |
| `Code.Architekturregeln` | Schichten und Kopplung des Projekts (wer darf wen kennen, wo wird verdrahtet), Regeln zu Migration und Daten |
| `Code.Tests` | Namen der Checks (Befehle unter `### Checks`, auch Build und Lint), Pflicht vor dem Commit |
| `Code.Auslieferung` | Schritte nach dem Commit |
| `Code.Mockup-Policy` | wann ein UI-Umbau zuerst als Mockup kommt (`required:<bedingung>`); `none` = nie Pflicht |
| `Code.Befund-Ort` | wo Befunde und Ideen ohne Aufgabe landen |
| `Doku.Router`, `Doku.Entscheidungs-Ort` | Routing zu den Docs; Grundentscheidungen des Projekts |
| `Commit.Format`, `Commit.Versionsquelle`, `Commit.Versionsregel`, `Commit.Doku-Check` | Commit-Zeile, Version, Doku-Hinweise |
| `Tracker.Provider`, `Tracker.Config` | Tracker-Abgleich und Präfix der Aufgaben |
| `Branch-Policy` | Branch (Grundsätze) |

Pflichtfelder: die Grundfelder, `Code.Stacks`, `Code.Pflichtkontext`, `Code.Architekturregeln`, `Code.Tests`,
`Code.Auslieferung`; `Code.Aufgabenquelle`, wenn das Projekt Aufgaben führt.

1. **Skill-Profil v1** (Abschnitt `## Skill-Profil`). `none` ist gültig: der Teil entfällt. Steht ein Pflichtfeld auf
   `fehlt` oder fehlt es: genau dieses Feld nennen und nach `docs/skill-profile-v1.md`, Abschnitt „Fehlende Werte“,
   fragen. Eine andere `Profil-Version` als 1: nicht weiterarbeiten.
2. **Rückfall:** der ältere Abschnitt `## Code-Profil` der CLAUDE.md. Seine Felder entsprechen den v1-Feldern: Stacks →
   `Code.Stacks`, Build/Lint und Tests → `Code.Tests`, Pflicht-Docs → `Code.Pflichtkontext`, Aufgabenquelle →
   `Code.Aufgabenquelle`, Schichten / Kopplung → `Code.Architekturregeln`, Auslieferung → `Code.Auslieferung`,
   Mockup-Pflicht → `Code.Mockup-Policy`, Notiz-Ort (Befunde und Ideen ohne Aufgabe) → `Code.Befund-Ort`.
3. **Fehlt beides:** der Router im Repo (meist `INDEX.md`), soweit vorhanden
   ([references/beispiele.md](references/beispiele.md#rückfall-ohne-profil-bpm)); was dann noch fehlt, per Auswahlfrage
   nach der Profil-Regel „Fehlende Werte“ (Profil ergänzen / einmalig nennen / abbrechen). Nie ohne Docs coden.

**Stack-Referenzen laden:** Für jeden Schlüssel in `Code.Stacks` die Datei `references/stacks/<key>.md`
lesen, **bevor** Modus, Impact Check oder Blocking beurteilt werden. Sie liefern die
sprachspezifische Lesart der neutralen Regeln unten. Fehlt eine Datei → Auswahlfrage
„Stack-Referenz aus dem Repo ableiten und anlegen“ / „Ohne Stack-Referenz weiter“; nie stumm
raten. Neue Sprache = neue Datei, der Skill selbst bleibt unverändert.
Vorhanden, auch ältere Bezeichnungen und welche Datei sie laden: siehe Tabelle im Abschnitt „Zweck“.

Werte von BPM und Heidi als Beispiel: [references/beispiele.md](references/beispiele.md#profilwerte-bpm-und-heidi).

---

## Ablauf (verbindlich)

### Anfrage klassifizieren → Modus

Kriterien sind stack-neutral; die konkreten Beispiele je Sprache stehen in
`references/stacks/<key>.md` (Abschnitt „Modus-Eskalation“).

```
mode = Lite

Eskalation auf Standard:
- neue öffentliche Funktion in einem bestehenden Baustein
- neuer Dialog / View / Komponente / Command
- Persistenz- oder Backend-Logik ohne neues Schema
- mehrere Dateien in einem Modul
- neue Validierungs-/Statuslogik

Eskalation auf Deep:
- neue Schnittstelle / Implementierung (Vertrag)
- Schema-Änderung
- externe Kommunikation / Import / Export
- mehrere Schichten / Projekte
- neuer Benutzerfluss / neue Seite
- Datenschutz
- Verdrahtung betroffen und nicht rein lokal
- Profil oder Stack-Referenz können eigene Kriterien ergänzen
```

**Bei Unsicherheit (Anfrage passt zu mehreren Modi):** Auswahlfrage (Grundsätze, „Modus unklar“).

**Mockup-Hook:** Modus Deep + UI betroffen + `Code.Mockup-Policy` greift → an
**mockup-erstellen** delegieren, Abnahme des Users abwarten, erst dann weiter mit
„Aufgabenquelle und Pflichtkontext laden“. Ausnahme nur per Auswahlfrage („Ohne Mockup weiter“).

### Aufgabenquelle und Pflichtkontext laden

1. **Aufgabenquelle** aus dem Profil lesen (`Code.Aufgabenquelle`, z.B. Aufgabe im Tracker oder Karte im Bauplan): Ziel,
   **Akzeptanzkriterien**, „Nicht ändern“, Voraussetzungen. Jede Akzeptanz-Zeile wird
   ein Testfall (Abschnitt „Tests“) und eine Zeile im Impact Check.
2. **Pflichtkontext** in der Reihenfolge des Profils laden (`Code.Pflichtkontext`; Beispiele:
   [references/beispiele.md](references/beispiele.md#ladereihenfolge-bpm)).
3. **Grundentscheidungen:** Nennt das Profil `Doku.Entscheidungs-Ort`, die dort dokumentierten
   Grundentscheidungen (Zweck, Grenzen, Datenhaltung, Auslieferung) vor der ersten fachlichen
   Erweiterung lesen. Sie sind Projektkontext, keine unveränderliche Architektur; eine Änderung
   daran wird dort nachgetragen.

### Kopf zuerst lesen

Gilt, wo die Docs einen Kopf haben (Frontmatter, Quickload); sonst die Docs des Pflichtkontexts ganz lesen.

**Ablauf:**
1. Relevante Docs aus dem Router (`Doku.Router`) bzw. dem Pflichtkontext identifizieren (Primary zuerst)
2. Für jede Doc: Nur den Kopf laden (etwa die ersten 30 Zeilen: Frontmatter + Quickload)
3. Fachliche Invarianten sofort in den Impact Check übernehmen
4. Pflichtlesen-Kapitel: IMMER laden wenn Modul betroffen → Blocking Condition
5. Aus dem Kopf (Kapitel-Feld) entscheiden welche Kapitel relevant sind
6. Nur relevante Kapitel als Langform nachladen
7. Kein Kopf vorhanden? → Fallback: ganze Doc laden

Höchstzahlen je Modus: Abschnitt „Modus-Übersicht“.

### Code Entry Points laden

Kopplungsregeln aus den Stack-Referenzen (Abschnitt „Schichten und Kopplungsregeln“ in
`references/stacks/<key>.md`) plus die Regeln des Projekts (`Code.Architekturregeln`). Bei mehreren Stacks (z.B. Karte +
Backend) die Schnittstelle dazwischen – der Vertrag – zuerst laden.

### Impact Check

Zeilen stack-neutral; die Lesart je Sprache (was „Verdrahtung“ oder „Persistenz“ konkret
heißt) steht in `references/stacks/<key>.md`, Abschnitt „Impact-Check-Zeilen“.

```
📋 Impact Check:
- UI / Styles / Design-Tokens: [Ja/Nein]
- Zustand / Bindings / Commands: [Ja/Nein]
- Domäne / Schnittstelle (Vertrag): [Ja/Nein]
- Persistenz / Backend: [Ja/Nein]
- Verdrahtung / Registrierung: [Ja/Nein]
- Externe Kommunikation: [Ja/Nein]
- Datenschutz: [Ja/Nein]
- Settings / Konfiguration: [Ja/Nein]
- Lebenszyklus / Render-Verhalten: [Ja/Nein]
- Logging / Fehlerbehandlung: [Ja/Nein]
- Bestehende Daten/Configs betroffen?: [Ja/Nein] (Frühphasen-Prinzip)
- Referenzimplementierung: [Name oder Nein]
- Fachliche Invarianten verletzt?: [Liste oder Nein] (Regeln des Projekts, „Nicht ändern“ der Aufgabe)
- Akzeptanzkriterien der Aufgabenquelle: [Liste → werden Testfälle]
- Tests betroffen (Code.Tests): [welche Dateien]
- Auslieferung nötig (Code.Auslieferung): [Ja/Nein, welcher Schritt]
```

### Blocking Conditions

Blockiere Code-Erstellung wenn:
- Zielschicht unklar → Auswahlfrage mit den Schichten der Stack-Referenz
- Referenzdatei nicht gefunden → Auswahlfrage mit Kandidaten oder "Ohne Referenz"
- Verdrahtung betroffen aber nicht geladen → erst laden (Datei laut Stack-Referenz „Blocking“)
- Externe Kommunikation ohne Datenschutz-Doc → erst laden (laut Stack-Referenz/Profil)
- UI ohne Design-Doc bzw. Mockup → erst laden
- Schema/Vertrag ohne Doc → erst laden (Vertrags-Doku des Profils)
- **Stack-Referenz für einen Schlüssel aus `Code.Stacks` nicht gelesen** → erst lesen
- **Pflichtlesen-Kapitel nicht geladen obwohl Modul betroffen** → laden
- **Akzeptanzkriterien der Aufgabenquelle nicht gelesen** → erst lesen
- **`Code.Mockup-Policy` greift und kein abgenommenes Mockup** → mockup-erstellen (siehe „Anfrage klassifizieren“, Mockup-Hook)
- **Fachliche Invariante würde verletzt werden** → Auswahlfrage (Trotzdem fortsetzen / Abbrechen / Andere Lösung)
- **Migration / Backward-Compatibility wäre nötig** → Auswahlfrage (Daten löschen + neu anlegen / Migration explizit gewünscht / Abbrechen) — Frühphasen-Prinzip laut `Code.Architekturregeln`

→ NICHT blind coden, per Auswahlfrage nachfragen welche Datei noch geladen werden muss.

### Code erzeugen

Standards aus den Architekturregeln und dem Pflichtkontext des Projekts, Referenzimplementierungen als Muster. Nichts fest
verdrahten, was das Profil als dynamisch nennt.

### Tests (Pflicht, Checks aus `Code.Tests`)

1. Für jede Akzeptanz-Zeile aus der Aufgabenquelle einen Test schreiben oder erweitern
   (Unit für Domäne/Selektoren, E2E für Bedienung; Muster und Orte laut Stack-Referenz „Tests“)
2. **Claude Code:** die Checks aus `Code.Tests` ausführen (dazu Build und Lint, soweit dort genannt).
   Exit-Code 0 ist Bedingung für den Commit.
   Es laufen nur Checks, deren Pfad-Muster eine geänderte Datei trifft; übersprungene werden genannt. Unabhängige
   Checks laufen gleichzeitig, lange im Hintergrund mit Ausgabe in eine Datei, die vollständig gelesen wird – Regeln in
   `skills/git-commit-helper/SKILL.md#Prüfläufe vor dem Commit`. Ist ein Pre-Commit-Check hier schon grün gelaufen und
   seitdem keine Datei mehr geändert, läuft er vor dem Commit nicht noch einmal. In Claude Code übernimmt das das
   Skript von git-commit-helper: `python3 <Skills-Ordner>/git-commit-helper/scripts/checks.py --checks <Code.Tests, mit
   Komma>`.
   **Cowork-Chat:** [references/cowork.md](references/cowork.md#tests-und-selbst-review-im-cowork-chat).
3. **Tests rot** → Auswahlfrage: „Fix jetzt“ / „Test anpassen (Begründung in Aufgabenquelle)“ /
   „Abbrechen“. Nie einen roten Test still löschen oder überspringen.
4. Ergebnis melden als Tabelle Check / Dauer / Ergebnis, übersprungene Checks eingeschlossen; dazu Anzahl der
   Tests, was rot war und warum. Kein „Tests laufen“ ohne Ausgabe.

### Selbst-Review (Pflicht vor dem Commit)

Tests finden nicht alles. Vor dem Commit den eigenen Diff mit frischem Blick prüfen: Fehler, Randfälle, Sicherheit,
unnötige Komplexität.

1. **Claude Code:** den eingebauten Skill `code-review` auf den aktuellen Diff laden (Stufe `low`, im Modus Deep
   `medium`). **Cowork-Chat:** [references/cowork.md](references/cowork.md#tests-und-selbst-review-im-cowork-chat).
   Das Review meldet nur; beheben, testen
   und committen macht dieser Skill. Hat es doch Dateien geändert oder committet (`git status`, `git log`), das dem
   Nutzer sagen und den Stand prüfen, bevor es weitergeht.
2. Jeden Befund beheben oder mit Begründung stehen lassen; nach einer Korrektur die betroffenen Checks aus „Tests“
   erneut laufen lassen.
3. Ergebnis als Zeile im Commit-Bericht (`🔍 Selbst-Review`).

Entfällt nur, wenn der Diff keinen Code enthält (nur Doku); dann im Bericht „entfällt: kein Code“.

### Ausgabe

**Claude Code:** Dateien werden direkt geändert; Ausgabe im Chat ist
die Zusammenfassung (Dateien, Tests, Commit), nicht der Code.

**Cowork-Chat:** Ausgabeformat (komplett, SUCHE/ERSETZE, Download) nach
[references/cowork.md](references/cowork.md#ausgabeformat).

### Commit und Doku-Hinweise (→ git-commit-helper + doc-pflege)

Format, Versionsquelle und Bump-Regel kommen aus dem Skill-Profil (`Commit.Format`, `Commit.Versionsquelle`,
`Commit.Versionsregel`; git-commit-helper). Die Doku-Zeilen (DocMaintenanceHints) sind die Punkte aus
`Commit.Doku-Check`. Beispiele aus zwei Projekten: [references/beispiele.md](references/beispiele.md#doku-check-und-commit).

```
[vX.Y.Z] Modul, Typ: Kurztitel

📝 Doc-Pflege nötig:
- <je Punkt aus Commit.Doku-Check>: [Ja/Nein]
- Frontmatter / Kopf: [welche Docs]

🧪 Tests: [Befehl, Ergebnis, Exit-Code]
🔍 Selbst-Review: [Stufe, Befunde, behoben / begründet offen]
📂 Gelesene Dateien: [Liste]
📋 Nur Kopf gelesen: [Liste]
⚠️ Annahmen: [falls vorhanden]
🚫 Nicht geladen: [Begründung]
```

**Version-Bump unklar?** Auswahlfrage nach den Grundsätzen („Commit-Version unklar“).

### Auslieferung (Schritte aus `Code.Auslieferung`)

Nur wenn das Profil eine Auslieferung nennt. **Claude Code** führt sie aus und prüft das
Ergebnis; im Cowork-Chat: [references/cowork.md](references/cowork.md#auslieferung). Die Schritte stehen im Profil
(`Code.Auslieferung`), die
Prüfreihenfolge je Stack in der Stack-Referenz (z.B. home-assistant: Deploy → check_config →
reload/restart → Zustand prüfen). Zum Schluss dem User sagen, was er wie sichtprüfen soll.

### Tracker-Abgleich (optional)

Nur wenn das Projekt einen Tracker führt (`Tracker.Provider`). Nach erfolgreichem Commit prüfen:
1. Gibt es eine offene Aufgabe, die zu dieser Änderung passt?
   - über tracker suchen (`tracker suche`) mit Schlüsselwörtern aus dem Commit-Titel
2. **Wenn Kandidaten gefunden → Auswahlfrage:**
   ```
   Frage: "Commit passt zu folgenden Aufgaben. Welche soll auf Done?"
   Optionen:
   - "<PRÄFIX>-NNN | <Titel der Aufgabe>"
   - "<PRÄFIX>-NNN | <andere passende Aufgabe>"
   - "Keine Aufgabe passt"
   - "Neue Aufgabe anlegen"
   ```
3. Bei "Neue Aufgabe anlegen" → `tracker neu` aufrufen
4. Bei Aufgaben-Auswahl → `tracker done` aufrufen
5. NICHT automatisch schließen — nur vorschlagen
6. Alle ClickUp-Operationen über den **tracker-Skill**, NICHT direkt

Beispiel aus einem Projekt: [references/beispiele.md](references/beispiele.md#tracker-abgleich).

---

## Aufgaben-Stichwörter

Klingt ein Thema im Gespräch offensichtlich nach einer späteren Aufgabe, für die es noch keine gibt (z.B. „das müssen
wir noch bauen“, „ins backlog“), fragt Claude in Claude Code per Auswahlfrage: „Aufgabe jetzt anlegen (`tracker neu`)“ /
„Am Befund-Ort vermerken“ (`Code.Befund-Ort`) / „Nichts“. Einen Chat-Anker gibt es hier nicht, weil Claude Code weder
Chat-Suche noch `[ANKER-LIVE]`-Memory hat. Im Cowork-Chat setzt Claude stattdessen einen Auto-Anker:
[references/cowork.md](references/cowork.md#auto-anker-bei-aufgaben-stichwörtern).

---

## Arbeit aufteilen

In Claude Code kann die Sitzung Teile der Arbeit an Agenten geben: Lesen und Suchen (`erkunder`), Checks (`pruefer`)
und ein unabhängiges Gutachten (`gutachter`). Den Code schreibt die Sitzung selbst. Das lohnt sich bei viel Lesen und
langen Checks; im Modus Lite nicht. Für die schwersten Aufgaben darf die Sitzung Fable nehmen und sagt das dem Nutzer
in einer Zeile. Was die Agenten liefern, prüft die Sitzung, bevor sie es übernimmt; Commit, Push, Auslieferung und
Neustart bleiben bei ihr. Wann, welcher Agent, welches Modell:
[references/agenten.md](references/agenten.md).

---

## Modus-Übersicht

| Modus | Kopf (Docs) | Langform | Code | Impact | Tests |
|-------|-------------|----------|------|--------|-------|
| Lite | max 3 | max 2 | 1-3 | Kurz | bestehende laufen lassen |
| Standard | max 6 | max 4 | 3-8 | Voll | + je Akzeptanz-Zeile ein Test |
| Deep | max 10 | max 8 | 5-12+ | Voll + Blocking | + E2E für den Benutzerfluss; Mockup-Hook |

Kopf und Langform zählen nur Docs mit Kopf (Abschnitt „Kopf zuerst lesen“).

---

## VERBOTEN

- Code ohne Pflichtkontext des Profils (`Code.Pflichtkontext`) und ohne die Stack-Referenzen aus `Code.Stacks`
- Kopf zuerst lesen überspringen, wo die Docs einen Kopf haben
- Pflichtlesen-Kapitel ignorieren
- Fachliche Invarianten ignorieren
- Annahmen ohne geladene Dateien
- Impact Check weglassen
- DocMaintenanceHints weglassen
- Branch automatisch annehmen — ohne Branch-Policy, Shell oder Auswahlfrage
- Hardcodierte absolute Pfade bei Dateizugriff, in keiner Umgebung
- ClickUp-Tasks direkt erstellen/schließen (→ immer über tracker-Skill)
- Tasks automatisch als Done markieren ohne User-Bestätigung
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER Auswahlfrage (Branch-Auswahl, wenn die Shell ihn nicht liefert; Task-Zuordnung nach Commit; Modus-Auswahl bei Unsicherheit; Blocking-Condition-Auflösung, wenn Kandidaten bekannt)
- **Commit bei roten Tests** oder ohne den Testbefehl des Profils ausgeführt zu haben (Claude Code)
- **Roten Test löschen oder überspringen** ohne Auswahlfrage und Begründung
- **Checks laufen lassen, deren Pfad-Muster keine geänderte Datei trifft**, oder übersprungene Checks verschweigen
- **Akzeptanzkriterien der Aufgabenquelle ignorieren** — sie sind die Testliste
- **Deep-UI-Umbau ohne Mockup**, wenn `Code.Mockup-Policy` greift — außer der User entscheidet es per Auswahlfrage
- **Auslieferung vergessen**, wenn das Profil eine nennt — nach dem Commit ist die Änderung erst fertig, wenn sie läuft
- **Stack-Begriffe eines Projekts (WPF, DI, SQLite, XAML) für ein anderes annehmen** — Schichten und Kopplung aus der Stack-Referenz des Profils
- **Sprachspezifisches in die SKILL.md schreiben** — gehört nach `references/stacks/<key>.md`; die SKILL.md bleibt neutral
- Optionen im Chat aufzählen und auf getippte Antwort warten
- Migration / Backward-Compatibility automatisch bauen ohne User-Freigabe (Frühphasen-Prinzip, `Code.Architekturregeln`)
- **Commit ohne Selbst-Review des Diffs** (Abschnitt „Selbst-Review“) oder mit offenem Befund ohne Begründung
- **Einen Agenten pushen, einspielen, neu starten oder Aufgaben im Tracker ändern lassen**, oder Ergebnisse eines
  Agenten ungeprüft übernehmen (Abschnitt „Arbeit aufteilen“)
- Verbote zum Auto-Anker im Cowork-Chat: [references/cowork.md](references/cowork.md#verboten-im-cowork-chat); in Claude
  Code statt Anker die Auswahlfrage aus „Aufgaben-Stichwörter“
