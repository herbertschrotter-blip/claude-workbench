# Beispielwerte BPM und Heidi

Werte aus den Review-Profilen von BPM und Heidi. Sie zeigen, wie die Felder der Review-Config gefüllt werden
(`../SKILL.md#Voraussetzung: Skill-Profil`); für BPM gelten sie außerdem als Rückfall (Abschnitt „Rückfall ohne Profil
(BPM)“). Für jedes andere Projekt gilt nur dessen eigene Config.

## Inhalt

- Profilwerte BPM und Heidi
- Rückfall ohne Profil (BPM)
- Themen
- Doc-Laderegel BPM und Heidi
- Pflicht-Blöcke
- Ergebnis-Ort

## Profilwerte BPM und Heidi

| Feld | Bedeutung | BPM | Heidi |
|------|-----------|-----|-------|
| Review-Ablage | Ordner der CGR-Serien + `INDEX.md` | `Docs/Referenz/chatgpt-reviews/` | `docs/chatgpt-reviews/` |
| Themen | erlaubte `<thema>`-Werte (kebab-case) | skillsystem, docs-refactor, bpm-architektur, datenschutz-dbschema | heidi-v2, karte, backend, geraeteprofil |
| GitHub-Repo | Owner/Repo für den Repo-Zugriff-Block | aus INDEX.md Projekt-Metadaten | `herbertschrotter-blip/herbert-smarthome` |
| Pflicht-Block | Abschnitt, der in jedem Initialprompt steht | „Frühphase“ (keine Migration, Reset statt Backward-Compat) | „Regeln des Neubaus“: Bauplan Abschnitt 2 in Kurzform, Paritätsregel (Abweichung nur mit PD-Eintrag), Entitäts-Vertrag eingefroren, v1 nur Referenz |
| Kontextquelle | woraus „Projektkontext“ im Prompt gebaut wird | Quickloads + Invarianten (DOC-STANDARD Kap. 8) | Bauplan Abschnitt 2 (Regeln), 4 (Vertrag), 7 (Seiten), die betroffene Karte aus 8, HANDOFF 3e; max. 3–5 Blöcke |
| Reviewer-Rolle | Rolle im Prompt | „erfahrener .NET/WPF-Architekt“ | „erfahrener Frontend-Architekt für Web Components / Home Assistant“ |
| Ergebnis-Ort | wohin Entscheidungen nach Phase 3 gehen | ADR.md, BACKLOG.md | Bauplan Abschnitt 10 (Notiz, Art `Widerspruch`/`Befund`), 10a bei Abweichung, HANDOFF 3e |

In einer Review-Config stehen Review-Ablage, Themen und GitHub-Repo unter „Allgemein“, die übrigen Felder je Thema.

## Rückfall ohne Profil (BPM)

Hat ein Repo weder `Review.Config` noch `## Review-Profil`, aber den Ordner `Docs/Referenz/`, gelten die BPM-Werte aus
„Profilwerte BPM und Heidi“.

## Themen

Beispiel BPM:
- `skillsystem` — Skill-System-Architektur, Trigger, Description-Schema
- `docs-refactor` — Dokumentationsstruktur, Frontmatter, INDEX, Quickloads
- `bpm-architektur` — BPM-Code-Architektur (SQLite, Domain, Infra)
- `datenschutz-dbschema` — DSGVO, DB-Schema, Whitelist

Beispiel Heidi: `heidi-v2` (Neubau der Karte), `karte`, `backend`, `geraeteprofil`.

## Doc-Laderegel BPM und Heidi

BPM (DOC-STANDARD.md Kapitel 8):
1. INDEX.md → Welche Docs sind für das Review-Thema relevant?
2. Quickloads der relevanten Docs lesen
3. Fachliche Invarianten sammeln
4. Relevante Quickloads + Invarianten als Kontext in den Prompt packen

Heidi:
1. Bauplan Abschnitt 2 (Regeln) → Kurzform der Regeln, die das Thema berühren
2. Abschnitt 4 (Entitäts-Vertrag) → nur die betroffenen Entitäten/Dienste
3. Die betroffene Aufgabenkarte aus Abschnitt 8 (Ziel, Nicht ändern, Akzeptanz) und Abschnitt 7 (Seite)
4. HANDOFF 3e → Stand, Version, Stolpersteine; Abschnitt 10/10a → bekannte Befunde und Abweichungen

So weiß ChatGPT z.B. "SQLite ist SoR" (BPM) oder "Schreiben nach HA nur über DxApi, Vertrag eingefroren"
(Heidi) ohne dass der User es manuell einfügt. Bei BPM füllen „Zweck“ und „Fachliche Invarianten“ im Block
„Projektkontext“ die Quickloads der Docs.

## Pflicht-Blöcke

**Heidi – „Regeln des Neubaus“:**

```
## Regeln des Neubaus (PFLICHT-Hinweis)

- v1 (heidi/archiv/heidi-panel.js) ist nur Referenz für Verhalten und Vektoren; v2 wird portiert, nicht neu erfunden.
- Der Entitäts-Vertrag (Bauplan Abschnitt 4) ist eingefroren; neue Entitäten nur mit Vertragsänderung.
- Jede gewollte Abweichung vom v1-Verhalten braucht einen PD-Eintrag (Abschnitt 10a) mit Freigabe durch Herbert.
- Schreiben nach HA nur über die API-Klasse; Komponenten lesen nur Views aus Selektoren; nichts fest verdrahten,
  was Roboter oder HA liefern.
- Keine externen Ressourcen (Fonts, CDN); Tests (npm test) grün vor jedem Commit.

Quelle: docs/dreame_x60/BAUPLAN.md Abschnitt 2.
```

**BPM – „Frühphase“:** INDEX.md hat das Kapitel "Projekt-Phase (VERBINDLICH)". Solange dieses Kapitel
besteht, MUSS jeder Initialprompt einen Frühphasen-Block enthalten, damit
ChatGPT keine Migrations-/Backward-Compatibility-Vorschläge macht die wir
ausdrücklich nicht wollen.

**Block der eingefügt werden muss (BPM):**

```
## Frühphase (PFLICHT-Hinweis)

BPM ist in früher Entwicklung ohne Produktivdaten.

Konsequenzen für deine Architektur-Vorschläge:
- KEINE Migrations-Logik vorschlagen
- KEINE Backward-Compatibility-Patterns
- KEINE Legacy-Tolerance in Parsern/Loadern/Deserializern
- Bei Schema-/Config-/DB-Änderungen: stattdessen "Datei löschen, neu anlegen lassen"
  als gewollter Standardweg

Ausnahme: Nur wenn explizit "Migration bauen" im Prompt steht.

Quelle: INDEX.md Kapitel "Projekt-Phase".
```

## Ergebnis-Ort

- „Entscheidungen an Ergebnis-Ort“: Heidi: Bauplan Abschnitt 10 als Notiz `[Datum] [Aufgabe] Widerspruch/Befund · Schwere: … Entscheidung Herbert: …`,
  Abweichung vom v1-Verhalten zusätzlich als PD-Eintrag 10a; BPM: ADR.md.
- Verweise: README der Serie nennt die Bauplan-Notizen bzw. ADRs; Notiz bzw. ADR nennt die CGR-ID.
