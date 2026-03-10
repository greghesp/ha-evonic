from __future__ import annotations

import asyncio
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

    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return EvonicOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            if not host:
                errors["base"] = "invalid_host"
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
                    errors=errors or {},
                )
            try:
                device = await self._async_get_device(host)
            except (EvonicConnectionError, OSError, asyncio.TimeoutError):
                errors["base"] = "cannot_connect"
            except Exception:
                LOGGER.exception("Unexpected error connecting to Evonic host")
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(device.info.ssdp)
                self._abort_if_unique_id_configured(
                    updates={CONF_HOST: host}
                )
                return self.async_create_entry(
                    title=device.info.ssdp, data={CONF_HOST: host}
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


class EvonicOptionsFlow(OptionsFlow):
    """Handle Evonic options flow."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors = {}

        if user_input is not None:
            new_host = user_input[CONF_HOST].strip()
            if not new_host:
                errors["base"] = "invalid_host"
            else:
                existing_host = self.config_entry.data.get(CONF_HOST, "")
                if new_host != existing_host:
                    # Validate the new host by attempting to connect
                    try:
                        session = async_get_clientsession(self.hass)
                        evonic = Evonic(new_host, session=session)
                        await evonic.get_config()
                    except (EvonicConnectionError, OSError, asyncio.TimeoutError):
                        errors["base"] = "cannot_connect"
                    except Exception:
                        LOGGER.exception("Unexpected error validating Evonic host")
                        errors["base"] = "cannot_connect"
                    else:
                        # Update the config entry data with the new host
                        self.hass.config_entries.async_update_entry(
                            self.config_entry,
                            data={**self.config_entry.data, CONF_HOST: new_host},
                        )
                        await self.hass.config_entries.async_reload(
                            self.config_entry.entry_id
                        )
                        return self.async_create_entry(title="", data={})
                else:
                    return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=self.config_entry.data.get(CONF_HOST, ""),
                    ): str,
                }
            ),
            errors=errors,
        )
