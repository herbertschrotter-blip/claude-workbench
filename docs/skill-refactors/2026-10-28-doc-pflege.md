# Regel-Inventar – doc-pflege, Phase 6 (2026-10-28)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Verweise von außen
- Prüfung

## Kopf

- **Skill:** `skills/doc-pflege/`
- **Stand vor dem Umbau:** `main` 3f0519d, v0.60.9 (doc-pflege bis 69e40dc unverändert); `SKILL.md` 432 Zeilen
  (Körper 414), keine references
- **Anlass:** Umbau Phase 6 (ClickUp 123ztrcxedq), Reihenfolge laut `docs/skillsystem-umbau.md`, Abschnitt „Phase 6 – Skill
  für Skill verkleinern“. Größe erfüllt; offen sind Projektwerte (BPM, Heidi) in fast jedem Abschnitt des Kerns
  (Zweck, Voraussetzungs-Tabelle, „Konkrete Pfade“, Doc-Laderegel, Frühphasen-/Paritätsregel, Doku-Hinweise, alle Modi,
  Ausgabeformat, VERBOTEN), Nummernverweise in Projekt-Docs („DOC-STANDARD Kapitel 3/7/8“, „HANDOFF 3e/4/5“,
  „Abschnitt 10/10a“), Cowork-Teile im Kern (DC, SUCHE/ERSETZE, cc-steuerung), Werkzeugnamen (Edit/Write, Bash/PowerShell,
  DC), ein Rückfall „BPM-Weg“ statt „Fehlende Werte“, „Heidi: Startprompt Abschnitt 0“ im Sitzungsabschluss. Historie im
  Regeltext: keine gefunden. Das frühere Inventar `2026-10-22-doc-pflege.md` (Phase 5) hat die Projektwerte ausdrücklich
  bis Phase 6 stehen lassen.
- **Entscheidungen Herbert 28.10.2026:** Zielstruktur „Umsetzen“ (neu `references/beispiele.md` und
  `references/cowork.md`); DROP-Gruppe D1 Skill-Governance freigegeben; R022 Branches ohne Shell über die GitHub-API
  (wie chat-wechsel); R025 „Ohne Push-Policy: Commit + Push“ bleibt (Widerspruch zu „Fehlende Werte“ wird Skill-Issue,
  betrifft auch chat-wechsel); vorgeschlagene neutrale Standard-Ladereihenfolge (Entwurf N006) entfällt; Description
  unverändert.
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem HA nicht (kein PowerShell); Kandidaten von Hand
  aus dem alten Text, Prüfung nach dem Push per GitHub Actions.

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `B` = `references/beispiele.md`, `C` = `references/cowork.md`,
`AV` = `skills/audit/references/doku-validierung.md`.

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Frontmatter (unverändert) · Zweck (neutral, Verweis auf B und C) · Vorrang / Delegation · Grundsätze · Arbeitsverzeichnis (nur Claude Code, Cowork → C) · **Voraussetzung: Skill-Profil** (neu gebaut wie chat-wechsel: Feldtabelle „Feld \| Wofür“, Reihenfolge v1 → älteres `## Doku-Profil` mit Zuordnungstabelle ohne Projektspalten → Router/Standard im Repo → „Fehlende Werte“) · Doc-Laderegel (neutral) · **Projektregeln für Schema-, Config- und Datenänderungen** (statt „Frühphasen-Regel“, neutral) · Doku-Hinweise nach Code-Änderungen · Modi (Projekt-Init, Router nachziehen, Begleit-Docs, Doku pflegen, Neue Doc oder Umbau, Sitzungsabschluss – alle neutral) · Prüfen nach dem Schreiben · Ausgabeformat · References (neu, je ein Verweis) · VERBOTEN |
| `references/beispiele.md` (neu) | Inhalt · Profilwerte BPM und Heidi · Rückfall ohne Profil (BPM) · Pfade BPM · Doc-Laderegel · Schema- und Datenänderungen (Frühphase BPM, Parität Heidi) · Doku-Hinweise · Projekt-Init · Router und Begleit-Docs · Neue Doc · Sitzungsabschluss · Commit |
| `references/cowork.md` (neu) | Skill-Profil und Docs lesen · Arbeitsverzeichnis · Branch · Dateien ändern |

„Konkrete Pfade (Beispiel BPM …)“ entfällt als Kern-Abschnitt (wandert ganz nach B). „Skill-Governance“ entfällt nur bei
Freigabe von D1 (freigegeben). Kein Split nötig: die Modi teilen Voraussetzung und Prüfung.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter (Z. 3–17) | Description | KEEP | S#Frontmatter | wörtlich, 994 Zeichen, keine Projektwerte | | ✅ |
| R002 | S#Zweck (Z. 24–25) | Schreibt, ändert, korrigiert Doku, behebt Audit-Befunde, Sitzungsabschluss; Prüfung ohne Auftrag macht audit | KEEP | S#Zweck | wörtlich | | ✅ |
| R003 | S#Zweck (Z. 25–27) | Welche Docs, Aufbau, Prüfung: Skill-Profil, Bereich Doku | KEEP | S#Zweck | wörtlich | | ✅ |
| R004 | S#Zweck (Z. 27–28) | BPM: Frontmatter, Quickload, Kapitelstruktur nach DOC-STANDARD.md | MOVE | B#Profilwerte BPM und Heidi | im Kern nur Verweis auf B (N003) | | ✅ |
| R005 | S#Zweck (Z. 28–29) | Heidi: Bauplan (Statusliste, Aufgabenkarten, Notizen, PD-Register) und HANDOFF | MOVE | B#Profilwerte BPM und Heidi | |  | ✅ |
| R006 | S#Zweck (Z. 29–30) | Initialisiert neue Projekte mit dem Standard-Doc-Set; erzwingt die Vorlagen des Profils | KEEP | S#Zweck | wörtlich | | ✅ |
| R007 | S#Vorrang (Z. 36–38) | Zuständigkeit Doku; sonst delegieren | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R008 | S#Vorrang (Z. 40–46) | Delegationstabelle (5 Zeilen) | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R009 | S#Vorrang (Z. 48–50) | Echte Doc-Arbeit bleibt hier (Liste mit „INDEX.md-Routing pflegen“) | REWRITE | S#Vorrang / Delegation an andere Skills | „Router-Einträge pflegen“ | | ✅ sinngemäß |
| R010 | S#Vorrang (Z. 52–57) | Doku-Hinweise aus code-erstellen/git-commit-helper sind kein Trigger; User entscheidet | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R011 | S#Grundsätze (Z. 63–64) | Fragen nur bei offener Entscheidung, als Auswahlfrage | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R012 | S#Grundsätze (Z. 68) | Auswahlfrage Modus-Auswahl (6 Modusnamen) | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R013 | S#Grundsätze (Z. 69) | Auswahlfrage Befund beim Prüfen nach dem Schreiben | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R014 | S#Grundsätze (Z. 70) | Auswahlfrage Sitzungsabschluss: fertig / offen (Rest im HANDOFF) / blockiert | REWRITE | S#Grundsätze | „Rest bei den offenen Punkten“ statt HANDOFF | | ✅ sinngemäß |
| R015 | S#Grundsätze (Z. 71) | Auswahlfrage Doc umbauen, Inhalt passt in kein Kapitel | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R016 | S#Grundsätze (Z. 72) | Auswahlfrage Doku-Hinweis nach Code-Änderung | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R017 | S#Grundsätze (Z. 73) | Auswahlfrage Schema-/DB-Änderung dokumentieren (Reset / Migration / Abbrechen) | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R018 | S#Grundsätze (Z. 75–78) | Prosa-Fragen nur bei … (3 Fälle) | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R019 | S#Grundsätze (Z. 79–81) | Branch nach Branch-Policy: `current`, `fixed:<branch>`, ohne Shell | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R020 | S#Grundsätze (Z. 81) | Ohne Skill-Profil: Branch aus Chat-Kontext | REWRITE | S#Grundsätze | wie chat-wechsel: „ein in dieser Sitzung schon bekannter Branch“ | | ✅ sinngemäß |
| R021 | S#Grundsätze (Z. 81–83) | Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC) `git branch --show-current`; älteres Profil mit Pflicht-Branch weicht ab → Auswahlfrage | REWRITE | S#Grundsätze; C#Branch | „Mit Shell“ ohne Werkzeugnamen; Cowork-Shell nach C | | ✅ sinngemäß |
| R022 | S#Grundsätze (Z. 83–84) | Ohne Shell und unbekannt: Auswahlfrage mit Branch-Namen aus `git branch -a` | REWRITE | S#Grundsätze | ohne Shell gibt es kein `git branch -a`: Branches über die GitHub-API auflisten (wie chat-wechsel); Herbert 28.10. | | ✅ sinngemäß |
| R023 | S#Grundsätze (Z. 84) | NIE automatisch einen Branch annehmen | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R024 | S#Grundsätze (Z. 85–88) | Push nach Push-Policy (3 Fälle) im Sitzungsabschluss | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R025 | S#Grundsätze (Z. 90) | Ohne Push-Policy: Commit + Push | KEEP | S#Grundsätze | wörtlich wie chat-wechsel R014; bleibt (Herbert 28.10.), Widerspruch zu „Fehlende Werte“ wird Skill-Issue | | ✅ |
| R026 | S#Arbeitsverzeichnis (Z. 96) | Claude Code: Repo-Wurzel (`git rev-parse --show-toplevel`) | KEEP | S#Arbeitsverzeichnis | wörtlich | | ✅ |
| R027 | S#Arbeitsverzeichnis (Z. 97) | Cowork: Arbeitsverzeichnis nach cc-steuerung, Abschnitt „Arbeitsverzeichnis“ | MOVE | C#Arbeitsverzeichnis | in S ein Satz mit Verweis auf C | | ✅ |
| R028 | S#Voraussetzung (Z. 103–104) | Quelle `## Skill-Profil` der CLAUDE.md; Spezifikation; „Claude Code liest automatisch, Cowork per DC“ | REWRITE | S#Voraussetzung: Skill-Profil; C#Skill-Profil und Docs lesen | DC nach C | | ✅ sinngemäß |
| R029 | S#Voraussetzung (Z. 104–108) | Pflichtfelder (Grundfelder, Doku.Router, Doku.Standard, Doku.Entscheidungs-Ort, Commit.Push-Policy beim Commit) und Felder „wo gesetzt“ | REWRITE | S#Voraussetzung: Skill-Profil | als Feldtabelle „Feld \| Wofür“ (N001); Pflicht/optional bleibt gleich | | ✅ sinngemäß |
| R030 | S#Voraussetzung (Z. 108–109) | Fehlt ein Pflichtfeld oder `fehlt`: Feld nennen, nach „Fehlende Werte“ fragen | KEEP | S#Voraussetzung: Skill-Profil | wörtlich | | ✅ |
| R031 | S#Voraussetzung (Z. 110–111) | Fehlt der Abschnitt: älteres `## Doku-Profil`; Spalte „Skill-Profil“ nennt das Ersatzfeld | REWRITE | S#Voraussetzung: Skill-Profil | Rückfall als Schritt 2 (N002), Hinweis auf die Doku-Checkliste im `## Commit-Profil` | | ✅ sinngemäß |
| R032 | S#Voraussetzung (Z. 113–123) | Zuordnungstabelle Feld → Skill-Profil → Bedeutung (9 Zeilen, inkl. „Frühphasen-Regel: Regel im Router oder Standard“) | REWRITE | S#Voraussetzung: Skill-Profil | Spalten BPM/Heidi raus (R033); „Frühphasen-Regel“ → „Regeln für Schema-/Datenänderungen“ | | ✅ sinngemäß |
| R033 | S#Voraussetzung (Z. 113–123) | Werte BPM und Heidi je Feld (Spalten BPM, Heidi) | MOVE | B#Profilwerte BPM und Heidi | wörtlich als Tabelle | | ✅ |
| R034 | S#Voraussetzung (Z. 125) | Fehlt beides: INDEX.md + DOC-STANDARD.md als Profil (BPM-Weg) | REWRITE | S#Voraussetzung: Skill-Profil; B#Rückfall ohne Profil (BPM) | neutral: Router und Standard des Repos, soweit vorhanden; BPM-Werte nach B | | ✅ sinngemäß |
| R035 | S#Voraussetzung (Z. 126) | Fehlt auch das: Auswahlfrage „Profil anlegen (Vorschlag aus dem Repo)“ / „Ohne Profil, ich nenne die Docs“ | REWRITE | S#Voraussetzung: Skill-Profil | nach „Fehlende Werte“: Profil ergänzen (Vorschlag aus dem Repo) / einmalig nennen / abbrechen; nie raten | | ✅ sinngemäß |
| R036 | S#Konkrete Pfade (Z. 130–144) | Pfadtabelle BPM (11 Dateien) | MOVE | B#Pfade BPM | wörtlich; Kern-Abschnitt entfällt | | ✅ |
| R037 | S#Doc-Laderegel (Z. 150) | Docs nach der Ladereihenfolge des Doku-Profils lesen | REWRITE | S#Doc-Laderegel | „des Standards bzw. Routers (`Doku.Standard`, `Doku.Router`)“ | | ✅ sinngemäß |
| R038 | S#Doc-Laderegel (Z. 152–157) | Ladereihenfolge BPM (DOC-STANDARD Kap. 8, 5 Schritte) | MOVE | B#Doc-Laderegel | wörtlich | | ✅ |
| R039 | S#Doc-Laderegel (Z. 159–164) | Ladereihenfolge Heidi (5 Schritte) | MOVE | B#Doc-Laderegel | wörtlich | | ✅ |
| R040 | S#Frühphasen-Regel (Z. 168–172) | Gilt bei „Frühphasen-Regel: ja“ (BPM, INDEX.md „Projekt-Phase (VERBINDLICH)“) für Schema-/Config-/DB-Doku | REWRITE | S#Projektregeln für Schema-, Config- und Datenänderungen; B#Schema- und Datenänderungen | neutral: „Führt Router oder Standard eine solche Regel, gilt sie“; BPM-Ort nach B | | ✅ sinngemäß |
| R041 | S#Frühphasen-Regel (Z. 174) | Statt Migrations-Kapitel → Reset-Anweisung | REWRITE | S#Projektregeln für Schema-, Config- und Datenänderungen | als Beispiel der häufigsten Regel (Frühphase) | | ✅ sinngemäß |
| R042 | S#Frühphasen-Regel (Z. 176–188) | Format Reset-Anweisung (❌ Migration / ✅ Betroffene Datei, Aktion) mit `bpm.db` | REWRITE | S#Projektregeln für Schema-, Config- und Datenänderungen; B#Schema- und Datenänderungen | Format neutral (Betroffene Datei(en), Aktion) im Kern; ❌/✅-Beispiel wörtlich nach B | | ✅ sinngemäß |
| R043 | S#Frühphasen-Regel (Z. 190–191) | JSON-Configs ebenso: Datei nennen, User löscht, App legt neu an (`profiles/*.json` …) | REWRITE | S#Projektregeln für Schema-, Config- und Datenänderungen; B#Schema- und Datenänderungen | Pfade nach B | | ✅ sinngemäß |
| R044 | S#Frühphasen-Regel (Z. 193–194) | Ausnahme: User sagt „Migration dokumentieren“ oder Kapitel in INDEX.md entfernt | REWRITE | S#Projektregeln für Schema-, Config- und Datenänderungen | „… oder die Regel im Projekt aufgehoben ist“ | | ✅ sinngemäß |
| R045 | S#Frühphasen-Regel (Z. 196–198) | Heidi-Paritätsregel: Abweichung von v1 nur mit freigegebenem PD-Eintrag (10a) | MOVE | B#Schema- und Datenänderungen | im Kern neutral als zweite Art von Projektregel („Abweichung nur mit freigegebenem Eintrag am Entscheidungs-Ort“) | | ✅ |
| R046 | S#Frühphasen-Regel (Z. 198–199) | Heidi: neue Entität/Dienst → Bauplan Abschnitt 4 und `contract.ts` im selben Commit | MOVE | B#Schema- und Datenänderungen | wörtlich | | ✅ |
| R047 | S#Doku-Hinweise (Z. 205–209) | Kein Trigger, kein Modus; Nachlauf-Checkliste anderer Skills; Intent nur in der Description | KEEP | S#Doku-Hinweise nach Code-Änderungen | wörtlich | | ✅ |
| R048 | S#Doku-Hinweise (Z. 212) | DocMaintenanceHints von code-erstellen übernehmen | KEEP | S#Doku-Hinweise nach Code-Änderungen | wörtlich | | ✅ |
| R049 | S#Doku-Hinweise (Z. 213–214) | Nach doc-relevanten Änderungen kurze Merkliste, nicht bei trivialen, ohne zu unterbrechen | KEEP | S#Doku-Hinweise nach Code-Änderungen | wörtlich | | ✅ |
| R050 | S#Quelle der Checkliste (Z. 218–220) | Quelle `Commit.Doku-Check` (älter: Doku-Checkliste des Commit-Profils); keine eigene Liste | KEEP | S#Quelle der Checkliste: `Commit.Doku-Check` | wörtlich | | ✅ |
| R051 | S#Quelle der Checkliste (Z. 220–221) | Beispiel BPM (Tabelle → DB-SCHEMA, Entscheidung → ADR, …) | MOVE | B#Doku-Hinweise | wörtlich | | ✅ |
| R052 | S#Quelle der Checkliste (Z. 222–223) | Beispiel Heidi (Statusliste, Abschnitt 10/10a, HANDOFF 3e, Abschnitt 4 + contract.ts) | MOVE | B#Doku-Hinweise | wörtlich | | ✅ |
| R053 | S#Typische Fälle (Z. 227–234) | Sieben Fälle doc-relevanter Änderungen | REWRITE | S#Typische Fälle (Change-Class-basiert) | „Paritätsabweichung“ → „gewollte Abweichung von einer Projektregel“, „im Vertrag“ raus; Rest wörtlich | | ✅ sinngemäß |
| R054 | S#NICHT triggern bei (Z. 236–243) | Sechs Fälle ohne Hinweis | KEEP | S#NICHT triggern bei: | wörtlich | | ✅ |
| R055 | S#Format (Z. 247, 254–255) | Kurze Merkliste am Ende; nur zutreffende Punkte; User entscheidet | KEEP | S#Format: Advisory (nicht interruptiv) | wörtlich | | ✅ |
| R056 | S#Format (Z. 249–252) | Musterzeilen `📝 Doc-Hinweis: [DB-SCHEMA.md — …]` | REWRITE | S#Format: Advisory (nicht interruptiv); B#Doku-Hinweise | Platzhalter `[<Doc> — <was>]` im Kern, BPM-Zeilen nach B | | ✅ sinngemäß |
| R057 | S#Projekt-Init (Z. 263) | Wann: „neues Projekt“, „init projekt“, kein Doku-Profil und keine INDEX.md | REWRITE | S#Projekt-Init | „kein Bereich Doku und kein Router“ | | ✅ sinngemäß |
| R058 | S#Projekt-Init (Z. 265) | Details: DOC-STANDARD.md Kapitel 3 (BPM) | MOVE | B#Projekt-Init | Nummernverweis bleibt nur als Projektwert in B | | ✅ |
| R059 | S#Projekt-Init (Z. 268) | Grundinfos sammeln | KEEP | S#Projekt-Init | wörtlich | | ✅ |
| R060 | S#Projekt-Init (Z. 269) | Repo scannen | KEEP | S#Projekt-Init | wörtlich | | ✅ |
| R061 | S#Projekt-Init (Z. 270–271) | Bereich Doku anlegen; fehlt das Profil, richtet es projekt-anlegen ein | KEEP | S#Projekt-Init | wörtlich | | ✅ |
| R062 | S#Projekt-Init (Z. 272) | Standard-Doc-Set laut Profil (BPM-Liste, Heidi-artige Liste) | REWRITE | S#Projekt-Init; B#Projekt-Init | Listen wörtlich nach B | | ✅ sinngemäß |
| R063 | S#Projekt-Init (Z. 273) | Vorlagen des Profils (BPM: Frontmatter + Quickload + Kapitelstruktur) | REWRITE | S#Projekt-Init | BPM-Klammer raus (steht in B#Profilwerte) | | ✅ sinngemäß |
| R064 | S#Projekt-Init (Z. 274) | Invarianten-Check | KEEP | S#Projekt-Init | wörtlich | | ✅ |
| R065 | S#Projekt-Init (Z. 275) | Paket dem User vorlegen | KEEP | S#Projekt-Init | wörtlich | | ✅ |
| R066 | S#Router nachziehen (Z. 281) | Wann: neues Doc, umbenannt, neuer Entry Point | KEEP | S#Router nachziehen | wörtlich | | ✅ |
| R067 | S#Router nachziehen (Z. 283) | Router aus `Doku.Router` laden und Eintrag nachziehen | KEEP | S#Router nachziehen | wörtlich | | ✅ |
| R068 | S#Router nachziehen (Z. 283–285) | BPM: INDEX.md Primary/Secondary/Reference; Heidi: CLAUDE.md „Repo-Aufbau“, HANDOFF 5, Plan-Docs | MOVE | B#Router und Begleit-Docs | wörtlich | | ✅ |
| R069 | S#Begleit-Docs (Z. 291) | Wann: Tabelle, Feature, Entscheidung, Abhängigkeit, Entität | KEEP | S#Begleit-Docs | wörtlich | | ✅ |
| R070 | S#Begleit-Docs (Z. 293) | `Commit.Doku-Check` → betroffene Pflicht-Docs ändern | KEEP | S#Begleit-Docs | wörtlich | | ✅ |
| R071 | S#Begleit-Docs (Z. 293–294) | BPM: INDEX.md → Doc-Pflege Policy; Heidi: Abschnitt 4, 10/10a, HANDOFF | MOVE | B#Router und Begleit-Docs | wörtlich | | ✅ |
| R072 | S#Doku pflegen (Z. 300–301) | Wann: „pflege die Doku“, Doku-Fehler, Audit-Befunde | KEEP | S#Doku pflegen | wörtlich | | ✅ |
| R073 | S#Doku pflegen (Z. 303–304) | Alle Pflicht-Docs durchgehen; Audit-Befunde als Aufgabenliste; danach prüfen | KEEP | S#Doku pflegen | wörtlich | | ✅ |
| R074 | S#Neue Doc oder Umbau (Z. 310–312) | Wann (Beispiel „refactore PlanManager.md nach Standard“) | REWRITE | S#Neue Doc oder Umbau | „refactore <Doc> nach Standard“ | | ✅ sinngemäß |
| R075 | S#Neue Doc oder Umbau (Z. 314) | Danach prüfen (Prüfen nach dem Schreiben) | KEEP | S#Neue Doc oder Umbau | wörtlich | | ✅ |
| R076 | S#Neue Doc (Z. 318) | Vorlage für den Doc-Typ aus `Doku.Standard` (BPM Kap. 7; Heidi-Muster) | REWRITE | S#Neue Doc; B#Neue Doc | Klammer nach B | | ✅ sinngemäß |
| R077 | S#Neue Doc (Z. 319) | Router laden → verwandte Docs (BPM INDEX; Heidi CLAUDE.md, HANDOFF 5) | REWRITE | S#Neue Doc; B#Neue Doc | Klammer nach B | | ✅ sinngemäß |
| R078 | S#Neue Doc (Z. 320) | Quickloads verwandter Docs → fachliche Invarianten sammeln | REWRITE | S#Neue Doc | „Kurzfassungen (z. B. Quickload)“ | | ✅ sinngemäß |
| R079 | S#Neue Doc (Z. 321) | Doc mit Frontmatter + Quickload + Kapitelstruktur erstellen | REWRITE | S#Neue Doc | „nach der Vorlage des Standards (z. B. Frontmatter, Quickload, Kapitel)“ | | ✅ sinngemäß |
| R080 | S#Neue Doc (Z. 322–332) | Invarianten-Check: drei Fragen mit Zielorten (Fachliche Invarianten, Pflichtlesen, related_docs) | REWRITE | S#Neue Doc; B#Neue Doc | Fragen wörtlich, Zielorte „wo der Standard sie vorsieht“; BPM-Zielorte nach B | | ✅ sinngemäß |
| R081 | S#Neue Doc (Z. 334) | INDEX.md-Routing-Eintrag vorschlagen | REWRITE | S#Neue Doc | „Router-Eintrag“ | | ✅ sinngemäß |
| R082 | S#Doc umbauen (Z. 338) | Vorlage aus dem Profil (BPM: DOC-STANDARD.md) | REWRITE | S#Doc umbauen | Klammer raus | | ✅ sinngemäß |
| R083 | S#Doc umbauen (Z. 339) | Bestehende Doc komplett laden | KEEP | S#Doc umbauen | wörtlich | | ✅ |
| R084 | S#Doc umbauen (Z. 340) | Inhalt auf die Standard-Kapitel mappen | KEEP | S#Doc umbauen | wörtlich | | ✅ |
| R085 | S#Doc umbauen (Z. 341) | Frontmatter + Quickload ergänzen/aktualisieren | REWRITE | S#Doc umbauen | „Pflichtteile der Vorlage (z. B. Frontmatter, Quickload)“ | | ✅ sinngemäß |
| R086 | S#Doc umbauen (Z. 342) | Invarianten-Check | KEEP | S#Doc umbauen | wörtlich | | ✅ |
| R087 | S#Doc umbauen (Z. 343) | Vollständigkeits-Check gegen das Original | KEEP | S#Doc umbauen | wörtlich | | ✅ |
| R088 | S#Doc umbauen (Z. 345–350) | REFACTORING-INVARIANTE (4 Punkte) | KEEP | S#Doc umbauen | wörtlich | | ✅ |
| R089 | S#Doc umbauen (Z. 352) | VERBOTEN: Doc ohne die Vorlage des Profils (BPM …; Heidi …) | REWRITE | S#VERBOTEN | neutral; Formate BPM/Heidi stehen in B#Profilwerte; Inline-Zeile geht in die VERBOTEN-Liste | | ✅ sinngemäß |
| R090 | S#Doc umbauen (Z. 353) | VERBOTEN: beim Refactoring weglassen, kürzen, zusammenfassen | KEEP | S#Doc umbauen | wörtlich | | ✅ |
| R091 | S#Sitzungsabschluss (Z. 359–360) | Wann: „sitzung abschließen“ …, nach dem letzten `tracker done` | KEEP | S#Sitzungsabschluss | wörtlich | | ✅ |
| R092 | S#Sitzungsabschluss (Z. 360–361) | … oder wenn Bauplan/Profil es am Ende jeder Sitzung verlangt (Heidi: Startprompt Abschnitt 0) | REWRITE | S#Sitzungsabschluss; B#Sitzungsabschluss | „wenn die Doku hinter `Doku.Sitzungsabschluss` es am Ende jeder Sitzung verlangt“; Heidi-Startprompt nach B (wie chat-wechsel v0.60.8) | | ✅ sinngemäß |
| R093 | S#Sitzungsabschluss (Z. 361) | Ersetzt chat-wechsel nicht, liefert zu | KEEP | S#Sitzungsabschluss | wörtlich | | ✅ |
| R094 | S#Sitzungsabschluss (Z. 363) | Orte aus `Doku.Sitzungsabschluss` (älter: Feld „Sitzungsabschluss“) | KEEP | S#Sitzungsabschluss | wörtlich | | ✅ |
| R095 | S#Sitzungsabschluss (Z. 364–366) | Statusliste nachziehen (Heidi: Bauplan 1 ↔ ClickUp DX); unklar → Auswahlfrage fertig/offen/blockiert | REWRITE | S#Sitzungsabschluss; B#Sitzungsabschluss | „Aufgabenquelle ↔ Tracker“; Heidi nach B | | ✅ sinngemäß |
| R096 | S#Sitzungsabschluss (Z. 367–368) | Befunde und Entscheidungen in `Doku.Entscheidungs-Ort` (Heidi 10/10a; BPM ADR/BACKLOG) | REWRITE | S#Sitzungsabschluss; B#Sitzungsabschluss | Klammer nach B | | ✅ sinngemäß |
| R097 | S#Sitzungsabschluss (Z. 369) | Stand-Abschnitt schreiben (Heidi HANDOFF 3e – Version, was gebaut, Stolpersteine; Datum) | REWRITE | S#Sitzungsabschluss; B#Sitzungsabschluss | Inhalt (Version, was gebaut, Stolpersteine, Datum) neutral im Kern, Ort nach B | | ✅ sinngemäß |
| R098 | S#Sitzungsabschluss (Z. 370–371) | Offene Punkte als Checkliste (Heidi HANDOFF 4), abhaken, ergänzen, je mit ClickUp-Bezug oder Begründung | REWRITE | S#Sitzungsabschluss; B#Sitzungsabschluss | „Tracker-Bezug“; Ort nach B | | ✅ sinngemäß |
| R099 | S#Sitzungsabschluss (Z. 372) | `Commit.Doku-Check` durchgehen (Abschnitt 4, INDEX, CHANGELOG) | REWRITE | S#Sitzungsabschluss | Klammer raus | | ✅ sinngemäß |
| R100 | S#Sitzungsabschluss (Z. 373–374) | Commit `[vX.Y.Z] <Doku-Modul>, Docs: Sitzungsabschluss <Datum> – <Kurztitel>` (git-commit-helper); Push nach Push-Policy | REWRITE | S#Sitzungsabschluss | „im `Commit.Format` mit Doku-Modul aus `Commit.Module`, Kurztitel „Sitzungsabschluss <Datum> – …““; Muster als Beispiel nach B#Commit | | ✅ sinngemäß |
| R101 | S#Sitzungsabschluss (Z. 375–376) | Kurzer Abschlussbericht erledigt/offen/nächster Schritt; Einstieg für chat-wechsel | KEEP | S#Sitzungsabschluss | wörtlich | | ✅ |
| R102 | S#Sitzungsabschluss (Z. 378) | VERBOTEN: Sitzung mit uncommitteten Doku-Änderungen beenden | KEEP | S#Sitzungsabschluss | wörtlich | | ✅ |
| R103 | S#Sitzungsabschluss (Z. 378) | VERBOTEN: Statusliste „fertig“ ohne Tests und Commit | KEEP | S#Sitzungsabschluss | wörtlich (zweite Stelle R129 bleibt, Redundanz gewollt) | | ✅ |
| R104 | S#Sitzungsabschluss (Z. 379) | VERBOTEN: offene Punkte nur im Chat | KEEP | S#Sitzungsabschluss | wörtlich | | ✅ |
| R105 | S#Prüfen nach dem Schreiben (Z. 385) | Gilt nach Doku pflegen und Neue Doc oder Umbau, nur für geänderte Docs | KEEP | S#Prüfen nach dem Schreiben | wörtlich | | ✅ |
| R106 | S#Prüfen nach dem Schreiben (Z. 386–387) | Prüfregeln `Doku.Validierungsregeln`; `none` → entfällt; sonst Prüflisten in AV | KEEP | S#Prüfen nach dem Schreiben | wörtlich | | ✅ |
| R107 | S#Prüfen nach dem Schreiben (Z. 388–389) | Eigene Befunde gleich beheben; Rest als Tabelle; mehrere Lösungen → Auswahlfrage | KEEP | S#Prüfen nach dem Schreiben | wörtlich | | ✅ |
| R108 | S#Prüfen nach dem Schreiben (Z. 390) | Nichts stillschweigend korrigieren, was eine Entscheidung des Users ist | KEEP | S#Prüfen nach dem Schreiben | wörtlich | | ✅ |
| R109 | S#Prüfen nach dem Schreiben (Z. 392–393) | Prüfung ohne Änderungsauftrag macht audit (Beispiele u. a. „stimmt der bauplan“) | REWRITE | S#Prüfen nach dem Schreiben | „stimmt die Statusliste“ statt Heidi-Begriff | | ✅ sinngemäß |
| R110 | S#Ausgabeformat (Z. 399) | Claude Code: Dateien direkt ändern (Edit/Write); Cowork: SUCHE/ERSETZE oder DC | REWRITE | S#Ausgabeformat; C#Dateien ändern | Handlung statt Werkzeug; Cowork-Teil nach C | | ✅ sinngemäß |
| R111 | S#Ausgabeformat (Z. 400) | Neue Docs komplett mit der Vorlage des Profils (BPM: …) | MERGE | S#VERBOTEN | R089 | | ✅ sinngemäß |
| R112 | S#Ausgabeformat (Z. 401–402) | Commit: `Commit.Format`, Modul aus `Commit.Module`, Typ `Docs` (BPM/Heidi-Beispiel) | REWRITE | S#Ausgabeformat; B#Commit | Beispiele nach B | | ✅ sinngemäß |
| R113 | S#Skill-Governance (Z. 408–409) | Bei Skill-Änderung prüfen: Trigger zu breit? | DROP | – | D1 | ✅ 28.10. | ✅ |
| R114 | S#Skill-Governance (Z. 410) | Redundanz zu anderer Skill-Regel? | DROP | – | D1 | ✅ 28.10. | ✅ |
| R115 | S#Skill-Governance (Z. 411) | Negativgrenzen noch korrekt? | DROP | – | D1 | ✅ 28.10. | ✅ |
| R116 | S#Skill-Governance (Z. 412) | DOC-STANDARD / INDEX / Doku-Profil betroffen? | DROP | – | D1 (bei „behalten“: REWRITE → „Bereich Doku des Skill-Profils oder INDEX.md betroffen?“) | ✅ 28.10. | ✅ |
| R117 | S#Skill-Governance (Z. 413) | Split-Prüfung nach skill-pflege | DROP | – | D1 | ✅ 28.10. | ✅ |
| R118 | S#VERBOTEN (Z. 419) | Frei inferieren, welche Docs betroffen sind | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R119 | S#VERBOTEN (Z. 420) | Docs ohne Frontmatter in Kern/Module/Referenz akzeptieren (BPM) | REWRITE | S#VERBOTEN; B#Profilwerte BPM und Heidi | „Docs ohne die Pflichtteile, die der Standard für ihren Bereich verlangt (z. B. Frontmatter)“ | | ✅ sinngemäß |
| R120 | S#VERBOTEN (Z. 421) | Neue Docs ohne die Vorlage des Profils | MERGE | S#VERBOTEN | R089 | | ✅ sinngemäß |
| R121 | S#VERBOTEN (Z. 422) | Doku-Hinweise bei trivialen Änderungen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R122 | S#VERBOTEN (Z. 423) | Doku-Hinweise als interruptive Checkliste | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R123 | S#VERBOTEN (Z. 424) | Ladereihenfolge des Profils ignorieren (BPM: DOC-STANDARD Kap. 8) | REWRITE | S#VERBOTEN | Klammer raus | | ✅ sinngemäß |
| R124 | S#VERBOTEN (Z. 425) | Invarianten-Check bei neuen Docs überspringen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R125 | S#VERBOTEN (Z. 426) | Branch automatisch annehmen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R126 | S#VERBOTEN (Z. 427) | Prosa-Fragen bei festen Entscheidungsoptionen | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R127 | S#VERBOTEN (Z. 428) | Migrations-Kapitel ohne User-Freigabe (Frühphasen-Regel, BPM: INDEX.md) | REWRITE | S#VERBOTEN | „Eine Projektregel für Schema-, Config- oder Datenänderungen ohne Freigabe umgehen (z. B. Migration statt Reset, Abweichung ohne freigegebenen Eintrag)“ | | ✅ sinngemäß |
| R128 | S#VERBOTEN (Z. 429) | Abweichung von v1 ohne PD-Eintrag mit Freigabe (Heidi) | MERGE | S#VERBOTEN | R127; Heidi-Wert in B#Schema- und Datenänderungen | | ✅ sinngemäß |
| R129 | S#VERBOTEN (Z. 430) | Statusliste `fertig` ohne Tests oder Commit | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R130 | S#VERBOTEN (Z. 431) | BPM-Pfade oder -Dateinamen für ein anderes Projekt annehmen | REWRITE | S#VERBOTEN | „Pfade oder Dateinamen eines anderen Projekts (auch aus `references/beispiele.md`) annehmen – alles aus dem Skill-Profil“ | | ✅ sinngemäß |
| R131 | S#VERBOTEN (Z. 432) | Sitzung ohne Sitzungsabschluss beenden, wenn Docs geändert wurden | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| N001 | – | Feldtabelle „Feld \| Wofür“: `Doku.Router`, `Doku.Standard`, `Doku.Entscheidungs-Ort`, `Doku.Pflichtdokumente`, `Doku.Validierungsregeln`, `Doku.Sitzungsabschluss`, `Commit.Doku-Check`, `Commit.Format`/`Commit.Module`, `Commit.Push-Policy`, `Branch-Policy` | NEW | S#Voraussetzung: Skill-Profil | wie chat-wechsel; Pflichtfelder nach `docs/skill-profile-v1.md` | | ✅ |
| N002 | – | Reihenfolge: v1 → älteres `## Doku-Profil` (Doku-Checkliste aus `## Commit-Profil`) → Router/Standard im Repo → Auswahlfrage nach „Fehlende Werte“; `none` gültig, der Teil entfällt | NEW | S#Voraussetzung: Skill-Profil | ordnet R031, R034, R035 | | ✅ |
| N003 | – | `references/beispiele.md` mit den Werten BPM und Heidi; Satz in Zweck, dass für jedes Projekt nur sein Profil gilt | NEW | S#Zweck; B | nimmt R004, R005, R033, R034, R036, R038, R039, R040, R042, R043, R045, R046, R051, R052, R056, R058, R062, R068, R071, R076, R077, R080, R092, R095–R098, R100, R112 auf | | ✅ |
| N004 | – | `references/cowork.md`: was im Cowork-Chat anders ist (Profil per DC, Arbeitsverzeichnis per cc-steuerung, Shell, SUCHE/ERSETZE) | NEW | C; S#Arbeitsverzeichnis | nimmt R021, R027, R028, R110 auf | | ✅ |
| N005 | – | Abschnitt „References“ in S mit je einem Verweis auf B und C | NEW | S#References | Pflicht nach `docs/skill-quality.md`, Abschnitt Aufbau | | ✅ |

## DROP-Gruppen

| Gruppe | IDs | Begründung | Freigabe |
|---|---|---|---|
| D1 Pflege-Checkliste des Skills | R113–R117 | Regeln für die Änderung des Skills, nicht für seine Arbeit; doppelt zu `skills/skill-pflege/SKILL.md` (Abschnitte „Split-Prüfung“, „Description ändern“, „Auffälligkeiten melden“) und `docs/skill-quality.md` (Abschnitt „Urteil – audit“); kein anderer Skill führt eine solche Liste. Alternative: behalten, R116 neutral (REWRITE). | |

## Verweise von außen

| Stelle | Verweis | Folge |
|---|---|---|
| `skills/audit/SKILL.md` Z. 100, 106 | „doc-pflege (Projekt-Init)“; Option „Profil anlegen (doc-pflege, Projekt-Init)“ / „Ohne Profil, ich nenne die Docs“ | Überschrift Projekt-Init bleibt; die Optionen folgen bei audit dem alten Wortlaut von R035 – im Phase-6-Schritt audit auf „Fehlende Werte“ umstellen |
| `skills/audit/SKILL.md` Z. 371 | Abschnitt „Doku pflegen“ | bleibt gültig |
| `skills/chatgpt-review/SKILL.md` Z. 323 | Abschnitte „Neue Doc“ und „Begleit-Docs“ | bleiben gültig |
| `skills/chat-wechsel/SKILL.md` Z. 7, 20, 152, 201, 210 | „doc-pflege, Sitzungsabschluss“ | bleibt gültig; der im chat-wechsel-Inventar notierte Rest („Heidi: Startprompt Abschnitt 0“) ist mit R092 erledigt |
| `skills/code-erstellen/SKILL.md` Z. 381 | „DocMaintenanceHints (→ … doc-pflege)“ | Begriff bleibt (R048) |
| `skills/code-erstellen/SKILL.md` Z. 326, 484; `references/stacks/csharp-wpf.md` Z. 57 | „Frühphasen-Prinzip (BPM: INDEX.md)“ | kein Verweis auf doc-pflege; Sache von code-erstellen (Phase 6) |
| `skills/cc-steuerung/SKILL.md#Arbeitsverzeichnis` | Ziel von R027 | existiert, Verweis wandert nach C |
| `skills/projekt-anlegen/SKILL.md#Bestehendes Repo einrichten` | Ziel von R061 | existiert |
| `skills/audit/references/doku-validierung.md` | Ziel von R106 | existiert, unverändert |
| `skills/tracker/SKILL.md` Z. 257, 266, 414, 447; `references/anti-patterns.md` Z. 51, 142; `references/start-task.md` Z. 119; `skills/ticket/SKILL.md` Z. 21, 123, 156; `skills/git-commit-helper/SKILL.md` Z. 28; `skills/projekt-anlegen/SKILL.md` Z. 17, 32; `skills/cc-steuerung/SKILL.md` Z. 25–26; `skills/chat-wechsel/references/prompt-struktur.md` Z. 84 | nur Skillname | bleiben gültig |
| `INDEX.md` Z. 21, 24, 40, 41, 54, 55, 59; `README.md` Z. 184, 199, 279, 636 | Zuständigkeit, Konfliktpaare, Baum | Zuständigkeit und Auslöser ändern sich nicht → keine Änderung; README-Baum bekommt `references/` (Doku-Check „Aufbau geändert“) |
| `docs/skill-profile-v1.md`, Pflichtfelder je Skill | doc-pflege: Doku.Router, Doku.Standard, Doku.Entscheidungs-Ort; Commit.Push-Policy | passt zu N001 |
| `docs/skillsystem-umbau.md`, Phase 6 | Reihenfolge mit doc-pflege | nach dem Umbau abhaken |
| `docs/skill-guard-v1.md` Z. 71, 76, 91 | Wächter-Regeln nennen doc-pflege | bleiben gültig |
| `quality/evals/doc-*`, `doc-pflege-real-uebergabe-bauplan` | Eval-Fälle | Description unverändert; Routing-Eval `--tag doc-pflege` vor dem Upload |

## Prüfung

- **Freigabe:** Zielstruktur und D1 Herbert 28.10.2026.
- **Alt→Neu:** R001–R131 haben einen Zustand (KEEP 63, MOVE 14, REWRITE 46, MERGE 3, DROP 5); jeder Neu-Ort ist als
  Überschrift im neuen Text gefunden (Prüfskript im Scratchpad: alle Überschriften von S, B und C), die Kernsätze der
  REWRITE-Zeilen (GitHub-API, Push-Rückfall, Feldtabelle, Reset-Anweisung, Sitzungsabschluss neutral) per Suche.
- **Neu→Alt:** alle Sätze mit Pflichtwörtern, Tabellenzeilen und VERBOTEN-Punkte von S, B und C durchgegangen; jede
  Aussage gehört zu einer ID oder zu N001–N005. Die Spalte „Pflicht“ der Feldtabelle gibt R029 wieder; der Satz
  „Werte zweier Projekte zu jedem Modus“ unter Modi gehört zu N003.
- **Qualität:** `SKILL.md` 389 Zeilen (Körper 371); `references/beispiele.md` 160 Zeilen mit Inhaltsverzeichnis,
  `references/cowork.md` 21 Zeilen; Projektnamen im Kern nur im Verweis auf B (Abschnitt „Rückfall ohne Profil (BPM)“);
  Werkzeugnamen (DC) nur in C; keine Historie; keine Nummernverweise auf Projekt-Docs im Kern.
- **Description:** unverändert, 994 Zeichen.
- **Prüfskript:** läuft auf dem HA nicht (kein PowerShell); CI nach dem Push.
- **Routing-Eval:** `--tag doc-pflege` nach Commit b323ed4: 21 Fälle, 20 mit 3/3, alle kritischen 3/3.
  `doc-pflege-real-uebergabe-bauplan` 2/3 (normal, ein Lauf ohne Skill). Schwelle erfüllt. CI-Lauf 40602535120 grün.
