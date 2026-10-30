---
name: chat-wechsel
description: >
  Erstellt die Übergabe an die nächste Claude-Sitzung: einen vollständigen
  Handover-Prompt mit Stand, Erledigtem, offenen Punkten, nächsten Schritten,
  Entscheidungen und Regeln (aus den Profilen); in Claude Code zusätzlich vorher
  den Sitzungsabschluss im Repo (doc-pflege, Sitzungsabschluss). Use when users want to continue in a new chat or session, ask for
  a session handover, a continuation prompt, or a next-chat summary. Do not trigger for ChatGPT review prompts,
  generic prompt requests, or casual goodbyes like "tschüss" or "gute Nacht".
---

# Chat-Wechsel Skill

## Zweck

Übergabe, wenn eine Sitzung endet und in der nächsten weitergearbeitet wird. Zwei Wege, ein Ziel:

- **Cowork-Chat:** Ein Handover-Prompt im Chat (PROMPT-STRUKTUR: `references/prompt-struktur.md`). Der Chat hat kein
  Repo-Gedächtnis, also trägt der Prompt den Stand.
- **Claude Code:** Erst **doc-pflege, Sitzungsabschluss** – Statusliste/Aufgabenquelle, Befunde,
  Stand-Abschnitt, offene Punkte, Commit + Push nach der Push-Policy –, dann **derselbe vollständige Handover-Prompt** nach
  PROMPT-STRUKTUR. Der Prompt darf den Repo-Stand zusammenfassen, verweist aber für Details auf die Orte aus
  `Doku.Sitzungsabschluss` (z. B. Übergabe-Doc, Bauplan) statt sie zu kopieren. Nennt das Projekt einen Startprompt
  (in der Doku hinter `Doku.Sitzungsabschluss`), steht er als Einstiegszeile **im** Prompt.
  Eine Kurzform (nur Startprompt) gibt es nur, wenn der User sie ausdrücklich verlangt („kurzer Prompt“).

Projektwerte (Präfix, Listen, Commit-Format, Doc-Namen, Testbefehl) kommen aus dem Skill-Profil der CLAUDE.md
(Abschnitt „Voraussetzung: Skill-Profil“). Beispielwerte zweier Projekte: `references/beispiele.md`.

---

## Vorrang / Delegation an andere Skills

**chat-wechsel erzeugt den Handover-Prompt für die NÄCHSTE Claude-Session.
Wenn die Hauptabsicht ein ChatGPT-Review-Prompt oder ein anderer
Prompt-Typ ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Prompt für ChatGPT-Review (zweite Meinung, Cross-LLM-Kritik) | **chatgpt-review** |
| Code schreiben | **code-erstellen** |
| ClickUp-Task-Aktion | **tracker** |
| Doc schreiben | **doc-pflege** |

Nur wenn die Hauptabsicht **ein Handover-Prompt für den nächsten Claude-Chat** ist
("neuer chat", "nächster chat", "übergabe", "session beenden"), bleibt
chat-wechsel zuständig.

**Wichtig:** Beide Skills können im selben Chat nacheinander laufen
(erst ChatGPT-Review abschließen, dann Claude-Handover). Sie triggern
aber nicht gemeinsam auf einen Satz — der User-Intent entscheidet,
welcher zuerst dran ist.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen
  ist –, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Link-Prüfung findet tote Verweise | "Korrigieren", "Mit Warnung übernehmen", "Weglassen" |
  | Claude Code: uncommittete Änderungen beim Abschluss | "Jetzt committen (Sitzungsabschluss)", "Als offen vermerken", "Abbrechen" |
  | Batch-Abschluss: erledigte Tasks | "Alle als Done markieren", "Einzeln wählen", "Keine" |
  | Batch-Abschluss: erledigte Tasks einzeln wählen | multi_select mit allen Task-Namen |
  | Batch-Anlage: neue Tasks aus Chat | "Alle anlegen", "Einzeln wählen", "Keine" |
  | Batch-Anlage: neue Tasks einzeln wählen | multi_select mit allen erkannten Problemen |
  | ClickUp nicht erreichbar | "Trotzdem Prompt erstellen", "Retry", "Abbrechen" |
  | Version-Angabe unklar | Aktuelle Versionen als Optionen |
  | Kein Commit-Stand erkennbar | "Version vom User eingeben", "Ohne Version", "Abbrechen" |

  Prosa nur bei einer offenen Frage ohne feste Optionen (Beispiel: "Welche Version ist aktuell?" ohne Kandidaten), wenn
  der Nutzer gerade eine klare Präferenz signalisiert hat, oder bei Erklärung/Kontext ohne echte Entscheidung.
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle muss dieser sein, sonst Auswahlfrage (wechseln /
  abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: ein in dieser Sitzung schon bekannter Branch; sonst mit Shell
  `git branch --show-current` – Tatsache, keine Frage; ohne Shell die Branches über die GitHub API auflisten und per
  Auswahlfrage wählen lassen (Optionen = Branch-Namen). NIE automatisch einen Branch annehmen (weder `main` noch einen
  anderen). Den Branch für die ganze Sitzung merken und im Übergabe-Prompt unter `**Branch:**` eintragen.
- **Push** im Sitzungsabschluss (Claude Code) nach der Push-Policy des Skill-Profils:
  - `user-only`: kein Push; der Nutzer pusht selbst
  - `allowed`: Push nur, wenn der Nutzer es ausdrücklich will
  - `required-after-commit`: Push direkt nach dem Commit des Sitzungsabschlusses
  - `required-at-session-end`: alle Commits der Sitzung pushen, bevor der Handover-Prompt ausgegeben wird

  Ohne Push-Policy (kein Skill-Profil): Commit im Sitzungsabschluss, Push nur nach Auswahlfrage (pushen / nicht pushen).

  Bleiben Commits ungepusht (`user-only`, `allowed`), nennt der Übergabe-Prompt sie unter „Sonstige offene Punkte“
  (Hash und Titel, „Push durch den Nutzer“).

---

## Voraussetzung: Skill-Profil

Die Werte kommen aus dem Skill-Profil der `CLAUDE.md` im Repo (`docs/skill-profile-v1.md` im Skill-Repo):

| Feld | Wofür |
|------|-------|
| `Doku.Sitzungsabschluss` | Orte für Stand, offene Punkte und Statusliste; Startprompt, falls das Projekt einen führt |
| `Doku.Entscheidungs-Ort` | Abschnitt „Aktive Entscheidungen“ im Prompt |
| `Commit.Push-Policy`, `Branch-Policy` | Push im Sitzungsabschluss, Branch im Prompt (Grundsätze) |
| `Commit.Versionsquelle` | Version im Prompt und in der Link-Prüfung |
| `Tracker.Config` | ClickUp-Abgleich, wenn Aufgaben eingebunden sind (Präfix, Listen, Statusmodell) |
| `Commit.*`, `Code.*`, `Doku.*` | Regeln-Block des Prompts |

1. **Skill-Profil v1** (Abschnitt `## Skill-Profil`). `none` ist gültig: der Teil entfällt im Prompt.
2. **Rückfall:** die älteren Abschnitte `## Commit-Profil`, `## Tracker-Profil`, `## Code-Profil` und `## Doku-Profil`
   der CLAUDE.md.
3. **Fehlt beides:** im Cowork-Chat der Memory-Eintrag `[CLICKUP]`, im Repo der Router (meist `INDEX.md`), soweit
   vorhanden; was dann noch fehlt, per Auswahlfrage nach der Profil-Regel „Fehlende Werte“ (Profil ergänzen / einmalig
   nennen / abbrechen). Nie raten.

---

## TRIGGER

Ja: "neuer chat", "nächster chat", "session beenden", "chat wechsel",
"weiter im nächsten chat", "mach mir den prompt", "übergabe", "neue sitzung",
"sitzung abschließen und übergabe"

Nein: "pause", "tschüss", "gute nacht"

---

## Fall → Reference

| Fall | Reference |
|------|-----------|
| Handover-Prompt aufbauen (beide Umgebungen) | [references/prompt-struktur.md](references/prompt-struktur.md) |
| ClickUp-Abgleich vor dem Übergabeprompt: offene Tasks, Chat-Scan, Batch-Abschluss, ClickUp nicht erreichbar | [references/tracker-abgleich.md](references/tracker-abgleich.md) |
| Cowork-Chat: Ablauf, Memory-Scan, Chat-Anker-Übergabe, Chat-URL im Übergabe-Prompt, Regeln und VERBOTEN | [references/cowork.md](references/cowork.md) |
| Claude Code in tmux: neues Fenster für die nächste Sitzung | [references/neues-fenster.md](references/neues-fenster.md) |
| Beispielwerte zweier Projekte (Startprompt, Orte, Gruppierung, Regeln ohne Profil) | [references/beispiele.md](references/beispiele.md) |

---

## Memory-Scan (PFLICHT bei Handover)

**Zweck:** Offene Merker, Verifikationen und Architektur-Fragen aus Memory in den Handover-Prompt übernehmen, damit sie nicht zwischen Chats verloren gehen.

**Claude Code:** Das Memory ist ein Ordner mit Dateien (Typen `user`/`feedback`/`project`/`reference`) und
bleibt über Sitzungen erhalten – es muss **nicht** in den Prompt kopiert werden. Stattdessen: offene Punkte,
die nur im Chat entstanden sind, gehören an den Ort für offene Punkte aus `Doku.Sitzungsabschluss`, erledigte Merker
werden mit Bestätigung des Nutzers als Datei entfernt. Die Schritte für den Cowork-Chat stehen in
[references/cowork.md](references/cowork.md), Abschnitt „Memory-Scan (PFLICHT bei Handover)“.

---

## ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt)

1. **doc-pflege, Sitzungsabschluss** ausführen: Statusliste/Aufgabenquelle ↔ Tracker, Befunde und
   Entscheidungen, Stand-Abschnitt, offene Punkte als Checkliste (Orte aus `Doku.Sitzungsabschluss`), Doku-Check
   des Skill-Profils (`Commit.Doku-Check`), Commit + Push nach der Push-Policy (Grundsätze). Uncommittete Änderungen →
   Auswahlfrage.
2. **ClickUp-Abgleich** nach [references/tracker-abgleich.md](references/tracker-abgleich.md) (Batch-Abschluss über tracker),
   **Memory**: erledigte Merker mit Bestätigung entfernen.
3. **Link-Prüfung** auf den Stand-Abschnitt und den Startprompt.
4. **Handover-Prompt nach PROMPT-STRUKTUR ausgeben** ([references/prompt-struktur.md](references/prompt-struktur.md);
   vollständig, als Markdown-Codeblock). Erste Zeile darin ist der Startprompt des Projekts, falls es einen führt
   (Muster: [references/beispiele.md](references/beispiele.md), Abschnitt „Startprompt“). Danach folgen die
   Abschnitte der PROMPT-STRUKTUR: Aktueller Stand, Erledigt in dieser Sitzung, Offene Punkte (ClickUp nach
   Liste oder Status, Chat, Sonstiges), Nächste Schritte, Aktive Entscheidungen, Kontext/Warnungen, Regeln aus dem
   Skill-Profil. Memory-Sektion: in Claude Code die relevanten Memory-Dateien nennen (Titel), nicht kopieren.
5. **Neues Fenster** (nur wenn die Sitzung in tmux läuft): Umgebung prüfen, per Auswahlfrage anbieten, dann ein
   tmux-Fenster im Projekt-Repo mit `claude --remote-control` anlegen und den Prompt dort einfügen, nicht absenden.
   Ablauf: [references/neues-fenster.md](references/neues-fenster.md).
6. Fertig. Kurzform (nur Startprompt) nur auf ausdrücklichen Wunsch.

---

## Ablauf im Cowork-Chat

Der Chat hat kein Repo-Gedächtnis, der Handover-Prompt trägt den Stand: ClickUp-Abgleich, Memory-Scan,
Chat-Anker-Übergabe, Chat-URL, Link-Prüfung, dann der Prompt im Chat. Reihenfolge, Regeln und VERBOTEN:
[references/cowork.md](references/cowork.md), Abschnitt „Ablauf im Cowork-Chat“.

---

## Link-Prüfung (PFLICHT vor der Ausgabe)

Jeder Verweis im Prompt muss stimmen, sonst startet die nächste Sitzung mit falschen Annahmen
(Beispiel: eine Datei, die seit einem Umbau anders heißt).

1. **Dateien und Pfade:** jede genannte Datei existiert (Datei suchen bzw. Ordner listen)
2. **Abschnitte:** genannte Kapitel/Abschnitte existieren in der Datei (Suche nach der Überschrift)
3. **Task-IDs:** jede `<PRÄFIX>-NNN` existiert im Tracker mit dem genannten Status (tracker read-only, `clickup_get_task`)
4. **Versionen:** Version im Prompt = `Commit.Versionsquelle` des Skill-Profils
5. Tote Verweise → Auswahlfrage „Korrigieren / Mit Warnung übernehmen / Weglassen“; nie stumm übernehmen

---

## REGELN

- Automatisch sammeln — nicht nachfragen was rein soll
- Chat-Nummer korrekt — N+1
- Nichts vergessen — inkl. pending Frontmatter, neue Invarianten
- Kompakt aber vollständig
- Kopierfähig als Markdown-Codeblock
- Version prüfen
- Keine Datei — direkt im Chat; Claude Code: zusätzlich vorher Stand ins Repo (doc-pflege, Sitzungsabschluss)
- Pending Quickload-Änderungen explizit nennen
- **ClickUp-Abgleich VOR Übergabeprompt** — offene Tasks laden + Chat scannen
- **Batch-Abschluss per Auswahlfrage** (nicht Prosa-Liste)
- **Keine automatischen ClickUp-Mutationen ohne Auswahlfrage-Bestätigung**
- **Nächste Schritte nach Meilenstein und Priorität laut Tracker-Config ableiten**
- **Sonstige offene Punkte** (Pending Commits, Frontmatter, Invarianten) ZUSÄTZLICH zu ClickUp auflisten
- **Link-Prüfung vor der Ausgabe** — Dateien, Abschnitte, Task-IDs, Version (Abschnitt „Link-Prüfung“)
- **Regeln-Block aus dem Skill-Profil** erzeugen, nicht aus einer festen Liste
- **Claude Code: erst doc-pflege, Sitzungsabschluss, dann vollständiger Handover-Prompt** — Kurzform nur auf Wunsch; Details verweisen auf die Orte aus `Doku.Sitzungsabschluss` statt sie zu kopieren
- Cowork-Chat zusätzlich: Chat-URL, `[ANKER-LIVE]`, Memory-Scan nach Rubriken, Memory-Cleanup nur mit Bestätigung
  ([references/cowork.md](references/cowork.md), Abschnitt „Regeln im Cowork-Chat“)

---

## VERBOTEN

- Nachfragen was rein soll (Prosa)
- Offene Punkte vergessen
- Als Datei liefern
- Ohne Version/Chat-Nummer
- Nummern verwechseln
- Pending Frontmatter/Invarianten vergessen
- Branch automatisch annehmen – ohne Branch-Policy, Shell oder Auswahlfrage
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER Auswahlfrage (Branch-Auswahl, Batch-Abschluss, "ja/nein/einzeln wählen")
- **Tasks automatisch in ClickUp erstellen/schließen ohne Auswahlfrage-Bestätigung**
- **ClickUp-Schreiboperationen direkt ausführen (→ tracker-Skill nutzen)**
- **Pending Commits/Doc-Updates/Frontmatter-Updates vergessen nur weil ClickUp da ist**
- **Memory-Einträge stillschweigend entfernen nach Abschluss** — der Nutzer muss explizit bestätigen
- **Prompt mit toten Verweisen ausgeben** (umbenannte Dateien, fehlende Abschnitte, falsche Task-IDs oder Version)
- **Regeln oder Präfix eines anderen Projekts in den Prompt schreiben** — Regeln und Präfix aus dem Skill-Profil
- **In Claude Code den Stand nur in den Prompt schreiben statt ins Repo** (Orte aus `Doku.Sitzungsabschluss`) — der Sitzungsabschluss kommt immer zuerst
- **In Claude Code ungefragt nur den kurzen Startprompt liefern** — der User erwartet den vollständigen Handover-Prompt
- **Sitzung mit uncommitteten Änderungen übergeben** ohne Auswahlfrage
- **Den Prompt im neuen Fenster selbst absenden oder das alte Fenster schließen** — beides entscheidet der User
- Was nur im Cowork-Chat verboten ist (Chat-URLs raten, Anker im Memory belassen, leere Sektionen, dauerhafte
  Memories im Prompt): [references/cowork.md](references/cowork.md), Abschnitt „VERBOTEN im Cowork-Chat“
