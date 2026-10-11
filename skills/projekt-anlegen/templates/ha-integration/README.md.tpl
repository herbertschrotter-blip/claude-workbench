# {{name}}

Eigene Home-Assistant-Integration. Angelegt als lauffähiges Grundgerüst: Einrichtung über die Oberfläche, ein
technischer Status-Sensor, Diagnose-Download, Übersetzungen (de, en). Die Fachlogik kommt danach.

## Entwickeln

Die Tests gegen Home Assistant brauchen Python 3.14 und laufen unter Linux (unter Windows in WSL).

```sh
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python -r requirements-logik.txt
uv pip install --python .venv/bin/python -r requirements-ha.txt
.venv/bin/python -m ruff format --check .
.venv/bin/python -m ruff check .
.venv/bin/python -m pytest -q tests/logik
.venv/bin/python -m pytest -q -n auto tests/integration
```

Läuft das auf Home Assistant OS, gehört zu beiden `uv pip install` noch `--index-strategy unsafe-best-match` (dort
ist ein zusätzlicher Paketindex eingetragen). Die Fachlogik-Tests unter `tests/logik` brauchen kein Home Assistant.

## In Home Assistant laden

```sh
python ausliefern.py             # nach custom_components/{{package}} der HA-Konfiguration
python ausliefern.py --zurueck   # vorige Fassung wiederherstellen
```

Das Skript kopiert `custom_components/{{package}}` in die Home-Assistant-Konfiguration: ohne `--ziel` in den Ordner
zwei Ebenen über dem Projekt, wenn dort eine `configuration.yaml` liegt. Die vorige Fassung sichert es vorher unter
`.auslieferung/vorher/` (nicht im Repo). Danach Konfiguration prüfen und Home Assistant neu starten. Beim ersten Mal
unter Einstellungen → Geräte & Dienste → Integration hinzufügen → „{{name}}“.

Grundentscheidungen: [docs/entscheidungen.md](docs/entscheidungen.md).
