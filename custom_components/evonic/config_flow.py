from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .pyevonic import Evonic, EvonicConnectionError

from .const import DOMAIN, LOGGER


class EvonicConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle Evonic config flow"""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user step."""
        errors = {}

        if user_input is not None:
            try:
                device = await self._async_get_device(user_input[CONF_HOST])
            except EvonicConnectionError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(device.info.ssdp)
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
        await evonic.get_config()
        return await evonic.get_device()