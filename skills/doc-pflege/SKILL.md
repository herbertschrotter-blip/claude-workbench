---
name: doc-pflege
description: >
  Schreibt, ändert und korrigiert Projektdokumentation nach dem Skill-Profil
  des Repos: legt neue Docs nach der Vorlage des Projekts an (z. B. ADR,
  Konzept, README, CHANGELOG, BACKLOG), aktualisiert
  Frontmatter, Quickload, Router-Einträge, Statuslisten und
  Übergabe-Dokumente, behebt kaputte Links, veraltete Kapitel und Befunde aus
  einem Audit und macht den Sitzungsabschluss im Repo. Use when users want to
  schreiben, erstellen, pflegen, aktualisieren, anlegen, formulieren,
  dokumentieren, ergänzen, korrigieren, umbauen, or refactoren documentation
  or concepts („Konzept für X“) —
  including bug fixes in docs (typos, broken links, outdated chapters),
  fixing audit findings, structural refactoring of existing docs, and the
  Sitzungsabschluss in the docs. Do not trigger for read-only checks
  or validation without changes (audit), code implementation, automatic
  post-change doc hints, mockup approvals (mockup-erstellen), ChatGPT review
  rounds (chatgpt-review), or generic
  project discussion without an explicit doc request.
---

# Doc-Pflege — Dokumentations-Skill

## Zweck

Schreibt, ändert und korrigiert Projektdokumentation, behebt Befunde aus einem Audit und macht
den Sitzungsabschluss im Repo; eine Prüfung ohne Änderungsauftrag macht audit. Welche Docs es gibt, wie sie
aufgebaut sind und was geprüft wird, steht im **Skill-Profil** des Projekts, Bereich Doku
(Abschnitt „Voraussetzung: Skill-Profil“). Initialisiert neue Projekte mit dem Standard-Doc-Set
des Profils. Erzwingt die Vorlagen des Profils bei neuen Docs.

Beispielwerte zweier Projekte (Vorlagen, Router, Orte, Pfade): `references/beispiele.md`. Für jedes Projekt gilt nur
sein eigenes Profil.

---

## Vorrang / Delegation an andere Skills

**doc-pflege ist für das Schreiben, Ändern, Korrigieren und Refactoren von
Projektdokumentation. Wenn die Hauptabsicht Code, Tasks, eine reine Prüfung
oder andere Aktionen sind, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (Services, ViewModels, Logik) | **code-erstellen** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| Commit-Befehl, Commit-Message, Version-Bump | **git-commit-helper** |
| ClickUp-Task anlegen, updaten, schließen | **tracker** |
| Prüfen oder validieren ohne Änderung (read-only): Konsistenz Code ↔ Docs, Frontmatter, Quickload, Router, Statuslisten | **audit** |

Nur wenn die Hauptabsicht **echte Doc-Arbeit** ist (neue Doc erstellen,
bestehende Doc refactoren, Frontmatter/Quickload ergänzen oder korrigieren, ADR schreiben,
Router-Einträge pflegen, Befunde aus einem Audit beheben, Sitzungsabschluss), bleibt doc-pflege zuständig.

**Wichtig:** Code-Änderungen, die "Doc-Folgen" haben (neues Schema,
neue ADR-würdige Entscheidung), werden von code-erstellen oder
git-commit-helper als **Doku-Hinweise** ausgegeben (Abschnitt
„Doku-Hinweise nach Code-Änderungen“). Diese Hinweise
sind KEIN Trigger für doc-pflege. Der User entscheidet explizit "pflege
jetzt die Doku" bevor doc-pflege selbst übernimmt.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen
  ist –, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Modus-Auswahl bei Unsicherheit | Modusnamen als Optionen: Projekt-Init, Router nachziehen, Begleit-Docs, Doku pflegen, Neue Doc oder Umbau, Sitzungsabschluss |
  | Befund beim Prüfen nach dem Schreiben mit mehreren Lösungen | Befund je Option: Doc anpassen, Quelle anpassen, Ignorieren mit Begründung |
  | Sitzungsabschluss: Aufgabe fertig oder offen? | fertig, offen (Rest bei den offenen Punkten), blockiert (Befund) |
  | Doc umbauen: Inhalt passt in kein Kapitel | Eigenes Kapitel am Ende, Vorhandenes Kapitel erweitern, Abbrechen |
  | Doku-Hinweis nach Code-Änderung | Jetzt pflegen, Später als Task anlegen, Ignorieren |
  | Schema-/DB-Änderung dokumentieren | "Mit Reset-Anweisung", "Mit Migrations-Kapitel (User will explizit)", "Abbrechen" |

  Prosa-Fragen nur, wenn:
  - Offene Frage ohne feste Optionen (z.B. Projektname, Modulname, Freitext-Beschreibung)
  - User hat Präferenz signalisiert
  - Freitext-Input nötig
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle muss dieser sein, sonst Auswahlfrage (wechseln /
  abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: ein
  in dieser Sitzung schon bekannter Branch; sonst mit Shell `git branch --show-current`; nennt ein älteres Profil der
  `CLAUDE.md` einen Pflicht-Branch und der aktuelle weicht ab → Auswahlfrage. Ohne Shell und unbekannt: die Branches über
  die GitHub-API auflisten und per Auswahlfrage wählen lassen (Optionen = Branch-Namen). NIE automatisch einen Branch
  annehmen.
- **Push** nach der Push-Policy im Skill-Profil (betrifft den Commit im Sitzungsabschluss):
  - `user-only`: kein Push; der User pusht selbst
  - `allowed`: Push nur, wenn der User es ausdrücklich will
  - `required-after-commit` oder `required-at-session-end`: Push nach dem Commit

  Ohne Push-Policy (kein Skill-Profil): Commit ja, Push nur nach Auswahlfrage (pushen / nicht pushen).

---

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Im Cowork-Chat: `references/cowork.md`, Abschnitt „Arbeitsverzeichnis“.

---

## Voraussetzung: Skill-Profil

Die Werte kommen aus dem Skill-Profil der `CLAUDE.md` im Repo (Spezifikation `docs/skill-profile-v1.md` im Skill-Repo;
im Cowork-Chat: `references/cowork.md`, Abschnitt „Skill-Profil und Docs lesen“):

| Feld | Wofür | Pflicht |
|------|-------|---------|
| Grundfelder (`Profil-Version`, `Projekt-ID`, `Repo`, `Branch-Policy`) | Repo und Branch (Grundsätze) | ja |
| `Doku.Router` | Wo steht, welche Doc wofür (Router nachziehen, Neue Doc) | ja |
| `Doku.Standard` | Regelwerk für Aufbau, Vorlagen je Doc-Typ, Ladereihenfolge | ja |
| `Doku.Entscheidungs-Ort` | Befunde und Entscheidungen (Sitzungsabschluss) | ja |
| `Commit.Push-Policy` | Push im Sitzungsabschluss | wenn der Sitzungsabschluss committet |
| `Doku.Pflichtdokumente` | Dateien mit Pfad (Doku pflegen, Begleit-Docs) | wo gesetzt |
| `Doku.Validierungsregeln` | Prüfen nach dem Schreiben | wo gesetzt |
| `Doku.Sitzungsabschluss` | Orte für Statusliste, Stand, offene Punkte; ob am Ende jeder Sitzung Pflicht | wo gesetzt |
| `Commit.Doku-Check` | Doku-Hinweise nach Code-Änderungen, Begleit-Docs | wo gesetzt |
| `Commit.Format`, `Commit.Module` | Doku-Commits | wo gesetzt |

1. **Skill-Profil v1** (Abschnitt `## Skill-Profil`). `none` ist gültig: der Teil entfällt. Fehlt ein Pflichtfeld oder
   steht es auf `fehlt`: genau dieses Feld nennen und nach `docs/skill-profile-v1.md`, Abschnitt „Fehlende Werte“, fragen.
2. **Rückfall:** Fehlt der Abschnitt, das ältere `## Doku-Profil` der `CLAUDE.md` mit den Feldern unten (die
   Doku-Checkliste steht dort im `## Commit-Profil`). Die Spalte „Skill-Profil“ nennt das Feld, das es dort ersetzt.

   | Feld | Skill-Profil | Bedeutung |
   |------|--------------|-----------|
   | Doc-Standard | `Doku.Standard` | Regelwerk für Aufbau und Validierung |
   | Router / Index | `Doku.Router` | Wo steht, welche Doc wofür |
   | Pflicht-Docs | `Doku.Pflichtdokumente` | Dateien mit Pfad (ersetzt die alte Pfadtabelle) |
   | Doc-Typen + Vorlagen | `Doku.Standard` | Was neu angelegt wird und wie |
   | Validierung | `Doku.Validierungsregeln` | Was nach dem Schreiben geprüft wird (Abschnitt „Prüfen nach dem Schreiben“) |
   | Frühphasen-Regel | – (Regel im Router oder Standard des Projekts) | Regeln für Schema-, Config- und Datenänderungen |
   | Advisory | `Commit.Doku-Check` | Doku-Folgen nach Code-Änderung |
   | Sitzungsabschluss | `Doku.Sitzungsabschluss` | Was am Ende jeder Sitzung zu tun ist |
   | Commit-Modul | `Commit.Module` | Modulname für Doku-Commits |

3. **Fehlt beides:** Router und Standard des Repos nehmen, soweit vorhanden (Beispiel: `references/beispiele.md`,
   Abschnitt „Rückfall ohne Profil (BPM)“). Was dann noch fehlt, per Auswahlfrage nach „Fehlende Werte“: Profil ergänzen
   (Vorschlag aus dem Repo) / Wert einmalig nennen / Abbrechen. Nie raten.

---

## Doc-Laderegel

Dieser Skill liest Docs nach der Ladereihenfolge des Standards bzw. Routers (`Doku.Standard`, `Doku.Router`).
Beispiele: `references/beispiele.md`, Abschnitt „Doc-Laderegel“.

---

## Projektregeln für Schema-, Config- und Datenänderungen

Führt der Router oder der Standard des Projekts eine Regel, wie Schema-, Config- oder Datenänderungen dokumentiert
werden, gilt sie für jede Doku solcher Änderungen. Zwei Arten kommen vor (Werte zweier Projekte:
`references/beispiele.md`, Abschnitt „Schema- und Datenänderungen“):

- **Frühphase: Reset statt Migration.** Solange das Projekt die Frühphase führt:
  **Statt Migrations-Kapitel → Reset-Anweisung dokumentieren.** Beschreibt eine Doc (z. B. Schema-Doc, ADR,
  Konzept-Doc) eine Schema-Änderung, NICHT als „Migration von Schema vN auf vN+1“ mit Änderungsschritten formulieren,
  sondern:

  > Schema-Änderung von N auf N+1 (Frühphase, keine Migration):
  > Betroffene Datei(en): <Datei>
  > Aktion: User löscht <Datei> → die App erstellt sie beim nächsten Start neu mit Schema vN+1.

  Gleiches gilt für Config-Dateien (z. B. JSON-Configs): betroffene Datei nennen, User löscht sie, App erstellt sie neu.

  **Ausnahme:** Wenn der User explizit "Migration dokumentieren" sagt oder die Regel im Projekt offiziell aufgehoben
  wurde.
- **Abweichung nur mit freigegebenem Eintrag.** Verlangt das Projekt für jede gewollte Abweichung von einem
  Referenzverhalten einen freigegebenen Eintrag (z. B. in einem Register am Entscheidungs-Ort), ist eine Abweichung ohne
  Eintrag ein Fehler.

---

## Doku-Hinweise nach Code-Änderungen

**Dieser Abschnitt ist KEIN Trigger und kein Modus.**
Er wird von anderen Skills nach einer Änderung als **Nachlauf-Checkliste** genutzt.
Der User-Intent für doc-pflege steht ausschließlich in der Frontmatter-Description.
Die hier beschriebene Checkliste wird passiv konsumiert (z.B. durch code-erstellen
oder git-commit-helper), sie aktiviert doc-pflege nicht selbst.

So wird sie genutzt:
- Hat code-erstellen Doku-Hinweise (DocMaintenanceHints) ausgegeben: sie übernehmen und als Hinweise ausgeben.
- Nach doc-relevanten Änderungen (Typische Fälle unten) eine kurze Merkliste im Format unten ausgeben – nicht bei
  trivialen Änderungen (NICHT triggern bei) und ohne den Arbeitsfluss zu unterbrechen.

### Quelle der Checkliste: `Commit.Doku-Check`

Die Nachlauf-Checkliste ist `Commit.Doku-Check` im Skill-Profil (im älteren `## Commit-Profil` die
Doku-Checkliste, gepflegt vom git-commit-helper). Dieser Skill führt keine
eigene Liste; er liest dieselbe. Beispiele: `references/beispiele.md`, Abschnitt „Doku-Hinweise“.

### Typische Fälle (Change-Class-basiert)

Die Nachlauf-Checkliste wird nach doc-relevanten Änderungen durchlaufen:
- Neue Tabelle / Schemaänderung / neue Entität
- Neue Architekturentscheidung / gewollte Abweichung von einer Projektregel
- Neuer Code-Entry-Point (neues Interface, neuer Service, neuer Dialog, neue Komponente)
- Neues Modul / neuer Workflow mit Benutzerwirkung
- Neue Abhängigkeit (NuGet, npm, Projektreferenz)
- Neues Doc / Doc-Refactor
- Bauschritt abgeschlossen (Statusliste, Aufgabenquelle)

### NICHT triggern bei:

- Lokale UI-Textfixes, Styling-Änderungen
- Kleine Refactors ohne Verhaltensänderung
- Umbenennungen ohne Strukturwirkung
- Reine Formatierungen
- Explorative Zwischenstände
- Bug-Fixes die keine Architektur berühren

### Format: Advisory (nicht interruptiv)

Statt voller Checkpoint-Checkliste → kurze Merkliste am Ende der Antwort:

```
📝 Doc-Hinweis: [<Doc> — <was sich geändert hat>]
```

Nur zutreffende Punkte. Keine Checkliste mit 10 leeren Punkten.
Der User entscheidet ob und wann die Doc-Pflege erfolgt.

---

## Modi

Werte zweier Projekte zu jedem Modus (Doc-Set, Router, Vorlagen, Orte): `references/beispiele.md`.

### Projekt-Init

**Wann:** "neues Projekt", "init projekt", kein Bereich Doku im Profil und kein Router vorhanden.

Kurzablauf:
1. Grundinfos sammeln (Projektname, Tech-Stack, Repo, DB?, Aufgabenquelle, Auslieferung)
2. Repo scannen
3. **Bereich Doku des Skill-Profils in der CLAUDE.md anlegen** (Felder oben). Fehlt das Skill-Profil ganz, richtet es
   projekt-anlegen ein (Abschnitt „Bestehendes Repo einrichten“); doc-pflege ergänzt danach den Bereich Doku
4. Standard-Doc-Set laut Profil generieren
5. Korrekte Vorlagen des Profils
6. Invarianten-Check
7. Paket dem User vorlegen

---

### Router nachziehen

**Wann:** Neues Doc, Doc umbenannt, neuer Code-Entry-Point.

Router aus `Doku.Router` laden und Eintrag nachziehen.

---

### Begleit-Docs

**Wann:** Neue Tabelle, Feature, Architekturentscheidung, Abhängigkeit, neue Entität.

`Commit.Doku-Check` → betroffene Pflicht-Docs ändern.

---

### Doku pflegen

**Wann:** "pflege die Doku", "aktualisiere alles", Doku-Fehler beheben (Tippfehler, kaputte Links, veraltete
Kapitel) oder Befunde aus einem Audit beheben.

Alle Pflicht-Docs (`Doku.Pflichtdokumente`) durchgehen und nachziehen, was nicht mehr stimmt; übergebene Audit-Befunde als
Aufgabenliste abarbeiten. Danach die geänderten Docs prüfen (Abschnitt „Prüfen nach dem Schreiben“).

**Mit Agenten (Claude Code):** Sind es viele Docs, sucht je Doc-Gruppe ein `work:erkunder` (Plugin `work`) parallel
die veralteten Stellen und meldet sie mit Datei, Stelle und Grund. Geschrieben wird nur in der Sitzung selbst, damit
die Doku aus einer Hand bleibt; jede gemeldete Stelle vor dem Ändern selbst nachlesen.

---

### Neue Doc oder Umbau

**Wann:** "neues Konzept für X", "erstelle Modul-Doc für Y",
"refactore <Doc> nach Standard", "docs umbauen",
oder wenn bei Projekt-Init oder Begleit-Docs ein neues Doc entsteht.

Danach die neue oder umgebaute Doc prüfen (Abschnitt „Prüfen nach dem Schreiben“).

#### Neue Doc

1. Vorlage für den Doc-Typ aus `Doku.Standard` laden
2. Router laden → verwandte Docs identifizieren
3. Kurzfassungen verwandter Docs (z. B. Quickload) lesen → Fachliche Invarianten sammeln
4. Doc nach der Vorlage des Standards erstellen (z. B. Frontmatter, Quickload, Kapitelstruktur)
5. Invarianten-Check durchführen – jede Antwort an den Ort, den der Standard dafür vorsieht:

```
📋 Invarianten-Check:
- Gibt es fachliche Regeln die bei JEDER Änderung gelten?
- Welche Kapitel müssen IMMER gelesen werden?
- Gibt es Abhängigkeiten zu anderen Modulen?
```

6. Router-Eintrag vorschlagen

#### Doc umbauen

1. Vorlage für den Doc-Typ aus dem Profil laden
2. Bestehende Doc komplett laden
3. Inhalt auf die Standard-Kapitel mappen
4. Pflichtteile der Vorlage (z. B. Frontmatter, Quickload) ergänzen oder aktualisieren
5. Invarianten-Check (siehe oben)
6. Vollständigkeits-Check gegen das Original; bei einer langen Doc in Claude Code zusätzlich ein `work:gutachter`, der
   Original und Umbau unabhängig abgleicht und fehlende Inhalte meldet

**REFACTORING-INVARIANTE (HARTE REGEL):**
- KEIN Inhalt darf gelöscht oder gekürzt werden — nur umordnen
- Inhalt der in kein Standard-Kapitel passt → eigenes Kapitel am Ende
- Nach dem Refactoring: Abschnitt-für-Abschnitt prüfen ob alles
  aus dem Original in der neuen Struktur vorhanden ist
- Im Zweifel lieber ein Kapitel zu viel als Inhalt verlieren

**VERBOTEN:** Beim Refactoring Inhalte weglassen, kürzen oder zusammenfassen.

---

### Sitzungsabschluss

**Wann:** "sitzung abschließen", "wir hören auf", "stand festhalten", nach dem letzten `tracker done`
einer Sitzung, oder wenn die Doku hinter `Doku.Sitzungsabschluss` ihn am Ende jeder Sitzung verlangt. Ersetzt nicht
chat-wechsel (Übergabeprompt für den nächsten Chat), sondern liefert ihm zu.

Ablauf (Orte aus `Doku.Sitzungsabschluss`; im älteren Doku-Profil Feld „Sitzungsabschluss“):
1. **Aufgabenquelle/Statusliste** nachziehen: jede in der Sitzung angefasste Aufgabe hat den richtigen
   Status (Statusliste ↔ Tracker; fertig / offen / blockiert per Auswahlfrage, wenn unklar)
2. **Befunde und Entscheidungen** eintragen, Entscheidungen in `Doku.Entscheidungs-Ort`
3. **Stand-Abschnitt** schreiben (Version, was gebaut, Stolpersteine; Datum)
4. **Offene Punkte** als Checkliste, erledigte abhaken, neue ergänzen, jede mit Tracker-Bezug oder Begründung,
   warum ohne
5. `Commit.Doku-Check` durchgehen (nichts vergessen)
6. Commit im `Commit.Format` mit dem Doku-Modul aus `Commit.Module`, Typ `Docs`, Kurztitel
   „Sitzungsabschluss <Datum> – <Kurztitel>“ (git-commit-helper); Push nach der Push-Policy (Grundsätze)
7. Kurzer Abschlussbericht im Chat: erledigt / offen / nächster Schritt – derselbe Text taugt als
   Einstieg für chat-wechsel

**VERBOTEN:** Sitzung beenden mit uncommitteten Doku-Änderungen; Statusliste „fertig“ ohne Tests und Commit;
offene Punkte nur im Chat statt im Doc.

---

## Prüfen nach dem Schreiben

Gilt nach Doku pflegen und nach Neue Doc oder Umbau – nur für die Docs, die dabei geändert oder angelegt wurden:
- Prüfregeln: Skill-Profil `Doku.Validierungsregeln` (im älteren Doku-Profil das Feld „Validierung“); bei `none`
  entfällt die Prüfung; führt das Projekt keine Regeln, die Prüflisten in `skills/audit/references/doku-validierung.md`.
- Befunde in der eigenen Änderung gleich beheben. Was eine Entscheidung braucht oder vor der Änderung schon so war, als
  Tabelle melden (Doc, Stelle, Befund, Vorschlag); bei mehreren Lösungen Auswahlfrage.
- Nichts stillschweigend korrigieren, was eine Entscheidung des Users ist (Status, Freigaben).

Eine Prüfung ohne Änderungsauftrag („prüfe frontmatter“, „quickload check“, „prüfe die doku“, „stimmt die statusliste“)
macht audit.

---

## Ausgabeformat

- Dateien direkt im Repo ändern; im Cowork-Chat: `references/cowork.md`, Abschnitt „Dateien ändern“
- Neue Docs komplett mit der Vorlage des Profils
- Commit: `Commit.Format` mit dem Doku-Modul aus `Commit.Module`, Typ `Docs` (Beispiele: `references/beispiele.md`,
  Abschnitt „Commit“)

---

## References

- `references/beispiele.md` – Werte zweier Projekte zu Profil, Pfaden, Ladereihenfolge, Schema-Regeln,
  Doku-Hinweisen, Modi, Sitzungsabschluss und Commit
- `references/cowork.md` – was im Cowork-Chat anders ist (Profil lesen, Arbeitsverzeichnis, Shell, Dateien ändern)

---

## VERBOTEN

- Frei inferieren welche Docs betroffen sind — Bereich Doku des Skill-Profils und `Commit.Doku-Check` lesen
- Docs ohne die Pflichtteile akzeptieren, die der Standard für ihren Bereich verlangt (z. B. Frontmatter)
- Neue Docs ohne die Vorlage des Profils erstellen
- Doku-Hinweise bei trivialen Änderungen ausgeben
- Doku-Hinweise als interruptive Checkliste statt kurzer Merkliste ausgeben
- Ladereihenfolge des Profils ignorieren
- Invarianten-Check bei neuen Docs überspringen
- Branch automatisch annehmen (Branch-Policy, Shell fragen oder Auswahlfrage)
- Prosa-Fragen bei festen Entscheidungsoptionen (z.B. Modus-Auswahl bei Unsicherheit)
- Eine Projektregel für Schema-, Config- oder Datenänderungen ohne Freigabe umgehen (z. B. Migrations-Kapitel statt
  Reset-Anweisung, Abweichung ohne freigegebenen Eintrag)
- Statusliste auf `fertig` setzen, solange Tests oder Commit fehlen
- Pfade oder Dateinamen eines anderen Projekts annehmen (auch aus `references/beispiele.md`) — alles aus dem Skill-Profil
- Sitzung ohne Sitzungsabschluss beenden, wenn Docs geändert wurden
- Docs von einem Agenten schreiben lassen oder seine Funde ungeprüft übernehmen (Abschnitt „Doku pflegen“, „Mit
  Agenten“)
