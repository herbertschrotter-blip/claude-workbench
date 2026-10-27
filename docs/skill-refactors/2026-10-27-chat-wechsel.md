# Regel-Inventar – chat-wechsel, Phase 6 (2026-10-27)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Verweise von außen
- Prüfung

## Kopf

- **Skill:** `skills/chat-wechsel/`
- **Stand vor dem Umbau:** `main` 5520884, v0.60.7; `SKILL.md` 236 Zeilen, references `cowork.md` 165,
  `neues-fenster.md` 37, `prompt-struktur.md` 88, `tracker-abgleich.md` 93
- **Anlass:** Umbau Phase 6 (ClickUp 123ztrcxedq), zweiter Skill. Größe erfüllt; offen waren Projektwerte (BPM, Heidi) im
  Kern und in den References, Historie, Cowork-Regeln im Kern, alte Profilbegriffe statt Skill-Profil v1, ein
  Werkzeugname (`ask_user_input_v0`) in `tracker-abgleich.md`.
- **Entscheidungen Herbert 27.10.2026:** Zielstruktur „Umsetzen“ (neu `references/beispiele.md`, Cowork-Regeln nach
  `references/cowork.md`); DROP-Gruppe D1 Historie freigegeben.
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem HA nicht (kein PowerShell); Kandidaten von Hand
  aus dem alten Text, Prüfung nach dem Push per GitHub Actions.

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `B` = `references/beispiele.md`, `C` = `references/cowork.md`,
`P` = `references/prompt-struktur.md`, `T` = `references/tracker-abgleich.md`, `F` = `references/neues-fenster.md`.

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck · Vorrang / Delegation · Grundsätze · **Voraussetzung: Skill-Profil** (neu) · TRIGGER · Fall → Reference · Memory-Scan · Ablauf in Claude Code · Ablauf im Cowork-Chat (Verweis) · Link-Prüfung · REGELN · VERBOTEN |
| `references/cowork.md` | Inhalt · **Ablauf im Cowork-Chat** (aus S) · Memory-Scan · Chat-Anker-Übergabe · Chat-URL · **Regeln im Cowork-Chat** · **VERBOTEN im Cowork-Chat** |
| `references/prompt-struktur.md` | Vorlage neutral; BPM-Block nach B |
| `references/tracker-abgleich.md` | Auswahlfragen als Handlung; Beispiele nach B |
| `references/beispiele.md` (neu) | Inhalt · Orte für den Sitzungsabschluss · Startprompt · ClickUp-Abgleich · Regeln ohne Profil (BPM) · Link-Prüfung |
| `references/neues-fenster.md` | unverändert |

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter | Description | KEEP | S#Frontmatter | wörtlich, 542 Zeichen | | ✅ |
| R002 | S#Zweck (Z. 16–19) | Zwei Wege; Cowork: Prompt trägt den Stand | KEEP | S#Zweck | wörtlich | | ✅ |
| R003 | S#Zweck (Z. 20–22) | Claude Code: erst doc-pflege Sitzungsabschluss, dann derselbe vollständige Prompt | KEEP | S#Zweck | wörtlich bis auf D1 | | ✅ |
| R004 | S#Zweck (Z. 22) | Zitat „Herbert, 16.09.2026 …“ | DROP | – | D1 Historie | ✅ 27.10. | ✅ |
| R005 | S#Zweck (Z. 23) | Details per Verweis auf HANDOFF/Bauplan statt Kopie | REWRITE | S#Zweck | Orte aus `Doku.Sitzungsabschluss` | | ✅ sinngemäß |
| R006 | S#Zweck (Z. 23–24) | Startprompt des Doku-Profils (Heidi: Bauplan 0) als Einstiegszeile im Prompt | REWRITE | S#Zweck; B#Orte für den Sitzungsabschluss | „falls das Projekt einen führt“, Heidi-Wert nach B | | ✅ sinngemäß |
| R007 | S#Zweck (Z. 25) | Kurzform nur auf ausdrücklichen Wunsch | KEEP | S#Zweck | wörtlich | | ✅ |
| R008 | S#Zweck (Z. 27–28) | Projektwerte aus den Profilen (Commit-, Tracker-, Code-, Doku-Profil) | REWRITE | S#Zweck; S#Voraussetzung: Skill-Profil | Skill-Profil v1 | | ✅ sinngemäß |
| R009 | S#Zweck (Z. 28) | Ohne Profil BPM-Weg (Memory `[CLICKUP]`, INDEX.md) | REWRITE | S#Voraussetzung: Skill-Profil (Schritt „Fehlt beides“); B#Orte für den Sitzungsabschluss | neutral: Memory `[CLICKUP]` im Cowork, Router im Repo, sonst Auswahlfrage | | ✅ sinngemäß |
| R010 | S#Vorrang (Z. 32–52) | Delegationstabelle (4 Zeilen), Zuständigkeit, nacheinander statt gemeinsam | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R011 | S#Grundsätze (Z. 58–74) | Fragen nur bei offener Entscheidung, Tabelle (9 Zeilen) | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R012 | S#Grundsätze (Z. 76–77) | Prosa nur bei … | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R013 | S#Grundsätze (Z. 78–83) | Branch nach Branch-Policy, nie automatisch, im Prompt eintragen | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R014 | S#Grundsätze (Z. 84–90) | Push nach Push-Policy (4 Werte, Rückfall) | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R015 | S#Grundsätze (Z. 92–93) | Ungepushte Commits unter „Sonstige offene Punkte“ | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R016 | S#TRIGGER (Z. 96–100) | Ja-/Nein-Auslöser | KEEP | S#TRIGGER | wörtlich | | ✅ |
| R017 | S#Fall → Reference (Z. 106–111) | Tabelle Fall → Reference (4 Zeilen) | REWRITE | S#Fall → Reference | Zeile Cowork um Ablauf, Regeln, VERBOTEN ergänzt; Zeile beispiele.md neu (N004) | | ✅ sinngemäß |
| R018 | S#Memory-Scan (Z. 117) | Zweck Memory-Scan | KEEP | S#Memory-Scan (PFLICHT bei Handover) | wörtlich | | ✅ |
| R019 | S#Memory-Scan (Z. 119–123) | Claude Code: Memory nicht kopieren; offene Punkte an den Doc-Ort (Heidi: HANDOFF 4 / Bauplan 10); erledigte Merker mit Bestätigung entfernen | REWRITE | S#Memory-Scan (PFLICHT bei Handover); B#Orte für den Sitzungsabschluss | Ort aus `Doku.Sitzungsabschluss`; „Herberts“ → „des Nutzers“ | | ✅ sinngemäß |
| R020 | S#Ablauf in Claude Code (Z. 129–131) | doc-pflege Sitzungsabschluss mit Statusliste, Befunden, Stand (Heidi: HANDOFF 3e), offenen Punkten (HANDOFF 4), Doku-Checkliste, Commit + Push; uncommittet → Auswahlfrage | REWRITE | S#ABLAUF IN CLAUDE CODE; B#Orte für den Sitzungsabschluss | Orte aus `Doku.Sitzungsabschluss`, `Commit.Doku-Check` | | ✅ sinngemäß |
| R021 | S#Ablauf in Claude Code (Z. 132–133) | ClickUp-Abgleich, Memory-Merker | KEEP | S#ABLAUF IN CLAUDE CODE | wörtlich | | ✅ |
| R022 | S#Ablauf in Claude Code (Z. 134) | Link-Prüfung auf Stand und Startprompt | KEEP | S#ABLAUF IN CLAUDE CODE | wörtlich | | ✅ |
| R023 | S#Ablauf in Claude Code (Z. 135–144) | Prompt vollständig als Codeblock; erste Zeile Startprompt; Heidi-Beispielblock | REWRITE | S#ABLAUF IN CLAUDE CODE; B#Startprompt | Beispielblock wörtlich nach B | | ✅ sinngemäß |
| R024 | S#Ablauf in Claude Code (Z. 146–149) | Quelle „Startprompt“ im Doku-Profil (Heidi: Bauplan 0); Abschnittsfolge der PROMPT-STRUKTUR; Memory-Dateien nennen statt kopieren | REWRITE | S#ABLAUF IN CLAUDE CODE; B#Orte für den Sitzungsabschluss | „Liste oder Status“, „Skill-Profil“ | | ✅ sinngemäß |
| R025 | S#Ablauf in Claude Code (Z. 150–153) | Neues Fenster in tmux, nicht absenden | KEEP | S#ABLAUF IN CLAUDE CODE | wörtlich | | ✅ |
| R026 | S#Ablauf in Claude Code (Z. 154) | Fertig; Kurzform nur auf Wunsch | KEEP | S#ABLAUF IN CLAUDE CODE | wörtlich | | ✅ |
| R027 | S#Ablauf im Cowork-Chat (Z. 159–170) | Sechs Schritte im Cowork-Chat | MOVE | C#Ablauf im Cowork-Chat; S#Ablauf im Cowork-Chat | in C wörtlich mit angepassten Verweisen; in S ein Satz mit Verweis | | ✅ |
| R028 | S#Link-Prüfung (Z. 176–177) | Zweck; Beispiel `heidi-panel-v2.js` | REWRITE | S#Link-Prüfung; B#Link-Prüfung | Beispiel neutral, Heidi-Fall nach B | | ✅ sinngemäß |
| R029 | S#Link-Prüfung (Z. 179–180) | Dateien (Glob / DC `list_directory`), Abschnitte (Grep) | REWRITE | S#Link-Prüfung | Handlung statt Werkzeug | | ✅ sinngemäß |
| R030 | S#Link-Prüfung (Z. 181) | Task-IDs im Tracker prüfen | KEEP | S#Link-Prüfung | wörtlich | | ✅ |
| R031 | S#Link-Prüfung (Z. 182) | Version = Versionsquelle (Heidi: package.json) | REWRITE | S#Link-Prüfung; B#Orte für den Sitzungsabschluss | `Commit.Versionsquelle` | | ✅ sinngemäß |
| R032 | S#Link-Prüfung (Z. 183) | Tote Verweise → Auswahlfrage | KEEP | S#Link-Prüfung | wörtlich | | ✅ |
| R033 | S#REGELN 1–11, 13 | Sammeln, N+1, nichts vergessen, kompakt, Codeblock, Version, keine Datei, Quickload, Abgleich vorher, Batch per Auswahlfrage, keine Mutation ohne Bestätigung, Sonstige offene Punkte | KEEP | S#REGELN | wörtlich, als Liste ohne Nummern | | ✅ |
| R034 | S#REGELN 12 | Nächste Schritte aus V1 + Priority | REWRITE | S#REGELN; B#ClickUp-Abgleich | Meilenstein und Priorität laut Tracker-Config | | ✅ sinngemäß |
| R035 | S#REGELN 14–17 | Chat-URL, `[ANKER-LIVE]`, Memory-Scan 4 Rubriken, Cleanup mit Bestätigung | MOVE | C#Regeln im Cowork-Chat; S#REGELN | wörtlich in C; Hinweiszeile in S | | ✅ |
| R036 | S#REGELN 18 | Link-Prüfung vor der Ausgabe | KEEP | S#REGELN | wörtlich | | ✅ |
| R037 | S#REGELN 19 | Regeln-Block aus den Profilen | REWRITE | S#REGELN | „aus dem Skill-Profil“ | | ✅ sinngemäß |
| R038 | S#REGELN 20 | Erst Sitzungsabschluss, dann Prompt; Details auf HANDOFF/Bauplan | REWRITE | S#REGELN | Orte aus `Doku.Sitzungsabschluss` | | ✅ sinngemäß |
| R039 | S#VERBOTEN (11 Punkte: Nachfragen … Pending vergessen) | gemeinsame Verbote | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R040 | S#VERBOTEN | Chat-URLs raten; `[ANKER-LIVE]` belassen; leere Anker-Tabelle; `[CLICKUP]`/`[SKILL-ISSUES]` übernehmen; leere Rubriken-H3 | MOVE | C#VERBOTEN im Cowork-Chat; S#VERBOTEN | wörtlich in C; Hinweiszeile in S | | ✅ |
| R041 | S#VERBOTEN | Memory still entfernen — „Herbert muss explizit bestätigen“ | REWRITE | S#VERBOTEN | „der Nutzer“ | | ✅ sinngemäß |
| R042 | S#VERBOTEN | Prompt mit toten Verweisen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R043 | S#VERBOTEN | BPM-Regeln oder BPM-NNN in fremdes Projekt | REWRITE | S#VERBOTEN | „Regeln oder Präfix eines anderen Projekts“ | | ✅ sinngemäß |
| R044 | S#VERBOTEN | Stand nur in den Prompt statt ins Repo (HANDOFF/Bauplan) | REWRITE | S#VERBOTEN | Orte aus `Doku.Sitzungsabschluss` | | ✅ sinngemäß |
| R045 | S#VERBOTEN | Nur Kurzprompt; uncommittet übergeben; im neuen Fenster absenden / altes schließen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R046 | P (Z. 1–4) | Vorlage gilt in beiden Umgebungen | KEEP | P | wörtlich, Satz zu Platzhaltern ergänzt (N005) | | ✅ |
| R047 | P (Z. 6–21) | Titel, Stand (App-Version, Commit, Branch, Chat-URL), Erledigt | REWRITE | P | „Version aus Commit.Versionsquelle“ | | ✅ sinngemäß |
| R048 | P (Z. 24–29) | ClickUp offen gruppiert (BPM: PlanManager/Docs) | REWRITE | P; B#ClickUp-Abgleich | `<Liste oder Status>` | | ✅ sinngemäß |
| R049 | P (Z. 31–63) | Anker (nur Cowork), Memory-Rubriken, neu erkannt, erledigt, Sonstige | KEEP | P | wörtlich; Memory-Sektion als „nur Cowork“ markiert | | ✅ |
| R050 | P (Z. 65–66) | Nächste Schritte nach V1 + high/urgent | REWRITE | P | Meilenstein und Priorität laut Tracker-Config | | ✅ sinngemäß |
| R051 | P (Z. 68–76) | Entscheidungen, Kontext | KEEP | P | wörtlich | | ✅ |
| R052 | P (Z. 78–85) | Regeln-Block aus den Profilen (Commit, Tracker, Docs, Code, Arbeitsweise) | REWRITE | P | Feldnamen Skill-Profil v1 | | ✅ sinngemäß |
| R053 | P (Z. 86–87) | BPM ohne Profile: Regeln | MOVE | B#Regeln ohne Profil (BPM); P | wörtlich nach B; Verweiszeile in P | | ✅ |
| R054 | T (Z. 1–10) | Offene Tasks laden: Config, read-only Filter, Gruppierung (BPM/Heidi) | REWRITE | T#Schritt 1; B#ClickUp-Abgleich | Heidi-Status nach B, Statusmodell der Tracker-Config | | ✅ sinngemäß |
| R055 | T (Z. 12–19) | Chat scannen nach klaren Mustern | KEEP | T#Schritt 2 | wörtlich | | ✅ |
| R056 | T (Z. 21–44) | Batch-Übersicht (BPM-Beispiel) | REWRITE | T#Schritt 3; B#ClickUp-Abgleich | Platzhalter in T, BPM-Beispiel wörtlich nach B | | ✅ sinngemäß |
| R057 | T (Z. 46–77) | Zwei Auswahlfragen multiSelect (als `ask_user_input_v0`) | REWRITE | T#Schritt 3 | Handlung statt Werkzeug, Optionen mit Platzhaltern | | ✅ sinngemäß |
| R058 | T (Z. 79–83) | Nach Bestätigung: tracker done/neu, Status (Heidi testing, BPM done), Memory/Next | REWRITE | T#Schritt 4; B#ClickUp-Abgleich | Status laut Tracker-Config | | ✅ sinngemäß |
| R059 | T (Z. 85–93) | ClickUp nicht erreichbar | KEEP | T#ClickUp nicht erreichbar? | wörtlich | | ✅ |
| R060 | C#Kopf, Inhalt | Gilt nur Cowork; Inhaltsverzeichnis | REWRITE | C | Titel und Inhalt um Ablauf, Regeln, VERBOTEN ergänzt | | ✅ sinngemäß |
| R061 | C#Memory-Scan Schritt 1–4, 6 | Lesen, Rubriken, nicht übernehmen, Eskalation + Fragilitäten, Sektion | KEEP | C#Memory-Scan (PFLICHT bei Handover) | wörtlich | | ✅ |
| R062 | C#Memory-Scan Schritt 5 | Vor Abschluss prüfen — „Herbert fragen“ | REWRITE | C#Memory-Scan (PFLICHT bei Handover) | „den Nutzer fragen“ | | ✅ sinngemäß |
| R063 | C#Chat-Anker-Übergabe | Zweck, Schritte 1–4, keine Anker | KEEP | C#Chat-Anker-Übergabe (nur Cowork) | wörtlich bis auf D1 | | ✅ |
| R064 | C#Chat-Anker Schritt 2 | „(Phase 1 Ausarbeitung)“ | DROP | – | D1 Historie | ✅ 27.10. | ✅ |
| R065 | C#Chat-URL | Ermittlung, nicht raten | KEEP | C#Chat-URL in Übergabe-Prompt (nur Cowork) | wörtlich | | ✅ |
| R066 | F | neues Fenster: Ablauf und Regeln | KEEP | F | Datei unverändert | | ✅ |
| N001 | – | Abschnitt „Voraussetzung: Skill-Profil“ mit Feldtabelle | NEW | S#Voraussetzung: Skill-Profil | `docs/skill-profile-v1.md`, Tabelle Pflichtfelder je Skill | | ✅ |
| N002 | – | Reihenfolge: v1 → ältere Profilabschnitte → Auswahlfrage „Fehlende Werte“; `none` gültig | NEW | S#Voraussetzung: Skill-Profil | wie mockup-erstellen v0.60.7 | | ✅ |
| N003 | – | `references/beispiele.md` mit Werten BPM und Heidi | NEW | B | nimmt R006, R009, R019, R020, R023, R024, R028, R031, R034, R048, R053, R054, R056, R058 auf | | ✅ |
| N004 | – | Zeile beispiele.md in Fall → Reference | NEW | S#Fall → Reference | | | ✅ |
| N005 | – | Platzhalter kommen aus dem Skill-Profil, Verweis auf B | NEW | P; T | | | ✅ |
| N006 | – | Mehr als vier Optionen auf mehrere Fragen verteilen | NEW | T#Schritt 3 | Grenze des Frage-Werkzeugs; ersetzt die festen Beispiel-Optionen | | ✅ |

## DROP-Gruppen

| Gruppe | IDs | Begründung | Freigabe |
|---|---|---|---|
| D1 Historie | R004, R064 | Datum und Anlass bzw. Phasenname im Regeltext (`docs/skill-quality.md`, Abschnitt Inhalt); die Regel dahinter bleibt (R003, R063) | Herbert 27.10.2026 |

## Verweise von außen

- `skills/sitzung/SKILL.md` → `skills/chat-wechsel/references/neues-fenster.md`: unverändert gültig.
- `skills/doc-pflege/SKILL.md#Sitzungsabschluss` nennt chat-wechsel nur beim Namen; dort steht noch „Heidi: Startprompt
  Abschnitt 0“ – Sache des Phase-6-Schritts doc-pflege.
- tracker (`SKILL.md`, `references/anti-patterns.md`, `batch-protocol.md`, `anker-system.md`, `chat-url-handling.md`)
  und ticket, chatgpt-review: nur Skillname, keine Abschnitte oder Nummern.
- Keine Stelle verweist auf die REGELN-Nummern von chat-wechsel; die Nummerierung entfällt daher ohne Folgen.

## Prüfung

- **Alt→Neu:** R001–R066 haben einen Zustand; jeder Neu-Ort ist im neuen Text vorhanden.
- **Neu→Alt:** Sätze mit Pflichtwörtern, Tabellenzeilen und VERBOTEN-Punkte des neuen Stands gehören zu einer ID oder
  zu N001–N006.
- **Qualität:** `SKILL.md` 237 Zeilen; References unter 200 Zeilen, `cowork.md` (200) und `beispiele.md` mit
  Inhaltsverzeichnis; keine Projektwerte außerhalb von `beispiele.md`; keine Historie; Werkzeugnamen nur in Cowork-Teilen
  bzw. `clickup_get_task` als nötiges Werkzeug.
- **Routing-Eval:** `--tag chat-wechsel` nach Commit 2725790: 15 Fälle, alle 3/3 (Score 1.00). CI-Lauf 40489915404 grün.
