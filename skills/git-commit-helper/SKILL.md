---
name: git-commit-helper
description: >
  Erstellt fertige Git-Commit-Befehle und Commit-Messages im einheitlichen Format
  [vX.Y.Z] Modul, Typ: Kurztitel – projektneutral, Versionsquelle und
  Doku-Checkliste kommen aus dem Skill-Profil (CLAUDE.md des Repos). Use when
  users want to commit changes, need a git commit command, ask for a commit
  message, or want the correct version bump for an existing change (including
  PATCH/MINOR/MAJOR decisions or semver questions). Do not trigger for code
  creation, code review, git push, or general Zustimmung wie "ok" oder "passt".
---

# Git Commit Helper

---

## Vorrang / Delegation an andere Skills

**git-commit-helper ist für Commit-Befehle, Commit-Messages und Version-Bumps.
Wenn die Hauptabsicht Code-Änderungen oder andere Aktionen sind, NICHT hier
weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (Services, ViewModels, Dialoge, Logik) | **code-erstellen** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| ClickUp-Task anlegen, updaten, schließen | **tracker** |
| Doku schreiben (ADR, Konzept, Frontmatter, Quickload) | **doc-pflege** |
| Konsistenzprüfung Code ↔ Docs | **audit** |

Nur wenn die Hauptabsicht **die Commit-Erstellung selbst** ist
(Commit-Message formulieren, Version-Bump wählen, git add/commit-Befehle),
bleibt git-commit-helper zuständig.

**Wichtig:** Nach Code-Änderungen liefert code-erstellen einen
Commit-Vorschlag INLINE (`skills/code-erstellen/SKILL.md`, Abschnitt „Commit und Doku-Hinweise“). Das ist kein
git-commit-helper-Trigger. Dieser Skill springt erst an wenn der User
explizit "commit", "commit-message", "welche Version" o.ä. fragt ODER
wenn code-erstellen an ihn delegiert hat.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung**, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:
  - Typ unklar: Feature, Fix, Change, Refactor, Perf, Docs
  - Version-Bump unklar: MAJOR (Breaking), MINOR (Feature), PATCH (Fix)
  - ein benötigter Wert fehlt im Skill-Profil (Abschnitt „Voraussetzung: Skill-Profil“)

  Prosa nur bei einer offenen Frage ohne feste Optionen (z.B. Kurztitel) oder wenn der Nutzer eine Präferenz
  signalisiert hat.
- **Branch** nach der Branch-Policy des Skill-Profils: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle Branch muss dieser sein, sonst Auswahlfrage
  (wechseln / abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Profil: ein in der Sitzung schon bekannter Branch, sonst die Shell; ohne Shell per
  Auswahlfrage fragen. NIE automatisch einen Branch annehmen.
- **Push** nach der Push-Policy des Skill-Profils:
  - `user-only`: kein `git push` in der Sequenz; der Nutzer pusht selbst
  - `allowed`: `git push` nur, wenn der Nutzer es ausdrücklich will
  - `required-after-commit`: `git push origin <branch>` als Glied der Sequenz
  - `required-at-session-end`: kein Push in der Sequenz; gepusht wird am Ende der Sitzung

  Ohne Push-Policy (kein Skill-Profil): `git push origin <branch>` bleibt als Glied in der Sequenz.

## Voraussetzung: Skill-Profil

Alles Projektspezifische steht im Repo, nicht im Skill: im Skill-Profil der `CLAUDE.md` (`docs/skill-profile-v1.md` im
Skill-Repo). Claude liest es, bevor Version, Doku oder Commit-Sequenz angefasst werden.

| Feld | Wofür |
|------|-------|
| `Commit.Format` | Format der ersten Zeile (Abschnitt „Commit-Format (Standard)“) |
| `Commit.Module` | Modul-Namen |
| `Commit.Versionsquelle` | aktuelle Version und die Datei, die hochgezählt wird |
| `Commit.Versionsregel` | wann und wie die Nummer steigt; überschreibt die Zuordnung unter „Typen“ |
| `Commit.Push-Policy`, `Branch-Policy` | Push und Branch (Grundsätze) |
| `Commit.Pre-Commit-Checks`, `### Checks` | Prüfläufe vor dem Commit |
| `Commit.Doku-Check` | Doku-Check vor dem Commit |

Quellen in dieser Reihenfolge:

1. **Skill-Profil v1** (Abschnitt `## Skill-Profil`). Eine andere `Profil-Version` als 1: nicht weiterarbeiten.
2. **Rückfall:** der ältere Abschnitt `## Commit-Profil` der CLAUDE.md. Modul-Namen entsprechen `Module`, Bump-Regel
   `Versionsregel`, Doku-Checkliste `Doku-Check`; die Versionsquelle heißt gleich (Muster:
   `references/beispiele.md#Älteres Commit-Profil`).
3. **Fehlt ein Wert:** nur dieses Feld melden und per Auswahlfrage klären: *Profil ergänzen* / *Wert einmalig nennen* /
   *Abbrechen* (Regel „Fehlende Werte“ in `docs/skill-profile-v1.md`). Fehlt das Profil ganz: das Repo selbst
   durchsuchen – `docs/`-Ordner, `*.md` in der Wurzel und in `docs/`, bekannte Versionsdateien
   (Directory.Build.props, package.json, pom.xml, pyproject.toml, *.csproj) – und das Gefundene als Vorschlag für einen
   Abschnitt `## Skill-Profil` zeigen. Angelegt wird er erst, wenn der Nutzer zustimmt.

`none` ist gültig: der Teil entfällt, ohne Rückfrage.

- `Commit.Format: none` → Commit ohne Versions- und Modulteil (Abschnitt „Commit-Format (Standard)“)
- `Commit.Module: none` → kein Modul in der ersten Zeile
- `Commit.Versionsquelle: none` → kein Versionsteil, keine Versionsdatei
- `Commit.Pre-Commit-Checks: none` → keine Prüfläufe vor dem Commit
- `Commit.Doku-Check: none` → kein Doku-Check

Steht in `Commit.Versionsregel` oder `Commit.Doku-Check` ein `ref:<pfad>#<überschrift>`, gilt der Abschnitt, auf den es
zeigt; Claude liest ihn vor dem Commit.

Das Profil wird nie aus dem Gedächtnis angenommen. Einmal gelesen, gilt es
für die Session.

## Commit-Format (Standard)

```
[vX.Y.Z] Modul, Typ: Kurztitel
```

Das Format ist der Standard für alle Projekte. Was sich je Projekt ändert (`Commit.Format`, `Commit.Module`,
`Commit.Versionsquelle`, `Commit.Versionsregel`, `Commit.Doku-Check`), steht im Skill-Profil (Abschnitt
„Voraussetzung: Skill-Profil“). Für `Commit.Format` gilt:

- gleich dem Standard → das Format oben
- ein anderes Format → dieses
- `none` → Commit ohne Versions- und Modulteil, also `Typ: Kurztitel`

Wenn das Projekt eine Aufgaben- oder Ticket-Nummer führt (z. B. Aufgaben-ID aus dem
Tracker; Beispiele: `references/beispiele.md#Aufgabennummer im Kurztitel`), gehört sie an den Anfang des Kurztitels
oder in die zweite Zeile der Message – nie vor das `[vX.Y.Z]`.

**Modul:** ein Name aus `Commit.Module`. Berührt eine
Änderung mehrere Module, gilt das Hauptmodul (wo die Absicht liegt); die
übrigen werden im Kurztitel genannt. Sind die Teile unabhängig, werden es
zwei Commits.

**Zweite Zeile (optional):** nach einer Leerzeile ein bis drei Sätze mit
Begründung, Befund oder Verweis (Ticket, Doku-Abschnitt). Nie Prosa in
die erste Zeile packen.

### Typen
- Feature → MINOR
- Fix → PATCH
- Change → PATCH/MINOR
- Refactor → PATCH
- Perf → PATCH
- Docs → PATCH
- Test → PATCH
- Chore (Werkzeuge, Konfiguration, Abhängigkeiten) → PATCH

Diese Zuordnung ist der Standard. `Commit.Versionsregel` darf sie überschreiben (Beispiele:
`references/beispiele.md#Versionsregel`).

Version aus der Versionsquelle des Skill-Profils ermitteln (z.B.
Directory.Build.props bei WPF, package.json bei Node/TypeScript, pom.xml
bei Java, INDEX.md wo das Projekt sie dort führt; bei `changelog:<Datei>` die
Nummer des obersten Eintrags).

## Ablauf

Die Schritte laufen in dieser Reihenfolge.

### Arbeitsverzeichnis (PFLICHT)

Arbeitsverzeichnis = Repo-Wurzel, ermittelt mit
`git rev-parse --show-toplevel` in der Shell, die gerade zur Verfügung steht
(im Cowork-Chat: `references/cowork.md#Shell im Cowork-Chat`).
Bei Worktrees gilt die Wurzel des Worktrees. Claude ermittelt es immer selbst, ohne zu fragen.

### Git-Status

```
git status --short
```

in der Shell der Umgebung ausführen. Kein Commit ohne vorherigen Status.

### Versionsdatei hochzählen (PFLICHT bei Version-Bump)

Die neue Version steht nicht nur in der Commit-Message: Die Versionsquelle
aus dem Skill-Profil (z.B. Directory.Build.props, package.json samt
package-lock.json, pom.xml; bei `changelog:<Datei>` ein neuer oberster Eintrag) wird auf die neue Nummer gesetzt und
gehört mit in denselben Commit. Ohne Änderung der Versionsdatei kein `[vX.Y.Z]` mit
neuer Nummer. Die neue Nummer folgt aus dem Typ und `Commit.Versionsregel`. Bei `Commit.Versionsquelle: none` entfällt
dieser Schritt.

### Doku-Check vor dem Commit (PFLICHT)

Der Doku-Check kommt aus `Commit.Doku-Check` (im älteren Commit-Profil `Doku-Checkliste:` je Datei eine Zeile „Datei →
wann“). Er wird vor der Commit-Sequenz abgearbeitet, damit Code, Version und Doku in einem Commit landen; jede
betroffene Datei wird genannt, geändert und im selben Commit mitgenommen.

Fehlt der Wert im Profil (anders als `none`): `docs/` und `*.md` im Repo auflisten und per
Auswahlfrage klären, welche Dateien bei dieser Änderung dran sind; das
Ergebnis als Vorschlag für `Commit.Doku-Check` ins Profil übernehmen (Regel „Fehlende Werte“).

Beispiel-Checklisten zweier Projekte: `references/beispiele.md#Doku-Check`.

### Commit-Befehle (One-Block-Regel)

**KERNREGEL:** Eine komplette Commit-Sequenz wird IMMER in EINEM Code-Block
geliefert. Niemals aufgeteilt in mehrere Blöcke für `cd` / `add` / `commit`
/ `push`. Der User soll mit einem Klick kopieren und in eine Shell einfügen
können. Führt Claude die Befehle selbst aus (Claude Code), gilt dieselbe
Sequenz als ein Aufruf.

Das Glied `git push origin <branch>` steht nur in der Sequenz, wenn die Push-Policy es verlangt oder erlaubt
(Grundsätze); sonst entfällt es. Die Vorlage richtet sich nach der Shell, in der die Sequenz läuft.

#### PowerShell (Windows)

Trenner: `;` (Semikolon)

```powershell
cd "[Arbeitsverzeichnis]" ; git add <spezifische-dateien> ; git commit -m "[vX.Y.Z] Modul, Typ: Kurztitel" ; git push origin <branch> ; git log -1 --format="%h %s"
```

#### Bash (Linux/macOS, WSL, Git Bash)

Trenner: `&&` (nur weitermachen wenn vorheriger Befehl OK)

```bash
cd "[Arbeitsverzeichnis]" && git add <spezifische-dateien> && git commit -m "[vX.Y.Z] Modul, Typ: Kurztitel" && git push origin <branch> && git log -1 --format="%h %s"
```

#### Regeln für die Sequenz

- Spezifische Pfade nach `git add`, nicht `git add .`
- Ein Commit pro logische Änderung
- `"` für Commit-Messages (Windows-kompatibel)
- `git log -1 --format="%h %s"` am Ende, damit der Nutzer den Commit-Hash sofort sieht
- Bei Renames: `git mv` als zusätzliches Glied vor `git add`
- Branch-Name nach den Grundsätzen einsetzen (nie hartkodiert "main" annehmen)
- Pre-Commit-Checks des Skill-Profils, die für die geänderten Dateien gelten (Pfad-Muster des Checks), laufen vor dem
  Commit (Abschnitt „Prüfläufe vor dem Commit“); ohne Skill-Profil der Testbefehl, den das Projekt vor dem Commit
  verlangt (CLAUDE.md). Bei rotem Ergebnis kein Commit

#### Prüfläufe vor dem Commit

Die Checks laufen auf der Maschine, nicht im Modell; ihre Laufzeit ist Wartezeit für den Nutzer.

**Claude Code:** Die Regeln unten setzt das Skript `scripts/checks.py` dieses Skills um:
`python3 <Skill-Ordner>/scripts/checks.py --vor-commit` (unter Windows je nach Installation `python`). Es liest das
Skill-Profil, wählt die passenden Checks, lässt sie gleichzeitig laufen (`(allein)` im Profil für sich), merkt sich
grüne Läufe und gibt die Tabelle aus. Exit 0 grün; 1 rot; 2 ein Befehl fehlt auf diesem Rechner (dann sagen, wo der
Check läuft, z. B. per CI); 3 Profil oder git nicht lesbar. Die Tabelle des Skripts wird unverändert gemeldet; bei Rot
die Ausgabe aus der Log-Datei lesen. Läuft das Skript nicht (kein Python), gelten die Regeln von Hand.

- **Nur passende Checks:** Ein Check aus `Pre-Commit-Checks` läuft nur, wenn mindestens eine geänderte Datei zu
  einem seiner Pfad-Muster passt (gestaged, ungestaged und neu, laut `git status --short`). Ein Check ohne
  Pfad-Muster läuft immer. Jeden übersprungenen Check ausdrücklich melden: `übersprungen: <check> – keine passende
  Datei`.
- **Auswahl und Eingaben:** Pfad-Muster sind die Auswahl (`[auswahl: …]` oder eine Klammer ohne Schlüssel);
  `[eingaben: …]` nennt alle Dateien, die das Ergebnis bestimmen, und löst den Check ebenfalls aus. Mit Eingaben
  gilt „schon grün“ nur, solange keine dieser Dateien sich geändert hat, auch eine eingecheckte nicht; je grünem Lauf
  legt das Skript einen Datensatz im Git-Ordner ab, den audit als Ausführungsnachweis liest
  (`docs/skill-profile-v1.md`, Abschnitt „Checks“). Fehlerhafte Angaben im Profil: kein Check läuft, Exit 3.
  Einen Nachweis für einen Stand ohne offene Änderung erzeugt `--checks <name> --immer`.
- **Gleichzeitig oder nacheinander:** Unabhängige Checks gleichzeitig starten, wenn sie sich nicht um Kerne, Dateien,
  Ports oder Datenbanken streiten. Zwei Läufe, die beide alle Kerne nutzen oder dieselbe Test-Datenbank schreiben,
  laufen nacheinander, die schnellen zuerst, damit ein rotes Ergebnis früh kommt.
- **Lange Checks** (über etwa eine Minute) im Hintergrund starten, Ausgabe in eine Datei. Danach das Ergebnis
  vollständig lesen (Zusammenfassung, Fehler, Warnungen), nicht nur die letzte Zeile oder den Exit-Code.
- **Meldung** als Tabelle, übersprungene Checks eingeschlossen:

  | Check | Dauer | Ergebnis |
  |---|---|---|
  | unit | 0:42 | grün |
  | integration | – | übersprungen – keine passende Datei |

- **Claude Code** führt die Checks vor der Commit-Sequenz aus; die Sequenz folgt erst, wenn alle gelaufenen Checks
  grün sind. Im Cowork-Chat: `references/cowork.md#Prüfläufe im Cowork-Chat`.

#### Wenn ein Glied der Sequenz fehlschlägt

Rotes Testergebnis, abgelehnter Push, Hook-Fehler oder Konflikt: Sequenz
bricht am fehlerhaften Glied ab (dafür `&&` bzw. Prüfung des Exit-Codes).
Ursache in einem Satz nennen, nichts überspringen, keinen Teil-Commit
„trotzdem“ pushen. Erst wenn die Ursache behoben ist, die ganze Sequenz
erneut liefern.

#### Mehrzeilig nur wenn User explizit darum bittet

Wenn der Nutzer eine besser lesbare, mehrzeilige Variante will, in EINEM Block
mit Backtick-Continuation (PowerShell) oder Backslash (Bash) liefern — nie
in mehrere Code-Blöcke aufteilen.

## Regeln

- Pfade in der Schreibweise der jeweiligen Shell (PowerShell: Backslash; Bash: Slash)
- Keine Erklärungen
- Bei mehreren Commits in einer Antwort: je Commit ein eigener Block (One-Block-Regel gilt je Commit)

## Fall → Reference

| Fall | Reference |
|------|-----------|
| Beispielwerte: älteres Commit-Profil, Aufgabennummer, Versionsregel, Doku-Checklisten, Commit ohne Format | [references/beispiele.md](references/beispiele.md) |
| Cowork-Chat: Shell, Sequenz zum Kopieren, Prüfläufe | [references/cowork.md](references/cowork.md) |

## VERBOTEN

- Branch automatisch annehmen – ohne Branch-Policy, Shell oder Auswahlfrage
- Pushen gegen die Push-Policy des Skill-Profils
- Prosa-Fragen bei festen Entscheidungsoptionen (Typ, Version-Bump, fehlender Profilwert)
- **Mehrere Code-Blöcke für eine Commit-Sequenz** — alles muss in EINEM Block stehen, semikolon- oder `&&`-getrennt (Abschnitt „Commit-Befehle (One-Block-Regel)“)
- **Erklärungen zwischen den Befehlen** die das Kopieren stören — Erklärungen kommen vor oder nach dem Block, nie hinein
- **Versionsquelle oder Doku-Dateien raten** — beides kommt aus dem Skill-Profil oder aus der Suche im Repo, nie aus dem Gedächtnis
- **Werkzeugnamen fest verdrahten** (Frage- oder Shell-Werkzeug einer bestimmten Umgebung) — der Skill beschreibt die Handlung, Claude wählt das Werkzeug der Umgebung
- **Checks ohne passende Datei ausführen oder übersprungene Checks verschweigen** (Abschnitt „Prüfläufe vor dem Commit“)
