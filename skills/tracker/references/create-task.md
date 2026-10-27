# tracker neu — Task anlegen

Vollständiger Ablauf, Description-Template und Beispiel-Workflow für `tracker neu`.

**Abgrenzung:** Diese Datei behandelt den Standard-Fall `tracker neu` für
Haupttasks im Projekt-Scope (die Listen des Projekts laut Tracker-Config).
Für **Skill-Issues** (`tracker-NNN`, `cc-steuerung-NNN`, etc.) gilt das
Kommando `tracker issue <skill>: <titel>` und die separate Spec in
`references/issue-task.md` — mit eigenem Field-Scope und eigener
Nummerierungslogik.

Beispiele aus zwei Projekten: `beispiele.md`, Abschnitt „tracker neu“.

## Inhalt

- Kommando (Schnellmodus, Fragemodus)
- Ablauf
- Ablauf für Projekte ohne Zähler, Felder oder Anker (Ausnahme)
- Description-Template (Default bei tracker neu)
- Bei Unteraufgaben

---

## Kommando

`tracker neu: <Beschreibung>`

### Schnellmodus
Stehen Modul, Meilenstein, Priorität, Typ und Aufwand schon im Satz (Beispiel in `beispiele.md`)
→ Direkt anlegen.

### Fragemodus (Infos fehlen)

Per Auswahlfrage (nicht Prosa!). Gültige Werte für Modul-Auswahl
und Meilensteine stehen in der Tracker-Config
(Modul-Kürzel-Tabelle + Meilenstein-Tags). Konkrete Zielversion-Optionen
ergeben sich aus der Tracker-Config und dem aktuellen Release-Stand (Cowork-Chat: `cowork.md`).

Muster:
```
Frage 1 — Modul: <Module laut Tracker-Config>, Anderes
Frage 2 — Meilenstein: <Meilenstein-Tags laut Tracker-Config>
Frage 3 — Priorität: urgent, high, normal, low
```

Nach Basics fragen per Auswahlfrage:
```
Frage 1 — Typ: <Typ-Optionen laut Tracker-Config>
Frage 2 — Aufwand: <Aufwand-Optionen laut Tracker-Config>
Frage 3 — Zielversion: Aktuelle, Nächste Minor, später
```

Die konkreten Typ/Aufwand-Options sind projekt-spezifisch — siehe
Tracker-Config; ausgefüllte Fragen eines Projekts: `beispiele.md`.

Offensichtliches aus Kontext überspringen. Max 3 Fragen pro Aufruf.

**Projekte ohne Custom Fields** (die Tracker-Config sagt
„Keine“): Fragen nach Modul, Meilenstein, Typ, Aufwand und Zielversion entfallen.
Gefragt wird nur, was in Titel oder Beschreibung landet (Nummer eines Plan-Schritts, Ziel,
Akzeptanz). Priorität nur, wenn nicht `normal`.

**Prosa-Fragen für Freitext:**
- "Welche Komponente/Datei ist betroffen?" (falls Code-Bezug)
- "Welche Docs sind relevant?" (falls Doc-Bezug)

---

## Ablauf

1. Nächste freie Haupt-Nummer `<PRÄFIX>-<Next>` — Präfix und `Next` aus der Tracker-Config (Cowork-Chat: `cowork.md`)
2. Kürzel + Liste-ID aus der Tracker-Config (Abschnitt „Listen und Routing“)
3. Dedup: `clickup_search` → wenn Treffer, per Auswahlfrage fragen: Trotzdem neu, Bestehenden nutzen, Abbrechen. Bei ähnlichen Treffern zusätzlich Review-Workflow-Check gemäß `references/review-workflow.md` — besprochene Änderungen könnten bestehende Tasks im Scope verschieben.
4. **Description**: Template aus Abschnitt "Description-Template" unten generieren
5. **TEMP-Anker prüfen** (nur Cowork-Chat, `cowork.md` Abschnitt „[ANKER-LIVE] im Ablauf“):
   gibt es einen offenen TEMP-Anker zum Thema dieses Tasks? → TEMP-ID merken; sonst kein TEMP
   (Task ohne vorherige Ausarbeitungsphase)
6. `clickup_create_task(list_id, name, priority, tags, markdown_description)` → Task-ID erhalten
7. **Pro-Task-Quittung im Chat schreiben** (direkt nach `clickup_create_task`):
   ```
   ✅ <PRÄFIX>-NNN oder Issue-ID — [<PRÄFIX>-ANCHOR-<task-id>] — erstellt: <kurzbeschreibung>
   ```
   Die Quittung ist Bestätigung + Body-Anker + Audit-Zeile in einem Format.
   Bei TEMP-Brücke: ` (war TEMP-<id>)` anhängen.
   **Bei ≥2 Tasks in einer Antwort:** Vollständiges Batch-Protokoll greift — siehe `references/batch-protocol.md` (Batch-Ansage, Pro-Task-Zyklus, Batch-Audit).
8. **Custom Fields nachträglich setzen** via `clickup_update_task`. Beispiel-Struktur:
   ```
   custom_fields = [
     {"id": "<Typ-Field-ID>",         "value": "<Typ-Option-ID>"},
     {"id": "<Aufwand-Field-ID>",     "value": "<Aufwand-Option-ID>"},
     {"id": "<Zielversion-Field-ID>", "value": "<Version>"},
     {"id": "<Komponente-Field-ID>",  "value": "<Datei/Modul>"},
     {"id": "<Docs-Field-ID>",        "value": "<Doc-Pfad>"},
     {"id": "<Chat-Anker-erstellt-ID>", "value": "[<PRÄFIX>-ANCHOR-<task-id>] ..."},
     // Falls TEMP existierte:
     {"id": "<Chat-Anker-temp-ID>",   "value": "TEMP-<id>"}
   ]
   ```
   Konkrete Field-IDs und Option-IDs: Tracker-Config.
9. **`[ANKER-LIVE]` aktualisieren** (nur Cowork-Chat, `cowork.md` Abschnitt „[ANKER-LIVE] im Ablauf“)
10. `Next` +1 in der Tracker-Config, Änderung mit committen (Cowork-Chat: `cowork.md`)
11. Bestätigung an User inkl. Task-ID als Anker-Referenz

### Ablauf für Projekte ohne Zähler, Felder oder Anker (Ausnahme)

Gilt nur, wenn die Tracker-Config ausdrücklich „kein Zähler“
oder „Chat-Anker: nicht verwendet“ sagt bzw. bei den Feldern „Keine“. Standard
ist das volle Schema (Präfix, Felder, Anker).

1. Nummer = Nummer aus dem Kontext (z.B. Nummer eines Plan-Schritts) — nichts
   hochzählen, kein Zähler-Eintrag
2. Liste = die eine Liste aus der Tracker-Config
3. Dedup wie oben im Ablauf
4. Beschreibung nach `clickup-fields.md` Abschnitt „Beschreibung ohne Felder“
   (statt Description-Template unten)
5. `clickup_create_task(list_id, name, priority, status, markdown_description)`
6. Quittung: `✅ <Titel> — erstellt — <ClickUp-Link>` (kein Anker)
7. Aus dem Ablauf oben entfallen TEMP-Anker, Custom Fields, `[ANKER-LIVE]` und `Next` +1

---

## Description-Template (Default bei tracker neu)

Neue Tasks bekommen automatisch dieses Markdown-Template als Description:

```markdown
## Problem
<Was ist kaputt / was fehlt / was muss besser werden?>

## Lösungsansatz
<Wie lösen wir das konkret? Falls noch unklar: "Offen">

## Acceptance Criteria
- [ ] <Kriterium 1>
- [ ] <Kriterium 2>

## Definition of Done
- [ ] Code implementiert
- [ ] Manuell getestet
- [ ] Dokumentation aktualisiert
- [ ] Commit gemacht

## Abhängigkeiten / Related
<Falls ClickUp-Dependencies gesetzt: hier noch mal Freitext-Notizen>
<Oder Verweise auf Docs: <Doc-Pfad>>

## Technische Notizen
<Beliebige weitere Infos, Code-Snippets, Links, Hintergrund>
```

**Regeln:**
- Für **Meta-Tasks** (ClickUp-Pflege, Skill-Updates) das Template **verkürzen**:
  nur Problem + Lösungsansatz
- Für **Mockup-Tasks**: AC ersetzen durch konkrete Screen-Bereiche
- Für **Konzept-Tasks**: DoD nur "Konzept-Doc geschrieben + im Router des Projekts (`Doku.Router`) verlinkt"
- Template auch bei `tracker done` prüfen: DoD-Checkliste abhaken

### Bei Unteraufgaben

Unteraufgaben bekommen ein **verkürztes Template**:

```markdown
## Aufgabe
<Was genau in diesem Schritt?>

## Definition of Done
- [ ] <konkret>
```

Kein Problem/Lösungsansatz (das steht im Parent).
