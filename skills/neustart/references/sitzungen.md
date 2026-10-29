# Prüfen, ob in einer anderen Sitzung etwas läuft

Gilt für Claude Code. Im Cowork-Chat gibt es keine anderen Sitzungen auf dem Rechner; dort bestätigt der Nutzer vor dem
Neustart, dass nichts anderes läuft.

## Frei oder belegt

Eine andere Sitzung ist **frei**, wenn beides gilt:

- Claude ruht dort (Status `idle`). Belegt sind `busy` (Claude arbeitet), `waiting` (wartet auf den Nutzer, etwa
  eine Freigabe oder Auswahlfrage) und `shell` (ein Befehl läuft).
- Kein Befehl der Sitzung läuft, auch keiner im Hintergrund: kein Shell-Prozess unter dem Claude-Prozess. Dauerhafte
  Hilfsprozesse wie MCP-Server zählen nicht.

Ein Agent im Hintergrund, der gerade nur liest und keinen Befehl ausführt, ist so nicht sicher zu erkennen; startet er
Befehle, ist die Sitzung belegt.

## Skript

```
python3 <Skill-Ordner>/scripts/sitzungen.py
```

zeigt je anderer Sitzung Status, laufende Befehle und `frei`/`belegt` (Quelle `~/.claude/sessions/`, nur lebende
Prozesse, ohne die eigene Sitzung). Exit 0 = alle frei, 1 = mindestens eine belegt.

Im Hintergrund warten, ohne den Chat zu blockieren:

```
python3 <Skill-Ordner>/scripts/sitzungen.py --warten 900
```

Das Skript endet, sobald alle frei sind (Exit 0), spätestens nach 900 Sekunden (Exit 1, mit der Liste der belegten).

## Ohne Skript

Die Sitzungsliste der Umgebung (`ListAgents`) zeigt den Status (`busy`, `idle`, `offline`); Sitzungen mit `offline`
oder in der Cloud arbeiten nicht auf diesem Rechner und zählen nicht. Laufende Befehle zeigt sie nicht; dann nur nach
dem Status entscheiden und das dem Nutzer sagen.
