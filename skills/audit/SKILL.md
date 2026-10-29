---
name: audit
description: >
  Prüft read-only, ob Code, Projektdoku und Skills zueinander passen, nach dem
  Skill-Profil des Repos: Doku gegen Code, Doku-Validierung (z. B. Frontmatter,
  Quickload, Router, Statuslisten), Aufgaben im Tracker gegen die
  Aufgabenquelle, Grundsatzregeln eines Stacks, im Skill-Repo die Skills gegen
  INDEX und Qualitätsregeln; ändert selbst nichts. Use when users want to
  prüfen, checken, auditieren, or validieren without changes — a consistency
  audit, a documentation-vs-code check, a Frontmatter or Quickload
  validation, a check of a project against its ground rules (Grundsatzregeln,
  e.g. Home Assistant), a check whether an index or router file matches the
  descriptions of the skills, modules or docs it lists, or a systematic
  read-only review of project rules. Do not trigger for writing documentation
  or fixing findings (doc-pflege), code implementation (code-erstellen), build
  debugging, or general code review of a function or diff without doc
  comparison.
---

# Audit-Skill — Projekt-Konsistenz-Prüfung

## Zweck

Prüft read-only, ob Code, Projektdoku, Aufgaben im Tracker und – im Skill-Repo – die Skills
zueinander passen. **Was** geprüft wird, steht im **Skill-Profil** des Repos (Abschnitt
„Voraussetzung: Skill-Profil“), dazu die Stack-Referenzen von code-erstellen
(`references/stacks/<key>.md`) für die Code-Seite. Im Skill-Repo kommen `docs/skill-quality.md`
und die Skill-Tabelle der `INDEX.md` dazu (Abschnitt „Modul 8 — Skills (im Skill-Repo)“). audit
erfindet keine Prüfregeln; es ist der Read-only-Läufer über diese Regeln. Eigene Prüflisten führt
es nur für die Doku-Validierung von Projekten ohne solche Regeln im Profil
(`references/doku-validierung.md`). Wie das in zwei Projekten aussieht, zeigt
[references/beispiele.md](references/beispiele.md).

---

## Vorrang / Delegation an andere Skills

**audit ist strikt read-only. Wenn die Hauptabsicht ein Fix, eine
Implementierung oder eine Doc-Pflege ist, NICHT hier weiterarbeiten,
sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (Fix, Feature, Refactor) | **code-erstellen** |
| Doku schreiben oder Befunde beheben, ADR, Konzept, Frontmatter-Pflege | **doc-pflege** |
| Skill ändern (auch Skill-Befunde beheben) | **skill-pflege** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| Commit-Befehl, Commit-Message | **git-commit-helper** |
| Aktion an einer Aufgabe im Tracker | **tracker** |

Nur wenn die Hauptabsicht **read-only Konsistenzprüfung** ist
(Audit-Report, Frontmatter-Check, Code-vs-Doc-Abgleich, INDEX-Validierung,
Skill-Prüfung im Skill-Repo), bleibt audit zuständig.

**Wichtig:** Nach einem Audit-Report bietet audit KEINE Fixes selbst an.
Die im Report empfohlenen Aktionen werden per Auswahlfrage an
den passenden Skill delegiert (code-erstellen für Code-Fixes, doc-pflege
für Doc-Fixes, skill-pflege für Skill-Befunde) oder als Aufgaben über
**tracker** angelegt (Abschnitt
„Nach dem Report“). audit ist der Analyse-Skill, nicht der Fix-Skill.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen
  ist –, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Modus-Auswahl (A oder B) | Vollaudit, Teilaudit, Abbrechen |
  | Teilaudit: welches Modul | Modul-Namen aus dem Router des Profils (`Doku.Router`; Beispiele in `references/beispiele.md`, Abschnitt „Teilaudit: Modulnamen“); „nur Grundsatz“, wenn das Profil Grundsatzregeln nennt |
  | Vollaudit-Warnung vor Start | Starten, Als Teilaudit starten, Abbrechen |
  | Nach dem Report: was mit den Befunden | Als Aufgaben anlegen (tracker), An code-erstellen/doc-pflege/skill-pflege, Nur Report |

  Prosa nur bei einer offenen Frage ohne feste Optionen oder wenn der Nutzer eine Präferenz signalisiert hat.
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle Branch muss dieser sein, sonst Auswahlfrage
  (auf dem aktuellen Branch prüfen / abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: Branch aus Chat-Kontext verwenden; mit Shell
  `git branch --show-current` (Shell im Cowork-Chat: `references/cowork.md`); ohne Shell und unbekannt: Auswahlfrage
  mit den Branch-Namen aus `git branch -a`. NIE automatisch einen Branch annehmen.

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Cowork-Chat: [references/cowork.md](references/cowork.md), Abschnitt „Arbeitsverzeichnis“.

---

## Voraussetzung: Skill-Profil (Pflicht vor jedem Audit)

Die Werte kommen aus dem Skill-Profil der `CLAUDE.md` im Repo (Spezifikation `docs/skill-profile-v1.md` im Skill-Repo).
Pflicht für audit sind die Grundfelder, `Doku.Router` und `Doku.Validierungsregeln`; die übrigen Felder, wenn das Modul
läuft, das sie braucht.

| Feld | Wofür |
|------|-------|
| Grundfelder (`Profil-Version`, `Projekt-ID`, `Repo`, `Branch-Policy`) | Pflicht; Branch (Grundsätze), Profil-Prüfung im Router-Selbst-Check |
| `Doku.Router` | Pflicht; Router-Selbst-Check, Modulnamen für das Teilaudit |
| `Doku.Validierungsregeln` | Pflicht; formale Doc-Prüfung (`none` → das Modul entfällt) |
| `Doku.Standard` | Doc-Laderegel, Format des Routers |
| `Doku.Pflichtdokumente` | Kern-Docs und Begleit-Docs |
| `Doku.Entscheidungs-Ort` | Notiz-Vorschläge nach dem Report |
| `Code.Architekturregeln` | Pflicht, wenn Code geprüft wird |
| `Code.Stacks` | Stack-Referenzen; Reference für die Grundsatzregeln |
| `Code.Aufgabenquelle` | Kern-Docs vs. Code, Aufgabenquelle ↔ Tracker |
| `Code.Tests` | Testergebnis beim Vollaudit (Tool-Strategie) |
| `Tracker.Config` | Pflicht, wenn der Tracker geprüft wird; Präfix und Statusmodell |
| Check `skill-validation` unter `### Checks` | im Skill-Repo die Mechanik der Skill-Prüfung |
| `Modul.Grundsatzregeln` | Verweis auf das Regelwerk; `none` → „Modul 7 — Grundsatzregeln“ entfällt |
| `Modul.Manifest` | Pfad oder Muster der Modul-Manifeste |
| `Modul.Prüfumfang` | Positivliste der lesbaren Bereiche |
| `Modul.Nachweise` | optional: Zuordnung Check/Testfall → Teilnachweis |

1. **Skill-Profil v1** (Abschnitt `## Skill-Profil`). `none` ist gültig: der Prüfpunkt oder das Modul entfällt.
2. **Rückfall:** die älteren Abschnitte `## Doku-Profil` (Feld „Validierung“, Pflicht-Docs, Router) und `## Code-Profil`
   (Schichten/Kopplung, Aufgabenquelle, Stacks, Tests) der CLAUDE.md.
3. **Fehlt beides:** was das Repo selbst nennt (Router, Standard-Doc, Tests), als Vorschlag sammeln und mit dem nächsten
   Punkt vorlegen; nie ohne Rückfrage übernehmen. Wie das bei einem Projekt aussieht: `references/beispiele.md`, Abschnitt
   „Rückfall ohne Profil“.
4. **Was dann noch fehlt** oder auf `fehlt` steht: genau dieses Feld melden und nach `docs/skill-profile-v1.md`,
   Abschnitt „Fehlende Werte“, fragen (Profil ergänzen / Wert einmalig nennen / abbrechen); fehlt das Profil ganz, mit
   einem Vorschlag aus dem Repo. Das Profil ergänzt nicht audit, sondern doc-pflege (Projekt-Init) oder der Nutzer. Nie
   raten.

Stack-Referenzen: `skills/code-erstellen/references/stacks/<key>.md` für jeden Schlüssel in `Code.Stacks` bzw. `Stacks:`.

Ein Verweis, der nicht auflöst, ist ein Befund; ein fehlender benötigter Wert wird erfragt, nie geraten. Beim Teilaudit
„nur Grundsatz“ werden Doku- und Tracker-Werte nicht verlangt.

## Fall → Reference

| Fall | Reference |
|------|-----------|
| Beispielwerte zweier Projekte: Modulnamen, Rückfall ohne Profil, Ladefolge, Prüfpunkte je Modul, Notiz-Ort, Suchmuster | [references/beispiele.md](references/beispiele.md) |
| Prüflisten der Doku-Validierung für Projekte ohne eigene Regeln | [references/doku-validierung.md](references/doku-validierung.md) |
| Prüfverfahren der Grundsatzregeln je Stack | Tabelle im Abschnitt „Modul 7 — Grundsatzregeln“ |
| Cowork-Chat: Arbeitsverzeichnis, Dateien auflisten und suchen, Shell | [references/cowork.md](references/cowork.md) |

## Doc-Laderegel

Ladereihenfolge des Projekts aus `Doku.Standard`; ohne eigene Regel diese Grundfolge:
1. Router (`Doku.Router`) → welche Docs gelten
2. Kopf bzw. Kurzfassung der Docs → filtern
3. Langform nur für die geprüften Stellen

Beispiele zweier Projekte: `references/beispiele.md`, Abschnitt „Doc-Laderegel“.

---

## 2 Modi

### Modus A — Vollaudit
Alle 8 Module („Modul 7 — Grundsatzregeln“ nur, wenn das Profil Grundsatzregeln nennt; „Modul 8 — Skills (im
Skill-Repo)“ nur im Skill-Repo). Token-intensiv — vor
Start per Auswahlfrage bestätigen lassen.

### Modus B — Teilaudit
Nur relevantes Modul.

---

## Ablauf

### Profil und Router laden (Abschnitt „Voraussetzung: Skill-Profil“)
### Prüfmodule – je Modul die neutrale Frage und die Prüfpunkte aus dem Profil (Beispiele zweier Projekte: `references/beispiele.md`, Abschnitt „Prüfpunkte je Modul“)

---

### Modul 1 — Router-Selbst-Check

Neutral: Zeigt der Router des Profils nur auf Dinge, die es gibt, und im richtigen Format?

- Jedes Ziel des Routers (`Doku.Router`) existiert: Docs, Code-Einstiege, genannte Pfade, Werkzeuge und Ordner.
- Das Format des Routers folgt `Doku.Standard`.
- Das Skill-Profil nach `docs/skill-profile-v1.md`, Abschnitt „Prüfung“: Version gültig; Bereiche vollständig, die die
  genutzten Skills brauchen; Dateien und Überschriften hinter `ref:` vorhanden; Profil und Prosa der CLAUDE.md
  widerspruchsfrei; keine unbekannten Felder oder veralteten Pfade.

---

### Modul 2 — Kern-Docs vs. Code (vorwärts)

Neutral: Stimmt das, was die Kern-Docs versprechen, im Code?

- Was `Doku.Pflichtdokumente` und `Code.Architekturregeln` zusagen (Schema, Schichten, Verträge, verbotene Muster),
  findet sich im Code.
- Was die Aufgabenquelle (`Code.Aufgabenquelle`) als fertig führt, hat Code, Tests und einen Commit; Offenes hat keinen
  Code, der schon behauptet, fertig zu sein.

---

### Modul 3 — Code vs. Docs (rückwärts)

Neutral: Gibt es im Code etwas, das die Docs nicht kennen?

- Bestandteile im Code (Komponenten, Dienste, Schnittstellen, Registrierungen, Einstiegspunkte), die keine Doku nennt.
- Abhängigkeiten im Code, die die Doku nicht nennt.

---

### Modul 4 — Referenz-Docs

Neutral: Sind die Begleit-Docs aktuell und vollständig?

- Begleit-Docs aus `Doku.Pflichtdokumente` (z. B. CHANGELOG, ADRs, Backlog, Übergabe) und der Entscheidungs-Ort
  (`Doku.Entscheidungs-Ort`) sind aktuell und vollständig.
- Versionsangaben in Doku und Code stimmen überein.

---

### Modul 5 — Aufgabenquelle ↔ Tracker

Neutral: Sagen Aufgabenquelle und Tracker dasselbe?

- Status in der Aufgabenquelle (`Code.Aufgabenquelle`) ↔ Status im Tracker nach dem Statusmodell der Tracker-Config
  (`Tracker.Config`): Abweichung ⚠️, fehlende Aufgabe ❌.
- Jede Aufgabe der Aufgabenquelle hat eine im Tracker und umgekehrt.

(Tracker lesen über den tracker-Skill, read-only, geschlossene Aufgaben eingeschlossen.)

---

### Modul 6 — Formale Doc-Prüfung nach Profil

Neutral: Halten die Docs die Validierungsregeln des Projekts ein?

- Die Prüfregeln stehen in `Doku.Validierungsregeln` des Skill-Profils (ohne Skill-Profil: Feld „Validierung“ des
  Doku-Profils).
- `none`: Das Projekt führt bewusst keine Doku-Validierung; Modul 6 entfällt.
- Ohne Skill-Profil und ohne Feld „Validierung“ gelten die Prüflisten in
  [references/doku-validierung.md](references/doku-validierung.md): je Projekt Stufe A (Blocker) und Stufe B (Warnung).
- Passt keine dieser Listen zum Projekt: `Doku.Validierungsregeln` nach „Fehlende Werte“ erfragen; keine fremde Liste
  anwenden.
- Im Skill-Repo zeigt das Feld auf die Skill-Prüfung; die läuft nur einmal, in „Modul 8 — Skills (im Skill-Repo)“.

---

### Modul 7 — Grundsatzregeln

Neutral: Hält das Projekt die Grundsatzregeln ein, auf die `Modul.Grundsatzregeln` zeigt?

- Läuft nur, wenn das Profil Grundsatzregeln nennt. Die Regeln liest audit zur Laufzeit aus dem Regelwerk; es führt
  keine eigenen.
- Je Modul-Manifest (aus `Modul.Manifest`) ein eigener Block mit Ausbaustufe (deklariert oder abgeleitet) und einer
  Zeile je anwendbarer Regel; Regeln über der Stufe gesammelt als „nicht anwendbar“.
- Ergebnisse und Belege nach dem Ergebnisvertrag (Abschnitt unten).
- Wie die Regeln je Plattform nachgewiesen werden, steht in einer Reference je Stack-Schlüssel aus `Code.Stacks`. Für
  einen Stack ohne Reference meldet audit „Prüfverfahren fehlt“ und rät keines.

| Stack | Reference |
|---|---|
| `home-assistant` | [`references/grundsatz/home-assistant.md`](references/grundsatz/home-assistant.md) |

---

### Modul 8 — Skills (im Skill-Repo)

Neutral: Passen die Skills zu INDEX und Qualitätsregeln?

Nur im Skill-Repo (Repo mit `skills/<name>/SKILL.md` und `docs/skill-quality.md`); sonst entfällt das Modul.

- **Mechanik:** Check `skill-validation` des Skill-Profils, mit JSON-Bericht in eine Datei außerhalb des Repos (audit
  schreibt nichts ins Repo). Fehler → ❌, Warnungen → ⚠️. Läuft der Check auf dieser Maschine nicht, gilt das Ergebnis
  der automatischen Prüfung zum aktuellen Stand; fehlt auch das, ist die Mechanik „Nachweis offen“.
- **Urteil** nach `docs/skill-quality.md`, Abschnitt „Urteil – audit“: Description zu breit oder zu eng, Kollisionen
  mit anderen Skills, Neutralität, inhaltliche Doppelungen, Schnitt Kern/References, Eval-Fälle realistisch.
- **INDEX ↔ Descriptions:** Skill-Tabelle der `INDEX.md` gegen die Descriptions – jeder Ordner unter `skills/` hat eine
  Zeile und umgekehrt; Zuständigkeit und Auslöser der Zeile decken sich mit der Description.
- **Befunde** → skill-pflege bzw. `tracker issue <skill>` (Abschnitt „Nach dem Report“).

---

## Report-Format

Befunde immer mit Datei und Stelle (Zeile oder Abschnitt), damit der Fix-Skill direkt hinspringen kann.

```
🔍 Audit-Report [Projekt] ([Datum]) — Modus A/B, Skill-Profil ✓ (oder Rückfall: <Quelle>) Stacks: <keys>
═══════════════════════════════════

📊 Zusammenfassung: X ✅ | Y ⚠️ | Z ❌

─── Modul 1–5 ───

──────────────────────────────────
Modul 7 — Grundsatzregeln · <Modul> (Stufe <n>, deklariert|abgeleitet)
──────────────────────────────────
G-15 | Nachweis offen
  Statisch: Entladepfad vorhanden — <Datei>:<Zeile>
  Test vorhanden: Einrichten → Entladen → Neu laden — <Testdatei>:<Zeile>
  Ausführung: offen (kein Lauf zum aktuellen Stand)
G-18 | ❌ Token in <Datei>:<Zeile> (Wert nicht zitiert)
Nicht anwendbar (Stufe): G-22

──────────────────────────────────
Modul 6 — Formale Doc-Prüfung
──────────────────────────────────
❌ [Doc]: [Problem]
⚠️ [Doc]: [Warnung]
✅ [Doc]: OK

═══════════════════════════════════
📝 Empfohlene Aktionen:
═══════════════════════════════════
1. ❌ [Aktion]
2. ⚠️ [Aktion]
```

---

## Ampel

| ✅ | Konsistent | — |
| ⚠️ | Inkonsistenz | Sollte korrigiert werden |
| ❌ | Fehler | Muss korrigiert werden |

---

## Ergebnisvertrag

Gilt für jede Prüfung gegen ein Regelwerk („Modul 7 — Grundsatzregeln“) und für jedes Projekt; die Reference des Stacks nutzt ihn.

**Anwendbarkeit:** Eine Regel gilt, wenn ihre Mindeststufe erreicht und ihr Gegenstand vorhanden ist. Fehlt ein
vorgeschriebener Bestandteil, ist das ein Befund, kein Grund für „nicht anwendbar“.

**Nachweisarten** (je Regel nur die nötigen, getrennt bewertet):
- **statisch:** Code oder Vertrag gelesen; Suchtreffer im Kontext geprüft
- **Test vorhanden:** Testinhalt und Assertions decken den Prüffall ab
- **Ausführung:** der zugeordnete Test lief erfolgreich, das Ergebnis gehört zum geprüften Stand aller Eingaben
- **Urteil:** begründete Bewertung anhand benannter Belege

| Ergebnis | Bedeutung |
|---|---|
| ✅ | alle nötigen Teilnachweise erfüllt, kein belegter Verstoß |
| ⚠️ | belegte Inkonsistenz ohne nachgewiesenen Pflichtverstoß |
| ❌ | konkreter Verstoß gegen eine anwendbare Pflicht nachgewiesen |
| Nachweis offen | ein nötiger Nachweis fehlt, ist veraltet oder ungeprüft; kein belegter Verstoß |
| nicht anwendbar | Stufe oder Gegenstand trifft nachweislich nicht zu |

Rangfolge je Regel: ❌ vor ⚠️ vor „Nachweis offen“ vor ✅; offene Teilnachweise bleiben auch neben ❌ sichtbar. Ein
ungeklärter Suchtreffer ist „Nachweis offen“. Verlangt die Regel einen Test und fehlt er nach Suche im Testbereich: ❌;
ein passender Test ohne gültigen Lauf: „Ausführung offen“.

**Pflichtbelege:** Regel, Modul, Stufe mit Herkunft, Bestandteil, Teilnachweis, Datei und Zeile bzw. Abschnitt,
Begründung; bei Ausführung die Zuordnung Check/Test und der Bezug zum Stand; bei Fehlendem der erwartete Pfad und der
durchsuchte Bereich. Geheime Werte werden nie zitiert.

**Budget:** Ist das Budget erschöpft (Abschnitt „Tool-Strategie“), endet die Prüfung mit „Teilprüfung – Nachweise
offen“: geprüfte Bereiche, offene Regeln, nächster nötiger Nachweis. Nicht gelesene Bereiche bekommen nie ✅.

---

## Nach dem Report: Befunde weitergeben

audit ändert nichts – aber es lässt die Befunde nicht im Chat liegen. Direkt nach dem Report
eine Auswahlfrage:

- **„Als Aufgaben anlegen“** → `tracker neu` (Schema und Präfix aus der Tracker-Config des Projekts; Beispiel in
  `references/beispiele.md`, Abschnitt „Nach dem Report“).
  Eine Sammel-Aufgabe pro Modul mit den Befunden als Checkliste in der Beschreibung; ❌-Befunde mit
  Priorität `high`, ⚠️ `normal`. Bei ≤ 3 Befunden auch je Befund eine Aufgabe (Auswahlfrage).
  Alle ClickUp-Operationen über den tracker-Skill, nie direkt.
  Skill-Befunde („Modul 8 — Skills (im Skill-Repo)“) stattdessen als `tracker issue <skill>: Audit: …`, je Skill ein
  Issue mit den Befunden als Checkliste.
- **„An code-erstellen / doc-pflege / skill-pflege“** → Befunde als Aufgabenliste an den Fix-Skill
  übergeben (Code-Befunde → code-erstellen, Doc-Befunde → doc-pflege, Abschnitt „Doku pflegen“,
  Skill-Befunde → skill-pflege); der Fix-Skill startet erst nach eigener Bestätigung.
- **„Nur Report“** → Report bleibt; Hinweis, dass Befunde ohne Aufgabe beim nächsten Audit wieder auftauchen.

Befunde, die eine Entscheidung des Nutzers brauchen (Regel-Widerspruch, Abweichung von einer
Vorgabe), zusätzlich als Notiz-Vorschlag für den Entscheidungs-Ort des Projekts
(`Doku.Entscheidungs-Ort`) formulieren, Entscheidung offen – eintragen tut doc-pflege, nicht audit.
Beispiel: `references/beispiele.md`, Abschnitt „Nach dem Report“.

---

## Tool-Strategie

- Docs gezielt lesen: Kopf bzw. Kurzfassung, nur die geprüften Abschnitte (Beispiele: `references/beispiele.md`,
  Abschnitt „Tool-Strategie“)
- Existenz: Dateien auflisten
- Inhalt: suchen, Muster aus den Prüfpunkten des Moduls (Beispiele: `references/beispiele.md`, Abschnitt „Tool-Strategie“)
- Im Cowork-Chat: `references/cowork.md`, Abschnitt „Dateien auflisten und suchen“
- Tracker („Modul 5 — Aufgabenquelle ↔ Tracker“): read-only über tracker, geschlossene Aufgaben eingeschlossen
- Teilaudit: max 10 Tool-Calls (Suchläufe zählen je einer)
- Teilaudit „nur Grundsatz“ („Modul 7 — Grundsatzregeln“): max 30 Tool-Calls je Modul-Manifest; Suchen mehrerer Regeln in
  einem Lauf bündeln
- Vollaudit: max 35 Tool-Calls; das Ergebnis der Tests (`Code.Tests`) vorher vom Nutzer erfragen statt selbst zu bauen
  (read-only)

### Arbeit aufteilen (Claude Code)

Ein Vollaudit oder ein Teilaudit über mehrere Module liest viel, und die Module hängen nicht voneinander ab. In Claude
Code gibt die Sitzung das Lesen deshalb an Agenten des Plugins `work`: je Modul (bei großen Modulen je Bereich) ein
`work:erkunder` mit klarem Auftrag – Modul, Prüfpunkte aus dem Profil, Prüfumfang, erwartete Rückgabe als Befunde mit
Datei und Stelle. Die Agenten laufen parallel; die Grenzen oben gelten für die Sitzung, jeder Agent bekommt seine
eigenen Prüfpunkte. Bewerten, Ampel, Report und Weitergabe macht die Sitzung selbst: Sie prüft jeden gemeldeten Befund
an der genannten Stelle nach, bevor er in den Report kommt. Ein Teilaudit mit einem Modul läuft ohne Agenten. Im
Cowork-Chat gibt es keine Agenten.

---

## VERBOTEN

- Dateien ändern (read-only)
- Annahmen ohne Dateien
- False Positives als Fehler
- Vollaudit ohne Auswahlfrage-Vorwarnung
- Ladereihenfolge des Profils ignorieren
- Prosa-Fragen bei festen Entscheidungsoptionen (Modus-Auswahl, Modul-Auswahl für Teilaudit)
- Branch automatisch annehmen (Branch-Policy lesen, Shell fragen oder Auswahlfrage)
- Eigene Prüfregeln erfinden statt Skill-Profil (bzw. Doku-/Code-Profil), Stack-Referenzen und
  `references/doku-validierung.md` zu lesen
- Prüfpunkte oder Beispielwerte eines anderen Projekts (`references/beispiele.md`, `references/doku-validierung.md`)
  auf ein Projekt anwenden, das sie laut Profil nicht hat
- Befunde ohne Datei und Stelle melden
- Report beenden ohne Auswahlfrage „Aufgaben / Fix-Skill / Nur Report“
- ClickUp direkt schreiben (Aufgaben nur über tracker, und nur nach Auswahlfrage)
- **Eine Regel grün melden, weil ein Test existiert** – „Test vorhanden“ ist kein Ausführungsnachweis
- **Geheime Werte im Report zitieren** oder gesperrte Bereiche öffnen, um darin zu suchen
- **Außerhalb des Prüfumfangs lesen** (`Modul.Prüfumfang`), wo das Profil ihn begrenzt
- **Befunde eines Agenten ungeprüft in den Report übernehmen** oder einem Agenten Schreibrechte geben (Abschnitt
  „Arbeit aufteilen (Claude Code)“)
