"""Abgleich der Seitenliste: stimmen Quelldatei, Code, Mockups und erzeugte Dateien überein?

Aufruf: python3 tools/seitenliste_check.py – Exit 0 grün, 1 Fehler. Läuft als Check (Mockup.Pruefung, Code.Tests,
Commit.Pre-Commit-Checks). Ein geänderter Fingerabdruck ohne neue Version ist nur ein Hinweis. Bekannte Grenze: Varianten
mit # zählen nur als „Hauptseite gibt es“.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

import datenliste as dl
import seitenliste as sl


def version(v: str | None) -> tuple[int, int]:
    teile = (v or "0.0").split(".")
    return int(teile[0]), int(teile[1])


def schluessel(s: dict) -> list[str]:
    k = s.get("schluessel") or []
    return [k] if isinstance(k, str) else k


def im_code(cfg: dict) -> set[str]:
    """Schlüssel aller Seiten im Code, gefunden über `seiten_im_code` (Muster des Projekts)."""
    da: set[str] = set()
    for q in cfg.get("seiten_im_code", []):
        text = (sl.WURZEL / q["datei"]).read_text(encoding="utf8")
        block = re.search(q["block"], text)
        if not block:
            raise ValueError(f"{q['datei']}: Muster „{q['block']}“ passt nicht mehr")
        da |= {f"{q['praefix']}:{m}" for m in re.findall(q["eintrag"], block[1])}
    return da


def pruefe_code(cfg: dict, seiten: list[dict]) -> list[str]:
    fehler = []
    gebaut = [s for s in seiten if s.get("version_code") or s.get("code")]  # neue Seite: Mockup läuft dem Code voraus
    basis = {k.split("#")[0] for s in gebaut for k in schluessel(s)}
    entwurf = {k.split("#")[0] for s in seiten for k in schluessel(s)} - basis
    if cfg.get("seiten_im_code"):
        try:
            da = im_code(cfg)
        except (OSError, ValueError) as e:
            return [str(e)]
        fehler += [f"im Code, nicht in der Liste: {k}" for k in sorted(da - basis - entwurf)]
        fehler += [f"in der Liste, nicht im Code: {k}" for k in sorted(basis - da)]
    fehler += [f"{s['nr']}: kein Schlüssel" for s in gebaut if not schluessel(s)]
    for s in seiten:
        fehler += [f"{s['nr']}: Datei fehlt: {d}" for d in sl.dateien(s) if not (sl.WURZEL / cfg["code_wurzel"] / d).exists()]
    return fehler


def pruefe_nummern(seiten: list[dict]) -> list[str]:
    nr = [s["nr"] for s in seiten]
    fehler = [f"Nummer doppelt: {n}" for n in sorted({n for n in nr if nr.count(n) > 1})]
    fehler += [f"{s['nr']}: Verbindung ins Leere: {z}" for s in seiten for z in s.get("zu", []) if z not in nr]
    return fehler


def pruefe_versionen(cfg: dict, seiten: list[dict]) -> list[str]:
    fehler = []
    ablage = sl.WURZEL / cfg["mockup_ablage"]
    for s in seiten:
        m, c = s.get("version_mockup"), s.get("version_code")
        hoechste = max(m, c, key=version) if m or c else None
        im_verlauf = [e["v"] for e in s.get("verlauf") or []]
        letzte = max(im_verlauf, key=version) if im_verlauf else None
        if letzte != hoechste:
            fehler.append(f"{s['nr']}: Verlauf reicht bis {letzte}, Version ist {hoechste}")
        if s.get("mockup_alt") and not (ablage / s["mockup_alt"]).exists():
            fehler.append(f"{s['nr']}: Mockup fehlt: {s['mockup_alt']}")
        if s.get("mockup"):
            pfad = ablage / s["mockup"]
            if not pfad.exists():
                fehler.append(f"{s['nr']}: Mockup fehlt: {s['mockup']}")
                continue
            t = pfad.read_text(encoding="utf8")
            if f"nr: '{s['nr']}'" not in t:
                fehler.append(f"{s['nr']}: Nummer fehlt im Mockup")
            if f"version: '{m}'" not in t:
                fehler.append(f"{s['nr']}: Version {m} fehlt im Mockup")
    return fehler


def pruefe_theme(cfg: dict) -> list[str]:
    """Führt den Theme-Befehl aus, vergleicht und stellt den alten Stand wieder her."""
    theme = cfg.get("theme")
    if not theme or not theme.get("befehl"):
        return []
    pfade = [sl.WURZEL / d for d in theme["dateien"]]
    alt = {p: p.read_bytes() if p.exists() else None for p in pfade}
    try:
        try:
            lauf = subprocess.run(theme["befehl"], cwd=sl.WURZEL, capture_output=True, text=True, check=False)
        except OSError as e:
            return [f"Theme-Befehl läuft nicht: {e}"]
        if lauf.returncode:
            return [f"Theme-Befehl scheitert: {lauf.stderr.strip()[-300:]}"]
        return [f"Theme veraltet: {p.name} ({' '.join(theme['befehl'])})" for p in pfade if p.read_bytes() != alt[p]]
    finally:
        for p, inhalt in alt.items():
            if inhalt is None:
                p.unlink(missing_ok=True)
            else:
                p.write_bytes(inhalt)


def pruefe_erzeugt(cfg: dict, gruppen: list[dict]) -> list[str]:
    fehler = []
    if cfg.get("daten") and not (sl.WURZEL / cfg["daten"]["quelle"]).exists():
        return [f"{cfg['daten']['quelle']} fehlt: python3 tools/datenliste.py"]
    for name, soll in ((cfg["doku"], sl.md(cfg, gruppen)), (cfg["seite"], sl.html(cfg, gruppen))):
        p = sl.WURZEL / name
        if not p.exists() or p.read_text(encoding="utf8") != soll:
            fehler.append(f"{name} veraltet: python3 tools/seitenliste.py")
    return fehler


def pruefe_daten(cfg: dict, seiten: list[dict]) -> list[str]:
    """Neue Tabelle oder Schema-Änderung ohne Eintrag ist rot."""
    d = cfg.get("daten")
    if not d:
        return []
    try:
        stand = dl.schema(d)
    except (OSError, ValueError, subprocess.CalledProcessError) as e:
        return [f"leeres Schema nicht lesbar: {e}"]
    tabellen, zugeordnet = set(stand["tabellen"]), dl.eingeordnet(d)
    fehler = [f"Tabelle ohne Eintrag: {t}" for t in sorted(tabellen - zugeordnet)]
    fehler += [f"Eintrag ohne Tabelle: {t}" for t in sorted(zugeordnet - tabellen)]
    if fehler:
        return fehler
    daten = dl.aufbauen(d, stand)
    q, doku = sl.WURZEL / d["quelle"], sl.WURZEL / d["doku"]
    if not q.exists() or json.loads(q.read_text(encoding="utf8")) != daten:
        fehler.append(f"{d['quelle']} veraltet: python3 tools/datenliste.py")
    if not doku.exists() or doku.read_text(encoding="utf8") != dl.md(daten):
        fehler.append(f"{d['doku']} veraltet: python3 tools/datenliste.py")
    nr = {s["nr"] for s in seiten}
    for g in daten["gruppen"]:
        fehler += [f"{g['nr']}: Seite gibt es nicht: {n}" for n in g["seiten"] if n not in nr]
    return fehler


def hinweise(cfg: dict, seiten: list[dict]) -> list[str]:
    aus = []
    for s in seiten:
        try:
            if s.get("code_stand") and sl.stand(cfg, s) != s["code_stand"]:
                aus.append(f"Hinweis: {s['nr']} {s['name']}: Code geändert ohne neue Version")
        except OSError:
            pass  # die fehlende Datei meldet pruefe_code
        if not s.get("zu") and not any(s["nr"] in x.get("zu", []) for x in seiten):
            aus.append(f"Hinweis: {s['nr']} {s['name']}: keine Verbindungen")
    if not cfg.get("seiten_im_code"):
        aus.append("Hinweis: seiten_im_code fehlt in der Config, Code und Liste sind nicht abgeglichen")
    return aus


def main() -> int:
    cfg = sl.config()
    gruppen = sl.lesen(cfg)
    seiten = [s for g in gruppen for s in g["seiten"]]
    fehler = (
        ([] if any(s["nr"] == cfg["start"] for s in seiten) else [f"Startseite fehlt in der Liste: {cfg['start']}"])
        + pruefe_code(cfg, seiten)
        + pruefe_nummern(seiten)
        + pruefe_versionen(cfg, seiten)
        + pruefe_erzeugt(cfg, gruppen)
        + pruefe_theme(cfg)
        + pruefe_daten(cfg, seiten)
    )
    print("\n".join(hinweise(cfg, seiten) + fehler))
    print(f"Seitenliste: {len(seiten)} Seiten, {len(fehler)} Fehler")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
