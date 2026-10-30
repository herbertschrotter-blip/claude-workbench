---
name: tracker
description: >
  Führt konkrete ClickUp-Aktionen für Projekt-Tasks und Skill-Issues aus, z.B.
  "tracker neu", "tracker issue", "tracker done", "tracker update",
  "tracker status", "tracker suche", "tracker next", "tracker split",
  "tracker relate" und "tracker field". Use when users want to anlegen,
  erstellen, eintragen, melden, dokumentieren, abschließen, aktualisieren,
  or update a ClickUp task or issue — including Projekt-Tasks, Skill-Issues,
  Bug-Reports, neue Aufgaben, offene Punkte, Task-Splits, Dependencies,
  oder Status-Abfragen. Triggers also on "issue erstellen", "task anlegen",
  "ClickUp-Eintrag", "Skill-Issue melden". Do not trigger for general talk
  about priorities, brainstorming, notes without concrete tracker command,
  or code/doc work without explicit task action.
---

# Tracker Skill — ClickUp Offene-Punkte-Verwaltung

## Zweck

Einzige standardisierte Schreibschnittstelle für den ClickUp-Task-Tracker.
Das Schema ist in jedem Projekt gleich: Titel `<PRÄFIX>-NNN | <KÜRZEL> | <Kurztitel>`,
Chat-Anker `[<PRÄFIX>-ANCHOR-<task-id>]`, dieselben Custom Fields, dasselbe
Description-Template. **Der Präfix wird pro Projekt festgelegt** und steht mit
Listen, Kürzeln, Zähler und Feld-IDs in der Tracker-Config des Projekts
(Abschnitt „Voraussetzung: Skill-Profil“). Der Präfix ist immer der des aktiven
Projekts; Beispielwerte zweier Projekte stehen nur in `references/beispiele.md`.

Die operativen Details sind in `references/` ausgelagert. Diese Hauptdatei
ist nur der Routing-Einstieg — je nach Kommando die passende Referenz laden.

---

## Voraussetzung: Skill-Profil

Die Werte kommen aus dem Skill-Profil der `CLAUDE.md` im Repo (`docs/skill-profile-v1.md` im Skill-Repo):

| Feld | Wofür |
|------|-------|
| `Tracker.Provider` | `clickup`; bei `none` führt das Projekt keinen Tracker – das melden, nichts anlegen |
| `Tracker.Config` | die Tracker-Config, meist `.claude/skill-config/tracker.md`, sonst `ref:CLAUDE.md#<Abschnitt>` |
| `Branch-Policy`, `Commit.Push-Policy` | Branch und Push-Zeile im Nachlauf nach `tracker done` (Grundsätze) |

Aus der Tracker-Config die benötigten Abschnitte lesen (Gliederung nach `docs/skill-profile-v1.md`, Abschnitt
„Configs unter `.claude/skill-config/`“): Nummernschema und nächste freie Nummer · Listen und Routing ·
Statusmodell · Felder und Option-IDs · Titel- und Beschreibungsformat · Quittungsformat · Sonderfälle.

1. **Skill-Profil v1** (Abschnitt `## Skill-Profil`, Bereich `### Tracker`).
2. **Rückfall:** der ältere Abschnitt `## Tracker-Profil` der CLAUDE.md (dort auch die Zeile „Nächste freie Nummer“).
3. **Fehlt beides** (kein Bereich Tracker, Config auf `fehlt`, Datei existiert nicht): Auswahlfrage nach der
   Profil-Regel „Fehlende Werte“ – Profil ergänzen / Wert einmalig nennen / Abbrechen. *Profil ergänzen* → Claude
   schlägt `.claude/skill-config/tracker.md` mit den Werten aus ClickUp vor; angelegt wird erst nach Zustimmung.
   *Wert einmalig nennen* → Universell-Modus: Claude fragt die konkreten Werte ab, die gerade gebraucht werden. Nie
   raten.

Im Cowork-Chat kommen Projektkennung, Zähler und Listen aus dem Memory: `references/cowork.md`.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist –,
  dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung (anklickbare Optionen). Wo in Skill oder references
  „Auswahlfrage“ steht, ist dieses Werkzeug gemeint. Mehrere Fragen in einem Aufruf sind erlaubt (max 3). Zu lange
  Options-Listen (>4) in Multi-Aufrufe aufteilen.

  Prosa nur bei einer offenen Frage ohne feste Optionen (z.B. "Welche Datei ist betroffen?"), wenn Freitext-Input nötig
  ist oder wenn der Nutzer gerade eine klare Präferenz signalisiert hat.
- **Branch** (Push-Zeile im Nachlauf nach `tracker done`) nach der Branch-Policy im Skill-Profil der `CLAUDE.md`:
  `current` → der aktuelle Branch aus der Shell (`git branch --show-current`); `fixed:<branch>` → der aktuelle muss
  dieser sein, sonst Auswahlfrage (wechseln / abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: der aktuelle Branch aus der Shell, wie der
  Commit-Hash; ohne Shell zusammen mit dem Commit-Hash erfragen. NIE automatisch einen Branch annehmen, auch nicht
  `main`.
- **Push** nach der Push-Policy im Skill-Profil der `CLAUDE.md`; danach richtet sich die Push-Zeile der
  Zwischenstand-Tabelle im Nachlauf nach `tracker done`:
  - `user-only`: Claude pusht nie – ⏳ Nutzer
  - `allowed`: Claude pusht nur auf Anweisung des Nutzers – bis dahin ⏳ offen
  - `required-after-commit`: Claude pusht nach jedem Commit ohne Rückfrage – ✅; fehlt der Push noch, jetzt pushen
  - `required-at-session-end`: Claude pusht am Ende der Sitzung – bis dahin ⏳ Sitzungsende

  Ohne Push-Policy (kein Skill-Profil): Auswahlfrage (pushen / nicht pushen); bei „nicht pushen“ ⏳ User.

---

## Vorrang / Delegation an andere Skills

**tracker ist für explizite ClickUp-Task-Aktionen. Wenn die Hauptabsicht
Code-Arbeit, Doku oder andere inhaltliche Tätigkeit ist, NICHT hier
weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (auch wenn ein Task-Bezug besteht) | **code-erstellen** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| Commit-Befehl, Commit-Message, Version-Bump | **git-commit-helper** |
| Doku schreiben, ADR, Konzept, Frontmatter-Pflege | **doc-pflege** |
| Konsistenzprüfung Code ↔ Docs | **audit** |

Nur wenn die Hauptabsicht **eine konkrete ClickUp-Task-Aktion** ist
(`tracker neu`, `tracker done`, `tracker update`, `tracker status`,
`tracker suche`, Issue anlegen, Scope-Check, Anker setzen),
bleibt tracker zuständig.

**Wichtig:** tracker wird NICHT automatisch ausgelöst durch Code-Commits
oder Doc-Änderungen. Andere Skills (code-erstellen, doc-pflege) rufen
tracker nur aktiv per Auswahlfrage auf ("Passt zu <Task>.
tracker done?"). Die User-Bestätigung ist Pflicht. Details siehe
Abschnitt "Integration mit anderen Skills".

---

## Befehl → Reference

| Befehl / Fall | Reference | Inhalt |
|---------------|-----------|--------|
| `tracker neu: <Beschreibung>` | `references/create-task.md` | Ablauf, Fragemodus, Description-Template |
| `tracker issue <skill>: <Titel>` | `references/issue-task.md` | Skill-Issue-Listen-Routing, Issue-ID-Nummerierung, Felder des Issue-Scopes |
| `tracker start: <Task-ID>` | `references/start-task.md` | Ablauf, Parent-Kaskade, implizite Trigger mit Task-ID, Fokus-Entscheidung |
| `tracker done: <Task-ID>` | `references/complete-task.md` | Ablauf, Commit-Ermittlung, Commit-Disziplin (ein Task = ein Commit), automatischer Nachlauf, Lieferung nach einem Skill-Issue |
| `tracker update: <Task-ID> → <Änderung>`, `tracker field: <Task-ID> <Feld> <Wert>` | `references/update-task.md` | gezielte Änderungen |
| `tracker status`, `tracker next`, `tracker suche: <Stichwort>`, `tracker listen` | `references/search-and-status.md` | Lese-Operationen |
| `tracker split: <Task-ID>`, `tracker relate: <A> <Bez> <B>` | `references/split-and-relations.md` | Unteraufgaben-Regeln, Dependency-Typen |
| ≥2 Task-Operationen in einer Antwort; Referenz-Anker in Folge-Antworten | `references/batch-protocol.md` | Pro-Task-Quittung, Batch-Ansage, Batch-Audit, Subtask/Parent-Regeln, Referenz-Anker |
| vor `tracker done` / `tracker start` / Fokus-Wechsel | `references/review-workflow.md` | 4-Punkte-Scope-Check |
| `anker setzen: <text>`; Chat-Anker | `references/anker-system.md` | Anker-Format; im Cowork-Chat Registry `[ANKER-LIVE]`, TEMP-ID, Stale-Check |
| Chat erstellt / erledigt, Chat-Start | `references/chat-url-handling.md` | Chat-URLs ermitteln (nur mit Chat-Feldern und Chat-Suche) |
| Feldwerte, Nummerierung, Titel, Status | `references/clickup-fields.md` | Custom-Field-Regeln, Nummerierung, Titel-Format, Meilensteine, Priority, Statusmodell |
| ClickUp-Werkzeuge | `references/clickup-tools.md` | Lade-Pattern, Tool-Inventar, Befehl→Tool-Mapping |
| Verbote, Automationspolitik | `references/anti-patterns.md` | Automationspolitik, Integration, VERBOTEN-Liste |
| Cowork-Chat | `references/cowork.md` | Memory-Einträge, Werkzeugsuche, Shell, `[ANKER-LIVE]` im Ablauf, Artifact-Lieferung |
| Beispiele | `references/beispiele.md` | Werte und Abläufe aus zwei Projekten |

`<Task-ID>` = `<PRÄFIX>-NNN` nach der Tracker-Config, eine Issue-ID (`tracker-NNN`) oder die ClickUp-Task-ID.

---

## 🚨 Kernregel: Pro-Task-Quittung (Format-Zwang)

Nach **jedem** Anlegen oder Statuswechsel einer Aufgabe
MUSS im selben Antwort-Block eine Quittungszeile stehen:

```
✅ <PRÄFIX>-NNN — [<PRÄFIX>-ANCHOR-<task-id>] — <typ>: <kurz>
```

Sollte ein Projekt laut Tracker-Config keine Chat-Anker führen, entfällt der
Anker-Teil: `✅ <PRÄFIX>-NNN — <Aktion> — <ClickUp-Link>`.

Die Quittung ist Bestätigung + Body-Anker + Audit-Spur in einem Format.
Keine Quittung am Ende gesammelt. Keine Tabellen statt Quittungen.

**Zusätzlich im selben Tool-Call-Block:** die Anker-Felder `Chat-Anker erstellt`
bzw. `Chat-Anker erledigt` setzen — IDs aus der Tracker-Config,
nur wenn das Projekt diese Felder hat — nicht später nachtragen.

Bei ≥2 Task-Operationen in derselben Antwort greift das **Batch-Protokoll**:
Batch-Ansage vor Beginn, Pro-Task-Zyklus, Batch-Audit am Ende.
Vollständige Spec: `references/batch-protocol.md`.

---

## 🚨 Kernregel: Referenz-Anker in Folge-Antworten

Anker-Präfix = Projekt-Präfix aus der Tracker-Config. Sollte ein Projekt keine
Chat-Anker führen, entfällt die Regel; der Task wird dann mit `<PRÄFIX>-NNN` und ClickUp-Link genannt.

**Bei JEDER Folge-Antwort die einen bereits existierenden Task inhaltlich
betrifft (ohne Tool-Call), MUSS oben ein Referenz-Anker stehen:**

```
Betroffene Tasks in dieser Antwort: [<PRÄFIX>-ANCHOR-<task-id>] <n>.
```

**Gilt auch wenn der Task nicht via `tracker neu`/`tracker done` angefasst
wurde, sondern nur gelesen, besprochen oder umgesetzt wird.**

**Wenn in derselben Antwort eine Pro-Task-Quittung steht** (die bereits
den Anker inline enthält), entfällt der Referenz-Anker oben für diesen
Task.

Wann Pflicht und wann nicht, mit Beispielen: `references/batch-protocol.md`, Abschnitt „Referenz-Anker in
Folge-Antworten (PFLICHT)“.

---

## 🚨 Kernregel: Review-Workflow vor Task-Übergang

**Vor JEDEM `tracker done` / `tracker start` (neu oder Wechsel) / Fokus-Wechsel
im Dialog MUSS ein 4-Punkte-Scope-Check durchgeführt werden:**

1. **Aktueller Task** — Description ändert sich durch neue Erkenntnisse?
2. **Parent-Task** — Scope/DoD betroffen?
3. **Sibling-Subtasks** im selben Parent — betroffen?
4. **Verweisende offene Tasks** (Related/Links/Dependencies) — betroffen?

Gefundene Änderungen werden in ClickUp umgesetzt **BEVOR** der Task-Übergang
passiert. Danach ggf. neue Abarbeitungs-Reihenfolge per Auswahlfrage
vorschlagen.

**Trigger:**
- Bevor `tracker done` ausgeführt wird
- Bevor `tracker start` auf neuen oder bereits gestarteten Task
- Nach expliziter User-Bestätigung `"so machen wir's"` / `"das merken wir uns so"`

**Check ENTFÄLLT bei:** reinen Pflege-Updates ohne Scope-Änderung, Zero-Change-Tasks,
explizitem User-Skip `"Scope-Check überspringen"`.

Vollständige Spec mit API-Calls und Beispiel-Ablauf: `references/review-workflow.md`.

---

## 🚨 Kernregel: Automatischer Nachlauf nach tracker done

**Nach jedem erfolgreichen `tracker done` MUSS Claude automatisch weiterführen —
niemals passiv auf User-Input warten.**

4 Schritte:

1. **Commit-Hash in der Shell der Umgebung holen** (`git log -1 --format='%h %s'`) — nicht vom User anfordern, wenn eine Shell verfügbar ist
2. **Custom Fields setzen** (Commit ID, Erledigt-Datum, Chat-Anker erledigt) — nur wenn das Projekt die Felder hat (`clickup-fields.md`); sonst Kommentar mit Version und Commit-Hash am Task
3. **Zwischenstand-Tabelle im Chat** (Task / Commit-Hash / Status / Push-Stand nach den Grundsätzen „Branch“ und „Push“)
4. **Folgeoptionen als Auswahlfrage** — niemals Prosa-Frage, niemals still warten

**Ausnahmen:** Zero-Change-Tasks (Schritt 1 entfällt), Batches (Schritte 3-4 nur einmal am Batch-Ende), keine Shell verfügbar (Schritt 1 entfällt → Prosa-Frage nach Hash).

Vollständige Spec mit Beispiel-Ablauf: `references/complete-task.md` Abschnitt "Automatischer Nachlauf nach tracker done".

---

## 🚨 Kernregel: Projektwerte aus der Tracker-Config

**Alle projekt-spezifischen Daten (Präfix, nächste freie Nummer, Listen-IDs,
Custom-Field-IDs, Option-IDs, Modul-Kürzel, Meilenstein-Tags, Status-Werte-Matrix)
werden zur Laufzeit aus der Tracker-Config des Projekts gelesen — NICHT
hartkodiert im Skill.** Wo die Config steht und was bei fehlenden Werten
passiert: Abschnitt „Voraussetzung: Skill-Profil“. Universelle Regel:
`docs/skill-profile-v1.md` (im Skill-Repo-Root).

---

## Notizen vs. Tasks (Trigger-Disambiguierung)

| Trigger | Aktion |
|---------|--------|
| "neue aufgabe", "neuer punkt", "tracker neu" | → Task in ClickUp |
| "merk dir", "remember" | → Memory (KEIN ClickUp) |
| "notiz", "nicht vergessen" | → Auswahlfrage: Task, Notiz, Beides |

---

## Memory-Eskalation

Memory-Einträge (Rubriken `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`,
`[REVIEW-PENDING]`) werden **nie automatisch** zu ClickUp-Tasks.

Wenn der Nutzer einen wiederholt auftauchenden Memory-Eintrag zu einem
echten Task eskalieren will:

1. Memory-Eintrag als Kontext in Task-Description übernehmen
2. Per `tracker neu` einen ClickUp-Task anlegen (normaler Ablauf)
3. Nach User-Bestätigung: Memory-Eintrag entfernen (Claude Code: Datei im Memory-Ordner löschen und Index-Zeile
   entfernen; Cowork-Chat: `references/cowork.md`) — **nie stillschweigend, nie automatisch**

**Memory ≠ Tracker-Light.** Memory bleibt nur offene Merker, Fragen,
Verifikationen. Substantielle Arbeit gehört in ClickUp.

Abgrenzung:
- **Ohne User-Anweisung:** Memory bleibt Memory, auch bei wiederholtem
  Handover-Vorkommen
- **Mit User-Anweisung:** Memory → Task via `tracker neu`, dann
  Bestätigung einholen fürs Entfernen

Rubriken-Konvention: `MEMORY-RUBRIKEN.md` im Skill-Repo.

---

## Automationspolitik (Kurzform)

**Goldene Regel:** Explizit → direkt. Alles andere → Auswahlfrage (keine Prosa!).

Vollständige Tabelle in `references/anti-patterns.md`.

---

## ClickUp-Tools (Lade-Pattern)

ClickUp-Werkzeuge sind oft erst nach einer Werkzeugsuche aufrufbar. Fehlt eines (`Tool '...' not found`), mit dem
**EXAKTEN Tool-Namen** nachladen, nicht mit Umschreibung.

Vollständiges Tool-Inventar, Lade-Pattern je Umgebung + Befehl→Tool-Mapping: `references/clickup-tools.md`.

---

## Integration mit anderen Skills

- **code-erstellen** nach Commit: Auswahlfrage "Passt zu <Task>. `tracker done`?"
- **chat-wechsel** am Ende: Batch-Abschluss + Chat-URL in Übergabeprompt
- **doc-pflege** nach Doc-Update: Auswahlfrage "Doc-Task <Task> erledigt?"

Details in `references/anti-patterns.md`.

---

## Kern-VERBOTEN (Kurzliste)

- Tasks automatisch erstellen aus freiem Chattext
- Tasks automatisch auf Done setzen ohne Trigger
- Titel ohne `<PRÄFIX>-NNN | KÜRZEL` (Hauptaufgaben; Präfix aus der Tracker-Config)
- Projekt-Nummern an Unteraufgaben vergeben
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER Auswahlfrage
- Status mit Grossbuchstaben setzen — IMMER klein (`open`/`in progress`/`done`)
- Custom Field Option-IDs raten — immer aus der Tracker-Config kopieren
- Chat-URLs raten oder erfinden — bei Unsicherheit Auswahlfrage oder leer lassen
- **Pro-Task-Quittung weglassen** nach `create`/`update` — Format-Zwang ist Pflicht
- **Custom Fields (Chat-Anker) erst am Ende eines Batches sammeln** — pro Task setzen
- **em-dash `—` in Custom-Field-Values** verwenden (nur ASCII `-`, em-dash löst ClickUp-Fehler aus)
- **Batch-Audit weglassen** (`N/N Body-Anker ✅ | N/N Custom Fields ✅`)
- **Impliziter Start-Trigger OHNE Task-ID** im Satz — "los geht's" / "fangen wir an" ohne Projekt-Nummer triggert NICHT
- **Inhaltliche Arbeit starten BEVOR `tracker start` ausgeführt wurde** — Task muss vorher auf `in progress`
- **Referenz-Anker in Folge-Antworten weglassen** — wenn eine Antwort einen Task inhaltlich betrifft und keine Quittung enthält, MUSS oben `Betroffene Tasks in dieser Antwort: [<PRÄFIX>-ANCHOR-<id>] <name>.` stehen. **Gilt auch bei Tasks die nur gelesen/bearbeitet wurden, ohne `tracker neu`/`tracker done` auszulösen**
- **Projekt-Daten hartkodieren** im Skill (Listen-IDs, Custom-Field-IDs, Option-IDs, Modul-Kürzel) — alles aus der Tracker-Config lesen
- **Projektkennung oder Präfix annehmen** — Projektkennung (Skill-Profil bzw. Memory) lesen und den tatsächlichen Wert verwenden; **Präfix nie raten**, er steht in der Tracker-Config
- **Commits sammeln statt pro Task** — jeder abgeschlossene (Sub-)Task bekommt sofort einen eigenen Commit (Details: `references/complete-task.md`)
- **Review-Workflow-Check vor Task-Übergang weglassen** — 4-Punkte-Check (aktueller Task + Parent + Siblings + verweisende offene Tasks) ist Pflicht vor `tracker done`, `tracker start` und Fokus-Wechsel (Details: `references/review-workflow.md`)
- **Nach `tracker done` passiv warten statt Nachlauf ausführen** — Hash in der Shell holen + Zwischenstand-Tabelle + Folgeoptionen als Auswahlfrage sind Pflicht (Details: `references/complete-task.md` Abschnitt "Automatischer Nachlauf")
- **Issue-IDs manuell vergeben lassen bei `tracker issue`** — Auto-Nummerierung ist Pflicht, inkl. aller erledigten Issues + Unique-Check (Details: `references/issue-task.md` Abschnitt „Issue-ID automatisch ermitteln“)
- **Memory-Einträge automatisch zu Tasks eskalieren** — nur auf ausdrückliche Anweisung des Nutzers `tracker neu` aus Memory ableiten, nie ungefragt. Entfernen des Memory-Eintrags erst nach Bestätigung (siehe Memory-Eskalation)
- **Werkzeugsuche mit Umschreibung statt exaktem Tool-Namen** wenn ein ClickUp-Tool nicht geladen ist — das liefert Müll-Treffer und kostet Zeit (Beispiele: `references/clickup-tools.md`)
- **Werkzeugnamen oder Umgebung fest annehmen** — der Skill beschreibt die Handlung; Claude nimmt Shell, Auswahlfrage und Projektkennung der jeweiligen Umgebung
- **Präfix oder IDs eines anderen Projekts annehmen** — Präfix, Kürzel, Listen- und Feld-IDs immer aus der Tracker-Config lesen; das Schema selbst (Titel, Anker, Felder, Template) gilt in jedem Projekt gleich
- **Code, Mockup oder Doku zu einem gestarteten Task unter tracker selbst schreiben** — nach `tracker start` (auch „mach <PRÄFIX>-NNN“, „weiter mit <PRÄFIX>-NNN“) den zuständigen Skill laden, bevor die erste Datei geändert wird: Code → code-erstellen, Mockup → mockup-erstellen, Doku → doc-pflege; tracker setzt nur den Status (Details: `references/start-task.md`)

**Vollständige VERBOTEN-Liste:** `references/anti-patterns.md`.
