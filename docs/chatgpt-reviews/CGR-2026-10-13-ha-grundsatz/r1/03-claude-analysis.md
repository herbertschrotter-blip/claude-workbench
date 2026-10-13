# Runde 1 – Einschätzung Claude

**Gesamt:** Fast alles übernehmen. ChatGPT bestätigt den Grundansatz und verlangt einen härteren Vertrag – zu Recht.

**Übernehmen:**
- Abgrenzung nach „normaler Entitätsverlauf“ vs. „fachlicher Vorgang“ statt „Zahlen“ vs. „Ereignisse“. Die Aussage „kein
  anderer Weg hält Ereignisse“ wird relativiert. G-10 wird präzisiert: Messreihen im Archiv nur mit Begründung.
- Zusätzliche Felder `id` (stabil), `instanz`, `erfasst`, `art_v`, `ersetzt`. Zeiten in UTC mit `Z`. Monatsdatei nach
  Erfassungszeit. Kein `NaN`, und ein fehlender Wert ist nie 0.
- Der Arten-Katalog wird zusätzlich als `schema/` im Archiv abgelegt.
- Sitzungen als Beginn, Signalblöcke (höchstens ein UTC-Tag) und Ende. Neustart = Beobachtungslücke, nicht Ende.
- Schreiber je Domain. Unvollständigen Dateischwanz sichern und abschneiden. gzip atomar. Rückstand sichtbar machen,
  Repairs nur bei dauerhaften Ursachen.
- HMAC-SHA256 mit geheimem Schlüssel statt sha256(salz:mac) (heute in Netzwerk). Zellkennungen als standortbezogen kennzeichnen.
- Regeltext G-24 im Kern übernehmen. `owns.data[].storage` um `archiv` erweitern, Validator mit.
- Rollenteilung Baustein / Integration wie in der Tabelle.

**Abwägen – Haltbarkeit:** Die volle Vormerkung (Outbox → Append → fsync → Bestätigung) ist sauber, für einen Einsteiger
und kleine Integrationen aber schwer. Mein Vorschlag: append-only mit stabiler `id` (Leser entfernen Duplikate), fsync
je Schreibvorgang, beim Start den Dateischwanz prüfen. Ein **dokumentiertes Verlustfenster** (das, was zwischen zwei
Schreibvorgängen anfällt, Netzwerk ≤ 1 Abruf) ist in Ordnung. Wo es eine SQLite gibt, darf die Integration die Outbox
nutzen, muss aber nicht.

**Größe neu gerechnet:** 105 120 Signalpunkte im Jahr à ca. 30 Byte sind ca. 3 MB roh, gepackt ca. 0,5–1 MB, dazu die
Geräte-Sitzungen. Unkritisch; der Baustein misst es trotzdem im Test.

**Antwort auf Rückfrage 3 (Journal):**
- Das Journal kennt `mobil_neu` (mit Dauer der vorigen Verbindung → Beginn und Ende rekonstruierbar), `mobil_technik`,
  `mobil_zelle` (mit RSRP zum Zeitpunkt), `internet_stoerung` und Geräte `neu/online/offline/ip_wechsel/anschluss`.
- 5-Minuten-Signalwerte gibt es rückblickend nur ca. 10 Tage (Recorder-Statistik), davor Stundenwerte. Der Nachtrag
  übernimmt diese als `aggregation: stunde` und weist Lücken aus.
