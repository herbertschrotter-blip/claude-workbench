# {{name}}

Eigene Home-Assistant-Integration `{{package}}` (Ordner `custom_components/{{package}}/`). Fachlogik ohne Home
Assistant liegt in `custom_components/{{package}}/logik/` und hat eigene Tests. Grundentscheidungen:
`docs/entscheidungen.md`.

## Regeln

- **Tickets:** Fehler, Wünsche und Anregungen werden Tickets (Ticket-Profil unten); hat das Projekt eine eigene Seite,
  bekommt sie den Melden-Knopf nach dem Muster von `ha-netzwerk` (`frontend/src/ansichten/melden.js`).

## Skill-Profil

- Profil-Version: 1
- Projekt-ID: {{slug}}
- Repo: none
- Branch-Policy: current

### Checks
- format: .venv/bin/python -m ruff format --check . [**/*.py; pyproject.toml]
- lint: .venv/bin/python -m ruff check . [**/*.py; pyproject.toml]
- typen: .venv/bin/python -m mypy [custom_components/{{package}}/logik/**; ausliefern.py; pyproject.toml]
- logik: .venv/bin/python -m pytest -q -p no:cacheprovider tests/logik [custom_components/**; tests/logik/**; ausliefern.py]
- integration: .venv/bin/python -m pytest -q -p no:cacheprovider -n auto tests/integration [custom_components/**; tests/integration/**; requirements-ha.txt; tools/**]

### Commit
- Format: [vX.Y.Z] <Modul>, <Typ>: <Kurztitel>
- Module: Integration=custom_components/**; Tests=tests/**; Werkzeuge=tools/**; Doku=docs/**, README.md, CHANGELOG.md, CLAUDE.md
- Versionsquelle: custom_components/{{package}}/manifest.json#version
- Versionsregel: none
- Push-Policy: allowed
- Pre-Commit-Checks: format; lint; typen; logik; integration
- Doku-Check: Funktion geändert → CHANGELOG.md; Entscheidung geändert → docs/entscheidungen.md

### Code
- Stacks: python
- Pflichtkontext: CLAUDE.md; docs/entscheidungen.md
- Aufgabenquelle: none
- Architekturregeln: none
- Tests: format; lint; typen; logik; integration
- Auslieferung: python ausliefern.py – nur durch den Nutzer oder nach seiner Bestätigung (schreibt in custom_components/ der HA-Konfiguration); danach Konfiguration prüfen, Neustart durch den Nutzer. Rückweg: python ausliefern.py --zurueck
- Mockup-Policy: none
- Befund-Ort: none

### Doku
- Router: none
- Standard: none
- Pflichtdokumente: README.md; CHANGELOG.md; docs/entscheidungen.md
- Validierungsregeln: none
- Sitzungsabschluss: none
- Entscheidungs-Ort: docs/entscheidungen.md

### Ticket
- Config: ref:CLAUDE.md#Ticket-Profil

## Ticket-Profil

Tickets = Meldungen an die Integration (Melden-Knopf der Seite, sonst über die Aktion `{{package}}.ticket` bzw. von
Claude). Die Integration sammelt sie und legt sie lesbar ab (`<config>/{{package}}/meldungen.json`, `meldungen.md`,
Bilder unter `<config>/{{package}}/meldungen/`). Abgearbeitet wird in Claude Code im Projekt (eigenes Fenster:
`sh tools/tickets-fenster.sh`): „Tickets prüfen“, Claude holt die offenen Tickets und bearbeitet sie einzeln nach dem
Skill `ticket`. **Bei Erfolg** (behoben, Tests grün, eingespielt) setzt Claude das Ticket auf `geschlossen` – mit
Version, Commit und kurzer Notiz.

- Präfix: `FE-NNNN` Fehler, `WU-NNNN` Wunsch, `AN-NNNN` Anregung (je Art ab 0001 aufsteigend)
- Befehle: `python3 tools/ticket.py liste [alle]` · `zeige <nr>` · `status <nr> <status> [--version X --commit Y --notiz T]` ·
  `notiz <nr> "<text>"` · `verwerfen <nr> "<grund>"` (liest `<config>/{{package}}/meldungen.json`, ändert nur über die
  Aktion `{{package}}.ticket`)
- Status: `neu → angenommen → in_arbeit → geloest → geschlossen`, daneben `verworfen`
- Pflichtangaben: geschlossen → Version + Commit + Notiz (was behoben wurde) · verworfen → Grund
- Aufgaben: kein Tracker – Befund und Plan als Notiz am Ticket
- Beweise nachlesen: `zeige <nr>` (Fenster, Stand der Seite, Screenshots als `bild:`-Zeilen – mit Read ansehen),
  Logbuch und Diagnose der Integration
- Regeln: `docs/entscheidungen.md`
- Doku: CHANGELOG.md-Eintrag nennt die Ticketnummer
