---
name: neustart
description: >
  Startet ein gemeinsam genutztes System (z. B. Home Assistant) abgestimmt neu: Konfiguration prüfen, still
  nachsehen, ob in einer anderen Claude-Code-Sitzung des Rechners gerade etwas läuft (Claude arbeitet, ein Befehl oder
  Agent läuft), sonst sofort neu starten, sonst warten (höchstens 15 Minuten, dann Auswahlfrage), danach den Zustand
  prüfen. Schreibt den anderen Sitzungen keine Nachrichten. Use when users say "neustart", "starte HA neu", "Home
  Assistant neu starten", "mach einen Neustart", or when a deployment (einspielen, ausliefern) needs a restart. Do not
  trigger for restarting Claude or a tmux window (sitzung), restarting the Claude add-on or the host, restarting
  devices like a robot vacuum or TV, a plain reload of automations or scripts without restart, or the code changes
  themselves (code-erstellen).
---

# neustart – abgestimmt neu starten

## Zweck

Mehrere Claude-Sitzungen arbeiten auf demselben Rechner gegen dasselbe System. Ein Neustart mitten in der Arbeit einer
anderen Sitzung lässt dort Aufrufe, Prüfungen oder Tests scheitern. Dieser Skill startet deshalb erst neu, wenn in keiner
anderen Sitzung etwas läuft, und prüft danach, ob das System wieder läuft. Die anderen Sitzungen bekommen keine
Nachricht. Wer warten muss, trägt sich in eine gemeinsame Warteschlange ein; was die anderen Sitzungen davon wissen
müssen, sagt ihnen ein Hook (Abschnitt „Warteschlange“).

- **Abgrenzung:** Claude oder ein tmux-Fenster neu starten → sitzung. Code ändern und einspielen → code-erstellen; das
  ruft diesen Skill auf, wenn das Einspielen einen Neustart braucht. Ein Reload ohne Neustart läuft ohne Abstimmung im
  Skill, der die Änderung macht.
- **Nie:** die App, in der Claude selbst läuft (z. B. das Claude-Add-on), oder den ganzen Rechner neu starten; das
  beendet alle Sitzungen. Das macht nur der Nutzer. Geräte neu starten nur auf ausdrücklichen Auftrag und nicht mit
  diesem Skill.

## Benötigte Werte

- **Ziel:** aus `Code.Stacks` des Skill-Profils der Sitzung (`docs/skill-profile-v1.md`). Je Ziel gibt es eine
  Reference mit Prüfung, Neustart und Kontrolle:

  | Stack im Profil | Reference |
  |---|---|
  | `home-assistant`, `home-assistant-yaml` | [references/stacks/home-assistant.md](references/stacks/home-assistant.md) |

  Passt kein Stack oder fehlt das Profil: Auswahlfrage mit den Zielen der Tabelle und „abbrechen“; nie raten.
- **Erlaubnis:** Die Regeln der Umgebung (CLAUDE.md) müssen Claude den Neustart erlauben. Steht dort, dass nur der
  Nutzer neu startet, bereitet der Skill alles vor (Prüfung, Warten) und bittet am Ende den Nutzer, neu zu starten.

## Ablauf

### 1. Konfiguration prüfen

Prüfung laut Reference. Ist sie nicht grün: kein Neustart, Fehler melden.

### 2. Nachsehen, ob anderswo etwas läuft

Die anderen laufenden Claude-Sitzungen des Rechners still prüfen, ohne die eigene. Eine Sitzung ist **frei**, wenn
Claude dort ruht oder auf den Nutzer wartet und kein Befehl von ihr läuft, auch keiner im Hintergrund. Das Warten auf
den Neustart zählt nicht als Befehl, und eine Sitzung mit eingetragenem Wunsch ist frei, sobald sie ruht. Wie das geht: [references/sitzungen.md](references/sitzungen.md).
Den anderen Sitzungen nichts schicken.

### 3. Warten, wenn nötig

Sind alle frei: gleich weiter mit Schritt 4. Sonst den eigenen Wunsch eintragen und still warten, beides mit **einem**
Befehl im Hintergrund: `sitzungen.py --warten 900 --ziel <Ziel> --grund "<kurz>"`
([references/sitzungen.md](references/sitzungen.md#skript)). Keine eigene Warteschleife bauen: Nur so steht der Wunsch
in der Warteschlange, und die anderen Sitzungen wissen davon. Gewartet wird, bis alle frei sind, **höchstens 15
Minuten**; dem Nutzer in einer Zeile sagen, auf welche Sitzung gewartet wird. Endet der Befehl mit 0, weiter mit
Schritt 4. Während des Wartens kann die Sitzung, die als Letzte fertig wird, den Neustart für alle machen; dann
endet das Warten mit „erledigt durch …“ und es geht gleich mit Schritt 5 weiter. Nach den 15 Minuten Auswahlfrage mit
den noch belegten Sitzungen: weiter warten (nochmals 15 Minuten) / trotzdem neu starten / abbrechen (Wunsch austragen).

### 4. Neu starten

Unmittelbar vor dem Neustart noch einmal prüfen, ob alle frei sind, und die Sperre der Warteschlange nehmen. Hat sie
schon eine andere Sitzung, startet diese gerade neu: nicht selbst neu starten, sondern warten, bis sie fertig ist, und
mit Schritt 5 weitermachen. Mit der Sperre neu starten, wie die Reference es beschreibt, und warten, bis das System
wieder antwortet. Dann den Neustart in der Warteschlange als erledigt melden; das löst die Sperre und trägt alle Wünsche
aus, die vor dem Neustart eingetragen waren.

### 5. Kontrollieren

Kontrolle laut Reference: läuft das System, sind neue Fehler im Protokoll, sind die betroffenen Teile da. Dem Nutzer
kurz berichten: Prüfung, Wartezeit, Neustart, Kontrolle. Ein Fehler nach dem Neustart wird nicht still übergangen.

## Frage vor dem Einspielen

Fragt ein Skill vor einem Einspielen, das einen Neustart braucht, den Nutzer per Auswahlfrage (z. B. code-erstellen,
ticket), läuft vorher das Nachsehen aus Schritt 2. Arbeitet eine andere Sitzung noch, stehen diese Optionen in dieser
Reihenfolge:

1. **Einspielen, `<Name der Sitzung>` startet danach neu (Empfehlung):** einspielen, Wunsch in die Warteschlange, ohne
   Zeitgrenze warten; die Sitzung, die zuletzt fertig wird, startet für alle neu (Abschnitt „Warteschlange“). Diese
   Sitzung kontrolliert danach selbst. Endet das Warten nach 15 Minuten ohne Neustart, wird derselbe Befehl still
   erneut gestartet, ohne Auswahlfrage.
2. **Einspielen und warten:** wie Schritt 3, höchstens 15 Minuten, dann Auswahlfrage.
3. **Einspielen, Nutzer startet neu.**

„Später“ entfällt in diesem Fall; es bleibt über die freie Antwort möglich. Sind alle frei, gelten die Optionen des
fragenden Skills unverändert.

## Warteschlange

Die Sitzungen eines Rechners teilen sich eine Warteschlange für Neustart-Wünsche, eine Sperre für den laufenden Neustart
und den Stand des letzten Neustarts. Ein Hook der Plugins `work` und `work-hooks` liest sie in jeder Sitzung:

- **Am Ende einer Runde:** Wartet eine andere Sitzung auf einen Neustart, ruht Claude noch nicht, sondern startet für
  sie neu (Abschnitt „Für eine andere Sitzung neu starten“). Der Hinweis kommt je Wunsch einmal.
- **Während des Neustarts:** Aufrufe anderer Sitzungen an das Ziel lehnt der Hook ab, bis die Sperre gelöst ist.
- **Danach:** Die nächste Eingabe oder Antwort des Nutzers in einer anderen Sitzung bringt dort den Hinweis, dass neu
  gestartet wurde und gelesene Zustände veraltet sein können.

Sitzungen ohne den Hook (älterer Plugin-Stand) kennen die Warteschlange nicht; für sie gilt nur das Nachsehen. Format,
Befehle und Grenzen: [references/sitzungen.md](references/sitzungen.md#warteschlange).

### Für eine andere Sitzung neu starten

Meldet der Hook am Ende der Runde einen wartenden Wunsch:

1. Eigene Befehle im Hintergrund abwarten.
2. Darf Claude hier nicht neu starten (Regeln der Umgebung, Abschnitt „Benötigte Werte“), das dem Nutzer in einer Zeile
   sagen und aufhören; der Wunsch bleibt eingetragen.
3. Sonst den Ablauf ab Schritt 1 für das **Ziel aus dem Eintrag** gehen, nicht für das Ziel des eigenen Profils.
   Hat die eigene Sitzung selbst einen Wunsch eingetragen, erledigt derselbe Neustart beide.
4. Kontrolliert wird, ob das System läuft und das Protokoll keine neuen Fehler zeigt; die Teile, die der Eintrag
   betrifft, prüft die wartende Sitzung selbst (Schritt 5 dort).
5. Dem Nutzer kurz berichten, für welche Sitzung neu gestartet wurde.

## VERBOTEN

- neu starten, ohne dass die Konfiguration grün geprüft ist
- neu starten, während eine andere Sitzung belegt ist, außer der Nutzer entscheidet es per Auswahlfrage
- den anderen Sitzungen Nachrichten über den Neustart schicken (etwa mit `SendMessage`); die Hinweise des Hooks sind
  erlaubt, sie landen nicht als Nachricht in der anderen Sitzung
- die App, in der Claude läuft, oder den Rechner neu starten
- einen Neustart melden, ohne danach kontrolliert zu haben
- neu starten, ohne die Sperre der Warteschlange zu haben, oder sie nach dem Neustart liegen lassen
- vor einem Einspielen mit Neustart fragen, ohne nachgesehen zu haben, ob eine andere Sitzung arbeitet (Abschnitt
  „Frage vor dem Einspielen“)
- eine eigene Warteschleife bauen, statt mit `sitzungen.py --warten … --ziel …` einzutragen und zu warten

## VERWEIS

- Sitzungen und Fenster verwalten → sitzung. Einspielen und Code → code-erstellen.
- Prüfen, ob anderswo etwas läuft: [references/sitzungen.md](references/sitzungen.md).
- Stacks: [references/stacks/home-assistant.md](references/stacks/home-assistant.md).
