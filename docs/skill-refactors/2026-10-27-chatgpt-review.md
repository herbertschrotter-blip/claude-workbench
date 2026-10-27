# Regel-Inventar – chatgpt-review, Phase 6 (2026-10-27)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Verweise von außen
- Prüfung

## Kopf

- **Skill:** `skills/chatgpt-review/`
- **Stand vor dem Umbau:** `main` e3585ac, v0.60.8; `SKILL.md` 405 Zeilen, references `archiv.md` 184, `beispiele.md` 95,
  `codex.md` 181
- **Anlass:** Umbau Phase 6 (ClickUp 123ztrcxedq), dritter Skill. Größe erfüllt; offen waren das alte `## Review-Profil`
  statt `Review.Config` (Skill-Profil v1, Felder je Thema), Projektwerte (BPM, Heidi) im Kern und in `archiv.md`,
  Werkzeugnamen im Kern (DC, Artifact, Write, Bash, `SendUserFile`, `present_files`).
- **Entscheidungen Herbert 27.10.2026:** Zielstruktur „Umsetzen“; keine DROP-Gruppe.
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem HA nicht (kein PowerShell); Kandidaten von Hand
  aus dem alten Text, Prüfung nach dem Push per GitHub Actions.

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `A` = `references/archiv.md`, `B` = `references/beispiele.md`,
`X` = `references/codex.md`.

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | unverändert gegliedert; **Voraussetzung: Skill-Profil** statt „Voraussetzung: Review-Profil“ (Review.Config, Push- und Branch-Policy, Felder Allgemein/je Thema, Quellen-Reihenfolge); alle Projektwerte neutral |
| `references/beispiele.md` | Inhalt · Profilwerte BPM und Heidi (+ Hinweis Allgemein/je Thema) · **Rückfall ohne Profil (BPM)** · Themen · Doc-Laderegel (+ Beispielsätze aus S) · Pflicht-Blöcke · Ergebnis-Ort (+ Verweise) |
| `references/archiv.md` | Platzhalter statt BPM-Themen, Review-Config statt Review-Profil, neues Thema in der Config |
| `references/codex.md` | Profilbegriffe angepasst, sonst unverändert |

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter | Description | KEEP | S#Frontmatter | wörtlich | | ✅ |
| R002 | S#Kopf (Z. 16–17) | Strukturiertes Review; Codex in Claude Code, sonst kopieren; User entscheidet je Runde | KEEP | S#ChatGPT Review-Gespräch | wörtlich | | ✅ |
| R003 | S#Kopf (Z. 19–20) | Projektspezifisches steht im Review-Profil der CLAUDE.md | REWRITE | S#ChatGPT Review-Gespräch | „Review-Config“, Verweis auf „Voraussetzung: Skill-Profil“ | | ✅ sinngemäß |
| R004 | S#Kopf (Z. 20–21) | Läuft im Cowork-Chat (DC, Artifact) und in Claude Code (Write, Bash) | REWRITE | S#ChatGPT Review-Gespräch | Handlung statt Werkzeug | | ✅ sinngemäß |
| R005 | S#Vorrang (Z. 27–46) | Delegationstabelle, Zuständigkeit, generischer Prompt → Auswahlfrage | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R006 | S#Voraussetzung (Z. 52–53) | Abschnitt `## Review-Profil` der CLAUDE.md; Cowork per DC | REWRITE | S#Voraussetzung: Skill-Profil | `Review.Config` aus dem Skill-Profil; altes Review-Profil als Quelle 2 | | ✅ sinngemäß |
| R007 | S#Voraussetzung (Z. 55–64) | Feldtabelle (8 Felder) | REWRITE | S#Voraussetzung: Skill-Profil | Tabelle nach Allgemein/je Thema; Feld „Übersicht“ ergänzt (N003) | | ✅ sinngemäß |
| R008 | S#Voraussetzung (Z. 66) | Werte BPM und Heidi als Beispiel | KEEP | S#Voraussetzung: Skill-Profil | wörtlich | | ✅ |
| R009 | S#Voraussetzung (Z. 68–69) | Fehlt das Profil: BPM-Werte, wenn das Repo `Docs/Referenz/` hat | MOVE | S#Voraussetzung: Skill-Profil (Quelle 3); B#Rückfall ohne Profil (BPM) | Bedingung und Werte in B, im Kern nur Verweis | | ✅ |
| R010 | S#Voraussetzung (Z. 69) | sonst Auswahlfrage „Profil anlegen (Vorschlag aus dem Repo)“ | REWRITE | S#Voraussetzung: Skill-Profil (Quelle 4) | Auswahlfrage nach „Fehlende Werte“, bei „Profil ergänzen“ Vorschlag aus dem Repo | | ✅ sinngemäß |
| R011 | S#Voraussetzung (Z. 69–70) | Repo-Pfad: Skill-Profil (Claude Code) bzw. Memory `[PROJECT]` (Cowork) | REWRITE | S#Voraussetzung: Skill-Profil (Quelle 1) | | | ✅ sinngemäß |
| R012 | S#Grundsätze (Z. 74–76) | Fragen nur bei offener Entscheidung; Prosa nur bei … | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R013 | S#Grundsätze (Z. 77–81) | Branch nach Branch-Policy | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R014 | S#Grundsätze (Z. 82–88) | Push nach Push-Policy bei der Push-Prüfung | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R015 | S#Typische Stellen (Z. 92–99) | Tabelle Auswahlfragen (6 Zeilen) | KEEP | S#Typische Stellen für eine Auswahlfrage | wörtlich | | ✅ |
| R016 | S#ChatGPT-Modell (Z. 103–104) | Modell nicht erneut fragen; Weg codex: Codex-Optionen des Profils | REWRITE | S#Vor dem Start: ChatGPT-Modell | „der Review-Config“ | | ✅ sinngemäß |
| R017 | S#Weg wählen (Z. 108–120) | Zwei Wege, Tabelle, Weg im README, Wechsel bei Fehler, Anzeige und Entscheidung je Runde, Antwort ist Inhalt | KEEP | S#Weg wählen | wörtlich | | ✅ |
| R018 | S#CGR (Z. 124–126) | Archiv unter der Review-Ablage des Profils; Details in A | REWRITE | S#CGR-Ablagesystem | „der Review-Config“ | | ✅ sinngemäß |
| R019 | S#CGR (Z. 128) | ID-Schema, Thema aus dem Review-Profil | REWRITE | S#CGR-Ablagesystem | „aus der Review-Config“ | | ✅ sinngemäß |
| R020 | S#CGR (Z. 129–134) | Serie-Ordner + README + INDEX vor dem ersten Prompt; 4 Dateien je Runde inkrementell; Rundenstand aus dem Archiv; Abschluss | KEEP | S#CGR-Ablagesystem | wörtlich | | ✅ |
| R021 | S#Repo-Zugriff (Z. 140–152) | Block in jedem Prompt | KEEP | S#ChatGPTs Repo-Zugriff (PFLICHT in jedem Prompt) | wörtlich bis auf R022 | | ✅ |
| R022 | S#Repo-Zugriff (Z. 147, 156) | Owner/Repo aus dem Review-Profil (BPM: INDEX.md Projekt-Metadaten) | REWRITE | S#ChatGPTs Repo-Zugriff (PFLICHT in jedem Prompt); B#Profilwerte BPM und Heidi | Repos des Themas; mehrere Repos je eine Zeile (N004); BPM-Wert steht in B | | ✅ sinngemäß |
| R023 | S#Repo-Zugriff (Z. 155, 157–166) | Branch nicht hardcoden; Push-Prüfung; uncommittete Dateien nennen; Weg codex | KEEP | S#ChatGPTs Repo-Zugriff (PFLICHT in jedem Prompt) | wörtlich | | ✅ |
| R024 | S#Doc-Laderegel (Z. 168–172) | Projektkontext aus der Kontextquelle des Profils; Verweis auf B | REWRITE | S#Doc-Laderegel (Kontextquelle aus der Review-Config) | „des Themas“ | | ✅ sinngemäß |
| R025 | S#Doc-Laderegel (Z. 174–175) | Beispiele „SQLite ist SoR“ (BPM), „DxApi“ (Heidi) | REWRITE | S#Doc-Laderegel (Kontextquelle aus der Review-Config); B#Doc-Laderegel BPM und Heidi | Zweck neutral im Kern, Beispielsatz wörtlich nach B | | ✅ sinngemäß |
| R026 | S#Doc-Laderegel (Z. 177–192) | Format im Prompt (Quickload-Felder), nur relevante Blöcke, max 3–5 | REWRITE | S#Doc-Laderegel (Kontextquelle aus der Review-Config); B#Doc-Laderegel BPM und Heidi | Platzhalter „aus der Kontextquelle“; Quickload-Bezug als BPM-Fall nach B; Limits wörtlich | | ✅ sinngemäß |
| R027 | S#Pflicht-Block (Z. 196–197) | Zweck; Block steht im Review-Profil | REWRITE | S#Pflicht-Block des Projekts (PFLICHT in jedem Initialprompt) | „in der Review-Config beim Thema“ | | ✅ sinngemäß |
| R028 | S#Pflicht-Block (Z. 199–200) | Blöcke Heidi und BPM wörtlich in B | KEEP | S#Pflicht-Block des Projekts (PFLICHT in jedem Initialprompt) | Verweis bleibt, Namen als Beispiel | | ✅ |
| R029 | S#Pflicht-Block (Z. 200–201) | BPM: solange INDEX.md „Projekt-Phase“ hat, MUSS der Frühphasen-Block rein | MERGE | B#Pflicht-Blöcke | stand dort schon wörtlich; im Kern nur „mit der Bedingung, wann er gilt“ | | ✅ |
| R030 | S#Pflicht-Block (Z. 203–206) | Vor Projektkontext; nicht in Folgeprompts; bewusstes Aussetzen | KEEP | S#Pflicht-Block des Projekts (PFLICHT in jedem Initialprompt) | wörtlich, „(beide Projekte)“ entfällt | | ✅ |
| R031 | S#Phase 1 (Z. 214–251) | Vorlage Initialprompt | REWRITE | S#Phase 1: Initialprompt | Reviewer-Rolle und Kontextquelle „des Themas“; Projektbeispiele aus dem Platzhalter entfernt | | ✅ sinngemäß |
| R032 | S#Phase 1 (Z. 253–260) | Wichtig: Kontext sammeln, Code vollständig, Kontextquelle (BPM/Heidi), Invarianten, Repo-Zugriff, Weg codex | REWRITE | S#Phase 1: Initialprompt; B#Profilwerte BPM und Heidi | Kontextquelle „des Themas“, Beispiele stehen in B | | ✅ sinngemäß |
| R033 | S#Phase 1 (Z. 262–266) | Archivierung Phase 1 | KEEP | S#Phase 1: Initialprompt | wörtlich | | ✅ |
| R034 | S#Phase 2 (Z. 268–299) | Stufe A und B mit Archivierung, Weg codex | KEEP | S#Phase 2: Antwort/Reaktion | wörtlich | | ✅ |
| R035 | S#Phase 3 (Z. 301–308) | Abschluss-Inhalte | KEEP | S#Phase 3: Abschluss | wörtlich | | ✅ |
| R036 | S#Phase 3 (Z. 309–315) | Ergebnisse übernehmen per Auswahlfrage; Ergebnis-Ort des Profils; doc-pflege schreibt; Tasks über tracker | REWRITE | S#Phase 3: Abschluss | „des Themas“ | | ✅ sinngemäß |
| R037 | S#Phase 3 (Z. 316) | Verweise in beide Richtungen: README ↔ Bauplan-Notizen/ADRs, Task-IDs | REWRITE | S#Phase 3: Abschluss; B#Ergebnis-Ort | „Einträge am Ergebnis-Ort“; BPM/Heidi-Fassung nach B | | ✅ sinngemäß |
| R038 | S#Phase 3 (Z. 318–323) | Archivierung Serie-Abschluss (Links zu ADRs/Commits) | REWRITE | S#Phase 3: Abschluss | „Einträge am Ergebnis-Ort und Commits“ | | ✅ sinngemäß |
| R039 | S#Grundhaltung (Z. 327–333) | Gleichwertiger Gesprächspartner | KEEP | S#Grundhaltung | wörtlich | | ✅ |
| R040 | S#Formatierung (Z. 339–361) | Zwei Ablage-Orte; Codeblock im Chat; Stufe A | REWRITE | S#Formatierung | nur „Review-Ablage der Review-Config“ | | ✅ sinngemäß |
| R041 | S#Anzeige im Chat (Z. 363–371) | 🟦/🟧, Statuszeile | KEEP | S#Anzeige im Chat | wörtlich | | ✅ |
| R042 | S#Sprache (Z. 375) | Prompts in der Sprache des Users | KEEP | S#Sprache | wörtlich | | ✅ |
| R043 | S#VERBOTEN (Z. 381–383, 385–388, 390–394, 396–405) | übrige Verbote | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R044 | S#VERBOTEN (Z. 384) | Initialprompt ohne Pflicht-Block (BPM Frühphase, Heidi Regeln des Neubaus) | REWRITE | S#VERBOTEN | „des Themas“, Beispiele entfallen (stehen in B) | | ✅ sinngemäß |
| R045 | S#VERBOTEN (Z. 389) | BPM-Ablage, -Themen, -Frühphase für ein anderes Projekt annehmen | REWRITE | S#VERBOTEN | „Ablage, Themen oder Pflicht-Block eines anderen Projekts“ | | ✅ sinngemäß |
| R046 | S#VERBOTEN (Z. 395) | Prompt als Datei/Download (`SendUserFile`, `present_files`) | REWRITE | S#VERBOTEN | Handlung statt Werkzeug | | ✅ sinngemäß |
| R047 | A#Kopf, Inhalt | Details zu S#CGR-Ablagesystem; Inhaltsverzeichnis | REWRITE | A | „Review-Config“ im Eintrag Themen-Enum | | ✅ sinngemäß |
| R048 | A (Z. 20–23) | Ablage des Profils (BPM-, Heidi-Pfad); Schreiben je Umgebung; inkrementell | REWRITE | A; B#Profilwerte BPM und Heidi | Pfade nur in B, Verweis | | ✅ sinngemäß |
| R049 | A#ID-Schema | ID-Schema | KEEP | A#ID-Schema | wörtlich | | ✅ |
| R050 | A#Themen-Enum | Beispiele in B; neues Thema → Themenliste im Review-Profil und INDEX | REWRITE | A#Themen-Enum (aus der Review-Config) | Thema in der Config (Allgemein → Themen + Abschnitt je Thema, N005) und INDEX | | ✅ sinngemäß |
| R051 | A#Ablagestruktur | Ordnerbaum; „Herberts Antworten“ | REWRITE | A#Ablagestruktur pro Serie | „des Users“ | | ✅ sinngemäß |
| R052 | A#Globaler Index | Zeile je Serie, Status, Kernergebnis | KEEP | A#Globaler Index | wörtlich | | ✅ |
| R053 | A#Serie starten Schritt 1 | Thema per Auswahlfrage (BPM-Beispieloptionen) | REWRITE | A#Serie starten (vor Phase 1); B#Themen | Platzhalter, Verweis auf B | | ✅ sinngemäß |
| R054 | A#Serie starten Schritte 2–6 | CGR-ID, nie überschreiben, Repo-Pfad, Ordner, README-Stub, INDEX | KEEP | A#Serie starten (vor Phase 1) | wörtlich | | ✅ |
| R055 | A#Rundenstand, Statuszeile, Runde starten, Lifecycle | | KEEP | A | wörtlich | | ✅ |
| R056 | A#Serie abschließen 1–2, 4 | README, INDEX, Commit | REWRITE | A#Serie abschließen | Links „zu den Einträgen am Ergebnis-Ort und zu Commits“ | | ✅ sinngemäß |
| R057 | A#Serie abschließen 3 | Ergebnisse an den Ergebnis-Ort des Profils | REWRITE | A#Serie abschließen | „des Themas“ | | ✅ sinngemäß |
| R058 | A#Retroaktive Nutzung | | KEEP | A#Retroaktive Nutzung | wörtlich | | ✅ |
| R059 | B#Kopf | Werte gelten als Rückfall für BPM | REWRITE | B; B#Rückfall ohne Profil (BPM) | eigener Abschnitt | | ✅ sinngemäß |
| R060 | B#Profilwerte, Themen, Doc-Laderegel, Pflicht-Blöcke, Ergebnis-Ort | Beispielwerte | KEEP | B | wörtlich, ergänzt um R025, R026, R037, N006 | | ✅ |
| R061 | X#Voraussetzung | Codex-Optionen des Profils | REWRITE | X#Voraussetzung | „der Review-Config (Allgemein)“ | | ✅ sinngemäß |
| R062 | X#Runde 1 | `<Optionen>` = Codex-Optionen des Review-Profils | REWRITE | X#Runde 1 | „der Review-Config“ | | ✅ sinngemäß |
| R063 | X#Prompt im Weg codex | Repo aus dem Review-Profil | REWRITE | X#Prompt im Weg codex | „aus den Repos des Themas“ | | ✅ sinngemäß |
| R064 | X (übrige Abschnitte) | Sandbox-Test, Folgerunde, Websuche, Sicherheit, Fehler, Geprüfte Umgebungen, Grenzen | KEEP | X | wörtlich | | ✅ |
| N001 | – | Felder aus dem Skill-Profil: `Review.Config`, `Commit.Push-Policy`, `Branch-Policy` | NEW | S#Voraussetzung: Skill-Profil | `docs/skill-profile-v1.md`, Pflichtfelder je Skill | | ✅ |
| N002 | – | Quellen-Reihenfolge Config → altes Review-Profil → Rückfall B → „Fehlende Werte“ | NEW | S#Voraussetzung: Skill-Profil | wie chat-wechsel v0.60.8 | | ✅ |
| N003 | – | Feld „Übersicht“ (INDEX.md der Ablage); Repos je Thema, sonst GitHub-Repo aus „Allgemein“ | NEW | S#Voraussetzung: Skill-Profil | Gliederung `review.md` | | ✅ |
| N004 | – | Mehrere Repos im Repo-Zugriff je eine Zeile | NEW | S#ChatGPTs Repo-Zugriff (PFLICHT in jedem Prompt) | Thema ha-grundsatz nennt zwei Repos | | ✅ |
| N005 | – | Neues Thema bekommt in der Config einen Abschnitt je Thema; fehlende Werte nach „Fehlende Werte“ | NEW | A#Themen-Enum (aus der Review-Config) | | | ✅ |
| N006 | – | Hinweis Allgemein/je Thema; Abschnitt „Rückfall ohne Profil (BPM)“ | NEW | B | nimmt R009 auf | | ✅ |

## DROP-Gruppen

Keine. Es entfällt keine Regel.

## Verweise von außen

- `CLAUDE.md#Review-Profil` (Verweis-Abschnitt „bis chatgpt-review die Config direkt liest“) und
  `docs/skill-profile-v1.md#Einführung in den Repos`: werden im folgenden Docs-Commit nachgezogen.
- `INDEX.md` nennt „Review-Profil“ nur in der Aufzählung der früheren Profile; bleibt.
- Andere Skills verweisen nur über den Namen auf chatgpt-review (chat-wechsel, tracker); keine Abschnitte oder Nummern.
- Anker `references/beispiele.md#profilwerte-bpm-und-heidi`, `#doc-laderegel-bpm-und-heidi`, `#pflicht-blöcke`,
  `#ergebnis-ort`, `#themen` unverändert; neu `#rückfall-ohne-profil-bpm`.

## Prüfung

- **Alt→Neu:** R001–R064 haben einen Zustand; jeder Neu-Ort ist im neuen Text vorhanden.
- **Neu→Alt:** Sätze mit Pflichtwörtern, Tabellenzeilen und VERBOTEN-Punkte des neuen Stands gehören zu einer ID oder
  zu N001–N006.
- **Qualität:** `SKILL.md` 418 Zeilen; References mit Inhaltsverzeichnis (`beispiele.md` jetzt 108 Zeilen); BPM und
  Heidi im Kern nur noch in Verweisen auf `beispiele.md`; keine Historie; Werkzeugnamen im Kern nur in den wörtlich
  übernommenen Grundsätzen (Shell je Umgebung) und im Weg codex (Codex CLI als nötiges Werkzeug).
- **Routing-Eval:** offen (nach dem Commit).
