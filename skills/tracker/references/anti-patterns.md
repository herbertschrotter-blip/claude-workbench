# Anti-Patterns + Automationspolitik + Integration

Kollektion aller Regeln die verhindern sollen dass tracker-Operationen schiefgehen. Die Kern-Verbote stehen in
`SKILL.md` (Abschnitt „Kern-VERBOTEN (Kurzliste)“), die Verbote eines Befehls oder Protokolls in dessen Reference;
hier stehen die übrigen und je Thema der Verweis.

## Inhalt

- Automationspolitik
- Integration mit anderen Skills
- VERBOTEN (allgemein, Projekt-Config, Verweise je Thema)

---

## Automationspolitik

| Situation | Verhalten |
|-----------|-----------|
| "tracker neu: ..." | Schnellmodus oder Fragemodus (Auswahlfrage!) + Chat erstellt + Custom Fields |
| "tracker start: ..." | Status auf `in progress` + Parent-Check + Pro-Task-Quittung |
| "starte <PRÄFIX>-NNN" / "fangen wir mit <PRÄFIX>-NNN an" | Auswahlfrage: Beide / Nur Subtask / Nein |
| "los geht's" / "fangen wir an" OHNE Task-ID | Ignorieren (kein impliziter Start) |
| User bestätigt vorgeschlagenen Task-Fokus ("ok", "mach", "weiter") | `tracker start` vor inhaltlicher Arbeit |
| "tracker done: ..." | Commit-Info ermitteln + Custom Fields laut Tracker-Config + Status setzen |
| "tracker split: ..." | Vorschlag + Auswahlfrage zur Bestätigung + NN.NN-Nummerierung |
| "tracker relate: ..." | Dependency setzen via ClickUp API |
| "tracker field: ..." | Einzelnes Feld gezielt aktualisieren |
| "anker setzen: ..." | Manuellen TEMP-Anker setzen + Memory-Eintrag (nur Cowork-Chat) |
| code-erstellen nach Commit | NUR vorschlagen (per Auswahlfrage) |
| chat-wechsel am Ende | Batch-Vorschlag + Chat-URL in Prompt einbetten |
| Alle Unteraufgaben done | Auswahlfrage: Parent auch schliessen? |
| "notiz" / "nicht vergessen" | Auswahlfrage: Task, Notiz, Beides |
| "merk dir" / "remember" | → Memory, NICHT ClickUp |

Goldene Regel und die Tabelle Notizen vs. Tasks: `SKILL.md`, Abschnitte „Automationspolitik (Kurzform)“ und „Notizen
vs. Tasks (Trigger-Disambiguierung)“.

---

## Integration mit anderen Skills

### code-erstellen
Nach Commit: Auswahlfrage: "Passt zu <PRÄFIX>-NNN. `tracker done`?" → Ja / Nein / Anderer Task
Wenn ja → Commit-Hash direkt aus der Session (schon bekannt) + Custom Fields befüllen + aktuellen Chat als "Chat erledigt" (nur mit Chat-Feldern, `chat-url-handling.md`).

### chat-wechsel
Am Chat-Ende: Batch-Abschluss + Übergabe.
Schreibt die aktuelle Chat-URL in den Übergabe-Prompt, damit im nächsten Chat sofort verfügbar.

### doc-pflege
Nach Doc-Update: Auswahlfrage: "Doc-Task <PRÄFIX>-NNN erledigt. `tracker done`?" → Ja / Nein
Gleiches Feld-Schema (laut Tracker-Config) wie bei Code-Tasks.

---

## VERBOTEN

- ClickUp-Calls in anderen Skills duplizieren
- Unteraufgaben ohne NN.NN-Nummerierung im Titel
- Sub-Nummern nachnummerieren wenn Lücken entstehen
- Tasks ohne Dedup-Prüfung erstellen
- Meilensteine dynamisch erstellen
- Nummern wiederverwenden
- Hauptaufgabe automatisch schließen wenn Unteraufgaben done
- **`tracker done` ohne Versuch, Custom Fields zu befüllen** (mindestens Erledigt-Datum + Chat erledigt, soweit das Projekt die Felder hat)
- **`tracker neu` ohne Chat erstellt URL** (nur bei Projekten mit Chat-Feldern und in Umgebungen mit Chat-Suche; außer User verweigert)
- **`tracker neu` ohne Typ** (außer Typ ist partout nicht ermittelbar)
- Relationships als Freitext statt ClickUp-Dependency nutzen
- Description ohne Template bei Standard-Tasks (Meta-Tasks dürfen verkürzen)
- **Stale-Check-Ergebnis automatisch aus Memory entfernen** ohne Auswahlfrage Bestätigung
- **Stale-Check bei jedem Chat-Turn wiederholen** — nur einmal beim Chat-Start ausführen

### Projekt-Config

Skills lesen projekt-spezifische Daten aus der Tracker-Config des Projekts (Skill-Profil → Tracker → Config).
VERBOTEN ist jede Form von Hartkodierung oder Fallback-Weglassung:

- **Modul-Kürzel oder Präfix raten** wenn die Projektkennung fehlt — stattdessen Auswahlfrage nach „Fehlende Werte“ (`SKILL.md`, Abschnitt „Voraussetzung: Skill-Profil“)
- **Projekt-Config-Dateipfade raten** — der Pfad steht im Skill-Profil (Tracker → Config), niemals davon abweichen
- **Fallback-Frage weglassen** wenn die Projektkennung (Skill-Profil bzw. Memory) fehlt — Skill MUSS aktiv nach dem aktiven Projekt fragen, nicht still rumraten
- **Tracker-Config ohne Lesen verwenden** — zuerst prüfen dass die Datei existiert, dann ihren Inhalt laden, erst dann verwenden
- **Projektwerte (Listen, Kürzel, Meilensteine, IDs) inline im Skill einbauen** — Beispiele stehen nur in `beispiele.md`, die Werte nur in der Tracker-Config
- **Status-Werte `done` oder `complete` hartkodieren** statt aus dem Statusmodell der Tracker-Config zu lesen

### Verbote je Thema

| Thema | Wo |
|-------|-----|
| Kern-Verbote (automatisch anlegen/abschließen, Titel, Status-Schreibweise, Option-IDs, Chat-URLs, Quittung, Prosa-Fragen, Präfix, Werkzeugsuche) | `SKILL.md`, Abschnitt „Kern-VERBOTEN (Kurzliste)“ |
| Commit-Disziplin (ein Task = ein Commit, Zero-Change, Version, WANN vs. WIE) | `complete-task.md`, Abschnitt „Commit-Disziplin: ein Task = ein Commit“ |
| Automatischer Nachlauf nach tracker done | `complete-task.md`, Abschnitt „Automatischer Nachlauf nach tracker done“ (VERBOTEN) |
| Review-Workflow (Scope-Check) | `review-workflow.md`, Abschnitt „VERBOTEN“ |
| Auto-Nummerierung für Skill-Issues | `issue-task.md`, Abschnitt „VERBOTEN“ |
| Batch (≥2 Task-Operationen in einer Antwort) | `batch-protocol.md`, Abschnitt „VERBOTEN (Batch-spezifisch)“ |
| Referenz-Anker in Folge-Antworten | `batch-protocol.md`, Abschnitt „Referenz-Anker in Folge-Antworten (PFLICHT)“ |
| Start | `start-task.md`, Abschnitt „VERBOTEN“ |
