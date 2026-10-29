# Sitzungen finden und benachrichtigen

Gilt für Claude Code. Im Cowork-Chat gibt es keine anderen Sitzungen auf dem Rechner; dort entfallen die Schritte
„Andere Sitzungen ansehen“ bis „Warten“, und der Nutzer bestätigt vor dem Neustart, dass nichts anderes läuft.

## Status holen

- **Werkzeug der Umgebung:** `ListAgents` listet die anderen Sitzungen dieses Rechners mit Name, Art und Status
  (`busy` = arbeitet, `idle` = ruht, `offline`). Sitzungen mit `offline` oder in der Cloud zählen nicht: Sie arbeiten
  nicht auf diesem Rechner.
- **Skript:** `python3 <Skill-Ordner>/scripts/sitzungen.py` zeigt dasselbe aus `~/.claude/sessions/` (ohne die eigene
  Sitzung, nur lebende Prozesse). Exit 0 = keine andere Sitzung arbeitet, 1 = mindestens eine arbeitet.

## Nachricht schicken

`SendMessage` an den Namen aus der Sitzungsliste, genau wie er dort steht. Antworten kommen als Benachrichtigung in die
eigene Sitzung zurück.

## Warten

Im Hintergrund warten, ohne den Chat zu blockieren:

```
python3 <Skill-Ordner>/scripts/sitzungen.py --warten 900
```

Das Skript endet, sobald keine andere Sitzung mehr arbeitet (Exit 0), spätestens nach 900 Sekunden (Exit 1, mit der
Liste der noch arbeitenden). Eine Antwort „bereit“ zählt auch, wenn die Sitzung danach noch kurz als arbeitend gilt.
