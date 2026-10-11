# Runde 1 – Einschätzung Claude

## Zustimmung

- **Sandbox als Zukunftsrisiko:** berechtigt. Heute scheitert jeder Befehl, weil bubblewrap im Add-on keine
  Namespaces anlegen kann. Funktioniert die Sandbox nach einem Update, darf Codex im Modus `read-only` das ganze
  Dateisystem *lesen* – also auch `secrets.yaml` und `.storage/` – und den Inhalt an OpenAI schicken. Vorschlag:
  vor jedem Aufruf `codex sandbox -- true` prüfen; gelingt der Test, Weg codex anhalten (Auswahlfrage: kopieren /
  abbrechen) bis zur erneuten Prüfung. So hängt die Grenze nicht stillschweigend an einem Fehlschlag.
- **Vertrauensblock im Prompt:** billig und sinnvoll; kommt in den Abschnitt „Gesprächsformat“ des Wegs codex.
- **Websuche bei vertraulichem Inhalt:** stimmt. Liegt Dateiinhalt im Prompt (privates Repo, Uncommittetes), mit
  `-c web_search="disabled"` aufrufen.
- **`-o` direkt in `02`:** echter Widerspruch zur eigenen Fehlerregel. Neu: `-o` in den Scratchpad
  (`codex-r<N>-v<Versuch>.md`), nach Exit 0 + `turn.completed` + nicht leer unverändert nach `02` kopieren.
- **Resume ohne Arbeitsverzeichnis:** `codex exec resume` kennt kein `-C`; Aufruf deshalb aus dem Scratchpad heraus.
- **Commit-URLs:** gut. Raw-Links mit dem geprüften Commit statt mit dem Branch; Branch und Commit stehen im Prompt
  und in `01`. Löst das Rennen zwischen Push-Prüfung und Abruf.
- **Optionen eingrenzen:** ja, Codex-Optionen nur Modell (`-m`) und Denktiefe (`model_reasoning_effort`).

## Teilweise

- **Regelqualität (Branch-/Push-Kopien, BPM-Fallback, „Code vollständig“, „Modus 7a/2“, Canvas und Personenname im
  Archiv, Themenfrage, ID-Kollision am selben Tag):** zutreffend, aber Altbestand, der im Refactor bewusst wörtlich
  blieb (KEEP/MOVE). Jetzt nur die klaren Widersprüche beheben: „Datei erst in Stufe B“ (widerspricht 03 in Stufe A),
  „Antwort im Canvas“ im Archiv, `codex login status` aus dem Kern in die Reference. Den Rest als Skill-Issue für
  Umbau Phase 6 (Skill für Skill verkleinern).
- **Prozessbeendigung bei Timeout, Quoting, bereinigte Fehlermeldungen:** `timeout` beendet den Prozess bereits;
  Quoting als ein Satz ergänzen. Mehr nicht – sonst wird die Reference zum Shell-Lehrbuch.

## Antworten auf die Rückfragen

- **Lesepfade bei funktionierender Sandbox:** bei `read-only` das gesamte Dateisystem lesbar → genau deshalb der
  Sandbox-Test oben.
- **MCP:** keine; `codex mcp list` meldet keine Server, eine `config.toml` gibt es nicht.
- **Commit als Quellenstand:** ja, akzeptabel (siehe Commit-URLs).

## Abnahme

Runde 1 lief ohne Kopieren: Prompt aus `01`, Antwort per `-o` in `02` (7 KB, Exit 0, `turn.completed`), Codex las
SKILL.md und weitere Dateien über die Live-Websuche, Thread-ID im README.
