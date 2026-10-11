# Runde 2 – Einschätzung Claude

## Ergebnis

Codex stimmt dem Ablauf zu und schärft zwei Punkte nach; beide überzeugen. Damit gibt es eine konsolidierte
Änderungsliste für chatgpt-review (Weg codex):

1. **Sandbox-Test mit eindeutiger Diagnose:** vor jedem Aufruf `codex sandbox -c sandbox_mode="read-only" -- true`.
   Weiter nur, wenn er mit genau `bwrap: Failed to make / slave: Permission denied` scheitert (am Pi geprüft:
   dieselbe Meldung wie bei `codex exec`). Gelingt der Test oder kommt eine andere Meldung: Weg codex anhalten
   (kopieren / abbrechen). Später prüfen: Berechtigungsprofile (`-P`, `--sandbox-state-readable-root`) als echte
   Lesegrenze, falls die Sandbox einmal läuft.
2. **Vertrauensblock** in jeder Runde kurz, beim Ersatz-Thread vollständig.
3. **Websuche threadweit aus**, sobald vertraulicher Inhalt im Thread war (Dateiinhalt im Prompt); im README der
   Serie vermerken (`**Websuche:** live | aus`) und nie wieder einschalten.
4. **Versuche im Scratchpad:** `-o` und JSONL je Versuch im Scratchpad, erst bei Erfolg unverändert nach `02`;
   Fehlversuch dokumentieren, im nächsten Prompt sagen, dass keine Antwort übernommen wurde; Thread unklar → neuer
   Thread mit archiviertem Kontext.
5. **Timeout** in einem Satz mit Ergebnis: geordnet beenden, nach Frist zwangsweise (`timeout -k`), Ende bestätigen,
   vorher kein neuer Versuch.
6. **Commit-URLs:** Raw-Links mit dem vollen Remote-Commit; Kern bekommt die Ausnahme von der Branch-Regel für den
   Weg codex; Commit-Wechsel zwischen Runden nennen.
7. **Codex-Optionen** nur Modell und Denktiefe.
8. **Konsistenz jetzt:** Weg-Tabelle, Phase 2 und Lifecycle („Codex schreibt 02“ → „Claude übernimmt 02 bei
   Erfolg“); „Datei erst in Stufe B“; „Antwort im Canvas“ im Archiv; `codex login status` in die Reference; eine
   bestehende Serie nie als neue überschreiben.
9. **Altbestand** (kopierte Querschnittsregeln, BPM-Fallback, „Code vollständig“, „Modus 7a/2“, Personenname und
   Cowork-Details im Archiv, pauschale Themenfrage, Namensschema bei Kollision) → Skill-Issue für Umbau Phase 6.

## Abnahme des Wegs codex

Zwei Runden ohne Kopieren: r1 per `codex exec`, r2 per `codex exec resume` im selben Thread; Antworten per `-o` in
`02`, Thread-ID im README, alle vier Dateien je Runde in ihrer Phase angelegt. Kriterium der ClickUp-Aufgabe erfüllt.
