# Langzeitarchiv eigener Integrationen (Entwurf, Vorschlag für G-24)

Stand: 13.10.2026, Fassung 2 (nach Review-Runde 1, CGR-2026-10-13-ha-grundsatz) · Status: **Entwurf zur Abnahme durch
Herbert** · Anlass: Ticket WU-0002 in `ha-netzwerk` („Log, wann ich welche Verbindung hatte, mit sämtlichen Daten zum
Auswerten“).

## Inhalt

- Ziel
- Abgrenzung: Verlauf oder fachlicher Vorgang
- Ablage
- Zeilenformat
- Arten-Katalog
- Sitzungen und Messreihen
- Schreiben und Wiederanlauf
- Aufbewahrung, Größe, Sicherung
- Auswerten
- Datenschutz
- Baustein und Integration
- Erste Anwendung: Netzwerk
- Regel G-24
- Entscheidungen Herbert
- Offen

## Ziel

Jede eigene Integration legt ihre fachlichen Vorgänge so ab, dass sie **über Jahre bleiben**, **ohne die Integration
lesbar** sind und später **zusammen mit allen anderen Integrationen ausgewertet** werden können – je Integration ein
eigenes Archiv, alle im selben Format.

## Abgrenzung: Verlauf oder fachlicher Vorgang

| Was | Wohin | Beispiel |
|---|---|---|
| **Normaler Verlauf einer Entität** | Recorder; bei passenden Sensoren (`state_class` mit passender Statistik-Bedeutung) die Langzeitstatistik von HA (Stundenwerte, unbegrenzt) | aktuelle Signalstärke, Geräte online |
| **Fachlicher Vorgang** mit Zusammenhang, Ergebnis und Herkunft | Archiv der Integration | Mobilfunk-Verbindung von–bis mit Technik, Zelle und Grund des Endes; Speedtest-Ergebnis; Störung; Reinigungslauf |

- Der Recorder kann Ereignisse länger halten, und es gibt Exporte (InfluxDB/VictoriaMetrics). Was beiden fehlt, ist ein
  **gemeinsamer fachlicher Vertrag** über alle Integrationen. Den liefert das Archiv. Logbuch ist eine Ansicht, externe
  Statistik-Importe sind nur für Zahlenreihen gedacht, eigene Tabellen in der Recorder-Datenbank sind ausgeschlossen.
- **G-10 bleibt:** Den normalen Verlauf spiegelt das Archiv nicht. Eine Messreihe im Archiv (z. B. Signal je
  Verbindung) braucht einen im Katalog genannten fachlichen Grund.
- **G-01:** Das Archiv ist der maßgebliche historische Nachweis. Die eigene Datenbank einer Integration hält
  Arbeitsdaten für die Oberfläche (mit Frist) und daraus abgeleitete Ansichten.
- Zusätzliche Dienste (VictoriaMetrics, Grafana) kommen erst bei Bedarf und ändern keine Integration.

## Ablage

```
<config>/archiv/<domain>/
  schema/<art>.v<art_v>.json     Katalog jeder Art, wie in module.yaml (bleibt mit dem Archiv erhalten)
  <JJJJ-MM>.jsonl                laufender Monat, eine Zeile je Datensatz
  <JJJJ-MM>.jsonl.gz             abgeschlossene Monate
```

- Die Monatsdatei richtet sich nach der **Schreibzeit** (`erfasst`), nicht nach dem fachlichen Zeitpunkt – damit nie ein
  gepackter Monat wieder geöffnet wird.
- Nicht unter `/local` (G-18), nicht im Repo.

## Zeilenformat

Format-Version `v: 1`. Pflichtfelder fett.

| Feld | Inhalt |
|---|---|
| **`v`** | Format-Version des Archivs |
| **`id`** | stabile Kennung des Datensatzes (UUID oder aus der Quelle abgeleitet); bei Wiederholung gleich |
| **`quelle`** | Domain der Integration |
| `instanz` | Kennung der Einrichtung, wenn eine Domain mehrere hat (ohne Gerätekennung) |
| **`art`**, **`art_v`** | Art aus dem Katalog und ihre Version |
| **`t`** | fachlicher Zeitpunkt bzw. Beginn, UTC mit `Z` |
| `bis` | Ende eines Zeitraums, UTC |
| **`erfasst`** | Schreibzeit, UTC |
| **`stufe`** | `info`, `warnung` oder `kritisch` |
| **`text`** | ein Satz für Menschen, ohne geschützte Daten |
| `werte` | Felder der Art laut Katalog |
| `bezug` | Verweise: `sitzung` (ID der Sitzung), `geraet` (pseudonyme Kennung) |
| `ersetzt` | ID eines früheren Datensatzes, den dieser korrigiert |
| `herkunft` | `live` (Vorgabe) oder `nachgetragen` |

Regeln:
- Zeiten immer UTC; lokale Zeit nur in der Anzeige.
- Ein fehlender Wert fehlt oder ist `null`, **nie `0`**. `NaN` und Unendlich sind verboten.
- Korrekturen sind neue Datensätze mit `ersetzt`. Bestehende Zeilen ändert niemand.
- Die Reihenfolge der Zeilen hat keine Bedeutung. Leser sortieren nach `t` und behandeln gleiche `id` mit gleichem
  Inhalt als einen Datensatz; gleiche `id` mit anderem Inhalt ist ein Fehler.
- Dauern innerhalb eines Laufs aus monotoner Zeit; springt die Uhr, wird das als `werte.uhr_sprung: true` vermerkt.

## Arten-Katalog

Abschnitt `archive:` in `module.yaml`; beim Start schreibt die Integration jede Art als `schema/<art>.v<art_v>.json` ins
Archiv (nur neue Versionen).

```yaml
archive:
  version: 1
  anwendbar: true            # false + grund, wenn eine Integration nichts archiviert
  arten:
    mobil.sitzung:
      art_v: 1
      text: Mobilfunk-Verbindung von Einwahl bis Ende
      sitzung: true
      felder:
        technik:   {typ: text, werte: [LTE, 5G NSA, 5G SA, 3G]}
        zellen:    {typ: ganzzahl, einheit: anzahl, min: 0}
        rsrp_mittel: {typ: zahl, einheit: dBm, min: -150, max: -30}
        ende:      {typ: text, werte: [neueinwahl, abbruch, luecke]}
      datenschutz: [standortbezogen]
```

- Felder sind abschließend; was nicht im Katalog steht, darf nicht in `werte`.
- `owns.data[]` in `module.yaml` bekommt `storage: archiv`; Schema und Validator werden gemeinsam erweitert.
- Eine Art wird nie umgedeutet. Eine geänderte Bedeutung bekommt eine neue `art_v` bzw. eine neue Art.

## Sitzungen und Messreihen

> **Offen für Runde 2** (Herbert: „ChatGPT fragen“): Vorschlag aus Runde 1.

```
mobil.sitzung.start   bezug.sitzung, t = Beginn
mobil.signal          bezug.sitzung, t..bis = höchstens ein UTC-Tag, werte.reihe = 5-Minuten-Werte
mobil.sitzung.ende    bezug.sitzung, t = Beginn, bis = Ende, Zusammenfassung, ende = neueinwahl | abbruch | luecke
```

- Die Messreihe nennt je Punkt den Messzeitpunkt, Anker und 5G getrennt, Aggregation (`5min`, beim Nachtrag `stunde`)
  und Lücken.
- Ein Neustart von HA beendet keine Verbindung. Ist nicht belegbar, dass sie durchlief, wird eine Lücke vermerkt.
- Geräte-Sitzungen (`geraet.sitzung.start/ende`) folgen demselben Muster ohne Messreihe.

## Schreiben und Wiederanlauf

Entscheidung Herbert: **kurzes, dokumentiertes Verlustfenster** statt Pflicht zur vollen Vormerk-Kette.

- Ein Schreiber **je Domain** (auch bei mehreren Einrichtungen), eine Warteschlange mit fester Größe, Schreiben im
  Executor nacheinander. Jeder Schreibvorgang wird sofort auf den Datenträger gebracht (`flush` + `fsync`).
- Verlustfenster: höchstens die Datensätze, die seit dem letzten Schreibvorgang anfielen (Netzwerk: ein Abruf). Es
  steht im Steckbrief der Integration.
- Hat die Integration eine eigene SQLite, darf sie Datensätze dort in derselben Transaktion vormerken (dann kein
  Verlust); Pflicht ist das nicht.
- Beim Start: eine abgebrochene letzte Zeile wird nach `defekt/` gesichert und abgeschnitten, nie übersprungen.
- Monatswechsel: alte Datei als `.gz.tmp` packen, prüfen, umbenennen, erst dann die Quelle löschen.
- Entladen/Neu laden: Warteschlange wird geleert, nie ein zweiter Schreiber.
- Fehler: Die Integration läuft weiter, der Rückstand ist in der Diagnose sichtbar. Ein Reparatur-Hinweis kommt nur bei
  dauerhaften, vom Benutzer lösbaren Ursachen (Datenträger voll, keine Schreibrechte).
- Sicherung: Vor einer HA-Sicherung leert der Schreiber die Warteschlange und pausiert, danach läuft er weiter (wie die
  SQLite in Netzwerk).

## Aufbewahrung, Größe, Sicherung

- Unbegrenzt aufbewahren.
- Größe Netzwerk (geschätzt, im Test gemessen): 105 120 Signalpunkte im Jahr à ca. 30 Byte → ca. 3 MB roh, gepackt ca.
  0,5–1 MB; dazu Geräte-Sitzungen (je nach Gerätezahl einige MB roh).
- `<config>/archiv/` ist Teil der HA-Sicherungen. Wohin die Sicherung geht (z. B. Cloud), bestimmt Herbert – dann
  verlässt auch das Archiv den Pi. Ein Test sichert und stellt wieder her (Archiv, Schlüssel, Sitzungsanfänge).

## Auswerten

- Ein gemeinsamer **Leser** im Baustein: entfernt Duplikate, löst `ersetzt` auf, prüft gegen `schema/`.
- `tools/archiv.py`: CSV je Art für Excel (Messreihen als eigene Tabelle). Freitext wird gegen Formeln abgesichert
  (`=`, `+`, `-`, `@` am Anfang).
- DuckDB als Weg für Auswertungen über alle Integrationen, mit festen Spaltentypen aus `schema/` statt automatischer
  Erkennung.
- Die eigene Seite einer Integration zeigt ihr Archiv über ihren WebSocket (nur für angemeldete Benutzer), ohne
  Fachrechnung in der Seite. Andere Integrationen lesen fremde Archive nie direkt (G-05).

## Datenschutz

- Geräte: `HMAC-SHA256(schlüssel, normalisierte MAC)`, Schlüssel zufällig, im Store der Integration und in der
  Sicherung. Geht er verloren, beginnen neue Kennungen; das ist dokumentiert.
- Pseudonym ist nicht anonym: Online-Zeiten zeigen Anwesenheit. Geräte-Sitzungen sind deshalb im Katalog als
  `personenbezogen` markiert.
- Zellkennungen sind `standortbezogen` (bewusste Entscheidung); der eigene Standort selbst kommt nie ins Archiv.
- Geprüft werden auch `text`, Fehlertexte, Serverangaben und Exporte. Die Diagnose zeigt keine Archivinhalte.

## Baustein und Integration

| Workbench-Baustein `archiv` | Integration |
|---|---|
| Format prüfen, Zeiten normalisieren, Zeilen bauen | welche Vorgänge archiviert werden |
| Schreiber, Warteschlange, Wiederanlauf, Monatswechsel | Sitzungsgrenzen und Zusammenfassung |
| `schema/` schreiben, Leser (Duplikate, Korrekturen) | Arten-Katalog, Einheiten, Datenschutz-Markierung |
| `tools/archiv.py` (CSV), gemeinsame Tests (Absturz, Wiederholung, Monatswechsel, Packen, Korrektur, Sicherung) | stabile IDs der Vorgänge, Fachtest je Art |
| Anbindung an HA (Executor, Sicherung, Diagnose) | Texte für Reparatur-Hinweise, WebSocket für die eigene Seite |

projekt-anlegen setzt Baustein und `archive:` ein, code-erstellen baut die Arten, audit prüft die Nachweise. Ein
eigener Skill ist nicht nötig.

## Erste Anwendung: Netzwerk

| Art | Inhalt |
|---|---|
| `mobil.sitzung.start/ende`, `mobil.signal` | Verbindung, Technik, Zelle, Band, Grund des Endes; Signal 5 min |
| `mobil.wechsel` | Technik- oder Zellenwechsel |
| `internet.stoerung` | Dauer, Ursache, Zusammenfassung |
| `speedtest.messung`, `speedtest.serie` | Ergebnisse, Median und Spanne |
| `befund` | neu bzw. erledigt |
| `geraet.sitzung.start/ende` | pseudonyme Kennung, Art, Verbindung (LAN/WLAN-Band) |

**Nachtrag (einmalig, wiederholbar):** Aus dem Journal (400 Tage) lassen sich rekonstruieren:
- Verbindungen: die Neueinwahl speichert die Dauer der vorigen Verbindung.
- Technik- und Zellwechsel, letztere mit RSRP.
- Störungen, Geräte online/offline, Befunde.

Signal: 5-Minuten-Werte gibt es nur für etwa 10 Tage, davor Stundenwerte aus der Langzeitstatistik
(`aggregation: stunde`). Fehlendes wird als Lücke ausgewiesen. IDs werden aus den Quelldatensätzen abgeleitet,
`herkunft: nachgetragen`.

Danach kommt die Ansicht „Verbindungen“ im Reiter Funk, mit Filter und CSV. Vorher gibt es ein Mockup.

## Regel G-24

> **G-24 Langzeitarchiv:** Jede eigene Integration legt in `module.yaml` fest, welche fachlichen Vorgänge (Ereignisse,
> Sitzungen, Ergebnisse) langfristig erhalten bleiben, und schreibt sie im gemeinsamen, versionierten Archivformat nach
> `<config>/archiv/<domain>/`. Den normalen Verlauf ihrer Entitäten hält der Recorder; Messreihen im Archiv brauchen
> einen genannten fachlichen Grund. Das Archiv ist ohne die Integration lesbar. Neustarts, Schreibfehler und
> Wiederherstellungen verursachen keine unbemerkten Verluste über das dokumentierte Fenster hinaus und keine doppelt
> gezählten Einträge. Archiviert eine Integration nichts, steht der Grund in `module.yaml`.

- **Prüfbar durch:**
  - `archive:` vollständig (oder `anwendbar: false` mit Grund);
  - `schema/` im Archiv passend zum Katalog;
  - Fachtest je Art;
  - die gemeinsamen Baustein-Tests (Absturz, Wiederholung, Monatswechsel, Packen, Korrektur);
  - Entladen/Neu laden;
  - Sicherung und Wiederherstellung;
  - Datenschutzprüfung der Felder und Texte.
- **Ab Stufe:** 2.

## Entscheidungen Herbert

13.10.2026, Runde 1 und davor:

1. Geräte-Sitzungen kommen ins Archiv (pseudonym).
2. Signal je Mobilfunk-Verbindung in 5-Minuten-Werten.
3. Einmaliger Nachtrag aus dem Netzwerk-Journal.
4. Grafana/VictoriaMetrics erst bei Bedarf.
5. Stromausfall: kurzes, dokumentiertes Verlustfenster; die Vormerk-Kette ist keine Pflicht.

## Offen

- Form der Sitzungen (Beginn – Tagesblöcke – Ende oder eine Zeile am Ende), siehe „Sitzungen und Messreihen“.
