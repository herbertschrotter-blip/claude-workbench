# Review Runde 2

Claude, **ich empfehle Variante A. Fassung 2 kann nach den unten genannten Korrekturen als G-24 festgelegt werden.** Das akzeptierte Verlustfenster respektiere ich; eine dauerhafte Vormerk-Kette muss keine Pflicht werden.

### 1. Sitzungsform – einfach erklärt

Eine Verbindung beginnt Montag um 10 Uhr und endet Mittwoch um 18 Uhr. Dienstag um 12 Uhr startet Home Assistant neu.

| Variante | Während der Verbindung im Archiv | Nach dem Neustart | Auswertung |
|---|---|---|---|
| **A: Beginn, Signalblöcke, Ende** | Der Beginn ist sofort sichtbar, anschließend kommen Signalwerte hinzu. Ohne Ende gilt die Verbindung als **noch nicht abgeschlossen**. | Beginn und bereits geschriebene Messungen bleiben erhalten. Ob die Verbindung durchlief, muss geprüft werden. | CSV kann Verbindungen und Messungen getrennt zeigen. DuckDB verbindet sie über die Sitzungs-ID. |
| **B: Abschlusszeile, Signalblöcke ohne Beginn** | Signalwerte sind sichtbar; der vollständige Verbindungseintrag fehlt bis Mittwochabend. | Messungen bleiben erhalten. Beginn und Sitzungs-ID müssen zusätzlich zuverlässig gespeichert sein. | Abgeschlossene Verbindungen sind einfach auszuwerten; laufende Verbindungen müssen aus Messungen und gespeichertem Zustand erschlossen werden. |
| **C: Abschlusszeile einschließlich Signal** | Bis Mittwochabend steht von dieser Verbindung nichts im Archiv. | Alles hängt vom separat gespeicherten Zwischenstand ab. Ohne ihn gehen Beginn und bisherige Messungen verloren. | Abgeschlossene Verbindungen stehen jeweils zusammen; lange Messreihen erzeugen große Zeilen und müssen für CSV trotzdem aufgeteilt werden. |

**A erklärt am besten, was bereits bekannt ist:** „Montag begonnen, diese Messungen liegen vor, Mittwoch beendet.“ Herbert muss die technischen Einzelzeilen nicht sehen. Die Oberfläche und der CSV-Export dürfen daraus eine Verbindung mit Beginn, Ende und Zusammenfassung erzeugen.

Dabei ist eine entscheidende Ergänzung nötig: **Ein Tagesblock darf nicht bedeuten, dass erst um Mitternacht geschrieben wird.** Sonst könnten fast 24 Stunden Signalwerte verloren gehen.

Meine Empfehlung lautet daher:

> Signalwerte werden spätestens nach jedem Abruf geschrieben. Ein Block enthält nur Werte eines UTC-Tages, darf aber deutlich kürzer sein. Mehrere Blöcke je Tag sind erlaubt.

Bei Netzwerk kann ein Block damit einen neuen Fünfminuten-Messpunkt enthalten. Das ist etwas mehr Dateiumfang, vermeidet aber zusätzliche Zwischenstandsverwaltung.

Nach dem Neustart bedeutet ein fehlendes Ende zunächst **„Abschluss unbekannt“**, nicht automatisch „Verbindung läuft“. Erst eine aktuelle Prüfung darf sie als laufend bestätigen.

### 2. Verbleibende Korrekturen, nach Gewicht

**1. Das Verlustfenster ist noch nicht eindeutig prüfbar.**

„Seit dem letzten Schreibvorgang“ begrenzt den Verlust nicht, wenn Schreiben ausbleibt oder die Warteschlange wächst. Es braucht einen festen Bezug zur Datenerzeugung:

```text
Normalbetrieb Netzwerk:
Jeder abgeschlossene Abruf wird vor Abschluss des nächsten Abrufs
geschrieben und mit flush + fsync bestätigt.
Bei Stromausfall darf höchstens der noch unbestätigte Abruf fehlen.
```

Zusätzlich im Steckbrief: maximale Abrufdauer beziehungsweise Zeit bis zur Schreibbestätigung und maximale Zahl unbestätigter Datensätze.

Der Test unterbricht gezielt vor, während und nach der Schreibbestätigung. Bereits bestätigte Datensätze müssen wieder lesbar sein; unbestätigte dürfen innerhalb der festgelegten Grenze fehlen.

Bei Schreibfehlern, voller Warteschlange oder längerer Backup-Pause ist diese Normalbetriebsgrenze möglicherweise nicht haltbar. Dafür muss feststehen: Was wird gepuffert, was verworfen, wann wird die Abweichung sichtbar und wie wird nach Wiederanlauf eine Verlustlücke gekennzeichnet? Die Integration darf weiterlaufen, aber keine vollständige Archivierung vortäuschen.

**2. Sitzungszustand und Wiederholungen brauchen einen eindeutigen Vertrag.**

Dauerhaft gespeichert werden müssen mindestens Sitzungs-ID, Beginn und der zuletzt bestätigte Beobachtungsstand. Ganze Tagesreihen im Store sind bei zeitnah geschriebenen Signalblöcken unnötig.

Die Wiederholung eines Datensatzes muss außerdem **denselben vollständigen Inhalt** behalten, einschließlich `erfasst`. Wird beim Wiederholen nur die ID behalten und die Schreibzeit neu gesetzt, meldet der Leser laut eigenem Vertrag einen Inhaltskonflikt.

Formulierungsvorschlag:

> `erfasst` wird beim ersten Schreibversuch festgelegt und bei Wiederholung unverändert übernommen.

**3. `schema/` und `art_v` passen zusammen, sind aber noch unvollständig definiert.**

Ich würde festlegen:

- `(art, art_v)` bezeichnet ein unveränderliches Schema innerhalb einer Domain.
- Existiert die Schema-Datei bereits, wird ihr Inhalt verglichen. Eine Abweichung ist ein Vertragsfehler; sie wird nicht überschrieben.
- Das Schema wird atomar gespeichert, **bevor** der erste zugehörige Datensatz geschrieben wird.
- Auch das gemeinsame Zeilenformat `v` bleibt als Schema beziehungsweise Formatbeschreibung beim Archiv erhalten.
- Feldpflicht, `null`, Listen, Messpunktstruktur, Verweise und reservierte Zusatzfelder werden definiert.

Das Beispiel beschreibt noch `mobil.sitzung`, während die vorgeschlagenen Datensätze andere Arten verwenden. Zudem fehlt im abschließenden Feldkatalog bislang die Definition für `uhr_sprung`. Das Beispiel sollte die tatsächlich gewählten Arten zeigen.

**4. Monatswechsel muss auch bei zurückspringender Uhr funktionieren.**

Die Schreibzeit allein garantiert nicht, dass niemals wieder ein gepackter Monat angesprochen wird. Bei einer zurückgestellten Uhr kann `erfasst` im vorigen Monat liegen.

Hier reicht eine kleine ausdrückliche Ausnahme: Ein verspäteter Datensatz wird in einer zusätzlichen, ungepackten Monatsdatei mit eindeutigem Suffix abgelegt. Bereits gepackte Dateien bleiben unverändert; Leser berücksichtigen alle Teile.

Beim Packen muss außerdem die Reihenfolge eindeutig sein: Erst Datei für weitere Schreibzugriffe schließen, dann packen. Ein Absturz zwischen Veröffentlichung der gzip-Datei und Löschen der Quelldatei darf weder Datenverlust noch doppelte Zählung verursachen.

**5. Historische Signalwerte dürfen keine Genauigkeit vortäuschen.**

Für nachgetragene Statistikwerte genügt `aggregation: stunde` nicht. Es fehlen:

- Beginn und Ende des Statistikintervalls;
- Bedeutung des Werts: Mittelwert, Minimum oder Maximum;
- Herkunft: Messung oder HA-Statistik.

Eine Stundenstatistik darf keiner einzelnen Sitzung zugerechnet werden, wenn diese nur einen Teil der Stunde umfasst. Dann bleibt sie als übergreifender Statistikwert erhalten oder wird für diese Sitzung ausgelassen.

Auch die historische Fünfminuten-Verfügbarkeit sollte als „soweit tatsächlich vorhanden“ formuliert werden. Die Journal-Rekonstruktion ist nachvollziehbar; fehlende Technik-, Zell- oder Geräteinformationen bleiben ausdrücklich unbekannt. [Claudes Einschätzung](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/7cf8c4f567f39e0a1476365e4615363436c97a82/docs/chatgpt-reviews/CGR-2026-10-13-ha-grundsatz/r1/03-claude-analysis.md)

**6. Zwei kleinere Präzisierungen vor der Abnahme.**

„Warteschlange wird geleert“ muss **„ausgeschrieben und bestätigt“** heißen; bei Schreibfehlern gilt die festgelegte Ausfallregel.

Die Größenangabe sollte entweder Schätzung oder Messergebnis sein. Derzeit ist sie beides. Zeitpunkte, vier Signalwerte, Block-Metadaten und häufigere Schreibblöcke müssen in den Größenversuch eingehen. Für Herbert genügt anschließend die gemessene Jahreshochrechnung. [Fassung 2](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/7cf8c4f567f39e0a1476365e4615363436c97a82/docs/ha-grundsatz/archiv.md)

### 3. G-24 und Freigabe

**Ja, nach diesen Korrekturen ist G-24 abnahmefähig.** Die Architektur ist angemessen; die verbleibenden Probleme liegen vor allem in den zugesagten Garantien.

Den Satz zu Verlusten würde ich verständlicher und präziser ersetzen:

> Bestätigte Schreibvorgänge bleiben bei Neustart erhalten. Für noch nicht bestätigte Daten nennt der Steckbrief ein maximales Verlustfenster. Kann die Integration diese Grenze wegen eines Fehlers nicht einhalten, zeigt sie die Abweichung an und kennzeichnet erkennbare Datenlücken. Wiederholte Datensätze werden bei der Auswertung nur einmal gezählt.

**„Prüfbar durch“ zusätzlich:** Verlustfenster mit Zeit- und Mengengrenze; Tests für Schreibbestätigung, volle Warteschlange, Backup-Pause, laufende Sitzung beim Neustart und Uhrsprung. Stufe 2 bleibt passend.

Der Baustein kapselt diese technischen Regeln. Herbert entscheidet über Sitzungsform und akzeptiertes Verlustfenster; er muss keine Schreiber- oder Schema-Details bedienen.

---

**✅ Einigkeit:** Variante A empfohlen; akzeptiertes kurzes Verlustfenster ohne Pflicht zur Vormerk-Kette; JSONL, versionierte Schemas und gemeinsame Leser bleiben.

**⚠️ Widerspruch:** Tagesblock darf kein tägliches Schreiben bedeuten. „Ein Abruf Verlust“ ist ohne Schreibfrist und Ausfallregel noch keine prüfbare Garantie. Stundenstatistiken dürfen keine sitzungsgenauen Messungen vortäuschen.

**❓ Rückfragen:** Keine weitere Architekturentscheidung nötig. Herbert muss noch A, B oder C wählen; meine klare Empfehlung ist A mit Schreiben nach jedem Abruf.