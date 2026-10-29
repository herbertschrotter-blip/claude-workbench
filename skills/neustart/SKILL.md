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
anderen Sitzung etwas läuft, und prüft danach, ob das System wieder läuft. Die anderen Sitzungen bekommen davon nichts
mit: keine Nachricht, nichts in ihrem Verlauf.

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
Claude dort ruht und kein Befehl von ihr läuft, auch keiner im Hintergrund. Wie das geht:
[references/sitzungen.md](references/sitzungen.md). Den anderen Sitzungen nichts schicken.

### 3. Warten, wenn nötig

Sind alle frei: gleich weiter mit Schritt 4. Sonst still warten, bis alle frei sind, **höchstens 15 Minuten**, und dem
Nutzer in einer Zeile sagen, auf welche Sitzung gewartet wird. Danach Auswahlfrage mit den noch belegten Sitzungen:
weiter warten (nochmals 15 Minuten) / trotzdem neu starten / abbrechen.

### 4. Neu starten

Unmittelbar vor dem Neustart noch einmal prüfen, ob alle frei sind. Dann neu starten, wie die Reference es beschreibt,
und warten, bis das System wieder antwortet.

### 5. Kontrollieren

Kontrolle laut Reference: läuft das System, sind neue Fehler im Protokoll, sind die betroffenen Teile da. Dem Nutzer
kurz berichten: Prüfung, Wartezeit, Neustart, Kontrolle. Ein Fehler nach dem Neustart wird nicht still übergangen.

## VERBOTEN

- neu starten, ohne dass die Konfiguration grün geprüft ist
- neu starten, während eine andere Sitzung belegt ist, außer der Nutzer entscheidet es per Auswahlfrage
- den anderen Sitzungen Nachrichten über den Neustart schicken
- die App, in der Claude läuft, oder den Rechner neu starten
- einen Neustart melden, ohne danach kontrolliert zu haben

## VERWEIS

- Sitzungen und Fenster verwalten → sitzung. Einspielen und Code → code-erstellen.
- Prüfen, ob anderswo etwas läuft: [references/sitzungen.md](references/sitzungen.md).
- Stacks: [references/stacks/home-assistant.md](references/stacks/home-assistant.md).
