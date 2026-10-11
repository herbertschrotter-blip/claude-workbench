# CGR-2026-10-11-skillsystem — chatgpt-review über die Codex CLI

**Thema:** `skillsystem` – Umbau von chatgpt-review auf den Weg codex (v0.53.0): Claude führt die Review-Runden selbst
über die Codex CLI; zugleich Abnahme des neuen Wegs (zwei Runden ohne Kopieren, Archiv vollständig).
**Zeitraum:** 2026-10-11
**Branch:** `main`
**Weg:** codex
**Codex-Thread:** 01a12cce-32ba-78c2-8acb-951a186f23ff
**Status:** Abgeschlossen (11.10.2026)
**Ergebnis:** Änderungsliste für chatgpt-review (r2/03 + Ergänzungen r3/03), Umsetzung per skill-pflege; Abnahme des
Wegs codex bestanden (drei Runden ohne Kopieren)

---

## Runden-Übersicht

### Runde 1 — Weg codex: Sicherheit, Ablauf, Regelqualität
- **Artefakte:** [r1/](./r1/)
- **Fokus:** Sicherheitsmodell (Sandbox, Websuche, Prompt-Inhalt), Robustheit von Aufruf und Folgerunde, Schnitt
  SKILL.md ↔ references, Lücken
- **Kernergebnis:** Sandbox-Fehlschlag ist keine dauerhafte Lesegrenze; `-o` direkt in `02` widerspricht der
  Fehlerregel; Commit-URLs statt Branch; Altbestand mit Qualitätsabweichungen

### Runde 2 — Claudes Einschätzung, Nachschärfung
- **Artefakte:** [r2/](./r2/)
- **Fokus:** Sandbox-Test, Websuche bei vertraulichem Inhalt, Versuche und Timeout, Trennung Altbestand
- **Kernergebnis:** Sandbox-Test nur mit eindeutiger Diagnose; Websuche threadweit aus nach vertraulichem Kontext;
  Retry kann den Thread verändern; konsolidierte Liste mit 9 Punkten

### Runde 3 — Prüfung der konsolidierten Liste
- **Artefakte:** [r3/](./r3/)
- **Fokus:** Vollständigkeit, Reihenfolge, Auslöser „Websuche aus“, Umfang
- **Kernergebnis:** umsetzungsreif mit Präzisierungen: Diagnose je geprüfter Umgebung in der Reference, ein
  Vertrauensblock in jedem Prompt, „Websuche aus“ auf Serienebene vor dem Senden mit Block „Dateien“ statt
  Repo-Zugriff, Kontextrekonstruktion beim Wechsel auf „kopieren“

## Abnahme

Weg codex in drei Runden ohne Kopieren: r1 `codex exec`, r2 und r3 `codex exec resume` im selben Thread; Codex las die
Dateien über die Live-Websuche; je Runde alle vier Dateien in ihrer Phase. r3 bereits mit Ausgabe im Scratchpad und
Übernahme nach Erfolg.

## Ergebnisse

- Umsetzung in `skills/chatgpt-review/` (skill-pflege, CHANGELOG)
- Altbestand (kopierte Querschnittsregeln, BPM-Fallback, „Code vollständig“, „Modus 7a/2“, Personenname und
  Cowork-Details im Archiv, pauschale Themenfrage, Namensschema) → Skill-Issue für Umbau Phase 6
- Gemini CLI als weiterer Reviewer → ClickUp-Aufgabe
- Später: Berechtigungsprofile von Codex als technische Lesegrenze prüfen
