# Beispielwerte BPM und Heidi

Werte aus zwei Projekten. Sie zeigen, wie die neutralen Regeln aus `../SKILL.md` in einem Projekt aussehen; für jedes
Projekt gilt nur dessen eigenes Skill-Profil. Die Prüfpunkte hier sind keine Pflicht für andere Projekte.

## Inhalt

- Teilaudit: Modulnamen
- Rückfall ohne Profil
- Doc-Laderegel
- Prüfpunkte je Modul
- Nach dem Report
- Tool-Strategie

## Teilaudit: Modulnamen

Optionen der Auswahlfrage „welches Modul“ aus dem Router des Profils:

| Projekt | Router | Modulnamen |
|---|---|---|
| BPM | `INDEX.md` | Module aus dem Routing |
| Heidi | Bauplan | Karte, Backend, Doku, Tools |

## Rückfall ohne Profil

BPM: Fehlen Skill-Profil und Doku-Profil, gelten `INDEX.md` + `DOC-STANDARD.md` (BPM-Weg).

## Doc-Laderegel

BPM (DOC-STANDARD.md Kapitel 8):
1. INDEX.md → Routing
2. Frontmatter + Quickload → Filter
3. Fachliche Invarianten → Prüfen
4. Langform nur bei Bedarf

Heidi: CLAUDE.md → HANDOFF 3e/4 → Bauplan Statusliste (1), Regeln (2), Vertrag (4) → Karten (8)
nur für die geprüften Schritte → 10/10a für Befunde und Register.

Eine Ladereihenfolge des Projekts nicht einzuhalten, ist verboten; bei BPM ist das die Quickload-Laderegel.

## Prüfpunkte je Modul

Schwerpunkte: BPM INDEX-Routing, Frontmatter, Quickload, Schema, DI. Heidi Bauplan, Vertrag, HANDOFF, PD-Register.

### Modul 1 — Router-Selbst-Check

BPM (INDEX.md):
- Routing-Einträge → Docs existieren?
- Code Entry Points → Dateien existieren?
- Referenzimplementierungen → existieren?
- Routing-Format korrekt (Primary/Secondary/Reference)?
- historical Docs als Primary? → ❌

Heidi (CLAUDE.md „Repo-Aufbau“, HANDOFF Abschnitt 5, Bauplan Abschnitt 5 Zielstruktur):
- Genannte Pfade, Werkzeuge und Docs existieren (`tools/*.ps1`, `docs/dreame_x60/*.md`, `heidi/archiv/`)?
- Profile in der CLAUDE.md vollständig (Commit, Tracker, Code, Doku) und untereinander widerspruchsfrei (Modulnamen, Testbefehl, Pfade)?
- Zielstruktur (Abschnitt 5) ↔ tatsächliche Ordner `src/{domain,ha,components,shared,styles}`?

### Modul 2 — Kern-Docs vs. Code (vorwärts)

BPM:
- 2a. DB-Schema-Check
- 2b. DSGVO-Check
- 2c. Architektur-Check
- 2d. UI-Konsistenz-Check

Heidi:
- 2a. Vertrag → Code: jede Entität/jeder Dienst aus Bauplan Abschnitt 4 ist in `contract.ts` erreichbar (`ENTITIES`, `ROBOT_FEATURES`, `roomEntity`, `SERVICES`)
- 2b. Verbotenes im Repo: `H:\.storage`, `secrets.yaml`, Datenbanken, `prognose/presence_log.csv`, `prognose/runlog.csv`, `access_token`/GPS in Fixtures und Abzügen → jeder Treffer ❌
- 2c. Regeln Abschnitt 2 im Code: kein `shouldUpdate` in der Shell; Schreiben nach HA nur über `DxApi`; Komponenten lesen nur Views aus Selektoren; keine externen Ressourcen; nichts fest verdrahtet, was Roboter/HA liefern (Räume, Optionen, Namen)
- 2d. Statusliste → Code: jeder Schritt `fertig`/`eingespielt` hat Dateien, Tests (`tests/unit`, `tests/e2e`) und einen Commit; `offen` hat keinen Code, der schon behauptet fertig zu sein

### Modul 3 — Code vs. Docs (rückwärts)

BPM:
- 3a. Interface-Implementierung
- 3b. DI-Registrierung
- 3c. Dependencies
- 3d. Code Entry Points

Heidi:
- 3a. Code → Vertrag: Entitäts-IDs oder Dienste im Code (`contract.ts`, `api.ts`, Paket-YAML), die in Abschnitt 4 fehlen
- 3b. Komponenten ohne Karte: `src/components/dx-*.ts` ohne Aufgabenkarte in Abschnitt 8 bzw. ohne Eintrag in Abschnitt 7
- 3c. Selektoren: jeder `memoizeSelector` in `ALL_SELECTORS`; `ids` vollständig (Proxy-Test vorhanden)
- 3d. Abhängigkeiten: `package.json` ↔ Bauplan Abschnitt 3 (Lit, esbuild, Playwright; keine ungenannten Laufzeit-Abhängigkeiten); Version in `package.json`, Lock und Ressourcen-`?v=` gleich

### Modul 4 — Referenz-Docs

BPM:
- 4a. ADR-Status
- 4b. CHANGELOG-Vollständigkeit
- 4c. BACKLOG-Aktualität

Heidi:
- 4a. PD-Register (10a): jede Abweichung von v1, die im Code oder in Abschnitt 10 genannt ist, hat einen Eintrag mit Status `freigegeben`; kein Eintrag `offen` älter als der zugehörige Bauschritt
- 4b. HANDOFF 3e/4: nennt letzten abgeschlossenen Bauschritt und aktuelle Version; offene Punkte haben ClickUp-Bezug oder Begründung
- 4c. Plan-Docs (GERAETEPROFIL, PLANER-NACHHOLEN, UX-TRANSITIONS, ENTITAETEN): Stand-Datum vorhanden, „So funktioniert es heute“ stimmt mit dem Code

### Modul 5 — Aufgabenquelle ↔ Tracker

BPM:
- Module/ vs. Konzepte/ Zuordnung
- INDEX Routing vollständig?
- ClickUp-Aufgaben (BPM-NNN) ↔ BACKLOG

Heidi:
- Bauplan Statusliste (Abschnitt 1) ↔ ClickUp `DX-NNN`-Status (Mapping aus der Tracker-Config des Projekts: fertig→shipped/testing, in Arbeit→in development, offen→backlog); Abweichung ⚠️, fehlende Aufgabe ❌
- Jede Aufgabenkarte hat eine DX-Aufgabe und umgekehrt (Phasen ausgenommen)
- Notizen in Abschnitt 10 mit Format `- [Datum] [Aufgabe] Art · Schwere: … Entscheidung Herbert: …`; Wünsche mit Post-2.0-Aufgabe

## Nach dem Report

- **Titel einer Audit-Aufgabe:** Heidi `DX-NNN | DOKU | Audit: …`.
- **Notiz-Vorschlag:** Heidi – Befunde, die eine Entscheidung von Herbert brauchen (Regel-Widerspruch, Abweichung von
  v1), als Notiz-Vorschlag für Bauplan Abschnitt 10 (Art `Widerspruch`, Entscheidung offen).

## Tool-Strategie

- **Gezielt lesen:** BPM Frontmatter/Quickload, nur erste 30 Zeilen jeder Doc; Heidi Statusliste, Abschnitt 4 und 10a
  gezielt lesen, Karten nur für geprüfte Schritte.
- **Suchmuster Heidi:** Entitäts-IDs, `shouldUpdate`, `callService`, `access_token`, `latitude`.
- **Testergebnis beim Vollaudit:** Heidi `npm test`, vom User erfragen statt selbst zu bauen.
