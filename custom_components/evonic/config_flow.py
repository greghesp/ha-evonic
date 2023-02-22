from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, data_entry_flow
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .pyevonic import Evonic, EvonicConnectionError
from homeassistant.components import ssdp
from pprint import pformat
import homeassistant.helpers.config_validation as cv
from yarl import URL
from homeassistant.const import (
    CONF_HOST
)

from .const import DOMAIN, LOGGER


def _schema_with_defaults(host=""):
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=host): str
        },
        extra=vol.ALLOW_EXTRA,
    )


class EvonicConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle Evonic config flow"""

    VERSION = 1

    def __init__(self) -> None:
        """Handle a config flow for Evonic."""
        self.discovery_schema = None
        self._user_input = None

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user step."""
        errors = {}

        if user_input is None and self._user_input:
            user_input = self._user_input

        if user_input is None:
            data = self.discovery_schema or _schema_with_defaults()
            return self.async_show_form(step_id="user", data_schema=data)

        if user_input is not None:
            try:
                device = await self._async_get_device(user_input[CONF_HOST])
            except EvonicConnectionError:
                errors["base"] = "cannot_connect"
            else:
                LOGGER.debug(f"User Input Exists, Flash Chip ID: {device.info.flashChip}")
                await self.async_set_unique_id(device.info.flashChip)
                self._abort_if_unique_id_configured(
                    updates={CONF_HOST: user_input[CONF_HOST]}
                )
                return self.async_create_entry(
                    title=device.info.ssdp, data={CONF_HOST: user_input[CONF_HOST]}
                )
        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors or {},
        )

    async def _async_get_device(self, host):
        session = async_get_clientsession(self.hass)
        evonic = Evonic(host, session=session)
        return await evonic.get_device()

    async def async_step_ssdp(
            self, discovery_info: ssdp.SsdpServiceInfo
    ) -> data_entry_flow.FlowResult:
        """Handle ssdp discovery flow."""
        LOGGER.debug("Evonic SSDP discovery %s", pformat(discovery_info))

        host = discovery_info.ssdp_location
        serial = discovery_info.upnp["serialNumber"]
        url = URL(host)

        LOGGER.debug("Evonic SSDP host %s", host)
        LOGGER.debug("Evonic SSDP serial %s", serial)

        await self.async_set_unique_id(serial)
        self._abort_if_unique_id_configured(updates={CONF_HOST: url.host})
        LOGGER.debug("Evonic Serial not unique")

        LOGGER.debug("Evonic SSDP url %s", url.host)

        self.context.update(
            {
                "configuration_url": url.host,
            }
        )

        self.discovery_schema = _schema_with_defaults(
            host=url.host,
        )

        return await self.async_step_user()
