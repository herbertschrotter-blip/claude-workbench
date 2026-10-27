# ClickUp-Integration (vor Übergabeprompt)

Gilt in beiden Umgebungen vor dem Handover-Prompt (`SKILL.md`, Abschnitte „ABLAUF IN CLAUDE CODE“ und „Ablauf im
Cowork-Chat“). Beispielwerte (BPM, Heidi): [beispiele.md](beispiele.md), Abschnitt „ClickUp-Abgleich“.

## Schritt 1: Offene Tasks laden

1. Space/Listen-ID und Präfix aus der **Tracker-Config** (Claude Code: Skill-Profil der CLAUDE.md → Tracker → Config) bzw. dem Memory-Eintrag `[CLICKUP]` (Cowork) lesen
2. `clickup_filter_tasks(list_ids/space_ids: [...], statuses: <offene Status laut Statusmodell der Tracker-Config>)` – read-only, über den tracker-Skill
3. Tasks gruppieren: mehrere Listen → nach Liste; eine Liste → nach Status (Status laut Statusmodell der Tracker-Config)

## Schritt 2: Chat-Verlauf scannen

Chat scannen auf:
- Tasks die bearbeitet aber nicht als Done markiert wurden
- Neue Probleme die aufgetaucht aber nicht erfasst sind
- NUR nach klaren Mustern: `TODO:`, `offen:`, `neuer punkt:`, `neue aufgabe:`,
  `später:`, klare Problemformulierungen mit Handlungsbezug
- NICHT jede Erwähnung eines Problems als neuen Task interpretieren

## Schritt 3: Batch-Abschluss (Auswahlfrage!)

Strukturierte Übersicht im Chat zeigen:

```
### ClickUp Tracker — Batch-Abschluss

**Im Chat erledigt — als Done markieren?**
- <PRÄFIX>-NNN | <Kurztitel>
- <PRÄFIX>-NNN | <Kurztitel>

**Im Chat neu erkannt — Task anlegen?**
- <Liste> — <neues Problem aus diesem Chat>
- <Liste> — <neuer Doc-Punkt>

**Weiterhin offen laut ClickUp:**
<Liste oder Status> (<Anzahl>):
- [<Priority>] [<Meilenstein>] <PRÄFIX>-NNN | <Kurztitel>
...
```

Dann **zwei Auswahlfragen** (multiSelect):

**Erste Auswahlfrage — Done-Markierungen** (Mehrfachauswahl): „Welche Tasks als Done markieren?“; Optionen: je
erledigtem Task `<PRÄFIX>-NNN | <Kurztitel>`, dazu „Keine“.

**Zweite Auswahlfrage — Neue Tasks** (Mehrfachauswahl): „Welche neuen Tasks anlegen?“; Optionen: je erkanntem Punkt
`<Liste> — <Beschreibung>`, dazu „Keine“.

Mehr als vier Optionen auf mehrere Fragen verteilen (Grenze des Frage-Werkzeugs).

## Schritt 4: Nach Bestätigung ausführen

- Done-Tasks: `tracker done` pro ausgewähltem Task (Status laut Übergängen der Tracker-Config; Commit-Felder bzw. Kommentar)
- Neue Tasks: `tracker neu` pro ausgewähltem Task (Fragemodus per Auswahlfrage im tracker-Skill, Präfix des Projekts)
- Cowork: Memory `[CLICKUP]` Eintrag aktualisieren: `Letzte Sync: Teil <N>`; Claude Code: `Next` in der Tracker-Config, wenn Tasks angelegt wurden

## ClickUp nicht erreichbar?

Per Auswahlfrage:
```
Frage: "ClickUp nicht erreichbar. Wie weiter?"
Optionen: "Trotzdem Prompt erstellen", "Retry", "Abbrechen"
```

Bei "Trotzdem Prompt erstellen": Hinweis in Prompt einfügen, Übergabe aus Chat-Verlauf.
