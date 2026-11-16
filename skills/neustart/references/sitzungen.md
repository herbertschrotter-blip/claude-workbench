# Prüfen, ob in einer anderen Sitzung etwas läuft

Gilt für Claude Code. Im Cowork-Chat gibt es keine anderen Sitzungen auf dem Rechner; dort bestätigt der Nutzer vor dem
Neustart, dass nichts anderes läuft.

## Frei oder belegt

Eine andere Sitzung ist **frei**, wenn beides gilt:

- Claude ruht dort (Status `idle`, mit Befehl im Hintergrund `shell`) oder wartet auf den Nutzer (`waiting`, etwa eine
  Freigabe oder Auswahlfrage). Belegt ist `busy` (Claude arbeitet). Eine wartende Sitzung erfährt nach dem Neustart
  über den Hook, dass neu gestartet wurde (Abschnitt „Warteschlange“).
- Kein Befehl der Sitzung läuft, auch keiner im Hintergrund: kein Shell-Prozess unter dem Claude-Prozess. Dauerhafte
  Hilfsprozesse wie MCP-Server zählen nicht, ebenso jeder Befehl, der `sitzungen.py` aufruft (das Warten auf den
  Neustart, auch in einer selbst gebauten Schleife).
- Ausnahme: Eine Sitzung mit eingetragenem Wunsch ist frei, sobald sie ruht oder auf den Nutzer wartet, auch wenn bei
  ihr noch ein Befehl läuft. Sie wartet selbst auf den Neustart.

Ein Agent im Hintergrund, der gerade nur liest und keinen Befehl ausführt, ist so nicht sicher zu erkennen; startet er
Befehle, ist die Sitzung belegt.

## Skript

```
python3 <Skill-Ordner>/scripts/sitzungen.py
```

zeigt je anderer Sitzung Status, laufende Befehle und `frei`/`belegt` (Quelle `~/.claude/sessions/`, nur lebende
Prozesse, ohne die eigene Sitzung). Exit 0 = alle frei, 1 = mindestens eine belegt.

Eintragen und im Hintergrund warten, ohne den Chat zu blockieren – **ein** Befehl, keine eigene Schleife:

```
python3 <Skill-Ordner>/scripts/sitzungen.py --warten 900 --ziel home-assistant --grund "<kurz>"
```

Mit `--ziel` trägt das Skript den eigenen Wunsch vorher in die Warteschlange ein; ohne `--ziel` wartet es nur. Es endet, sobald alle frei sind und keine andere Sitzung die Sperre hat (Exit 0), spätestens nach 900 Sekunden
(Exit 1, mit der Liste der belegten). Hat eine andere Sitzung den eigenen Wunsch inzwischen erledigt, endet es mit
Exit 4 („erledigt durch …“): dann nur noch kontrollieren.

## Warteschlange

Ablage `~/.claude/neustart/` (bzw. `$CLAUDE_CONFIG_DIR/neustart/`), gemeinsam für alle Sitzungen des Rechners:

| Datei | Inhalt |
|---|---|
| `wuensche/<sitzung>.json` | ein Wunsch je Sitzung: `sitzung`, `pid`, `name`, `ordner`, `ziel` (Stack), `grund`, `seit` |
| `sperre.json` | wer gerade neu startet: `sitzung`, `pid`, `name`, `ziel`, `seit`; atomar angelegt |
| `letzter.json` | letzter Neustart: `zeit`, `beginn`, `sitzung`, `name`, `ziel`, `erledigt` (Sitzungen) |
| `sitzungen/<sitzung>.json` | nur für den Hook: welcher Neustart schon gemeldet, nach welchen Wünschen schon gefragt |

Befehle:

```
python3 <Skill-Ordner>/scripts/sitzungen.py --eintragen --ziel home-assistant --grund "<kurz>"
```

```
python3 <Skill-Ordner>/scripts/sitzungen.py --wuensche
```

```
python3 <Skill-Ordner>/scripts/sitzungen.py --sperre --ziel home-assistant
```

```
python3 <Skill-Ordner>/scripts/sitzungen.py --fertig
```

```
python3 <Skill-Ordner>/scripts/sitzungen.py --austragen
```

- `--sperre`: Exit 0 = genommen, Exit 1 = eine andere Sitzung startet gerade neu (Name und Uhrzeit in der Ausgabe).
- `--fertig`: trägt alle Wünsche aus, die vor dem Nehmen der Sperre eingetragen waren, schreibt `letzter.json` und löst
  die Sperre. Ein später eingetragener Wunsch bleibt stehen, er braucht einen weiteren Neustart.
- Wünsche beendeter Sitzungen fallen weg. Eine Sperre gilt als liegen geblieben, wenn ihre Sitzung beendet ist oder sie
  älter als 15 Minuten ist; dann darf eine andere Sitzung sie übernehmen.

Der Hook (`plugins/work-hooks/hooks/neustart_hook.py`) wirkt nur in der Sitzung, in der er läuft:

- **Stop:** offene Wünsche anderer Sitzungen, keine Sperre → Claude ruht noch nicht, sondern startet für sie neu. Je
  Wunsch einmal; ein zweiter Stop direkt danach geht durch.
- **PreToolUse** (Werkzeuge des Ziels, bei Home Assistant `mcp__home-assistant__…`): hat eine andere Sitzung die
  Sperre, wird der Aufruf abgelehnt.
- **UserPromptSubmit, PostToolUse** (Antwort auf eine Auswahlfrage): Hinweis auf einen Neustart einer anderen Sitzung,
  einmal je Neustart.
- **SessionStart:** merkt sich den Stand; eine neue Sitzung bekommt keinen älteren Neustart gemeldet.

Abschalten: Umgebungsvariable `NEUSTART_HOOK=aus`. Befehle der Shell (`ha core …`) sperrt der Hook nicht.

## Ohne Skript

Die Sitzungsliste der Umgebung (`ListAgents`) zeigt den Status (`busy`, `idle`, `offline`); Sitzungen mit `offline`
oder in der Cloud arbeiten nicht auf diesem Rechner und zählen nicht. Laufende Befehle zeigt sie nicht; dann nur nach
dem Status entscheiden und das dem Nutzer sagen.
