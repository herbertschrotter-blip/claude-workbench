# Runde 3 – Einschätzung Claude

Ich stimme allen Präzisierungen zu; es gibt keinen Widerspruch mehr. Die Liste aus `r2/03` gilt mit diesen
Ergänzungen:

- **Punkt 1:** weiter nur bei Exit 1 **und** genau der erwarteten Sandbox-Diagnose. Im Skill steht die
  Freigabelogik; die konkrete Diagnose der geprüften Umgebung (HA-Add-on: `bwrap: Failed to make / slave: Permission
  denied`) in einem Abschnitt „Geprüfte Umgebungen“ der Reference `codex.md`. Unbekannte Umgebung → anhalten.
- **Punkt 2:** der vollständige Vertrauensblock in jedem Prompt, nur eine Fassung.
- **Punkt 3:** „Websuche aus“ auf Serienebene, gesetzt vor dem Senden: wenn Dateiinhalt oder Kontext aus privaten,
  lokalen, unveröffentlichten oder vertraulichen Quellen mitgeht (auch Auszüge, Zusammenfassungen, Entscheidungen);
  bei unklarer Herkunft aus. Ist sie aus, ersetzt ein Block „Dateien“ den Repo-Zugriff-Block – Claude liefert die
  nötigen Inhalte mit. Ersatz-Thread erbt „aus“.
- **Punkt 4/5:** Erfolg = Exit 0 + `turn.completed` + nicht leere Ausgabe dieses Versuchs; Thread-ID sofort ins
  README; vor einem neuen Versuch läuft kein alter mehr (samt Kindprozessen). Absolute, gequotete Pfade;
  Arbeitsverzeichnis Scratchpad auch beim Resume.
- **Punkt 6:** auch zusätzlich gelesene Dateien am selben Commit; bei Commit-Wechsel alte Bewertungen zur erneuten
  Prüfung stellen.
- **Punkt 8:** zusammen mit den jeweiligen Änderungen, nicht am Schluss.
- **Neu (Punkt 10):** Wechsel auf „kopieren“ nach Codex-Runden → Kopierprompt mit Kontextrekonstruktion wie beim
  Ersatz-Thread (Auftrag, Regeln, Ergebnisse, Entscheidungen, geltende Zugriffsbeschränkung).
- **Später:** Berechtigungsprofile von Codex als technische Lesegrenze prüfen (eigene Untersuchung).

Umsetzungsreihenfolge (Codex' Bündel): Sicherheitsfreigabe (1, 3, 7) → Rundenablauf (4, 5) → Review-Grundlage
(2, 6) → Konsistenz (8) laufend mit, Rückfall (10); Altbestand (9) als Skill-Issue.

Bereits in dieser Runde angewendet: Ausgabe zuerst in den Scratchpad (`codex-r3-v1.md`), nach Erfolg nach `02`
kopiert; Aufruf aus dem Scratchpad mit `timeout -k`.
