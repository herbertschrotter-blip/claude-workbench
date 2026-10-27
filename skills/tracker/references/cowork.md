# tracker im Cowork-Chat

Was nur im Cowork-Chat gilt. Hauptumgebung ist Claude Code; dort kommen alle Werte aus dem Skill-Profil und der
Tracker-Config (`SKILL.md`, Abschnitt „Voraussetzung: Skill-Profil“), und es gibt weder Memory-Einträge noch
`[ANKER-LIVE]`.

## Inhalt

- Projektkennung und Zähler im Memory
- Werkzeugsuche im Cowork-Chat
- Shell
- Memory-Einträge ändern
- [ANKER-LIVE] im Ablauf
- Lieferung nach einem Skill-Issue

## Projektkennung und Zähler im Memory

- **Projektkennung:** Memory-Eintrag `[PROJECT] <n> | Repo: <pfad> | ...` → Tracker-Config im Repo lesen (Shell
  unten).
- **Zähler und Listen:** Memory-Eintrag
  `[CLICKUP] Space:<ID> | Listen: <Modul>:<ListID>, ... | Next:<NNN> | Letzte Sync: Teil <N>`. Daraus `Next` für
  `tracker neu` und die Listen-IDs; bei Abweichung zwischen Modul-Kürzeln ist der `[CLICKUP]`-Eintrag die Quelle,
  danach die Tracker-Config.
- **Zielversion** im Fragemodus von `tracker neu`: Optionen aus `[CLICKUP]` und dem aktuellen Release-Stand.
- **Fehlt die Config** (kein `[PROJECT]`-Eintrag): Auswahlfrage nach „Fehlende Werte“ wie in `SKILL.md`;
  *Profil ergänzen* → zusätzlich den `[PROJECT]`-Eintrag ins Memory (`memory_user_edits`), erst nach Zustimmung.
- **Memory-Pflege** nach jeder relevanten Änderung:
  - Next-Nummer nach jedem `tracker neu` erhöhen (`Next:` +1)
  - neue Liste (Auto-Create für neue Module, `clickup-fields.md`) → `[CLICKUP]`-Eintrag um die Listen-ID erweitern;
    Space-ID dafür aus `[CLICKUP]`
  - Letzte Sync-Markierung (z.B. `Letzte Sync: Teil <N>`) setzen

## Werkzeugsuche im Cowork-Chat

ClickUp-Tools sind in Claude.ai **deferred-loaded** und werden mit `tool_search` und dem **exakten Tool-Namen** geladen:

```
✅ tool_search("clickup_get_task")          # lädt das Tool
❌ tool_search("clickup task subtasks")     # liefert Müll-Treffer
❌ tool_search("clickup retrieve task")     # liefert Müll-Treffer
```

Recovery bei „Tool not found“ wie in `clickup-tools.md`, mit `tool_search("<exakter Name>")`.

## Shell

Die Shell ist im Cowork-Chat Desktop Commander, nach cc-steuerung (dort Default-Ausführungsmodus). Commit-Hash,
`git log` und TEMP-ID laufen darüber; den Hash nicht vom User anfordern, wenn Desktop Commander verfügbar ist.

## Memory-Einträge ändern

- Memory-Eskalation (`SKILL.md`): den Memory-Eintrag nach Bestätigung mit `memory_user_edits` (`remove`) entfernen —
  nie stillschweigend, nie automatisch.
- `[ANKER-LIVE]`-Einträge: hinzufügen mit `memory_user_edits(command: "add", control: "[ANKER-LIVE] …")`, entfernen mit
  `memory_user_edits(remove, <line>)` (Stale-Check in `anker-system.md`).

## [ANKER-LIVE] im Ablauf

Format und Lifecycle: `anker-system.md`. In den Abläufen der Befehle:

| Befehl | Aktion auf `[ANKER-LIVE]` |
|--------|---------------------------|
| `tracker neu` vor dem Anlegen | `[ANKER-LIVE]` aus Memory lesen; Eintrag mit Typ `offen` zum Thema dieses Tasks? → TEMP-ID merken (Feld „Chat-Anker temp“, Quittung mit ` (war TEMP-<id>)`); sonst kein TEMP |
| `tracker neu` / `tracker issue` nach dem Anlegen | Falls TEMP existierte: Eintrag **ersetzen** (TEMP-... → Task-ID-Eintrag mit Typ `erstellt`); sonst neuen Eintrag mit Typ `erstellt` hinzufügen |
| `tracker done` | Eintrag mit Task-ID und Typ `erstellt` entfernen; falls temporär ein Typ `erledigt` gesetzt wurde, auch entfernen. Danach existiert im Memory nichts mehr zu diesem Task |
| Batch | dieselben Regeln **pro Task einzeln**; keine Sammelaktualisierung am Batch-Ende. Jeder Memory-Aufruf ist Teil des Pro-Task-Zyklus (`batch-protocol.md`, „Pro Task: Tool-Call → Quittung“) |

## Lieferung nach einem Skill-Issue

Regeln: `complete-task.md`, Abschnitt „Lieferung nach einem Skill-Issue“, und
`skills/skill-pflege/references/delivery.md`, Abschnitt „Cowork“. Im Cowork-Chat als Artifact-Paar direkt
hintereinander, in separatem Antwort-Block:

```
Schritt A: create_file
  path: /home/claude/SKILL.md
  file_text: <komplette neue Skill-Datei aus dem Repo>

Schritt B: present_files
  filepaths: ["/home/claude/SKILL.md"]
```

Skills mit references: eine Zip statt des Artifacts (`delivery.md`, Abschnitt „Cowork“). Pro geändertem Skill ein
Artifact in separatem Antwort-Block; der User bestätigt „gespeichert“ zwischen den Skills.
