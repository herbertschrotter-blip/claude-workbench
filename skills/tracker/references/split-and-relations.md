# tracker split / tracker relate — Unteraufgaben + Beziehungen

Ablauf für Task-Aufteilung und Task-Beziehungen. Beispiele: `beispiele.md`, Abschnitt „tracker split / relate“.

## Inhalt

- Unteraufgaben (wann, wann nicht, erstellen, Hauptaufgabe schließen)
- Kommando `tracker split: <Task-ID>`
- Relationships (ClickUp-Dependencies)
- Kommando `tracker relate: <Task-A> <Beziehung> <Task-B>`

---

## Unteraufgaben

### Wann Unteraufgaben erstellen?

| Situation | Unteraufgaben? |
|-----------|---------------|
| Task ist in 1 Chat erledigt | Nein |
| Task hat 3+ klar trennbare Schritte | Ja |
| Task läuft über 3+ Chats | Ja |
| Modul-Platzhalter ("Dashboard implementieren") | Ja, wenn Modul gestartet wird |

### Wann KEINE Unteraufgaben?

- Task ist trivial (1-2 Stunden Arbeit)
- Schritte sind nicht klar trennbar
- Nur der Vollständigkeit halber

### Unteraufgaben erstellen

Via `clickup_create_task` mit `parent` Parameter:

```
clickup_create_task(
  list_id: "<gleiche Liste wie Parent>",
  name: "<Parent-NNN>.<Sub-NN> — <Beschreibung>",
  parent: "<Parent-Task-ID>",
  priority: "<von Parent erben oder eigene>",
  custom_fields: [
    {"id": "<Typ-ID>", "value": "<Typ-Option-ID>"},
    // Aufwand/Komponente je nach Bedarf
  ]
)
```

Custom Fields bei Unteraufgaben sind optional, aber Typ + Aufwand werden
empfohlen wenn bekannt.

### Hauptaufgabe automatisch Done?

Wenn alle Unteraufgaben Done → per Auswahlfrage fragen:
"Alle Unteraufgaben von <PRÄFIX>-NNN erledigt. Hauptaufgabe auch schließen?"
Optionen: Ja / Nein

NICHT automatisch schließen.

---

## Kommando `tracker split: <Task-ID>`

Hauptaufgabe in Unteraufgaben aufteilen. Task-ID im Format `<PRÄFIX>-NNN` des Projekts
(Präfix aus der Tracker-Config) oder Issue-ID (`tracker-NNN`).

1. Task laden: `clickup_get_task(task_id, subtasks: true)`
2. Claude analysiert den Task und schlägt Unteraufgaben vor
3. Per Auswahlfrage bestätigen lassen:
   - "Diese X Unteraufgaben anlegen?" → Ja / Anders aufteilen / Abbrechen
4. Wenn "Anders aufteilen": weitere Auswahlfrage Fragen zur Struktur
5. **Bestehende Sub-Nummern ermitteln** (Lücken beachten)
6. Pro Unteraufgabe:
   ```
   clickup_create_task(
     parent: "<task_id>",
     name: "<Parent-NNN>.<Sub-NN> — <Beschreibung>",
     markdown_description: "<verkürztes Template>",
     custom_fields: [Typ + ggf. Aufwand]
   )
   ```
7. Hauptaufgabe auf "in progress" setzen

---

## Relationships (ClickUp-Dependencies)

Task-Beziehungen werden über ClickUp's eigene **Dependency-Funktion** (bzw. für „relates to“ und „duplicates“ über die
Task-Verknüpfung) gepflegt, NICHT als Custom Field oder Freitext in der Description.

### Beziehungstypen

| Typ | Bedeutung | In ClickUp |
|-----|-----------|------------|
| **blocks** | Task A muss fertig sein bevor Task B starten kann | "blocking" |
| **is blocked by** | Umkehrung von blocks | "waiting on" |
| **relates to** | Lose inhaltliche Verbindung | "linked task" |
| **duplicates** | A ist Duplikat von B | "duplicate" |

### API-Aufruf

Für **blocks** und **is blocked by** per `clickup_add_task_dependency`:
```
clickup_add_task_dependency(
  task_id: "<Task A>",
  depends_on: "<Task B>"  // Task A is_blocked_by Task B
  // oder
  dependency_of: "<Task B>"  // Task A blocks Task B
)
```

Für **relates to** und **duplicates** per `clickup_add_task_link` (beidseitige Verknüpfung).

---

## Kommando `tracker relate: <Task-A> <Beziehung> <Task-B>`

Task-Beziehung setzen. Task-IDs im projekt-üblichen Format.

1. Beide Tasks laden via `clickup_search` oder direkte ID
2. Beziehungstyp prüfen:
   - Wenn unklar: Auswahlfrage mit blocks/is blocked by/relates to/duplicates
3. Dependency bzw. Verknüpfung (siehe API-Aufruf) mit korrekter Richtung setzen
4. Bestätigung: "✅ <PRÄFIX>-A blocks <PRÄFIX>-B"

Bei unklarer Richtung: Auswahlfrage mit den 4 Beziehungstypen.
