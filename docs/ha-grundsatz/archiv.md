# Langzeitarchiv eigener Integrationen (Entwurf, Vorschlag für G-24)

Stand: 13.10.2026 · Status: **Entwurf zur Abnahme durch Herbert** · Anlass: Ticket WU-0002 in `ha-netzwerk`
(„Log, wann ich welche Verbindung hatte, mit sämtlichen Daten zum Auswerten“).

## Inhalt

- Ziel
- Was HA schon kann und was fehlt
- Grundsatz: zwei Schichten
- Ablage und Format
- Arten-Katalog je Integration
- Schreiben
- Aufbewahrung, Größe, Sicherung
- Auswerten über alle Integrationen
- Datenschutz
- Erste Anwendung: Netzwerk
- Was zum Standard gehört
- Entscheidungen Herbert (13.10.2026)

## Ziel

Jede eigene Integration legt ihre Daten so ab, dass sie **über Jahre bleiben** und später **ohne Umbau zusammen mit allen
anderen Integrationen ausgewertet** werden können – je Integration ein eigenes Archiv, aber alle im selben Format.

## Was HA schon kann und was fehlt

| Weg | Was bleibt | Fehlt |
|---|---|---|
| Recorder (Verlauf) | jede Zustandsänderung, ca. 10 Tage (`purge_keep_days`) | Dauer |
| Langzeitstatistik (Sensoren mit `state_class`) | Stundenmittel/-min/-max, unbegrenzt, ohne Zusatzsoftware | Ereignisse, feinere Auflösung |
| InfluxDB bzw. VictoriaMetrics + Grafana (Add-ons, Community-Weg) | jede Zustandsänderung, unbegrenzt, Dashboards über alles | **Ereignisse und Sitzungen**; zusätzliche Dienste am Pi |

Keiner dieser Wege hält **Ereignisse und Sitzungen** mit ihren Daten fest – „14:02–18:40 LTE, Zelle X, Ø −98 dBm, endete
mit Neueinwahl“, ein Reinigungslauf von Heidi, eine Speedtest-Serie. Das liegt heute in eigenen Datenbanken jeder
Integration, in eigenem Format und mit begrenzter Aufbewahrung (Netzwerk: Journal 400 Tage).

## Grundsatz: zwei Schichten

1. **Zahlen über die Zeit** → Sensoren mit `state_class` (G-07, G-10). Die Langzeitstatistik von HA archiviert sie
   unbegrenzt; wer später feiner auflösen will, ergänzt VictoriaMetrics + Grafana, ohne eine Integration zu ändern. Das
   Archiv **spiegelt diesen Verlauf nicht** (G-10).
2. **Ereignisse, Sitzungen und Ergebnisse** → das **Archiv** der Integration im gemeinsamen Format (unten): Dinge mit
   Anfang, Ende oder Ergebnis, die kein einzelner Zustand sind.

Die eigenen Datenbanken der Integrationen bleiben Arbeitsspeicher für die Oberfläche (schnelle Abfragen, Aufräumen nach
Frist); das Archiv ist die dauerhafte, gemeinsame Ablage.

## Ablage und Format

- Ort: `<config>/archiv/<domain>/<JJJJ-MM>.jsonl` – eine Datei je Monat, eine Zeile je Eintrag (JSON Lines). Nicht unter
  `/local` (G-18), nicht im Repo.
- Abgeschlossene Monate werden zu `<JJJJ-MM>.jsonl.gz` gepackt.
- Jede Zeile hat dieselben Felder (Format-Version 1):

| Feld | Pflicht | Inhalt |
|---|---|---|
| `v` | ja | Format-Version, `1` |
| `t` | ja | Beginn bzw. Zeitpunkt, ISO 8601 mit Zeitzone |
| `bis` | nein | Ende einer Sitzung; fehlt sonst |
| `quelle` | ja | Domain der Integration, z. B. `netzwerk` |
| `art` | ja | Art aus dem Katalog der Integration, `<bereich>.<was>`, z. B. `mobil.sitzung` |
| `stufe` | ja | `info`, `warnung` oder `kritisch` |
| `text` | ja | ein Satz für Menschen |
| `werte` | nein | Zahlen und Texte der Art; Einheit steht im Katalog, nicht im Wert |
| `bezug` | nein | Kennungen, z. B. `{"geraet": "<gesalzene Kennung>"}` – nie MAC-Adresse oder Name |

Beispiel:

```json
{"v":1,"t":"2026-10-13T14:02:11+02:00","bis":"2026-10-13T18:40:05+02:00","quelle":"netzwerk","art":"mobil.sitzung","stufe":"info","text":"LTE-Verbindung 4 h 38 min, endete mit Neueinwahl","werte":{"technik":"LTE","zellen":2,"rsrp_mittel":-98,"rsrp_min":-109,"speedtests":3,"down_median":41.2,"ende":"neueinwahl"}}
```

## Arten-Katalog je Integration

Neuer Abschnitt `archive:` in `module.yaml` beschreibt jede Art mit Bedeutung und Einheiten – die einzige Stelle, die
ein Auswerter lesen muss:

```yaml
archive:
  version: 1
  arten:
    mobil.sitzung:
      text: Eine Mobilfunk-Verbindung von Einwahl bis Abbruch
      sitzung: true
      werte: {technik: text, zellen: anzahl, rsrp_mittel: dBm, rsrp_min: dBm, speedtests: anzahl, down_median: Mbit/s, ende: text}
```

Eine Art wird nie umgedeutet; ändert sich ihr Inhalt grundlegend, gibt es eine neue Art.

## Schreiben

- Nur **anhängen**, nie ändern oder löschen. Eine Sitzung wird geschrieben, wenn sie zu Ende ist (eine Zeile mit `t` und
  `bis`); ihr Anfang wird im Store gemerkt, damit sie einen HA-Neustart übersteht.
- Ein Schreiber je Integration, im Executor, mit Sperre. Ein Schreibfehler stoppt die Integration nicht, sondern wird
  als Reparatur-Hinweis gemeldet (G-17, G-21).
- Die Fachlogik (`logik/`) baut die Zeilen ohne HA-Code und testbar (G-12); geschrieben wird außerhalb.
- Ein gemeinsames kleines Modul kommt als Workbench-Baustein `archiv` in jede Integration (wie `tickets`).

## Aufbewahrung, Größe, Sicherung

- Unbegrenzt aufbewahren. Grobe Größe Netzwerk: einige hundert Zeilen im Monat, gepackt deutlich unter 1 MB im Jahr.
- `<config>/archiv/` ist in den HA-Sicherungen enthalten; die Integration schließt es nicht aus.
- Rückblickend füllen: einmalig aus vorhandenen Daten (z. B. Netzwerk-Journal der letzten 400 Tage), mit
  `werte.nachgetragen: true`.

## Auswerten über alle Integrationen

- **DuckDB** liest alle Archive direkt, auch gepackt:
  `SELECT quelle, art, count(*) FROM read_json_auto('archiv/*/*.jsonl*') GROUP BY ALL` – und lässt sich mit der
  HA-Langzeitstatistik verbinden (z. B. Verbindungsabbrüche gegen Temperatur oder Stromverbrauch).
- Werkzeug `tools/archiv.py` im Baustein: CSV für Excel (Filter Integration, Art, Zeitraum).
- Später möglich, nicht Teil des Standards: Grafana mit VictoriaMetrics (Sensoren) und einem DuckDB- bzw. JSON-Plugin
  (Archive).
- Die eigene Seite einer Integration darf ihr Archiv zeigen (z. B. Verbindungs-Log in Netzwerk) – über den WebSocket der
  Integration, ohne Fachrechnung in der Seite.

## Datenschutz

- Keine MAC-Adressen, Gerätenamen, Kennwörter oder Koordinaten im Archiv. Geräte mit gesalzener Kennung (Muster
  `verlauf.geraete_id` in Netzwerk); das Salz bleibt im Store, damit Kennungen über Jahre gleich bleiben.
- Zellkennungen sind öffentliche Senderdaten und dürfen ins Archiv; der eigene Standort nicht.
- Das Archiv verlässt den Pi nur, wenn Herbert es selbst kopiert.

## Erste Anwendung: Netzwerk (WU-0002)

| Art | Wann | Werte (Auswahl) |
|---|---|---|
| `mobil.sitzung` | Neueinwahl bzw. Ende der Verbindung | Technik, Zellen, Band, RSRP/RSRQ Ø und min (aus der Statistik), Speedtests in der Zeit, Grund des Endes |
| `mobil.wechsel` | Technik- oder Zellenwechsel | von, nach, RSRP |
| `internet.stoerung` | Ende einer Störung | Dauer, Ursache (Lage), Zusammenfassung |
| `speedtest.messung` | jedes Ookla-Ergebnis | down, up, ping, Server, Anteil vom Tarif |
| `speedtest.serie` | Ende einer Serie | Durchläufe, Median, Spanne |
| `befund` | Befund neu bzw. erledigt | Schlüssel, Stufe |
| `geraet.sitzung` | Gerät online → offline | gesalzene Kennung, Art, Verbindung (LAN/WLAN-Band), Dauer |

Danach Ansicht „Verbindungen“ im Reiter Funk aus dem Archiv, mit Filter und CSV-Knopf – vorher Mockup.

## Was zum Standard gehört

1. Regel **G-24 Archiv**: „Ereignisse, Sitzungen und Ergebnisse, die über die Frist der eigenen Datenbank hinaus Wert
   haben, schreibt eine Integration in ihr Archiv `<config>/archiv/<domain>/` im gemeinsamen Format; Zahlen über die
   Zeit bleiben Sensoren mit `state_class`.“ Prüfbar durch `archive:` in `module.yaml` und einen Test je Art; ab Stufe 2.
2. Baustein `archiv` in projekt-anlegen: Schreiber, `logik/archiv.py` (Zeile bauen, Format prüfen), `tools/archiv.py`
   (CSV), Test-Vorlage; Abschnitt `archive:` in `module-yaml.md`; Zeile in der Audit-Tabelle.
3. Nachziehen: Netzwerk zuerst, dann Baustrommanager und Baustelle; Heidi beim Neubau.

## Entscheidungen Herbert (13.10.2026)

1. **Geräte-Sitzungen** (`geraet.sitzung`) kommen ins Archiv – nur mit gesalzener Kennung.
2. **Signal je Mobilfunk-Sitzung** mit 5-Minuten-Werten: die Zeile `mobil.sitzung` trägt in `werte.verlauf` die Reihe
   `[[sekunden_seit_t, rsrp, rsrq], …]` (5 min, aus den eigenen Abrufen der Integration, nicht aus dem Recorder).
3. **Rückblickend füllen** aus dem Netzwerk-Journal (bis 400 Tage) – ja, einmalig, `werte.nachgetragen: true`.
4. **Grafana/VictoriaMetrics** erst bei Bedarf.
5. Vor der Abnahme ein **ChatGPT-Review** des Entwurfs.
