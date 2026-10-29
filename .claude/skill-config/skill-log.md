# Skill-Log-Konfiguration – Skill-Repo

Für den Skill skill-auswertung (Skill-Profil → Skill-Log): welche Logs ausgewertet werden, wie weit, und wohin die
Befunde gehen. Format des Logs: [docs/skill-log-v1.md](../../docs/skill-log-v1.md).

## Inhalt

- Log-Ordner
- Ausgewertet bis
- Ablage der Befunde

## Log-Ordner

| Rechner (`host`) | Ordner | Anmerkung |
|---|---|---|
| ha-pi | `/data/home/.claude/skill-log` | Home Assistant, Terminal-App; Log läuft seit 29.09.2026 |
| desktop-pc | `~/.claude/skill-log` am Desktop-PC (Windows) | Plugin `work-hooks@workbench` seit 07.10.2026; Desktop-App: `!`-Zeilen sind dort normale Prompts (Art `befehl`); im Sammel-Repo unter `logs/desktop-pc/` seit 21.10.2026 (`log_repo` nachgetragen); Umlaute bis zum Plugin-Update nach 21.10. doppelt kodiert (die Auswertung repariert sie beim Lesen) |
| surface7 | `~/.claude/skill-log` am Surface (Windows) | eingerichtet 08.10.2026 mit `tools/install.ps1`, Plugin `work-hooks` (Desktop-App) seit 09.10.2026; im Sammel-Repo unter `logs/surface7/` |
| Firmenlaptop | `~/.claude/skill-log` am Firmenlaptop (Windows) | im Sammel-Repo unter `logs/Firmenlaptop/` (Rechnername so im Log); bisher nur ein Abgleich am 11.10.2026 |

Sammel-Repo: `herbertschrotter-blip/skill-log` (privat, seit 08.10.2026; Klon `~/.claude/skill-log-sammel/logs/<rechner>/`). Rechner, die `log_repo` gesetzt haben, sind dort mit drin. Wird auf einem Rechner ausgewertet, der die Ordner der anderen nicht sieht, nur die erreichbaren auswerten und die
fehlenden im Bericht nennen.

## Ausgewertet bis

| Rechner | ausgewertet bis (UTC) |
|---|---|
| ha-pi | 2026-10-29T15:34:30Z |
| surface7 | 2026-10-14T20:02:48Z |
| desktop-pc | 2026-10-27T21:11:47Z |
| Firmenlaptop | 2026-10-26T21:51:21Z |

`–` heißt: noch nie ausgewertet, „seit letzter Auswertung“ bedeutet dann „alles“.

## Ablage der Befunde

- Eval-Fälle: `quality/evals/<fall>/`, Regeln und Tabelle in `quality/README.md`; Fallname mit dem Skill als Präfix
  und `-real-` im Namen (Beispiel: `tracker-real-aufgabe-anlegen`), Tag `real` zusätzlich zum Skillnamen
- Skill-Issues: über tracker in die Liste des Skills (`.claude/skill-config/tracker.md`)
- Nachschärfen: skill-pflege, Befund und Vorschlag als Auftrag
