# Beispielwerte BPM und Heidi

Werte aus zwei Projekten. Sie zeigen, wie die Felder aus `../SKILL.md#Voraussetzung: Skill-Profil` gefüllt werden; für
jedes Projekt gilt nur dessen eigenes Profil. „–“ heißt: im Skill nicht als Beispiel geführt.

## Inhalt

- Profilwerte BPM und Heidi
- Rückfall ohne Profil (BPM)
- Pfade BPM
- Doc-Laderegel
- Schema- und Datenänderungen
- Doku-Hinweise
- Projekt-Init
- Router und Begleit-Docs
- Neue Doc
- Sitzungsabschluss
- Commit

## Profilwerte BPM und Heidi

Kurz: BPM führt Frontmatter, Quickload und Kapitelstruktur nach `DOC-STANDARD.md`; Heidi den Bauplan (Statusliste,
Aufgabenkarten, Notizen, PD-Register) und das HANDOFF.

| Feld (älteres Doku-Profil) | Skill-Profil | BPM | Heidi |
|------|--------------|-----|-------|
| Doc-Standard | `Doku.Standard` | `DOC-STANDARD.md` (Frontmatter, Quickload, Kapitelvorlagen, Ladereihenfolge Kap. 8) | Bauplan selbst (Abschnitt 0–2, Formate in 8/10/10a) |
| Router / Index | `Doku.Router` | `INDEX.md` (Task-to-Doc, Primary/Secondary/Reference) | `CLAUDE.md` (Repo-Aufbau) + `docs/HANDOFF.md` Abschnitt 5 |
| Pflicht-Docs | `Doku.Pflichtdokumente` | Tabelle „Pfade BPM“ unten | `docs/dreame_x60/BAUPLAN.md`, `docs/HANDOFF.md`, `CLAUDE.md`, `heidi/CLAUDE.md`, `docs/dreame_x60/*.md` (Pläne) |
| Doc-Typen + Vorlagen | `Doku.Standard` | ADR, Konzept, Modul-Doc, Architektur (Kapitelvorlagen Kap. 7) | Aufgabenkarte (Voraussetzung/Ziel/Nicht ändern/Akzeptanz/Tests/Dateien), Notiz Abschnitt 10 (Datum/Aufgabe/Art/Schwere/Text/Entscheidung), PD-Eintrag 10a (id/bereich/v1/v2/grund/spec_test/Status), Plan-Doc (Stufen, Stand) |
| Validierung | `Doku.Validierungsregeln` | Frontmatter/Quickload Stufe A/B | Statusliste ↔ ClickUp ↔ Code; PD-Register vollständig; Notizformat; HANDOFF 3e aktuell; Abschnitt 4 ↔ contract.ts |
| Frühphasen-Regel | – (Regel im Router oder Standard des Projekts) | ja (INDEX.md Kapitel „Projekt-Phase“) | nein – stattdessen Regel: Abweichung von v1 nur mit PD-Eintrag |
| Advisory | `Commit.Doku-Check` | Doku-Checkliste des Commit-Profils | Doku-Checkliste des Commit-Profils |
| Sitzungsabschluss | `Doku.Sitzungsabschluss` | Handover via chat-wechsel | Statusliste, HANDOFF 3e, offene Punkte Abschnitt 4, Commit + Push |
| Commit-Modul | `Commit.Module` | `Docs` | `Doku` |

Pflichtteile der Vorlage (BPM): Docs in Kern/Module/Referenz brauchen Frontmatter. Vorlage bei neuen Docs: BPM
Frontmatter, Quickload, Kapitelvorlage; Heidi Karten-/Notiz-/PD-Format.

## Rückfall ohne Profil (BPM)

Fehlen Skill-Profil und Doku-Profil, aber das Repo hat `INDEX.md` + `DOC-STANDARD.md`: beide als Profil nehmen (BPM-Weg).

## Pfade BPM

| Datei | Pfad im Repo |
|-------|-------------|
| INDEX.md | `/INDEX.md` (Repo-Root) |
| DOC-STANDARD.md | `/Docs/Referenz/DOC-STANDARD.md` |
| BACKLOG.md | `/Docs/Kern/BACKLOG.md` |
| ADR.md | `/Docs/Referenz/ADR.md` |
| DB-SCHEMA.md | `/Docs/Kern/DB-SCHEMA.md` |
| CHANGELOG.md | `/Docs/Referenz/CHANGELOG.md` |
| DEPENDENCY-MAP.md | `/Docs/Referenz/DEPENDENCY-MAP.md` |
| VISION.md | `/Docs/Referenz/VISION.md` |
| Architektur-Doc | `/Docs/Kern/BauProjektManager_Architektur.md` |
| CODING_STANDARDS.md | `/Docs/Kern/CODING_STANDARDS.md` |
| DSVGO-Architektur.md | `/Docs/Kern/DSVGO-Architektur.md` |

## Doc-Laderegel

BPM (DOC-STANDARD.md Kapitel 8):
1. INDEX.md → Routing
2. Frontmatter + Quickload → Filter
3. Fachliche Invarianten → Prüfen
4. Pflichtlesen → Laden wenn betroffen
5. Langform nur bei Bedarf

Heidi:
1. CLAUDE.md (automatisch) → Repo-Aufbau, Profile
2. HANDOFF.md Abschnitt 3e + 4 → Stand und offene Punkte
3. BAUPLAN.md Statusliste (Abschnitt 1) → welche Aufgabe, welcher Status
4. Nur die betroffene Aufgabenkarte (Abschnitt 8) und Regeln (Abschnitt 2)
5. Abschnitt 10/10a nur, wenn Befund oder Abweichung einzutragen ist

## Schema- und Datenänderungen

**BPM – Frühphasen-Regel.** Gilt, solange INDEX.md das Kapitel "Projekt-Phase (VERBINDLICH)" hat; Ausnahme, wenn es
offiziell entfernt wurde.

Wenn z.B. DB-SCHEMA.md, ADR.md oder ein Konzept-Doc eine Schema-Änderung
beschreibt, NICHT formulieren wie "Migration von Schema v2 auf v3":

❌ Falsch:
> Migration von SchemaVersion 2 auf 3:
> 1. ALTER TABLE plans ADD COLUMN ...
> 2. UPDATE plans SET ... WHERE schema_version = 2
> 3. UPDATE plans SET schema_version = 3

✅ Richtig:
> Schema-Änderung von 2 auf 3 (Frühphase, keine Migration):
> Betroffene Datei(en): bpm.db
> Aktion: User löscht bpm.db → BPM erstellt sie beim nächsten Start neu mit Schema v3.

JSON-Configs in BPM: `profiles/*.json`, `manifest.json`, `settings.json`.

**Heidi – Paritätsregel statt Frühphasen-Regel.** Jede gewollte Abweichung vom
v1-Verhalten braucht einen PD-Eintrag in Abschnitt 10a mit Status `freigegeben` (Herbert);
ohne Eintrag ist eine Abweichung ein Fehler. Neue Entität oder Dienst → Abschnitt 4 des
Bauplans **und** `contract.ts` im selben Commit.

## Doku-Hinweise

- **BPM:** Neue Tabelle → DB-SCHEMA.md; Architekturentscheidung → ADR.md; neuer Entry Point → INDEX.md; neues Doc →
  INDEX.md + BACKLOG.md.
- **Heidi:** Bauschritt fertig → Statusliste; Befund/Entscheidung → Abschnitt 10 (Abweichung → 10a); Stand geändert →
  HANDOFF 3e; neue Entität/Dienst → Abschnitt 4 + contract.ts.

Merkliste (BPM):

```
📝 Doc-Hinweis: [DB-SCHEMA.md — neue Spalte angelegt]
📝 Doc-Hinweis: [ADR.md — neue Architekturentscheidung]
```

## Projekt-Init

- Details: DOC-STANDARD.md Kapitel 3 (BPM).
- Standard-Doc-Set BPM: INDEX.md, Architektur.md, BACKLOG.md, CHANGELOG.md, ADR.md, DEPENDENCY-MAP.md, ggf. DB-SCHEMA.md.
- Heidi-artig: CLAUDE.md, HANDOFF.md, BAUPLAN.md mit Statusliste/Regeln/Vertrag/Aufgabenkarten/Notizen/Register.
- Vorlagen BPM: Frontmatter + Quickload + Kapitelstruktur.

## Router und Begleit-Docs

- **Router nachziehen** – BPM: INDEX.md, Routing-Eintrag im Primary/Secondary/Reference-Format. Heidi: CLAUDE.md
  „Repo-Aufbau“ und HANDOFF Abschnitt 5 (Referenzen); neue Plan-Docs unter `docs/dreame_x60/` dort verlinken.
- **Begleit-Docs** – BPM: INDEX.md → Doc-Pflege Policy; Heidi: Abschnitt 4 + Abschnitt 10/10a + HANDOFF.

## Neue Doc

- **Vorlage:** BPM: DOC-STANDARD.md Kapitel 7; Heidi: Muster im Bauplan – Aufgabenkarte, Notiz, PD-Eintrag, Plan-Doc.
- **Router für verwandte Docs:** BPM: INDEX.md; Heidi: CLAUDE.md, HANDOFF 5.
- **Doc umbauen:** BPM: Vorlage aus DOC-STANDARD.md.
- **Invarianten-Check BPM** – Zielorte der Antworten:

```
📋 Invarianten-Check:
- Gibt es fachliche Regeln die bei JEDER Änderung gelten?
  → Fachliche Invarianten im Quickload
- Welche Kapitel müssen IMMER gelesen werden?
  → Pflichtlesen im Quickload
- Gibt es Abhängigkeiten zu anderen Modulen?
  → related_docs im Frontmatter
```

## Sitzungsabschluss

| Schritt | BPM | Heidi |
|---------|-----|-------|
| Pflicht am Ende jeder Sitzung | – | Startprompt im Bauplan (Abschnitt 0) |
| Statusliste ↔ Tracker | – | Bauplan Abschnitt 1 ↔ ClickUp DX-Status |
| Entscheidungs-Ort | ADR/BACKLOG | Abschnitt 10, Abweichungen 10a |
| Stand-Abschnitt | – | HANDOFF 3e – Version, was gebaut, Stolpersteine; Datum |
| Offene Punkte | – | HANDOFF Abschnitt 4 |
| `Commit.Doku-Check`, nicht vergessen | INDEX, CHANGELOG | Abschnitt 4 |

## Commit

- Doku-Commit BPM: `[vX.Y.Z] Docs, Docs: [Kurztitel]`; Heidi: Modul `Doku`.
- Sitzungsabschluss: `[vX.Y.Z] <Doku-Modul>, Docs: Sitzungsabschluss <Datum> – <Kurztitel>`.
