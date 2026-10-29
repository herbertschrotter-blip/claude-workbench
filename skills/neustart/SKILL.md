---
name: neustart
description: >
  Startet ein gemeinsam genutztes System (z. B. Home Assistant) abgestimmt neu: Konfiguration prüfen, die anderen
  laufenden Claude-Code-Sitzungen des Rechners ansehen, arbeitende um eine Pause nach ihrer Aufgabe bitten, warten
  (höchstens 15 Minuten, dann Auswahlfrage), neu starten, den Zustand prüfen und die Sitzungen wieder freigeben. Regelt
  auch, wie eine Sitzung auf eine solche Pause-Bitte antwortet. Use when users say "neustart", "starte HA neu", "Home
  Assistant neu starten", "mach einen Neustart", when a deployment (einspielen, ausliefern) needs a restart, or when
  another Claude session asks for a pause before a restart. Do not trigger for restarting Claude or a tmux window
  (sitzung), restarting the Claude add-on or the host, restarting devices like a robot vacuum or TV, a plain reload of
  automations or scripts without restart, or the code changes themselves (code-erstellen).
---

# neustart – abgestimmt neu starten

## Zweck

Mehrere Claude-Sitzungen arbeiten auf demselben Rechner gegen dasselbe System. Ein Neustart mitten in der Arbeit einer
anderen Sitzung lässt dort Aufrufe, Prüfungen oder Tests scheitern. Dieser Skill startet deshalb nur neu, wenn die
anderen Sitzungen ihre Aufgabe abgeschlossen haben und Bescheid wissen, und prüft danach, ob das System wieder läuft.

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
  Nutzer neu startet, bereitet der Skill alles vor (Prüfung, Abstimmung) und bittet am Ende den Nutzer, neu zu starten.

## Ablauf

### 1. Konfiguration prüfen

Prüfung laut Reference. Ist sie nicht grün: kein Neustart, Fehler melden, Abstimmung gar nicht erst beginnen.

### 2. Andere Sitzungen ansehen

Die laufenden Claude-Sitzungen des Rechners mit Status holen (arbeitet / ruht), ohne die eigene. Wie das geht:
[references/sitzungen.md](references/sitzungen.md). Gibt es keine andere Sitzung, weiter mit Schritt 5.

### 3. Bescheid geben

Jeder anderen Sitzung eine Nachricht schicken, Absender ist der Name der eigenen Sitzung:

- **arbeitet:** „<System> wird neu gestartet (angefragt von <eigener Name>). Bitte schließe deine laufende Aufgabe ab,
  beginne danach keine Aktion gegen <System> und antworte mit ‚bereit‘. Freigabe folgt nach dem Neustart.“
- **ruht:** „<System> wird gleich neu gestartet (<eigener Name>). Bitte bis zur Freigabe keine Aktion gegen <System>.“

Dem Nutzer in einer Zeile sagen, wer arbeitet und worauf gewartet wird.

### 4. Warten

Warten, bis jede arbeitende Sitzung „bereit“ geantwortet hat oder nicht mehr arbeitet, **höchstens 15 Minuten**.
Danach Auswahlfrage an den Nutzer mit den noch arbeitenden Sitzungen: weiter warten (nochmals 15 Minuten) / trotzdem neu
starten / abbrechen. Bei „abbrechen“ den anderen Sitzungen die Freigabe schicken.

Beginnt eine Sitzung, die schon „bereit“ war, wieder zu arbeiten, wartet der Skill erneut auf sie.

### 5. Neu starten

Unmittelbar vor dem Neustart noch einmal den Status holen. Dann neu starten, wie die Reference es beschreibt, und
warten, bis das System wieder antwortet.

### 6. Kontrollieren

Kontrolle laut Reference: läuft das System, sind neue Fehler im Protokoll, sind die betroffenen Teile da. Befunde dem
Nutzer melden; ein Fehler nach dem Neustart wird nicht still übergangen.

### 7. Freigeben

Allen in Schritt 3 benachrichtigten Sitzungen: „<System> läuft wieder (<Ergebnis in einem Satz>). Ihr könnt
weitermachen.“ Dem Nutzer kurz berichten: Prüfung, Wartezeit, Neustart, Kontrolle.

## Pause-Bitte einer anderen Sitzung

Kommt eine Nachricht einer anderen Sitzung, dass ein System neu gestartet wird:

- **Läuft gerade eine Aufgabe:** sie bis zu einem sauberen Zwischenstand abschließen (laufende Prüfung oder Test zu
  Ende, nichts halb eingespielt), danach keine neue Aktion gegen dieses System beginnen und der anfragenden Sitzung mit
  „bereit“ antworten. Dem Nutzer in einer Zeile sagen, dass auf einen Neustart gewartet wird.
- **Ruht die Sitzung:** nur merken, keine Antwort nötig.
- Bis zur Freigabe nichts gegen dieses System tun; Arbeit ohne das System (Lesen, Schreiben im Repo) darf weitergehen.
  Kommt nach 30 Minuten keine Freigabe, den Status des Systems selbst prüfen und den Nutzer fragen.

Ob eine Sitzung der Bitte folgt, regelt die CLAUDE.md der Umgebung; ohne diese Regel ist die Nachricht nur ein Hinweis,
und die Sitzung fragt ihren Nutzer.

## VERBOTEN

- neu starten, ohne dass die Konfiguration grün geprüft ist
- neu starten, während eine andere Sitzung arbeitet und nicht „bereit“ gemeldet hat, außer der Nutzer entscheidet es
  per Auswahlfrage
- die App, in der Claude läuft, oder den Rechner neu starten
- einen Neustart melden, ohne danach kontrolliert zu haben
- benachrichtigte Sitzungen ohne Freigabe zurücklassen, auch nach Abbruch oder Fehler

## VERWEIS

- Sitzungen und Fenster verwalten → sitzung. Einspielen und Code → code-erstellen.
- Sitzungen finden und Nachrichten schicken: [references/sitzungen.md](references/sitzungen.md).
- Ziele: [references/stacks/home-assistant.md](references/stacks/home-assistant.md).
