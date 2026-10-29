# Beispielwerte BPM und Heidi

Werte aus zwei Projekten. Sie zeigen, wie die Felder aus `../SKILL.md#Voraussetzung: Skill-Profil` gefüllt werden; für
jedes Projekt gilt nur dessen eigenes Profil. BPM ist eine C#/WPF-Anwendung mit Doku nach DOC-STANDARD, Heidi eine
Home-Assistant-Karte mit Backend (Dreame X60). Die Spalten stammen aus dem älteren `## Code-Profil`.

## Inhalt

- Profilwerte BPM und Heidi
- Rückfall ohne Profil (BPM)
- Ladereihenfolge BPM
- Pflichtkontext Heidi
- Branch
- Doku-Check und Commit
- Tracker-Abgleich
- Aufgaben-Stichwörter

## Profilwerte BPM und Heidi

| Feld (alt) | Skill-Profil | BPM | Heidi |
|------|------|-----|-------|
| Stacks | `Code.Stacks` | `csharp-wpf` | `typescript-lit, home-assistant, python` |
| Build/Lint | `Code.Tests` (Checks) | laut INDEX.md | `npm run check`, `npm run lint`, `npm run build` |
| Pflicht-Docs | `Code.Pflichtkontext` | INDEX.md → Quickload → Invarianten → Pflichtlesen (DOC-STANDARD Kap. 8) | CLAUDE.md, docs/HANDOFF.md, BAUPLAN.md Abschnitt 2 (Regeln) + 4 (Vertrag) |
| Aufgabenquelle | `Code.Aufgabenquelle` | ClickUp-Task (Description-Template) | BAUPLAN.md Abschnitt 8 Karte + ClickUp DX-Task |
| Schichten / Kopplung | `Code.Architekturregeln` | View→ViewModel, Service→Interface+DI, DB→Schema | contract → device/profile → selectors → Komponenten; Schreiben nur über DxApi |
| Tests | `Code.Tests` | laut INDEX.md | `npm test` in dreame_x60/card (check, unit, build, E2E) |
| Auslieferung | `Code.Auslieferung` | laut INDEX.md | `deploy.ps1 -OnlyCard` + Ressourcen-Version; Backend: check_config + reload/restart |
| Mockup-Pflicht | `Code.Mockup-Policy` | nein | ja (Herbert: große Umbauten zuerst als Mockup) |
| Notiz-Ort | `Code.Befund-Ort` | Memory / Backlog | BAUPLAN.md Abschnitt 10 |
| Frühphasen-Prinzip | `Code.Architekturregeln` | INDEX.md (Daten löschen und neu anlegen statt Migration) | – |

## Rückfall ohne Profil (BPM)

Fehlen Skill-Profil und `## Code-Profil`: `INDEX.md` im Repo als Profil nehmen (BPM-Weg, optional DOC-STANDARD.md;
Stack `csharp-wpf`).

## Ladereihenfolge BPM

BPM: verbindliche Ladereihenfolge aus DOC-STANDARD.md Kapitel 8 (Quickload-First-Pass):

```
1. INDEX.md → Routing (welche Doc?)
2. Frontmatter + AI-Quickload lesen → Filter (relevant? welches Kapitel?)
3. Fachliche Invarianten prüfen → Sofort sichtbar ohne Langform
4. Pflichtlesen-Kapitel laden → Immer wenn Modul betroffen
5. Weitere Kapitel nur bei Bedarf nachladen
```

Pflicht-Docs BPM: INDEX.md → Task-to-Doc Routing → Primary/Secondary/Reference.

## Pflichtkontext Heidi

CLAUDE.md (automatisch), HANDOFF.md Abschnitt 3e, BAUPLAN.md Abschnitt 2 und 4, bei Domänen-Logik Abschnitt 6.
Aufgabenquelle: Bauplan-Karte (Abschnitt 8) bzw. ClickUp-Task.

## Branch

Heidi nannte im älteren Code-Profil den Pflicht-Branch `dreame_x60`; im Skill-Profil v1 heißt das
`Branch-Policy: fixed:dreame_x60`.

## Doku-Check und Commit

Doku-Zeilen im Commit-Bericht, BPM-Beispiel:

```
📝 Doc-Pflege nötig (BPM-Beispiel):
- INDEX.md: [Ja/Nein]
- DB-SCHEMA.md: [Ja/Nein]
- CHANGELOG.md: [Ja/Nein]
- ADR.md: [Ja/Nein]
- Frontmatter: [welche Docs]
- Quickload: [welche Docs]
```

Heidi: Bauplan-Statusliste, Abschnitt 10/10a, HANDOFF 3e, Abschnitt 4 + contract.ts bei neuen Entitäten.

Beispiel-Ausgabe nach Commit (BPM):

```
[v0.25.30] PlanManager, Fix: 5998er Statikplaene Erkennung

📝 Doc-Pflege nötig: Nein
🎯 ClickUp: 1 passender Task gefunden
```
→ dann Auswahlfrage mit dem Task als Option

## Tracker-Abgleich

Optionen der Auswahlfrage nach dem Commit, BPM-Beispiel:

```
- "BPM-004 | 5998er Statikplaene Erkennung"
- "BPM-007 | andere passende Task"
- "Kein Task passt"
- "Neuen Task anlegen"
```

## Aufgaben-Stichwörter

| Wert | BPM | Heidi |
|------|-----|-------|
| Befund-Ort (Auswahlfrage in Claude Code) | Memory / Backlog | Bauplan Abschnitt 10 |
| Anker-Präfix (Cowork) | `BPM` | `DX` |
