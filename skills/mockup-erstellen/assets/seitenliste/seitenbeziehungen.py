"""Sucht aus dem Code, welche Seite welche öffnet, und schreibt es als `zu` und `nutzt` in die Quelldatei.

Aufruf: python3 tools/seitenbeziehungen.py, danach python3 tools/seitenliste.py. Die Suchmuster stehen in
tools/seitenliste.config.json unter `beziehungen`: `einstieg` (Seite → Funktion oder „datei:*“), `ziel` (Muster → Seiten),
`hand` (Wege, die der Code nicht zeigt), `bausteine` (Name → Seiten). Das Ergebnis ist eine Näherung, keine Garantie.
"""

from __future__ import annotations

import re

import seitenliste as sl


def funktionen(cfg: dict, b: dict) -> tuple[dict[str, str], dict[str, str]]:
    """Name → Text je Top-Level-Funktion; Dateiname → ganzer Text."""
    kopf = re.compile(b["kopf"], re.M)
    aus: dict[str, str] = {}
    texte: dict[str, str] = {}
    for f in sorted(x for x in (sl.WURZEL / cfg["code_wurzel"]).rglob(b.get("dateien", "*")) if x.is_file()):
        t = f.read_text(encoding="utf8")
        texte[f.name] = t
        treffer = list(kopf.finditer(t))
        for i, m in enumerate(treffer):
            ende = treffer[i + 1].start() if i + 1 < len(treffer) else len(t)
            aus.setdefault(next(x for x in m.groups() if x), t[m.start() : ende])
    return aus, texte


def text_von(root: str, fn: dict[str, str], texte: dict[str, str], wurzeln: set[str]) -> str:
    """Text der Funktion samt der Hilfsfunktionen, die sie nutzt (zwei Stufen, ohne andere Seiten)."""
    if root.endswith(":*"):
        return texte[root[:-2]]
    teile, gesehen, offen = [], {root}, [root]
    for _ in range(3):
        neu = []
        for n in offen:
            t = fn.get(n, "")
            teile.append(t)
            for w in set(re.findall(r"\b([a-zA-Z_]\w+)\(", t)) - gesehen - wurzeln:
                if w in fn:
                    gesehen.add(w)
                    neu.append(w)
        offen = neu
    return "\n".join(teile)


def sortiert(nummern: set[str]) -> list[str]:
    return sorted(nummern, key=lambda x: [int(y) for y in x.split(".")])


def main() -> None:
    cfg = sl.config()
    b = cfg["beziehungen"]
    fn, texte = funktionen(cfg, b)
    wurzeln = {n for x in b["einstieg"].values() for n in x}
    fehlt = sorted(n for n in wurzeln if not n.endswith(":*") and n not in fn)
    if fehlt:
        print("nicht gefunden:", ", ".join(fehlt))
    gruppen = sl.lesen(cfg)
    alle = [s for g in gruppen for s in g["seiten"]]
    for s in alle:
        t = "\n".join(text_von(r, fn, texte, wurzeln) for r in b["einstieg"].get(s["nr"], []))
        zu = {z for m, ziele in b["ziel"].items() if re.search(m, t) for z in ziele}
        zu |= set(b["hand"].get(s["nr"], []))
        zu.discard(s["nr"])
        s["zu"] = sortiert(zu)
        s["nutzt"] = [k for k, v in b["bausteine"].items() if s["nr"] in v]
    sl.schreiben(cfg, gruppen)
    print(sum(len(s["zu"]) for s in alle), "Verbindungen,", sum(1 for s in alle if not s["zu"]), "Seiten ohne Ziel")


if __name__ == "__main__":
    main()
