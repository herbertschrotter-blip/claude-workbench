#!/usr/bin/env python3
"""Neustart-Warteschlange: stimmt Neustarts eines gemeinsamen Systems zwischen den Claude-Sitzungen eines Rechners ab.

Die Warteschlange schreibt der Skill neustart (skills/neustart/scripts/sitzungen.py); Format in
skills/neustart/references/sitzungen.md#Warteschlange. Ablage: ~/.claude/neustart/ (bzw. $CLAUDE_CONFIG_DIR/neustart).

Hook für Claude Code:
- Stop             → wartet eine andere Sitzung auf einen Neustart, ruht Claude hier noch nicht: Hinweis, jetzt mit dem
                     Skill neustart für sie neu zu starten (je Wunsch einmal, nie zweimal hintereinander).
- PreToolUse       → während eine andere Sitzung neu startet, werden Aufrufe an das Ziel abgelehnt (Exit 2).
- UserPromptSubmit,
  PostToolUse      → nach einem Neustart durch eine andere Sitzung einmal der Hinweis, Zustände neu zu lesen.
- SessionStart     → merkt sich den Stand, damit eine neue Sitzung keinen alten Neustart gemeldet bekommt.
Die anderen Sitzungen bekommen keine Nachricht; der Hook wirkt nur in der Sitzung, in der er gerade läuft.

Ein Fehler im Skript stört nie: Exit 0 ohne Ausgabe. Abschalten: Umgebungsvariable NEUSTART_HOOK=aus.
"""

import json
import os
import re
import sys
import time

OFF = ("aus", "off", "0", "false", "no", "nein")
SPERRE_MAX = 900  # Sekunden, wie sitzungen.py
# Werkzeuge je Ziel, die während des Neustarts abgelehnt werden
ZIEL_WERKZEUGE = {
    "home-assistant": r"^mcp__home-assistant__",
    "home-assistant-yaml": r"^mcp__home-assistant__",
}


def queue_dir():
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    return os.path.join(base, "neustart")


def alive(pid):
    try:
        os.kill(pid, 0)
    except PermissionError:
        return True
    except (OSError, ValueError):
        return False
    return pid > 0


def lesen(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def schreiben(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    os.replace(tmp, path)


def uhr(t):
    return time.strftime("%H:%M", time.localtime(t))


def sperre(q, is_alive=alive, now=time.time):
    s = lesen(os.path.join(q, "sperre.json"))
    if s and is_alive(int(s.get("pid") or 0)) and now() - s.get("seit", 0) < SPERRE_MAX:
        return s
    return None


def fremde_wuensche(q, sid, is_alive=alive):
    result = []
    try:
        names = sorted(os.listdir(os.path.join(q, "wuensche")))
    except OSError:
        return result
    for name in names:
        if not name.endswith(".json"):
            continue
        w = lesen(os.path.join(q, "wuensche", name))
        if w and w.get("sitzung") != sid and is_alive(int(w.get("pid") or 0)):
            result.append(w)
    return sorted(result, key=lambda w: w.get("seit", 0))


def stand_pfad(q, sid):
    return os.path.join(q, "sitzungen", re.sub(r"[^\w-]", "_", sid) + ".json")


def handle(data, q=None, is_alive=alive, now=time.time):
    """Liefert (exit_code, stdout, stderr)."""
    q = q or queue_dir()
    event = data.get("hook_event_name") or ""
    sid = data.get("session_id") or ""
    if not sid:
        return 0, "", ""
    if not os.path.isdir(q):
        return 0, "", ""
    letzter = lesen(os.path.join(q, "letzter.json")) or {}
    stand_datei = stand_pfad(q, sid)
    stand = lesen(stand_datei)

    if event == "SessionStart" or stand is None:
        stand = {"gesehen": letzter.get("zeit", 0), "gefragt": []}
        schreiben(stand_datei, stand)
        if event == "SessionStart":
            return 0, "", ""

    if event == "PreToolUse":
        s = sperre(q, is_alive, now)
        muster = ZIEL_WERKZEUGE.get((s or {}).get("ziel") or "")
        if s and s.get("sitzung") != sid and muster and re.search(muster, data.get("tool_name") or ""):
            return 2, "", (f"Neustart-Warteschlange: {s.get('ziel')} startet gerade neu (durch Sitzung {s.get('name')}, "
                           f"seit {uhr(s.get('seit', 0))}). Warte, bis es wieder läuft (etwa alle 30 Sekunden erneut "
                           f"versuchen, höchstens 5 Minuten), und lies danach die Zustände neu.")
        return 0, "", ""

    if event == "Stop":
        if data.get("stop_hook_active") or sperre(q, is_alive, now):
            return 0, "", ""
        gefragt = set(stand.get("gefragt", []))
        neu = [w for w in fremde_wuensche(q, sid, is_alive) if f"{w.get('sitzung')}@{w.get('seit')}" not in gefragt]
        if not neu:
            return 0, "", ""
        stand["gefragt"] = sorted(gefragt | {f"{w.get('sitzung')}@{w.get('seit')}" for w in neu})[-50:]
        schreiben(stand_datei, stand)
        liste = "; ".join(f"Sitzung {w.get('name')} ({w.get('ordner')}) wartet seit {uhr(w.get('seit', 0))} auf einen "
                          f"Neustart von {w.get('ziel')}: {w.get('grund') or 'ohne Grund'}" for w in neu)
        grund = (f"Neustart-Warteschlange: {liste}. Deine Runde ist fertig, also startest du jetzt für sie neu: Skill "
                 f"neustart, Abschnitt „Für eine andere Sitzung neu starten“ (Ziel aus dem Eintrag, "
                 f"sitzungen.py --wuensche). Laufen bei dir noch Befehle im Hintergrund, warte sie zuerst ab. Darfst "
                 f"du hier nicht neu starten (Regeln der Umgebung), sag das dem Nutzer in einer Zeile und höre auf.")
        return 0, json.dumps({"decision": "block", "reason": grund}, ensure_ascii=False), ""

    if event in ("UserPromptSubmit", "PostToolUse"):
        zeit = letzter.get("zeit", 0)
        if zeit <= stand.get("gesehen", 0):
            return 0, "", ""
        stand["gesehen"] = zeit
        schreiben(stand_datei, stand)
        if letzter.get("sitzung") == sid:
            return 0, "", ""
        text = (f"Neustart-Warteschlange: {letzter.get('ziel') or 'Das System'} wurde um {uhr(zeit)} neu gestartet "
                f"(durch Sitzung {letzter.get('name')}). Zustände, die du vorher gelesen hast, können veraltet sein; "
                f"vor dem Weiterarbeiten neu lesen.")
        if sid in letzter.get("erledigt", []):
            text += " Dein eigener Neustart-Wunsch ist damit erledigt: nur noch kontrollieren (Skill neustart)."
        out = {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}
        return 0, json.dumps(out, ensure_ascii=False), ""

    return 0, "", ""


def main():
    if (os.environ.get("NEUSTART_HOOK") or "").strip().lower() in OFF:
        return 0
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        code, out, err = handle(json.loads(raw or "{}"))
    except Exception:  # noqa: BLE001 – der Hook darf nie stören
        return 0
    if out:
        sys.stdout.write(out)
    if err:
        sys.stderr.write(err)
    return code


if __name__ == "__main__":
    sys.exit(main())
