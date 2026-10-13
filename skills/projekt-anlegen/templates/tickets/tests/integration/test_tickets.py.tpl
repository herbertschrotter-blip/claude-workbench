"""Tickets über den ganzen Weg: Seite meldet (mit Bild) → Datei liegt unter <config>/{{package}}/ → tools/ticket.py findet
Ticket und Bild → Dienst {{package}}.ticket ändert den Status → Seite sieht ihn. Geht auch ohne geladene Einrichtung."""

import base64
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.{{package}}.const import DOMAIN as D
from custom_components.{{package}}.logik import tickets as tk


@pytest.fixture(autouse=True)
def eigener_ordner(hass, tmp_path):
    """Eigene HA-Konfiguration je Test: Ablage und Bilder liegen nur dort."""
    hass.config.config_dir = str(tmp_path)
    return tmp_path


BILD = b"\xff\xd8\xff\xe0screenshot"
URL = "data:image/jpeg;base64," + base64.b64encode(BILD).decode()
WERKZEUG = Path(__file__).parents[2] / "tools" / "ticket.py"


async def _start(hass: HomeAssistant) -> None:
    assert await async_setup_component(hass, D, {})
    await hass.async_block_till_done()


async def _ws(client, **msg):
    await client.send_json_auto_id(msg)
    return await client.receive_json()


async def test_melden_mit_bild_ganzer_weg(hass, hass_ws_client, eigener_ordner):
    await _start(hass)
    client = await hass_ws_client(hass)
    neu = await _ws(
        client,
        type=f"{D}/meldung/neu",
        meldung={
            "art": "fehler",
            "text": "Karte grau",
            "kontext": "Funk · Mobilfunk",
            "geraet": "Handy",
            "version": "0.10.0",
            "seite": {"reiter": "funk"},
        },
    )
    assert neu["success"], neu
    assert neu["result"]["ticket"] == "FE-0001"
    bild = await _ws(client, type=f"{D}/meldung/bild", meldung_id=neu["result"]["id"], bild=URL)
    assert bild["success"] and bild["result"] == {"ticket": "FE-0001", "bilder": 1}
    await hass.async_block_till_done()

    ordner = eigener_ordner / D
    assert (ordner / "meldungen" / "FE-0001-1.jpg").read_bytes() == BILD
    gespeichert = json.loads((ordner / "meldungen.json").read_text(encoding="utf-8"))
    assert gespeichert[0]["bilder"] == ["FE-0001-1.jpg"] and gespeichert[0]["status"] == "neu"
    assert f"{D}/meldungen/FE-0001-1.jpg" in (ordner / "meldungen.md").read_text(encoding="utf-8")

    # Claude liest das Ticket mit dem Werkzeug und findet das Bild
    aus = subprocess.run(
        [sys.executable, str(WERKZEUG), "zeige", "fe-0001"],
        env={**os.environ, "HA_CONFIG": str(eigener_ordner)},
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "Karte grau" in aus and f"bild: {ordner / 'meldungen' / 'FE-0001-1.jpg'}" in aus

    zeigen = await _ws(client, type=f"{D}/meldung/bild_zeigen", meldung_id="FE-0001", nr=0)
    assert zeigen["result"]["url"] == URL

    # Dienst wie tools/ticket.py status … --version --commit --notiz
    antwort = await hass.services.async_call(
        D,
        "ticket",
        {
            "ticket": "FE-0001",
            "status": "geschlossen",
            "version": "0.10.0",
            "commit": "abc1234",
            "notiz": "behoben",
        },
        blocking=True,
        return_response=True,
    )
    assert antwort == {"ticket": "FE-0001", "status": "geschlossen", "status_text": "geschlossen"}
    liste = (await _ws(client, type=f"{D}/meldungen"))["result"]
    assert liste[0]["status"] == "geschlossen" and liste[0]["verlauf"][-1]["commit"] == "abc1234"


async def test_bild_grenzen_und_fehler(hass, hass_ws_client):
    await _start(hass)
    client = await hass_ws_client(hass)
    mid = (await _ws(client, type=f"{D}/meldung/neu", meldung={"art": "wunsch", "text": "x"}))[
        "result"
    ]["id"]
    falsch = await _ws(
        client, type=f"{D}/meldung/bild", meldung_id=mid, bild="data:image/gif;base64,AAAA"
    )
    assert not falsch["success"] and falsch["error"]["code"] == "ungueltig"
    for _ in range(tk.BILDER_MAX):
        assert (await _ws(client, type=f"{D}/meldung/bild", meldung_id=mid, bild=URL))["success"]
    vierte = await _ws(client, type=f"{D}/meldung/bild", meldung_id=mid, bild=URL)
    assert not vierte["success"] and "höchstens" in vierte["error"]["message"]
    leer = await _ws(client, type=f"{D}/meldung/neu", meldung={"art": "fehler", "text": " "})
    assert not leer["success"] and leer["error"]["code"] == "ungueltig"
    weg = await _ws(client, type=f"{D}/meldung/bild", meldung_id="WU-9999", bild=URL)
    assert weg["error"]["code"] == "not_found"


async def test_schliessen_und_loeschen_nur_admin(
    hass, hass_ws_client, hass_read_only_access_token, eigener_ordner
):
    await _start(hass)
    gast = await hass_ws_client(hass, hass_read_only_access_token)
    neu = await _ws(gast, type=f"{D}/meldung/neu", meldung={"art": "anregung", "text": "Idee"})
    assert neu["success"]  # melden darf jeder
    mid = neu["result"]["id"]
    assert (await _ws(gast, type=f"{D}/meldung/bild", meldung_id=mid, bild=URL))["success"]
    assert (await _ws(gast, type=f"{D}/meldung/status", meldung_id=mid, status="geschlossen"))[
        "error"
    ]["code"] == "unauthorized"
    assert (await _ws(gast, type=f"{D}/meldung/loeschen", meldung_id=mid))["error"][
        "code"
    ] == "unauthorized"

    admin = await hass_ws_client(hass)
    st = await _ws(admin, type=f"{D}/meldung/status", meldung_id=mid, status="geschlossen")
    assert st["success"] and st["result"]["verlauf"][-1]["von"] == "Seite"
    assert (await _ws(admin, type=f"{D}/meldung/loeschen", meldung_id=mid))["success"]
    await hass.async_block_till_done()
    assert not (eigener_ordner / D / "meldungen" / "AN-0001-1.jpg").exists()
    assert json.loads((eigener_ordner / D / "meldungen.json").read_text(encoding="utf-8")) == []


async def test_dienst_unbekanntes_ticket(hass):
    await _start(hass)
    import pytest
    from homeassistant.exceptions import ServiceValidationError

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            D, "ticket", {"ticket": "FE-0042", "notiz": "x"}, blocking=True
        )


async def test_zwei_bilder_gleichzeitig_zwei_dateien(hass, hass_ws_client, eigener_ordner):
    import asyncio

    from custom_components.{{package}}.tickets import meldungen

    await _start(hass)
    ml = meldungen(hass)
    m = await ml.async_neu({"art": "fehler", "text": "x"})
    namen = await asyncio.gather(ml.async_bild(m, URL), ml.async_bild(m, URL))
    assert sorted(namen) == ["FE-0001-1.jpg", "FE-0001-2.jpg"] and m["bilder"] == namen
    assert all((eigener_ordner / D / "meldungen" / n).exists() for n in namen)


async def test_liste_fuer_seite_und_leere_aenderung(hass, hass_ws_client):
    import pytest
    from homeassistant.exceptions import ServiceValidationError

    await _start(hass)
    client = await hass_ws_client(hass)
    await _ws(client, type=f"{D}/meldung/neu", meldung={"art": "wunsch", "text": "x"})
    m = (await _ws(client, type=f"{D}/meldungen"))["result"][0]
    assert (m["offen"], m["art_text"], m["status_text"]) == (True, "Wunsch", "neu")
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(D, "ticket", {"ticket": "WU-0001"}, blocking=True)


def test_werkzeug_verworfen_braucht_grund(tmp_path):
    (tmp_path / D).mkdir()
    (tmp_path / D / "meldungen.json").write_text(
        json.dumps([{"ticket": "FE-0001", "status": "neu", "art": "fehler", "text": "x"}]),
        encoding="utf-8",
    )
    lauf = subprocess.run(
        [sys.executable, str(WERKZEUG), "status", "FE-0001", "verworfen"],
        env={**os.environ, "HA_CONFIG": str(tmp_path), "SUPERVISOR_TOKEN": ""},
        capture_output=True,
        text=True,
    )
    assert lauf.returncode != 0 and "Grund" in lauf.stderr
    liste = subprocess.run(
        [sys.executable, str(WERKZEUG), "liste"],
        env={**os.environ, "HA_CONFIG": str(tmp_path)},
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "FE-0001" in liste and "neu" in liste
