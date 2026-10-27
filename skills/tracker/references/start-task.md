# tracker start — Task + Parent auf "in progress" setzen

Setzt einen Subtask auf `in progress` und aktualisiert den Parent-Task
ebenfalls (nur wenn Parent aktuell `open`/`to do`). Beispiele: `beispiele.md`, Abschnitt „tracker start“.

## Inhalt

- Kommando (implizite Trigger, Fokus-Entscheidung im Dialog)
- Ablauf
- Projekte mit eigenem Status-Wert (oder ohne Anker)
- Status-Werte pro Listen-Typ
- VERBOTEN

---

## Kommando

`tracker start: <PRÄFIX>-NNN oder Issue-ID`

### Implizite Trigger (nur mit Task-ID im Satz!)

Folgende Natural-Language-Phrasen lösen eine **Rückfrage** aus (nicht
automatisch ausführen):

- `"starte <PRÄFIX>-NNN"` / `"starte tracker-002"`
- `"<PRÄFIX>-NNN starten"` / `"Issue-XXX starten"`
- `"fangen wir mit <PRÄFIX>-NNN an"`
- `"los mit <PRÄFIX>-NNN"`
- `"wir machen jetzt <PRÄFIX>-NNN"`

Bei Treffer: Auswahlfrage:
```
Frage: "<PRÄFIX>-NNN + Parent auf 'in progress' setzen?"
Optionen:
- "Ja — beide"
- "Nur Subtask"
- "Nein"
```

**VERBOTEN:** Implizite Erkennung OHNE Task-ID im Satz.
Phrasen wie `"los geht's"`, `"fangen wir an"`, `"starten wir"` OHNE Projekt-Nummer
werden ignoriert. Keine rate-basierte Task-Erkennung.

### Fokus-Entscheidung im Dialog (dritte Trigger-Art)

Wenn im Gesprächsverlauf ein Task **zum Arbeitsfokus wird** — auch ohne dass
der User explizit das Wort "starte" verwendet — MUSS Claude `tracker start`
ausführen bevor mit inhaltlicher Arbeit begonnen wird.

**Auslöser:**

- Claude hat einen konkreten Task-Fix vorgeschlagen (`"als nächstes tracker-002"`
  / `"wir machen jetzt <PRÄFIX>-NNN"`)
- User bestätigt mit `"ja"`, `"ok"`, `"weiter"`, `"mach"`, `"passt"`, `"genau"`,
  `"los"`, `"gemacht"` — oder irgendeiner anderen Zustimmung
- → **In der darauffolgenden Antwort ZUERST `tracker start`**, dann Analyse/Code im zuständigen Skill (Code → code-erstellen)

**Voraussetzung:** Der zu fokussierende Task muss **eindeutig aus dem vorigen
Turn hervorgehen**. Wenn mehrere Tasks im Raum stehen: Auswahlfrage
welcher gestartet werden soll.

Beispiel: `beispiele.md`, Abschnitt „tracker start“.

---

## Ablauf

1. **Task-ID auflösen:**
   - Explizite ID (`<PRÄFIX>-NNN`, Issue `tracker-003`) → direkt nutzen
   - Kurzform (`4.1`, `3.5`): via `clickup_search` den passenden Task finden
   - Bei mehreren Treffern: Auswahlfrage

2. **Aktuellen Status prüfen:** `clickup_get_task(task_id)` → wenn schon
   `in progress` oder `done`/`complete`: keine Aktion, Hinweis an User

3. **Review-Workflow-Check** (Pflicht vor jedem Task-Wechsel): Wurden im
   Chat neue Regeln/Entscheidungen besprochen die andere Tasks betreffen?
   4-Punkte-Check (aktueller Task, Parent, Siblings, verweisende offene
   Tasks) gemäß `references/review-workflow.md`. Gefundene Änderungen in
   ClickUp umsetzen BEVOR der Start ausgeführt wird.

4. **Subtask-Status setzen:**
   ```
   clickup_update_task(
     task_id: <id>,
     status: "in progress"
   )
   ```

5. **Parent ermitteln:** `clickup_get_task` liefert `parent`-Feld
   - Wenn `parent` null: kein Parent vorhanden → weiter mit der Quittung
   - Wenn `parent` vorhanden: weiter

6. **Parent-Status prüfen und ggf. setzen:**
   - `clickup_get_task(parent_id)` → aktuellen Status lesen
   - Nur wenn Parent auf `open` / `to do`: auch auf `in progress` setzen
   - Wenn Parent schon `in progress` / `done` / `complete`: keine Änderung

7. **Pro-Task-Quittung im Chat** (pro geändertem Task):
   ```
   ✅ <PRÄFIX>-NNN oder Issue-ID — [<PRÄFIX>-ANCHOR-<task-id>] — start: in progress
   ✅ <Parent-ID> — [<PRÄFIX>-ANCHOR-<parent-task-id>] — start: in progress (als Parent)
   ```

8. **Batch-Audit** (wenn Parent mit geändert wurde):
   ```
   Batch-Audit: 2/2 Body-Anker ✅ | 2/2 Custom Fields (Status) ✅
   ```

9. **Erst DANN inhaltliche Arbeit beginnen**, und zwar im zuständigen Skill: Code → code-erstellen, Mockup →
   mockup-erstellen, Doku → doc-pflege. Den Skill laden, bevor die erste Datei geändert wird; tracker setzt nur den
   Status. Das gilt auch für die Fokus-Entscheidung und für „weiter mit <PRÄFIX>-NNN“.

### Projekte mit eigenem Status-Wert (oder ohne Anker)

- Status-Wert für „gestartet“ aus der Tracker-Config
  Abschnitt „Statusmodell“ nehmen (z.B. `in development` statt `in progress`).
- Parent-Regel (Parent ermitteln, Parent-Status prüfen) gilt unverändert.
- Nur falls das Projekt keine Anker führt: Quittung `✅ <PRÄFIX>-NNN — start: <Status> — <ClickUp-Link>`,
  Batch-Audit ohne den Teil „Custom Fields“.

---

## Status-Werte pro Listen-Typ

Matrix, Wert für „gestartet“ und Fallback-Reihenfolge: `clickup-fields.md`, Abschnitt „Status-Modell“.

---

## VERBOTEN

- Impliziter Start-Trigger OHNE Task-ID im Satz (Prosa-Phrasen wie
  "los geht's" triggern NICHT)
- Status-Änderung ohne Pro-Task-Quittung
- Parent ohne Check auf aktuellen Status automatisch überschreiben
  (wenn Parent schon `in progress` oder `done`: nichts tun)
- Inhaltliche Arbeit beginnen BEVOR `tracker start` ausgeführt wurde
- Raten welche Task-ID gemeint ist wenn unklar — Auswahlfrage
- Code, Mockup oder Doku zu einem gestarteten Task unter tracker selbst schreiben, statt den zuständigen Skill zu laden
- User-Zustimmung zu einem vorgeschlagenen Task-Fokus ignorieren — nach "ok" / "mach" / "weiter" MUSS `tracker start` vor der Arbeit
- Status-Wert raten bei Listen-Typen — Fallback-Reihenfolge einhalten (`clickup-fields.md`), bei Scheitern Auswahlfrage
