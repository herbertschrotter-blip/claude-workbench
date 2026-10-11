# Runde 3 – Einschätzung Claude

Zustimmung in allen Punkten, keine offene Rückfrage; das Konzept ist umsetzungsreif.

- **Ergebnisvertrag in den neutralen Kern von audit** (gilt für jedes Regelwerk); die HA-Reference enthält Stufen,
  Prüftabelle G-01 … G-22 und den Sonderfall `/config`.
- **Check-Format** `[auswahl: …] [eingaben: …]`, alte Zeilen bleiben gültig (Globs = Auswahl). Der Parser von
  `checks.py` muss zuerst angepasst werden (Tests für alte Zeilen, unbekannte Metadaten ablehnen). Nachweis-Datensatz
  in `.git/skill-checks.json` mit den Feldern aus Runde 3.
- **`module.yaml`:** `components` (Pflicht ab Stufe 2), `module.type` = primärer Bestandteil aus `integration | card |
  panel | adapter`, `ui.types`, `critical_for` mit `entities:` / `actions:` / `settings:`; Pflichtfelder gelten erst ab
  Stufe 2, freiwillige Manifeste in Stufe 0–1 ohne Validator.
- **Profilfelder** `Modul.Nachweise` (Zuordnung Check → Teilnachweis) und `Modul.Prüfumfang` (Positivliste, für
  `/config`); `Projekte.Geschützt` bleibt Änderungsschutz.
- **Reihenfolge:** Doku und audit zuerst; `checks.py` getrennt, bis dahin „Ausführung offen“.

## Umsetzung (Vorschlag)

1. Doku: `docs/ha-grundsatz/module-yaml.md`, `docs/skill-profile-v1.md`
2. audit per skill-pflege: Ergebnisvertrag im Kern, Modul 7, Reference `references/grundsatz/home-assistant.md`
3. `checks.py` (git-commit-helper) als eigene ClickUp-Aufgabe
4. chatgpt-review: Anzeige der Antwort als Zitat, Statuszeile (Wunsch Herbert)
