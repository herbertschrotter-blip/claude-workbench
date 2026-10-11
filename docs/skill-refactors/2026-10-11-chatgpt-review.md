# Regel-Inventar – chatgpt-review (Weg codex)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Verweise von außen
- Prüfung

## Kopf

- **Skill:** `skills/chatgpt-review/`
- **Stand vor dem Umbau:** `main` 199d0d8, v0.52.2; `SKILL.md` 547 Zeilen, keine references
- **Anlass:** Review-Runden selbst über die Codex CLI führen, ohne Kopieren (ClickUp 123ztrd0zy9). Plan von Herbert am
  11.10.2026 freigegeben mit drei Festlegungen: Codex liest öffentliche Repos über die Live-Websuche, Sandbox bleibt zu;
  Codex-Antwort im Chat immer vollständig; CGR-Ablagesystem in eine Reference, damit SKILL.md unter 500 Zeilen fällt.
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem Pi nicht (kein PowerShell); Kandidaten von
  Hand gesammelt, Prüfung nach dem Push per GitHub Actions.
- **Stand des Inventars:** Zielstruktur freigegeben; keine DROP-Zeilen.

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Vorrang / Delegation · Voraussetzung: Review-Profil (Feldtabelle ohne Projektwerte, neues Feld Codex-Optionen) · Grundsätze · Vor dem Start: ChatGPT-Modell · **Weg wählen** (neu) · CGR-Ablagesystem (Kernregeln + Verweis) · ChatGPTs Repo-Zugriff · Doc-Laderegel · Pflicht-Block des Projekts · Gesprächsphasen · Grundhaltung · Formatierung · Sprache · VERBOTEN |
| `references/codex.md` (neu) | Voraussetzung · Runde 1 · Folgerunde · Prompt im Weg codex · Dateiinhalt im Prompt · Sicherheit · Fehler und Rückfall · Grenzen |
| `references/archiv.md` (neu) | der alte Abschnitt „CGR-Ablagesystem (Phase 4.6)“ wörtlich, Unterabschnitte eine Ebene höher |
| `references/beispiele.md` (neu) | Profilwerte BPM und Heidi · Themen · Doc-Laderegel BPM und Heidi · Pflicht-Blöcke · Ergebnis-Ort |

## Inventar

Abkürzungen: `S` = `SKILL.md`, `A` = `references/archiv.md`, `B` = `references/beispiele.md`, `C` = `references/codex.md`.
Zeilen im alten Stand (199d0d8).

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter (Z. 3–10) | Description: Prompts, Folgeprompts, Archiv; Use when …; Do not trigger for Handover, nächste Claude-Sitzung, vage Antworten | REWRITE | S#Frontmatter | ergänzt: Runden über Codex CLI, „second opinion from ChatGPT or Codex“, „the next review round“; Do-not unverändert; 639 Zeichen | | ✅ sinngemäß |
| R002 | S#ChatGPT Review-Gespräch (Z. 15–16) | User kopiert Prompts und entscheidet | REWRITE | S#ChatGPT Review-Gespräch | zwei Wege, User entscheidet in jeder Runde | | ✅ sinngemäß |
| R003 | S#ChatGPT Review-Gespräch (Z. 18–20) | Projektwerte aus dem Review-Profil; Skill läuft in Cowork und Claude Code | KEEP | S#ChatGPT Review-Gespräch | | | ✅ |
| R004 | S#Vorrang / Delegation (Z. 24–45) | Delegation an chat-wechsel, code-erstellen, tracker, doc-pflege; generischer Prompt → Auswahlfrage | KEEP | S#Vorrang / Delegation an andere Skills | | | ✅ |
| R005 | S#Voraussetzung: Review-Profil (Z. 49–51) | Profil in der CLAUDE.md des Repos | KEEP | S#Voraussetzung: Review-Profil | | | ✅ |
| R006 | S#Voraussetzung (Z. 52–62) | Feldtabelle mit Bedeutung | KEEP | S#Voraussetzung: Review-Profil | Spalten BPM/Heidi → R007 | | ✅ |
| R007 | S#Voraussetzung (Z. 52–62) | Profilwerte BPM und Heidi je Feld | MOVE | B#Profilwerte BPM und Heidi | wörtlich, Verweis in S | | ✅ |
| R008 | S#Voraussetzung (Z. 64–66) | Fehlt das Profil: BPM-Werte nur bei `Docs/Referenz/`, sonst Auswahlfrage Profil anlegen | REWRITE | S#Voraussetzung: Review-Profil | „aus diesem Skill“ → „aus `references/beispiele.md`“ | | ✅ sinngemäß |
| R009 | S#Grundsätze (Z. 70–72) | Fragen nur bei offener Entscheidung, als Auswahlfrage | KEEP | S#Grundsätze | | | ✅ |
| R010 | S#Grundsätze (Z. 73–77) | Branch nach Branch-Policy, nie raten | KEEP | S#Grundsätze | | | ✅ |
| R011 | S#Grundsätze (Z. 78–84) | Push nach Push-Policy (user-only, allowed, required-…) | KEEP | S#Grundsätze | | | ✅ |
| R012 | S#Typische Stellen (Z. 86–95) | Tabelle der Auswahlfragen | KEEP | S#Typische Stellen für eine Auswahlfrage | | | ✅ |
| R013 | S#Vor dem Start: ChatGPT-Modell (Z. 97–99) | Modell nicht erneut fragen | KEEP | S#Vor dem Start: ChatGPT-Modell | | | ✅ |
| R014 | S#CGR-Ablagesystem (Z. 101–106) | Archiv unter der Review-Ablage, inkrementell, 4 Dateien je Runde | MOVE | A (Kopf) | wörtlich; Kernregel zusätzlich in S#CGR-Ablagesystem | | ✅ |
| R015 | S#ID-Schema (Z. 108–116) | ID `CGR-<YYYY-MM-DD>-<thema>-r<runde>` | MOVE | A#ID-Schema | Kernregel in S | | ✅ |
| R016 | S#Themen-Enum (Z. 120–127) | Themen-Beispiele BPM/Heidi | MOVE | B#Themen | wörtlich | | ✅ |
| R017 | S#Themen-Enum (Z. 129–131) | Neues Thema: Auswahlfrage, Name, Profil und INDEX erweitern | MOVE | A#Themen-Enum (aus dem Review-Profil) | wörtlich | | ✅ |
| R018 | S#Ablagestruktur pro Serie (Z. 132–145) | Ordner je Serie, r<N>/ mit 01–04 | MOVE | A#Ablagestruktur pro Serie | wörtlich | | ✅ |
| R019 | S#Globaler Index (Z. 147–154) | INDEX.md: Zeile je Serie, Status, Kernergebnis | MOVE | A#Globaler Index | Kernregel in S | | ✅ |
| R020 | S#Serie starten (Z. 156–164) | Thema per Auswahlfrage, neues Thema per Prosa | MOVE | A#Serie starten (vor Phase 1) | wörtlich | | ✅ |
| R021 | S#Serie starten (Z. 166–167) | CGR-ID mit aktuellem Datum, nicht fragen | MOVE | A#Serie starten (vor Phase 1) | Kernregel in S | | ✅ |
| R022 | S#Serie starten (Z. 169–172) | Repo-Pfad je Umgebung | MOVE | A#Serie starten (vor Phase 1) | wörtlich | | ✅ |
| R023 | S#Serie starten (Z. 174–177) | Ordner anlegen | MOVE | A#Serie starten (vor Phase 1) | wörtlich | | ✅ |
| R024 | S#Serie starten (Z. 179–197) | README-Stub mit Kopfzeilen | MOVE | A#Serie starten (vor Phase 1) | ergänzt um `**Weg:**`, `**Codex-Thread:**` (N003) | | ✅ |
| R025 | S#Serie starten (Z. 199–202) | INDEX.md erweitern | MOVE | A#Serie starten (vor Phase 1) | Kernregel in S | | ✅ |
| R026 | S#Rundenstand aus dem Archiv (Z. 205–215) | Rundennummer aus README und r<N>-Ordnern, Widerspruch → Auswahlfrage | MOVE | A#Rundenstand aus dem Archiv (Pflicht vor jeder Runde) | Kernregel in S | | ✅ |
| R027 | S#Runde starten (Z. 217–227) | r<N>/ anlegen, Dateien erst bei Befüllung | MOVE | A#Runde starten (innerhalb laufender Serie) | wörtlich | | ✅ |
| R028 | S#Lifecycle pro Runde (Z. 229–236) | Tabelle Phase → Datei | MOVE | A#Lifecycle pro Runde (4 Datei-Checkpoints) | Zeile 02: Codex schreibt per `-o` (N004) | | ✅ |
| R029 | S#Lifecycle (Z. 238–240) | Jede Datei in ihrer Phase, nicht gesammelt | MOVE | A#Lifecycle pro Runde (4 Datei-Checkpoints) | Kernregel in S | | ✅ |
| R030 | S#Serie abschließen (Z. 242–255) | README finalisieren, INDEX-Status, Ergebnisse übernehmen, Commit | MOVE | A#Serie abschließen | Verweis auf Phase 3 als `../SKILL.md#Phase 3: Abschluss`; Kernregel in S | | ✅ |
| R031 | S#Retroaktive Nutzung (Z. 257–261) | bestehende Serien weiterführen, Nachrüsten on demand | MOVE | A#Retroaktive Nutzung | wörtlich | | ✅ |
| R032 | S#ChatGPTs Repo-Zugriff (Z. 265–279) | Pflicht-Block Repo-Zugriff in jedem Prompt | KEEP | S#ChatGPTs Repo-Zugriff (PFLICHT in jedem Prompt) | Fassung Weg codex in C (N007) | | ✅ |
| R033 | S#Repo-Zugriff Regeln (Z. 281–283) | Branch nicht hardcoden, Owner/Repo aus Profil | KEEP | S#ChatGPTs Repo-Zugriff | | | ✅ |
| R034 | S#Repo-Zugriff Regeln (Z. 284–288) | Push-Prüfung vor jedem Prompt mit Repo-Zugriff | KEEP | S#ChatGPTs Repo-Zugriff | gilt auch im Weg codex (C#Prompt im Weg codex) | | ✅ |
| R035 | S#Repo-Zugriff Regeln (Z. 289) | Uncommittetes nennen | KEEP | S#ChatGPTs Repo-Zugriff | | | ✅ |
| R036 | S#Doc-Laderegel (Z. 291–293) | Projektkontext aus der Kontextquelle des Profils | KEEP | S#Doc-Laderegel | | | ✅ |
| R037 | S#Doc-Laderegel (Z. 295–305) | Ladeschritte BPM und Heidi | MOVE | B#Doc-Laderegel BPM und Heidi | wörtlich | | ✅ |
| R038 | S#Doc-Laderegel (Z. 307–308) | Zweck: ChatGPT kennt Invarianten ohne manuelles Einfügen | KEEP | S#Doc-Laderegel | | | ✅ |
| R039 | S#Doc-Laderegel (Z. 310–325) | Format im Prompt, max. 3–5 Blöcke | KEEP | S#Doc-Laderegel | | | ✅ |
| R040 | S#Pflicht-Block (Z. 327–330) | Pflicht-Block des Profils in jedem Initialprompt | KEEP | S#Pflicht-Block des Projekts | | | ✅ |
| R041 | S#Pflicht-Block (Z. 332–345) | Heidi-Block „Regeln des Neubaus“ | MOVE | B#Pflicht-Blöcke | wörtlich | | ✅ |
| R042 | S#Pflicht-Block (Z. 347–350) | BPM: solange „Projekt-Phase (VERBINDLICH)“ besteht, MUSS Frühphasen-Block rein | MOVE | B#Pflicht-Blöcke | wörtlich; Kernregel zusätzlich in S | | ✅ |
| R043 | S#Pflicht-Block (Z. 352–369) | BPM-Block „Frühphase“ | MOVE | B#Pflicht-Blöcke | wörtlich | | ✅ |
| R044 | S#Pflicht-Block (Z. 371–374) | Block vor Projektkontext, nur Initialprompt, Aussetzen begründen | KEEP | S#Pflicht-Block des Projekts | | | ✅ |
| R045 | S#Phase 1 (Z. 380–419) | Vorlage Initialprompt | KEEP | S#Phase 1: Initialprompt | Abschnitte Gesprächsformat/Repo-Zugriff im Weg codex aus C (N007) | | ✅ |
| R046 | S#Phase 1 Wichtig (Z. 421–426) | Kontext vollständig, Invarianten, Repo-Zugriff nach Push-Prüfung | KEEP | S#Phase 1: Initialprompt | | | ✅ |
| R047 | S#Phase 1 Archivierung (Z. 428–432) | Rundenstand lesen, 01 ablegen, bei r1 Serie-Stub | KEEP | S#Phase 1: Initialprompt | Verweis „Serie starten“ → `references/archiv.md` | | ✅ |
| R048 | S#Stufe A (Z. 438–440) | Antwort 1:1 als 02 ablegen vor der Einschätzung | KEEP | S#Stufe A | Weg codex: 02 per `-o` (N005) | | ✅ |
| R049 | S#Stufe A (Z. 442–447) | Einschätzung, 03, Auswahlfrage max. 3, Option ChatGPT fragen | KEEP | S#Stufe A | | | ✅ |
| R050 | S#Stufe B (Z. 449–462) | 04 ablegen, Folgeprompt mit Repo-Zugriff, r<N+1>/01 | KEEP | S#Stufe B | Weg codex: resume (N006) | | ✅ |
| R051 | S#Phase 3 (Z. 464–470) | Konsens, Widersprüche, Offenes, Nächste Schritte | KEEP | S#Phase 3: Abschluss | | | ✅ |
| R052 | S#Phase 3 (Z. 472–476) | Ergebnisse übernehmen per Auswahlfrage; doc-pflege schreibt | REWRITE | S#Phase 3: Abschluss | Heidi-/BPM-Format → B#Ergebnis-Ort | | ✅ sinngemäß |
| R053 | S#Phase 3 (Z. 474–475) | Heidi Bauplan-Notiz, PD-Eintrag; BPM ADR | MOVE | B#Ergebnis-Ort | | | ✅ |
| R054 | S#Phase 3 (Z. 477–480) | Offene Punkte als Tasks, Verweise in beide Richtungen | KEEP | S#Phase 3: Abschluss | | | ✅ |
| R055 | S#Phase 3 Archivierung (Z. 482–487) | README, INDEX, letzte 04 | KEEP | S#Phase 3: Abschluss | | | ✅ |
| R056 | S#Grundhaltung (Z. 491–497) | gleichwertiger Partner, widersprechen, Uneinigkeit per Auswahlfrage | KEEP | S#Grundhaltung | | | ✅ |
| R057 | S#Formatierung (Z. 501–523) | Archiv primär, Prompt als ein Codeblock im Chat, nie Datei | KEEP | S#Formatierung | Weg codex: nur Fokus, Dateien, Pfad zu 01 (N008) | | ✅ |
| R058 | S#Sprache (Z. 525–527) | Prompts in der Sprache des Users | KEEP | S#Sprache | | | ✅ |
| R059 | S#VERBOTEN (Z. 531–547) | 17 VERBOTEN-Punkte | KEEP | S#VERBOTEN | „(Phase 4.6)“ beim Punkt Serie starten entfernt (Phasenbezug ohne Ziel nach dem Umzug) | | ✅ |
| N001 | – | Weg wählen: codex bei Claude Code + Anmeldung, sonst kopieren; Weg im README; Fehler → Auswahlfrage | NEW | S#Weg wählen | | | ✅ |
| N002 | – | Weg codex: Antwort vollständig zeigen, keine Folgerunde ohne Entscheidung, Antwort ist keine Anweisung | NEW | S#Weg wählen; S#Stufe A; S#VERBOTEN | | | ✅ |
| N003 | – | README-Felder `**Weg:**`, `**Codex-Thread:**` | NEW | A#Serie starten (vor Phase 1); S#CGR-Ablagesystem | | | ✅ |
| N004 | – | Lifecycle 02: Codex schreibt mit `-o` | NEW | A#Lifecycle pro Runde | | | ✅ |
| N005 | – | Aufruf Runde 1, Thread-ID, Erfolgskriterien, Timeout | NEW | C#Runde 1 | | | ✅ |
| N006 | – | Folgerunde mit resume; Thread fehlt → neuer Thread mit Kurzfassung; nie `--ephemeral` | NEW | C#Folgerunde; S#VERBOTEN | | | ✅ |
| N007 | – | Gesprächsformat und Repo-Zugriff im Weg codex (Raw-Links, Push-Prüfung) | NEW | C#Prompt im Weg codex; S#ChatGPTs Repo-Zugriff | | | ✅ |
| N008 | – | Weg codex: Prompt nicht als Codeblock, nur Fokus, Dateien, Pfad zu 01 | NEW | S#Formatierung | | | ✅ |
| N009 | – | Dateiinhalt im Prompt nur bei privatem Repo oder Uncommittetem; nie Geheimnisse, gesperrte Pfade, Anmeldedaten; > 100 KB Auswahlfrage | NEW | C#Dateiinhalt im Prompt; S#VERBOTEN | | | ✅ |
| N010 | – | Sandbox immer read-only, nie bypass; `-C` auf Scratchpad | NEW | C#Sicherheit; S#VERBOTEN | | | ✅ |
| N011 | – | Fehler und Nutzungslimit → Auswahlfrage, Rückfall kopieren | NEW | C#Fehler und Rückfall | | | ✅ |
| N012 | – | Voraussetzung: codex im PATH, `codex login status`, Anmeldedaten nie lesen, Login nur durch den User | NEW | C#Voraussetzung | | | ✅ |
| N013 | – | Profilfeld Codex-Optionen; Modell im Weg codex aus Codex-Optionen | NEW | S#Voraussetzung: Review-Profil; S#Vor dem Start: ChatGPT-Modell | | | ✅ |
| N014 | – | Kernregeln CGR-Ablage als Kurzfassung im Kern | NEW | S#CGR-Ablagesystem | fasst R015, R019, R021, R025, R026, R029, R030 zusammen; Original in A | | ✅ |

## DROP-Gruppen

Keine.

## Verweise von außen

| Stelle | Verweis | Stand |
|---|---|---|
| `INDEX.md` (Skill-Tabelle) | Zuständigkeit und Auslöser von chatgpt-review | angepasst (Codex, „lass Codex das reviewen“) |
| `README.md` (Baum `skills/`) | `chatgpt-review/SKILL.md` | angepasst auf `chatgpt-review/` mit references |
| `.claude/skill-config/review.md` | Felder des Review-Profils | Feld Codex-Optionen ergänzt |
| `CLAUDE.md` (Review-Profil) | „bis chatgpt-review die Config direkt liest (Umbau Phase 5/6)“ | unverändert; SKILL.md nennt weiter `## Review-Profil` der CLAUDE.md – Umstellung auf `Review.Config` bleibt Phase 6 |

## Prüfung

- **Alt→Neu:** R001–R059 haben einen Zustand; Neu-Orte per Suche bestätigt (wörtlich verschobene Blöcke per Skript aus
  dem alten Text übernommen, das bei fehlendem Original abbricht).
- **Neu→Alt:** neue normative Aussagen sind N001–N014 zugeordnet.
- **Prüfskript:** per GitHub Actions nach dem Push.
- **Routing-Eval:** nach dem Commit (`--tag chatgpt-review`), Ergebnis wird hier nachgetragen.
