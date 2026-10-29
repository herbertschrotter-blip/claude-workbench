#!/usr/bin/env python3
"""Andere laufende Claude-Code-Sitzungen dieses Rechners: frei oder belegt – für den Skill neustart.

  python3 sitzungen.py                 Tabelle: frei/belegt, status, laufende Befehle, name, ordner (ohne die eigene)
  python3 sitzungen.py --warten 900    wartet, bis alle anderen frei sind (höchstens so viele Sekunden)

Frei = Status idle und kein Shell-Befehl unter dem Claude-Prozess (Claude Code startet jeden Befehl, auch im
Hintergrund, über eine Shell mit einem Snapshot unter shell-snapshots/; MCP-Server zählen nicht).
Quelle: ~/.claude/sessions/<pid>.json (bzw. $CLAUDE_CONFIG_DIR/sessions); Einträge ohne lebenden Prozess zählen nicht.
Die eigene Sitzung wird über die Prozesskette erkannt (das Skript läuft als Kind von Claude Code).
Exit 0: alle anderen frei; 1: nach Ablauf der Wartezeit noch belegt; 2: Sitzungsordner nicht lesbar.
"""

import argparse
import glob
import json
import os
import sys
import time


def sessions_dir():
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    return os.path.join(base, "sessions")


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
    """Laufende Befehle einer Sitzung: direkte Kind-Prozesse, die eine Shell von Claude Code sind (shell-snapshots)."""
    return sum(1 for c in kids(pid) if "shell-snapshots" in cmd(c))


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
                       "frei": status == "idle" and laufend == 0, "tmux": data.get("tmux") or "",
                       "ordner": data.get("cwd") or "", "art": data.get("kind") or ""})
    return result


def show(rows):
    if not rows:
        print("keine andere laufende Sitzung")
    for r in rows:
        zustand = "frei" if r["frei"] else "belegt"
        print(f"{zustand:<7} {r['status']:<8} {r['befehle']} Befehle  {r['name']:<40} {r['ordner']}")


def main():
    parser = argparse.ArgumentParser(description="Andere laufende Claude-Code-Sitzungen: frei oder belegt")
    parser.add_argument("--warten", type=int, default=0, help="Sekunden warten, bis alle anderen Sitzungen frei sind")
    parser.add_argument("--takt", type=int, default=10, help="Abstand der Prüfungen in Sekunden")
    args = parser.parse_args()
    if not os.path.isdir(sessions_dir()):
        print(f"Sitzungsordner fehlt: {sessions_dir()}")
        return 2
    end = time.monotonic() + args.warten
    while True:
        rows = others()
        busy = [r for r in rows if not r["frei"]]
        if not busy or time.monotonic() >= end:
            show(rows)
            return 1 if busy else 0
        time.sleep(min(args.takt, max(1, end - time.monotonic())))


if __name__ == "__main__":
    sys.exit(main())
