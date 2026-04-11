"""Diagnostics support for Evonic."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

MODULES_REDACT = {"mail"}

OPTIONS_REDACT = {"token", "server", "ip"}

SETUP_REDACT = {"ssid", "ssidPass", "ip", "subnet", "getway", "mail", "pass", "ssidAP", "ssidApPass"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    evonic = coordinator.evonic

    async def fetch_json(uri: str) -> dict:
        try:
            response = await evonic.http_request(uri, "GET", None)
            return await response.json(content_type=None)
        except Exception as err:
            return {"error": str(err)}

    modules = await fetch_json("/modules.json")
    admin = await fetch_json("/config.admin.json")
    live = await fetch_json("/config.live.json")
    options = await fetch_json("/config.options.json")
    setup = await fetch_json("/config.setup.json")

    return {
        "modules": async_redact_data(modules, MODULES_REDACT),
        "config_admin": admin,
        "config_live": live,
        "config_options": async_redact_data(options, OPTIONS_REDACT),
        "config_setup": async_redact_data(setup, SETUP_REDACT),
    }
