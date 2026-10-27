# code-erstellen im Cowork-Chat

Gilt nur im Cowork-Chat. In Claude Code gelten die Abschnitte in `../SKILL.md`; dort ersetzt der Abschnitt
„Aufgaben-Stichwörter“ den Auto-Anker.

## Inhalt

- Profil und Dateien lesen
- Auto-Anker bei Aufgaben-Stichwörtern
- Tests und Selbst-Review im Cowork-Chat
- Ausgabeformat
- Auslieferung
- VERBOTEN im Cowork-Chat

## Profil und Dateien lesen

- Das Skill-Profil der `CLAUDE.md` (bzw. das ältere `## Code-Profil`) per Desktop Commander lesen; Claude Code liest es
  automatisch.
- Wenn dieser Skill DC-Operationen auslöst (z.B. Code-Dateien lesen, Entry Points prüfen), das Arbeitsverzeichnis nach
  **cc-steuerung**, Abschnitt „Arbeitsverzeichnis“, ermitteln.
- Branch: die Shell ist hier die PowerShell über DC (`git branch --show-current`).

## Auto-Anker bei Aufgaben-Stichwörtern

**Zweck:** Wenn im Chat ein Thema auftaucht das offensichtlich ein späterer Task wird (aber aktuell noch kein Task
existiert), setzt dieser Skill automatisch einen temp-Anker. Das stellt sicher, dass die Diskussionsstelle später via
`conversation_search` wiederfindbar ist.

**Gilt nur im Cowork-Chat.** In Claude Code gibt es weder Chat-Suche noch `[ANKER-LIVE]`-Memory; dort gilt der Abschnitt
„Aufgaben-Stichwörter“ in `../SKILL.md`. Anker-Präfix = Projekt-Präfix aus der Tracker-Config (`Tracker.Config`;
Beispiele: [beispiele.md](beispiele.md#aufgaben-stichwörter)).

Anker-Format + Memory-Registry (Master-Spec): `skills/tracker/references/anker-system.md`, Abschnitte „Anker-Format im
Chat-Body“ und „Memory-Registry `[ANKER-LIVE]`“.

### Aufgaben-Stichwörter (Trigger für Auto-Anker)

Claude erkennt folgende Formulierungen als klares Task-Signal:

- "das müssen wir noch bauen"
- "später implementieren"
- "ins backlog"
- "backlog-wert"
- "da brauchen wir einen task"
- "sollten wir im task tracken"
- "muss noch gemacht werden"
- "als task anlegen"

Wenn User diese Keywords nutzt UND das Thema noch keinen offenen Task hat → Auto-Anker setzen.

### Ablauf

1. Keyword erkannt UND Kontext ist klar (Thema identifizierbar)
2. TEMP-ID generieren:
   - Primär in der Shell (DC PowerShell, siehe `skills/tracker/references/anker-system.md`, Abschnitt „TEMP-ID
     Generierung“)
   - Fallback: Claude erzeugt `TEMP-<yyMMddHHmm><3 Zufallsbuchstaben>`
3. Anker-Zeile im Chat-Response einfügen (möglichst am Anfang des relevanten Abschnitts):
   ```
   [<PRÄFIX>-ANCHOR-TEMP-<id>] — Idee: <kurzbeschreibung max 60 Zeichen>
   ```
4. Memory aktualisieren:
   ```
   memory_user_edits(command: "add", control: "[ANKER-LIVE] TEMP-<id>|offen|<ISO-timestamp>|<kurzbeschreibung>")
   ```
5. Kurzer Hinweis im Chat: "Anker gesetzt — wird bei `tracker neu` mit Task-ID verknüpft."

### Wann KEIN Auto-Anker

- User spricht nur über bestehende Tasks (nicht Task-würdiger Neu-Content)
- Thema ist zu vage für eine 60-Zeichen-Kurzbeschreibung
- Innerhalb 24h existiert bereits ein Anker mit ähnlichem Thema (Duplikat-Check via `[ANKER-LIVE]`)
- User sagt explizit "kein Task daraus" o.ä.
- Mehr als 10 Anker bereits in `[ANKER-LIVE]` — User sollte erst aufräumen

**Im Zweifel: KEIN Anker.** Lieber ein paar Anker verpassen als den Chat zuspammen.

### Anti-Pattern

- Anker mitten in Code-Blöcken einfügen
- Mehrere Anker direkt hintereinander für dasselbe Thema
- Anker setzen für Dinge die der User nur erwähnt ohne Handlungsabsicht
- Anker mit generischen Beschreibungen wie "Feature X" oder "TODO"

## Tests und Selbst-Review im Cowork-Chat

- **Tests:** Testbefehl im Commit-Block mitliefern; der User führt aus und meldet das Ergebnis.
- **Selbst-Review:** den Diff selbst lesen, mit denselben vier Fragen wie in `../SKILL.md`, Abschnitt „Selbst-Review“
  (Fehler, Randfälle, Sicherheit, unnötige Komplexität).

## Ausgabeformat

Claude Code ändert die Dateien direkt; im Cowork-Chat gilt:

- Neue Datei → komplett
- < 600 Zeilen UND > 30% geändert → komplett
- ≥ 600 Zeilen → SUCHE/ERSETZE
- Stack-Besonderheiten (z.B. XAML → Download) laut Stack-Referenz „Ausgabe“

**Bei Mehrdeutigkeit:** Auswahlfrage mit den möglichen Formaten (Komplette Datei, SUCHE/ERSETZE, Download).

## Auslieferung

Im Cowork-Chat liefert Claude die Befehle aus `Code.Auslieferung`; der User führt sie aus. Prüfreihenfolge und
Sichtprüfung wie in `../SKILL.md`, Abschnitt „Auslieferung“.

## VERBOTEN im Cowork-Chat

- **Auto-Anker bei vagen Themen setzen** — lieber keinen Anker als einen unscharfen
- **Anker mit generischen Beschreibungen** ("Feature X", "TODO") — immer konkret benennen
- **Anker setzen ohne Memory-Update** — Chat-Zeile UND `[ANKER-LIVE]`-Eintrag gehören zusammen
