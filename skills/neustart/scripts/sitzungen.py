#!/usr/bin/env python3
"""Andere laufende Claude-Code-Sitzungen dieses Rechners: frei oder belegt – für den Skill neustart.

  python3 sitzungen.py                 Tabelle: frei/belegt, status, laufende Befehle, name, ordner (ohne die eigene)
  python3 sitzungen.py --warten 900    wartet, bis alle anderen frei sind (höchstens so viele Sekunden)

Warteschlange (~/.claude/neustart/, references/sitzungen.md#Warteschlange):
  --eintragen --ziel <stack> --grund <text>   eigenen Neustart-Wunsch eintragen
  --austragen                                 eigenen Wunsch entfernen
  --wuensche                                  offene Wünsche aller Sitzungen zeigen
  --sperre                                    Sperre für den Neustart nehmen (Exit 0) oder melden, wer sie hat (Exit 1)
  --fertig                                    Neustart erledigt: Wünsche von vorher austragen, Sperre lösen

Frei = Status idle oder waiting (wartet auf den Nutzer) und kein Shell-Befehl unter dem Claude-Prozess (Claude Code
startet jeden Befehl, auch im Hintergrund, über eine Shell mit einem Snapshot unter shell-snapshots/; MCP-Server und
das Warten dieses Skripts zählen nicht).
Quelle: ~/.claude/sessions/<pid>.json (bzw. $CLAUDE_CONFIG_DIR/sessions); Einträge ohne lebenden Prozess zählen nicht.
Die eigene Sitzung wird über die Prozesskette erkannt (das Skript läuft als Kind von Claude Code).
Exit 0: alle anderen frei; 1: nach Ablauf der Wartezeit noch belegt; 2: Sitzungsordner nicht lesbar;
4: der eigene Wunsch wurde von einer anderen Sitzung erledigt (nur kontrollieren).
"""

import argparse
import glob
import json
import os
import sys
import time


FREI = ("idle", "waiting")
SPERRE_MAX = 900  # Sekunden; eine ältere Sperre gilt als liegen geblieben


def base_dir():
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


def sessions_dir():
    return os.path.join(base_dir(), "sessions")


def queue_dir():
    return os.path.join(base_dir(), "neustart")


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def ancestors():
    """PIDs der Prozesskette nach oben (Linux /proc; sonst nur die eigene und die Eltern-PID)."""
    pids, pid = set(), os.getpid()
    for _ in range(64):
        pids.add(pid)
        try:
            with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
                pid = int(fh.read().rsplit(")", 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            pids.add(os.getppid())
            break
        if pid <= 1:
            break
    return pids


def children(pid):
    try:
        with open(f"/proc/{pid}/task/{pid}/children", encoding="utf-8") as fh:
            return [int(x) for x in fh.read().split()]
    except (OSError, ValueError):
        return []


def cmdline(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as fh:
            return fh.read().replace(b"\0", b" ").decode("utf-8", "replace").strip()
    except OSError:
        return ""


def befehle(pid, kids=children, cmd=cmdline):
    """Laufende Befehle einer Sitzung: direkte Kind-Prozesse, die eine Shell von Claude Code sind (shell-snapshots).
    Das Warten dieses Skripts (Neustart-Wunsch in der Warteschlange) zählt nicht."""
    zahl = 0
    for c in kids(pid):
        text = cmd(c)
        if "shell-snapshots" in text and not ("sitzungen.py" in text and "--warten" in text):
            zahl += 1
    return zahl


def others(directory=None, own=None, is_alive=alive, count=befehle):
    own = ancestors() if own is None else own
    result = []
    for path in sorted(glob.glob(os.path.join(directory or sessions_dir(), "*.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            pid = int(data.get("pid"))
        except (OSError, ValueError, TypeError):
            continue
        if pid in own or not is_alive(pid):
            continue
        status = data.get("status") or "?"
        laufend = count(pid)
        result.append({"name": data.get("name") or data.get("sessionId"), "status": status, "befehle": laufend,
                       "frei": status in FREI and laufend == 0, "sitzung": data.get("sessionId") or "", "tmux": data.get("tmux") or "",
                       "ordner": data.get("cwd") or "", "art": data.get("kind") or ""})
    return result


def own_session(directory=None, own=None):
    """Eintrag der eigenen Sitzung (sessions/<pid>.json eines Prozesses der eigenen Prozesskette)."""
    own = ancestors() if own is None else own
    for path in glob.glob(os.path.join(directory or sessions_dir(), "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            if int(data.get("pid")) in own:
                return data
        except (OSError, ValueError, TypeError):
            continue
    return {}


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
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def wuensche(q=None, is_alive=alive):
    """Offene Neustart-Wünsche; Wünsche beendeter Sitzungen werden entfernt."""
    q = q or queue_dir()
    result = []
    for path in sorted(glob.glob(os.path.join(q, "wuensche", "*.json"))):
        w = lesen(path)
        if not w:
            continue
        if not is_alive(int(w.get("pid") or 0)):
            try:
                os.remove(path)
            except OSError:
                pass
            continue
        result.append(w)
    return sorted(result, key=lambda w: w.get("seit", 0))


def eintragen(me, ziel, grund, q=None, now=time.time):
    q = q or queue_dir()
    w = {"sitzung": me["sessionId"], "pid": me["pid"], "name": me.get("name") or me["sessionId"],
         "ordner": me.get("cwd") or "", "ziel": ziel, "grund": grund, "seit": now()}
    schreiben(os.path.join(q, "wuensche", f"{me['sessionId']}.json"), w)
    return w


def austragen(sitzung, q=None):
    try:
        os.remove(os.path.join(q or queue_dir(), "wuensche", f"{sitzung}.json"))
    except OSError:
        pass


def sperre_lesen(q=None, is_alive=alive, now=time.time):
    """Gültige Sperre oder None; eine liegen gebliebene (Prozess weg, zu alt) wird entfernt."""
    path = os.path.join(q or queue_dir(), "sperre.json")
    s = lesen(path)
    if s and is_alive(int(s.get("pid") or 0)) and now() - s.get("seit", 0) < SPERRE_MAX:
        return s
    if s is not None:
        try:
            os.remove(path)
        except OSError:
            pass
    return None


def sperre_nehmen(me, ziel, q=None, is_alive=alive, now=time.time):
    """Nimmt die Sperre atomar; liefert (True, eigene) oder (False, fremde Sperre)."""
    q = q or queue_dir()
    os.makedirs(q, exist_ok=True)
    path = os.path.join(q, "sperre.json")
    for _ in range(2):
        s = {"sitzung": me["sessionId"], "pid": me["pid"], "name": me.get("name") or me["sessionId"], "ziel": ziel,
             "seit": now()}
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            alt = sperre_lesen(q, is_alive, now)
            if alt:
                return (alt["sitzung"] == me["sessionId"], alt)
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(s, fh, ensure_ascii=False)
        return True, s
    return False, sperre_lesen(q, is_alive, now)


def fertig(me, q=None, is_alive=alive, now=time.time):
    """Neustart erledigt: Wünsche von vor dem Neustart austragen, letzten Neustart festhalten, Sperre lösen."""
    q = q or queue_dir()
    s = lesen(os.path.join(q, "sperre.json")) or {}
    beginn = s.get("seit", now()) if s.get("sitzung") == me["sessionId"] else now()
    erledigt = [w for w in wuensche(q, is_alive) if w.get("seit", 0) <= beginn]
    for w in erledigt:
        austragen(w["sitzung"], q)
    letzter = {"zeit": now(), "beginn": beginn, "sitzung": me["sessionId"], "name": me.get("name") or me["sessionId"],
               "ziel": s.get("ziel") or "", "erledigt": [w["sitzung"] for w in erledigt]}
    schreiben(os.path.join(q, "letzter.json"), letzter)
    if s.get("sitzung") == me["sessionId"]:
        try:
            os.remove(os.path.join(q, "sperre.json"))
        except OSError:
            pass
    return letzter


def erledigt_fuer(sitzung, seit, q=None):
    """Letzter Neustart, wenn er den eigenen Wunsch (eingetragen zu `seit`) erledigt hat, sonst None."""
    letzter = lesen(os.path.join(q or queue_dir(), "letzter.json")) or {}
    if sitzung in letzter.get("erledigt", []) and letzter.get("beginn", 0) >= seit:
        return letzter
    return None


def show(rows):
    if not rows:
        print("keine andere laufende Sitzung")
    for r in rows:
        zustand = "frei" if r["frei"] else "belegt"
        print(f"{zustand:<7} {r['status']:<8} {r['befehle']} Befehle  {r['name']:<40} {r['ordner']}")


def uhr(t):
    return time.strftime("%H:%M", time.localtime(t))


def main():
    parser = argparse.ArgumentParser(description="Andere laufende Claude-Code-Sitzungen: frei oder belegt")
    parser.add_argument("--warten", type=int, default=0, help="Sekunden warten, bis alle anderen Sitzungen frei sind")
    parser.add_argument("--takt", type=int, default=10, help="Abstand der Prüfungen in Sekunden")
    parser.add_argument("--eintragen", action="store_true", help="eigenen Neustart-Wunsch eintragen")
    parser.add_argument("--ziel", default="", help="Ziel des Neustarts (Stack, z. B. home-assistant)")
    parser.add_argument("--grund", default="", help="Grund des Neustarts")
    parser.add_argument("--austragen", action="store_true", help="eigenen Neustart-Wunsch entfernen")
    parser.add_argument("--wuensche", action="store_true", help="offene Neustart-Wünsche zeigen")
    parser.add_argument("--sperre", action="store_true", help="Sperre für den Neustart nehmen")
    parser.add_argument("--fertig", action="store_true", help="Neustart erledigt melden, Sperre lösen")
    args = parser.parse_args()
    if not os.path.isdir(sessions_dir()):
        print(f"Sitzungsordner fehlt: {sessions_dir()}")
        return 2
    me = own_session()
    if (args.eintragen or args.austragen or args.sperre or args.fertig) and not me.get("sessionId"):
        print("eigene Sitzung nicht gefunden (Skript nicht aus Claude Code gestartet?)")
        return 2
    if args.wuensche:
        for w in wuensche():
            print(f"{uhr(w['seit'])}  {w['ziel']:<16} {w['name']:<30} {w['grund']}  ({w['ordner']})")
        s = sperre_lesen()
        print(f"Sperre: {s['name']} seit {uhr(s['seit'])}" if s else "Sperre: keine")
        return 0
    if args.eintragen:
        if not args.ziel:
            print("--ziel fehlt")
            return 2
        w = eintragen(me, args.ziel, args.grund)
        print(f"eingetragen: {w['ziel']} um {uhr(w['seit'])}")
        return 0
    if args.austragen:
        austragen(me["sessionId"])
        print("ausgetragen")
        return 0
    if args.sperre:
        ok, s = sperre_nehmen(me, args.ziel)
        print("Sperre genommen" if ok else f"Sperre hat {s['name']} seit {uhr(s['seit'])}")
        return 0 if ok else 1
    if args.fertig:
        letzter = fertig(me)
        print(f"Neustart um {uhr(letzter['zeit'])} festgehalten, erledigt für {len(letzter['erledigt'])} Wünsche")
        return 0
    mein = lesen(os.path.join(queue_dir(), "wuensche", f"{me.get('sessionId')}.json")) if me else None
    end = time.monotonic() + args.warten
    while True:
        if mein:
            letzter = erledigt_fuer(mein["sitzung"], mein["seit"])
            if letzter:
                print(f"Neustart erledigt durch {letzter['name']} um {uhr(letzter['zeit'])}")
                return 4
        rows = others()
        busy = [r for r in rows if not r["frei"]]
        s = sperre_lesen()
        fremd = s if s and s.get("sitzung") != me.get("sessionId") else None
        if (not busy and not fremd) or time.monotonic() >= end:
            show(rows)
            if fremd:
                print(f"Sperre: {fremd['name']} startet gerade neu (seit {uhr(fremd['seit'])})")
            return 1 if busy or fremd else 0
        time.sleep(min(args.takt, max(1, end - time.monotonic())))


if __name__ == "__main__":
    sys.exit(main())
