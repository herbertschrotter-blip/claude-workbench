# `module.yaml` Schema v1

Die maschinenlesbare Kurzfassung eines Moduls für Claude: Vertrag und Eigentumsregister. Pflicht ab Stufe 2 (G-19),
freiwillig in Stufe 0–1. Für Herbert lesbar ist der Steckbrief ([`steckbrief-vorlage.md`](./steckbrief-vorlage.md));
`module.yaml` und Steckbrief beschreiben dasselbe Modul und werden zusammen geändert (G-20). Die Pflichtfelder gelten
für Manifeste ab Stufe 2; ein freiwilliges Manifest in Stufe 0–1 folgt derselben Struktur, ohne Pflichtfelder und ohne
Schema-Prüfung.

## Inhalt

- Grundregel
- Felder
- Bestandteile und Stufe
- Pflichtfelder
- Ausfallverhalten
- Beispiel Roboter-Modul
- Beispiel Haus-Modul
- Beispiel Lüftung (Höchstalter)

## Grundregel

Unter `owns` steht nur, was dem Modul selbst gehört (`module.id`). Fremde Daten stehen ausschließlich unter `sources`
oder `depends_on`. Daran prüft der Drift-Test: Jeder Eintrag unter `owns` gehört `module.id`.

Ein Eigentümerfeld gibt es nicht: Jeder Eintrag unter `owns` behauptet `owner = module.id`. Belegt wird das im Code –
wer Änderungen prüft, wer den maßgeblichen Speicher schreibt, wer Entität bzw. Aktion registriert. Eine fremde Entität
wird durch Lesen oder Anzeigen nicht zu Eigentum.

## Felder

| Feld | Inhalt |
|---|---|
| `schema` | immer `1` |
| `module.id` | Name des Moduls bzw. der Integration (nach ihrer Aufgabe, nicht nach dem Gerät) |
| `module.level` | Ausbaustufe 0–5: die höchste Stufe der vorhandenen Bestandteile |
| `module.type` | primärer Bestandteil: `integration`, `card`, `panel` oder `adapter` |
| `components[]` | alle vorhandenen Bestandteile (enthält `module.type`), siehe „Bestandteile und Stufe“ |
| `depends_on.integrations` | Integrationen, die vorhanden sein müssen |
| `sources[]` | Eingänge: `key`, `owner` (wem der Wert gehört), `interface` (`entities`, `entity`), optional `domain`, `outage` |
| `owns.settings[]` | eigene Einstellungen: `key`, `storage` (`store`, `options`), `exposure` (`config_entity`, `websocket`), optional `domain`, `action` |
| `owns.data[]` | eigene Fachdaten: `key`, `storage` (`sqlite`) |
| `owns.entities[]` | eigene Ergebnis-Entitäten: `key`, `domain` |
| `owns.actions[]` | eigene Aktionen |
| `interfaces.websocket[]` | WebSocket-Bereiche der eigenen Oberfläche |
| `adapters[]` | Herstelleradapter: `id`, `reason` (welche Fähigkeit HA nicht vereinheitlicht) |
| `database` | `schema_versioned`, `backup_hooks` (G-14) |
| `quality` | `unload_reload` (G-15), `diagnostics`, `repairs` (G-17), optional `shadow_mode`, `replay_tests` |
| `ui.types[]` | Arten der eigenen Oberfläche, z. B. `custom_card`, `custom_panel` |
| `failure_policy` | Verhalten von Aufträgen bei Ausfall (G-21), siehe unten |

Welche Einstellung wohin gehört, regelt die Einstellungsmatrix ([`einstellungen.md`](./einstellungen.md)).

## Bestandteile und Stufe

Ein Modul ist eine Einheit, auch wenn es aus mehreren Bestandteilen besteht. `components` nennt alle, `module.type` den
primären:

| Bestandteil | Mindeststufe | verlangt |
|---|---|---|
| `integration` | 2 | – |
| `card` | 3 | `ui.types` mit `custom_card` |
| `panel` | 4 | `ui.types` mit `custom_panel` |
| `adapter` | 5 | `adapters[]` mit konkretem `reason` |

- `components` ist nicht leer, ohne Doppelte und enthält `module.type`.
- `module.level` ist die höchste Mindeststufe der Bestandteile.
- Die Bestandteile werden mit dem Code abgeglichen: Ein vorhandener Bestandteil, der hier fehlt, ist ein Befund (G-19).

## Pflichtfelder

Ab Stufe 2. Bedingte Felder werden gegen den Code geprüft – ein fehlendes `owns.data` hebt die Pflicht für `database`
nicht auf, wenn das Modul eine Datenbank hat.

| Feld | Pflicht | Bedingung / Inhalt |
|---|---|---|
| `schema` | immer | `1` |
| `module.id` | immer | nicht leer, nach der Aufgabe benannt |
| `module.level` | immer | 2–5, höchste Stufe der Bestandteile |
| `module.type` | immer | `integration`, `card`, `panel` oder `adapter` |
| `components` | immer | siehe „Bestandteile und Stufe“ |
| `owns` | immer | Objekt; `{}`, wenn nichts Eigenes existiert |
| `owns.settings` | bedingt | eigene Einstellungen; je Eintrag `key`, `storage`; `exposure`, wenn veröffentlicht |
| `owns.data` | bedingt | eigene dauerhafte Fachdaten; je Eintrag `key`, `storage` |
| `owns.entities` | bedingt | eigene Ergebnis-Entitäten; je Eintrag `key`, `domain` |
| `owns.actions` | bedingt | eigene Aktionen; eindeutige Namen |
| `depends_on.integrations` | bedingt | Integrationen, die vorhanden sein müssen |
| `sources` | bedingt | fremde Eingänge; je Quelle `key`, `owner`, `interface`; `domain`, wenn zur Auswahl nötig |
| `sources[].outage` | bedingt | wenn ein eigenes Ergebnis, eine Aktion oder eine Einstellung von der Quelle abhängt |
| `database` | bedingt | eigene Datenbank; `schema_versioned`, `backup_hooks` (`false` ist ein Befund zu G-14, kein Formfehler) |
| `adapters` | bedingt | Bestandteil `adapter`; je Eintrag `id` und konkreter `reason` |
| `ui.types` | bedingt | Bestandteil `card` oder `panel` |
| `interfaces.websocket` | bedingt | eigene WebSocket-Schnittstellen |
| `failure_policy.scheduled` | bedingt | zeitabhängige Aufträge; `strategy`, `on_recovery` |
| `failure_policy.manual` | bedingt | eigene manuelle Aktionen; `strategy: fail` |
| `quality.unload_reload` | bedingt | eigene Integration mit Einrichtung (Config Entry) |
| `quality.diagnostics`, `quality.repairs` | bedingt | wenn die Anforderung anwendbar ist; Anwendbarkeit im Steckbrief begründet |

## Ausfallverhalten

Je Quelle, klein gehalten (G-21):

| Feld unter `sources[].outage` | Werte |
|---|---|
| `critical_for` | was ohne diese Quelle nicht gültig ist, als Verweis: `entities:<key>`, `actions:<name>`, `settings:<key>` |
| `on_unavailable` | `block` (Aktion sperren, Grund zeigen), `fallback` (benannte Ersatzregel, im Steckbrief beschrieben), `ignore` (für diese Ergebnisse nicht kritisch) |
| `recovery` | `re_evaluate` (nach der Rückkehr mit aktuellen Daten neu bewerten) |
| `max_age` | optional, ISO-Dauer (z. B. `PT30M`) – nur wenn eine Quelle technisch noch einen Wert hat, der fachlich zu alt sein kann |

Je Modul:

| Feld unter `failure_policy` | Werte |
|---|---|
| `scheduled.strategy` | `drop`, `defer`, `retry`, `fail` (geplante Aufträge) |
| `scheduled.on_recovery` | `re_evaluate` |
| `manual.strategy` | `fail` (manuelle Aktion schlägt mit verständlichem Fehler fehl) |

Ein Feld für den Reparatur-Hinweis gibt es nicht: Er kommt immer und nur bei Problemen, die der Benutzer lösen kann
(G-21, Unterregel 3).

Verweise in `critical_for` lösen nur im selben Manifest auf und müssen existieren:

| Verweis | Ziel |
|---|---|
| `entities:<key>` | `owns.entities[].key` |
| `actions:<name>` | Eintrag in `owns.actions[]` |
| `settings:<key>` | `owns.settings[].key` – nur, wenn Gültigkeit oder Änderung der Einstellung von der Quelle abhängt |

Bei `fallback` steht die Ersatzregel im Steckbrief (Abschnitt Quellen); `ignore` darf keine tatsächlich nötige
Abhängigkeit verdecken.

## Beispiel Roboter-Modul

`planer` ist ein Arbeitsname; der Name der Integration wird beim Neubau festgelegt. Nichts hier gehört `haus`.

```yaml
schema: 1

module:
  id: planer            # Platzhalter
  level: 5              # mit Herstelleradapter (Dreame)
  type: integration

components:
  - integration
  - card
  - adapter

depends_on:
  integrations:
    - dreame_vacuum
    - haus

sources:
  - key: robot
    owner: dreame_vacuum
    interface: entities
    outage:
      critical_for:
        - entities:decision
        - actions:run_plan
      on_unavailable: block
      recovery: re_evaluate

  - key: house
    owner: haus
    interface: entities
    outage:
      critical_for:
        - entities:automation_allowed
      on_unavailable: block
      recovery: re_evaluate

owns:
  settings:
    - key: automation_enabled
      storage: store
      exposure: config_entity
      domain: switch

    - key: minimum_battery
      storage: store
      exposure: config_entity
      domain: number

    - key: presence_people
      storage: store
      exposure: websocket
      action: set_presence_people

  data:
    - key: plans
      storage: sqlite
    - key: runs
      storage: sqlite
    - key: robot_learning
      storage: sqlite

  entities:
    - key: decision
      domain: sensor
    - key: automation_allowed
      domain: binary_sensor
    - key: next_run
      domain: sensor

  actions:
    - create_plan
    - update_plan
    - delete_plan
    - run_plan
    - set_presence_people
    - reset_learning

interfaces:
  websocket:
    - settings
    - plans
    - room_mapping

adapters:
  - id: dreame
    reason: "Raumreinigung mit Werten je Raum gibt es in HA nicht einheitlich (vacuum.clean_area reicht nicht)"

database:
  schema_versioned: true
  backup_hooks: true

quality:
  unload_reload: true
  diagnostics: true
  repairs: true
  shadow_mode: true
  replay_tests: true

ui:
  types:
    - custom_card

failure_policy:
  scheduled:
    strategy: defer
    on_recovery: re_evaluate
  manual:
    strategy: fail
```

## Beispiel Haus-Modul

```yaml
schema: 1

module:
  id: haus
  level: 2
  type: integration

components:
  - integration

sources:
  - key: persons
    owner: home_assistant
    interface: entities
    domain: person
    outage:
      critical_for:
        - entities:someone_home
        - entities:expected_return
        - entities:presence_forecast
      on_unavailable: block
      recovery: re_evaluate

owns:
  settings:
    - key: household_people
      storage: store
      exposure: websocket
    - key: work_schedule
      storage: store
      exposure: websocket
    - key: forecast_interval
      storage: options
    - key: forecast_resolution
      storage: options
    - key: forecast_learning_weeks
      storage: options
    - key: forecast_half_life
      storage: options
    - key: forecast_minimum_days
      storage: options

  data:
    - key: presence_learning
      storage: sqlite

  entities:
    - key: someone_home
      domain: binary_sensor
    - key: work_time
      domain: binary_sensor
    - key: quiet_time
      domain: binary_sensor
    - key: expected_return
      domain: sensor
    - key: presence_forecast
      domain: sensor

database:
  schema_versioned: true
  backup_hooks: true

quality:
  unload_reload: true
  diagnostics: true
  repairs: true
```

## Beispiel Lüftung (Höchstalter)

Ausschnitt: Eine Wetterquelle kann noch einen alten Wert liefern, der fachlich nicht mehr gilt – dafür `max_age`.

```yaml
sources:
  - key: weather
    owner: weather
    interface: entity
    outage:
      critical_for:
        - entities:ventilation_decision
      max_age: PT30M
      on_unavailable: block
      recovery: re_evaluate
```
