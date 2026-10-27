# PROMPT-STRUKTUR (beide Umgebungen)

Aufbau des Handover-Prompts im Cowork-Chat wie in Claude Code (`SKILL.md`, Abschnitte „ABLAUF IN CLAUDE CODE“ und
„Ablauf im Cowork-Chat“). Platzhalter in spitzen Klammern kommen aus dem Skill-Profil; Beispielwerte:
[beispiele.md](beispiele.md).

```
# [Projektname] Teil [N+1]

Weiterführung aus **[Projektname] Teil [N]**.

---

## Aktueller Stand
- **Version:** [Version aus Commit.Versionsquelle]
- **Letzter Commit:** [Hash + Message]
- **Branch:** [Branch]
- **Chat-URL Teil [N]:** [aktuelle Chat-URL falls bekannt]

## Erledigt in Teil [N]
- [Erledigte Punkte/Commits]

## Offene Punkte (aus ClickUp + Chat)

### ClickUp offen (mehrere Listen: nach Liste gruppiert; Ein-Listen-Projekte: nach Status):
<Liste oder Status>:
- [Priority] [Meilenstein] <PRÄFIX>-NNN | Beschreibung
<Liste oder Status>:
- [Priority] [Meilenstein] <PRÄFIX>-NNN | Beschreibung
(nur Listen/Status mit offenen Tasks auflisten)

### Offene Anker aus Teil [N] (aus [ANKER-LIVE]):
| ID | Typ | Thema |
|----|-----|-------|
| TEMP-xxx | offen | Thema (noch kein Task) |
| 86c9xxx | erstellt | Thema (<PRÄFIX>-NNN) |
(nur wenn Einträge vorhanden — sonst Sektion weglassen; nur Cowork)

### Offene Punkte aus Memory (gefiltert nach Rubriken; nur Cowork):

#### VERIFY
- [Eintragstext]

#### ARCH-OPEN
- [Eintragstext]

#### INFRA-TODO
- [Eintragstext]

#### REVIEW-PENDING
- [Eintragstext]
(leere Rubriken weglassen; wenn alle leer: ganze Sektion weglassen)

### Im Chat neu erkannt (noch nicht in ClickUp):
- Modul — Beschreibung

### Im Chat erledigt (noch nicht in ClickUp markiert):
- <PRÄFIX>-NNN | Beschreibung

### Sonstige offene Punkte (nicht in ClickUp):
- [Pending Commits]
- [Pending Doc-Updates]
- [Pending Frontmatter/Quickload-Updates]
- [Neue Fachliche Invarianten die noch eingetragen werden müssen]

## Nächste Schritte (geplant)
- [Prioritäten — nach Meilenstein und Priorität laut Tracker-Config, high/urgent zuerst]

## Aktive Entscheidungen
- [Architektur-Entscheidungen]
- [Offene Fragen]

## Kontext
- [Wichtige Erkenntnisse]
- [Warnungen]
- [Docs die gelesen werden sollten]
- [Docs deren Quickload/Invarianten veraltet sein könnten]

## Regeln (Erinnerung) — aus dem Skill-Profil der CLAUDE.md erzeugt, nicht fest
- Commit: <Commit.Format, Commit.Module, Commit.Versionsquelle, Commit.Versionsregel>
- Tracker: <Präfix, Liste, Übergänge aus Tracker.Config>; tracker-Skill ist einzige Schreibschnittstelle zu ClickUp
- Docs: <Doku.Router, Doku.Pflichtdokumente, Code.Aufgabenquelle>
- Code: <Code.Tests, Branch-Policy, Code.Auslieferung>; Code-Arbeit nur mit dem Skill code-erstellen (vor
  der ersten Dateiänderung laden); Tickets → ticket, Mockups → mockup-erstellen, Doku → doc-pflege, ClickUp → tracker
- Ein Schritt pro Antwort; nachfragen wenn Kontext fehlt → Auswahlfrage bei festen Optionen
- Wer committet: Cowork der User; Claude Code Claude selbst
(Projekt ohne Profil: Regeln aus dem Rückfall in SKILL.md, Abschnitt „Voraussetzung: Skill-Profil“; Beispiel in
beispiele.md, Abschnitt „Regeln ohne Profil (BPM)“)
```
