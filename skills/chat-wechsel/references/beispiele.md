# Beispielwerte BPM und Heidi

Werte aus zwei Projekten. Sie zeigen, wie die Felder aus `../SKILL.md#Voraussetzung: Skill-Profil` gefüllt werden; für
jedes Projekt gilt nur dessen eigenes Profil. „–“ heißt: im Skill nicht als Beispiel geführt.

## Inhalt

- Orte für den Sitzungsabschluss
- Startprompt
- ClickUp-Abgleich
- Regeln ohne Profil (BPM)
- Link-Prüfung

## Orte für den Sitzungsabschluss

| Wert | BPM | Heidi |
|------|-----|-------|
| Stand-Abschnitt | – | `docs/HANDOFF.md` Abschnitt 3e |
| Offene Punkte | – | `docs/HANDOFF.md` Abschnitt 4; Bauplan Abschnitt 10 |
| Statusliste | – | Bauplan Abschnitt 1 |
| Startprompt | – | Bauplan Abschnitt 0 |
| Versionsquelle | – | `package.json` der Karte |
| Ohne Profil | Memory `[CLICKUP]`, `INDEX.md` | – |

## Startprompt

Muster aus dem Heidi-Bauplan (Abschnitt 0), erste Zeile des Handover-Prompts:

```
> Lies CLAUDE.md, docs/HANDOFF.md (Abschnitt 3e + 4) und docs/dreame_x60/BAUPLAN.md. Nimm die nächste offene
> Aufgabe aus der Statusliste (Abschnitt 1): <DX-NNN | Kürzel | Schritt>. Prüfe Voraussetzungen, lies ihre Karte
> in Abschnitt 8 und arbeite nur diese Aufgabe ab (Skills: tracker start, code-erstellen nach Code-Profil).
> Regeln: Abschnitt 2. Widerspruch Code ↔ Bauplan → Befund in Abschnitt 10, Aufgabe blockiert, stoppen.
```

## ClickUp-Abgleich

- **Gruppierung:** BPM mehrere Listen → nach Liste (PlanManager, Docs, …); Heidi eine Liste → nach Status
  (in development, testing, backlog).
- **Status nach `tracker done`:** BPM `done`, Heidi `testing`.
- **Batch-Abschluss BPM:**

```
### ClickUp Tracker — Batch-Abschluss

**Im Chat erledigt — als Done markieren?**
- BPM-003 | DB-Anbindung Orchestrator        (Heidi: DX-031 | KARTE | 4.4 dx-planer …)
- BPM-007 | CS8629 Warning behoben
- BPM-012 | Token-Migration

**Im Chat neu erkannt — Task anlegen?**
- PlanManager — <neues Problem aus diesem Chat>
- Docs — <neuer Doc-Punkt>

**Weiterhin offen laut ClickUp:**
PlanManager (4):
- [high] [V1] BPM-004 | 5998er Statikplaene Erkennung
- [normal] [V1] BPM-008 | Mockup ManuellSortieren
...
Docs (1):
- [normal] [V1-Nice] BPM-015 | ADR-050 schreiben
```

- **Nächste Schritte:** BPM nach Meilenstein V1 und Priorität high/urgent zuerst.

## Regeln ohne Profil (BPM)

User committet und pusht selbst · Commit-Format [vX.Y.Z] Modul, Typ: Kurztitel · Docs Quickload-First-Pass →
Pflichtlesen → Langform · DOC-STANDARD.md · ClickUp Space "BPM Entwicklung" ist Source of Truth · Task-Nummern BPM-NNN

## Link-Prüfung

Typischer toter Verweis: `heidi-panel-v2.js`, das seit dem Umbau `dreame_x60.js` heißt.
