# Regel-Inventar – mockup-erstellen, Phase 6 (2026-10-25)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Verweise von außen
- Prüfung

## Kopf

- **Skill:** `skills/mockup-erstellen/`
- **Stand vor dem Umbau:** `main` 8cfb8c5, v0.60.4; `SKILL.md` 304 Zeilen, `references/sitemap.md` 322 Zeilen
- **Anlass:** Umbau Phase 6 (ClickUp 123ztrcxedq), erster Skill. Größe ist seit dem Split vom 22.10.2026
  (`2026-10-22-mockup-erstellen.md`) erfüllt; offen waren Projektwerte im Kern, Historie, Cowork-Teile im Kern, das alte
  Mockup-Profil statt Skill-Profil v1 und Verweise über Schrittnummern.
- **Entscheidungen Herbert 25.10.2026:** Zielstruktur „Umsetzen“ (neu `references/beispiele.md` und `references/cowork.md`);
  DROP-Gruppe Historie freigegeben.
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem HA nicht (kein PowerShell); Kandidaten von Hand
  aus dem alten Text, Prüfung nach dem Push per GitHub Actions.

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `B` = `references/beispiele.md`, `C` = `references/cowork.md`,
`M` = `references/sitemap.md`.

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck · Vorrang / Delegation · Grundsätze · Arbeitsverzeichnis · **Voraussetzung: Skill-Profil** · Sitemap und Klick-Navigation · Docs laden (Bestehende Mockups prüfen, Sitemap laden, Design-Referenz) · **Workflow** mit benannten Schritten (Kontext sammeln, Docs laden (im Ablauf), Vorschau, Token-Abgleich, Ansichten prüfen, Auf Platte speichern, Abnahme festhalten, Commit-Vorschlag) · HTML-Regeln · VERBOTEN |
| `references/beispiele.md` (neu) | Inhalt · Profilwerte BPM und Heidi · Docs laden BPM und Heidi · Abnahme-Ort · Commit |
| `references/cowork.md` (neu) | Inhalt · Docs und Ablage lesen · Vorschau · Speichern · Visualizer-Variablen |
| `references/sitemap.md` | unverändert bis auf Historie, Schrittüberschriften ohne Nummer, „Beispiel BPM“ bei den Modulnamen |

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter | Description | KEEP | S#Frontmatter | wörtlich (v0.60.4) | | ✅ |
| R002 | S#Zweck (Z. 23–28) | Stellt sicher: Namenskonvention/Ablage, Docs und Tokens, Workflow, nicht überschreiben, Token-Abgleich | REWRITE | S#Zweck | „Mockup-Profil“ → „Skill-Profil, Bereich Mockup“; „Preview“ → „Vorschau“ | | ✅ sinngemäß |
| R003 | S#Zweck (Z. 30) | Projektspezifisches steht im Mockup-Profil | REWRITE | S#Zweck | Skill-Profil, Abschnitt „Voraussetzung: Skill-Profil“ | | ✅ sinngemäß |
| R004 | S#Zweck (Z. 31–33) | Werte BPM (Ablage, Sitemap, Colors.xaml) und Heidi (Ablage, Tabs, `--dx-*`, bento.html, Abnahme im Bauplan) | MOVE | B#Profilwerte BPM und Heidi; S#Zweck | in S neutral beschrieben mit Verweis auf B | | ✅ |
| R005 | S#Vorrang (Z. 39–54) | Delegation an code-erstellen (4 Zeilen), Zuständigkeit inkl. Generator-Quellen und Abnahme-Eintrag | KEEP | S#Vorrang / Delegation an andere Skills | wörtlich | | ✅ |
| R006 | S#Vorrang (Z. 56–59) | HTML in die Ablage; echter Code → code-erstellen; Mockup-Hook wartet auf festgehaltene Abnahme („Workflow, Schritt 4b“) | REWRITE | S#Vorrang / Delegation an andere Skills | Verweis über Abschnitt „Abnahme festhalten“ | | ✅ sinngemäß |
| R007 | S#Grundsätze (Z. 65–82) | Fragen nur bei offener Entscheidung, Auswahlfrage-Tabelle (8 Zeilen), Prosa nur wenn … | REWRITE | S#Grundsätze | Zeile „Pflichtansicht fehlt (Profil „Ansichten“)“ → `Mockup.Ansichten`; sonst wörtlich | | ✅ sinngemäß |
| R008 | S#Grundsätze (Z. 83–87) | Branch nach Branch-Policy, Rückfall ohne Profil, nie automatisch | KEEP | S#Grundsätze | wörtlich | | ✅ |
| R009 | S#Arbeitsverzeichnis (Z. 93–94) | Claude Code Repo-Wurzel; Cowork nach cc-steuerung | KEEP | S#Arbeitsverzeichnis (PFLICHT bei Dateizugriff) | wörtlich | | ✅ |
| R010 | S#Voraussetzung: Mockup-Profil (Z. 100–101) | Profil steht im Abschnitt `## Mockup-Profil` der CLAUDE.md | REWRITE | S#Voraussetzung: Skill-Profil | jetzt Schritt 2 (Rückfall) hinter dem Skill-Profil v1 (N001) | | ✅ sinngemäß |
| R011 | S#Voraussetzung (Z. 103–114) | Felder und Bedeutung (10 Zeilen) | REWRITE | S#Voraussetzung: Skill-Profil | Feld und Bedeutung bleiben, neue Spalte „Skill-Profil“ (N002); BPM/Heidi-Spalten → R012 | | ✅ sinngemäß |
| R012 | S#Voraussetzung (Z. 103–114) | Werte BPM und Heidi je Feld | MOVE | B#Profilwerte BPM und Heidi | wörtlich | | ✅ |
| R013 | S#Voraussetzung (Z. 116–117) | Fehlt das Profil: BPM-Werte nur bei `Docs/Mockups/`, sonst Auswahlfrage | REWRITE | S#Voraussetzung: Skill-Profil | Schritt 3 „Fehlt beides“, BPM-Werte aus B | | ✅ sinngemäß |
| R014 | S#Sitemap und Klick-Navigation (Z. 123–126) | Bei „Sitemap: ja“ gilt M; vor jedem Mockup lesen; sonst nicht laden | REWRITE | S#Sitemap und Klick-Navigation (Profil „Sitemap: ja“) | „(BPM)“ entfernt | | ✅ sinngemäß |
| R015 | S#Docs laden (Z. 132–136) | Pflicht vor der Erstellung; keine Werte im Skill; Designquelle und Referenz-Mockup lesen | REWRITE | S#Docs laden | Werkzeugnamen (Read, DC, github) → „Datei lesen“; Cowork-Werkzeuge → C#Docs und Ablage lesen | | ✅ sinngemäß |
| R016 | S#Docs laden (Z. 138–141) | Heidi: tokens.ts komplett, bento.html Kopf, Bauplan 7, Aufgabenkarte, Regel 14 | MOVE | B#Docs laden BPM und Heidi; S#Docs laden | in S neutral: Designquelle vollständig, Kopf des Referenz-Mockups, Seitenübersicht, Aufgabe, Projektregeln für Mockups | | ✅ |
| R017 | S#Quickload-First-Pass (BPM) (Z. 143–152) | BPM-Docs mit Pfaden | MOVE | B#Docs laden BPM und Heidi; S#Docs laden | in S neutral: Ladereihenfolge des Projekts (Quickload, Router) | | ✅ |
| R018 | S#Bestehende Mockups prüfen (Z. 156–161) | Ablage listen; NN_Fenster existiert → Variante | REWRITE | S#Bestehende Mockups prüfen; C#Docs und Ablage lesen | Werkzeuge raus, Muster `<Ablage>/**/*.html`; Heidi-Pfad → B | | ✅ sinngemäß |
| R019 | S#Bestehende Mockups prüfen (Z. 162–163) | Update: Auswahlfrage; Heidi: abgelöste Mockups bleiben, „abgelöst durch“ im Bauplan | REWRITE | S#Bestehende Mockups prüfen; B#Docs laden BPM und Heidi | neutral: Vermerk am Abnahme-Ort | | ✅ sinngemäß |
| R020 | S#Sitemap laden (Z. 165–172) | Vor jedem neuen Mockup `_SITEMAP.md` lesen; Kanten kennen; tote Pfade prüfen | REWRITE | S#Sitemap laden (zusätzlich, nur bei Profil „Sitemap: ja“) | Pfad über `<Ablage>`; „ab 2026-05“ → D1; `read_file` → C | | ✅ sinngemäß |
| R021 | S#Design-Referenz (Z. 176–179) | Bestehenden UI-Code oder Screenshot als Stil-Referenz; Konsistenz | REWRITE | S#Design-Referenz aus bestehenden Screens | BPM-/Heidi-Dateien → B | | ✅ sinngemäß |
| R022 | S#Workflow (Z. 185) | Workflow verbindlich | REWRITE | S#Workflow | „Verbindlich, in dieser Reihenfolge.“ (Schritte ohne Nummern) | | ✅ sinngemäß |
| R023 | S#Schritt 1 (Z. 187–191) | Kontext sammeln, vier Fragen | KEEP | S#Kontext sammeln | Überschrift ohne Nummer | | ✅ |
| R024 | S#Schritt 2 (Z. 193–197) | Docs laden: Designquelle/Referenz, Sitemap (BPM), Aufgabenquelle (Heidi-Karte), Memory/Design-Entscheidungen | REWRITE | S#Docs laden (im Ablauf); B#Docs laden BPM und Heidi | neutral: `Code.Aufgabenquelle`, `Doku.Entscheidungs-Ort` (N003); Heidi-Orte → B | | ✅ sinngemäß |
| R025 | S#Schritt 3 (Z. 199–206) | Vorschau: Cowork Visualizer; Claude Code Datei + Browser + SendUserFile + Ansichten nachstellen; iterieren | REWRITE | S#Vorschau; C#Vorschau | Cowork-Teil → C; „390 px“ → „Breite der Ansicht“ | | ✅ sinngemäß |
| R026 | S#Schritt 3b (Z. 208–214) | Token-Abgleich Pflicht; Abweichungsliste + Auswahlfrage; neue Tokens = Abweichung; keine Werte, die Standard werden | REWRITE | S#Token-Abgleich (Pflicht vor dem Speichern) | Heidi/BPM-Quellen raus; „Karten-Standard“ → „Standard der App“ | | ✅ sinngemäß |
| R027 | S#Schritt 3c (Z. 216–218) | Pflichtansichten vorhanden; sonst Auswahlfrage | REWRITE | S#Ansichten prüfen (`Mockup.Ansichten`) | Heidi-Werte → Beispiel „Desktop und Smartphone-Breite“ | | ✅ sinngemäß |
| R028 | S#Schritt 4 (Z. 220–225) | Speichern erst nach Bestätigung; Claude Code Write; Cowork DC mit Trigger; Namensschema; Sitemap-Pflichten | REWRITE | S#Auf Platte speichern; C#Speichern | Cowork-Teil → C | | ✅ sinngemäß |
| R029 | S#Schritt 4b (Z. 227–234) | Abnahme: Auswahlfrage nach finaler Vorschau; an Abnahme-Ort schreiben (Datum, Datei, Umfang, Weggelassenes); ohne Eintrag nicht abgenommen; „Später“ blockiert | REWRITE | S#Abnahme festhalten; B#Abnahme-Ort | Heidi-/BPM-Orte → B; neutral: Register für Abweichungen (N004) | | ✅ sinngemäß |
| R030 | S#Schritt 5 (Z. 236–240) | Commit-Vorschlag: Format, Version nach Bump-Regel, Abnahme im selben Commit, Sitemap erwähnen | REWRITE | S#Commit-Vorschlag; B#Commit | `Commit.Format`, `Commit.Module`, `Commit.Versionsregel`; BPM/Heidi → B | | ✅ sinngemäß |
| R031 | S#Standalone-fähig (Z. 246–249) | allein öffenbar; eigener style-Block mit Tokens; kein Framework, keine externen Dependencies | REWRITE | S#Standalone-fähig | „Heidi Regel 14“ → „wenn das Projekt sie verbietet“ | | ✅ sinngemäß |
| R032 | S#Tokens in der Form des Profils (Z. 251–255) | Visualizer-Variablen nie ins Mockup; BPM Hex; Heidi `--dx-*` wie tokens.ts; Werte laden, nicht hardcoden | REWRITE | S#Tokens in der Form des Profils; C#Visualizer-Variablen; B#Profilwerte BPM und Heidi | neutral: Hex oder CSS-Variablen mit Werten der Quelle | | ✅ sinngemäß |
| R033 | S#Struktur (Z. 257–272) | HTML-Grundgerüst | REWRITE | S#Struktur | Kommentar im style-Block neutral | | ✅ sinngemäß |
| R034 | S#Interaktivität (Z. 274–278) | Hover, Tabs, Klick-Navigation Pflicht bei Sitemap; Heidi Tabs/Zustände; keine komplexe Logik | REWRITE | S#Interaktivität | Heidi → „ohne Sitemap: Tabs … Zustände (z. B. …)“ | | ✅ sinngemäß |
| R035 | S#VERBOTEN (Z. 285–288) | Werte hardcoden; ohne Docs; ohne Bestätigung; ohne DC-Trigger (Cowork) | KEEP | S#VERBOTEN | DC-Zeile mit Verweis auf C | | ✅ |
| R036 | S#VERBOTEN (Z. 289) | NN-Nummer doppelt (BPM) | REWRITE | S#VERBOTEN | „(Profil „Sitemap: ja“)“ | | ✅ sinngemäß |
| R037 | S#VERBOTEN (Z. 290–293) | Umlaute/Leerzeichen; Visualizer-HTML speichern; Branch | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R038 | S#VERBOTEN (Z. 294–296) | Speichern ohne Token-Abgleich (Schritt 3b), ohne Pflichtansichten (Heidi …), Abnahme nur im Chat (Schritt 4b) | REWRITE | S#VERBOTEN | Verweise über Abschnittsnamen, `Mockup.Ansichten` | | ✅ sinngemäß |
| R039 | S#VERBOTEN (Z. 297) | BPM-Ablage für anderes Projekt annehmen – alles aus dem Mockup-Profil | REWRITE | S#VERBOTEN | „aus dem Skill-Profil“ | | ✅ sinngemäß |
| R040 | S#VERBOTEN (Z. 298–302) | externe Ressourcen; Prosa-Fragen; Klick-Navigation; Sitemap-Update; tote Pfade | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R041 | S#VERBOTEN (Z. 303) | Aufrufer-HTMLs patchen – „Schritt 2 ist Pflicht“ | REWRITE | S#VERBOTEN | Abschnitt „Aufrufer-HTMLs patchen“ in M | | ✅ sinngemäß |
| R042 | S#VERBOTEN (Z. 304) | onclick ohne Selbstcheck | KEEP | S#VERBOTEN | wörtlich | | ✅ |
| R043 | M#Namenskonvention (Z. 18) | Überschrift „Ordnerstruktur (ab 2026-05)“ | REWRITE | M#Ordnerstruktur | Datum → D1 | | ✅ sinngemäß |
| R044 | M#Modul-Ordner (Z. 65) | Ordnername = Modulname, Liste der BPM-Module | REWRITE | M#Modul-Ordner | als „Beispiel BPM“ gekennzeichnet | | ✅ sinngemäß |
| R045 | M#Sonderregeln (Z. 96) | Legacy-Dateien (vor 2026-05) bei Bedarf in Fenster-Ordner verschieben | REWRITE | M#Sonderregeln | „Einzelne Mockup-Dateien außerhalb eines Fenster-Ordners …“; Datum → D1 | | ✅ sinngemäß |
| R046 | M#Interaktivität (Z. 102) | Pflicht bei Sitemap (ab 2026-05) | REWRITE | M#Interaktivität und Klick-Navigation | Datum → D1 | | ✅ sinngemäß |
| R047 | M#Sitemap und Selbstcheck (Z. 175) | Ab 2026-05, nur bei Sitemap | REWRITE | M#Sitemap und Selbstcheck | Datum → D1 | | ✅ sinngemäß |
| R048 | M#Neues Fenster anlegen (Z. 242–285) | Sub-Workflow Schritt 1–6 | REWRITE | M#Neues Fenster anlegen | Überschriften ohne „Schritt N —“, „in dieser Reihenfolge“; „Schritt 6 — Selbstcheck“ → „Selbstcheck nach dem Anlegen“ | | ✅ sinngemäß |
| R049 | M#Sitemap-Cleanup (Z. 321) | Wie „Neues Fenster anlegen“, Schritt 5 | REWRITE | M#Sitemap-Cleanup auch hier | Abschnitt „Tote Pfade scannen“ | | ✅ sinngemäß |
| R050 | M (übrige Abschnitte) | Schema, NN-Vergabe, Beispiele, Klick-Navigation, Sitemap-Format, Pflege-Pflicht, Selbstcheck, Nachträglich hinzufügen | KEEP | M | wörtlich | | ✅ |
| N001 | – | Skill-Profil v1 zuerst: Pflichtfelder `Mockup.Ablage`, `Designquelle`, `Ansichten`, `Abnahme-Ort`, dazu `Commit.Format`/`Module`; fehlendes Feld nach „Fehlende Werte“ | NEW | S#Voraussetzung: Skill-Profil | `docs/skill-profile-v1.md`, Pflichtfelder je Skill; Muster doc-pflege v0.60.0 | Herbert 25.10.2026 | ✅ |
| N002 | – | Spalte „Skill-Profil“: wo jedes Feld des alten Profils im Skill-Profil v1 steht (Sitemap = `_SITEMAP.md` in der Ablage) | NEW | S#Voraussetzung: Skill-Profil | wie N001 | Herbert 25.10.2026 | ✅ |
| N003 | – | Aufgabenquelle `Code.Aufgabenquelle`, Design-Entscheidungen am `Doku.Entscheidungs-Ort` | NEW | S#Docs laden (im Ablauf) | Skill-Profil v1 statt Heidi-Orte | Herbert 25.10.2026 | ✅ |
| N004 | – | Abnahme: Register für gewollte Abweichungen, wenn das Projekt eins führt | NEW | S#Abnahme festhalten | verallgemeinert den Heidi-PD-Eintrag (R029) | Herbert 25.10.2026 | ✅ |
| N005 | – | Neue Reference `beispiele.md` mit Inhaltsverzeichnis, Rückfall nur für BPM | NEW | B | Muster chatgpt-review `references/beispiele.md` | Herbert 25.10.2026 | ✅ |
| N006 | – | Neue Reference `cowork.md`: Lesen, Vorschau, Speichern nur auf DC-Auftrag, Visualizer-Variablen | NEW | C | `docs/skill-quality.md#Neutralität` (Cowork in eine Reference) | Herbert 25.10.2026 | ✅ |

## DROP-Gruppen

| Gruppe | IDs | Was fällt weg | Grund | Freigabe |
|---|---|---|---|---|
| D1 Historie | R020, R043, R045, R046, R047 | die Datumsangaben „ab 2026-05“ und „Legacy-Stand vor 2026-05“ – die Regeln selbst bleiben | `docs/skill-quality.md#Inhalt` (keine Historie im Regeltext); Historie im CHANGELOG | Herbert 25.10.2026 |

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/code-erstellen/SKILL.md` Z. 238, 324 | Mockup-Hook, „Schritt 1/2“ | Schritte von code-erstellen selbst; passt |
| `INDEX.md` Z. 26 | „HTML-Mockups nach dem Mockup-Profil“ | passt (Description nennt weiter „Mockup-Profil“) |
| `README.md` Z. 278 | „nach Mockup-Profil“ | passt |
| `README.md` Aufbau | `mockup-erstellen/SKILL.md` | im selben Commit: „SKILL.md + references/ (sitemap, beispiele, cowork)“ |
| `docs/skill-refactors/2026-10-22-mockup-erstellen.md` | Abschnitte „Voraussetzung: Mockup-Profil“, „Workflow Schritt 4b“ | Historie, bleibt |

## Prüfung

- **Freigabe:** Zielstruktur und D1 per Auswahlfrage am 25.10.2026.
- **Alt→Neu:** R001–R050 haben einen Zustand (KEEP 10, MOVE 4, REWRITE 36, DROP 0 – D1 streicht nur Datumsteile innerhalb
  von REWRITE-Zeilen) und N001–N006. Jeder Neu-Ort ist als Überschrift im neuen Text vorhanden.
- **Neu→Alt:** neuer Text Zeile für Zeile gegen den alten gelesen (`git diff` gegen 8cfb8c5); jede Aussage gehört zu einer
  R-ID oder N001–N006.
- **Zeilen:** `SKILL.md` 304 → 294; References 322 + 59 + 31. Keine Projektwerte mehr im Kern außer den Hinweisen auf B
  und dem Rückfall „nur wenn das Repo `Docs/Mockups/` hat“ (R013).
- **Description:** unverändert (911 Zeichen).
- **Prüfskript:** CI `validate-skills` für 7fb60b4 grün (Lauf 40171408860).
- **Routing-Eval** (7fb60b4, `--runs 3 --tag mockup-erstellen`): 16/16 Fälle mit 3/3. Report
  `quality/evals/results/2026-10-25T07-04-29-900Z/`.
