# tracker done — Task abschließen

Vollständiger Ablauf, Commit-Ermittlung und Nachlauf für `tracker done`. Beispiele: `beispiele.md`, Abschnitt
„tracker done“.

## Inhalt

- Kommando
- Ablauf
- Ablauf für Projekte ohne Custom Fields oder Anker (Ausnahme)
- Automatischer Nachlauf nach tracker done (4-Schritt-Nachlauf, Lieferung nach einem Skill-Issue, Ausnahmen, VERBOTEN)
- Commit-Disziplin: ein Task = ein Commit (Workflow pro Task, Ausnahmen, Version, Abgrenzung zu `git-commit-helper`)
- Keine Shell verfügbar?
- Keine Commit-Info ermittelbar?
- Git-Commit-Ermittlung (Detailhilfe)

---

## Kommando

`tracker done: <Stichwort oder <PRÄFIX>-NNN>`

---

## Ablauf

1. **Task finden** via `clickup_search` (falls `<PRÄFIX>-NNN` nicht explizit)
2. **Mehrere Treffer** → mit Auswahlfrage User wählen lassen
3. **Review-Workflow-Check** (Pflicht vor jedem Task-Abschluss): Wurden im
   Chat neue Regeln/Entscheidungen besprochen die andere Tasks betreffen?
   4-Punkte-Check (aktueller Task, Parent, Siblings, verweisende offene
   Tasks) gemäß `references/review-workflow.md`. Gefundene Änderungen in
   ClickUp umsetzen BEVOR der Task auf done gesetzt wird.
4. **Commit-Infos ermitteln** (Pflicht):
   - Wenn Task Code-Bezug hat (Modul mit Code-Scope — siehe Tracker-Config, Modul-Kürzel):
     - Claude fragt User: "Welche Datei(en) sind betroffen?" (Prosa, offene Frage!)
     - In der Shell: `git log -1 --format="%h|%ad|%s" --date=short -- <Datei>`
     - Oder: `git log --all --diff-filter=A --format="%h %ad %s" --date=short -- <Datei>` (erste Erwähnung)
     - Oder: `git log --grep="vX.Y.Z" --format="%h %ad %s" --date=short` (Version bekannt)
   - Wenn Task reiner Doc-Bezug:
     - Gleicher Weg, aber auf die Doku-Pfade
   - Wenn Task keinen Code-Bezug hat (z.B. Meta-Task):
     - Commit ID + Commit Text leer lassen
     - Erledigt-Datum = heute (YYYY-MM-DD)
5. **Bei mehreren Commits:** Auswahlfrage mit allen Kandidaten (Hash + erste Zeile)
6. **Pro-Task-Quittung im Chat schreiben** (direkt vor `clickup_update_task`):
   ```
   ✅ <PRÄFIX>-NNN oder Issue-ID — [<PRÄFIX>-ANCHOR-<task-id>] — erledigt: Commit <hash> <kurzbeschreibung>
   ```
   Die Quittung ist Bestätigung + Body-Anker + Audit-Zeile in einem Format.
   **Bei ≥2 Tasks in einer Antwort:** Vollständiges Batch-Protokoll greift — siehe `references/batch-protocol.md` (Batch-Ansage, Pro-Task-Zyklus, Batch-Audit).
7. **Nachpflege-Felder prüfen** (falls bei `tracker neu` nicht gesetzt):
   - Typ, Aufwand, Zielversion, Komponente, Zugehörige Docs
   - Falls alle leer: Auswahlfrage mit fehlenden Feldern
8. **Custom Fields vorbereiten** (konkrete Field-IDs siehe Tracker-Config):
   ```
   custom_fields = [
     {"id": "<Commit-ID-Field>",         "value": "<7-char-hash>"},
     {"id": "<Commit-Text-Field>",       "value": "<erste Zeile der Commit-Message>"},
     {"id": "<Erledigt-Field>",          "value": "<YYYY-MM-DD>"},
     {"id": "<Chat-Anker-erledigt-Field>", "value": "[<PRÄFIX>-ANCHOR-<task-id>] - erledigt: ..."},
     // + Nachpflege-Felder falls gesetzt
   ]
   ```
9. **Einziger API-Call**:
   ```
   clickup_update_task(
     task_id: "<TaskID>",
     status: "<Status laut Statusmodell der Tracker-Config>",   ← KLEINGESCHRIEBEN; Werte je Projekt: beispiele.md
     custom_fields: custom_fields
   )
   ```
10. **`[ANKER-LIVE]` aufräumen** (nur Cowork-Chat, `cowork.md` Abschnitt „[ANKER-LIVE] im Ablauf“)
11. **Bestätigung** an User:
    ```
    ✅ <PRÄFIX>-NNN auf <Status> gesetzt
       Commit: <hash> — <Erste Zeile der Message>
       Erledigt: <YYYY-MM-DD>
       Anker: [<PRÄFIX>-ANCHOR-<task-id>] (erstellt + erledigt)
    ```

### Ablauf für Projekte ohne Custom Fields oder Anker (Ausnahme)

Gilt nur, wenn die Tracker-Config ausdrücklich „Keine“ sagt.
Standard ist das volle Schema:

1. Task finden, Review-Check, Commit-Hash ermitteln wie im Ablauf oben
   (Hash in der Shell der Umgebung: `git log -1 --format='%h %s'`)
2. Nachpflege-Felder, Feld-Liste und `[ANKER-LIVE]` entfallen
3. Status-Wert aus der Tracker-Config, Abschnitt „Statusmodell“ (z.B. ein Abnahme-Status
   statt `done`, wenn die Abnahme der User macht)
4. `clickup_update_task(task_id, status)` + `clickup_create_task_comment` nach
   `clickup-fields.md` Abschnitt „Kommentar statt Felder“ (Version, Commit-Hash, was
   der User prüfen soll)
5. Quittung: `✅ <PRÄFIX>-NNN — erledigt: Commit <hash> — <ClickUp-Link>` (kein Anker)
6. Nachlauf unten gilt unverändert (Zwischenstand-Tabelle, Folgeoptionen
   als Auswahlfrage); nur das Setzen der Custom Fields entfällt
---

## Automatischer Nachlauf nach tracker done

**Kernregel:** Nach jedem erfolgreichen `clickup_update_task` auf `done`/`complete`
MUSS Claude automatisch den Nachlauf ausführen. **Niemals passiv auf
User-Input warten nach `tracker done`.**

### 4-Schritt-Nachlauf

1. **Commit-Hash selbst in der Shell der Umgebung holen** (falls nicht schon aus vorhergehendem
   `git commit`-Call bekannt; Shell im Cowork-Chat: `cowork.md`):
   ```
   cd "<Repo-Pfad>"
   git log -1 --format='%h %s'
   ```
   Den Hash nicht vom User anfordern wenn eine
   Shell verfügbar ist.

2. **Custom Fields in ClickUp setzen** — passiert typischerweise schon im
   einzigen API-Call des Ablaufs (Commit ID, Commit Text, Erledigt-Datum,
   Chat-Anker erledigt). Falls der Hash erst jetzt im Nachlauf
   ermittelt wurde: zweiter `clickup_update_task` mit den Feld-Updates.

2a. **Wenn abgeschlossener Task ein Skill-Issue war: Skill liefern** (Abschnitt „Lieferung nach einem
   Skill-Issue“ unten), in separatem Antwort-Block (nicht mit Schritt 3/4 vermischen).

3. **Zwischenstand-Tabelle im Chat** zeigen — Kompakt-Überblick was erledigt
   wurde und was noch offen ist:
   ```
   | Item | Status |
   |------|--------|
   | <Task-ID> done (<hash>, <version>) | ✅ |
   | Push nach origin/<branch> | <Push-Stand> |
   ```
   `<branch>` und `<Push-Stand>` nach SKILL.md, Abschnitt „Grundsätze“ (Branch, Push).
   Bei mehreren parallelen Items (z.B. Skill-Issues-Session): vollständige
   Session-Tabelle mit allen abgeschlossenen und offenen Punkten.

4. **Folgeoptionen als Auswahlfrage** — 2-4 Optionen mit konkreten nächsten Schritten:
   ```
   Auswahlfrage:
     question: "Was als nächstes?"
     options:
       - "<Nächster geplanter Issue/Task mit Kurzbeschreibung>"
       - "<Alternativer thematisch passender Task>"
       - "Anderen Punkt anpacken (ich sag welchen)"
       - "Pause"
   ```
   Niemals als Prosa-Frage. Niemals still warten.

### Lieferung nach einem Skill-Issue

Gilt wenn der Task aus einer Skill-Issues-Liste stammt UND der zugehörige Commit einen Skill unter `skills/<skill>/`
geändert hat – `SKILL.md` oder eine Reference.

- Lieferung nach `skills/skill-pflege/references/delivery.md`: Reihenfolge (zuerst das Repo, dann die Lieferung) im
  Abschnitt „Reihenfolge“; immer die vollständige Datei, bei einem Skill mit references die Zip mit `SKILL.md` und
  `references/` – auch wenn nur eine Reference geändert wurde – im Abschnitt „Was geliefert wird“.
- In Claude Code die Datei an den Nutzer schicken (`delivery.md`, Abschnitt „Claude Code“); er speichert sie bei
  claude.ai. Im Cowork-Chat als Artifact (`delivery.md`, Abschnitt „Cowork“; `cowork.md` Abschnitt „Lieferung nach
  einem Skill-Issue“).
- **Ausnahmen (keine Lieferung):** Zero-Change-Tasks; Commits, die keinen Skill-Inhalt ändern.
- **Mehrere Skill-Issues in einer Batch-Session:** pro geändertem Skill EINE Lieferung in SEPARATEM Antwort-Block;
  der User bestätigt „gespeichert“ zwischen den Skills (`delivery.md`, Abschnitt „Ein Skill je Antwort“). Nennt das
  Skill-Profil eine Upload-Liste, gilt stattdessen die gesammelte Upload-Runde (`delivery.md`, Abschnitt
  „Upload-Runde“).

### Ausnahmen

- **Zero-Change-Tasks:** Schritt 1 entfällt (kein Commit, kein Hash). Schritte
  2-4 bleiben. Im Quittungstext `(Zero-Change)` vermerkt (Abschnitt „Commit-Disziplin“).

- **Batch-Abschluss (mehrere Tasks hintereinander done):** Schritte 1-2 pro
  Task durchlaufen, Schritt 3 einmal am Batch-Ende mit Gesamt-Übersicht,
  Schritt 4 **nur einmal** nach dem letzten Task.

- **Keine Shell verfügbar:** Schritt 1 entfällt automatisch. Dann Prosa-Frage
  an den User: "Commit-Hash?" (offene Frage, nicht Auswahlfrage).

### VERBOTEN

- Nach `tracker done` passiv auf User-Input warten ohne Auswahlfrage
- Commit-Hash vom User anfordern wenn eine Shell verfügbar ist
- Zwischenstand-Tabelle nach Task-Abschluss weglassen
- Folgeoptionen als Prosa-Frage statt Auswahlfrage
- Folgeoptionen bereits nach dem ersten Task eines Batches zeigen — erst am Batch-Ende
- Skill-Issue auf done setzen ohne Lieferung des Skills im nachfolgenden Antwort-Block
- Nachlauf komplett überspringen, weil „der User weiß ja eh was er will“ — die Regel ist verbindlich, auch wenn der
  User aktiv ist
- Zero-Change-Tasks als Grund für komplettes Überspringen nehmen — nur Schritt 1 (Hash holen) entfällt, Schritte 2-4
  bleiben

---

## Commit-Disziplin: ein Task = ein Commit

**Kernregel:** Jeder abgeschlossene (Sub-)Task bekommt sofort einen eigenen
Commit. Kein Sammeln am Session-Ende.

### Workflow pro Task

1. Task umsetzen (Code/Doc-Änderung)
2. Review-Workflow-Check (`review-workflow.md`): Parent / Siblings / verweisende offene Tasks betroffen?
3. Commit-Befehl vorbereiten (Versionierung siehe unten)
4. Commit **sofort** nach Abschluss — nicht sammeln
5. Hash aus Commit-Output übernehmen (oder via `git log -1 --format="%h"` ermitteln)
6. `tracker done` mit Commit-Hash im Custom Field `Commit ID` ausführen

### Ausnahmen

- **Zero-Change-Tasks:** Tasks ohne Git-Änderung (Task-Description-Updates,
  Memory-Edits, reine ClickUp-Pflege) brauchen keinen Commit. Custom Field
  `Commit ID` und `Commit Text` bleiben leer (bzw. Kommentar ohne Hash, wenn
  das Projekt keine Felder hat). Im Quittungstext mit
  `(Zero-Change)` markieren, damit das leere Feld nachvollziehbar ist.

### Version

Die Versionsnummer des Commits richtet sich nach `Commit.Versionsregel` im Skill-Profil; Format und Nummer setzt
git-commit-helper.

### Abgrenzung zu `git-commit-helper`

| Skill | Verantwortung |
|-------|---------------|
| `tracker` | **WANN** committet wird (Task-Lebenszyklus-Kopplung) |
| `git-commit-helper` | **WIE** der Commit formatiert wird (Format, Version, Titel, Body) |

Commit-Disziplin gehört in `tracker`, Commit-Formatierung in `git-commit-helper`.

---

## Keine Shell verfügbar?

1. User nach Commit-Hash fragen (Prosa, offene Frage)
2. User nach Commit-Message fragen (Prosa)
3. Erledigt-Datum = heute
4. Chat-URLs (nur mit Chat-Feldern, `chat-url-handling.md`): aktueller Chat als Fallback für beide Felder

---

## Keine Commit-Info ermittelbar?

Per Auswahlfrage: Manuell eingeben, Feld leer lassen, Abbrechen.

---

## Git-Commit-Ermittlung (Detailhilfe)

### Szenario A: Commit wurde gerade in dieser Session gemacht
Der Hash ist Claude aus dem `git commit` Output bereits bekannt → direkt verwenden.
Chat erledigt = aktueller Chat.

### Szenario B: Task ist früher erledigt worden (Nachtrag)

In der Shell:
```sh
cd "<Repo-Pfad>"
# Suche nach erster Datei-Erstellung
git log --all --diff-filter=A --format="%h|%ad|%s" --date=short -- "<Pfad/zur/Datei.cs>"

# Oder: Suche nach bestimmter Version
git log --all --format="%h|%ad|%s" --date=short --grep="vX.Y.Z"

# Oder: Suche nach Stichwort
git log --all --format="%h|%ad|%s" --date=short --grep="<Stichwort>"

# Oder: Genauer Zeitpunkt (für Chat-Matching)
git log --all --format="%h|%aI|%s" -- "<Datei>"
```
Der Pipe-Separator `|` erleichtert das Parsen: `<hash>|<datum>|<message>`.

### Szenario C: Mehrere relevante Commits

Auswahlfrage mit allen Kandidaten als Optionen (Hash + erste Zeile Message).
In der Regel: Erster Commit der die Funktionalität eingeführt hat (diff-filter=A).

### Datumsformat

- git liefert: `YYYY-MM-DD` (mit `--date=short`) oder ISO (`%aI`)
- ClickUp erwartet: `YYYY-MM-DD` (direkt)
- Für Chat-Suche (nur Cowork): ISO-Zeitstempel mit Stunde/Minute (für recent_chats Zeitfilter)
