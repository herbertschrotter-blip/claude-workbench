#!/usr/bin/env python3
"""Prüfläufe vor dem Commit nach dem Skill-Profil (nur Standardbibliothek).

Liest `### Checks` und `Pre-Commit-Checks` aus dem Skill-Profil der `CLAUDE.md` (docs/skill-profile-v1.md), nimmt die
geänderten Dateien aus git, lässt nur passende Checks laufen und meldet eine Tabelle Check / Dauer / Ergebnis.
Regeln: skills/git-commit-helper/SKILL.md, Abschnitt „Prüfläufe vor dem Commit“.

    python3 checks.py --vor-commit            # Pre-Commit-Checks, die für die Änderung gelten
    python3 checks.py --checks logik,lint     # bestimmte Checks (auch nur, wenn sie gelten)
    python3 checks.py --checks logik --immer  # genannte Checks auf jeden Fall, auch ohne Änderung (Nachweis für den Stand)
    python3 checks.py --vor-commit --json     # Ergebnis als JSON

- Befehle eines Checks laufen nacheinander in einer Shell (`cd` gilt für die folgenden), Abbruch beim ersten Fehler.
- Checks laufen gleichzeitig; ein Check mit `(allein)` im Profil läuft danach für sich (z. B. Tests auf allen Kernen).
- Profilzeile: `- <name>: <befehl; befehl> [(allein)] [auswahl: <glob>; …] [eingaben: <glob>; …]`; eine Klammer ohne
  Schlüssel (`[<glob>; …]`) ist die Auswahl. Unbekannte oder fehlerhafte Angaben brechen vor jedem Lauf ab (Exit 3).
- Ein Check gilt, wenn eine geänderte Datei zu seinen Auswahl- oder Eingabemustern passt. Eingabemuster erfassen alle
  aktuellen Dateien (`git ls-files`, ohne ignorierte), nicht nur die geänderten.
- Ein Check, der mit demselben Stand schon grün war, läuft nicht noch einmal (`--immer` erzwingt es). Je grünem Lauf
  steht ein Datensatz in `.git/skill-checks.json` (Definition, Eingaben, Umgebung, Zeiten, Exit-Code, Log als
  Ergebnisartefakt unter `.git/skill-checks/`, Eingaben vor und nach dem Lauf gleich), nie im Repo.
- Ausgabe je Check in eine Datei; bei Rot stehen die letzten Zeilen im Ergebnis.

Exit 0: nichts rot und kein Befehl fehlt. 1: mindestens ein Check rot. 2: nichts rot, aber ein Befehl fehlt auf diesem
Rechner (z. B. pwsh); der Check muss dann woanders laufen. 3: Profil oder git nicht lesbar.
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

TIMEOUT = 1800  # Sekunden je Check
MERKER = "skill-checks.json"
ARTEFAKTE = "skill-checks"
SCHEMA = 2
SCHLUESSEL = ("auswahl", "eingaben")
_CHECK = re.compile(r"^-\s+([\w.-]+):\s*(.*?)\s*$")
_SCHLUESSEL = re.compile(r"^([A-Za-zÄÖÜäöüß_-]+)\s*:\s*(.*)$", re.S)


class ProfilFehler(Exception):
    pass


def abschnitt(text, ueberschrift, ebene):
    """Zeilen unter einer Überschrift bis zur nächsten gleicher oder höherer Ebene."""
    zeilen, drin = [], False
    for zeile in text.splitlines():
        if re.match(rf"^#{{1,{ebene}}}\s", zeile):
            if drin:
                break
            drin = zeile.strip() == ueberschrift
            continue
        if drin:
            zeilen.append(zeile)
    return zeilen if drin or zeilen else None


def befehle_teilen(text):
    """`a; b` → [a, b]; Semikolons in Anführungszeichen bleiben stehen."""
    teile, aktuell, quote = [], "", None
    for zeichen in text:
        if quote:
            quote = None if zeichen == quote else quote
        elif zeichen in "'\"":
            quote = zeichen
        elif zeichen == ";":
            teile.append(aktuell.strip())
            aktuell = ""
            continue
        aktuell += zeichen
    teile.append(aktuell.strip())
    return [t for t in teile if t]


def ausserhalb(text):
    """Je Zeichen: steht es außerhalb von Anführungszeichen? Dazu, ob am Ende ein Anführungszeichen offen ist."""
    frei, quote = [], None
    for zeichen in text:
        if quote:
            frei.append(False)
            quote = None if zeichen == quote else quote
        elif zeichen in "'\"":
            frei.append(False)
            quote = zeichen
        else:
            frei.append(True)
    return frei, quote is not None


def check_lesen(name, rest):
    """Befehl und Angaben am Zeilenende: `(allein)`, `[auswahl: …]`, `[eingaben: …]`, alt `[<glob>; …]` = Auswahl."""
    frei, offen = ausserhalb(rest)
    if offen:
        raise ProfilFehler(f"Check {name}: Anführungszeichen nicht geschlossen")
    angaben, allein, ende = {}, False, len(rest)
    while True:
        while ende and rest[ende - 1].isspace():
            ende -= 1
        if (ende >= 8 and rest[ende - 8:ende] == "(allein)" and all(frei[ende - 8:ende])
                and (ende == 8 or rest[ende - 9].isspace())):
            if allein:
                raise ProfilFehler(f"Check {name}: (allein) doppelt")
            allein, ende = True, ende - 8
            continue
        if not ende or rest[ende - 1] != "]" or not frei[ende - 1]:
            break
        anfang = next((i for i in range(ende - 2, -1, -1) if frei[i] and rest[i] in "[]"), None)
        if anfang is None or rest[anfang] != "[":
            raise ProfilFehler(f"Check {name}: Klammer am Ende ohne passende öffnende Klammer")
        inhalt = rest[anfang + 1:ende - 1].strip()
        ende = anfang
        m = _SCHLUESSEL.match(inhalt)
        if m and m.group(1) not in SCHLUESSEL:
            raise ProfilFehler(f"Check {name}: unbekannte Angabe „{m.group(1)}“ (erlaubt: {', '.join(SCHLUESSEL)})")
        if not m and any(" " in w.strip() or w.strip().startswith("-") for w in inhalt.split(";")):
            raise ProfilFehler(f"Check {name}: [{inhalt}] ist kein Pfad-Muster – Shell-Klammer am Ende? "
                               "Muster als [auswahl: …] schreiben")
        schluessel, werte = (m.group(1), m.group(2)) if m else ("auswahl", inhalt)
        muster = [w.strip() for w in werte.split(";") if w.strip()]
        if not muster:
            raise ProfilFehler(f"Check {name}: leere Angabe [{inhalt}]")
        if schluessel in angaben:
            raise ProfilFehler(f"Check {name}: {schluessel} doppelt")
        angaben[schluessel] = muster
    befehl = rest[:ende]
    if any(f and z in "[]" for f, z in zip(frei, befehl)) and re.search(r"\[\s*(auswahl|eingaben)\s*:", befehl):
        raise ProfilFehler(f"Check {name}: Angaben müssen am Zeilenende stehen")
    befehle = befehle_teilen(befehl)
    if not befehle:
        raise ProfilFehler(f"Check {name}: kein Befehl")
    return {"befehle": befehle, "muster": angaben.get("auswahl", []), "eingaben": angaben.get("eingaben", []),
            "allein": allein}


def profil_lesen(text):
    """{'checks': {name: {befehle, muster, eingaben, allein}}, 'vor_commit': [namen]} aus einer CLAUDE.md.

    `muster` ist die Auswahl. Fehlerhafte Angaben lösen ProfilFehler aus, bevor irgendein Check läuft."""
    profil = abschnitt(text, "## Skill-Profil", 2)
    if profil is None:
        raise ProfilFehler("kein Abschnitt „## Skill-Profil“ in der CLAUDE.md")
    profil_text = "\n".join(profil)
    checks = {}
    for zeile in abschnitt(profil_text, "### Checks", 3) or []:
        m = _CHECK.match(zeile)
        if not m or m.group(2) in ("", "none"):
            continue
        checks[m.group(1)] = check_lesen(m.group(1), m.group(2))
    vor_commit = []
    for zeile in abschnitt(profil_text, "### Commit", 3) or []:
        m = re.match(r"^-\s+Pre-Commit-Checks:\s*(.*?)\s*$", zeile)
        if m and m.group(1) != "none":
            vor_commit = [n.strip() for n in m.group(1).split(";") if n.strip()]
    return {"checks": checks, "vor_commit": vor_commit}


def muster_regex(muster):
    """Pfad-Glob → Regex: `**` beliebig tief (auch null Ordner), `*` und `?` innerhalb eines Ordners."""
    teile, i = [], 0
    while i < len(muster):
        if muster.startswith("**/", i):
            teile.append("(?:.*/)?")
            i += 3
        elif muster.startswith("**", i):
            teile.append(".*")
            i += 2
        elif muster[i] == "*":
            teile.append("[^/]*")
            i += 1
        elif muster[i] == "?":
            teile.append("[^/]")
            i += 1
        else:
            teile.append(re.escape(muster[i]))
            i += 1
    return re.compile("^" + "".join(teile) + "$")


def passende(dateien, muster):
    """Geänderte Dateien, die zu einem der Muster passen; ohne Muster gilt der Check immer (alle Dateien)."""
    if not muster:
        return sorted(dateien)
    regexe = [muster_regex(m) for m in muster]
    return sorted(d for d in dateien if any(r.match(d) for r in regexe))


def geaendert(wurzel):
    """Geänderte Dateien relativ zur Wurzel: gestaged, ungestaged und neu (bei Umbenennung alter und neuer Name)."""
    r = subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=wurzel,
                       capture_output=True, check=False)
    if r.returncode:
        raise ProfilFehler("git status gescheitert: " + r.stderr.decode(errors="replace").strip())
    teile, dateien, i = r.stdout.decode("utf-8", errors="replace").split("\0"), set(), 0
    while i < len(teile):
        eintrag = teile[i]
        if len(eintrag) > 3:
            dateien.add(eintrag[3:])
            if eintrag[0] in "RC":  # Umbenennung: der alte Name folgt als eigener Eintrag
                i += 1
                if i < len(teile) and teile[i]:
                    dateien.add(teile[i])
        i += 1
    return dateien


def aktuelle(wurzel):
    """Alle aktuellen Dateien relativ zur Wurzel: versioniert und neu, ohne ignorierte und ohne gelöschte."""
    r = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z"], cwd=wurzel, capture_output=True,
                       check=False)
    if r.returncode:
        raise ProfilFehler("git ls-files gescheitert: " + r.stderr.decode(errors="replace").strip())
    return {n for n in r.stdout.decode("utf-8", errors="replace").split("\0") if n}


def datei_hash(pfad):
    """Inhaltshash; None, wenn die Datei fehlt oder nicht lesbar ist."""
    h = hashlib.sha256()
    try:
        with open(pfad, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
    except OSError:
        return None
    return h.hexdigest()


def eingaben_stand(wurzel, check):
    """Stand aller aktuellen Dateien, die zu den Eingabemustern passen: sortiert, je Datei der Inhaltshash."""
    if not check.get("eingaben"):
        return {"patterns": [], "files": [], "digest": None}
    kandidaten = [d for d in passende(aktuelle(wurzel), check["eingaben"]) if (Path(wurzel) / d).is_file()]
    dateien = [{"path": d, "sha256": datei_hash(Path(wurzel) / d)} for d in kandidaten]
    digest = hashlib.sha256(json.dumps(dateien, sort_keys=True).encode()).hexdigest()
    return {"patterns": check["eingaben"], "files": dateien, "digest": digest}


def definition_digest(check):
    """Hash der wirksamen Checkdefinition: Befehle, Auswahl, Eingaben, (allein)."""
    teile = {"befehle": check["befehle"], "auswahl": check.get("muster", []), "eingaben": check.get("eingaben", []),
             "allein": check.get("allein", False)}
    return hashlib.sha256(json.dumps(teile, sort_keys=True).encode()).hexdigest()


def fingerabdruck(wurzel, check, dateien, eingaben=None):
    """Stand des Checks: Definition, Eingabestand und Inhalt der geänderten passenden Dateien (gelöschte als solche)."""
    h = hashlib.sha256(definition_digest(check).encode())
    stand = (eingaben or {}).get("digest")
    if not stand:  # ohne Eingaben: wenigstens der eingecheckte Stand, damit ein Branchwechsel den Vermerk entwertet
        r = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=wurzel, capture_output=True, text=True,
                           check=False)
        stand = "baum:" + (r.stdout.strip() if r.returncode == 0 else "")
    h.update(stand.encode() + b"\0")
    for datei in dateien:
        pfad = Path(wurzel) / datei
        h.update(datei.encode() + b"\0")
        if pfad.is_file():
            h.update(hashlib.sha256(pfad.read_bytes()).digest())
        else:
            h.update(b"<weg>")
    return h.hexdigest()


def git_pfad(wurzel, name):
    """Pfad unter dem Git-Ordner (auch in Worktrees), nie im Repo."""
    r = subprocess.run(["git", "rev-parse", "--git-path", name], cwd=wurzel, capture_output=True, text=True,
                       check=False)
    return Path(wurzel) / r.stdout.strip() if r.returncode == 0 else None


def merker_pfad(wurzel):
    return git_pfad(wurzel, MERKER)


def merker_lesen(datei):
    """Datensätze je Check; ein Merker im alten Format (nur Abdrücke) zählt nicht."""
    try:
        daten = json.loads(datei.read_text(encoding="utf-8")) if datei and datei.is_file() else {}
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(daten, dict) or daten.get("schema") != SCHEMA or not isinstance(daten.get("checks"), dict):
        return {}
    return daten["checks"]


def gilt_noch(wurzel, satz, abdruck):
    """Ein Datensatz trägt „schon grün“ nur bei gleichem Abdruck, stabilen Eingaben und intaktem Ergebnisartefakt."""
    if not satz or satz.get("abdruck") != abdruck or satz.get("input_stable") is not True:
        return False
    artefakt = satz.get("result_artifact") or {}
    if not artefakt.get("path") or not artefakt.get("sha256"):
        return False
    return datei_hash(Path(wurzel) / artefakt["path"]) == artefakt["sha256"]


def jetzt():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def umgebung(wurzel, check):
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=wurzel, capture_output=True, text=True, check=False)
    return {"platform": sys.platform, "python": platform.python_version(), "shell": shell(check["befehle"])[0],
            "head": r.stdout.strip() if r.returncode == 0 else None}


def datensatz(wurzel, name, check, vorher, lauf):
    """Datensatz eines grünen Laufs; das Log wird als Ergebnisartefakt unter den Git-Ordner kopiert."""
    artefakt = None
    ordner = git_pfad(wurzel, ARTEFAKTE)
    if ordner:
        try:
            ordner.mkdir(parents=True, exist_ok=True)
            ziel = ordner / f"{name}.log"
            shutil.copyfile(lauf["ergebnis"]["log"], ziel)
            try:
                pfad = os.path.relpath(ziel, wurzel)
            except ValueError:  # Windows: Worktree auf anderem Laufwerk als der Git-Ordner
                pfad = str(ziel.resolve())
            artefakt = {"path": pfad.replace("\\", "/"), "sha256": datei_hash(ziel)}
        except OSError:
            artefakt = None
    return {"schema": SCHEMA, "check": name, "definition_digest": definition_digest(check),
            "inputs": vorher["eingaben"], "environment": umgebung(wurzel, check), "started_at": lauf["start"],
            "finished_at": lauf["ende"], "exit_code": 0, "result_artifact": artefakt,
            "input_stable": lauf.get("abdruck_nachher") == vorher["abdruck"], "abdruck": vorher["abdruck"]}


def shell(befehle):
    """Aufruf für die Befehle eines Checks: nacheinander, Abbruch beim ersten Fehler."""
    if os.name != "nt":
        return ["sh", "-c", " && ".join(befehle)]
    if shutil.which("pwsh"):
        return ["pwsh", "-NoProfile", "-Command", " && ".join(befehle)]
    return ["powershell", "-NoProfile", "-Command", "; if (-not $?) { exit 1 }; ".join(befehle)]


def ausfuehren(name, check, wurzel, ordner):
    """Führt einen Check aus; Ausgabe nach <ordner>/<name>.log."""
    log = Path(ordner) / f"{name}.log"
    start = time.monotonic()
    try:
        with open(log, "w", encoding="utf-8", errors="replace") as fh:
            r = subprocess.run(shell(check["befehle"]), cwd=wurzel, stdout=fh, stderr=subprocess.STDOUT,
                               timeout=TIMEOUT, check=False)
        code = r.returncode
    except subprocess.TimeoutExpired:
        code = -1
    except OSError as exc:
        log.write_text(str(exc), encoding="utf-8")
        code = 127
    dauer = round(time.monotonic() - start, 1)
    text = log.read_text(encoding="utf-8", errors="replace")
    if code == 0:
        return {"name": name, "ergebnis": "grün", "dauer": dauer, "log": str(log)}
    # Befehl nicht vorhanden: Exit 127 der POSIX-Shell bzw. die Ausnahme von PowerShell – nicht jeder Text, der so klingt
    fehlt = code == 127 or (os.name == "nt" and "CommandNotFoundException" in text)
    letzte = "\n".join(text.strip().splitlines()[-20:])
    if code == -1:
        letzte = f"Zeitlimit {TIMEOUT} s überschritten" + (f"\n{letzte}" if letzte else "")
    return {"name": name, "ergebnis": "fehlt" if fehlt else "rot", "dauer": dauer, "exit": code, "log": str(log),
            "ausgabe": letzte}


def laufen(wurzel, profil, namen, dateien, immer=False, ordner=None, ohne_auswahl=False):
    """Wählt, überspringt und führt aus. Ergebnisliste in der Reihenfolge der Namen.

    `ohne_auswahl`: genannte Checks laufen auch ohne passende geänderte Datei (Nachweis für einen sauberen Stand).
    """
    ordner = ordner or tempfile.mkdtemp(prefix="checks-")
    merker_datei = merker_pfad(wurzel)
    merker = merker_lesen(merker_datei)
    ergebnisse, offen = {}, []
    for name in namen:
        check = profil["checks"].get(name)
        if check is None:
            ergebnisse[name] = {"name": name, "ergebnis": "unbekannt", "grund": "nicht unter ### Checks im Profil"}
            continue
        ausloeser = check["muster"] + check.get("eingaben", [])
        treffer = passende(dateien, ausloeser)
        if ausloeser and not treffer and not ohne_auswahl:
            ergebnisse[name] = {"name": name, "ergebnis": "übersprungen", "grund": "keine passende Datei"}
            continue
        eingaben = eingaben_stand(wurzel, check)
        abdruck = fingerabdruck(wurzel, check, treffer, eingaben)
        if not immer and gilt_noch(wurzel, merker.get(name), abdruck):
            ergebnisse[name] = {"name": name, "ergebnis": "schon grün", "grund": "seit dem letzten grünen Lauf unverändert"}
            continue
        offen.append((name, check, treffer))

    def stand(check, treffer):
        try:
            eingaben = eingaben_stand(wurzel, check)
            return {"abdruck": fingerabdruck(wurzel, check, treffer, eingaben), "eingaben": eingaben}
        except (OSError, ProfilFehler):
            return None

    def eins(eintrag):
        name, check, treffer = eintrag
        vorher = stand(check, treffer)  # erst jetzt: parallele Checks (z. B. Formatierer) sind schon durch
        start = jetzt()
        ergebnis = ausfuehren(name, check, wurzel, ordner)
        lauf = {"ergebnis": ergebnis, "start": start, "ende": jetzt()}
        if ergebnis["ergebnis"] == "grün":
            nachher = stand(check, treffer)
            lauf["abdruck_nachher"] = nachher and nachher["abdruck"]
        return name, check, vorher, lauf

    gemeinsam = [e for e in offen if not e[1]["allein"]]
    allein = [e for e in offen if e[1]["allein"]]
    fertig = []
    if gemeinsam:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(gemeinsam)) as pool:
            fertig += list(pool.map(eins, gemeinsam))
    fertig += [eins(e) for e in allein]
    for name, check, vorher, lauf in fertig:
        ergebnisse[name] = lauf["ergebnis"]
        if lauf["ergebnis"]["ergebnis"] == "grün" and vorher:
            merker[name] = datensatz(wurzel, name, check, vorher, lauf)
        else:
            merker.pop(name, None)
    if merker_datei and fertig:
        try:
            merker_datei.write_text(json.dumps({"schema": SCHEMA, "checks": merker}, indent=2, sort_keys=True,
                                               ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass
    return [ergebnisse[n] for n in namen]


def exit_code(ergebnisse):
    werte = {e["ergebnis"] for e in ergebnisse}
    if "rot" in werte or "unbekannt" in werte:
        return 1
    return 2 if "fehlt" in werte else 0


def tabelle(ergebnisse):
    zeilen = ["| Check | Dauer | Ergebnis |", "|---|---|---|"]
    for e in ergebnisse:
        dauer = f"{int(e['dauer'] // 60)}:{int(e['dauer'] % 60):02d}" if "dauer" in e else "–"
        text = e["ergebnis"] + (f" – {e['grund']}" if e.get("grund") else "")
        if e["ergebnis"] == "fehlt":
            text += " – Befehl auf diesem Rechner nicht vorhanden"
        zeilen.append(f"| {e['name']} | {dauer} | {text} |")
    for e in ergebnisse:
        if e.get("ausgabe"):
            zeilen += ["", f"{e['name']} ({e['ergebnis']}, Ausgabe {e['log']}):", e["ausgabe"]]
    return "\n".join(zeilen)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prüfläufe vor dem Commit nach dem Skill-Profil")
    wahl = parser.add_mutually_exclusive_group(required=True)
    wahl.add_argument("--vor-commit", action="store_true", help="die Pre-Commit-Checks des Profils")
    wahl.add_argument("--checks", help="Namen, durch Komma getrennt")
    parser.add_argument("--profil", help="CLAUDE.md (Standard: in der Repo-Wurzel)")
    parser.add_argument("--immer", action="store_true", help="auch Checks, die mit diesem Stand schon grün waren; mit --checks auch ohne passende geänderte Datei")
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON")
    args = parser.parse_args(argv)
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
        if r.returncode:
            raise ProfilFehler("kein git-Repo")
        wurzel = r.stdout.strip()
        profil_datei = Path(args.profil) if args.profil else Path(wurzel) / "CLAUDE.md"
        profil = profil_lesen(profil_datei.read_text(encoding="utf-8"))
        namen = profil["vor_commit"] if args.vor_commit else [n.strip() for n in args.checks.split(",") if n.strip()]
        dateien = geaendert(wurzel)
    except (OSError, ProfilFehler) as exc:
        print(json.dumps({"fehler": str(exc)}, ensure_ascii=False) if args.json else f"Fehler: {exc}")
        return 3
    ergebnisse = laufen(wurzel, profil, namen, dateien, immer=args.immer,
                        ohne_auswahl=bool(args.checks) and args.immer)
    code = exit_code(ergebnisse)
    if args.json:
        print(json.dumps({"ok": code == 0, "exit": code, "checks": ergebnisse}, ensure_ascii=False, indent=2))
    else:
        print(tabelle(ergebnisse) if ergebnisse else "Keine Pre-Commit-Checks im Profil.")
    return code


if __name__ == "__main__":
    sys.exit(main())
