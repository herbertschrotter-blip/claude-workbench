"""Tickets aus dem Melden-Knopf (Muster ha-netzwerk): speichern, lesbar ablegen, über WebSocket und Dienst ändern.

Quelle ist der Integrations-Speicher (Store `{{package}}.meldungen`, eine Liste für die ganze Integration, auch ohne
geladene Einrichtung). Bei jeder Änderung schreibt die Integration die Liste lesbar nach `<config>/{{package}}/`
(`meldungen.json`, `meldungen.md`, Bilder unter `meldungen/`), damit Claude sie ohne Zugriff auf `.storage/` lesen
kann. Geändert wird nur über die Befehle hier: die Seite (melden, Bild dazu, schließen, löschen) und den Dienst
`{{package}}.ticket` für `tools/ticket.py`. Die Meldungen enthalten nur, was im Melde-Dialog steht – keine Zugangsdaten.
"""

from __future__ import annotations

import asyncio
import base64
import copy
import json
import logging
import os
import uuid
from typing import Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
    callback,
)
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util
from homeassistant.util.file import write_utf8_file

from .const import DOMAIN
from .logik import tickets as tk

LOGGER = logging.getLogger(__package__)
DATA = f"{DOMAIN}_meldungen"
ORDNER = DOMAIN  # <config>/{{package}}
BILDER = "meldungen"  # <config>/{{package}}/meldungen/FE-0001-1.jpg
VERZOEGERUNG_S = 2


class Meldungen:
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._store: Store[dict[str, Any]] = Store(hass, 1, f"{DOMAIN}.meldungen")
        self.liste: list[dict[str, Any]] = []
        self.nummern: dict[str, int] = {}
        self._geladen = False
        self._laden = (
            asyncio.Lock()
        )  # nur einmal laden, auch wenn Start und Seite gleichzeitig fragen
        self._ablage = (
            asyncio.Lock()
        )  # Ablage nacheinander; jede schreibt den Stand bei ihrem Beginn
        self.ordner = hass.config.path(ORDNER)

    async def async_laden(self) -> list[dict[str, Any]]:
        async with self._laden:
            if not self._geladen:
                daten = (await self._store.async_load()) or {}
                self.liste = list(daten.get("meldungen") or [])
                self.nummern = {k: int(v) for k, v in (daten.get("nummern") or {}).items()}
                self._geladen = True
                self.hass.async_create_task(self.async_ablegen(), f"{DOMAIN}_meldungen_ablegen")
        return self.liste

    def speichern(self) -> None:
        self._store.async_delay_save(
            lambda: {"meldungen": self.liste, "nummern": self.nummern}, VERZOEGERUNG_S
        )
        self.hass.async_create_task(self.async_ablegen(), f"{DOMAIN}_meldungen_ablegen")

    async def async_ablegen(self) -> None:
        """Lesbare Fassung nach <config>/{{package}}/ (im Hintergrund-Thread). Nacheinander: die zuletzt begonnene Ablage
        schreibt den neuesten Stand, eine ältere kann ihn nicht mehr überschreiben."""
        async with self._ablage:
            stand = dt_util.now().isoformat(timespec="seconds")
            await self.hass.async_add_executor_job(
                _ablegen, self.ordner, copy.deepcopy(self.liste), stand
            )

    async def async_neu(self, roh: dict[str, Any]) -> dict[str, Any]:
        await self.async_laden()
        m = tk.meldung_pruefen(roh)
        m.update(
            id=uuid.uuid4().hex[:12],
            ticket=tk.neue_nummer(self.nummern, m["art"]),
            zeit=dt_util.now().isoformat(timespec="seconds"),
            status="neu",
            stand=None,
            bilder=[],
            verlauf=[],
        )
        self.liste.insert(0, m)
        self.speichern()
        return m

    async def async_bild(self, m: dict[str, Any], url: str) -> str:
        """Bild zu einer frischen Meldung als Datei ablegen; gibt den Dateinamen zurück."""
        grund = tk.bild_erlaubt(m, dt_util.now().timestamp(), _sekunden(m.get("zeit")))
        if grund:
            raise tk.Ungueltig(grund)
        endung, roh = tk.bild_lesen(url)
        bilder = m.setdefault("bilder", [])
        name = tk.bild_name(m["ticket"], len(bilder) + 1, endung)
        bilder.append(
            name
        )  # Platz belegen, bevor geschrieben wird: zwei Bilder zugleich bekommen zwei Namen
        try:
            await self.hass.async_add_executor_job(_bild_schreiben, self.ordner, name, roh)
        except OSError:
            bilder.remove(name)
            raise
        self.speichern()
        return name

    async def async_bild_url(self, m: dict[str, Any], nr: int) -> str | None:
        namen = m.get("bilder") or []
        if not 0 <= nr < len(namen):
            return None
        return await self.hass.async_add_executor_job(_bild_url, self.ordner, namen[nr])

    async def async_loeschen(self, m: dict[str, Any]) -> None:
        self.liste.remove(m)
        await self.hass.async_add_executor_job(_bilder_loeschen, self.ordner, m.get("bilder") or [])
        self.speichern()

    def aendern(self, m: dict[str, Any], **kw: Any) -> None:
        tk.aendern(m, dt_util.now().isoformat(timespec="seconds"), **kw)
        self.speichern()


def _sekunden(zeit: Any) -> float:
    t = dt_util.parse_datetime(str(zeit or ""))
    return t.timestamp() if t else 0.0


def _ablegen(ordner: str, liste: list[dict[str, Any]], stand: str) -> None:
    os.makedirs(ordner, exist_ok=True)
    write_utf8_file(
        os.path.join(ordner, "meldungen.json"),
        json.dumps(liste, ensure_ascii=False, indent=2) + "\n",
    )
    text = tk.markdown(liste, stand, f"{ORDNER}/{BILDER}").replace("<domain>", DOMAIN)
    write_utf8_file(os.path.join(ordner, "meldungen.md"), text + "\n")


def _bild_schreiben(ordner: str, name: str, roh: bytes) -> None:
    ziel = os.path.join(ordner, BILDER)
    os.makedirs(ziel, exist_ok=True)
    with open(os.path.join(ziel, os.path.basename(name)), "wb") as f:
        f.write(roh)


def _bild_url(ordner: str, name: str) -> str | None:
    art = next((k for k, v in tk.BILD_ARTEN.items() if name.endswith("." + v)), "image/jpeg")
    try:
        with open(os.path.join(ordner, BILDER, os.path.basename(name)), "rb") as f:
            return f"data:{art};base64," + base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


def _bilder_loeschen(ordner: str, namen: list[str]) -> None:
    for name in namen:
        try:
            os.remove(os.path.join(ordner, BILDER, os.path.basename(name)))
        except FileNotFoundError:
            pass


def meldungen(hass: HomeAssistant) -> Meldungen:
    if DATA not in hass.data:
        hass.data[DATA] = Meldungen(hass)
    m: Meldungen = hass.data[DATA]
    return m


# ---------------------------------------------------------------------- WebSocket (Seite)
def _ticket(
    connection: websocket_api.ActiveConnection, msg: dict[str, Any], liste: list[dict[str, Any]]
) -> dict[str, Any] | None:
    m = tk.finden(liste, msg["meldung_id"])
    if m is None:
        connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "Meldung nicht gefunden")
    return m


@websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/meldungen"})
@websocket_api.async_response
async def _liste(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """Alle Meldungen, neueste zuerst."""
    liste = await meldungen(hass).async_laden()
    connection.send_result(msg["id"], [tk.fuer_seite(m) for m in liste])


@websocket_api.websocket_command(
    {vol.Required("type"): f"{DOMAIN}/meldung/neu", vol.Required("meldung"): dict}
)
@websocket_api.async_response
async def _neu(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """Neue Meldung (jeder angemeldete Benutzer); Bilder kommen danach einzeln mit meldung/bild."""
    try:
        m = await meldungen(hass).async_neu(msg["meldung"])
    except tk.Ungueltig as err:
        connection.send_error(msg["id"], "ungueltig", str(err))
        return
    connection.send_result(msg["id"], {"id": m["id"], "ticket": m["ticket"]})


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/meldung/bild",
        vol.Required("meldung_id"): str,
        vol.Required("bild"): vol.All(str, vol.Length(max=tk.BILD_MAX_BYTES * 4 // 3 + 64)),
    }
)
@websocket_api.async_response
async def _bild(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """Ein Bild zur gerade gesendeten Meldung; die Antwort nennt, wie viele Bilder angekommen sind."""
    ml = meldungen(hass)
    if (m := _ticket(connection, msg, await ml.async_laden())) is None:
        return
    try:
        await ml.async_bild(m, msg["bild"])
    except tk.Ungueltig as err:
        connection.send_error(msg["id"], "ungueltig", str(err))
        return
    except OSError as err:
        connection.send_error(
            msg["id"], "nicht_gespeichert", f"Bild nicht gespeichert: {err.strerror or err}"
        )
        return
    connection.send_result(msg["id"], {"ticket": m["ticket"], "bilder": len(m["bilder"])})


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/meldung/bild_zeigen",
        vol.Required("meldung_id"): str,
        vol.Required("nr"): vol.All(int, vol.Range(min=0, max=tk.BILDER_MAX - 1)),
    }
)
@websocket_api.async_response
async def _bild_zeigen(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """Bild zur Anzeige auf der Seite – nur über die Verbindung, nicht öffentlich unter /local."""
    ml = meldungen(hass)
    if (m := _ticket(connection, msg, await ml.async_laden())) is None:
        return
    url = await ml.async_bild_url(m, msg["nr"])
    if url is None:
        connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "Bild nicht gefunden")
        return
    connection.send_result(msg["id"], {"url": url})


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/meldung/status",
        vol.Required("meldung_id"): str,
        vol.Required("status"): vol.In(tk.STATUS),
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def _status(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """Schließen oder wieder öffnen auf der Seite (nur Admins)."""
    ml = meldungen(hass)
    if (m := _ticket(connection, msg, await ml.async_laden())) is None:
        return
    ml.aendern(m, status=msg["status"], von="Seite")
    connection.send_result(msg["id"], tk.fuer_seite(m))


@websocket_api.websocket_command(
    {vol.Required("type"): f"{DOMAIN}/meldung/loeschen", vol.Required("meldung_id"): str}
)
@websocket_api.require_admin
@websocket_api.async_response
async def _loeschen(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    ml = meldungen(hass)
    if (m := _ticket(connection, msg, await ml.async_laden())) is None:
        return
    await ml.async_loeschen(m)
    connection.send_result(msg["id"], {"ok": True})


BEFEHLE = (_liste, _neu, _bild, _bild_zeigen, _status, _loeschen)

# ---------------------------------------------------------------------- Dienst (tools/ticket.py)
DIENST = vol.Schema(
    {
        vol.Required("ticket"): cv.string,
        vol.Optional("status"): vol.In(tk.STATUS),
        vol.Optional("notiz"): vol.All(cv.string, vol.Length(max=tk.TEXT_MAX)),
        vol.Optional("version"): vol.All(cv.string, vol.Length(max=50)),
        vol.Optional("commit"): vol.All(cv.string, vol.Length(max=80)),
        vol.Optional("von"): vol.All(cv.string, vol.Length(max=50)),
    }
)


@callback
def registrieren(hass: HomeAssistant) -> None:
    for befehl in BEFEHLE:
        websocket_api.async_register_command(hass, befehl)

    async def ticket(call: ServiceCall) -> ServiceResponse:
        """Ticket ändern (Status, Notiz, Version, Commit) – für die Bearbeitung in Claude Code."""
        ml = meldungen(hass)
        m = tk.finden(await ml.async_laden(), call.data["ticket"])
        if m is None:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="ticket_fehlt",
                translation_placeholders={"ticket": call.data["ticket"]},
            )
        try:
            ml.aendern(
                m,
                status=call.data.get("status"),
                notiz=call.data.get("notiz"),
                version=call.data.get("version"),
                commit=call.data.get("commit"),
                von=call.data.get("von") or "Claude",
            )
        except tk.Ungueltig as err:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="ticket_ungueltig",
                translation_placeholders={"grund": str(err)},
            ) from err
        return {
            "ticket": m["ticket"],
            "status": m["status"],
            "status_text": tk.STATUS_TEXT.get(m["status"], m["status"]),
        }

    async_register_admin_service(
        hass, DOMAIN, "ticket", ticket, schema=DIENST, supports_response=SupportsResponse.OPTIONAL
    )
