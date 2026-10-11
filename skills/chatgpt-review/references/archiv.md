# CGR-Ablagesystem

Ablauf des Review-Archivs im Detail; Kernregeln in `../SKILL.md#CGR-Ablagesystem`.

## Inhalt

- ID-Schema
- Themen-Enum (aus dem Review-Profil)
- Ablagestruktur pro Serie
- Globaler Index
- Serie starten (vor Phase 1)
- Rundenstand aus dem Archiv (Pflicht vor jeder Runde)
- Runde starten (innerhalb laufender Serie)
- Lifecycle pro Runde (4 Datei-Checkpoints)
- Serie abschließen
- Retroaktive Nutzung


Jede Review-Runde wird im Repo unter der **Review-Ablage des Profils** archiviert
(BPM: `Docs/Referenz/chatgpt-reviews/`; Heidi: `docs/chatgpt-reviews/`). Schreiben: Cowork via DC,
Claude Code via Write/Bash – die Struktur ist dieselbe. Die Archivierung läuft **inkrementell** — pro Runde 4 Dateien,
angelegt in der jeweiligen Gesprächsphase.

## ID-Schema

```
CGR-<YYYY-MM-DD>-<thema>-r<runde>
```

- `YYYY-MM-DD` = Vollständiges Startdatum der Serie (Tag der ersten Runde)
- `<thema>` = kebab-case aus Themen-Enum
- `r<runde>` = Rundennummer (r1, r2, r3, ...)

## Themen-Enum (aus dem Review-Profil)

Beispiele (BPM, Heidi): [`beispiele.md`](beispiele.md#themen).

- **Neues Thema** — Auswahlfrage mit Option "neues Thema", dann
  Namensvorschlag per Prosa-Frage, danach Themenliste im Review-Profil **und** in der
  `INDEX.md` der Review-Ablage erweitern

## Ablagestruktur pro Serie

```
<Repo>/<Review-Ablage>/
└── CGR-YYYY-MM-DD-<thema>/
    ├── README.md          ← Serie-Übersicht, Runden-Zusammenfassung
    ├── r1/
    │   ├── 01-claude-prompt.md       ← Claudes Prompt an ChatGPT
    │   ├── 02-chatgpt-response.md    ← ChatGPTs Antwort im Canvas
    │   ├── 03-claude-analysis.md     ← Claudes Einschätzung/Reaktion
    │   └── 04-user-decisions.md      ← Herberts Antworten + Entscheidungen
    ├── r2/ ...
    └── r3/ ...
```

## Globaler Index

```
<Repo>/<Review-Ablage>/INDEX.md
```

Pro Serie eine Zeile in der Tabelle "Aktueller Stand". Bei neuer Runde:
Status-Update. Bei Serie-Abschluss: Kernergebnis eintragen.

## Serie starten (vor Phase 1)

Wenn der User eine neue Review-Serie startet, VOR Phase 1 Initialprompt:

1. **Thema ermitteln** via Auswahlfrage (Optionen = Themen aus dem Review-Profil + "neues Thema"):
   ```
   Frage: "Thema der Review-Serie?"
   Optionen (Beispiel BPM): "skillsystem", "docs-refactor", "bpm-architektur",
             "datenschutz-dbschema", "neues Thema"
   ```
   Bei "neues Thema": Prosa-Frage nach Kurzname (kebab-case).

2. **CGR-ID festziehen:** `CGR-<aktuelles-YYYY-MM-DD>-<thema>`
   (aktuelles Datum nehmen, nicht fragen)

3. **Repo-Pfad ermitteln:**
   - Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`)
   - Cowork: Memory `[PROJECT]`-Eintrag (enthält Repo-Pfad); falls nicht vorhanden: Prosa-Frage

4. **Ordner anlegen** (Cowork DC `create_directory`, Claude Code Bash `mkdir -p`):
   ```
   <Repo>/<Review-Ablage>/CGR-YYYY-MM-DD-<thema>/
   ```

5. **README.md Stub** (Cowork DC, Claude Code Write):
   ```markdown
   # CGR-YYYY-MM-DD-<thema> — <Serie-Titel>

   **Thema:** <Beschreibung>
   **Zeitraum:** <YYYY-MM-DD>
   **Branch:** <Branch>
   **Weg:** codex | kopieren
   **Codex-Thread:** <thread_id, nur Weg codex>
   **Ursprungs-Chat:** <optional, nur Cowork>
   **Status:** Runde 1 offen

   ---

   ## Runden-Übersicht

   ### Runde 1 — <Titel>
   - **Artefakte:** [r1/](./r1/)
   - **Fokus:** ...
   - **Kernergebnis:** ...
   ```

6. **INDEX.md erweitern** (Cowork DC `edit_block`, Claude Code Edit):
   ```
   <Repo>/<Review-Ablage>/INDEX.md → neue Zeile in Tabelle "Aktueller Stand"
   ```

## Rundenstand aus dem Archiv (Pflicht vor jeder Runde)

Rundennummer und Status werden **aus dem Archiv gelesen, nicht aus dem Chat gezählt**:

1. `README.md` der Serie lesen (Status-Zeile, Runden-Übersicht)
2. Vorhandene `r<N>/`-Ordner listen (Claude Code: Glob; Cowork: DC `list_directory`) und je Ordner prüfen,
   welche der vier Dateien existieren
3. Daraus folgt: letzte Runde = höchstes N; ist `r<N>/04-user-decisions.md` vorhanden → nächste Runde ist N+1;
   fehlt in r<N> eine Datei → diese Runde ist offen, dort weitermachen
4. Widerspricht der Chat dem Archiv (z.B. „Runde 3 erstellen“, aber r3 existiert schon mit 01) →
   Auswahlfrage „Archiv gilt / Chat gilt / Abbrechen“

## Runde starten (innerhalb laufender Serie)

Wenn innerhalb einer bestehenden Serie eine neue Runde beginnt:

1. **r<N>/-Ordner anlegen** (Cowork DC `create_directory`, Claude Code Bash `mkdir -p`):
   ```
   <Repo>/<Review-Ablage>/CGR-YYYY-MM-DD-<thema>/r<N>/
   ```

2. **4 Platzhalter-Dateien** erst bei Befüllung anlegen — nicht vorab
   alle 4 leer anlegen. Lifecycle siehe unten.

## Lifecycle pro Runde (4 Datei-Checkpoints)

| Phase | Aktion | Datei |
|-------|--------|-------|
| Phase 1 Initialprompt erstellt | `01-claude-prompt.md` schreiben (DC / Write) | r<N>/01-claude-prompt.md |
| ChatGPT-Antwort liegt vor (codex: Aufruf fertig; kopieren: User pastet) | `02-chatgpt-response.md` schreiben (codex: schreibt Codex mit `-o`; sonst DC / Write) | r<N>/02-chatgpt-response.md |
| Phase 2 Stufe A Claude-Analyse | `03-claude-analysis.md` schreiben (DC / Write) | r<N>/03-claude-analysis.md |
| User-Entscheidungen nach Stufe A | `04-user-decisions.md` schreiben (DC / Write) | r<N>/04-user-decisions.md |

**Regel:** Jede Datei wird direkt in der zugehörigen Gesprächsphase
angelegt — nicht gesammelt am Rundenende. So bleibt das Archiv auch bei
Chat-Abbruch lückenlos.

## Serie abschließen

Wenn User signalisiert "Serie fertig" / "keine weitere Runde":

1. **README.md finalisieren:**
   - Kernergebnisse pro Runde
   - Links zu resultierenden ADRs / Bauplan-Notizen / Commits
   - Status: "Abgeschlossen"
2. **INDEX.md Status-Update:** Status-Spalte auf "Abgeschlossen",
   Kernergebnis-Spalte befüllen.
3. **Ergebnisse übernehmen** (Auswahlfrage, siehe `../SKILL.md#Phase 3: Abschluss`): Entscheidungen an den Ergebnis-Ort des Profils,
   offene Punkte als Tasks über den tracker-Skill (Präfix des Projekts).
4. Commit der Archivdateien: `[vX.Y.Z] <Doku-Modul>, Docs: CGR-<id> Runde <N> / Abschluss`
   (Claude Code committet selbst; Cowork liefert den Befehl)

## Retroaktive Nutzung

Der Skill verwaltet auch bestehende Serien-Ordner:
- Neue Runde in bestehender Serie: regulärer "Runde starten"-Ablauf
- Historische Runden nachrüsten: on-demand, kein Pflicht-Workflow
