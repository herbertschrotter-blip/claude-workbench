# Beispielwerte und Abläufe aus zwei Projekten

Werte und Abläufe aus BPM (Bauprojektmanager, mehrere Listen, volles Schema) und Heidi (eine Liste, eigene Status), dazu
der Space des Skill-Repos. Sie zeigen, wie die Regeln aus `../SKILL.md` und den references angewendet werden; für jedes
Projekt gelten nur dessen eigenes Skill-Profil und dessen Tracker-Config. IDs sind gekürzt oder Platzhalter.

## Inhalt

- Präfixe, Anker und Spaces
- Quittungen und Referenz-Anker
- tracker neu
- tracker start
- tracker done
- tracker issue
- tracker update / field / status
- tracker split / relate
- Scope-Check
- Batch
- Chat-Anker
- Statuswerte je Projekt

## Präfixe, Anker und Spaces

| Wert | BPM | Heidi | Skill-Repo |
|------|-----|-------|-----------|
| Präfix | `BPM-NNN` | `DX-NNN` | ClaudeSkills ohne Nummern; Skill-Issues `<skill>-NNN` |
| Anker | `[BPM-ANCHOR-…]` | `[DX-ANCHOR-…]` | `[BPM-ANCHOR-…]` (historisch derselbe Präfix) |
| Listen | eine Liste je Modul | eine Liste | ClaudeSkills + Ordner „Skill Issues“ |
| Space | „BPM Entwicklung“ | „Smart Home“ | „Claude Skills Entwicklung“ |

- Titel einer Hauptaufgabe (BPM): `BPM-016 | PM | Recovery nach Crash`
- Chat-Start im Cowork-Chat (BPM):
  ```
  📋 ClickUp: 12 offene V1-Tasks, 4 davon high
     Höchste Prio: BPM-001 | PM | DB-Anbindung Orchestrator [high] [v1] [M]
  ```

## Quittungen und Referenz-Anker

Quittungen:
```
✅ BPM-123 — [BPM-ANCHOR-86c9…] — Feature: …
✅ DX-031 — [DX-ANCHOR-123z…] — Feature: …
✅ BPM-082 — [BPM-ANCHOR-86c9cg8u5] — erstellt: Regex-Erkennung DocumentTypeRecognizer
✅ tracker-001 — [BPM-ANCHOR-86c9f7awj] — erledigt: Commit a1b2c3d Pro-Task-Quittung
✅ Phase-3-Parent — [BPM-ANCHOR-86c9eqnk6] — erledigt: via Subtask-Kaskade (3.1, 3.2, 3.3, 3.4, 3.5)
```

Referenz-Anker mit zwei Tasks:
```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-86c9feyj9] tracker-005, [BPM-ANCHOR-86c9f7awj] tracker-001.
```

**Quittung in der Antwort → KEIN separater Referenz-Anker für diesen Task:**

```
[clickup_update_task tracker-002 status: "in progress"]

✅ tracker-002 — [BPM-ANCHOR-86c9f7cm4] — start: in progress
```

**Reine inhaltliche Diskussion ohne Tool-Call → Referenz-Anker oben:**

```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-86c9feyj9] tracker-005.

Dein Vorschlag A passt besser weil [...]
```

**Mix: Ein Task mit Tool-Call, zweiter nur erwähnt:**

```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-86c9feyj9] tracker-005.

[clickup_update_task tracker-002 status: "in progress"]

✅ tracker-002 — [BPM-ANCHOR-86c9f7cm4] — start: in progress

Die Regel für tracker-005 greift danach analog [...]
```

## tracker neu

Schnellmodus (BPM): `"neue aufgabe: PM — Index-Erkennung spinnt, v1, high, Fix, M"` → direkt anlegen.

Fragemodus (BPM):
```
Frage 1 — Modul: PlanManager, Settings, Infrastructure, Docs, Anderes
Frage 2 — Meilenstein: v1, v1-nice, post-v1, backlog
Frage 3 — Priorität: urgent, high, normal, low
```
```
Frage 1 — Typ: Feature, Fix, Refactor, Perf, Docs, Konzept, Meta
Frage 2 — Aufwand: S (<1h), M (1-4h), L (halber Tag), XL (>1 Tag), Später
Frage 3 — Zielversion: Aktuelle, Nächste Minor, später
```

Durchlauf mit allen Feldern (BPM; Feld- und Option-IDs in der Tracker-Config des BPM-Repos):

```
User: tracker neu: PM — neue Regex-Erkennung in DocumentTypeRecognizer, v1, high

Claude intern:
  1. BPM-<Next> aus Memory: BPM-082
  2. Kürzel PM → Liste-ID aus der Tracker-Config (PlanManager-Zeile)
  3. Dedup: clickup_search "Regex DocumentTypeRecognizer" → kein Treffer
  4. Auswahlfrage:
     Frage 1 — Typ: Feature, Fix, Refactor, Perf, Docs, Konzept, Meta
     Frage 2 — Aufwand: S, M, L, XL, Später
     User antwortet: Feature, M
  5. Prosa-Frage: "Welche Komponente?"
     User: "DocumentTypeRecognizer.cs"
  6. Prosa-Frage: "Zielversion?"
     User: "v0.26.0"
  7. Description-Template generieren
  8. Chat erstellt = aktueller Chat (URL aus Session-Memory)
  9. custom_fields = [Typ=Feature, Aufwand=M, Zielversion=v0.26.0, 
                      Komponente=DocumentTypeRecognizer.cs, Chat erstellt=<url>]
  10. clickup_create_task(...) → Task-ID 86c9xyz12 erhalten
  11. Pro-Task-Quittung im Chat:
      ✅ BPM-082 — [BPM-ANCHOR-86c9xyz12] — erstellt: Neue Regex-Erkennung DocumentTypeRecognizer
  12. clickup_update_task(task_id="86c9xyz12", custom_fields=[{Chat-Anker erstellt: "[BPM-ANCHOR-86c9xyz12] - erstellt: Neue Regex-Erkennung"}])
  13. Memory: Next 082 → 083
```

## tracker start

Fokus-Entscheidung im Dialog:
```
Claude: "Vorschlag: Als nächstes tracker-002 Fix — drei Optionen..."
User:   "Vorschlag OK — Option A + restriktives B"

→ In der Antwort die mit "Plan fix:" beginnt:
   1. clickup_update_task(tracker-002, status: "in progress")  ← ZUERST
   2. Pro-Task-Quittung
   3. Erst DANN "Plan fix: ..."
```

Explizites Kommando:

```
User: tracker start: tracker-002

Claude intern:
  1. Task-ID: tracker-002 → 86c9f7cm4 (aus Issue-ID-Lookup)
  2. clickup_get_task(86c9f7cm4) → status = "to do", parent = null
  3. clickup_update_task(86c9f7cm4, status: "in progress")
  4. Kein Parent → weiter mit der Quittung
  5. Pro-Task-Quittung im Chat:
     ✅ tracker-002 — [BPM-ANCHOR-86c9f7cm4] — start: in progress
  6. Inhaltliche Arbeit beginnt im zuständigen Skill (bei Code: code-erstellen laden).
```

Impliziter Trigger mit Task-ID:

```
User: fangen wir mit tracker-002 an

Claude:
  [Auswahlfrage]
  Frage: "tracker-002 auf 'in progress' setzen? (Kein Parent vorhanden.)"
  Optionen: Ja / Nein

  User: Ja
  → Ablauf wie oben
```

Impliziter Trigger mit Parent:

```
User: starte 4.1

Claude intern:
  1. clickup_search "4.1" → Task 86c9xyz (Parent: 86c9parent)
  2. Auswahlfrage:
     "4.1 + Parent (Phase 4) auf 'in progress' setzen?"
     Optionen: Ja - beide / Nur Subtask / Nein
  3. User: Ja - beide
  4. clickup_update_task(86c9xyz, "in progress")
  5. clickup_get_task(86c9parent) → status = "to do"
  6. clickup_update_task(86c9parent, "in progress")
  7. Quittungen:
     ✅ 4.1 — [BPM-ANCHOR-86c9xyz] — start: in progress
     ✅ Phase-4 — [BPM-ANCHOR-86c9parent] — start: in progress (als Parent)
     Batch-Audit: 2/2 Body-Anker ✅ | 2/2 Custom Fields ✅
```

## tracker done

Code-Task mit Nachlauf (BPM):

```
tracker done auf BPM-082 (Code-Task)
  [Ablauf durchlaufen]
  ✓ Status auf done gesetzt, Custom Fields gefüllt

Automatischer Nachlauf:
  1. Shell: git log -1 --format='%h %s' → hash bereits bekannt aus Commit-Session
  2. Custom Fields schon im Update-Call des Ablaufs → übersprungen
  3. Zwischenstand-Tabelle:
     | Item | Status |
     |------|--------|
     | BPM-082 done (ee4476d, v0.26.0) | ✅ |
     | Push nach origin/main | ⏳ User |
  4. Auswahlfrage:
     "Was als nächstes?"
     - "BPM-083 (Folgefeature laut Prio)"
     - "BPM-084 (Bugfix, geplant)"
     - "Anderer Task"
     - "Pause"
```

Skill-Issue im Cowork-Chat (Lieferung als Artifact):

```
tracker done auf skill-pflege-005 (Skill-Issue)
  [Ablauf durchlaufen]
  ✓ Status auf complete gesetzt, Commit-Hash 09c120b in Custom Field

Automatischer Nachlauf:
  1. Shell: git log -1 → 09c120b bereits bekannt
  2. Custom Fields schon gesetzt
  2a. SKILL.md-Änderung erkannt → Artifact-Block folgt:
      - create_file path=/home/claude/SKILL.md file_text=<Inhalt aus dem Repo>
      - present_files filepaths=["/home/claude/SKILL.md"]
      - User klickt "Skill speichern"
  3. Zwischenstand-Tabelle (nach "gespeichert"-Bestätigung)
  4. Auswahlfrage für Folgeoptionen
```

Commit-Ermittlung mit Chat-Suche im Cowork-Chat (BPM; Feld-IDs und Status-Werte in der Tracker-Config des BPM-Repos):

```
User: tracker done BPM-007

Claude intern:
  1. clickup_get_task("86c9cg8u5") → BPM-007 PlanTyp-Erkennung
  2. Prosa-Frage: "Welche Datei(en) sind betroffen?"
     User: "DocumentTypeRecognizer.cs"
  3. Shell: git log --all --diff-filter=A --format="%h|%aI|%s" -- "src/.../DocumentTypeRecognizer.cs"
     → "cb46a48|2026-04-15T11:34:52+02:00|[v0.25.5] PlanManager, Feature: PatternTemplates..."
  4. Nur 1 Kandidat → direkt verwenden
  5. Chat erledigt:
     → recent_chats(after: "2026-04-15T07:34", before: "2026-04-15T15:34", n: 5, sort_order: "asc")
     → Treffer: Teil 17 (015353fe-...)
  6. Chat erstellt (nicht gesetzt):
     → conversation_search("Plantyp-Erkennung DocumentTypeRecognizer prefix contains")
     → Teil 10 (d546b50b-...) als ältester konkreter Treffer
  7. Nachpflege: Typ fehlt noch
     → Auswahlfrage: Typ → Feature
  8. Pro-Task-Quittung im Chat:
     ✅ BPM-007 — [BPM-ANCHOR-<task-id>] — erledigt: Commit cb46a48 PlanTyp-Erkennung
  9. clickup_update_task(
       status: "done",
       custom_fields: [
         {id: "<Typ-ID>", value: "<Feature-Option-ID>"},
         {id: "<Commit ID-ID>", value: "cb46a48"},
         {id: "<Commit Text-ID>", value: "[v0.25.5] PlanManager, Feature: ..."},
         {id: "<Erledigt-ID>", value: "2026-04-15"},
         {id: "<Chat erstellt-ID>", value: "https://claude.ai/chat/d546b50b-..."},
         {id: "<Chat erledigt-ID>", value: "https://claude.ai/chat/015353fe-..."},
         {id: "<Chat-Anker-erledigt-ID>", value: "[BPM-ANCHOR-<task-id>] - erledigt: Commit cb46a48"}
       ]
     )
  10. Memory `[ANKER-LIVE]`: Einträge zu BPM-007 entfernen
```

## tracker issue

```
User: tracker issue tracker: Em-Dash-Problem in Custom-Field-Values

Claude intern:
  1. Skill-Name: "tracker" → gültig (aus der Tracker-Config)
  2. Listen-ID Lookup: <Listen-ID tracker>
  3. Dedup: clickup_filter_tasks → kein Treffer
  4. Issue-ID automatisch:
     - clickup_filter_tasks(list_ids: ["<Listen-ID tracker>"], include_closed: true)
     - Custom Field Issue-ID jedes Tasks lesen
     - Pattern ^tracker-(\d{3})$ parsen
     - Höchste Nummer: 008 (aus tracker-008)
     - Neue Issue-ID: tracker-009
     - Chat-Output: "Ermittelt: tracker-009 (höchste vorhandene: tracker-008)"
  5. Typ-Frage: Auswahlfrage → User: "Bug"
  6. Beobachtungs-Chat: "Bauprojektmanager Teil 28"
  7. Description-Template mit Bug-Anpassung generieren
  8. clickup_create_task(
       list_id: "<Listen-ID tracker>",
       name: "tracker-009: Em-Dash-Problem in Custom-Field-Values",
       custom_fields: [
         {id: "<Issue-ID-Field>",          value: "tracker-009"},
         {id: "<Typ-Field>",               value: "<Bug-Option-ID>"},
         {id: "<Beobachtungs-Chat-Field>", value: "Bauprojektmanager Teil 28"}
       ]
     )
     → Task-ID 86c9xyz
  9. Unique-Check: clickup_filter_tasks → genau 1 Treffer mit tracker-009 ✓
  10. Pro-Task-Quittung:
      ✅ tracker-009 — [BPM-ANCHOR-86c9xyz] — erstellt: Em-Dash-Problem in Custom-Field-Values
  11. Chat-Anker nachtragen mit Task-ID 86c9xyz
  12. Memory [ANKER-LIVE] Eintrag
```

## tracker update / field / status

- `tracker field: BPM-007 Zielversion v0.26.0`
- `tracker field: BPM-016 Aufwand L`
- `tracker field: BPM-079 Komponente SettingsView.xaml`

`tracker status` (BPM, gruppiert nach Liste):
```
**PlanManager** (6 offen)
- [high] [v1] [M] BPM-001 | PM | DB-Anbindung Orchestrator
  └─ (3 Unteraufgaben, 1 erledigt)
- [normal] [v1] [L] BPM-002 | PM | 5998er Statikplaene
```

Heidi (eine Liste, ohne Felder): gruppiert nach Status (in development, testing, backlog); als offen zählen alle Status
außer `shipped`/`done`/`cancelled`; `tracker next` nennt `testing`-Tasks zuerst und folgt sonst der
Bauplan-Reihenfolge.

## tracker split / relate

```
User: tracker split BPM-016

Claude intern:
  1. Task laden, analysieren
  2. Bestehende Sub-Nummern prüfen (z.B. schon 01-05 vergeben → neue ab 06)
  3. Struktur-Vorschlag mit N Unteraufgaben erarbeiten
  4. Auswahlfrage:
     Frage 1: "5 neue Unteraufgaben anlegen oder anders aufteilen?"
     Optionen: "5 anlegen", "6 (mit Tests)", "3 (kompakt)", "Abbrechen"
  5. Wenn User "5 anlegen" → loslegen
  6. Pro Unteraufgabe: 
     name: "016.<NN> — <Beschreibung>"
     parent: "<task_id>"
     markdown_description: verkürztes Template
  7. Parent auf "in progress" setzen
```

Beziehungen (BPM):
- BPM-007 `blocks` BPM-XX → BPM-XX kann nicht beginnen
- BPM-079 `is blocked by` BPM-079.01 → Mockup muss vor Umsetzung fertig sein
- BPM-004 `relates to` BPM-005 → Thematisch verwandt
- BPM-050 `duplicates` BPM-048 → BPM-050 zum Schließen

Befehle: `tracker relate: BPM-X blocks BPM-Y`, `tracker relate: BPM-X relates BPM-Y`; Bestätigung „✅ BPM-A blocks
BPM-B“.

## Scope-Check

```
Kontext: Phase 7 eines Umbaus. Unteraufgabe 7.1 wird auf done gesetzt.
Im Chat wurde zwischen 7.1 und 7.6 beschlossen, dass alle Projektwerte
künftig aus einer zentralen Config gelesen werden.

OHNE Review-Workflow:
  → 7.1 wird auf done gesetzt
  → 7.6 wird gestartet
  → Erst beim Umsetzen von 7.6 wird bemerkt dass 7.2, 7.3 und 7.4 auch
    den neuen Config-Ansatz brauchen, aber ihre Description das
    nicht reflektiert.
  → Chaos, Nachbesserungs-Loop.

MIT Review-Workflow (bevor 7.1 auf done gesetzt wird):
  Punkt 1: 7.1 Description → passt noch.
  Punkt 2: Parent Phase-7 → Scope passt, aber DoD erwähnt die Config nicht.
           → Parent-DoD ergänzen.
  Punkt 3: Siblings 7.2, 7.3, 7.4, 7.5, 7.6 → alle haben Description aus
           der Zeit vor dem Beschluss.
           → Descriptions aller Siblings updaten mit dem neuen Ansatz.
  Punkt 4: Verweisende offene Tasks → tracker-001/002 verweisen auf 7.x
           → keine Scope-Änderung für diese, aber sie werden später von 7.6
             abhängig sein → Dependency setzen.

  Danach Auswahlfrage: "Siblings sind jetzt konsistent. Direkt mit 7.6
  weitermachen oder die ursprünglich geplante Reihenfolge 7.2 → 7.3 einhalten?"
```

## Batch

Zwei Skill-Issues in der Liste cc-steuerung anlegen:

```
📦 Batch: 2 Tasks (create: 2, update: 0, done: 0)

[clickup_create_task cc-steuerung-001 mit Anker-Platzhalter]
[clickup_update_task 86c9fczy4 mit echter Anker-ID]
✅ cc-steuerung-001 — [BPM-ANCHOR-86c9fczy4] — erstellt: DC-Erkennung am Chat-Start

[clickup_create_task cc-steuerung-002 mit Anker-Platzhalter]
[clickup_update_task 86c9fd0g0 mit echter Anker-ID]
✅ cc-steuerung-002 — [BPM-ANCHOR-86c9fd0g0] — erstellt: DC PowerShell verschluckt Dollar-Variablen

Batch-Audit: 2/2 Body-Anker ✅ | 2/2 Custom Fields ✅
```

## Chat-Anker

```
[BPM-ANCHOR-TEMP-01JS7KABCD] — Idee: Wetter-Modul Google-Sheets-Worker
[BPM-ANCHOR-86c9eupfk] — erstellt: tracker-Skill Anker-Logik (war TEMP-01JS7KABCD)
[BPM-ANCHOR-86c9eupfk] — erledigt: Commit abc1234 tracker Anker-Logik
```

`anker setzen` im Cowork-Chat:

```
User: anker setzen: Wetter-Modul Google-Sheets Polling-Intervall diskutiert

Claude:
  1. TEMP-ID: TEMP-01JS9ABCDE
  2. [BPM-ANCHOR-TEMP-01JS9ABCDE] — Idee: Wetter-Modul GS Polling-Intervall
  3. Memory hinzufügen: "[ANKER-LIVE] TEMP-01JS9ABCDE|offen|2026-04-21T23:15|Wetter-Modul GS Polling-Intervall")
  4. ✅ Anker gesetzt: TEMP-01JS9ABCDE
     Thema: Wetter-Modul GS Polling-Intervall
     Wird bei `tracker neu` mit Task-ID verknüpft oder bei `chat-wechsel` in Übergabeprompt übernommen.
```

## Statuswerte je Projekt

| Projekt / Liste | gestartet | nach `tracker done` | Abschluss |
|-----------------|-----------|---------------------|-----------|
| BPM | `in progress` | `done` | – |
| Skill-Issues | `in progress` | `complete` | – |
| Heidi | `in development` | `testing` | `shipped` setzt der User nach der Abnahme |
