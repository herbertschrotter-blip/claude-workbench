# Arbeit auf Agenten aufteilen (Claude Code)

Gilt nur in Claude Code. Im Cowork-Chat gibt es keine Agenten; dort macht die Sitzung alles selbst.

## Die Agenten

Sie kommen mit dem Plugin `work` und heißen dort `work:<name>`. Modell und Stufe stehen in ihrer Definition; die
Hauptsitzung kann beides beim Start überschreiben. Den Code schreibt die Hauptsitzung selbst: Ein Agent startet leer,
jede Übergabe kostet Token und kann Wissen verlieren, und beim Programmieren lässt sich wenig unabhängig aufteilen.
Agenten lohnen sich dort, wo sie den Kontext der Hauptsitzung sauber halten oder parallel arbeiten.

| Agent | Modell / Stufe | Darf | Wofür |
|---|---|---|---|
| `erkunder` | Haiku, low | nur lesen und suchen | viele Dateien, Doku oder Logs durchsehen und zusammenfassen, bevor geplant wird |
| `pruefer` | Sonnet, low | lesen, Shell; ändert nichts | Tests und Checks laufen lassen, lange Ausgaben auswerten |
| `gutachter` | Opus, high | nur lesen | unabhängiger Blick auf Plan oder Diff |

## Wann aufteilen

- **Viel lesen, bevor geplant werden kann** (mehrere Module, unbekannter Code, lange Logs): ein oder mehrere
  `erkunder` parallel, je mit klarer Frage.
- **Lange oder viele Checks:** `pruefer`, damit die Hauptsitzung weiterarbeiten kann.
- **Deep oder heikle Änderung:** vor dem Commit zusätzlich `gutachter` auf den Diff, neben dem Selbst-Review.

## Wann nicht

- Modus Lite und alles, was in wenigen Schritten selbst erledigt ist: Ein Agent kostet Übergabe und Kontext.
- Code schreiben oder ändern: Das macht die Hauptsitzung.
- Alles gegen das laufende System (einspielen, neu starten, Live-Daten, Geräte), Push, Tracker-Änderungen: Das macht
  nur die Hauptsitzung.

## Modell und Stufe wählen

- Standard ist die Definition des Agenten.
- **Fable** (`fable`) für die schwersten Aufgaben: ein Fehler, an dem Opus zweimal gescheitert ist, eine knifflige
  Architekturfrage. Als `gutachter` oder `erkunder` mit `fable` starten; hängt die ganze Aufgabe daran, dem Nutzer
  vorschlagen, die Sitzung mit `/model` auf Fable zu stellen. Etwa 2,5-mal so teuer wie Opus; dem Nutzer in einer
  Zeile sagen, wofür Fable läuft.
- Stufe: `low` für Lesen und Prüfen, `high` für Code, `max` nur, wenn Richtigkeit wichtiger ist als Kosten.

## Auftrag schreiben

Ein Agent kennt nur seinen Auftrag. Darin stehen: Ziel und Akzeptanz, die betroffenen Dateien, was nicht geändert
werden darf, welche Checks laufen sollen, was zurückkommen soll.

## Ergebnis übernehmen

- Ergebnisse von Agenten sind Vorschläge: Die Hauptsitzung prüft sie (an der genannten Stelle nachlesen, Befund
  nachvollziehen), bevor sie danach handelt.
- Selbst-Review, Commit, Push und Auslieferung laufen wie gewohnt in der Hauptsitzung.
