# ChatGPT-Reviews – Übersicht

Review-Gespräche zwischen Claude und ChatGPT zu diesem Repo (Skill `chatgpt-review`, Review-Profil in `CLAUDE.md`).
Je Serie ein Ordner `CGR-<JJJJ-MM-TT>-<thema>/` mit `README.md` und je Runde `r<N>/` (01 Prompt, 02 Antwort, 03 Einschätzung,
04 Entscheidungen).

## Aktueller Stand

| Serie | Thema | Start | Status | Kernergebnis |
|---|---|---|---|---|
| [CGR-2026-09-23-ha-grundsatz](./CGR-2026-09-23-ha-grundsatz/README.md) | ha-grundsatz | 2026-09-23 | Abgeschlossen | Grundsatzregeln G-01 … G-21, Einstellungsmatrix, `module.yaml` Schema v1; ein fachlicher Eigentümer je Wert, Schnittstelle ≠ Speicherort; Ergebnis-Ort `docs/ha-grundsatz/` und Skill `modul-bauplan` |
| [CGR-2026-09-24-skillsystem](./CGR-2026-09-24-skillsystem/README.md) | skillsystem | 2026-09-24 | Abgeschlossen | Umbau-Plan [docs/skillsystem-umbau.md](../skillsystem-umbau.md): Skill-Profil v1 je Repo, Configs unter `.claude/skill-config/`, kein Skill-Analyse-Skill (Prüfskript + audit), Messung mit `claude plugin eval` und echten Sitzungen, cc-steuerung als Cowork-Adapter, Phasen 1–7 |
| [CGR-2026-10-09-skillsystem](./CGR-2026-10-09-skillsystem/README.md) | skillsystem | 2026-10-09 | Abgeschlossen | projekt-anlegen als Generator für ein Walking Skeleton: Bausteine + Manifeste, eigenes Skript, Grenze technische Funktionsfähigkeit vs. fachliches Verhalten, Pilot Python (+SQLite) → HA-Integration; Plan in [docs/skillsystem-umbau.md](../skillsystem-umbau.md) |
| [CGR-2026-10-11-skillsystem](./CGR-2026-10-11-skillsystem/README.md) | skillsystem | 2026-10-11 | Abgeschlossen | chatgpt-review über die Codex CLI: Abnahme in drei Runden ohne Kopieren; Sandbox-Test mit eindeutiger Diagnose, „Websuche aus“ bei vertraulichem Kontext, Ausgabe erst bei Erfolg nach `02`, Commit-URLs; Altbestand → Phase 6 |
| [CGR-2026-10-12-ha-grundsatz](./CGR-2026-10-12-ha-grundsatz/README.md) | ha-grundsatz | 2026-10-12 | Abgeschlossen | audit prüft gegen G-01 … G-22: Modul 7 mit HA-Reference, Ergebnisvertrag im neutralen Kern, mehrere Nachweise je Regel, Check-Format mit Auswahl/Eingaben, `module.yaml` mit `components`/`ui.types`/`critical_for` |
| [CGR-2026-10-13-ha-grundsatz](./CGR-2026-10-13-ha-grundsatz/README.md) | ha-grundsatz | 2026-10-13 | Abgeschlossen | G-24 Langzeitarchiv: fachliche Vorgänge als JSONL je Monat unter `<config>/archiv/<domain>/` mit versionierten Schemas, Sitzungen als Beginn – Signal je Abruf – Ende, dokumentiertes Verlustfenster; Konzept [docs/ha-grundsatz/archiv.md](../ha-grundsatz/archiv.md) |
