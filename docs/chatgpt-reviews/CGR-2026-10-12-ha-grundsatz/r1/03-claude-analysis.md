# Runde 1 – Einschätzung Claude

## Zustimmung

- **Mehrere Nachweise je Regel** statt exklusiver Prüfart: Fundstelle, Test und nachgewiesenes Verhalten sind
  verschiedene Nachweise; der Report zeigt je Regel, welche vorliegen. Überzeugt.
- **„Test vorhanden“ färbt nicht grün.** Ein Testergebnis zählt nur, wenn es zum geprüften Stand gehört.
- **Zwei Schritte bei Suchprüfungen** (Kandidat → Kontext), mit den konkreten Schärfungen zu G-06, G-11, G-13, G-17,
  G-18 (Geheimnisse nie wiedergeben), G-21. Dazu die neue G-09-Prüfung `RestoreEntity` und `null`/`[]`.
- **Ausbaustufe:** belegte Mindeststufe aus dem Aufbau, Vertrag hat Vorrang; fehlt der Vertrag bei eigener
  Integration → G-19-Befund, Einzelprüfungen laufen weiter. Die Reference beschreibt Nachweisverfahren und erfindet
  keine neuen Pflichten.
- **Budget:** Teilaudit bleibt bei 10 Aufrufen; bei Erschöpfung „Teilprüfung – folgende Nachweise offen“.
- **`/config` als begrenztes Konfigurationsaudit** mit eingegrenztem Umfang, ohne Steckbriefpflicht.

## Antworten auf die Rückfragen (mein Vorschlag)

1. **`module.level`** = höchste im Modul eingesetzte Stufe (Integration mit Karte und Adapter → 5). Das gehört als
   Satz in `module-yaml.md`.
2. **Pflichtfelder des Manifests** sind bisher nicht festgelegt – berechtigter Befund. Vorschlag: Pflicht immer
   `schema`, `module.id`, `module.level`, `module.type`, `owns`; Pflicht bedingt: `sources[].outage` für jede Quelle,
   von der ein eigenes Ergebnis oder eine Aktion abhängt (ab Stufe 2); `database` wenn `owns.data` eine Datenbank
   nennt; `adapters` ab Stufe 5; `ui` ab Stufe 3; `failure_policy` wenn das Modul zeitabhängige Aufträge hat. Das
   Haus-Beispiel bekommt `outage` für `persons`.
3. **Testergebnis zum geprüften Stand:** Das Prüfskript von git-commit-helper (`scripts/checks.py`) merkt sich grüne
   Läufe je Stand der passenden Dateien. audit kann diesen Speicher lesen (read-only): grün für den aktuellen Stand →
   Nachweis „ausgeführt“; sonst „Ausführung offen“ mit dem Befehl aus dem Profil. audit führt selbst keine Tests aus.

## Offen für Herbert

- Ob Runde 2 den Ergebnisvertrag und die Manifest-Pflichtfelder konkret ausarbeiten soll, oder ob wir mit diesem Stand
  den Plan für audit und die Doku-Ergänzungen schreiben.
