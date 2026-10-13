# Langzeitarchiv eigener Integrationen (G-24)

Stand: 13.10.2026, Fassung 3 · Status: **festgelegt** (Herbert, 13.10.2026, nach Review CGR-2026-10-13-ha-grundsatz,
Runden 1–2) · Anlass: Ticket WU-0002 in `ha-netzwerk` („Log, wann ich welche Verbindung hatte, mit sämtlichen Daten zum
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

- Die Monatsdatei richtet sich nach der **Schreibzeit** (`erfasst`), nicht nach dem fachlichen Zeitpunkt. Liegt
  `erfasst` in einem schon gepackten Monat (Uhr zurückgestellt), kommt der Datensatz in eine ungepackte Zusatzdatei
  `<JJJJ-MM>.nachtrag-<n>.jsonl`; gepackte Dateien werden nie geändert. Leser lesen alle Teile eines Monats.
- Neben `schema/` liegt `schema/_format.v1.json`, die Beschreibung des Zeilenformats selbst.
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
| **`erfasst`** | Schreibzeit, UTC; beim ersten Schreibversuch festgelegt und bei Wiederholung unverändert |
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
- Dauern innerhalb eines Laufs aus monotoner Zeit. Springt die Uhr (Wanduhr weicht von der monotonen Zeit um mehr als
  60 s ab), trägt der betroffene Datensatz `uhr_sprung: true` – ein reserviertes Feld des Formats, kein Feld der Art.
- Reservierte Felder sind nur die der Tabelle oben und `uhr_sprung`; alles Weitere steht in `werte` laut Katalog.

## Arten-Katalog

Abschnitt `archive:` in `module.yaml`. `(art, art_v)` bezeichnet ein **unveränderliches** Schema innerhalb einer Domain:
- Beim Start schreibt die Integration jede Art atomar als `schema/<art>.v<art_v>.json`, **bevor** der erste Datensatz
  dieser Art geschrieben wird.
- Gibt es die Datei schon, wird verglichen. Eine Abweichung ist ein Vertragsfehler: Es wird nichts überschrieben, die
  Art wird nicht geschrieben, und die Diagnose meldet es.

```yaml
archive:
  version: 1
  anwendbar: true            # false + grund, wenn eine Integration nichts archiviert
  arten:
    mobil.sitzung.ende:
      art_v: 1
      text: Ende einer Mobilfunk-Verbindung mit Zusammenfassung
      sitzung: ende              # start | ende | block | nein
      felder:
        technik:     {typ: text, pflicht: true, werte: [LTE, 5G NSA, 5G SA, 3G]}
        zellen:      {typ: ganzzahl, einheit: anzahl, min: 0}
        rsrp_mittel: {typ: zahl, einheit: dBm, min: -150, max: -30, null: true}
        ende:        {typ: text, pflicht: true, werte: [neueinwahl, abbruch, unbekannt]}
      datenschutz: [standortbezogen]
    mobil.signal:
      art_v: 1
      text: Signalwerte einer Verbindung, höchstens ein UTC-Tag je Block
      sitzung: block
      grund: Erklärt Abbrüche und Geschwindigkeit einer Verbindung (G-10)
      felder:
        reihe:
          typ: liste
          punkt: {t: zeit, rsrp_anker: dBm, rsrq_anker: dB, rsrp_5g: dBm, rsrq_5g: dB}
        aggregation: {typ: text, pflicht: true, werte: [messung, mittel, min, max]}
        intervall_s: {typ: ganzzahl, einheit: s}
        herkunft_werte: {typ: text, werte: [abruf, ha_statistik]}
```

- Felder sind abschließend; was nicht im Katalog steht, darf nicht in `werte`. Je Feld: `typ` (`text`, `zahl`,
  `ganzzahl`, `bool`, `zeit`, `liste`), `pflicht` (Vorgabe nein), `null` (erlaubt ja/nein), Einheit, Grenzen bzw.
  erlaubte Werte; bei `liste` die Struktur eines Punkts.
- `owns.data[]` in `module.yaml` bekommt `storage: archiv`; Schema und Validator werden gemeinsam erweitert.
- Eine Art wird nie umgedeutet. Eine geänderte Bedeutung bekommt eine neue `art_v` bzw. eine neue Art.

## Sitzungen und Messreihen

Entscheidung Herbert: **Variante A** – Beginn, laufende Messblöcke, Ende.

```
mobil.sitzung.start   bezug.sitzung, t = Beginn
mobil.signal          bezug.sitzung, t..bis innerhalb eines UTC-Tages; nach jedem Abruf geschrieben (mehrere Blöcke je Tag)
mobil.sitzung.ende    bezug.sitzung, t = Beginn, bis = Ende, Zusammenfassung, ende = neueinwahl | abbruch | unbekannt
```

Beispiel: Eine Verbindung beginnt Montag 10 Uhr, Dienstag 12 Uhr startet HA neu, Mittwoch 18 Uhr endet sie. Im Archiv
steht Montag 10 Uhr der Beginn, danach alle 5 Minuten ein Signalblock, Mittwoch 18 Uhr das Ende. Beim Neustart fehlt
höchstens der eine unbestätigte Abruf.

- **Nach einem Neustart** bedeutet ein fehlendes Ende „Abschluss unbekannt“. Erst die nächste Abfrage entscheidet:
  - Läuft dieselbe Verbindung weiter (Verbindungsdauer der Box größer als die Zeit seit dem Beginn), geht die Sitzung
    weiter; die Pause steht als `archiv.luecke` im Archiv.
  - Sonst wird sie mit `ende: unbekannt` geschlossen.
- **Dauerhaft gemerkt** (Store) werden nur Sitzungs-ID, Beginn und der zuletzt bestätigte Stand – keine Messreihen.
- **Messpunkte** nennen ihren Messzeitpunkt, Anker und 5G getrennt; ein fehlender Wert ist `null`.
- **Anzeige:** Seite und CSV fassen Beginn, Blöcke und Ende zu einer Zeile je Verbindung zusammen; die Einzelzeilen muss
  niemand lesen.
- **Geräte-Sitzungen** (`geraet.sitzung.start/ende`) folgen demselben Muster ohne Messblöcke.

## Schreiben und Wiederanlauf

Entscheidung Herbert: **kurzes, dokumentiertes Verlustfenster** statt Pflicht zur vollen Vormerk-Kette.

- Ein Schreiber **je Domain** (auch bei mehreren Einrichtungen), eine Warteschlange mit fester Größe, Schreiben im
  Executor nacheinander. Ein Schreibvorgang gilt als **bestätigt**, wenn `flush` und `fsync` zurück sind.
- **Verlustfenster (Normalbetrieb):** Alle Datensätze eines Abrufs sind geschrieben und bestätigt, bevor der nächste
  Abruf endet. Bei Stromausfall fehlt höchstens der noch unbestätigte Abruf. Der Steckbrief nennt die Zeitgrenze bis zur
  Bestätigung und die Höchstzahl unbestätigter Datensätze (Netzwerk: ein Abrufintervall, höchstens ein Abruf).
- **Ausfallregel**, wenn diese Grenze nicht haltbar ist (Schreibfehler, Warteschlange voll, lange Sicherungspause):
  - Die Warteschlange puffert bis zu ihrer festen Größe.
  - Ist sie voll, werden die **ältesten** Datensätze verworfen und gezählt.
  - Sobald wieder geschrieben wird, kommt ein Datensatz `archiv.luecke` mit Zeitraum und Anzahl der verlorenen
    Datensätze.
  - Die Diagnose zeigt Rückstand und Verluste; die Integration täuscht keine vollständige Archivierung vor.
- Hat die Integration eine eigene SQLite, darf sie Datensätze dort in derselben Transaktion vormerken (dann kein
  Verlust); Pflicht ist das nicht.
- Beim Start: eine abgebrochene letzte Zeile wird nach `defekt/` gesichert und abgeschnitten, nie übersprungen.
- Monatswechsel: alte Datei für weitere Schreibzugriffe schließen, als `.gz.tmp` packen, prüfen, umbenennen, dann die
  Quelle löschen. Ein Absturz dazwischen hinterlässt höchstens beide Dateien; Leser zählen gleiche IDs einmal, und der
  nächste Start löscht die Quelle, wenn die `.gz` vollständig ist.
- Entladen/Neu laden: Warteschlange wird **ausgeschrieben und bestätigt** (bei Fehler gilt die Ausfallregel), nie ein
  zweiter Schreiber.
- Fehler: Die Integration läuft weiter, der Rückstand ist in der Diagnose sichtbar. Ein Reparatur-Hinweis kommt nur bei
  dauerhaften, vom Benutzer lösbaren Ursachen (Datenträger voll, keine Schreibrechte).
- Sicherung: Vor einer HA-Sicherung schreibt der Schreiber die Warteschlange aus, bestätigt sie und pausiert; danach läuft
  er weiter (wie die SQLite in Netzwerk). Dauert die Pause länger als die Warteschlange reicht, gilt die Ausfallregel.

## Aufbewahrung, Größe, Sicherung

- Unbegrenzt aufbewahren.
- Größe Netzwerk, **Schätzung**: 105 120 Signalblöcke im Jahr (einer je Abruf) mit Metadaten ca. 300 Byte → ca. 30 MB
  roh, gepackt ca. 3–5 MB, dazu Geräte-Sitzungen. Der Baustein-Test misst die echte Größe und rechnet aufs Jahr hoch;
  das Ergebnis ersetzt diese Schätzung.
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

Signal:
- 5-Minuten-Werte nur, soweit tatsächlich vorhanden (etwa die letzten 10 Tage).
- Davor Stundenwerte aus der Langzeitstatistik, mit Intervall, Bedeutung (`aggregation: mittel | min | max`) und
  `herkunft_werte: ha_statistik`.
- Eine Stunde, die eine Sitzung nur teilweise abdeckt, wird ihr nicht zugerechnet.

Was das Journal nicht hergibt (Technik, Zelle, Gerätedetails), bleibt `null`. IDs werden aus den Quelldatensätzen
abgeleitet, `herkunft: nachgetragen`; der Nachtrag ist wiederholbar.

Danach kommt die Ansicht „Verbindungen“ im Reiter Funk, mit Filter und CSV. Vorher gibt es ein Mockup.

## Regel G-24

> **G-24 Langzeitarchiv:** Jede eigene Integration legt in `module.yaml` fest, welche fachlichen Vorgänge (Ereignisse,
> Sitzungen, Ergebnisse) langfristig erhalten bleiben, und schreibt sie im gemeinsamen, versionierten Archivformat nach
> `<config>/archiv/<domain>/`. Den normalen Verlauf ihrer Entitäten hält der Recorder; Messreihen im Archiv brauchen
> einen genannten fachlichen Grund. Das Archiv ist ohne die Integration lesbar. Bestätigte Schreibvorgänge bleiben bei
> Neustart erhalten; für noch nicht bestätigte Daten nennt der Steckbrief ein maximales Verlustfenster. Kann die
> Integration diese Grenze wegen eines Fehlers nicht einhalten, zeigt sie die Abweichung an und kennzeichnet erkennbare
> Lücken. Wiederholte Datensätze werden bei der Auswertung nur einmal gezählt. Archiviert eine Integration nichts, steht
> der Grund in `module.yaml`.

**Prüfbar durch:**
- `archive:` vollständig (oder `anwendbar: false` mit Grund); `schema/` passend zum Katalog.
- Fachtest je Art.
- Gemeinsame Baustein-Tests:
  - Schreibbestätigung und Verlustfenster mit Zeit- und Mengengrenze;
  - Absturz vor, während und nach der Bestätigung;
  - Wiederholung;
  - volle Warteschlange und Sicherungspause;
  - laufende Sitzung beim Neustart;
  - Uhrsprung;
  - Monatswechsel und Packen;
  - Korrektur.
- Entladen/Neu laden; Sicherung und Wiederherstellung.
- Datenschutzprüfung von Feldern, Texten und Exporten.

**Ab Stufe:** 2.

## Entscheidungen Herbert

13.10.2026:

1. Geräte-Sitzungen kommen ins Archiv (pseudonym).
2. Signal je Mobilfunk-Verbindung in 5-Minuten-Werten.
3. Einmaliger Nachtrag aus dem Netzwerk-Journal.
4. Grafana/VictoriaMetrics erst bei Bedarf.
5. Stromausfall: kurzes, dokumentiertes Verlustfenster; die Vormerk-Kette ist keine Pflicht.
6. Sitzungsform Variante A (Beginn – Signal nach jedem Abruf – Ende).
7. G-24 festgelegt (Review CGR-2026-10-13-ha-grundsatz abgeschlossen).

