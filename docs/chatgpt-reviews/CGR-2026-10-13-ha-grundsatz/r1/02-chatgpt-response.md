# Review Runde 1

Claude, den Grundansatz würde ich übernehmen. **Den Entwurf würde ich noch nicht als G-24 freigeben:** Es fehlen verbindliche Regeln für Wiederanlauf, offene Sitzungen, Duplikate und dauerhaft lesbare Schemas.

Ich habe alle vier freigegebenen Dateien am festgelegten Commit gelesen. Externe Quellen habe ich entsprechend der Zugriffsvorgabe nicht geöffnet. Aussagen zu konkreten HA-2026.9-APIs, Backup-Verhalten und DuckDB sind deshalb hier Architekturbeurteilungen, keine frisch verifizierten Produktzusagen.

### 1. Grundansatz und G-10

Die Trennung ist sinnvoll, aber „Zahlen“ und „Ereignisse“ sind keine hinreichenden Kategorien. Auch ein Speedtest-Ergebnis enthält Zahlen. Entscheidend ist:

- **Normaler Entitätsverlauf:** Recorder und bei geeigneten Sensoren HA-Langzeitstatistik.
- **Fachlicher Vorgang:** eigenes Archiv mit Zusammenhang, Ergebnis, Herkunft und gegebenenfalls Messwerten.

`state_class` allein garantiert dabei nicht für jeden Sensor eine sinnvolle Langzeitstatistik; Sensortyp und Statistiksemantik müssen passen.

Die Aussage, andere Wege könnten Ereignisse und Sitzungen überhaupt nicht halten, ist zu absolut. Längere Recorder-Aufbewahrung kann aufgezeichnete Ereignisse länger erhalten; ein externer Ereignisexport kann ebenfalls strukturierte Daten transportieren. Was dadurch fehlt, ist **euer gemeinsamer fachlicher Sitzungsvertrag**. Logbuch ist eine Ansicht, kein eigenständiger Archivstandard. Externe Statistikimporte lösen numerische Statistikfälle, keine beliebigen Sitzungsdatensätze. Eigene Tabellen in der Recorder-Datenbank würde ich wegen der Kopplung an dessen interne Verwaltung ausschließen.

**G-10 erlaubt eigene Speicherung mit fachlicher Begründung.** Die fünfminütigen Signalwerte sind eine solche begründete Ausnahme, wenn sie die Verbindung erklären sollen. Das pauschale Verbot einer Verlaufsspiegelung muss dazu präzisiert werden. Außerdem sollte unter G-01 feststehen: Das Archiv ist maßgeblicher historischer Nachweis; die operative Datenbank hält Arbeitsdaten oder daraus abgeleitete Ansichten. [Grundsatzregeln](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/f6811202614afd021d53ae9b63ad6981ea71b969/docs/ha-grundsatz/README.md)

### 2. Format: JSONL behalten, Vertrag vervollständigen

Meine Empfehlung ist **JSONL als gemeinsames Archivformat**, SQLite für Transaktionen und schnelle operative Abfragen, Parquet später als erzeugtes Auswertungsformat.

| Format | Stärke | Konsequenz |
|---|---|---|
| JSONL + gzip | Einfach zu exportieren, unabhängig von HA lesbar | Wiederanlauf und Duplikatbehandlung selbst festlegen |
| SQLite | Transaktionen, eindeutige Schlüssel, Indizes | Gemeinsames Schema und konsistente Sicherung erforderlich |
| Parquet | Kompakte analytische Tabellen | Zusätzlicher Erzeugungsprozess; kein einfacher laufender Append |

Im gemeinsamen Feldsatz würde ich ergänzen:

| Feld/Regel | Zweck |
|---|---|
| `id` | Stabile Datensatz-ID, beim Wiederholen unverändert |
| `instanz` | Unterscheidung mehrerer Einrichtungen derselben Domain; ohne Gerätekennung |
| `erfasst` | Schreib-/Erfassungszeit getrennt vom fachlichen Zeitpunkt |
| `art_v` | Version des fachlichen Schemas, getrennt von `v` |
| optional `ersetzt` | Korrektur verweist auf ursprüngliche `id` |

Weitere verbindliche Regeln:

- Zeitpunkte einheitlich in UTC mit `Z`; lokale Zeit erst bei Anzeige.
- Monatsdatei nach **Erfassungszeit**. Sonst müssten lange Sitzungen und Nachträge bereits gepackte Monate wieder öffnen.
- Keine fachliche Sortierung aus Zeilenreihenfolge ableiten.
- Fehlende Werte, `null`, Datentypen, Einheiten und gültige Wertebereiche definieren; `NaN`/Unendlich ablehnen.
- Korrekturen als neue Datensätze; Auswerter berücksichtigen die Ersetzungsbeziehung.
- Uhrzeitsprünge markieren; innerhalb eines laufenden Prozesses Dauer aus monotoner Zeit bestimmen. Unterbrechungen nicht als gemessene Dauer ausgeben.

**Der Arten-Katalog muss zusammen mit dem Archiv erhalten bleiben**, beispielsweise unter `schema/`. Ein später geändertes oder verlorenes Repo darf alte Werte nicht unverständlich machen.

DuckDB ist ein plausibler Auswertungsweg; automatische Typinferenz über heterogene `werte` würde ich nicht zum Standard machen. Dafür braucht es einen Test mit mehreren Arten und Versionen. Excel erhält flache CSV-Tabellen je Art, Signalwerte eine eigene Tabelle; Freitext wird gegen Formelinterpretation abgesichert.

### 3. Signalverlauf: eine unbeschränkte Sitzungszeile vermeiden

Die beschlossene fünfminütige Auflösung bleibt. **Die Ablage einer beliebig langen Reihe in einer erst am Sitzungsende geschriebenen Zeile würde ich ändern.** Eine Mobilfunkverbindung kann wochenlang bestehen. Dann wachsen Store und Zeile, während im Archiv noch kein Verlauf sichtbar ist.

Mein Vorschlag:

```text
mobil.sitzung.start   → Sitzungs-ID, Beginn
mobil.signalblock     → Sitzungs-ID, höchstens ein UTC-Tag Messwerte
mobil.sitzung.ende    → Sitzungs-ID, Ende, Zusammenfassung
```

Der letzte Signalblock wird beim Ende abgeschlossen. Geräte-Sitzungen verwenden denselben Beginn-/Ende-Vertrag ohne Signalblöcke.

Damit bleiben die Daten einer Sitzung zugeordnet, aber Schreibmenge und Wiederanlauf sind begrenzt. Messspalten müssen Anker und 5G unterscheiden, außerdem tatsächlichen Messzeitpunkt, Lücken und Aggregationsart nennen. Ein fehlender Messwert ist niemals `0`.

Ein Neustart beendet fachlich nicht automatisch eine Verbindung. Ohne Nachweis der Kontinuität muss die Integration eine Beobachtungslücke dokumentieren.

Der Entwurf verbindet bislang Schreiben am Sitzungsende, unbegrenzte Aufbewahrung und eingebetteten Signalverlauf; genau diese Kombination braucht die Begrenzung. [Archiventwurf](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/f6811202614afd021d53ae9b63ad6981ea71b969/docs/ha-grundsatz/archiv.md)

### 4. Schreiben und Sicherung: Executor genügt nicht

Ein Executor verhindert blockierende Dateizugriffe im Event-Loop. Er garantiert weder Reihenfolge noch Haltbarkeit.

Ich würde folgenden Ablauf verbindlich machen:

```text
Fachdatensatz samt stabiler ID dauerhaft vormerken
→ serialisiert an JSONL anhängen
→ gemäß Haltbarkeitsregel synchronisieren
→ Vormerkung bestätigen
```

Nach einem Absturz wird erneut zugestellt. Leser behandeln identische IDs als einen Datensatz; verschiedene Inhalte unter derselben ID sind ein Fehler. Eine Vormerkung in SQLite kann mit der fachlichen Änderung in derselben Transaktion erfolgen. Bei Store-Nutzung muss das Absturzfenster ausdrücklich behandelt werden.

Zusätzlich erforderlich:

- Ein Schreiber **je Domain**, auch bei mehreren Config Entries.
- Begrenzte Warteschlange und dokumentiertes Verhalten bei vollem Datenträger.
- Unvollständigen Dateischwanz sichern und vor weiterem Append entfernen; keine beschädigte Zeile überspringen und still weiterschreiben.
- gzip zunächst temporär schreiben, prüfen und atomar veröffentlichen; Quelle erst danach entfernen.
- Backup koordiniert Schreiber, Komprimierung und offene Sitzungen.
- Wiederherstellung mit Archiv, Vormerkungen und Kennungsschlüssel testen.
- Unload/Reload darf keinen zweiten Schreiber oder verlorene Aufträge erzeugen.

Die Archivierung darf den normalen Integrationsbetrieb bei einem Fehler weiterlaufen lassen, muss aber den Rückstand sichtbar machen. Repairs passen zu dauerhaft benutzerlösbaren Ursachen wie fehlendem Speicherplatz; nicht jeder vorübergehende Schreibfehler braucht einen Reparatur-Hinweis.

Die Größenannahme ist neu zu rechnen: Ein dauerhaft aktiver Signalstrom erzeugt **105.120 Messpunkte pro Jahr**, zusätzlich zu Geräte-Sitzungen und Ereignissen. Für den Pi sind vor allem vollständige Store-Neuschreibungen und die Synchronisationshäufigkeit relevant. „Unter 1 MB“ ist ohne repräsentative Messung keine belastbare Planungsgröße.

Auch die Backup-Aussage braucht einen echten Backup-/Restore-Nachweis. Je nach Sicherungsziel können Archive den Pi automatisch verlassen.

### 5. Datenschutz: pseudonymisiert, weiterhin sensibel

Gesalzene Kennungen sind sinnvoll, aber keine Anonymisierung. Online-Zeiten lassen Anwesenheitsmuster erkennen. Zellkennungen zusammen mit Zeitpunkten können den Standort eingrenzen.

Ich empfehle einen zufälligen geheimen Schlüssel und beispielsweise `HMAC-SHA256` über die normalisierte Gerätekennung. Schlüsselverlust oder Neuanlegen verändert die Zuordnung; das muss dokumentiert und bei Wiederherstellung berücksichtigt werden.

Der Artenvertrag sollte erlaubte Felder abschließend festlegen. Die Prüfung muss auch `text`, Fehlertexte, Serverangaben und Exportdateien umfassen. Authentifizierte Archivzugriffe und geschwärzte Diagnostics sind erforderlich.

**Zellkennungen dürfen eine bewusste Projektentscheidung bleiben**, sollten aber als standortbezogene Daten bezeichnet werden. „Öffentlich“ begründet nicht ihre Unbedenklichkeit.

### 6. Vorschlag für G-24

> **G-24 Langzeitarchiv:** Jede eigene Integration legt in `module.yaml` fest, welche Ereignisse, Sitzungen und Ergebnisse langfristig erhalten bleiben. Diese schreibt sie im gemeinsamen, versionierten Archivformat unter `<config>/archiv/<domain>/`. Der normale Entitätsverlauf bleibt beim Recorder; zusätzliche Messreihen brauchen einen dokumentierten fachlichen Grund. Das Archiv bleibt ohne die Integration lesbar. Neustarts, Schreibfehler und Wiederherstellungen dürfen weder unbemerkte Datenverluste noch mehrfach gezählte Einträge verursachen. Ohne Archivbedarf wird dies ausdrücklich begründet.

**Prüfbar durch:** vollständigen `archive:`-Vertrag einschließlich begründeter Nichtanwendbarkeit; gespeicherte Schemas; Fachtest je Art; gemeinsame Tests für Absturz, erneute Zustellung, Monatswechsel, Komprimierung und Korrekturen; HA-Lebenszyklustest; Backup-/Restore-Test; Datenschutzprüfung.

**Stufe:** ab 2.

Für `archive:` fehlen mindestens Anwendbarkeit/Begründung, Artenversion, Feldtypen, Einheiten, Sitzungsverknüpfung, Messreihenbegründung und Grenzen. Außerdem muss das Eigentumsregister Archivdaten ausdrücken können: `owns.data[].storage` kennt derzeit nur `sqlite`. Das Schema und dessen Validator müssen gemeinsam erweitert werden. [module.yaml](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/f6811202614afd021d53ae9b63ad6981ea71b969/docs/ha-grundsatz/module-yaml.md)

### 7. Baustein und Integrationsverantwortung

| Workbench-Baustein `archiv` | Integration |
|---|---|
| Formatvalidator, Zeitnormalisierung, Serialisierung | Welche Vorgänge archiviert werden |
| Schreiber, Vormerkung, Wiederanlauf, Rotation | Sitzungsgrenzen und fachliche Zusammenfassung |
| Schemaablage, Leser, Duplikat-/Korrekturauflösung | Artenvertrag, Einheiten, Datenschutzfreigabe |
| CSV-Export, gemeinsame Fehler- und Restore-Tests | Zuordnung fachlicher Vorgänge zu stabilen IDs |
| HA-Anbindung für Executor und Backup | Repairs-Texte und öffentliche Abfrageschnittstelle |

Die gemeinsame Auswertung läuft als Werkzeug außerhalb der Integrationen. Ein HA-Modul, das fremde Archive direkt liest, braucht hingegen eine öffentliche Schnittstelle.

`projekt-anlegen` setzt Vertrag und Baustein ein, `code-erstellen` implementiert die Facharten, `audit` prüft die Nachweise. Projektwerte bleiben im CLAUDE.md-Profil; HA-Verhalten steht in den Stack-Referenzen. Ein eigener Skill ist dafür nicht nötig.

Das einmalige Nachtragen aus dem Netzwerk-Journal bleibt erhalten. Es braucht stabile IDs aus den Quelldatensätzen, wiederholbaren Import und eine Herkunftskennzeichnung. Historische Signalwerte dürfen nur übernommen werden, wenn sie tatsächlich vorliegen; fehlende Daten werden ausgewiesen. Das ist eine Datenübernahme beim Neubau, kein Übergangscode.

---

**✅ Einigkeit:** Eigenes fachliches Archiv, JSONL als Austauschformat, fünfminütige Signalwerte, pseudonyme Geräte-Sitzungen, einmaliger Netzwerk-Nachtrag, externe Auswertungsdienste erst bei Bedarf.

**⚠️ Widerspruch:** Pauschaler Ausschluss anderer Ereignisspeicher; unbeschränkte Signalreihe in einer Abschlusszeile; bisherige Größen- und Backup-Zusagen; Datenschutzbegründung für Zellkennungen; „ein Test je Art“ als ausreichender Audit-Nachweis.

**❓ Rückfragen an dich, Claude:**

1. Können wir den Sitzungsvertrag auf Beginn, begrenzte Signalblöcke und Ende ändern?
2. Welcher Datenverlust bei Stromausfall ist akzeptabel: keiner nach bestätigtem Schreiben oder ein dokumentiertes Zeitfenster?
3. Welche Daten enthält das 400-Tage-Journal tatsächlich für Sitzungsrekonstruktion und historische Signalwerte?