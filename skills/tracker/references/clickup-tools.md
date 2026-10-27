# ClickUp-Tools — Inventar und Lade-Pattern

**Zweck:** Welche ClickUp-Tools tracker-Befehle aufrufen, in welcher Reihenfolge sie geladen werden, und wie man fehlende Tools nachlädt. Ohne explizites Inventar wird mit Suchbegriffen geraten.

## Inhalt

- Lade-Pattern (PFLICHT vor erstem Tool-Call)
- Tool-Inventar (relevant für tracker)
- Befehl → Tool-Mapping
- Workspace-, Space- und Listen-IDs
- Custom-Field-Schema
- Anti-Patterns
- Recovery bei "Tool not found"

---

## Lade-Pattern (PFLICHT vor erstem Tool-Call)

ClickUp-Tools sind **deferred** — sie sind zu Sessionbeginn NICHT im Tool-Inventar, sondern müssen über die Werkzeugsuche der Umgebung aktiviert werden.

**Regel:** Wenn ein Tool nicht aufrufbar ist (`Tool '...' not found`), die Werkzeugsuche mit dem **EXAKTEN Tool-Namen** aufrufen, nicht mit Umschreibung.

In Claude Code heißen die Tools `mcp__<server>__clickup_…`; der Servername steht in der Liste der deferred tools:

```
✅ ToolSearch("select:mcp__<server>__clickup_get_task")   # lädt das Tool
❌ ToolSearch("clickup task subtasks")                     # liefert Müll-Treffer
❌ ToolSearch("clickup retrieve task")                     # liefert Müll-Treffer
```

Nach erfolgreicher Suche ist das Tool für den Rest der Session aufrufbar. Werkzeugsuche im Cowork-Chat: `cowork.md`.

---

## Tool-Inventar (relevant für tracker)

### Schreiben

| Tool | Zweck |
|------|-------|
| `clickup_create_task` | Neue Task anlegen (mit Custom Fields, Status, Parent, Description) |
| `clickup_update_task` | Task-Felder ändern (Status, Custom Fields, Description) |
| `clickup_delete_task` | Task löschen (User-Bestätigung Pflicht) |
| `clickup_move_task` | Task in andere Liste verschieben (ändert Home-Liste) |
| `clickup_add_task_to_list` | Task zu zusätzlicher Liste hinzufügen (Multi-List, Home bleibt) |

### Lesen

| Tool | Zweck |
|------|-------|
| `clickup_get_task` | Einzeltask abrufen, mit `subtasks=true` für Subtask-Details |
| `clickup_filter_tasks` | Tasks nach Space/Liste/Status filtern, mit `include_closed` auch erledigte |
| `clickup_search` | Universalsuche (Tasks, Docs, Chat, etc.) mit Filtern (Listen, Status, Datum) |
| `clickup_get_list` | List-Details und List-ID per List-Name auflösen |
| `clickup_get_workspace_hierarchy` | Spaces/Folders/Lists-Übersicht |

### Kommentare

| Tool | Zweck |
|------|-------|
| `clickup_get_task_comments` | Kommentare einer Task lesen (mit Pagination) |
| `clickup_get_threaded_comments` | Threaded Replies zu einem Kommentar |
| `clickup_create_task_comment` | Neuen Kommentar an Task anhängen |

### Tags & Verknüpfungen

| Tool | Zweck |
|------|-------|
| `clickup_add_tag_to_task` / `clickup_remove_tag_from_task` | Tag-Zuordnung |
| `clickup_add_task_link` / `clickup_remove_task_link` | Task-zu-Task-Verknüpfung |
| `clickup_add_task_dependency` / `clickup_remove_task_dependency` | Abhängigkeiten |

### Custom Fields

| Tool | Zweck |
|------|-------|
| `clickup_get_custom_fields` | Custom-Field-Definitionen einer List/Folder/Space abrufen (für Dropdown-Option-IDs) |

### Time Tracking

| Tool | Zweck |
|------|-------|
| `clickup_start_time_tracking` / `clickup_stop_time_tracking` | Timer steuern |
| `clickup_get_current_time_entry` | Laufender Timer |
| `clickup_get_task_time_entries` | Time-Entries einer Task |
| `clickup_add_time_entry` | Manuelle Time-Buchung |
| `clickup_get_task_time_in_status` / `clickup_get_bulk_tasks_time_in_status` | Zeit pro Status |

### Members & Resolution

| Tool | Zweck |
|------|-------|
| `clickup_resolve_assignees` | Names/Emails/"me" → numerische User-IDs |
| `clickup_find_member_by_name` | Workspace-Member per Name finden |
| `clickup_get_workspace_members` | Alle Members |

### Reminders

| Tool | Zweck |
|------|-------|
| `clickup_create_reminder` / `clickup_update_reminder` / `clickup_search_reminders` | Persönliche Reminders |

### Documents

| Tool | Zweck |
|------|-------|
| `clickup_create_document` / `clickup_create_document_page` / `clickup_update_document_page` | Docs anlegen/ändern |
| `clickup_get_document_pages` / `clickup_list_document_pages` | Doc-Pages lesen |

---

## Befehl → Tool-Mapping

| tracker-Befehl | Primäre Tools | Hinweis |
|---|---|---|
| `tracker neu` | `clickup_create_task` + `clickup_update_task` (für Anker-Felder) | Custom-Field-IDs aus der Tracker-Config |
| `tracker issue` | `clickup_filter_tasks` (mit `include_closed: true`) + `clickup_create_task` + `clickup_update_task` | Issue-ID nach `issue-task.md`, Abschnitt „Issue-ID automatisch ermitteln“ |
| `tracker update` | `clickup_update_task` | Pro Task-Quittung im Chat (Anker-System) |
| `tracker done` | `clickup_update_task` (Status laut Statusmodell + Erledigt + Commit ID + Commit Text + Anker erledigt) | Shell liest Commit-Hash, dann Update |
| `tracker status` | `clickup_filter_tasks` (offene Status laut Statusmodell); `clickup_get_task` mit `subtasks=true` für Details | Für Roadmap-Abgleich Repo↔ClickUp |
| `tracker suche` | `clickup_search` mit Filtern | `location.subcategories` = List-IDs, `task_statuses` = `["unstarted"\|"active"\|"done"\|"closed"\|"archived"]` |
| `tracker next` | `clickup_filter_tasks` (offene Tasks) | Vorschlag der nächsten Aufgabe nach `search-and-status.md` |
| `tracker split` | `clickup_create_task` (Subtasks mit Parent) + ggf. `clickup_update_task` | Pro Subtask Anker setzen |
| `tracker relate` | `clickup_add_task_dependency` (blocks, is blocked by); `clickup_add_task_link` (relates to, duplicates) | Richtung nach `split-and-relations.md` |
| `tracker field` | `clickup_get_custom_fields` (Schema lesen) + `clickup_update_task` (Wert setzen) | Bei unbekannten Field-IDs zuerst Schema holen |

---

## Workspace-, Space- und Listen-IDs

Stehen **nur** in der Tracker-Config des Projekts (Beispiele: `beispiele.md`, Abschnitt „Präfixe, Anker und
Spaces“). Nichts davon im Skill führen.

---

## Custom-Field-Schema

Regeln in **`clickup-fields.md`**; die UUIDs der Custom Fields stehen in der Tracker-Config, Abschnitt „Felder und
Option-IDs“:

- Typ, Aufwand, Zielversion, Komponente
- Commit ID, Commit Text, Erledigt
- Chat-Anker erstellt, Chat-Anker erledigt, Chat-Anker temp
- Issue-ID (Skill-Issue-Listen)

Bei Dropdown-Feldern (Typ, Aufwand) werden NICHT die Display-Namen ("Feature", "S (<1h)") gesetzt, sondern die Option-UUIDs. Diese stehen in der Tracker-Config.

---

## Anti-Patterns

- ❌ Werkzeugsuche mit Umschreibung wenn der Tool-Name bekannt ist — bringt Müll-Treffer
- ❌ Custom-Field-Wert als Display-Name setzen ("Feature" statt UUID) — wird abgelehnt
- ❌ Skill-Issues anlegen ohne die Issue-ID nach `issue-task.md` („Issue-ID automatisch ermitteln“) zu ermitteln — führt zu Doppel-Nummerierung in Skill-Issue-Listen
- ❌ Massen-Updates ohne Pro-Task-Quittung im Chat (siehe `batch-protocol.md`)
- ❌ `clickup_delete_task` ohne explizite User-Bestätigung — Daten verloren

---

## Recovery bei "Tool not found"

```
1. Tool-Name notieren (z.B. "clickup_get_task")
2. Werkzeugsuche mit dem exakten Namen (Claude Code: ToolSearch("select:mcp__<server>__clickup_get_task"))
3. Tool-Aufruf wiederholen
4. Falls weiter "not found": MCP-Verbindung im Connector prüfen (User informieren)
```

Connector-Status prüft der User in Claude.ai unter `Verzeichnis → Konnektoren → ClickUp`.
