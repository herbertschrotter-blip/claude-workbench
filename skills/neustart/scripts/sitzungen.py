#!/usr/bin/env python3
"""Andere laufende Claude-Code-Sitzungen dieses Rechners und ihr Status (busy/idle) – für den Skill neustart.

  python3 sitzungen.py                 Tabelle: name, status, tmux, ordner (ohne die eigene Sitzung)
  python3 sitzungen.py --warten 900    wartet, bis keine andere Sitzung mehr busy ist (höchstens so viele Sekunden)

Quelle: ~/.claude/sessions/<pid>.json (bzw. $CLAUDE_CONFIG_DIR/sessions); Einträge ohne lebenden Prozess zählen nicht.
Die eigene Sitzung wird über die Prozesskette erkannt (das Skript läuft als Kind von Claude Code).
Exit 0: keine andere Sitzung busy; 1: nach Ablauf der Wartezeit noch busy; 2: Sitzungsordner nicht lesbar.
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


def others(directory=None, own=None, is_alive=alive):
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
        result.append({"name": data.get("name") or data.get("sessionId"), "status": data.get("status") or "?",
                       "tmux": data.get("tmux") or "", "ordner": data.get("cwd") or "", "art": data.get("kind") or ""})
    return result


def show(rows):
    if not rows:
        print("keine andere laufende Sitzung")
    for r in rows:
        print(f"{r['status']:<6} {r['name']:<40} {r['tmux']:<16} {r['ordner']}")


def main():
    parser = argparse.ArgumentParser(description="Andere laufende Claude-Code-Sitzungen und ihr Status")
    parser.add_argument("--warten", type=int, default=0, help="Sekunden warten, bis keine andere Sitzung busy ist")
    parser.add_argument("--takt", type=int, default=10, help="Abstand der Prüfungen in Sekunden")
    args = parser.parse_args()
    if not os.path.isdir(sessions_dir()):
        print(f"Sitzungsordner fehlt: {sessions_dir()}")
        return 2
    end = time.monotonic() + args.warten
    while True:
        rows = others()
        busy = [r for r in rows if r["status"] == "busy"]
        if not busy or time.monotonic() >= end:
            show(rows)
            return 1 if busy else 0
        time.sleep(min(args.takt, max(1, end - time.monotonic())))


if __name__ == "__main__":
    sys.exit(main())
