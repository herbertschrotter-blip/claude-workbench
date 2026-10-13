"""Tickets aus dem Melden-Knopf: Nummern, Prüfung, Bilder, Status, lesbare Fassung."""

import base64

import pytest
from logik import tickets as tk

JPEG = "data:image/jpeg;base64," + base64.b64encode(b"\xff\xd8\xff\xe0bild").decode()


def test_nummern_je_art_ab_0001():
    n: dict[str, int] = {}
    assert [tk.neue_nummer(n, a) for a in ("fehler", "wunsch", "fehler", "anregung")] == [
        "FE-0001",
        "WU-0001",
        "FE-0002",
        "AN-0001",
    ]
    assert n == {"FE": 2, "WU": 1, "AN": 1}


def test_meldung_pruefen():
    m = tk.meldung_pruefen(
        {
            "art": "wunsch",
            "text": "  mehr Farbe ",
            "kontext": "Funk",
            "seite": {"reiter": "funk", "x": None},
            "zuviel": 1,
        }
    )
    assert (
        m["text"] == "mehr Farbe"
        and m["seite"] == {"reiter": "funk", "x": None}
        and "zuviel" not in m
    )
    with pytest.raises(tk.Ungueltig, match="art"):
        tk.meldung_pruefen({"art": "lob", "text": "x"})
    with pytest.raises(tk.Ungueltig, match="beschreiben"):
        tk.meldung_pruefen({"art": "fehler", "text": "   "})
    with pytest.raises(tk.Ungueltig, match="höchstens"):
        tk.meldung_pruefen({"art": "fehler", "text": "x" * (tk.TEXT_MAX + 1)})
    with pytest.raises(tk.Ungueltig, match="seite"):
        tk.meldung_pruefen({"art": "fehler", "text": "x", "seite": {"a": {"tief": 1}}})


def test_bild_lesen():
    assert tk.bild_lesen(JPEG) == ("jpg", b"\xff\xd8\xff\xe0bild")
    for falsch in (
        "data:image/gif;base64,AAAA",
        "data:image/jpeg,AAAA",
        "data:image/jpeg;base64,***",
        5,
    ):
        with pytest.raises(tk.Ungueltig):
            tk.bild_lesen(falsch)
    gross = "data:image/png;base64," + base64.b64encode(b"x" * (tk.BILD_MAX_BYTES + 1)).decode()
    with pytest.raises(tk.Ungueltig, match="zu groß"):
        tk.bild_lesen(gross)


def test_bild_erlaubt_nur_frisch_und_hoechstens_drei():
    assert tk.bild_erlaubt({"bilder": []}, 1000, 900) is None
    assert "höchstens" in (tk.bild_erlaubt({"bilder": ["a", "b", "c"]}, 1000, 900) or "")
    assert "direkt" in (tk.bild_erlaubt({}, 1000 + tk.BILD_FRIST_S, 999) or "")


def test_aendern_haelt_verlauf_fest():
    m: dict = {"status": "neu"}
    tk.aendern(
        m,
        "2026-10-13T20:00:00",
        status="geschlossen",
        version="0.10.0",
        commit="abc",
        notiz="behoben",
        von="Claude",
    )
    assert m["status"] == "geschlossen" and m["stand"] == "2026-10-13T20:00:00"
    assert m["verlauf"] == [
        {
            "zeit": "2026-10-13T20:00:00",
            "von": "Claude",
            "status": "geschlossen",
            "version": "0.10.0",
            "commit": "abc",
            "notiz": "behoben",
        }
    ]
    tk.aendern(m, "2026-10-13T21:00:00", notiz="nur Notiz")
    assert m["status"] == "geschlossen" and len(m["verlauf"]) == 2
    with pytest.raises(tk.Ungueltig):
        tk.aendern(m, "x", status="erledigt")
    with pytest.raises(tk.Ungueltig, match="nichts"):
        tk.aendern(m, "x", von="Claude")
    assert len(m["verlauf"]) == 2 and not tk.offen(m)
    s = tk.fuer_seite(m | {"art": "wunsch"})
    assert (s["offen"], s["art_text"], s["status_text"]) == (False, "Wunsch", "geschlossen")


def test_finden_und_markdown():
    liste = [
        {
            "id": "a1",
            "ticket": "FE-0001",
            "art": "fehler",
            "status": "neu",
            "zeit": "2026-10-13T19:42:00",
            "text": "Karte grau",
            "kontext": "Funk",
            "bilder": ["FE-0001-1.jpg"],
            "verlauf": [],
        },
        {
            "id": "b2",
            "ticket": "WU-0001",
            "art": "wunsch",
            "status": "geschlossen",
            "zeit": "2026-10-12T10:00:00",
            "text": "mehr",
            "verlauf": [
                {
                    "zeit": "2026-10-13T08:00:00",
                    "von": "Claude",
                    "status": "geschlossen",
                    "version": "0.9.1",
                    "commit": "abc",
                }
            ],
        },
    ]
    assert (
        tk.finden(liste, "fe-0001") is liste[0]
        and tk.finden(liste, "b2") is liste[1]
        and tk.finden(liste, "X") is None
    )
    md = tk.markdown(liste, "2026-10-13T20:00:00", "{{package}}/meldungen")
    assert "offen: 1 · erledigt: 1" in md
    assert (
        md.index("## Offen") < md.index("FE-0001") < md.index("## Erledigt") < md.index("WU-0001")
    )
    assert "- Bilder: {{package}}/meldungen/FE-0001-1.jpg" in md
    assert "(Claude): geschlossen · v0.9.1 · Commit abc" in md
