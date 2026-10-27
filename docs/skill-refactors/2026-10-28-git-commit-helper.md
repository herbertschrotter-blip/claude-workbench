# Regel-Inventar – git-commit-helper, Phase 6 (2026-10-28)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Entscheidungen
- Verweise von außen
- Prüfung

## Kopf

- **Skill:** `skills/git-commit-helper/`
- **Stand vor dem Umbau:** `main` 3f0519d, v0.60.9; `SKILL.md` 312 Zeilen (Körper 301), keine references;
  `scripts/checks.py` 493 Zeilen und `scripts/tests/test_checks.py` (nicht Teil des Umbaus, nur Verweise geprüft)
- **Anlass:** Umbau Phase 6 (ClickUp 123ztrcxedq). Größe erfüllt; offen sind der Abschnitt „Skill-Profil (PFLICHT vor
  Schritt 1)“ statt „Voraussetzung: Skill-Profil“ (Feldtabelle, „Fehlende Werte“, `none`), das ältere `## Commit-Profil`
  mit Heidi-Pfad als Codeblock im Kern, Projektbeispiele (Doku-Checklisten BPM/Heidi, „Bauplan-Schritt“,
  `skills/**`-Versionsregel), Querverweise über Nummern („Schritt 1b“, „Schritt 3“, „vor Schritt 2“, „siehe Schritt 2“,
  „Schritt 9 seiner Load Order“), nummerierte Regeln mit Doppelungen, Werkzeugnamen (Desktop Commander,
  `ask_user_input_v0`, `AskUserQuestion`) und Cowork-Regeln im Kern. Keine Historie im Regeltext gefunden.
- **Vorgänger:** `docs/skill-refactors/2026-09-28-git-commit-helper.md` (Phase 5; R045 dort: „Projektbeispiele bleiben bis
  Phase 6“).
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem HA nicht (kein PowerShell); Kandidaten von Hand
  aus dem alten Text, Prüfung nach dem Push per GitHub Actions.
- **Entscheidungen Herbert 28.10.2026:** Zielstruktur wie vorgeschlagen (neu `references/beispiele.md` und
  `references/cowork.md`). E1: Description „aus dem Projektprofil“ → „aus dem Skill-Profil“. E2: `Commit.Format` wird
  gelesen; Standard bleibt, ein abweichendes Format gilt, `none` = Commit ohne Versions- und Modulteil. E3: Doppelungen
  der Regeln zusammenführen. E4: kein Split, Überschrift „Prüfläufe vor dem Commit“ bleibt exakt. `scripts/` unverändert.

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `B` = `references/beispiele.md`, `C` = `references/cowork.md`.

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Git Commit Helper · Vorrang / Delegation an andere Skills · Grundsätze · **Voraussetzung: Skill-Profil** (statt „Skill-Profil (PFLICHT vor Schritt 1)“: Feldtabelle, Quellen v1 → `## Commit-Profil` → „Fehlende Werte“, `none` je Feld, `ref:`) · **Commit-Format (Standard)** (statt „Commit-Format (VERBINDLICH, in allen Projekten gleich)“) mit Typen · **Ablauf** mit benannten Schritten: Arbeitsverzeichnis · Git-Status · Versionsdatei hochzählen · **Doku-Check vor dem Commit** (aus SCHRITT 1b + SCHRITT 3) · Commit-Befehle (One-Block-Regel) mit PowerShell, Bash, Regeln für die Sequenz, **Prüfläufe vor dem Commit** (Überschrift unverändert, wird von außen verlinkt), Wenn ein Glied der Sequenz fehlschlägt, Mehrzeilig nur wenn User explizit darum bittet · Regeln (ohne Nummern, nur was nicht schon oben steht) · **Fall → Reference** (neu) · VERBOTEN |
| `references/beispiele.md` (neu, 68 Zeilen) | Inhalt · Älteres Commit-Profil (Block mit Heidi-Versionsquelle) · Aufgabennummer im Kurztitel · Versionsregel (Vorabversion, `skills/**`) · Doku-Check (Checkliste ADR/Quickload BPM, Checkliste Bauplan/Übergabe Heidi) · Commit ohne Format (HA-Konfigurationsordner) |
| `references/cowork.md` (neu, 17 Zeilen) | Shell im Cowork-Chat (Desktop Commander; Sequenz kopiert der Nutzer) · Shell am Windows-PC (PowerShell) · Prüfläufe im Cowork-Chat (Checks als erste Glieder) |

Ergebnis: `SKILL.md` 312 → 301 Zeilen (Körper 290), `beispiele.md` 68, `cowork.md` 17. Die Schritte des Ablaufs sind
`###` unter `## Ablauf`, die Unterabschnitte von „Commit-Befehle“ `####`; die Überschriftentexte von „Prüfläufe vor dem
Commit“, „Regeln für die Sequenz“, „Wenn ein Glied der Sequenz fehlschlägt“ und „Mehrzeilig …“ sind unverändert.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter (Z. 3–10) | Description (526 Zeichen) | REWRITE | S#Frontmatter | E1: „Projektprofil“ → „Skill-Profil“, 525 Zeichen | | ✅ sinngemäß |
| R002 | S#Vorrang (Z. 19–21) | Zuständig für Commit-Befehle, Messages, Bumps; sonst delegieren | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R003 | S#Vorrang (Z. 23–29) | Delegationstabelle (5 Zeilen) | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R004 | S#Vorrang (Z. 31–33) | Nur bei Commit-Erstellung selbst zuständig | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R005 | S#Vorrang (Z. 35–39) | Inline-Commit-Vorschlag von code-erstellen („Schritt 9 seiner Load Order“) ist kein Auslöser; erst bei ausdrücklichem Wunsch oder Delegation | REWRITE | S#Vorrang / Delegation an andere Skills | Verweis über Überschrift: `skills/code-erstellen/SKILL.md`, Abschnitt „Commit und Doku-Hinweise“ (neuer Name aus dem parallelen Umbau von code-erstellen) | | ✅ sinngemäß |
| R006 | S#Grundsätze (Z. 45) | Fragen nur bei offener Entscheidung, als Auswahlfrage | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R007 | S#Grundsätze (Z. 46) | Typische Stelle: Typ unklar | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R008 | S#Grundsätze (Z. 47) | Typische Stelle: Version-Bump unklar | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R009 | S#Grundsätze (Z. 48) | Typische Stelle: Wert fehlt im Skill-Profil („Abschnitt ‚Skill-Profil‘ unten“) | REWRITE | S#Grundsätze | Verweis auf „Voraussetzung: Skill-Profil“ | | ✅ sinngemäß |
| R010 | S#Grundsätze (Z. 50–51) | Prosa nur bei offener Frage ohne feste Optionen oder signalisierter Präferenz | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R011 | S#Grundsätze (Z. 52–55) | Branch nach Branch-Policy (`current`, `fixed:`, ohne Shell, ohne Profil); nie automatisch | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R012 | S#Grundsätze (Z. 56–60) | Push nach Push-Policy (4 Werte) | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R013 | S#Grundsätze (Z. 62) | Ohne Push-Policy bleibt `git push origin <branch>` in der Sequenz | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R014 | S#Commit-Format (Z. 64–68) | Format `[vX.Y.Z] Modul, Typ: Kurztitel` verbindlich, in allen Projekten gleich | REWRITE | S#Commit-Format (Standard) | E2: Standard; `Commit.Format` kann abweichen (N004) | | ✅ sinngemäß |
| R015 | S#Commit-Format (Z. 70–71) | Je Projekt Versionsquelle, Versionsregel, Doku-Checkliste aus dem Skill-Profil | REWRITE | S#Commit-Format (Standard) | Feldnamen `Commit.Versionsquelle`, `Commit.Versionsregel`, `Commit.Doku-Check`, Verweis auf Voraussetzung | | ✅ sinngemäß |
| R016 | S#Commit-Format (Z. 73–75) | Aufgaben-/Ticket-Nummer an den Anfang des Kurztitels oder in die zweite Zeile, nie vor `[vX.Y.Z]` (z. B. Bauplan-Schritt, ClickUp-ID) | REWRITE | S#Commit-Format (Standard); B#Aufgabennummer im Kurztitel | Regel wörtlich, Beispiel neutral („Aufgaben- oder Ticket-ID“); Bauplan-Schritt nach B | | ✅ sinngemäß |
| R017 | S#Commit-Format (Z. 77–80) | Modul aus der Modul-Liste; mehrere → Hauptmodul, Rest im Kurztitel; unabhängig → zwei Commits | REWRITE | S#Commit-Format (Standard) | „aus `Commit.Module`“ | | ✅ sinngemäß |
| R018 | S#Commit-Format (Z. 82–84) | Zweite Zeile optional, 1–3 Sätze (Ticket, Bauplan-Abschnitt); nie Prosa in der ersten Zeile | REWRITE | S#Commit-Format (Standard) | „Bauplan-Abschnitt“ → „Doku-Abschnitt“ | | ✅ sinngemäß |
| R019 | S#Typen (Z. 86–94) | Typ → Bump-Zuordnung (8 Typen) | KEEP | S#Typen | wörtlich | | ✅ |
| R020 | S#Typen (Z. 96–99) | Zuordnung ist Standard; Versionsregel darf überschreiben (Beispiele Vorabversion, `skills/**`) | REWRITE | S#Typen; B#Versionsregel | Kern: „`Commit.Versionsregel` darf sie überschreiben“; beide Beispiele wörtlich nach B | | ✅ sinngemäß |
| R021 | S#Typen (Z. 101–104) | Version aus der Versionsquelle ermitteln (Directory.Build.props, package.json, pom.xml, INDEX.md; `changelog:` oberster Eintrag) | KEEP | S#Typen | Stack-Beispiele allgemein, kein Projektwert | | ✅ |
| R022 | S#Skill-Profil (Z. 106–109) | Alles Projektspezifische im Repo; Quellen in fester Reihenfolge; „PFLICHT vor Schritt 1“ | REWRITE | S#Voraussetzung: Skill-Profil | Überschrift wie chat-wechsel, ohne Schrittnummer | | ✅ sinngemäß |
| R023 | S#Skill-Profil (Z. 111–113) | Quelle 1: `## Skill-Profil`, Bereich Commit, `Branch-Policy`, `### Checks` | REWRITE | S#Voraussetzung: Skill-Profil | als Feldtabelle (N001) | | ✅ sinngemäß |
| R024 | S#Skill-Profil (Z. 114–122) | Quelle 2: älteres `## Commit-Profil` (Block mit `dreame_x60/card/package.json`), Feldzuordnung | REWRITE | S#Voraussetzung: Skill-Profil; B#Älteres Commit-Profil | Kern: Rückfall + Zuordnung in einem Satz (Modul-Namen → Module, Bump-Regel → Versionsregel, Doku-Checkliste → Doku-Check); Block wörtlich nach B | | ✅ sinngemäß |
| R025 | S#Skill-Profil (Z. 123–126) | Quelle 3: Repo durchsuchen (docs/, *.md, Versionsdateien), Vorschlag zeigen | REWRITE | S#Voraussetzung: Skill-Profil | gilt, wenn das Profil ganz fehlt (`docs/skill-profile-v1.md#Fehlende Werte`) | | ✅ sinngemäß |
| R026 | S#Skill-Profil (Z. 127–129) | Auswahlfrage: Profil anlegen / Einmalig angeben / Abbrechen | REWRITE | S#Voraussetzung: Skill-Profil | nach „Fehlende Werte“: je fehlendes Feld *Profil ergänzen* / *Wert einmalig nennen* / *Abbrechen*; Profil ganz fehlt → Vorschlag aus R025, anlegen nur mit Zustimmung | | ✅ sinngemäß |
| R027 | S#Skill-Profil (Z. 131–132) | Profil nie aus dem Gedächtnis; einmal gelesen gilt es für die Sitzung | KEEP | S#Voraussetzung: Skill-Profil | wörtlich | | ✅ |
| R028 | S#SCHRITT 0 (Z. 134–139) | Arbeitsverzeichnis = Repo-Wurzel per `git rev-parse --show-toplevel` in der Shell der Umgebung (Claude Code: Bash/PowerShell; Cowork: Desktop Commander); Worktree | REWRITE | S#Arbeitsverzeichnis (PFLICHT); C#Shell im Cowork-Chat | Überschrift ohne Nummer; Desktop Commander nach C | | ✅ sinngemäß |
| R029 | S#SCHRITT 1 (Z. 141–147) | `git status --short`; kein Commit ohne Status | REWRITE | S#Git-Status | nur Überschrift ohne Nummer | | ✅ sinngemäß |
| R030 | S#SCHRITT 1a (Z. 149–155) | Versionsquelle auf neue Nummer setzen, im selben Commit; ohne das kein neues `[vX.Y.Z]` | REWRITE | S#Versionsdatei hochzählen (PFLICHT bei Version-Bump) | Überschrift ohne Nummer; `none` → N003 | | ✅ sinngemäß |
| R031 | S#SCHRITT 1b (Z. 157–161) | Doku-Checkliste vor der Commit-Sequenz, damit Code, Version und Doku in einem Commit landen | MERGE | S#Doku-Check vor dem Commit (PFLICHT) | R054; die Zeigersätze „Schritt 3 beschreibt …, vor Schritt 2“ entfallen mit der Zusammenlegung | | ✅ sinngemäß |
| R032 | S#SCHRITT 2 (Z. 163–169) | One-Block-Regel; in Claude Code dieselbe Sequenz als ein Aufruf | REWRITE | S#Commit-Befehle (One-Block-Regel) | Überschrift ohne Nummer | | ✅ sinngemäß |
| R033 | S#SCHRITT 2 (Z. 171–172) | Push-Glied nur nach Push-Policy | KEEP | S#Commit-Befehle (One-Block-Regel) | wörtlich | | ✅ |
| R034 | S#PowerShell (Z. 174–180) | PowerShell-Vorlage mit `;`, „Default, Windows“ | REWRITE | S#PowerShell (Windows); C#Shell am Windows-PC | „(Windows)“; Vorlage nach der Shell, in der die Sequenz läuft; „Default“ als Cowork-Fall nach C | | ✅ sinngemäß |
| R035 | S#Bash (Z. 182–188) | Bash-Vorlage mit `&&` | KEEP | S#Bash (Linux/macOS, WSL, Git Bash) | wörtlich | | ✅ |
| R036 | S#Regeln für die Sequenz (Z. 192) | Spezifische Pfade nach `git add` | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R037 | S#Regeln für die Sequenz (Z. 193) | Ein Commit pro logische Änderung | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R038 | S#Regeln für die Sequenz (Z. 194) | `"` für Commit-Messages | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R039 | S#Regeln für die Sequenz (Z. 195) | `git log -1 --format="%h %s"` am Ende | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R040 | S#Regeln für die Sequenz (Z. 196) | Renames: `git mv` vor `git add` | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R041 | S#Regeln für die Sequenz (Z. 197) | Branch nach den Grundsätzen, nie hartkodiert `main` | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R042 | S#Regeln für die Sequenz (Z. 198–200) | Passende Pre-Commit-Checks vor dem Commit; ohne Profil Testbefehl der CLAUDE.md; rot → kein Commit | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R043 | S#Prüfläufe (Z. 204) | Checks laufen auf der Maschine; Laufzeit ist Wartezeit | KEEP | S#Prüfläufe vor dem Commit | Überschrift bleibt (Verweise von außen) | | ✅ |
| R044 | S#Prüfläufe (Z. 206–211) | Claude Code: `scripts/checks.py --vor-commit`, Exit-Codes 0–3, Tabelle unverändert melden, Log bei Rot, ohne Python von Hand | KEEP | S#Prüfläufe vor dem Commit | Pfad zum Skript gültig | | ✅ |
| R045 | S#Prüfläufe (Z. 213–216) | Nur passende Checks; ohne Pfad-Muster immer; übersprungene ausdrücklich melden | KEEP | S#Prüfläufe vor dem Commit | | | ✅ |
| R046 | S#Prüfläufe (Z. 217–222) | Auswahl und Eingaben; Nachweis-Datensatz; fehlerhafte Angaben → Exit 3; `--immer` | KEEP | S#Prüfläufe vor dem Commit | | | ✅ |
| R047 | S#Prüfläufe (Z. 223–225) | Gleichzeitig oder nacheinander (Ressourcen), schnelle zuerst | KEEP | S#Prüfläufe vor dem Commit | | | ✅ |
| R048 | S#Prüfläufe (Z. 226–227) | Lange Checks im Hintergrund, Ergebnis vollständig lesen | KEEP | S#Prüfläufe vor dem Commit | | | ✅ |
| R049 | S#Prüfläufe (Z. 228–233) | Meldung als Tabelle mit übersprungenen | KEEP | S#Prüfläufe vor dem Commit | | | ✅ |
| R050 | S#Prüfläufe (Z. 235–236) | Claude Code: Checks vor der Sequenz, Sequenz erst bei Grün | KEEP | S#Prüfläufe vor dem Commit | | | ✅ |
| R051 | S#Prüfläufe (Z. 236–237) | Cowork: passende Checks als erste Glieder, übersprungene vor dem Block nennen | MOVE | C#Prüfläufe im Cowork-Chat; S#Prüfläufe vor dem Commit | wörtlich in C, Hinweiszeile in S | | ✅ |
| R052 | S#Wenn ein Glied fehlschlägt (Z. 241–245) | Abbruch am Glied, Ursache nennen, kein Teil-Commit pushen, dann ganze Sequenz neu | KEEP | S#Wenn ein Glied der Sequenz fehlschlägt | wörtlich | | ✅ |
| R053 | S#Mehrzeilig (Z. 249–251) | Mehrzeilig nur auf Wunsch, in EINEM Block | KEEP | S#Mehrzeilig nur wenn User explizit darum bittet | wörtlich | | ✅ |
| R054 | S#SCHRITT 3 (Z. 253–258) | Doku-Checkliste aus `Doku-Check` (älteres Commit-Profil `Doku-Checkliste:`); vor der Sequenz; jede betroffene Datei nennen, ändern, im selben Commit | REWRITE | S#Doku-Check vor dem Commit (PFLICHT) | Überschrift „Doku-Check vor dem Commit“ statt „SCHRITT 3 — Doc-Pflege Trigger“; ohne Schrittnummern; Rückfall-Hinweis steht in Voraussetzung; `ref:` → N007 | | ✅ sinngemäß |
| R055 | S#SCHRITT 3 (Z. 260–262) | Fehlt die Checkliste: docs/ und *.md auflisten, Auswahlfrage, Ergebnis als Vorschlag fürs Profil | REWRITE | S#Doku-Check vor dem Commit (PFLICHT) | „fehlt“ (nicht `none`, N003) → nach „Fehlende Werte“, die Auflistung ist der Vorschlag | | ✅ sinngemäß |
| R056 | S#SCHRITT 3 (Z. 264–276) | Beispiel-Checkliste (ADR/Quickload, BPM) | MOVE | B#Doku-Check | wörtlich | | ✅ |
| R057 | S#SCHRITT 3 (Z. 278–286) | Beispiel-Checkliste (Bauplan/Übergabe, Heidi) | MOVE | B#Doku-Check | wörtlich | | ✅ |
| R058 | S#Regeln 1 (Z. 290) | Pfade in der Schreibweise der Shell | REWRITE | S#Regeln | ohne Nummer | | ✅ sinngemäß |
| R059 | S#Regeln 2 (Z. 291) | `"` für Messages | MERGE | S#Regeln für die Sequenz | R038 (E3) | | ✅ sinngemäß |
| R060 | S#Regeln 3 (Z. 292) | Ein Commit = eine Änderung | MERGE | S#Regeln für die Sequenz | R037 (E3) | | ✅ sinngemäß |
| R061 | S#Regeln 4 (Z. 293) | Version korrekt hochzählen (Versionsquelle, Versionsregel) | MERGE | S#Versionsdatei hochzählen (PFLICHT bei Version-Bump) | R030 (E3) | | ✅ sinngemäß |
| R062 | S#Regeln 5 (Z. 294) | One-Block-Regel („siehe Schritt 2“) | MERGE | S#Commit-Befehle (One-Block-Regel) | R032 (E3) | | ✅ sinngemäß |
| R063 | S#Regeln 6 (Z. 295) | Keine Erklärungen | REWRITE | S#Regeln | ohne Nummer | | ✅ sinngemäß |
| R064 | S#Regeln 7 (Z. 296) | Bei Renames: git mv | MERGE | S#Regeln für die Sequenz | R040 (E3) | | ✅ sinngemäß |
| R065 | S#Regeln 8 (Z. 297) | Arbeitsverzeichnis immer automatisch | MERGE | S#Arbeitsverzeichnis (PFLICHT) | R028 (E3) | | ✅ sinngemäß |
| R066 | S#Regeln 9 (Z. 298) | Doc-Pflege immer vor dem Commit | MERGE | S#Doku-Check vor dem Commit (PFLICHT) | R054 (E3) | | ✅ sinngemäß |
| R067 | S#Regeln 10 (Z. 299) | Skill-Profil immer lesen, bevor Version oder Doku angefasst werden | MERGE | S#Voraussetzung: Skill-Profil | R027 (E3) | | ✅ sinngemäß |
| R068 | S#Regeln 11 (Z. 300) | Versionsdatei im selben Commit wie die Nummer | MERGE | S#Versionsdatei hochzählen (PFLICHT bei Version-Bump) | R030 (E3) | | ✅ sinngemäß |
| R069 | S#Regeln 12 (Z. 301) | Mehrere Commits: je Commit ein Block | REWRITE | S#Regeln | ohne Nummer | | ✅ sinngemäß |
| R070 | S#VERBOTEN (Z. 305) | Branch automatisch annehmen | KEEP | S#VERBOTEN | | | ✅ |
| R071 | S#VERBOTEN (Z. 306) | Pushen gegen die Push-Policy | KEEP | S#VERBOTEN | | | ✅ |
| R072 | S#VERBOTEN (Z. 307) | Prosa-Fragen bei festen Optionen | KEEP | S#VERBOTEN | | | ✅ |
| R073 | S#VERBOTEN (Z. 308) | Mehrere Code-Blöcke für eine Sequenz („siehe Schritt 2 One-Block-Regel“) | REWRITE | S#VERBOTEN | Verweis über Überschrift „Commit-Befehle (One-Block-Regel)“ | | ✅ sinngemäß |
| R074 | S#VERBOTEN (Z. 309) | Erklärungen zwischen den Befehlen | KEEP | S#VERBOTEN | | | ✅ |
| R075 | S#VERBOTEN (Z. 310) | Versionsquelle oder Doku-Dateien raten | KEEP | S#VERBOTEN | | | ✅ |
| R076 | S#VERBOTEN (Z. 311) | Werkzeugnamen fest verdrahten (Desktop Commander, ask_user_input_v0, AskUserQuestion) | REWRITE | S#VERBOTEN | Regel bleibt, Beispiele ohne Namen („Frage- oder Shell-Werkzeug einer Umgebung“) | | ✅ sinngemäß |
| R077 | S#VERBOTEN (Z. 312) | Checks ohne passende Datei ausführen oder übersprungene verschweigen | KEEP | S#VERBOTEN | | | ✅ |
| N001 | – | Feldtabelle: `Commit.Format`, `Commit.Module`, `Commit.Versionsquelle`, `Commit.Versionsregel`, `Commit.Push-Policy`, `Commit.Pre-Commit-Checks`, `Commit.Doku-Check`, `Branch-Policy`, `### Checks` – je Feld wofür | NEW | S#Voraussetzung: Skill-Profil | `docs/skill-profile-v1.md`, Pflichtfelder je Skill (Doku-Check dort nicht Pflicht, wird aber gelesen) | | ✅ |
| N002 | – | Quellen: v1 → älteres `## Commit-Profil` → „Fehlende Werte“; Profil-Version ≠ 1 → nicht weiterarbeiten | NEW | S#Voraussetzung: Skill-Profil | wie chat-wechsel v0.60.8; nimmt R022–R026 auf | | ✅ |
| N003 | – | `none` ist gültig: Versionsquelle `none` → kein Versionsteil, keine Versionsdatei; Module `none` → kein Modul; Pre-Commit-Checks `none` → keine; Doku-Check `none` → kein Doku-Check, keine Rückfrage | NEW | S#Voraussetzung: Skill-Profil | bisher ungeregelt; betrifft z. B. das Profil von `/config` (Format, Module, Versionsquelle, Doku-Check `none`) | | ✅ |
| N004 | – | `Commit.Format`: gleich dem Standard → Standard; anderes Format → dieses; `none` → `Typ: Kurztitel` ohne Versions- und Modulteil | NEW | S#Commit-Format (Standard); S#Voraussetzung: Skill-Profil | E2 | | ✅ |
| N005 | – | Tabelle Fall → Reference (Beispielwerte, Cowork-Chat) | NEW | S#Fall → Reference | Verweis je Reference | | ✅ |
| N006 | – | `references/beispiele.md`: Werte BPM/Heidi/Skill-Repo als Beispiel, gilt nur das eigene Profil | NEW | B | nimmt R016, R020, R024, R056, R057 auf | | ✅ |
| N007 | – | `ref:` in `Doku-Check` oder `Versionsregel`: den verwiesenen Abschnitt lesen | NEW | S#Voraussetzung: Skill-Profil | Schema erlaubt `ref:` für beide Felder | | ✅ |
| N008 | – | `references/cowork.md`: Shell im Cowork-Chat ist Desktop Commander; die Sequenz kopiert der Nutzer als einen Block in seine Shell | NEW | C | nimmt R028, R034, R051 auf; deckt sich mit `skills/skill-neu/references/cowork.md` | | ✅ |

## DROP-Gruppen

Keine. Es entfällt keine Regel; die Doppelungen der nummerierten Regeln sind MERGE (E3), die Zeigersätze von SCHRITT 1b
gehen in R054 auf.

## Entscheidungen

Alle am 28.10.2026 so freigegeben, wie hier vorgeschlagen.

- **E1 Description:** „aus dem Projektprofil“ → „aus dem Skill-Profil“ (525 Zeichen statt 526). Sonst keine Projektwerte
  drin. Ändern heißt Routing-Eval `--tag git-commit-helper`. Vorschlag: ändern (verbotener Begriff laut Feste Begriffe).
- **E2 `Commit.Format`:** Das Feld ist laut `docs/skill-profile-v1.md` Pflichtfeld für git-commit-helper, der Skill sagt
  „fest, in allen Projekten gleich“ und liest es nicht. Vorschlag: Format bleibt Standard; das Feld wird gelesen – gleich
  dem Standard → wie bisher; `none` (z. B. `/config`) → kein Versions- und Modulteil, nur „Typ: Kurztitel“ bzw. freie
  Kurzzeile; abweichendes Format → dieses gilt.
- **E3 Regeln-Liste:** Doppelungen zusammenführen (Vorschlag, R059–R068 MERGE, Liste behält R058, R063, R069) oder die
  Liste wörtlich ohne Nummern behalten wie bei chat-wechsel (dann alle REWRITE, ~9 Zeilen mehr).
- **E4 Split:** Kein Split nötig (301 Zeilen Körper). „Prüfläufe vor dem Commit“ (~35 Zeilen, nur Claude Code + Skript)
  könnte nach `references/pruefläufe.md`, Vorschlag aber: bleibt im Kern, weil Überschrift von `code-erstellen` und
  `checks.py` verlinkt ist und es der Kern der Commit-Voraussetzung ist.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/code-erstellen/SKILL.md` (Abschnitt Tests) | `skills/git-commit-helper/SKILL.md#Prüfläufe vor dem Commit`, `…/scripts/checks.py` | bleibt gültig (Überschrift und Pfad unverändert) |
| `skills/git-commit-helper/scripts/checks.py` Z. 6 | Docstring „Abschnitt ‚Prüfläufe vor dem Commit‘“ | bleibt gültig |
| `skills/audit/references/grundsatz/home-assistant.md` Z. 104 | Datensatz des Prüfskripts (`skill-checks.json`) | bleibt gültig |
| `skills/code-erstellen/SKILL.md` (Abschnitt Commit und Doku-Hinweise) | früher „Commit-Profil“, „Bump-Regel“ | im parallelen Phase-6-Umbau von code-erstellen schon auf `Commit.*` umgestellt (Arbeitsstand 28.10.) |
| `skills/doc-pflege/SKILL.md` Z. 121, 218; `skills/ticket/SKILL.md` Z. 123 | „Doku-Checkliste des (älteren) Commit-Profils“ | passt zum Rückfall; beim jeweiligen Phase-6-Schritt |
| `README.md` Z. 285 | Skill-Tabelle „(Commit-Profil)“ | Docs-Commit nach dem Umbau: „(Skill-Profil)“ |
| `INDEX.md` Z. 25, 53 | Zuständigkeit, Konfliktpaar code-erstellen | unverändert; bei E1 prüfen, ob die Auslöser gleich bleiben |
| `docs/skill-profile-v1.md` Z. 142, 167 | Prüfskript; Pflichtfelder inkl. `Commit.Format` | passt; bei E2 „Format“ ggf. erläutern |
| tracker, cc-steuerung, projekt-anlegen, ticket, skill-neu, audit, doc-pflege | nur Skillname | keine Abschnitte oder Nummern |
| Gegenrichtung: R005 | „Schritt 9 seiner Load Order“ in code-erstellen | wird Verweis über die Überschrift „Commit und Doku-Hinweise“ (Name aus dem parallelen Umbau von code-erstellen; bleibt die alte Überschrift, hier nachziehen) |

Keine Stelle verweist auf SCHRITT- oder Regel-Nummern von git-commit-helper; Umbenennen der Schritte ohne Folgen.
Evals mit Bezug: `quality/evals/commit-command`, `commit-version-bump`, `commit-no-trigger-push`, `skill-pflege-typo`.

## Prüfung

- **Alt→Neu:** R001–R077 haben einen Zustand (KEEP 38, MOVE 3, MERGE 10, REWRITE 26, DROP 0); jeder Neu-Ort ist im
  neuen Text vorhanden. Die MERGE-Ziele tragen den Inhalt: R059→R038, R060→R037, R061→„Die neue Nummer folgt aus dem
  Typ und `Commit.Versionsregel`“, R062→R032, R064→R040, R065→„Claude ermittelt es immer selbst, ohne zu fragen“,
  R066→R054, R067→„Claude liest es, bevor Version, Doku oder Commit-Sequenz angefasst werden“, R068→R030, R031→R054.
- **Neu→Alt:** Jede geänderte oder neue Zeile im Diff von `SKILL.md` und jede Aussage in `beispiele.md` und `cowork.md`
  gehört zu einer ID oder zu N001–N008. Gepatcht mit einem Skript, das bei fehlendem Originaltext abbricht.
- **Qualität:** `SKILL.md` 301 Zeilen; References unter 100 Zeilen (`beispiele.md` trotzdem mit Inhaltsverzeichnis);
  BPM, Heidi, Bauplan, `dreame_x60` und `skills/**` nur noch in `beispiele.md`; Werkzeugnamen (Desktop Commander) nur in
  `cowork.md`; keine Querverweise über Nummern; keine Historie. Description 525 Zeichen.
- **Prüfskript:** läuft auf dem HA nicht; nach dem Push per GitHub Actions.
- **Routing-Eval:** offen (nach dem Commit, `--tag git-commit-helper`, wegen E1 Pflicht).
