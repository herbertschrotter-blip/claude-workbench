#!/usr/bin/env python3
"""Statuszeile für Claude Code: Modell · Repo@Branch · laufende Review-Serie (CGR) mit Runde und Fortschritt.

Liest das JSON von Claude Code auf stdin. Die Ablage kommt aus `.claude/skill-config/review.md`. Eine Serie gilt als laufend, wenn im README der Serie die Zeile
**Status:** nicht mit „Abgeschlossen“ beginnt. Fortschritt = vorhandene Dateien der höchsten Runde (01–04).
"""
import json
import pathlib
import re
import subprocess
import sys


def git(cwd, *args):
    try:
        r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, timeout=2)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def review_ablage(wurzel):
    """Review-Ablage aus der Review-Config des Repos (Zeile „Review-Ablage: `<pfad>`“), sonst docs/chatgpt-reviews."""
    config = pathlib.Path(wurzel) / ".claude" / "skill-config" / "review.md"
    try:
        m = re.search(r"Review-Ablage:\s*`([^`]+)`", config.read_text(encoding="utf-8"))
        if m:
            return pathlib.Path(wurzel) / m.group(1).strip().rstrip("/")
    except Exception:
        pass
    return pathlib.Path(wurzel) / "docs" / "chatgpt-reviews"


def laufende_serie(wurzel):
    ablage = review_ablage(wurzel)
    if not ablage.is_dir():
        return ""
    serien = []
    for readme in ablage.glob("CGR-*/README.md"):
        try:
            text = readme.read_text(encoding="utf-8")
        except Exception:
            continue
        m = re.search(r"^\*\*Status:\*\*\s*(.+)$", text, re.M)
        if m and not m.group(1).strip().startswith("Abgeschlossen"):
            serien.append(readme.parent)
    if not serien:
        return ""
    serie = sorted(serien)[-1]
    runden = sorted((p for p in serie.glob("r*") if p.is_dir() and p.name[1:].isdigit()), key=lambda p: int(p.name[1:]))
    if not runden:
        return f"CGR {serie.name[4:]}"
    runde = runden[-1]
    n = sum(1 for f in ("01-claude-prompt.md", "02-chatgpt-response.md", "03-claude-analysis.md",
                        "04-user-decisions.md") if (runde / f).exists())
    weg = "codex" if "**Weg:** codex" in (serie / "README.md").read_text(encoding="utf-8") else "kopieren"
    return f"CGR {serie.name[15:]} {runde.name} {n}/4 ({weg})"


def main():
    try:
        daten = json.load(sys.stdin)
    except Exception:
        daten = {}
    modell = (daten.get("model") or {}).get("display_name") or ""
    cwd = (daten.get("workspace") or {}).get("current_dir") or daten.get("cwd") or "."
    teile = [modell] if modell else []
    wurzel = git(cwd, "rev-parse", "--show-toplevel")
    if wurzel:
        branch = git(cwd, "branch", "--show-current") or "?"
        teile.append(f"{pathlib.Path(wurzel).name}@{branch}")
        serie = laufende_serie(wurzel)
        if serie:
            teile.append(serie)
    print(" · ".join(teile))


if __name__ == "__main__":
    main()
