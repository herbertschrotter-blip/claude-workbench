# Runde 2 – Einschätzung Claude

**Gesamt:** Volle Zustimmung, kein Widerspruch. Variante A mit Schreiben nach jedem Abruf ist die richtige Wahl; die
sechs Korrekturen sind berechtigt und schärfen nur Garantien, nicht die Architektur.

Übernehmen:
1. **Sitzungen Variante A**, Signalblöcke höchstens ein UTC-Tag, aber nach **jedem Abruf** geschrieben (mehrere Blöcke
   je Tag). Ein fehlendes Ende nach einem Neustart heißt „Abschluss unbekannt“, bis eine Prüfung die Verbindung bestätigt.
2. **Verlustfenster prüfbar:** Jeder Abruf ist vor dem Ende des nächsten geschrieben und mit fsync bestätigt. Der
   Steckbrief nennt die Zeitgrenze und die Höchstzahl unbestätigter Datensätze. Ausfallregel für Schreibfehler, volle
   Warteschlange und Backup-Pause: was puffern, was verwerfen, Lücke als Datensatz `archiv.luecke` kennzeichnen,
   Abweichung sichtbar.
3. **Wiederholung mit identischem Inhalt:** `erfasst` wird beim ersten Versuch festgelegt. Gespeichert werden
   Sitzungs-ID, Beginn und der letzte bestätigte Stand.
4. **Schema:** `(art, art_v)` ist unveränderlich. Abweichung = Vertragsfehler. Atomar schreiben, bevor der erste Datensatz
   kommt; Format `v` auch als Schema. Beispiel auf die echten Arten umstellen, `uhr_sprung` definieren.
5. **Monatswechsel:** Verspätete Datensätze kommen in eine ungepackte Zusatzdatei `<JJJJ-MM>.nachtrag-<n>.jsonl`. Packen
   erst nach dem Schließen; ein Absturz zwischen gz und Löschen wird über Duplikat-Entfernung (gleiche IDs) aufgefangen.
6. **Nachgetragene Statistik:** Intervall, Bedeutung (Mittel/Min/Max) und Herkunft. Stunden, die eine Sitzung nur
   teilweise abdecken, werden ihr nicht zugerechnet. „5 min soweit vorhanden“.
7. Kleinigkeiten: „ausgeschrieben und bestätigt“ statt „geleert“. Größe als Schätzung kennzeichnen, gemessen wird im
   Baustein-Test. G-24-Satz zu Verlusten wie vorgeschlagen.

Keine dritte Runde nötig; nach Einarbeitung kann Herbert abnehmen.
