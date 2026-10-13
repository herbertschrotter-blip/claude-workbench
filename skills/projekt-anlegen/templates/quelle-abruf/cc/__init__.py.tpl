"""Integration einrichten und entladen."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .api import Client
from .const import CONF_ADRESSE, DOMAIN
from .coordinator import Abruf
from .tickets import meldungen
from .tickets import registrieren as tickets_registrieren

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATTFORMEN = [Platform.SENSOR]


@dataclass
class Laufzeit:
    """Was die Integration zur Laufzeit braucht (entry.runtime_data)."""

    abruf: Abruf

    def diagnose(self) -> dict[str, Any]:
        return {
            "adresse": self.abruf.client.adresse,
            "daten": self.abruf.data,
            "letzter_abruf_ok": self.abruf.last_update_success,
        }


type EintragMitLaufzeit = ConfigEntry[Laufzeit]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Tickets (Aktion {{package}}.ticket, WebSocket für eine eigene Seite) einmal je HA-Start anmelden."""
    tickets_registrieren(hass)
    # lesbare Kopie beim Start
    hass.async_create_task(meldungen(hass).async_laden(), f"{DOMAIN}_meldungen_laden")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: EintragMitLaufzeit) -> bool:
    abruf = Abruf(hass, entry, Client(entry.data[CONF_ADRESSE]))
    await abruf.async_config_entry_first_refresh()
    entry.runtime_data = Laufzeit(abruf=abruf)
    await hass.config_entries.async_forward_entry_setups(entry, PLATTFORMEN)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: EintragMitLaufzeit) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATTFORMEN)
