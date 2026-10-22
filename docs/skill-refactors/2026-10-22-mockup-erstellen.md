# Regel-Inventar – mockup-erstellen, Split 2026-10-22

- **Skill:** mockup-erstellen
- **Stand vor dem Umbau:** Commit 3b77fa7, `SKILL.md` 589 Zeilen (Körper rund 573, über der Grenze von 500)
- **Anlass:** Split-Prüfung bei mockup-erstellen-003; Herbert hat „Jetzt aufteilen“ und die Zielstruktur freigegeben
- **Quellen:** `skills/mockup-erstellen/SKILL.md` (alt), `docs/skill-quality.md#Aufbau`

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck · Vorrang / Delegation · Grundsätze · Arbeitsverzeichnis · Voraussetzung: Mockup-Profil · Sitemap und Klick-Navigation (Profil „Sitemap: ja“) · Docs laden · Workflow · HTML-Regeln für Mockups · VERBOTEN |
| `references/sitemap.md` | Inhalt · Namenskonvention · Interaktivität und Klick-Navigation · Sitemap und Selbstcheck · Neues Fenster anlegen · Fenster nachträglich hinzufügen |

Die bisherigen Kapitel 1 und 5–8 (nur bei Profil „Sitemap: ja“, BPM) ziehen wörtlich in die Reference. Überschriften
verlieren ihre Nummern; Zusätze wie „verbindlich“ oder „nur bei Profil …“ stehen als erste Zeile darunter. Verweise der
Form „Kapitel N“ zeigen jetzt auf Datei und Überschrift.

## Inventar

Eine Zeile je Listenpunkt, Tabellenzeile, Absatz oder Codeblock (Muster) des alten Stands; Überschriften nur, wo sie
umformuliert wurden.

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 3) | Description (Use when / Do not trigger) | KEEP | SKILL.md#Frontmatter |  | | ✅ |
| R002 | SKILL.md#Frontmatter (Z. 18) | # Mockup-Erstellen — UI-Entwürfe als HTML | KEEP | SKILL.md#Frontmatter |  | | ✅ |
| R003 | SKILL.md#Zweck (Z. 22) | Erstellt HTML-Mockups für die Screens des aktiven Projekts. Stellt sicher dass: | KEEP | SKILL.md#Zweck |  | | ✅ |
| R004 | SKILL.md#Zweck (Z. 23) | - Die Namenskonvention und Ablage des Projekts eingehalten wird (Mockup-Profil) | KEEP | SKILL.md#Zweck |  | | ✅ |
| R005 | SKILL.md#Zweck (Z. 24) | - Die richtigen Docs und Design-Tokens des Projekts geladen werden | KEEP | SKILL.md#Zweck |  | | ✅ |
| R006 | SKILL.md#Zweck (Z. 25) | - Der Workflow (Preview → Bestätigung → Speichern → Abnahme festhalten) befolgt wird | KEEP | SKILL.md#Zweck |  | | ✅ |
| R007 | SKILL.md#Zweck (Z. 26) | - Bestehende Mockups nicht überschrieben werden | KEEP | SKILL.md#Zweck |  | | ✅ |
| R008 | SKILL.md#Zweck (Z. 27) | - Der Stil konsistent über alle Screens bleibt (Token-Abgleich mit der Design-Quelle) | KEEP | SKILL.md#Zweck |  | | ✅ |
| R009 | SKILL.md#Zweck (Z. 29) | Was projektspezifisch ist, steht im **Mockup-Profil** (Abschnitt „Voraussetzung: Mockup-Profil“). | KEEP | SKILL.md#Zweck |  | | ✅ |
| R010 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 38) | **mockup-erstellen ist für UI-Entwürfe als HTML-Mockup. Wenn die Hauptabsicht | KEEP | SKILL.md#Vorrang / Delegation an andere Skills |  | | ✅ |
| R011 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 43) | \| View/Komponente schreiben oder ändern (XAML, Lit-Komponente, Dialog) \| **code-erstellen** \| | KEEP | SKILL.md#Vorrang / Delegation an andere Skills |  | | ✅ |
| R012 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 44) | \| ViewModel, Commands, Bindings, Selektoren implementieren \| **code-erstellen** \| | KEEP | SKILL.md#Vorrang / Delegation an andere Skills |  | | ✅ |
| R013 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 45) | \| Kleiner UI-Fix in bestehendem Code (Farbe, Größe, Binding) \| **code-erstellen** \| | KEEP | SKILL.md#Vorrang / Delegation an andere Skills |  | | ✅ |
| R014 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 46) | \| Code-Struktur oder Logik der UI \| **code-erstellen** \| | KEEP | SKILL.md#Vorrang / Delegation an andere Skills |  | | ✅ |
| R015 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 48) | Nur wenn die Hauptabsicht **ein neuer UI-Entwurf als HTML-Mockup** ist | KEEP | SKILL.md#Vorrang / Delegation an andere Skills |  | | ✅ |
| R016 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 53) | **Wichtig:** Mockup-erstellen liefert HTML in die Mockup-Ablage des Profils. Sobald es um | REWRITE | SKILL.md#Vorrang / Delegation an andere Skills |  | | ✅ sinngemäß |
| R017 | SKILL.md#Grundsätze (Z. 62) | - **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas  | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R018 | SKILL.md#Grundsätze (Z. 67) | \| Token-Abgleich zeigt Abweichungen \| Mockup an Tokens anpassen, Tokens-Datei ändern (→ code-erstellen), Abw | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R019 | SKILL.md#Grundsätze (Z. 68) | \| Pflichtansicht fehlt (Profil „Ansichten“) \| Ansicht ergänzen, Ohne speichern (Begründung), Abbrechen \| | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R020 | SKILL.md#Grundsätze (Z. 69) | \| Abnahme \| Abgenommen, Änderungen nötig, Später \| | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R021 | SKILL.md#Grundsätze (Z. 70) | \| Bestehendes Mockup gefunden: Archiv vs. Überschreiben \| Archivieren (_ARCHIV suffix), Überschreiben, Abbre | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R022 | SKILL.md#Grundsätze (Z. 71) | \| NN-Nummer belegt \| Nächste freie Nummer, Andere Nummer wählen, Abbrechen \| | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R023 | SKILL.md#Grundsätze (Z. 72) | \| Mehrere Stil-Referenzen möglich \| Referenz-Dateinamen als Optionen \| | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R024 | SKILL.md#Grundsätze (Z. 73) | \| Fenster-Ordner existiert bereits (neue Variante) \| Variante hinzufügen, Bestehende ersetzen, Abbrechen \| | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R025 | SKILL.md#Grundsätze (Z. 74) | \| Eingehende Links unklar beim neuen Fenster \| Liste vorhandener Fenster aus Sitemap als Optionen + "Keine e | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R026 | SKILL.md#Grundsätze (Z. 77) | - Offene Frage ohne feste Optionen (z.B. "Welche Daten/Felder soll der Screen zeigen?") | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R027 | SKILL.md#Grundsätze (Z. 78) | - User hat Präferenz signalisiert | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R028 | SKILL.md#Grundsätze (Z. 79) | - Freitext-Input nötig | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R029 | SKILL.md#Grundsätze (Z. 80) | - **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der S | KEEP | SKILL.md#Grundsätze |  | | ✅ |
| R030 | SKILL.md#Arbeitsverzeichnis (PFLICHT bei Dateizugriff) (Z. 90) | Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`). | KEEP | SKILL.md#Arbeitsverzeichnis (PFLICHT bei Dateizugriff) |  | | ✅ |
| R031 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 97) | Abschnitt `## Mockup-Profil` in der `CLAUDE.md` des Repos (Claude Code liest sie automatisch; | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R032 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 102) | \| Ablage \| Ordner für Mockups \| `Docs/Mockups/<Modul>/NN_Fenster/` \| `dreame_x60/mockups/` (flach) \| | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R033 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 103) | \| Namensschema \| Datei- und Ordnernamen \| `NN_Fenster/NN_Variante.html` (Kapitel 1) \| `<thema>.html`, klei | REWRITE | SKILL.md#Voraussetzung: Mockup-Profil | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R034 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 104) | \| Design-Quelle \| Datei mit den gültigen Tokens \| `Colors.xaml`, `UI_UX_Guidelines.md`, `WPF_UI_Architectur | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R035 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 105) | \| Referenz-Mockup \| Stilvorlage für neue Mockups \| letztes Mockup im selben Modul \| `dreame_x60/mockups/be | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R036 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 106) | \| Token-Form im HTML \| wie Tokens im Mockup stehen \| Hex-Werte aus Colors.xaml \| CSS-Variablen `--dx-*` mi | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R037 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 107) | \| Ansichten \| Pflichtansichten je Mockup \| Desktop \| Desktop **und** 390 px (Smartphone) nebeneinander, Ta | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R038 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 108) | \| Sitemap / Klick-Navigation \| Kapitel 1 und 5–8 anwenden? \| ja \| nein (Tabs in der Datei, keine Kanten) \ | REWRITE | SKILL.md#Voraussetzung: Mockup-Profil | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R039 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 109) | \| Vorschau \| wie der User das Mockup sieht \| Visualizer (Cowork) \| Claude Code: Browser-Bereich (Datei öff | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R040 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 110) | \| Abnahme-Ort \| wo die Abnahme festgehalten wird \| `_SITEMAP.md` (Status ✅) \| Bauplan Abschnitt 7 (Seitent | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R041 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 111) | \| Commit-Modul \| Modulname für den Commit \| `Docs` \| `Doku` \| | KEEP | SKILL.md#Voraussetzung: Mockup-Profil |  | | ✅ |
| R042 | SKILL.md#Voraussetzung: Mockup-Profil (Z. 113) | **Fehlt das Profil:** BPM-Werte aus diesem Skill annehmen (Kapitel 1–8) – nur wenn das Repo | REWRITE | SKILL.md#Voraussetzung: Mockup-Profil | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R043 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 118) | ## 1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) | REWRITE | references/sitemap.md#Namenskonvention | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R044 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 122) | Jedes Fenster (Screen, Wizard, Dialog) bekommt **einen eigenen Ordner**. Mockup-Dateien | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R045 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 126) | Codeblock/Muster: Docs/Mockups/ | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R046 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 142) | Codeblock/Muster: <Modul>/NN_Fenster/NN_Variante.html | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R047 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 148) | \| **Modul** \| Modulname aus der App \| PlanManager, Settings \| | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R048 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 149) | \| **NN_Fenster** \| Ordner pro Fenster, NN = Navigationstiefe (2-stellig) \| 01_Projektuebersicht, 04_ProfilW | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R049 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 150) | \| **NN_Variante** \| Datei innerhalb des Fenster-Ordners. NN = Reihenfolge bei Mehrfach-Files \| 01_Hauptansi | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R050 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 154) | - **01** — Hauptseite des Moduls (z.B. Projektübersicht) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R051 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 155) | - **02** — Detail-/Unterseite (z.B. Projektdetail) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R052 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 156) | - **03+** — weitere Screens, Dialoge, Wizards in der Reihenfolge des Auftretens | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R053 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 160) | - **Single-Screen-Fenster:** eine Datei, z.B. `01_Hauptansicht.html` oder `01_<Fenstername>.html` | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R054 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 161) | - **Tab-Ansichten:** eine Datei pro Tab, NN entspricht Tab-Reihenfolge | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R055 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 162) | - **Wizard-Schritte:** eine Datei pro Schritt, NN = Schritt-Nummer | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R056 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 163) | - **Design-Varianten während Klärungsphase:** `01_Variante_Kompakt.html`, `01_Variante_Breit.html` — nach Ausw | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R057 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 167) | Ordnername = Modulname aus der App: | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R058 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 168) | - `PlanManager` | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R059 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 169) | - `Settings` (oder `Einstellungen`, je nach App-Namen) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R060 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 170) | - `Foto` (wenn Modul gebaut wird) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R061 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 171) | - `Zeiterfassung` (wenn Modul gebaut wird) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R062 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 172) | - `Bautagebuch` (wenn Modul gebaut wird) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R063 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 176) | Codeblock/Muster: PlanManager/01_Projektuebersicht/01_Projektuebersicht.html | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R064 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 195) | - Keine Umlaute in Ordner- und Dateinamen (ue statt ü, ae statt ä) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R065 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 196) | - Keine Leerzeichen (Underscore als Trenner) | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R066 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 197) | - Archiv-Ordner: `_Archiv/` mit Unterstrich-Prefix → sortiert ans Ende | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R067 | SKILL.md#1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM) (Z. 198) | - Bestehende einzelne Mockup-Dateien (Legacy-Stand vor 2026-05) werden bei Bedarf in passenden Fenster-Ordner  | MOVE | references/sitemap.md#Namenskonvention |  | | ✅ |
| R068 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 202) | ## 2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) | REWRITE | SKILL.md#Docs laden | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R069 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 204) | Der Skill speichert KEINE Farbwerte, Spacing, Token-Namen. | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R070 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 208) | Heidi: `tokens.ts` komplett (alle `--dx-*`), `bento.html` Kopf (`:root`-Block, Layout-Regeln | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R071 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 215) | Folgende Docs laden (Quickload reicht, kein Langform): | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R072 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 219) | \| **UI_UX_Guidelines.md** \| Design-Token, Spacing, Komponenten \| `github:get_file_contents` → `Docs/Referen | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R073 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 220) | \| **WPF_UI_Architecture.md** \| Token→WPF-Key Mapping, Dialog-Pattern \| `github:get_file_contents` → `Docs/R | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R074 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 221) | \| **Colors.xaml** \| Aktuelle Farbwerte \| `github:get_file_contents` → `src/BauProjektManager.App/Themes/Col | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R075 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 222) | \| **Icons.xaml** \| Verfügbare Icon-Keys \| `github:get_file_contents` → `src/BauProjektManager.App/Themes/Ic | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R076 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 226) | Vor Erstellung eines neuen Mockups die Ablage des Profils listen: | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R077 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 227) | Codeblock/Muster: Cowork: list_directory → Docs/Mockups/<Modul>/ | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R078 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 231) | - Prüfe ob `NN_Fenster/`-Ordner schon existiert (dann ist es eine neue Variante, kein neues Fenster — siehe Ka | REWRITE | SKILL.md#Docs laden | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R079 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 232) | - Bei Update einer bestehenden Mockup-Datei: Per Auswahlfrage fragen (Archivieren, Überschreiben, Abbrechen). | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R080 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 237) | Vor jedem neuen Mockup: | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R081 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 238) | Codeblock/Muster: read_file → Docs/Mockups/<Modul>/_SITEMAP.md | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R082 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 241) | - Bestehende Navigationskanten kennen (welche Fenster gibt es schon? wer ruft was auf?) | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R083 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 242) | - Bei totem Pfad (`alert('Mockup folgt: X')`): prüfen ob X jetzt existiert → Cleanup (siehe Kapitel 6) | REWRITE | SKILL.md#Docs laden | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R084 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 246) | Wenn ein neuer Screen im gleichen Modul/Stil wie ein bestehender sein soll: | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R085 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 247) | - Bestehenden UI-Code laden (BPM: XAML via GitHub/DC; Heidi: Komponente `src/components/dx-*.ts` + `styles/con | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R086 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 248) | - ODER Screenshot vom User anfragen | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R087 | SKILL.md#2. DOCS LADEN (PFLICHT vor Mockup-Erstellung) (Z. 249) | - Ziel: Konsistenz über alle Screens | KEEP | SKILL.md#Docs laden |  | | ✅ |
| R088 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 253) | ## 3. WORKFLOW (VERBINDLICH) | REWRITE | SKILL.md#Workflow | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R089 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 256) | - Welches Modul? Welcher Screen? | KEEP | SKILL.md#Workflow |  | | ✅ |
| R090 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 257) | - Gibt es schon ein Mockup das aktualisiert werden soll? | KEEP | SKILL.md#Workflow |  | | ✅ |
| R091 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 258) | - Welche Daten/Felder soll der Screen zeigen? | KEEP | SKILL.md#Workflow |  | | ✅ |
| R092 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 259) | - Gibt es einen bestehenden Screen als Stil-Referenz? | KEEP | SKILL.md#Workflow |  | | ✅ |
| R093 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 262) | - Design-Quelle und Referenz-Mockup des Profils (Kapitel 2); BPM zusätzlich Quickload-First-Pass, Colors.xaml | REWRITE | SKILL.md#Workflow | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R094 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 263) | - `_SITEMAP.md` des betroffenen Moduls (nur BPM) | KEEP | SKILL.md#Workflow |  | | ✅ |
| R095 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 264) | - Aufgabenquelle des Schritts (Heidi: Bauplan-Karte, Akzeptanz = was das Mockup zeigen muss) | KEEP | SKILL.md#Workflow |  | | ✅ |
| R096 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 265) | - Memory prüfen auf Design-Entscheidungen (z.B. Karten-Design-Regeln; Heidi: Bauplan Abschnitt 10, PD-Register | KEEP | SKILL.md#Workflow |  | | ✅ |
| R097 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 268) | - **Cowork:** Mockup als **Visualizer** (show_widget) im Chat anzeigen | KEEP | SKILL.md#Workflow |  | | ✅ |
| R098 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 269) | - **Claude Code:** Datei in die Ablage schreiben (Schritt 4 ist hier dieselbe Datei) und im | KEEP | SKILL.md#Workflow |  | | ✅ |
| R099 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 273) | - User bestätigt oder gibt Änderungswünsche | KEEP | SKILL.md#Workflow |  | | ✅ |
| R100 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 274) | - Iterieren bis User zufrieden ist | KEEP | SKILL.md#Workflow |  | | ✅ |
| R101 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 277) | - Alle Token-Werte im Mockup (`:root`-Block bzw. Hex-Werte) gegen die **Design-Quelle** des Profils | KEEP | SKILL.md#Workflow |  | | ✅ |
| R102 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 279) | - Abweichungen als Liste (Token, Mockup-Wert, Quell-Wert) → Auswahlfrage: Mockup anpassen / | KEEP | SKILL.md#Workflow |  | | ✅ |
| R103 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 281) | - Neue Tokens, die es in der Quelle nicht gibt, gelten als Abweichung | KEEP | SKILL.md#Workflow |  | | ✅ |
| R104 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 282) | - Mockup darf keine Werte enthalten, die später „aus Versehen“ Karten-Standard werden | KEEP | SKILL.md#Workflow |  | | ✅ |
| R105 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 285) | - Jede Pflichtansicht ist im Mockup vorhanden (Heidi: Desktop + 390 px; Tablet bei Container-Regeln) | KEEP | SKILL.md#Workflow |  | | ✅ |
| R106 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 286) | - Fehlt eine → Auswahlfrage: ergänzen / ohne speichern (Begründung) / abbrechen | KEEP | SKILL.md#Workflow |  | | ✅ |
| R107 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 289) | - Erst nach User-Bestätigung | KEEP | SKILL.md#Workflow |  | | ✅ |
| R108 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 290) | - **Claude Code:** Write in die Ablage des Profils (Repo-Wurzel + Ablage); kein zusätzlicher Trigger nötig | KEEP | SKILL.md#Workflow |  | | ✅ |
| R109 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 291) | - **Cowork:** via DC `write_file` in `<workFolder>/<Ablage>/…`; User muss DC explizit triggern ("dc", "cc", "a | KEEP | SKILL.md#Workflow |  | | ✅ |
| R110 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 292) | - Dateiname nach Namensschema des Profils (BPM: Kapitel 1) | REWRITE | SKILL.md#Workflow | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R111 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 293) | - Nur bei Profil „Sitemap: ja“: Sitemap aktualisieren (Kapitel 6), Aufrufer-HTMLs patchen (Kapitel 5 + 7), tot | REWRITE | SKILL.md#Workflow | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R112 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 296) | - Auswahlfrage „Abgenommen / Änderungen nötig / Später“ – erst nach der Vorschau der finalen Datei | KEEP | SKILL.md#Workflow |  | | ✅ |
| R113 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 297) | - Bei „Abgenommen“ an den **Abnahme-Ort des Profils** schreiben: Datum, Datei, Umfang (welche Seiten/Zustände) | KEEP | SKILL.md#Workflow |  | | ✅ |
| R114 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 301) | - Ohne festgehaltene Abnahme gilt das Mockup für code-erstellen (Mockup-Hook) als **nicht** abgenommen. | KEEP | SKILL.md#Workflow |  | | ✅ |
| R115 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 302) | - Bei „Später“: Hinweis, dass der Bau des Schritts blockiert bleibt. | KEEP | SKILL.md#Workflow |  | | ✅ |
| R116 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 305) | - Format: `[vX.Y.Z] <Commit-Modul des Profils>, Docs: Mockup <Datei> – <Kurztitel>` (BPM: `Docs`, Heidi: `Doku | KEEP | SKILL.md#Workflow |  | | ✅ |
| R117 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 306) | - Version: Bump-Regel des Commit-Profils (BPM: PATCH; Heidi: reine Doku-Commits behalten die Kartenversion) | KEEP | SKILL.md#Workflow |  | | ✅ |
| R118 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 307) | - Abnahme-Eintrag (Schritt 4b) im selben Commit | KEEP | SKILL.md#Workflow |  | | ✅ |
| R119 | SKILL.md#3. WORKFLOW (VERBINDLICH) (Z. 308) | - Falls Sitemap mitgeändert oder Aufrufer-Mockups gepatcht: in Commit-Message erwähnen | KEEP | SKILL.md#Workflow |  | | ✅ |
| R120 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 312) | ## 4. HTML-REGELN FÜR MOCKUPS | REWRITE | SKILL.md#HTML-Regeln für Mockups | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R121 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 315) | - Mockup-HTML muss im Browser allein öffenbar sein | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R122 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 316) | - Eigenes `<style>` Block mit den Tokens der Design-Quelle des Profils (geladen, nicht im Skill gespeichert) | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R123 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 317) | - Kein Framework, keine externen Dependencies (keine Web-Fonts, keine CDN-Skripte – Heidi Regel 14) | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R124 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 320) | - Der Visualizer (Cowork) nutzt eigene CSS-Variablen (--color-background-primary etc.) – die dürfen nie ins ge | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R125 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 321) | - BPM: Tokens als Hex-Werte aus Colors.xaml | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R126 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 322) | - Heidi: Tokens als CSS-Variablen `--dx-*` in einem `:root`-Block mit **denselben Werten wie tokens.ts** (Toke | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R127 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 323) | - Werte aus der Design-Quelle laden, nicht hardcoden im Skill | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R128 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 326) | Codeblock/Muster: <!DOCTYPE html> | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R129 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 343) | - Hover-Effekte über `onmouseover`/`onmouseout` erlaubt | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R130 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 344) | - Tab-Wechsel via einfaches JS erlaubt | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R131 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 345) | - **Klick-Navigation zwischen Mockups: PFLICHT bei Profil „Sitemap: ja“** — siehe Kapitel 5; Heidi: Tabs inner | REWRITE | SKILL.md#HTML-Regeln für Mockups | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R132 | SKILL.md#4. HTML-REGELN FÜR MOCKUPS (Z. 346) | - Keine komplexe Logik — es ist ein Mockup, kein Prototyp | KEEP | SKILL.md#HTML-Regeln für Mockups |  | | ✅ |
| R133 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 350) | ## 5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) | REWRITE | references/sitemap.md#Interaktivität und Klick-Navigation | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R134 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 352) | Alle Mockups werden als **durchklickbarer Prototyp** ausgelegt. Buttons, Tabs, Karten, | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R135 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 357) | Jedes interaktive Element bekommt: | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R136 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 358) | Codeblock/Muster: onclick="location.href='<relativer_pfad>'" | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R137 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 362) | Plus visueller Hinweis auf Klickbarkeit (mindestens `cursor:pointer`, idealerweise Hover-Effekt). | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R138 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 366) | Pfade beziehen sich auf den Ordner des aktuellen Mockups: | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R139 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 368) | Codeblock/Muster: gleicher Fenster-Ordner: ./<NN_Variante>.html (z.B. Wizard-Schritt → nächster Schritt) | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R140 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 376) | Wenn das Ziel-Mockup geplant aber noch nicht gebaut ist: | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R141 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 378) | Codeblock/Muster: onclick="alert('Mockup folgt: <Fenstername>')" | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R142 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 383) | Plus visueller Hinweis (gestrichelter Rand, reduzierte Deckkraft) — damit User beim | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R143 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 386) | Tote Pfade werden in der Sitemap mit Status `🟡 tot` markiert (Kapitel 6). | REWRITE | references/sitemap.md#Interaktivität und Klick-Navigation | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R144 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 390) | - **Gleicher Tab** (Default — natürliche App-Navigation, Browser-Zurück funktioniert) | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R145 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 391) | - Kein `target="_blank"` — Mockups simulieren echte App-Navigation, nicht externe Links | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R146 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 392) | - Sidebar/Modulleisten verlinken zwischen Modul-Ordnern | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R147 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 396) | **Projektübersicht-Karte klickt zur Detail-Ansicht:** | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R148 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 397) | Codeblock/Muster: <div class="projekt-karte" onclick="location.href='../02_Projektdetail/01_Profile.html'"> | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R149 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 403) | **Wizard "Weiter →"-Button:** | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R150 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 404) | Codeblock/Muster: <button onclick="location.href='./02_Segmente.html'">Weiter →</button> | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R151 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 408) | **Sidebar Settings-Eintrag aus PlanManager-Modul:** | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R152 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 409) | Codeblock/Muster: <div onclick="location.href='../../Settings/01_Allgemein/01_Allgemein.html'">⚙ Einstellungen | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R153 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 413) | **Toter Pfad (Mockup noch nicht da):** | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R154 | SKILL.md#5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05) (Z. 414) | Codeblock/Muster: <button onclick="alert('Mockup folgt: ImportVorschau')" | MOVE | references/sitemap.md#Interaktivität und Klick-Navigation |  | | ✅ |
| R155 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 421) | ## 6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) | REWRITE | references/sitemap.md#Sitemap und Selbstcheck | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R156 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 425) | Zentrale Wahrheit für Navigationskanten. Wird bei jedem neuen Mockup gelesen und | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R157 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 428) | **Speicherort:** `Docs/Mockups/<Modul>/_SITEMAP.md` | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R158 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 432) | Codeblock/Muster: # <Modul> — Sitemap | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R159 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 456) | - **✅ aktiv** — beide Mockups existieren, Klick-Navigation funktioniert | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R160 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 457) | - **🟡 tot** — Ziel-Mockup fehlt noch, Aufrufer hat `alert('Mockup folgt: X')` | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R161 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 458) | - **❌ kaputt** — Pfad-Inkonsistenz (z.B. Datei verschoben, Link nicht angepasst) | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R162 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 462) | - **Vor jedem neuen Mockup:** Sitemap lesen | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R163 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 463) | - **Nach jedem neuen Mockup:** Sitemap aktualisieren (neue Kanten ergänzen, tote → aktiv wenn Ziel jetzt da) | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R164 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 464) | - **Bei Umbenennung/Verschiebung:** alle Pfade in Sitemap UND in HTML-onclick-Refs anpassen | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R165 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 465) | - **Bei Mockup-Löschung:** Sitemap-Einträge entfernen, eingehende Kanten auf `🟡 tot` setzen oder Aufrufer-Mock | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R166 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 469) | Vor Commit: | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R167 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 471) | 1. **Sitemap-Kanten vs HTML-onclick-Refs vergleichen** | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R168 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 472) | - Jede Kante in Sitemap muss als `onclick` im Quell-HTML existieren | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R169 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 473) | - Jeder `onclick` im HTML muss als Kante in der Sitemap stehen | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R170 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 474) | 2. **Datei-Existenz prüfen** | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R171 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 475) | - Jedes Ziel in `onclick="location.href='...'"` muss als Datei existieren | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R172 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 476) | - Falls nicht → Kante als `🟡 tot` markieren ODER `alert('Mockup folgt: X')` verwenden | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R173 | SKILL.md#6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“) (Z. 477) | 3. **Diskrepanzen melden** statt stillschweigend zu korrigieren — User entscheidet | MOVE | references/sitemap.md#Sitemap und Selbstcheck |  | | ✅ |
| R174 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 481) | ## 7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) | REWRITE | references/sitemap.md#Neues Fenster anlegen | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R175 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 483) | Wenn ein komplett neues Fenster (Screen, Wizard, Dialog) angelegt wird, läuft der | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R176 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 488) | Per Auswahlfrage oder Prosa (bei freiem Text-Input): | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R177 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 490) | - **Eingehende Links:** Aus welchen bestehenden Fenstern wird das neue aufgerufen? | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R178 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 491) | - Liste der vorhandenen Fenster aus Sitemap als Optionen | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R179 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 492) | - Plus "Keine eingehenden Links" (z.B. neues Hauptmenü) | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R180 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 493) | - **Trigger im Aufrufer:** Welcher Button/Karte/Tab löst die Navigation aus? | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R181 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 494) | - Freier Text-Input (z.B. "Button 'Neuen Dokumenttyp anlernen'") | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R182 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 495) | - **Ausgehende Links / Zurück-Verhalten:** Wohin kehrt das neue Fenster zurück? | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R183 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 496) | - Aufrufer (typisch bei Dialogen) \| Hauptseite \| Anderes Fenster \| Nirgends (Standalone) | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R184 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 497) | - **NN-Vergabe:** nächste freie Nummer, oder dazwischen-rücken (dann müssen nachfolgende renamed werden) | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R185 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 501) | Für jede genannte Eingangs-Quelle: | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R186 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 502) | 1. HTML-Datei laden | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R187 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 503) | 2. Passende Klick-Stelle suchen (Button-Label, Karte mit bekanntem Text, Tab) | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R188 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 504) | 3. `onclick="location.href='<pfad_zum_neuen_fenster>'"` einfügen | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R189 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 505) | 4. Falls bisher `alert('Mockup folgt: X')` mit dem genauen Fenster-Namen drin war → ersetzen | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R190 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 509) | Standard-Workflow (Kapitel 3) für das neue Fenster: | REWRITE | references/sitemap.md#Neues Fenster anlegen | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R191 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 510) | - Stil-Referenz: bestehende Mockups im selben Modul | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R192 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 511) | - Klick-Navigation: Zurück-Pfeil/Schließen-Button mit `onclick` zum angegebenen Rückkehr-Ziel | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R193 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 512) | - Tote Pfade für noch nicht existente Folge-Mockups | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R194 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 516) | `_SITEMAP.md` patchen: | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R195 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 517) | - Neuen Fenster-Eintrag in "Fenster"-Tabelle | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R196 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 518) | - Neue Kanten in "Navigationskanten"-Tabelle (eingehend + ausgehend) | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R197 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 519) | - Status entsprechend: `✅` wenn beide Seiten existieren, `🟡 tot` wenn Ziel/Quelle fehlt | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R198 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 523) | In allen HTML-Files des Moduls nach `alert('Mockup folgt: <neues_fenster>')` suchen: | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R199 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 524) | - Wenn gefunden → durch echten `location.href`-Link ersetzen | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R200 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 525) | - Sitemap-Status entsprechend von `🟡 tot` auf `✅` aktualisieren | MOVE | references/sitemap.md#Neues Fenster anlegen |  | | ✅ |
| R201 | SKILL.md#7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“) (Z. 529) | Kapitel 6 — Sitemap-Kanten vs HTML-onclick-Refs vergleichen, Datei-Existenz prüfen. | REWRITE | references/sitemap.md#Neues Fenster anlegen | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R202 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 533) | ## 8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) | REWRITE | references/sitemap.md#Fenster nachträglich hinzufügen | Überschrift ohne Nummer, Zusatz als erste Zeile | | ✅ sinngemäß |
| R203 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 535) | Wenn ein Fenster nachträglich (nach mehreren bereits gebauten Mockups) hinzugefügt | REWRITE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ sinngemäß |
| R204 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 540) | Beim nachträglichen Einfügen verändern sich oft auch **bestehende Navigationsflüsse**: | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R205 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 542) | - Bestehendes Fenster A ruft jetzt zusätzlich das neue Fenster N auf | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R206 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 543) | - Bestehendes Fenster B verlinkt evtl. auf N statt auf altes Fenster C | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R207 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 544) | - Sitemap-Reorganisation möglich (NN-Vergabe) | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R208 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 546) | **Aktion:** Per Auswahlfrage fragen ob bestehende Flüsse angepasst werden müssen. | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R209 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 550) | Falls die NN-Vergabe geändert werden soll (z.B. neues Fenster zwischen alten 02 und 03 | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R210 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 553) | - ALLE Mockup-Ordner umbenennen | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R211 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 554) | - ALLE relativen Pfade in allen `onclick="location.href='...'"` anpassen | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R212 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 555) | - Sitemap komplett neu pflegen | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R213 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 557) | Das ist aufwendig. **Default:** neue Nummer am Ende vergeben (z.B. 06_NeuesFenster), | MOVE | references/sitemap.md#Fenster nachträglich hinzufügen |  | | ✅ |
| R214 | SKILL.md#8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“) (Z. 563) | Wie in Kapitel 7 Schritt 5: tote Pfade auf das neue Fenster scannen und ersetzen, | REWRITE | references/sitemap.md#Fenster nachträglich hinzufügen | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R215 | SKILL.md#VERBOTEN (Z. 570) | - Farbwerte, Spacing-Werte, Token-Namen im Skill hardcoden | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R216 | SKILL.md#VERBOTEN (Z. 571) | - Mockup erstellen ohne Docs zu laden | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R217 | SKILL.md#VERBOTEN (Z. 572) | - Mockup auf Platte schreiben ohne User-Bestätigung im Chat | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R218 | SKILL.md#VERBOTEN (Z. 573) | - Mockup auf Platte schreiben ohne expliziten DC-Trigger vom User (Cowork) | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R219 | SKILL.md#VERBOTEN (Z. 574) | - NN-Nummer doppelt vergeben (BPM) | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R220 | SKILL.md#VERBOTEN (Z. 575) | - Umlaute oder Leerzeichen in Dateinamen oder Ordnernamen | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R221 | SKILL.md#VERBOTEN (Z. 576) | - Mockup im Visualizer anzeigen und direkt das Visualizer-HTML speichern | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R222 | SKILL.md#VERBOTEN (Z. 578) | - Branch automatisch annehmen (Branch-Policy des Skill-Profils, Shell fragen oder Auswahlfrage) | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R223 | SKILL.md#VERBOTEN (Z. 579) | - **Speichern ohne Token-Abgleich** gegen die Design-Quelle (Schritt 3b) oder mit Tokens, die es dort nicht gi | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R224 | SKILL.md#VERBOTEN (Z. 580) | - **Speichern ohne die Pflichtansichten des Profils** (Heidi: Desktop + 390 px) ohne Auswahlfrage | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R225 | SKILL.md#VERBOTEN (Z. 581) | - **Abnahme nur im Chat** – ohne Eintrag am Abnahme-Ort gilt das Mockup als nicht abgenommen (Schritt 4b) | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R226 | SKILL.md#VERBOTEN (Z. 582) | - **BPM-Ablage oder -Namensschema für ein anderes Projekt annehmen** – alles aus dem Mockup-Profil | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R227 | SKILL.md#VERBOTEN (Z. 583) | - **Externe Ressourcen im Mockup** (Web-Fonts, CDN), wenn das Projekt sie verbietet | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R228 | SKILL.md#VERBOTEN (Z. 584) | - Prosa-Fragen bei festen Entscheidungsoptionen (z.B. Archiv-vs-Überschreiben-Entscheidung) | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R229 | SKILL.md#VERBOTEN (Z. 585) | - **Mockup ohne Klick-Navigation auf interaktive Elemente speichern** (Profil „Sitemap: ja“) — alle Buttons/Ta | REWRITE | SKILL.md#VERBOTEN | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R230 | SKILL.md#VERBOTEN (Z. 586) | - **Sitemap-Update vergessen nach Mockup-Erstellung** (Profil „Sitemap: ja“) — `_SITEMAP.md` ist Single Source | REWRITE | SKILL.md#VERBOTEN | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R231 | SKILL.md#VERBOTEN (Z. 587) | - **Tote Pfade nicht prüfen vor Mockup-Erstellung** — `alert('Mockup folgt: X')` muss ersetzt werden wenn X je | KEEP | SKILL.md#VERBOTEN |  | | ✅ |
| R232 | SKILL.md#VERBOTEN (Z. 588) | - **Aufrufer-HTMLs nicht patchen** beim Anlegen eines neuen Fensters — Workflow Kapitel 7 Schritt 2 ist Pflich | REWRITE | SKILL.md#VERBOTEN | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| R233 | SKILL.md#VERBOTEN (Z. 589) | - **Pfade in onclick ohne Selbstcheck speichern** — Datei-Existenz und Sitemap-Konsistenz prüfen (Kapitel 6) | REWRITE | SKILL.md#VERBOTEN | Verweis auf Datei/Überschrift statt Kapitel-Nummer | | ✅ sinngemäß |
| N001 | – | Bei Profil „Sitemap: ja“ gelten zusätzlich die Regeln der Reference; vor jedem Mockup lesen, sonst nicht laden | NEW | SKILL.md#Sitemap und Klick-Navigation (Profil „Sitemap: ja“) | Verweis auf die neue Reference | | ✅ |
| N002 | – | Kopf und Inhaltsverzeichnis der Reference (Geltungsbereich, über 100 Zeilen) | NEW | references/sitemap.md#Inhalt | docs/skill-quality.md#Aufbau | | ✅ |

## DROP-Gruppen

Keine.

## Verweise von außen

Keine. Kein anderer Skill, `INDEX.md` oder die Doku verweist auf Kapitel von mockup-erstellen.

## Prüfung

- **Alt→Neu:** 233 Zeilen, alle mit Zustand (KEEP 109, MOVE 97, REWRITE 27, DROP 0); jeder KEEP- und MOVE-Kern ist am
  Neu-Ort zu finden.
- **Neu→Alt:** Zeilenvergleich alt gegen neu (`SKILL.md` + `references/sitemap.md`): Jede neue Zeile gehört zu einer
  REWRITE-Zeile (Verweis oder Überschrift) oder zu N001/N002.
- **Prüfskript:** läuft per CI nach dem Push (`validate-skills`).
- **Routing-Eval:** nach dem Commit, `--tag mockup-erstellen`.
