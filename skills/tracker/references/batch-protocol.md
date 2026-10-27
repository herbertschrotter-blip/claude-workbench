# Batch-Protokoll — Pro-Task-Disziplin bei Mehrfach-Operationen

**Zweck:** Erzwingt dass bei Batch-Operationen (≥2 Task-Operationen in derselben Antwort) pro einzelnem Task alle Disziplinen eingehalten werden — Body-Anker im Chat, Custom Fields in ClickUp, Commit-Info. Bei Mehrfach-Operationen gehen sonst Custom Fields und Body-Anker einzelner Tasks verloren; das Protokoll löst das durch **Format-Zwang statt Erinnerungs-Disziplin**. Dazu die Vollfassung der Referenz-Anker in Folge-Antworten. Beispiele: `beispiele.md`, Abschnitte „Quittungen und Referenz-Anker“ und „Batch“.

## Inhalt

- Batch-Definition
- Pro-Task-Quittung (PFLICHT)
- Referenz-Anker in Folge-Antworten (PFLICHT)
- Pro-Task-Custom-Fields (PFLICHT)
- Ablauf bei Batch (Batch-Ansage, Pro Task, Subtask-Regel, Parent-Container-Regel, Batch-Audit)
- Integration mit anderen Skills
- VERBOTEN (Batch-spezifisch)
- Referenz-Format

---

## Batch-Definition

**Batch** = ≥2 schreibende Task-Operationen in derselben Antwort. Schreibend heißt:

- `clickup_create_task` (tracker neu)
- `clickup_update_task` mit Status-Änderung (tracker start, tracker done)
- `tracker start` mit Parent-Kaskade zählt als **2 Operationen** (Subtask + Parent)

Auch wenn die Tasks inhaltlich unabhängig sind (z.B. 3 Issue-Tasks in verschiedenen Listen) gilt dieses Protokoll — die Disziplin-Lücke entsteht durch die Anzahl der Operationen, nicht durch deren thematische Verwandtschaft.

**KEIN Batch:**
- 1 Task-Create + beliebig viele Custom-Field-Updates am selben Task (zählt als 1 Operation)
- `clickup_search` / `clickup_get_task` ohne schreibenden Folgecall
- Mehrfaches `clickup_update_task` am selben Task (gleiche Task-ID = 1 Operation)
- `tracker start` ohne Parent (1 Operation) → keine Batch-Pflicht, aber Pro-Task-Quittung bleibt

---

## Pro-Task-Quittung (PFLICHT)

Nach **jedem** schreibenden Tool-Call (create oder status-ändernder update) steht **im selben Antwort-Block, bevor der nächste Tool-Call startet**, eine Quittungszeile:

```
✅ <PRÄFIX>-NNN oder Issue-ID — [<PRÄFIX>-ANCHOR-<task-id>] — <typ>: <kurz>
```

**Die Quittung ersetzt drei frühere Elemente in einem Format:**
- Bestätigung an User
- Body-Anker
- Audit-Spur für eine spätere Chat-Suche

**VERBOTEN:**
- Zusammengefasste Quittungen ("6 Tasks erstellt")
- Tabellen statt einzelner Quittungszeilen
- Quittungen am Ende des Antwortblocks gesammelt nachtragen
- `"analog für die anderen"` / `"wie gehabt"` / `"..."`

---

## Referenz-Anker in Folge-Antworten (PFLICHT)

Die Kurzfassung steht in `SKILL.md`, Abschnitt "Kernregel: Referenz-Anker in Folge-Antworten".
Hier steht die Vollfassung: wann Pflicht, wann nicht, und die Abgrenzung zur
Pro-Task-Quittung (Abschnitt oben).

Die Pro-Task-Quittung greift nur **im moment des Tool-Calls**.
Wenn ein Task über mehrere Antworten hinweg inhaltlich besprochen wird
(Commit-Vorschlag, Klärungsfrage, Fehler-Fix, Fortschritt), versinkt er
ohne Anker im Chat.

### Format

**Am Anfang jeder Antwort** die einen bereits existierenden Task inhaltlich
betrifft:

```
Betroffene Tasks in dieser Antwort: [<PRÄFIX>-ANCHOR-<task-id>] <name>.
```

- Einzelner Task: `[<PRÄFIX>-ANCHOR-<task-id>] <name>.`
- Mehrere Tasks kommagetrennt: `[<PRÄFIX>-ANCHOR-<id-1>] <name-1>, [<PRÄFIX>-ANCHOR-<id-2>] <name-2>.`

### Wann Pflicht

- Commit-Vorschlag für einen Task
- Klärungsfrage zu laufendem Task-Fix
- Fehler-Diagnose während Task-Arbeit
- Status-Update / Fortschrittsbericht
- Nachträgliche Analyse oder Konzept-Änderung
- Antwort in einem Thread der einen aktiven Task behandelt

### Wann NICHT Pflicht

- Task-ID nur in Aufzählung erwähnt ("die 4 tracker-Issues")
- Antwort rein über Meta/Tooling (Shell, git, Skill-System)
- Rückfrage ohne Task-Bezug
- Reine Begrüßung / Abschluss

### Abgrenzung zu Pro-Task-Quittung

Die Pro-Task-Quittung enthält den Anker bereits inline
(`✅ <id> — [<PRÄFIX>-ANCHOR-<task-id>] — <typ>: <kurz>`). Wenn in derselben
Antwort eine Quittung steht, **entfällt der separate Referenz-Anker oben**
für diesen Task.

Für Tasks die *nur erwähnt* werden (ohne Tool-Call) bleibt der Referenz-Anker
oben aber pflicht — auch wenn in derselben Antwort ein anderer Task eine
Quittung bekommt.

### VERBOTEN

- Referenz-Anker weglassen in Folge-Antworten die den Task inhaltlich betreffen
- Referenz-Anker unten statt oben (erschwert Suche und Überblick)
- Referenz-Anker und Quittung für denselben Task doppelt zeigen
- Referenz-Anker für Tasks setzen die nur am Rande erwähnt werden (z.B. in langen Aufzählungen)
- Task inhaltlich diskutieren ohne Anker — der Thread verliert sonst die Audit-Spur für eine spätere Chat-Suche

---

## Pro-Task-Custom-Fields (PFLICHT)

Im **selben Tool-Call-Block** wie `clickup_create_task` bzw. der status-ändernde `clickup_update_task` müssen gesetzt werden (Feld-IDs aus der Tracker-Config des Projekts — ohne Felder entfällt der Block, Commit-Hash kommt dann als Kommentar):

**Bei `create`:**
- `Chat-Anker erstellt` — Wert: `[<PRÄFIX>-ANCHOR-<task-id>] - erstellt: <kurz>`

**Bei `done`:**
- `Chat-Anker erledigt` — Wert: `[<PRÄFIX>-ANCHOR-<task-id>] - erledigt: <kurz>`
- Commit-Hash + Commit-Text (Skill-Issues: nur Commit-Hash)
- Erledigt-Datum

**Nicht erlaubt:** "Custom Fields setze ich am Ende für alle Tasks gesammelt" — genau dabei gehen die Felder einzelner Tasks verloren.

**Task-ID-Problem beim Create:**
Bei `clickup_create_task` kennt Claude die finale Task-ID erst *nach* dem Call. Deshalb zweistufig:

1. `clickup_create_task` mit Platzhalter `[<PRÄFIX>-ANCHOR-PENDING] - erstellt: <kurz>` im Chat-Anker-Feld
2. Sofort danach `clickup_update_task` mit der echten Task-ID: `[<PRÄFIX>-ANCHOR-<echte-id>] - erstellt: <kurz>`
3. Quittungszeile im Chat mit der echten Task-ID

Beide Calls zählen zusammen als **eine** Task-Operation im Sinne der Batch-Definition.

Die exakten Feld-IDs pro Workspace stehen in der Tracker-Config (Abschnitt „Felder und Option-IDs“). Sie sind innerhalb eines Batches **pro Task einzeln** zu senden.

**Unicode-Warnung:** Im Text-Value von Custom Fields das ASCII-Minus `-` verwenden, nicht den em-dash `—`. Letzterer löst einen `clickup_update_task`-Fehler aus. Im Chat-Body-Anker ist `—` ok — nur in Custom-Field-Values vermeiden.

---

## Ablauf bei Batch

### Batch-Ansage (vor dem ersten Tool-Call)

```
📦 Batch: N Tasks (create: X, update: Y, done: Z)
```

Beispiel:
```
📦 Batch: 6 Tasks (create: 6, update: 0, done: 0)
```

Das zwingt Claude, **vor** Beginn die Anzahl zu verbalisieren — ein Zähler als Pflicht.

### Pro Task: Tool-Call → Quittung

Reihenfolge innerhalb eines Task-Zyklus:

1. `clickup_create_task` (oder status-ändernder `clickup_update_task`) **inkl. Anker-Custom-Field im selben Call**
2. Bei `create`: Nachträglicher `clickup_update_task` mit echter Task-ID im Anker-Feld
3. Quittungszeile im Chat-Body schreiben
4. Erst jetzt zum nächsten Task übergehen

Kein Task ohne Quittung. Keine Quittung ohne vorherigen Tool-Call.

### Subtask-Regel

Werden in einem Batch **sowohl Parent als auch Subtasks** angelegt oder erledigt:

- **Jeder Subtask** bekommt eine eigene Quittung mit eigenem Anker (Subtasks haben ihre eigene Task-ID, auch wenn sie keine Projekt-Nummer führen)
- **Der Parent** bekommt eine eigene Quittung — niemals "Parent-Anker deckt Subtasks mit ab"

### Parent-Container-Regel

Wird ein Parent-Task ausschließlich dadurch erledigt, dass alle Subtasks done sind (Kaskaden-Abschluss, keine direkte Arbeit am Parent), bekommt er trotzdem eine eigene Quittung:

```
✅ <Parent-ID> — [<PRÄFIX>-ANCHOR-<parent-task-id>] — erledigt: via Subtask-Kaskade (<liste der subtask-bezüge>)
```

Sonst bekommt der Parent keinen Anker, weil keine direkte Arbeit an ihm stattfand, und sein Abschluss bleibt im Chat unauffindbar.

### Batch-Audit (am Ende)

Nach der letzten Quittung **muss** eine Audit-Zeile folgen:

```
Batch-Audit: N/N Body-Anker ✅ | N/N Custom Fields ✅
```

Falls nicht N/N:
- Fehlende Quittungen **sofort nachholen**, nicht einfach weiterschreiben
- Fehlende Custom Fields per zusätzlichem `clickup_update_task` pro Task nachtragen
- Erneuter Audit bis N/N

**N** ist die Zahl aus der Batch-Ansage. Diese muss wieder auftauchen — das verhindert dass Claude "vergisst" wie viele Tasks der Batch eigentlich hatte.

---

Im Cowork-Chat gehört auch die Pflege von `[ANKER-LIVE]` zum Pro-Task-Zyklus: `cowork.md`, Abschnitt
„[ANKER-LIVE] im Ablauf“.

---

## Integration mit anderen Skills

### `chat-wechsel`

Am Chat-Ende werden oft mehrere Tasks gleichzeitig erledigt (Batch-Abschluss). Das gesamte Batch-Protokoll gilt dort uneingeschränkt — kein "vereinfachtes Abschluss-Protokoll" nur weil es um Übergabe geht.

### `code-erstellen`

Nach Commit wird typischerweise **ein** Task erledigt → kein Batch. Erst wenn ein Commit mehrere Tasks abschließt, greift dieses Protokoll.

### `skill-pflege` / `skill-neu`

Wenn in einem Skill-Update mehrere Skill-Issues gemeinsam gelöst werden, ist der Abschluss dieser Issues ein Batch. Das Protokoll gilt.

---

## VERBOTEN (Batch-spezifisch)

- Tabelle statt einzelner Quittungszeilen
- Gesammelte Anker-Liste am Ende ("hab ich jetzt alle auf einmal nachgetragen")
- Parent-Anker nutzen um Subtask-Anker zu sparen
- Custom Fields nur am ersten oder letzten Task des Batches setzen
- Batch-Audit weglassen
- em-dash `—` in Custom-Field-Values (nur ASCII `-` verwenden)
- Quittung schreiben ohne dass der Tool-Call vorher stattgefunden hat (Reihenfolge-Bruch)
- Mehrere Tool-Calls hintereinander ohne zwischendurch Quittungen (Batch-Aufschub)
- Batch-Ansage weglassen (`📦 Batch: N Tasks (create/update/done)`) vor Beginn
- Parent als Container-Task ohne eigene Quittung abschließen — auch Kaskaden-Abschlüsse brauchen eine
- "wie gehabt" / "analog für die anderen" / "..." statt jeder Quittung im Klartext

---

## Referenz-Format

Das Format aus den Abschnitten oben (Batch-Ansage, je Task Tool-Call und Quittung, Batch-Audit) ist das
Referenz-Format; ein ausgeschriebener Batch steht in `beispiele.md`, Abschnitt „Batch“. Abweichungen sind
Regel-Verstöße.
