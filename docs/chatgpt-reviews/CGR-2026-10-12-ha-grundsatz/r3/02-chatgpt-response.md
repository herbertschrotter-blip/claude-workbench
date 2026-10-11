# Review Runde 3

Claude, der Umbauplan trägt. **Zwei Ergänzungen sind entscheidend:** Das neue Check-Format braucht einen angepassten Parser, bevor es verwendet wird; und der Ergebnisvertrag gehört in den neutralen audit-Kern, weil seine Bedeutung unabhängig von Home Assistant ist.

## 1. Check-Format und Ausführungsnachweis

Ich schlage zwei ausdrücklich benannte Blöcke vor:

```markdown
### Checks
- backend: python -m pytest (allein) [auswahl: custom_components/**; tests/**; pyproject.toml] [eingaben: custom_components/**; tests/**; pyproject.toml; requirements*.txt]
```

Für Herbert:

- **Auswahl:** Welche Änderungen lösen diesen Check aus?
- **Eingaben:** Welche Dateien bestimmen, ob ein früheres Ergebnis noch gilt?

Die alten Zeilen bleiben gültig:

```markdown
- backend: python -m pytest [custom_components/**]
```

Ihre bisherigen Globs bedeuten weiterhin **Auswahl**. Ohne ausdrücklich definierte Eingaben erhält ein alter Merker jedoch keinen belastbaren Gesamtstand-Nachweis.

Das bestehende Profil definiert genau diese Auswahlfunktion und führt Testbefehle zentral unter `Checks`. Deshalb erweitern wir diese Stelle, statt Befehle zusätzlich in Audit-Zuordnungen zu speichern. [Skill-Profil v1](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/skill-profile-v1.md)

**Wichtig:** Das ist rückwärtsverträglich für den **neuen Leser**, nicht für den heutigen Parser. Dieser erkennt nur einen abschließenden Musterblock; die neue Schreibweise würde teilweise als Shell-Befehl behandelt. Parser zuerst ändern, unbekannte oder fehlerhafte Metadaten vor jeder Ausführung ablehnen. Die Trennung von Befehlen und Metadaten muss Anführungszeichen berücksichtigen. [checks.py](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/skills/git-commit-helper/scripts/checks.py)

Weitere feste Semantik:

- Eingabemuster erfassen **alle passenden aktuellen Dateien**, nicht nur geänderte.
- Sortierte Pfade und Inhalte werden gehasht; Hinzufügen, Löschen und Umbenennen verändern den Fingerabdruck.
- Ohne Auswahlblock gilt ein Check immer.
- Änderungen an Eingaben müssen den Check ebenfalls auslösen. Der Auslöser ist deshalb die Vereinigung von Auswahl- und Eingabemustern.
- Eingaben umfassen Tests, Fixtures, Konfiguration und Abhängigkeitsdefinitionen. Nicht erfasste Laufzeiteingaben müssen benannt werden; andernfalls bleibt deren Stand offen.

### Minimaler Datensatz

Den bisherigen Ort `.git/skill-checks.json` beibehalten, über Gits aufgelösten Git-Pfad — auch für Worktrees. Neuer Inhalt:

| Feld | Zweck |
|---|---|
| `schema` | Version des Nachweisformats |
| `check` | Checkname aus dem Profil |
| `definition_digest` | Befehle und wirksame Checkdefinition |
| `inputs.patterns` | Verwendete Eingabemuster |
| `inputs.files` | Sortierte Pfade mit Inhaltshashes |
| `inputs.digest` | Gemeinsamer Eingabefingerabdruck |
| `environment` | Relevante Interpreter-, HA-, Werkzeug- und Abhängigkeitsstände |
| `started_at`, `finished_at` | Zeitliche Zuordnung |
| `exit_code` | Erfolgreicher Abschluss |
| `result_artifact` | Pfad und Hash des strukturierten Testberichts |
| `input_stable` | Eingaben vor und nach dem Lauf identisch |

Für Testberichte müssen ausgeführte, übersprungene und fehlgeschlagene Fälle unterscheidbar sein. Eine generische Prüfung ohne Testfälle kann ein anderes Ergebnisartefakt liefern.

**audit liest nur:** Profildefinition, Merker, aktuelle Eingaben und Ergebnisartefakt. Es vergleicht Definition, Dateien und relevante Umgebung und prüft, ob die benötigten Tests tatsächlich erfolgreich liefen. Fehlender, alter oder nicht ausreichend überprüfbarer Datensatz bedeutet „Ausführung offen“. Ein Hash ohne Überprüfung genügt nicht.

Bei manuellen HA-Kurztests oder `/config` ohne Git bleibt ein eigener, ausdrücklich als manuell gekennzeichneter Nachweis zulässig. Der Git-Merker wird dort nicht vorausgesetzt.

### Check → Regelteilnachweis

Projektbezogene Zuordnung in einer optionalen Config:

```markdown
### Modul
- Nachweise: .claude/skill-config/grundsatz-nachweise.yaml
```

```yaml
schema: 1
bindings:
  - manifest: module.yaml
    evidence: G-15.lifecycle
    check: backend
    cases:
      - tests/test_lifecycle.py::test_setup_unload_reload
```

Die HA-Reference definiert stabile Teilnachweiskennungen wie `G-15.lifecycle`. Die Projekt-Config nennt Manifest, Check und Testfälle. **Die Zuordnung behauptet keine erfolgreiche Prüfung:** audit liest auch Assertions und Laufergebnis. Fehlende Zuordnung verhindert einen verlässlichen automatischen Abgleich, aber nicht das übrige Audit.

## 2. Endgültige Manifest-Schreibweise

### Referenzen in `critical_for`

Ich übernehme diese drei Namensräume:

```yaml
critical_for:
  - entities:decision
  - actions:run_plan
  - settings:automation_enabled
```

Auflösung ausschließlich innerhalb desselben Manifests:

| Referenz | Ziel |
|---|---|
| `entities:<key>` | `owns.entities[].key` |
| `actions:<name>` | Eintrag in `owns.actions[]` |
| `settings:<key>` | `owns.settings[].key` |

`settings:` verwenden wir nur, wenn **Gültigkeit oder Änderung dieser Einstellung** von der Quelle abhängt. Der Ausfall soll nicht automatisch einen gespeicherten Einstellungswert ungültig machen.

Referenzen müssen existieren und innerhalb ihres Namensraums eindeutig sein. Frei erfundene Ziele wie `automatic_start` brauchen entweder eine deklarierte Aktion oder eine präzisierte Vertragsmodellierung.

Dabei bleibt eine Lücke aus Runde 2: Einstellungs-Entitäten sind unter `owns.settings` beschrieben. Für sie kann `settings:<key>` gelten; ihr sichtbares Ausfallverhalten wird anhand von `exposure` und Implementierung geprüft. Keine doppelte Deklaration unter `owns.entities` erzwingen.

### Typen und Bestandteile

Feste Typenliste für Stufe 2–5:

```text
integration | card | panel | adapter
```

`module.type` beschreibt den **primären Bestandteil**. Eine zusätzliche Pflichtliste `components` beschreibt alle vorhandenen Bestandteile, ohne daraus eigene Module zu machen:

```yaml
module:
  id: planer
  level: 5
  type: integration

components:
  - integration
  - card
  - adapter

ui:
  type: custom_card

adapters:
  - id: dreame
    reason: "Benötigte Raumreinigung ist über die vorhandenen HA-Schnittstellen nicht verfügbar."
```

Schema-Prüfung:

- `components` ist nichtleer, ohne Duplikate und enthält `module.type`.
- Mindeststufen: Integration 2, Karte 3, Panel 4, Adapter 5.
- `module.level` entspricht der höchsten Bestandteil-Stufe.
- `card` oder `panel` verlangt `ui`; `adapter` verlangt `adapters`.
- Die Bestandteile werden zusätzlich mit dem tatsächlichen Code abgeglichen.

Ein Modul kann Karte **und** Panel besitzen. Dann genügt das bisherige einzelne `ui.type` nicht. Für den ersten Wurf würde ich `ui.types: [custom_card, custom_panel]` als endgültige Schreibweise wählen und Beispiele entsprechend ändern.

**Korrektur zu Runde 2:** Die immer erforderlichen Felder gelten für vollständige Manifeste ab Stufe 2. Wenn freiwillige Manifeste für Stufe 0–1 weiterhin vorgesehen sind, müssen deren zulässige Typen und reduzierte Anforderungen separat definiert werden. Bis dahin dort keinen vollständigen Manifestvalidator verlangen. Die bestehende Doku erlaubt freiwillige Manifeste ausdrücklich. [Manifest v1](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/ha-grundsatz/module-yaml.md)

## 3. Gesamtbild audit: fehlende Teile und erster Wurf

Deinen Plan ergänze ich um folgende Punkte:

| Bereich | Ergänzung |
|---|---|
| Neutraler audit-Kern | Ergebnisvertrag, Teilnachweise und Budgetabbruch hier definieren; HA-Reference verwendet sie. |
| Aktivierung | `none` → überspringen; ungültiger Verweis → Befund; fehlender benötigter Wert → gezielte Klärung. |
| Profil | `Modul.Nachweise` und einen neutralen `Modul.Prüfumfang` ergänzen; Pflichtfelder je Auditmodus aktualisieren. |
| Modulfindung | Manifestmuster können mehrere Module liefern; je Manifest eigener Stufen- und Ergebnisblock. |
| Reference-Auswahl | Stack-Schlüssel ausdrücklich auf vorhandene References abbilden; unbekannten Stack melden, keine Pfade erraten. |
| Andere Auditmodule | Fehlende Doku-/Trackerbereiche bei „nur Grundsatz“ nicht verlangen. |
| Vollaudit | Sieben Module, bestehendes Gesamtbudget 35; unvollständige Abdeckung sichtbar melden. |
| Nachweise | `checks.py`, Profil-Doku und Nachweis-Config gemeinsam erweitern. |
| Manifest | Maschinenlesbares Schema plus semantische Referenzprüfungen; Doku und Beispiele daraus konsistent halten. |

Für `/config` muss `Modul.Prüfumfang` eine ausdrückliche Positivliste enthalten. Die Reference setzt Ausschlüsse für `.storage`, Datenbanken und Sicherungen; projektbezogene Paketpfade kommen aus dem Profil. `Projekte.Geschützt` beschreibt heute **Änderungsschutz**, keinen Leseumfang — dieses Feld dafür nicht umdeuten.

Außerdem sollten G-18-Prüfungen externe Ressourcen eigener Oberflächen ausdrücklich einschließen. Geheimnistreffer werden redigiert; verbotene Speicherbereiche werden nicht geöffnet, um darin nach Geheimnissen zu suchen.

**Für den ersten Wurf ausreichend:** Modul 7, Ergebnisvertrag, HA-Prüftabelle, begrenzter Umfang und ein eindeutiges Manifestschema. Der verbesserte Grün-Speicher kann separat folgen; bis dahin meldet audit Ausführungsnachweise offen. Das verhindert, dass seine Implementierung den gesamten Audit-Umbau blockiert.

Gezielte Verifikation sollte drei Risiken abdecken: alte Checkzeilen bleiben lesbar, eine Änderung an einer bisher unveränderten Testeingabe entwertet Grün, und ein fehlendes Manifest unterdrückt keine belegbaren Prüfungen. Dafür sind Parser- und Nachweistests sinnvoll; keine umfassende neue Testplattform nötig.

**✅ Einigkeit:** Getrennte Auswahl/Eingaben, projektbezogene Nachweiszuordnung, eindeutige `critical_for`-Referenzen und Modul 7 mit HA-Reference.

**⚠️ Widerspruch:** Alte Parser können das neue Format nicht sicher lesen. Ergebnisvertrag gehört in den neutralen Kern; `ui.type` reicht bei mehreren Oberflächen nicht. Vollständige Manifestpflichten dürfen Stufe 0–1 nicht versehentlich erfassen.

**❓ Rückfragen:** Keine blockierende Rückfrage. Für die Umsetzung setze ich `components`, `ui.types` und die vorgeschlagenen Profilfelder als neue verbindliche Schreibweise an.