# `module.yaml` Schema v1

Die maschinenlesbare Kurzfassung eines Moduls für Claude: Vertrag und Eigentumsregister. Pflicht ab Stufe 2 (G-19),
freiwillig in Stufe 0–1. Für Herbert lesbar ist der Steckbrief ([`steckbrief-vorlage.md`](./steckbrief-vorlage.md));
`module.yaml` und Steckbrief beschreiben dasselbe Modul und werden zusammen geändert (G-20).

## Inhalt

- Grundregel
- Felder
- Ausfallverhalten
- Beispiel Roboter-Modul
- Beispiel Haus-Modul
- Beispiel Lüftung (Höchstalter)

## Grundregel

Unter `owns` steht nur, was dem Modul selbst gehört (`module.id`). Fremde Daten stehen ausschließlich unter `sources`
oder `depends_on`. Daran prüft der Drift-Test: Jeder Eintrag unter `owns` gehört `module.id`.

## Felder

| Feld | Inhalt |
|---|---|
| `schema` | immer `1` |
| `module.id` | Name des Moduls bzw. der Integration (nach ihrer Aufgabe, nicht nach dem Gerät) |
| `module.level` | Ausbaustufe 0–5 |
| `module.type` | z. B. `integration` |
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
| `ui.type` | z. B. `custom_card` |
| `failure_policy` | Verhalten von Aufträgen bei Ausfall (G-21), siehe unten |

Welche Einstellung wohin gehört, regelt die Einstellungsmatrix ([`einstellungen.md`](./einstellungen.md)).

## Ausfallverhalten

Je Quelle, klein gehalten (G-21):

| Feld unter `sources[].outage` | Werte |
|---|---|
| `critical_for` | Ergebnisse und Aktionen, die ohne diese Quelle nicht gültig sind |
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

## Beispiel Roboter-Modul

`planer` ist ein Arbeitsname; der Name der Integration wird beim Neubau festgelegt. Nichts hier gehört `haus`.

```yaml
schema: 1

module:
  id: planer            # Platzhalter
  level: 5              # mit Herstelleradapter (Dreame)
  type: integration

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
        - decision
        - run_plan
      on_unavailable: block
      recovery: re_evaluate

  - key: house
    owner: haus
    interface: entities
    outage:
      critical_for:
        - automatic_start
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
    reason: capabilities_not_standardized

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
  type: custom_card

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

sources:
  - key: persons
    owner: home_assistant
    interface: entities
    domain: person

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
        - ventilation_decision
      max_age: PT30M
      on_unavailable: block
      recovery: re_evaluate
```
