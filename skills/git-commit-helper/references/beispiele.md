# Beispielwerte

Werte aus mehreren Projekten (BPM, Heidi, Skill-Repo, Konfigurationsordner von Home Assistant). Sie zeigen, wie die
Felder aus `../SKILL.md#Voraussetzung: Skill-Profil` gefüllt werden; für jedes Projekt gilt nur dessen eigenes Profil.

## Inhalt

- Älteres Commit-Profil
- Aufgabennummer im Kurztitel
- Versionsregel
- Doku-Check
- Commit ohne Format

## Älteres Commit-Profil

Rückfall, wenn die CLAUDE.md noch kein `## Skill-Profil` hat. Die Versionsquelle ist die der Heidi-Karte:

```
## Commit-Profil
- Modul-Namen: <feste Liste, z.B. Karte, Backend, Doku>
- Versionsquelle: <Datei und Feld, z.B. dreame_x60/card/package.json "version">
- Bump-Regel: <Standard | Vorabversion: jede Änderung zählt hoch | eigene Regel>
- Doku-Checkliste: <Datei → wann anfassen, eine Zeile je Datei>
```

Modul-Namen entsprechen „Module“, Bump-Regel „Versionsregel“, Doku-Checkliste „Doku-Check“.

## Aufgabennummer im Kurztitel

- Projekt mit Bauplan (Heidi): der Bauplan-Schritt am Anfang des Kurztitels; in der zweiten Zeile ein Verweis auf den
  Bauplan-Abschnitt.
- Projekt mit ClickUp: die ClickUp-ID am Anfang des Kurztitels.

## Versionsregel

- „Vorabversion: jede eingespielte Änderung zählt die Vorab-Nummer hoch, unabhängig vom Typ“
- „neue Nummer nur bei Änderungen unter `skills/**`“ (Skill-Repo)

## Doku-Check

Beispiel einer Checkliste (Projekt mit ADR/Quickload-Standard, BPM):

```
Checkliste:
- [ ] Neues Doc? → INDEX.md
- [ ] Neues Feature? → CHANGELOG.md
- [ ] DB geändert? → DB-SCHEMA.md
- [ ] Neue Architekturentscheidung? → ADR.md
- [ ] Neues Konzept? → INDEX.md + BACKLOG.md
- [ ] Neuer Entry Point? → INDEX.md
- [ ] Doc geändert? → Frontmatter + Quickload aktuell?
- [ ] Fachliche Invarianten betroffen? → Quickload prüfen
```

Beispiel einer Checkliste (Projekt mit Bauplan/Übergabe, Heidi):

```
Checkliste:
- [ ] Bauschritt fertig? → Statusliste im Bauplan
- [ ] Befund oder Entscheidung? → Bauplan Abschnitt „Notizen aus dem Bau“
- [ ] Stand geändert? → HANDOFF.md
- [ ] Neue Entität oder Dienst? → Entitäts-Vertrag im Bauplan
```

## Commit ohne Format

Konfigurationsordner von Home Assistant: `Commit.Format`, `Commit.Module` und `Commit.Versionsquelle` sind `none`. Die
erste Zeile ist dann nur `Typ: Kurztitel`, ohne Versionsdatei.
