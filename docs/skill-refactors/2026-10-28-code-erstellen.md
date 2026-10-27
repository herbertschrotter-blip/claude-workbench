# Regel-Inventar – code-erstellen, Phase 6 (2026-10-28)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Verweise von außen
- Entscheidungen
- Prüfung

## Kopf

- **Skill:** `skills/code-erstellen/`
- **Stand vor dem Umbau:** `main` 3f0519d, v0.60.9; `SKILL.md` 488 Zeilen (Körper 470), references
  `stacks/csharp-wpf.md` 59, `stacks/home-assistant-yaml.md` 72, `stacks/python.md` 67, `stacks/typescript-lit.md` 83
- **Frühere Inventare:** `2026-09-28-code-erstellen.md` (Abschnitt Arbeitsverzeichnis), `2026-09-28-code-erstellen-2.md`
  (Fragen, Branch) – beide Teil-Refactors, IDs hier neu ab R001.
- **Anlass:** Umbau Phase 6 (ClickUp 123ztrcxedq), vierter Skill. Größe knapp erfüllt (470 < 500); offen sind das alte
  `## Code-Profil` mit BPM-/Heidi-Spalten statt Skill-Profil v1, BPM-Ladereihenfolge (DOC-STANDARD Kap. 8, Quickload-
  Limits) im Kern, der Cowork-Abschnitt „Auto-Anker“ (60 Zeilen) samt Historie („Phase 1“) im Kern, weitere Cowork-Teile
  (Ausgabeformat, Testbefehl, Selbst-Review, Arbeitsverzeichnis), BPM-Commit- und ClickUp-Beispiele, Verweise über
  Schrittnummern („Schritt 2“, „Schritt 7b“, „Schritt 9“, „siehe Schritt 1“), ein Werkzeugname (`clickup_search`) im
  Kern, Projektwerte und eine Historienzeile in den Stack-Referenzen.
- **Entscheidungen Herbert 28.10.2026:** Zielstruktur „Umsetzen“; DROP-Gruppe D1 Historie freigegeben; Description
  „Code-Profil“ → „Skill-Profil“, BSM-Beispiele bleiben; altes „Notiz-Ort“ → `Code.Befund-Ort` mit Erklärung im
  Rückfall-Satz; E4 und E5 nicht in diesem Umbau (Skill-Issues); Kopf-Limits neutral in der Modus-Übersicht; toter Verweis
  „Kapitel Chat-Anker-System“ auf `skills/tracker/references/anker-system.md`.
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem HA nicht (kein PowerShell); Kandidaten von Hand
  aus dem alten Text, Prüfung nach dem Push per GitHub Actions.

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `B` = `references/beispiele.md` (neu), `C` = `references/cowork.md` (neu),
`CS` = `references/stacks/csharp-wpf.md`, `HY` = `references/stacks/home-assistant-yaml.md`,
`PY` = `references/stacks/python.md`, `TL` = `references/stacks/typescript-lit.md`.

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck (+ Tabelle Fall → Reference, N004) · Vorrang / Delegation · Grundsätze · Arbeitsverzeichnis (Claude Code; Cowork ein Satz mit Verweis) · **Voraussetzung: Skill-Profil** (neu, statt „Voraussetzung: Code-Profil“; Feldtabelle v1, Quellen v1 → `## Code-Profil` → Router/Auswahlfrage; Stack-Referenzen laden) · **Ablauf (verbindlich)** mit benannten Schritten statt Nummern: Anfrage klassifizieren · Aufgabenquelle und Pflichtkontext laden · Kopf zuerst lesen (neutral, statt „Quickload-First-Pass (BPM)“) · Code Entry Points laden · Impact Check · Blocking Conditions · Code erzeugen · Tests · Selbst-Review · Ausgabe · Commit und Doku-Hinweise · Auslieferung · Tracker-Abgleich · **Aufgaben-Stichwörter** (Claude-Code-Fassung des Auto-Ankers, 6–8 Zeilen) · Modus-Übersicht · VERBOTEN |
| `references/beispiele.md` (neu) | Inhalt · Profilwerte BPM und Heidi (alte Spalten der Code-Profil-Tabelle) · Rückfall ohne Profil (BPM) · Ladereihenfolge BPM (DOC-STANDARD Kap. 8) · Pflichtkontext Heidi · Branch · Doku-Check und Commit (BPM-Block, Heidi-Liste, Beispielausgabe) · Tracker-Abgleich (BPM-Optionen) · Aufgaben-Stichwörter (Notiz-Ort Heidi, Anker-Präfixe) |
| `references/cowork.md` (neu) | Inhalt · Profil und Dateien lesen (DC, Arbeitsverzeichnis nach cc-steuerung) · **Auto-Anker bei Aufgaben-Stichwörtern** (ganzer Abschnitt, ohne Historie) · Tests und Selbst-Review im Cowork-Chat · Ausgabeformat · Auslieferung · VERBOTEN im Cowork-Chat |
| `references/stacks/*.md` | inhaltlich unverändert; Kopfsatz „Code-Profil“ → „Skill-Profil (`Code.Stacks`)“, Projektwerte als „Beispiel BPM/Heidi“ gekennzeichnet bzw. neutral, eine Historienzeile raus (D1) |

Länge nach dem Umbau: `SKILL.md` 422 Zeilen (Körper 404), `references/beispiele.md` 104 und `references/cowork.md` 111
(beide mit Inhaltsverzeichnis); Stack-Referenzen 59, 72, 68, 83.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter (Z. 1–18) | Description (1013 Zeichen) mit „nach dessen Code-Profil“ und Beispielen „mach BSM-002“, „weiter mit BSM-014“ | REWRITE | S#Frontmatter | „Code-Profil“ → „Skill-Profil“ (1014 Zeichen); BSM-Beispiele bleiben (E2) | | ✅ sinngemäß |
| R002 | S#Zweck (Z. 24–26) | Vor jeder Code-Erstellung Docs gelesen und geprüft, Akzeptanz bekannt, Tests laufen, Änderung ausgeliefert | KEEP | S#Zweck | wörtlich | | ✅ |
| R003 | S#Zweck (Z. 26–28) | Welche Docs, Tests, Auslieferung: Code-Profil des Projekts | REWRITE | S#Zweck; S#Voraussetzung: Skill-Profil | „Skill-Profil“, Abschnittsverweis neu | | ✅ sinngemäß |
| R004 | S#Zweck (Z. 28–29) | BPM: verbindliche Ladereihenfolge aus DOC-STANDARD.md Kap. 8; andere Projekte ihre eigene | MOVE | B#Ladereihenfolge BPM; S#Zweck | in S neutral „Ladereihenfolge des Projekts (`Code.Pflichtkontext`)“ | | ✅ |
| R005 | S#Vorrang (Z. 35–37) | Größter Catch-all: bei Hauptabsicht eines Nachbarn delegieren | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R006 | S#Vorrang (Z. 41) | UI-Entwurf, Layout, Screen-Vorschlag, HTML-Mockup → mockup-erstellen | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R007 | S#Vorrang (Z. 42) | Großer UI-Umbau (Deep) + „Mockup-Pflicht: ja“ → zuerst Mockup, Abnahme, dann weiter | REWRITE | S#Vorrang / Delegation an andere Skills | Bedingung aus `Code.Mockup-Policy` (`required:<bedingung>`) | | ✅ sinngemäß |
| R008 | S#Vorrang (Z. 43) | Commit-Befehl, Message, Bump → git-commit-helper | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R009 | S#Vorrang (Z. 44) | ADR, Konzept, Frontmatter, Quickload, Doku-Refactor → doc-pflege | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R010 | S#Vorrang (Z. 45) | Tracker-Aktion ohne Code → tracker; Aufgabe per ID umsetzen („mach BSM-002“) bleibt hier | REWRITE | S#Vorrang / Delegation an andere Skills | Beispiele `<PRÄFIX>-NNN` wie in tracker; „Task“ → „Aufgabe“ | | ✅ sinngemäß |
| R011 | S#Vorrang (Z. 46) | Read-only Konsistenzprüfung → audit | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R012 | S#Vorrang (Z. 48–50) | Nur bei echter Code-Implementierung zuständig | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R013 | S#Vorrang (Z. 52–54) | Lokaler Vorrang, kein globales Regelsystem | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R014 | S#Grundsätze (Z. 60–61) | Fragen nur bei offener Entscheidung, dann Auswahlfrage | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R015 | S#Grundsätze (Z. 65) | Modus unklar → Lite/Standard/Deep | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R016 | S#Grundsätze (Z. 66) | Zielschicht mehrdeutig → Domain/Application/Infrastructure/UI | REWRITE | S#Grundsätze | Optionen = Schichten der Stack-Referenz (die vier Namen sind C#-Lesart) | | ✅ sinngemäß |
| R017 | S#Grundsätze (Z. 67) | Mehrere Referenz-Implementierungen → Dateinamen | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R018 | S#Grundsätze (Z. 68) | Fachliche Invariante verletzt → Trotzdem / Abbrechen / Andere Lösung | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R019 | S#Grundsätze (Z. 69) | Ausgabeformat mehrdeutig (nur Cowork) | MOVE | C#Ausgabeformat | | | ✅ |
| R020 | S#Grundsätze (Z. 70) | ClickUp-Task-Zuordnung nach Commit → Kandidaten + Kein + Neu | REWRITE | S#Grundsätze | „Aufgaben-Zuordnung“ (Begriff), sonst gleich | | ✅ sinngemäß |
| R021 | S#Grundsätze (Z. 71) | Mehrere Blocking Conditions → welche Datei zuerst | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R022 | S#Grundsätze (Z. 72) | Commit-Version unklar → MAJOR/MINOR/PATCH | KEEP | S#Grundsätze | wörtlich; nimmt R107 auf | | ✅ |
| R023 | S#Grundsätze (Z. 73) | Referenzdatei angeben → Kandidaten | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R024 | S#Grundsätze (Z. 74) | Bestehende Daten/Configs → Daten löschen / Migration / Abbrechen | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R025 | S#Grundsätze (Z. 75) | Tests rot → Fix / Test anpassen / Abbrechen | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R026 | S#Grundsätze (Z. 76) | Mockup-Pflicht greift → Mockup zuerst / ohne Mockup | REWRITE | S#Grundsätze | „`Code.Mockup-Policy` greift“ | | ✅ sinngemäß |
| R027 | S#Grundsätze (Z. 78–82) | Prosa-Fragen nur bei offener Frage, Präferenz, Erklärung, Freitext | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R028 | S#Grundsätze (Z. 83–85) | Branch vor erstem Schreibzugriff nach Branch-Policy (`current`/`fixed:`), ohne Shell | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R029 | S#Grundsätze (Z. 85–86) | Ohne Profil: Branch aus der Sitzung verwenden | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R030 | S#Grundsätze (Z. 87–90) | Shell (Claude Code; Cowork: DC) liefert Branch; Pflicht-Branch des Code-Profils (Heidi `dreame_x60`) weicht ab → Auswahlfrage | REWRITE | S#Grundsätze; B#Branch; C#Profil und Dateien lesen | „Shell“ ohne DC; Pflicht-Branch = älteres Code-Profil; Heidi-Wert nach B | | ✅ sinngemäß |
| R031 | S#Grundsätze (Z. 91–92) | Keine Shell → Branches als Auswahlfrage | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R032 | S#Grundsätze (Z. 93) | Gewählten Branch für die Sitzung merken | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R033 | S#Grundsätze (Z. 95) | Nie automatisch einen Branch annehmen | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R034 | S#Arbeitsverzeichnis (Z. 101–103) | Claude Code: Repo-Wurzel der Sitzung, Worktree statt Haupt-Checkout | KEEP | S#Arbeitsverzeichnis (PFLICHT bei Dateizugriff) | wörtlich | | ✅ |
| R035 | S#Arbeitsverzeichnis (Z. 105–107) | Cowork: Arbeitsverzeichnis nach cc-steuerung, Abschnitt „Arbeitsverzeichnis“ | MOVE | C#Profil und Dateien lesen; S#Arbeitsverzeichnis (PFLICHT bei Dateizugriff) | in S ein Satz mit Verweis auf C | | ✅ |
| R036 | S#Arbeitsverzeichnis (Z. 109) | Keine hardcodierten absoluten Pfade | KEEP | S#Arbeitsverzeichnis (PFLICHT bei Dateizugriff) | wörtlich | | ✅ |
| R037 | S#Auto-Anker (Z. 113–115) | Zweck: bei späterem Aufgabenthema temp-Anker setzen, per Chat-Suche wiederfindbar | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | Überschrift ohne „(Phase 1 …)“ (R038) | | ✅ |
| R038 | S#Auto-Anker (Z. 113, 122) | „Phase 1 des Chat-Anker-Systems“, „(Phase 1)“ | DROP | | D1 Historie | ✅ 28.10. | ✅ |
| R039 | S#Auto-Anker (Z. 117) | Gilt nur im Cowork-Chat (keine Chat-Suche, kein `[ANKER-LIVE]` in Claude Code) | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern; S#Aufgaben-Stichwörter | in S als Begründung ein Halbsatz | | ✅ |
| R040 | S#Auto-Anker (Z. 117–119) | Claude Code: Auswahlfrage „Aufgabe jetzt anlegen (`tracker neu`)“ / „Im Notiz-Ort vermerken“ (Heidi: Bauplan 10) / „Nichts“ | REWRITE | S#Aufgaben-Stichwörter; B#Aufgaben-Stichwörter | Notiz-Ort = `Code.Befund-Ort` (E3), Abbildung im Rückfall-Satz von S#Voraussetzung: Skill-Profil erklärt; Heidi-Wert nach B; nimmt Stichwortliste und „Wann kein“ als Verweis auf C auf | | ✅ sinngemäß |
| R041 | S#Auto-Anker (Z. 119–120) | Anker-Präfix = Projekt-Präfix aus der Tracker-Config (BPM `BPM`, Heidi `DX`) | REWRITE | C#Auto-Anker bei Aufgaben-Stichwörtern; B#Aufgaben-Stichwörter | `Tracker.Config`; Werte nach B | | ✅ sinngemäß |
| R042 | S#Auto-Anker (Z. 122) | Konzept-Doc `docs/chat-anker-konzept.md` | MERGE | C#Auto-Anker bei Aufgaben-Stichwörtern | R043; Master-Spec ist `skills/tracker/references/anker-system.md`, das Konzept-Doc liegt außerhalb des Skills | | ✅ sinngemäß |
| R043 | S#Auto-Anker (Z. 123) | Anker-Format + Memory-Registry: tracker „Kapitel Chat-Anker-System“ | REWRITE | C#Auto-Anker bei Aufgaben-Stichwörtern | Verweis `skills/tracker/references/anker-system.md#Anker-Format im Chat-Body` und `#Memory-Registry [ANKER-LIVE]`, ohne „Kapitel“ | | ✅ sinngemäß |
| R044 | S#Task-Keywords (Z. 127–136) | Acht Stichwörter als Aufgaben-Signal | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich; Überschrift „Aufgaben-Stichwörter“ | | ✅ |
| R045 | S#Task-Keywords (Z. 138) | Stichwort und noch keine offene Aufgabe → Anker | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich | | ✅ |
| R046 | S#Ablauf (Z. 142) | Stichwort erkannt und Thema klar | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich | | ✅ |
| R047 | S#Ablauf (Z. 143–145) | TEMP-ID in der Shell (tracker „TEMP-ID Generierung“), Rückfall `TEMP-<yyMMddHHmm><3 Buchstaben>` | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | Verweis `skills/tracker/references/anker-system.md#TEMP-ID Generierung` | | ✅ |
| R048 | S#Ablauf (Z. 146–149) | Anker-Zeile `[<PRÄFIX>-ANCHOR-TEMP-<id>] — Idee: …` (max. 60 Zeichen) | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | Pflichtformat, wörtlich | | ✅ |
| R049 | S#Ablauf (Z. 150–153) | Memory `[ANKER-LIVE]` mit `memory_user_edits` aktualisieren | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich (Werkzeugname in Cowork-Reference zulässig) | | ✅ |
| R050 | S#Ablauf (Z. 154) | Hinweis „Anker gesetzt — wird bei `tracker neu` verknüpft“ | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich | | ✅ |
| R051 | S#Wann KEIN Auto-Anker (Z. 158–162) | Kein Anker: bestehende Aufgabe, zu vage, Duplikat 24 h, Nutzer will keinen, > 10 Anker | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich | | ✅ |
| R052 | S#Wann KEIN Auto-Anker (Z. 164) | Im Zweifel kein Anker | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich | | ✅ |
| R053 | S#Anti-Pattern (Z. 168–171) | Nicht in Codeblöcken, nicht doppelt, nicht ohne Handlungsabsicht, nicht generisch | MOVE | C#Auto-Anker bei Aufgaben-Stichwörtern | wörtlich | | ✅ |
| R054 | S#Voraussetzung: Code-Profil (Z. 177–179) | Profil im Abschnitt `## Code-Profil` der CLAUDE.md; Claude Code liest automatisch, Cowork per DC | REWRITE | S#Voraussetzung: Skill-Profil; C#Profil und Dateien lesen | Quelle 1 Skill-Profil v1 (N001), `## Code-Profil` als Rückfall (Quelle 2); DC nach C | | ✅ sinngemäß |
| R055 | S#Voraussetzung (Z. 181–191) | Felder und Bedeutung (Stacks, Build/Lint, Pflicht-Docs, Aufgabenquelle, Schichten/Kopplung, Tests, Auslieferung, Mockup-Pflicht, Notiz-Ort) | REWRITE | S#Voraussetzung: Skill-Profil | Tabelle mit v1-Feldern: `Code.Stacks`, `### Checks` (Build/Lint), `Code.Pflichtkontext`, `Code.Aufgabenquelle`, `Code.Architekturregeln`, `Code.Tests`, `Code.Auslieferung`, `Code.Mockup-Policy`, `Code.Befund-Ort`; dazu `Doku.Entscheidungs-Ort`, `Commit.*`, `Tracker.Config` | | ✅ sinngemäß |
| R056 | S#Voraussetzung (Z. 181–191) | Werte BPM und Heidi je Feld | MOVE | B#Profilwerte BPM und Heidi | wörtlich | | ✅ |
| R057 | S#Voraussetzung (Z. 193–195) | Je Schlüssel in `Stacks:` die Stack-Referenz lesen, bevor Modus, Impact, Blocking beurteilt werden | REWRITE | S#Voraussetzung: Skill-Profil | `Code.Stacks` | | ✅ sinngemäß |
| R058 | S#Voraussetzung (Z. 195–197) | Stack-Datei fehlt → Auswahlfrage ableiten und anlegen / ohne; nie raten | KEEP | S#Voraussetzung: Skill-Profil | wörtlich (greift heute bei `home-assistant`, E4 als Skill-Issue) | | ✅ |
| R059 | S#Voraussetzung (Z. 197) | Neue Sprache = neue Datei, Skill bleibt unverändert | KEEP | S#Voraussetzung: Skill-Profil | wörtlich | | ✅ |
| R060 | S#Voraussetzung (Z. 198) | Vorhandene Stack-Schlüssel | KEEP | S#Zweck (Fall → Reference) | als Zeilen der Tabelle N004, je Datei verlinkt | | ✅ |
| R061 | S#Voraussetzung (Z. 200–201) | Fehlt das Profil: `INDEX.md` als Profil (BPM-Weg, DOC-STANDARD, Stack `csharp-wpf`) | REWRITE | S#Voraussetzung: Skill-Profil; B#Rückfall ohne Profil (BPM) | Quelle 3: Router (`INDEX.md`) soweit vorhanden; BPM-Bedingung und Werte nach B | | ✅ sinngemäß |
| R062 | S#Voraussetzung (Z. 202–203) | Sonst Auswahlfrage „Profil anlegen (Vorschlag)“ / „Ich nenne die Dateien“; nie ohne Docs coden | REWRITE | S#Voraussetzung: Skill-Profil | Optionen nach `docs/skill-profile-v1.md#Fehlende Werte` (Profil ergänzen / einmalig nennen / abbrechen); „Nie ohne Docs coden“ wörtlich | | ✅ sinngemäß |
| R063 | S#Load Order (Z. 207) | Ablauf verbindlich in dieser Reihenfolge | REWRITE | S#Ablauf (verbindlich) | Überschrift deutsch, Schritte ohne Nummern | | ✅ sinngemäß |
| R064 | S#Anfrage klassifizieren (Z. 211–212) | Kriterien neutral, Beispiele je Sprache in der Stack-Referenz | KEEP | S#Anfrage klassifizieren | wörtlich | | ✅ |
| R065 | S#Anfrage klassifizieren (Z. 214–233) | Eskalationskriterien Standard/Deep | KEEP | S#Anfrage klassifizieren | wörtlich | | ✅ |
| R066 | S#Anfrage klassifizieren (Z. 235) | Unsicherheit → Auswahlfrage Lite/Standard/Deep | MERGE | S#Grundsätze | R015 | | ✅ sinngemäß |
| R067 | S#Anfrage klassifizieren (Z. 237–239) | Mockup-Hook: Deep + UI + Mockup-Pflicht → mockup-erstellen, Abnahme abwarten, „erst dann Schritt 2“; Ausnahme per Auswahlfrage | REWRITE | S#Anfrage klassifizieren | `Code.Mockup-Policy`; „erst dann weiter mit Aufgabenquelle und Pflichtkontext“ | | ✅ sinngemäß |
| R068 | S#Aufgabenquelle (Z. 243–245) | Aufgabenquelle (ClickUp-Task, Bauplan-Karte) lesen: Ziel, Akzeptanz, Nicht ändern, Voraussetzungen; Akzeptanz → Testfall (Schritt 7b) + Impact-Zeile | REWRITE | S#Aufgabenquelle und Pflichtkontext laden | `Code.Aufgabenquelle`; Beispiele nach B; Verweis „Tests“ statt „Schritt 7b“ | | ✅ sinngemäß |
| R069 | S#Aufgabenquelle (Z. 246–248) | Pflicht-Docs in Reihenfolge des Profils (BPM INDEX → Routing …; Heidi CLAUDE.md, HANDOFF 3e, BAUPLAN 2/4/6) | REWRITE | S#Aufgabenquelle und Pflichtkontext laden; B#Ladereihenfolge BPM; B#Pflichtkontext Heidi | `Code.Pflichtkontext`; Projektwerte nach B | | ✅ sinngemäß |
| R070 | S#Aufgabenquelle (Z. 249–252) | Grundentscheidungen am `Doku.Entscheidungs-Ort` vor erster fachlicher Erweiterung lesen; Änderung dort nachtragen | KEEP | S#Aufgabenquelle und Pflichtkontext laden | wörtlich | | ✅ |
| R071 | S#Quickload-First-Pass (Z. 254) | Überschrift „BPM: DOC-STANDARD Kapitel 8; andere: Ladereihenfolge des Profils“ | REWRITE | S#Kopf zuerst lesen | neutral; Kapitelnummer nach B | | ✅ sinngemäß |
| R072 | S#Quickload-First-Pass (Z. 256–264) | Verbindliche Ladereihenfolge BPM (fünf Stufen) | MOVE | B#Ladereihenfolge BPM | wörtlich | | ✅ |
| R073 | S#Quickload-First-Pass (Z. 266–273) | Router → Docs; je Doc nur Kopf (~30 Zeilen); Invarianten in Impact; Pflichtlesen laden; Langform nur relevante Kapitel; ohne Quickload ganze Doc | REWRITE | S#Kopf zuerst lesen | neutral „wo die Docs einen Kopf (Frontmatter, Quickload) haben“; Router aus `Doku.Router` | | ✅ sinngemäß |
| R074 | S#Quickload-First-Pass (Z. 275–278) | Limits Quickload/Langform je Modus (3/2, 6/4, 10/8) | MERGE | S#Modus-Übersicht | R119 (dieselben Zahlen) | | ✅ sinngemäß |
| R075 | S#Code Entry Points (Z. 282–285) | Kopplungsregeln aus Stack-Referenz + Zeile „Schichten / Kopplung“ des Profils; bei mehreren Stacks den Vertrag zuerst | REWRITE | S#Code Entry Points laden | `Code.Architekturregeln` | | ✅ sinngemäß |
| R076 | S#Impact Check (Z. 289–290) | Zeilen neutral, Lesart in der Stack-Referenz | KEEP | S#Impact Check | wörtlich | | ✅ |
| R077 | S#Impact Check (Z. 292–310) | Impact-Check-Block (16 Zeilen, Pflichtformat) | REWRITE | S#Impact Check | „(Profil-Befehl)“ → „(`Code.Tests`)“, „Auslieferung nötig (`Code.Auslieferung`)“; sonst wörtlich | | ✅ sinngemäß |
| R078 | S#Blocking (Z. 314–316) | Zielschicht unklar, Referenzdatei fehlt → Auswahlfrage | KEEP | S#Blocking Conditions | wörtlich | | ✅ |
| R079 | S#Blocking (Z. 317–320) | Verdrahtung, externe Kommunikation, UI, Schema/Vertrag → erst laden | KEEP | S#Blocking Conditions | wörtlich | | ✅ |
| R080 | S#Blocking (Z. 321–324) | Stack-Ref, Pflichtlesen, Akzeptanz nicht gelesen; Mockup-Pflicht ohne Abnahme (siehe Schritt 1) | REWRITE | S#Blocking Conditions | `Code.Stacks`, `Code.Mockup-Policy`; Verweis „Anfrage klassifizieren“ | | ✅ sinngemäß |
| R081 | S#Blocking (Z. 325) | Invariante verletzt → Auswahlfrage | KEEP | S#Blocking Conditions | wörtlich (Tabellenzeile R018 bleibt daneben) | | ✅ |
| R082 | S#Blocking (Z. 326) | Migration nötig → Auswahlfrage — Frühphasen-Prinzip (BPM: INDEX.md) | REWRITE | S#Blocking Conditions; B#Profilwerte BPM und Heidi | „laut `Code.Architekturregeln`“; Ort BPM nach B | | ✅ sinngemäß |
| R083 | S#Blocking (Z. 328) | Nicht blind coden, per Auswahlfrage fehlende Datei klären | KEEP | S#Blocking Conditions | wörtlich | | ✅ |
| R084 | S#Code erzeugen (Z. 332–333) | Standards aus Project Files, Referenzimplementierungen als Muster, nichts fest verdrahten, was dynamisch ist | REWRITE | S#Code erzeugen | „Project Files“ (Cowork-Begriff) → „Architekturregeln und Pflichtkontext“ | | ✅ sinngemäß |
| R085 | S#Tests (Z. 337–338) | Je Akzeptanz-Zeile (Schritt 2) ein Test; Unit/E2E laut Stack-Referenz | REWRITE | S#Tests | Verweis über Abschnittsnamen | | ✅ sinngemäß |
| R086 | S#Tests (Z. 339–340) | Claude Code: Testbefehl + Build/Lint des Profils; Exit 0 Bedingung für Schritt 9 | REWRITE | S#Tests | Checks aus `Code.Tests`; „Bedingung für den Commit“ | | ✅ sinngemäß |
| R087 | S#Tests (Z. 341) | Nur Checks mit getroffenem Pfad-Muster, übersprungene nennen | KEEP | S#Tests | wörtlich | | ✅ |
| R088 | S#Tests (Z. 341–343) | Gleichzeitig, lange im Hintergrund mit Datei; Regeln in git-commit-helper | KEEP | S#Tests | wörtlich | | ✅ |
| R089 | S#Tests (Z. 343–344) | Grüner Pre-Commit-Check ohne Änderung läuft nicht noch einmal | KEEP | S#Tests | wörtlich | | ✅ |
| R090 | S#Tests (Z. 344–346) | Claude Code: `checks.py --checks <Tests des Profils>` | KEEP | S#Tests | „Tests des Profils“ → `Code.Tests` | | ✅ |
| R091 | S#Tests (Z. 347) | Cowork: Testbefehl im Commit-Block, Nutzer meldet Ergebnis | MOVE | C#Tests und Selbst-Review im Cowork-Chat | | | ✅ |
| R092 | S#Tests (Z. 348–349) | Tests rot → Auswahlfrage; nie still löschen/überspringen | KEEP | S#Tests | wörtlich | | ✅ |
| R093 | S#Tests (Z. 350–351) | Ergebnis als Tabelle Check/Dauer/Ergebnis, Anzahl, Rot-Gründe | KEEP | S#Tests | wörtlich | | ✅ |
| R094 | S#Selbst-Review (Z. 355–356) | Vor dem Commit eigenen Diff prüfen (Fehler, Randfälle, Sicherheit, Komplexität) | KEEP | S#Selbst-Review (Pflicht vor dem Commit) | wörtlich | | ✅ |
| R095 | S#Selbst-Review (Z. 358–359) | Claude Code: Skill `code-review` (low, Deep medium) | KEEP | S#Selbst-Review (Pflicht vor dem Commit) | wörtlich | | ✅ |
| R096 | S#Selbst-Review (Z. 359) | Cowork: Diff selbst lesen mit denselben vier Fragen | MOVE | C#Tests und Selbst-Review im Cowork-Chat | | | ✅ |
| R097 | S#Selbst-Review (Z. 359–361) | Review meldet nur; hat es geändert/committet → sagen und prüfen | KEEP | S#Selbst-Review (Pflicht vor dem Commit) | wörtlich | | ✅ |
| R098 | S#Selbst-Review (Z. 362–363) | Befund beheben oder begründen; Checks erneut | KEEP | S#Selbst-Review (Pflicht vor dem Commit) | wörtlich | | ✅ |
| R099 | S#Selbst-Review (Z. 364) | Zeile `🔍 Selbst-Review` im Bericht | KEEP | S#Selbst-Review (Pflicht vor dem Commit) | wörtlich | | ✅ |
| R100 | S#Selbst-Review (Z. 366) | Entfällt bei reinem Doku-Diff | KEEP | S#Selbst-Review (Pflicht vor dem Commit) | wörtlich | | ✅ |
| R101 | S#Ausgabeformat (Z. 368–371) | Claude Code: direkt ändern, Chat zeigt Zusammenfassung, nicht Code | REWRITE | S#Ausgabe | Überschrift ohne „nur Cowork“; „Edit/Write“ → „direkt in den Dateien“ | | ✅ sinngemäß |
| R102 | S#Ausgabeformat (Z. 373–377) | Cowork: neue Datei komplett, < 600 und > 30 % komplett, ≥ 600 SUCHE/ERSETZE, Stack-Besonderheiten | MOVE | C#Ausgabeformat; S#Ausgabe | in S ein Satz mit Verweis | | ✅ |
| R103 | S#Ausgabeformat (Z. 379) | Mehrdeutig → Auswahlfrage Formate | MERGE | C#Ausgabeformat | R019 | | ✅ sinngemäß |
| R104 | S#Commit (Z. 383–384) | Format, Versionsquelle, Bump aus dem Commit-Profil (git-commit-helper) | REWRITE | S#Commit und Doku-Hinweise | `Commit.Format`, `Commit.Versionsquelle`, `Commit.Versionsregel` | | ✅ sinngemäß |
| R105 | S#Commit (Z. 384–386) | Doku-Zeilen = Doku-Checkliste des Commit-Profils; Heidi-Liste | REWRITE | S#Commit und Doku-Hinweise; B#Doku-Check und Commit | `Commit.Doku-Check`; Heidi-Liste nach B | | ✅ sinngemäß |
| R106 | S#Commit (Z. 388–405) | Bericht-Block: Commit-Zeile, Doc-Pflege (BPM-Zeilen), Tests, Selbst-Review, Gelesene Dateien, Quickload-Only, Annahmen, Nicht geladen | REWRITE | S#Commit und Doku-Hinweise; B#Doku-Check und Commit | Block neutral (`<Zeile je Punkt aus Commit.Doku-Check>`, „Nur Kopf gelesen“); BPM-Zeilen wörtlich nach B | | ✅ sinngemäß |
| R107 | S#Commit (Z. 407–411) | Bump unklar → Auswahlfrage; Bump-Regel des Profils hat Vorrang (Vorabversion) | MERGE | S#Grundsätze | R022; Vorrang-Satz als `Commit.Versionsregel` an R022 | | ✅ sinngemäß |
| R108 | S#Auslieferung (Z. 415) | Nur wenn das Profil eine Auslieferung nennt | REWRITE | S#Auslieferung | `Code.Auslieferung` | | ✅ sinngemäß |
| R109 | S#Auslieferung (Z. 415–416) | Claude Code führt aus und prüft; Cowork liefert Befehle | REWRITE | S#Auslieferung; C#Auslieferung | Cowork-Halbsatz nach C | | ✅ sinngemäß |
| R110 | S#Auslieferung (Z. 417–418) | Schritte aus dem Profil, Prüfreihenfolge je Stack (Beispiel home-assistant-yaml) | KEEP | S#Auslieferung | wörtlich | | ✅ |
| R111 | S#Auslieferung (Z. 418) | Zum Schluss sagen, was wie sichtzuprüfen ist | KEEP | S#Auslieferung | wörtlich | | ✅ |
| R112 | S#ClickUp Tracker-Abgleich (Z. 420–424) | Nach Commit passende offene Aufgabe suchen (`clickup_search` mit Commit-Stichwörtern) | REWRITE | S#Tracker-Abgleich | Handlung statt Werkzeug: über tracker („tracker suche“), passt zu R117; nur wenn `Tracker.Provider` ≠ none | | ✅ sinngemäß |
| R113 | S#ClickUp Tracker-Abgleich (Z. 425–433) | Kandidaten → Auswahlfrage (Aufgaben, Kein, Neu); BPM-Optionen | REWRITE | S#Tracker-Abgleich; B#Tracker-Abgleich | Optionen mit Platzhaltern; BPM-Beispiel nach B | | ✅ sinngemäß |
| R114 | S#ClickUp Tracker-Abgleich (Z. 434) | „Neu anlegen“ → `tracker neu` | KEEP | S#Tracker-Abgleich | wörtlich | | ✅ |
| R115 | S#ClickUp Tracker-Abgleich (Z. 435) | Auswahl → `tracker done` | KEEP | S#Tracker-Abgleich | wörtlich | | ✅ |
| R116 | S#ClickUp Tracker-Abgleich (Z. 436) | Nicht automatisch schließen | KEEP | S#Tracker-Abgleich | wörtlich | | ✅ |
| R117 | S#ClickUp Tracker-Abgleich (Z. 437) | Alle ClickUp-Operationen über tracker | KEEP | S#Tracker-Abgleich | wörtlich | | ✅ |
| R118 | S#ClickUp Tracker-Abgleich (Z. 439–447) | Beispielausgabe `[v0.25.30] PlanManager, Fix: …` | MOVE | B#Doku-Check und Commit | wörtlich, als Beispiel BPM | | ✅ |
| R119 | S#Modus-Übersicht (Z. 453–457) | Tabelle Modus → Kopf/Langform-Limits, Code, Impact, Tests, Mockup-Hook | REWRITE | S#Modus-Übersicht | Spalte „Quickload“ → „Kopf“ (gilt, wo Docs einen Kopf haben); nimmt R074 auf | | ✅ sinngemäß |
| R120 | S#VERBOTEN (Z. 463) | Code ohne Pflicht-Docs des Profils und Stack-Referenzen aus `Stacks:` | REWRITE | S#VERBOTEN | `Code.Pflichtkontext`, `Code.Stacks` | | ✅ sinngemäß |
| R121 | S#VERBOTEN (Z. 464) | Quickload-First-Pass überspringen | REWRITE | S#VERBOTEN | „Kopf zuerst lesen überspringen“ | | ✅ sinngemäß |
| R122 | S#VERBOTEN (Z. 465) | Pflichtlesen-Kapitel ignorieren | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R123 | S#VERBOTEN (Z. 466) | Fachliche Invarianten ignorieren | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R124 | S#VERBOTEN (Z. 467) | Annahmen ohne geladene Dateien | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R125 | S#VERBOTEN (Z. 468) | Impact Check weglassen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R126 | S#VERBOTEN (Z. 469) | DocMaintenanceHints weglassen | KEEP | S#VERBOTEN | wörtlich (doc-pflege nutzt den Begriff) | | ✅ |
| R127 | S#VERBOTEN (Z. 470) | Branch automatisch annehmen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R128 | S#VERBOTEN (Z. 471) | Hardcodierte absolute Pfade (DC oder Claude Code) | REWRITE | S#VERBOTEN | „in keiner Umgebung“ statt DC | | ✅ sinngemäß |
| R129 | S#VERBOTEN (Z. 472) | Aufgaben direkt im Tracker erstellen/schließen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R130 | S#VERBOTEN (Z. 473) | Automatisch Done ohne Bestätigung | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R131 | S#VERBOTEN (Z. 474) | Prosa-Fragen bei festen Optionen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R132 | S#VERBOTEN (Z. 475) | Commit bei roten Tests oder ohne Testbefehl | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R133 | S#VERBOTEN (Z. 476) | Roten Test löschen/überspringen ohne Auswahlfrage | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R134 | S#VERBOTEN (Z. 477) | Checks ohne Pfad-Treffer laufen lassen, übersprungene verschweigen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R135 | S#VERBOTEN (Z. 478) | Akzeptanzkriterien ignorieren | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R136 | S#VERBOTEN (Z. 479) | Deep-UI-Umbau ohne Mockup bei Mockup-Pflicht | REWRITE | S#VERBOTEN | `Code.Mockup-Policy` | | ✅ sinngemäß |
| R137 | S#VERBOTEN (Z. 480) | Auslieferung vergessen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R138 | S#VERBOTEN (Z. 481) | Stack-Begriffe eines Projekts für ein anderes annehmen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R139 | S#VERBOTEN (Z. 482) | Sprachspezifisches in die SKILL.md | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R140 | S#VERBOTEN (Z. 483) | Optionen im Chat aufzählen und auf Tippen warten | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R141 | S#VERBOTEN (Z. 484) | Migration automatisch bauen (Frühphasen-Prinzip in INDEX.md) | REWRITE | S#VERBOTEN | „(Architekturregeln des Projekts)“; INDEX-Bezug nach B | | ✅ sinngemäß |
| R142 | S#VERBOTEN (Z. 485) | Auto-Anker bei vagen Themen | MOVE | C#VERBOTEN im Cowork-Chat | wörtlich | | ✅ |
| R143 | S#VERBOTEN (Z. 486) | Anker mit generischen Beschreibungen | MOVE | C#VERBOTEN im Cowork-Chat | wörtlich | | ✅ |
| R144 | S#VERBOTEN (Z. 487) | Anker ohne Memory-Update (Cowork); Claude Code: Auswahlfrage tracker neu / Notiz-Ort | MOVE | C#VERBOTEN im Cowork-Chat; S#VERBOTEN | Cowork-Teil nach C; Claude-Code-Teil MERGE auf R040, in S Hinweiszeile „Cowork-Verbote: C“ | | ✅ |
| R145 | S#VERBOTEN (Z. 488) | Commit ohne Selbst-Review oder mit unbegründetem Befund | KEEP | S#VERBOTEN | Verweis über Abschnittsnamen bleibt | | ✅ |
| R146 | CS (Z. 1) | Titel „— C# / .NET / WPF (BPM)“ | REWRITE | CS | „(BPM)“ raus | | ✅ sinngemäß |
| R147 | CS (Z. 3–5) | Geladen bei `Stacks: csharp-wpf` im Code-Profil; Projektwerte im Code-Profil | REWRITE | CS | „Skill-Profil (`Code.Stacks`)“ | | ✅ sinngemäß |
| R148 | CS#Schichten (Z. 11–15) | View→ViewModel, Service+Interface+DI, Dialog-Muster, DB → `ProjectDatabase.cs` + `DB-SCHEMA.md`, Externe → DSGVO-Doc | REWRITE | CS#Schichten und Kopplungsregeln | DB-Zeile neutral „Datenbank-Klasse + Schema-Doku (Beispiel BPM: …)“; sonst wörtlich | | ✅ sinngemäß |
| R149 | CS#Modus-Eskalation (Z. 19–25) | Beispiele Standard/Deep | KEEP | CS#Modus-Eskalation (Beispiele) | wörtlich | | ✅ |
| R150 | CS#Impact (Z. 29–35) | Stack-Lesart Impact | KEEP | CS#Impact-Check-Zeilen (Stack-Lesart) | wörtlich | | ✅ |
| R151 | CS#Blocking (Z. 39–44) | DI → `App.xaml.cs`; Extern → `DSGVO-Architektur.md`; UI; DB → `DB-SCHEMA.md` | REWRITE | CS#Blocking: welche Doc zuerst | Doc-Namen als „Beispiel BPM“ | | ✅ sinngemäß |
| R152 | CS#Tests (Z. 48–49) | xUnit/NUnit; Befehl aus dem Code-Profil; Cowork: Nutzer führt aus | REWRITE | CS#Tests | `Code.Tests`; Cowork-Halbsatz bleibt (Verweis C) | | ✅ sinngemäß |
| R153 | CS#Ausgabe (Z. 51–53) | Cowork-Ausgabe, XAML → Download | KEEP | CS#Ausgabe (Cowork-Chat) | wörtlich; Ziel des Verweises aus C#Ausgabeformat | | ✅ |
| R154 | CS#Typische Fehler (Z. 57) | Migration statt Daten löschen (Frühphasen-Prinzip, INDEX.md) | REWRITE | CS#Typische Fehler | „(Architekturregeln des Projekts, Beispiel BPM: INDEX.md)“ | | ✅ sinngemäß |
| R155 | CS#Typische Fehler (Z. 58–59) | Service ohne Interface; Bindings; Theme-Farben hart | KEEP | CS#Typische Fehler | wörtlich | | ✅ |
| R156 | HY (Z. 1–5) | Kopf: Code-Profil bzw. CLAUDE.md | REWRITE | HY | „Skill-Profil (`Code.Stacks`)“ | | ✅ sinngemäß |
| R157 | HY#Schichten (Z. 11–12) | Quelle der Wahrheit Repo (`ha/`), nie Host; Repo → deployen → prüfen | REWRITE | HY#Schichten und Kopplungsregeln | „(Beispiel Heidi: `ha/`)“ | | ✅ sinngemäß |
| R158 | HY#Schichten (Z. 13–14) | Pakete je Thema; neue Helfer-Domäne braucht Neustart | KEEP | HY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R159 | HY#Schichten (Z. 15–16) | Automationen/Skripte in `automations.yaml`/`scripts.yaml`; Werte aus Attributen | KEEP | HY#Schichten und Kopplungsregeln | wörtlich; Widerspruch zu `/config/CLAUDE.md` siehe E5 | | ✅ |
| R160 | HY#Schichten (Z. 17–18) | Dashboards, Ressourcen mit `?v=` | KEEP | HY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R161 | HY#Schichten (Z. 19–20) | Vertrag: Entitäten der Karte in der Vertrags-Doku; Umbenennung = Breaking | KEEP | HY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R162 | HY#Schichten (Z. 21–22) | Entitäts-IDs mit Umlaut per API prüfen | KEEP | HY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R163 | HY#Schichten (Z. 23) | Nie ins Repo: `.storage/`, `secrets.yaml`, DBs, Protokolle, Abzüge | KEEP | HY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R164 | HY#Modus-Eskalation (Z. 27–32) | Beispiele Standard/Deep | KEEP | HY#Modus-Eskalation (Beispiele) | wörtlich | | ✅ |
| R165 | HY#Impact (Z. 36–41) | Stack-Lesart Impact | KEEP | HY#Impact-Check-Zeilen (Stack-Lesart) | wörtlich | | ✅ |
| R166 | HY#Blocking (Z. 45–49) | Neue Entität → Vertrag + `contract.ts`; unbekannte ID → `ha.ps1 get states/<id>`; Automation → Trace | REWRITE | HY#Blocking: was zuerst | `ha.ps1` → „Zustand per REST-API (Beispiel Heidi: `ha.ps1 get states/<id>`)“; `contract.ts` als Beispiel Heidi | | ✅ sinngemäß |
| R167 | HY#Prüfen und Ausliefern (Z. 53–58) | Deploy UTF-8 ohne BOM, check_config, Reload statt Neustart, Ergebnis prüfen | KEEP | HY#Prüfen und Ausliefern (Befehle aus dem Profil) | wörtlich | | ✅ |
| R168 | HY#Tests (Z. 62–64) | Kein Unit-Framework; Fixtures nach Entitätsänderung erneuern | KEEP | HY#Tests | wörtlich | | ✅ |
| R169 | HY#Typische Fehler (Z. 68–72) | Fünf typische Fehler | KEEP | HY#Typische Fehler | wörtlich | | ✅ |
| R170 | PY (Z. 1) | Titel „neben HA (Prognose, Laufprotokoll) und allgemein“ | REWRITE | PY | „neben HA und allgemein“ (Prognose, Laufprotokoll = Heidi) | | ✅ sinngemäß |
| R171 | PY (Z. 3–5) | Kopf: Code-Profil | REWRITE | PY | „Skill-Profil (`Code.Stacks`)“ | | ✅ sinngemäß |
| R172 | PY#Schichten (Z. 11–12) | Reine Funktionen, I/O am Rand | KEEP | PY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R173 | PY#Schichten (Z. 13–14) | Gemeinsame Vektoren als Vertrag | KEEP | PY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R174 | PY#Schichten (Z. 15–16) | HA-Skripte geben JSON aus, schreiben nur in vorgesehene Dateien; Laufprotokolle nie löschen | REWRITE | PY#Schichten und Kopplungsregeln | „Protokolle des Projekts (Beispiel Heidi: Laufprotokoll) nie löschen“ | | ✅ sinngemäß |
| R175 | PY#Schichten (Z. 17) | Nur Standardbibliothek auf dem HA-Host | KEEP | PY#Schichten und Kopplungsregeln | wörtlich | | ✅ |
| R176 | PY#Modus-Eskalation (Z. 21–25) | Beispiele Standard/Deep | KEEP | PY#Modus-Eskalation (Beispiele) | wörtlich | | ✅ |
| R177 | PY#Impact (Z. 29–33) | Stack-Lesart Impact | KEEP | PY#Impact-Check-Zeilen (Stack-Lesart) | wörtlich | | ✅ |
| R178 | PY#Blocking (Z. 37–40) | Ausgabeformat → Sensor + Vertrag; gemeinsame Logik → Vektoren | KEEP | PY#Blocking: was zuerst | wörtlich | | ✅ |
| R179 | PY#Tests (Z. 44–45) | pytest, Vektoren, Abweichung als `xfail` mit Begründung | KEEP | PY#Tests | wörtlich | | ✅ |
| R180 | PY#Tests (Z. 46–47) | Befehl aus dem Profil; ohne Python am PC auf dem Host oder als Nutzer-Aufgabe, nie ungetestet | KEEP | PY#Tests | wörtlich | | ✅ |
| R181 | PY#Tests (Z. 48) | Exit 0 vor Commit | KEEP | PY#Tests | wörtlich | | ✅ |
| R182 | PY#Tests (Z. 49–51) | pytest-xdist `-n auto`, keine feste Zahl, Version angeheftet, `--maxprocesses` | KEEP | PY#Tests | wörtlich | | ✅ |
| R183 | PY#Tests (Z. 52–53) | Isolation je Test in `tmp_path` | KEEP | PY#Tests | wörtlich | | ✅ |
| R184 | PY#Tests (Z. 54–59) | Kein Test beeinflusst einen anderen; Server-DB je Lauf und Worker | KEEP | PY#Tests | wörtlich | | ✅ |
| R185 | PY#Typische Fehler (Z. 63–67) | Fünf typische Fehler | KEEP | PY#Typische Fehler | wörtlich | | ✅ |
| R186 | TL (Z. 1–5) | Kopf: Code-Profil | REWRITE | TL | „Skill-Profil (`Code.Stacks`)“ | | ✅ sinngemäß |
| R187 | TL (Z. 7–8) | Gilt für jede eigene Oberfläche in HA (HA-Grundsatz G-22); Heidi-Pfade als Beispiele; Entsprechungen im Code-Profil/README | REWRITE | TL | „im Skill-Profil oder in der README“; G-22 bleibt (Regel-ID, keine Kapitelnummer) | | ✅ sinngemäß |
| R188 | TL (Z. 9–10) | JavaScript-Projekte (z. B. ha-baustelle, esbuild): Regeln sinngemäß | REWRITE | TL | Projektname raus („z. B. mit esbuild gebündelt“) | | ✅ sinngemäß |
| R189 | TL#Schichten (Z. 16–29) | Vertrag, Erkennung, Selektoren, Schreiben über API, Komponenten, Shell, Tokens, keine externen Ressourcen | KEEP | TL#Schichten und Kopplungsregeln | wörtlich (Heidi-Werte schon als Beispiel markiert) | | ✅ |
| R190 | TL#Modus-Eskalation (Z. 33–38) | Beispiele Standard/Deep | KEEP | TL#Modus-Eskalation (Beispiele) | wörtlich | | ✅ |
| R191 | TL#Impact (Z. 42–49) | Stack-Lesart Impact (Heidi `--dx-*` als Beispiel) | KEEP | TL#Impact-Check-Zeilen (Stack-Lesart) | wörtlich | | ✅ |
| R192 | TL#Blocking (Z. 53–58) | Vertrag/Verdrahtung/UI-Umbau/Domänenregel zuerst | KEEP | TL#Blocking: welche Doc/Datei zuerst | wörtlich | | ✅ |
| R193 | TL#Tests (Z. 62–69) | Befehle aus dem Profil (Feld Tests); Heidi-Beispiel Unit, E2E, Pflicht, je Akzeptanz ein Test | REWRITE | TL#Tests | „`Code.Tests`“; Rest wörtlich | | ✅ sinngemäß |
| R194 | TL#Typische Fehler (Z. 73–78) | Sechs typische Fehler | KEEP | TL#Typische Fehler | wörtlich | | ✅ |
| R195 | TL#Typische Fehler (Z. 79–83) | Dateiauswahl in der HA-Android-App: kein `multiple`, MIME nicht vorab prüfen, Schritte sichtbar melden | KEEP | TL#Typische Fehler | wörtlich bis auf R196 | | ✅ |
| R196 | TL#Typische Fehler (Z. 83) | „Befund ha-netzwerk FE-0001 (13.10.2026); derselbe Fehler steckt im Baustrommanager (FE-0027)“ | DROP | | D1 Historie | ✅ 28.10. | ✅ |
| N001 | – | Abschnitt „Voraussetzung: Skill-Profil“: Pflichtfelder `Code.Stacks`, `Code.Pflichtkontext`, `Code.Architekturregeln`, `Code.Tests`, `Code.Auslieferung`; `Code.Aufgabenquelle`, wenn das Projekt Aufgaben führt; dazu genutzt `Code.Mockup-Policy`, `Code.Befund-Ort`, `Doku.Router`, `Doku.Entscheidungs-Ort`, `Commit.*`, `Tracker.Config`, Branch-Policy | NEW | S#Voraussetzung: Skill-Profil | `docs/skill-profile-v1.md#Pflichtfelder je Skill`; Muster chat-wechsel | | ✅ |
| N002 | – | Quellen-Reihenfolge: v1 → `## Code-Profil` als Rückfall → Router/Auswahlfrage nach „Fehlende Werte“; `none` gültig; `fehlt` blockiert; Profil-Version ≠ 1 → nicht weiter | NEW | S#Voraussetzung: Skill-Profil | wie chat-wechsel, mockup-erstellen | | ✅ |
| N003 | – | `references/beispiele.md` mit BPM- und Heidi-Werten | NEW | B | nimmt R004, R030, R040, R041, R056, R061, R069, R072, R082, R105, R106, R113, R118 auf | | ✅ |
| N004 | – | Tabelle Fall → Reference (Stacks je Schlüssel, Beispiele, Cowork) | NEW | S#Zweck | Split-Muster `skills/skill-pflege/SKILL.md#Split-Prüfung` | | ✅ |
| N005 | – | `references/cowork.md` mit Inhaltsverzeichnis; gilt nur im Cowork-Chat | NEW | C | nimmt R019, R035, R037–R053, R091, R096, R102, R103, R109, R142–R144 auf | | ✅ |

## DROP-Gruppen

| Gruppe | IDs | Begründung | Freigabe |
|---|---|---|---|
| D1 Historie | R038, R196 | Phasenname bzw. Befund-Nummern mit Datum und Projektnamen im Regeltext (`docs/skill-quality.md`, Abschnitt Inhalt); die Regeln dahinter bleiben (R037, R195) | Herbert 28.10.2026 |

Keine weitere DROP-Gruppe. Alles andere wandert (MOVE), wird neutral (REWRITE) oder geht in einer Doppelung auf (MERGE:
R042, R066, R074, R103, R107).

## Verweise von außen

| Stelle | Verweis | Wann und wohin korrigieren |
|---|---|---|
| `skills/mockup-erstellen/SKILL.md` Z. 56–59, Z. 86, Z. 223 | „Mockup-Hook (Deep + UI + Profil „Mockup-Pflicht: ja“)“; „Pflicht-Branch aus dem Code-Profil“ | „Mockup-Hook“ bleibt als Begriff in S#Anfrage klassifizieren. „Mockup-Pflicht: ja“ → `Code.Mockup-Policy` und „Code-Profil“ → Skill-Profil: im selben Commit (Safe Patch) oder als Merker für einen späteren mockup-erstellen-Patch |
| `skills/tracker/references/anker-system.md` Z. 7, 82, 85 | „`code-erstellen` (Auto-Anker) hat lokale Kopie“ | Kopie liegt dann in `skills/code-erstellen/references/cowork.md`; Pfad im tracker-Schritt von Phase 6 nachziehen (dort auch „Phase 1“) |
| `skills/tracker/SKILL.md` Z. 412; `references/batch-protocol.md` 6.2 | Auswahlfrage nach Commit, kein Batch | unverändert gültig |
| `skills/doc-pflege/SKILL.md` Z. 208–212 | DocMaintenanceHints | Begriff bleibt; unverändert |
| `skills/audit/SKILL.md` Z. 28–30, 101–103, 402 | Stack-Referenzen `skills/code-erstellen/references/stacks/<key>.md`; „Code-Profil“ | Pfad bleibt gültig; „Code-Profil“ im audit-Schritt von Phase 6 |
| `skills/ticket/SKILL.md` Z. 115, 118, 154 | „Mockup-Pflicht des Projekts“, „Auslieferung nach dem Code-Profil“ | im ticket-Schritt von Phase 6 → `Code.Mockup-Policy`, `Code.Auslieferung` |
| `skills/projekt-anlegen/references/stacks/home-assistant.md` Z. 83 | Stack-Reference `typescript-lit`, „Typische Fehler“ | Überschrift bleibt; unverändert gültig |
| `skills/projekt-anlegen/references/stacks/python.md` Z. 4 | `skills/code-erstellen/references/stacks/python.md` | unverändert gültig |
| `skills/chat-wechsel/references/beispiele.md` Z. 32, 68 | „code-erstellen nach Code-Profil“, „Quickload-First-Pass“ | Zitat aus dem Heidi-Bauplan bzw. BPM-Regeln (Beispielwerte); unverändert |
| `INDEX.md` Z. 23, 40, 52–58, 63 | Name, Konfliktpaare, Z. 56 „mach BSM-002“ | nur bei Änderung der Description-Beispiele (E2) Z. 56 angleichen |
| `README.md` Z. 277 | „Code-Profil in der CLAUDE.md des Projekts“ | im selben Commit → „Skill-Profil“ (Doku-Check: Aufbau unverändert, Text veraltet) |
| `README.md` Z. 338 | `references/` mit `stacks/` | um `beispiele.md`, `cowork.md` ergänzen (selber Commit) |
| `docs/chat-anker-konzept.md` Z. 6, 213 | code-erstellen „Phase 1 Auto-Anker“ | Konzept-Archiv, unverändert |
| `quality/evals/code-erstellen-real-task-id`, `-real-weiter-mit` | Prompts mit BSM-IDs | Nutzertext, unverändert; Routing-Eval `--tag code-erstellen` nach dem Umbau |

Keine Stelle außerhalb des Skills verweist auf die Schrittnummern (1–10, 7b, 7c, 9b); die Umbenennung in benannte
Schritte hat außen keine Folgen.

## Entscheidungen

- **E1 Zielstruktur:** umgesetzt; kein Split.
- **E2 Description:** „Code-Profil“ → „Skill-Profil“ (1014 Zeichen); „mach BSM-002“, „weiter mit BSM-014“ bleiben.
- **E3 Notiz-Ort:** auf `Code.Befund-Ort` abgebildet; der Rückfall-Satz in S#Voraussetzung: Skill-Profil erklärt es.
- **E4 Stack-Schlüssel `home-assistant`:** nicht in diesem Umbau; Skill-Issue (Profile nennen `home-assistant`, der Skill
  hat `stacks/home-assistant-yaml.md`; bis dahin greift R058).
- **E5 Widerspruch `stacks/home-assistant-yaml.md` ↔ `/config/CLAUDE.md` (Automationen in Paketen):** nicht in diesem
  Umbau; Skill-Issue.
- **E6 Kopf-Limits:** neutral in S#Modus-Übersicht.

## Prüfung

- **Alt→Neu:** R001–R196 haben einen Zustand; 99 Regelkerne per Skript im neuen Text gefunden (KEEP, MOVE, REWRITE), die
  übrigen Zeilen durch Lesen der Abschnitte; „Phase 1“, `chat-anker-konzept`, FE-0001/FE-0027 und „Code-Profil“ (außer
  als Rückfall) kommen nicht mehr vor.
- **Neu→Alt:** Sätze mit Pflichtwörtern, Tabellenzeilen und VERBOTEN-Punkte des neuen Stands gehören zu einer ID oder zu
  N001–N005 (Profil-Version ≠ 1 → N002; Hinweis „Kopf und Langform zählen nur Docs mit Kopf“ → R119; Shell im Cowork-Chat
  → R030; Zeile Frühphasen-Prinzip in B → R082/R141).
- **Qualität:** `SKILL.md` 422 Zeilen (Körper 404); References mit Inhaltsverzeichnis ab 100 Zeilen; Projektwerte nur in
  `beispiele.md` und als „Beispiel BPM/Heidi“ in den Stack-Referenzen; keine Historie; Werkzeugnamen der Cowork-Umgebung
  nur in `cowork.md`; Verweise über Abschnittsnamen statt Schrittnummern. Description 1014 Zeichen.
- **Prüfskript:** läuft nach dem Push per GitHub Actions (kein PowerShell auf dem HA).
- **Routing-Eval:** offen (`--tag code-erstellen` nach dem Commit).
