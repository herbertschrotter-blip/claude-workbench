# CGR-2026-10-12-ha-grundsatz — audit prüft gegen die HA-Grundsatzregeln

**Thema:** `ha-grundsatz` – HA-Grundsatz Phase 2 (ClickUp 123ztrd1027): Wie prüft der Skill `audit` ein HA-Projekt
gegen die Regeln G-01 … G-22 aus `docs/ha-grundsatz/`?
**Zeitraum:** 2026-10-12
**Branch:** `main`
**Weg:** codex
**Codex-Thread:** 01a12d0a-f548-71d0-805b-d14fbe904ebf
**Websuche:** live
**Status:** Abgeschlossen (12.10.2026)
**Ergebnis:** Konzept für audit Modul 7 „Grundsatzregeln“; Umsetzung in vier Schritten (siehe unten)

---

## Runden-Übersicht

### Runde 1 — Konzept: Ort im Skill, Prüfbarkeit je Regel, Stufen, Report
- **Artefakte:** [r1/](./r1/)
- **Fokus:** wo die Prüfung in audit lebt, was je Regel statisch prüfbar ist, Erkennung der Ausbaustufe, Report
- **Kernergebnis:** Modul 7 in audit plus HA-Reference; mehrere Nachweise je Regel (Fundstelle, Test, Ausführung,
  Urteil), „Test vorhanden“ färbt nicht grün; Kandidat → Kontext; belegte Mindeststufe, Vertrag hat Vorrang; Budget 10
  mit „Teilprüfung – Nachweise offen“; begrenztes `/config`-Audit

### Runde 2 — Ergebnisvertrag, Manifest-Pflichtfelder, Prüftabelle
- **Artefakte:** [r2/](./r2/)
- **Fokus:** Ergebnisvertrag, Pflichtfelder von `module.yaml`, Grün-Speicher von `checks.py`, Prüftabelle G-01 … G-22
- **Kernergebnis:** fünf Ergebnisse mit Rangfolge ❌ > ⚠️ > „Nachweis offen“ > ✅ (+ „nicht anwendbar“); Pflichtfeld-
  Tabelle; Eigentum unter `owns` implizit `module.id`; Befund: Grün-Speicher hasht nur geänderte Dateien

### Runde 3 — Check-Format, Schema-Details, Gesamtbild
- **Artefakte:** [r3/](./r3/)
- **Fokus:** Auswahl- und Eingabemuster je Check, Nachweis-Datensatz, `critical_for`, Typen und Bestandteile, Umbauplan
- **Kernergebnis:** `[auswahl: …] [eingaben: …]` (Parser zuerst); Datensatz in `.git/skill-checks.json`; Profilfelder
  `Modul.Nachweise`, `Modul.Prüfumfang`; `components`, `ui.types`, `critical_for` mit `entities:`/`actions:`/
  `settings:`; Ergebnisvertrag im neutralen Kern von audit

## Ergebnisse

1. Doku: `docs/ha-grundsatz/module-yaml.md`, `docs/skill-profile-v1.md`
2. audit (skill-pflege): Ergebnisvertrag im Kern, Modul 7, Reference `references/grundsatz/home-assistant.md`
3. `checks.py` (git-commit-helper): neues Check-Format und Nachweis-Datensatz – eigene ClickUp-Aufgabe
4. chatgpt-review: Antwort als Zitat, Statuszeile
