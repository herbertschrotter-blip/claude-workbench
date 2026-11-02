"""Erzeugt aus der Quelldatei die Seitenliste: Doku und veröffentlichte Seite (Standard: mockup-erstellen,
references/seitenliste.md).

Aufruf: python3 tools/seitenliste.py [--abnahme <nr> ... | --abnahme alle]
Alle Projektwerte stehen in tools/seitenliste.config.json. --abnahme setzt den Fingerabdruck der Code-Dateien neu.

Aktualisieren (references/seitenliste.md#Aktualisieren), jeweils mit anschließendem Erzeugen:
  --start                einmalig: stand_commit auf HEAD, version_abgenommen aus version_mockup
  --offen                gibt je Seite die Commits seit stand_commit als JSON aus, ändert nichts
  --eintragen <datei>    trägt die bewerteten Versionen ein und setzt stand_commit aller Seiten auf HEAD
  --abgenommen <nr> ...  setzt version_abgenommen auf version_mockup
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
MARKE = "Seitenliste aktualisiert"  # steht im Commit-Titel des Laufs; der Lauf selbst zählt nicht als Änderung


def config() -> dict:
    return json.loads((WURZEL / "tools/seitenliste.config.json").read_text(encoding="utf8"))


def lesen(cfg: dict) -> list[dict]:
    return json.loads((WURZEL / cfg["quelle"]).read_text(encoding="utf8"))


def schreiben(cfg: dict, gruppen: list[dict]) -> None:
    (WURZEL / cfg["quelle"]).write_text(json.dumps(gruppen, ensure_ascii=False, indent=1) + "\n", encoding="utf8")


def md(cfg: dict, gruppen: list[dict]) -> str:
    aus = [
        f"# {cfg['titel']}\n",
        f"Erzeugt aus `{cfg['quelle']}` (`python3 tools/seitenliste.py`) – dort ändern, nicht hier. Die **Nr.** ist der",
        "feste Ort einer Seite. Je Seite zwei Versionen: läuft **Mockup** vor **Code**, ist es abgenommen, aber noch nicht",
        "gebaut. **1.0** = überarbeitet und abgenommen, **0.1** = noch nicht durchgegangen.\n",
    ]
    for g in gruppen:
        aus += [
            f"## {g['nr']} {g['bereich']}\n",
            "| Nr. | Seite | Art | Version Mockup | Version Code | Mockup | Code |",
            "|---|---|---|---|---|---|---|",
        ]
        for s in g["seiten"]:
            m = s.get("mockup") or (f"{s['mockup_alt']} (alt)" if s.get("mockup_alt") else "–")
            aus.append(
                f"| {s['nr']} | {s['name']} | {s['art']} | {s.get('version_mockup') or '–'} "
                f"| {s.get('version_code') or '–'} | `{m}` | `{s.get('code') or '–'}` |"
            )
        aus.append("")
    return "\n".join(aus)


def html(cfg: dict, gruppen: list[dict]) -> str:
    vorlage = (WURZEL / cfg["vorlage"]).read_text(encoding="utf8")
    daten = json.dumps(gruppen, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    tabellen = {"schema": None, "gruppen": []}
    if cfg.get("daten"):
        tabellen = json.loads((WURZEL / cfg["daten"]["quelle"]).read_text(encoding="utf8"))
    tabellen_text = json.dumps(tabellen, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (
        vorlage.replace("@@TITEL@@", cfg["titel"]).replace("@@START@@", cfg["start"])
        .replace("@@DATEN@@", daten).replace("@@TABELLEN@@", tabellen_text).replace("@@THEME@@", theme_text(cfg))
    )  # fmt: skip


def theme_text(cfg: dict) -> str:
    """Bewertete Theme-Hinweise je Seite; ohne Abgleich leer."""
    ziel = (cfg.get("themeabgleich") or {}).get("ziel")
    befunde = json.loads((WURZEL / ziel).read_text(encoding="utf8")) if ziel and (WURZEL / ziel).exists() else {}
    return json.dumps(befunde, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def dateien(s: dict) -> list[str]:
    return sorted(x.strip() for x in (s.get("code") or "").split(",") if x.strip())


def stand(cfg: dict, s: dict) -> str:
    """Fingerabdruck der Code-Dateien einer Seite; ändert sich der Code ohne neue Version, meldet der Abgleich es."""
    h = hashlib.sha1(usedforsecurity=False)
    for d in dateien(s):
        h.update((WURZEL / cfg["code_wurzel"] / d).read_bytes())
    return h.hexdigest()[:10]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=WURZEL, capture_output=True, text=True, check=True).stdout.strip()


def naechste(v: str | None) -> str:
    """+0.1 ohne Überlauf: Aus 0.9 wird 0.10, denn 1.0 entsteht nur durch die Abnahme."""
    haupt, neben = (v or "0.0").split(".")
    return f"{haupt}.{int(neben) + 1}"


def code_pfade(cfg: dict, s: dict) -> list[str]:
    return [str(Path(cfg["code_wurzel"]) / d) for d in dateien(s)]


def mockup_pfad(cfg: dict, s: dict) -> list[str]:
    return [str(Path(cfg["mockup_ablage"]) / s["mockup"])] if s.get("mockup") else []


def commits(ref: str, pfade: list[str]) -> list[dict]:
    if not pfade:
        return []
    zeilen = git("log", "--reverse", "--format=%h%x09%ad%x09%s", "--date=format:%d.%m.%Y", f"{ref}..HEAD", "--", *pfade)
    aus = []
    for z in zeilen.splitlines():
        h, datum, titel = z.split("\t", 2)
        if MARKE not in titel:
            aus.append({"commit": h, "datum": datum, "titel": titel})
    return aus


def offen(cfg: dict, gruppen: list[dict]) -> dict:
    seiten = [s for g in gruppen for s in g["seiten"]]
    anzahl: dict[str, int] = {}
    for s in seiten:
        for d in dateien(s):
            anzahl[d] = anzahl.get(d, 0) + 1
    aus = {"kopf": git("rev-parse", "--short", "HEAD"), "ohne_stand": [], "seiten": []}
    for s in seiten:
        ref = s.get("stand_commit")
        if not ref:
            aus["ohne_stand"].append(s["nr"])
            continue
        code, mockup = commits(ref, code_pfade(cfg, s)), commits(ref, mockup_pfad(cfg, s))
        if code or mockup:
            aus["seiten"].append({
                "nr": s["nr"], "name": s["name"], "code": code, "mockup": mockup,
                "gemeinsam": [d for d in dateien(s) if anzahl[d] > 1],
            })  # fmt: skip
    pfade = sorted({p for s in seiten for p in code_pfade(cfg, s) + mockup_pfad(cfg, s)})
    aus["nicht_committet"] = git("status", "--porcelain", "--", *pfade).splitlines() if pfade else []
    return aus


def mockup_version(cfg: dict, s: dict) -> None:
    """Die Version steht auch in der Mockup-Datei; der Abgleich prüft das."""
    pfad = WURZEL / cfg["mockup_ablage"] / s["mockup"]
    alt = pfad.read_text(encoding="utf8")
    pfad.write_text(re.sub(r"version: '[^']*'", f"version: '{s['version_mockup']}'", alt, count=1), encoding="utf8")


def eintragen(cfg: dict, gruppen: list[dict], liste: list[dict]) -> None:
    """Je Eintrag eine Version. `art` ist code oder mockup, `gebaut: true` zieht den Code auf die Abnahme nach."""
    seiten = {s["nr"]: s for g in gruppen for s in g["seiten"]}
    for e in liste:
        s = seiten[e["nr"]]
        if e["art"] not in ("code", "mockup"):
            raise ValueError(f"{e['nr']}: art muss code oder mockup sein")
        s.setdefault("version_abgenommen", s.get("version_mockup"))
        feld = f"version_{e['art']}"
        if e.get("gebaut"):
            s[feld] = max(s.get(feld), s["version_abgenommen"], key=lambda v: tuple(map(int, (v or "0.0").split("."))))
        else:
            s[feld] = naechste(s.get(feld))
        punkt = {"v": s[feld], "datum": e.get("datum") or date.today().strftime("%d.%m.%Y"), "was": e["was"], "art": e["art"]}
        punkt.update({k: e[k] for k in ("ticket", "commit") if e.get(k)})
        s.setdefault("verlauf", []).append(punkt)
        if e["art"] == "mockup":
            mockup_version(cfg, s)
        else:
            s["code_stand"] = stand(cfg, s)
    kopf = git("rev-parse", "--short", "HEAD")
    for s in seiten.values():
        s["stand_commit"] = kopf


def main() -> None:
    cfg = config()
    gruppen = lesen(cfg)
    if "--offen" in sys.argv:
        print(json.dumps(offen(cfg, gruppen), ensure_ascii=False, indent=1))
        return
    abnahme = []
    if "--abnahme" in sys.argv:
        abnahme = sys.argv[sys.argv.index("--abnahme") + 1 :]
    if "--eintragen" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--eintragen") + 1])
        eintragen(cfg, gruppen, json.loads(datei.read_text(encoding="utf8")))
    if "--abgenommen" in sys.argv:
        nummern = sys.argv[sys.argv.index("--abgenommen") + 1 :]
        for s in (s for g in gruppen for s in g["seiten"] if s["nr"] in nummern):
            s["version_abgenommen"] = s.get("version_mockup")
    if "--start" in sys.argv:
        kopf = git("rev-parse", "--short", "HEAD")
        for s in (s for g in gruppen for s in g["seiten"]):
            s.setdefault("stand_commit", kopf)
            s.setdefault("version_abgenommen", s.get("version_mockup"))
    for g in gruppen:
        for s in g["seiten"]:
            s.setdefault("zu", [])
            s.setdefault("nutzt", [])
            s.setdefault("verlauf", [])
            if s["nr"] in abnahme or "alle" in abnahme or "code_stand" not in s:
                s["code_stand"] = stand(cfg, s)
    schreiben(cfg, gruppen)
    (WURZEL / cfg["doku"]).write_text(md(cfg, gruppen), encoding="utf8")
    (WURZEL / cfg["seite"]).write_text(html(cfg, gruppen), encoding="utf8")


if __name__ == "__main__":
    main()
