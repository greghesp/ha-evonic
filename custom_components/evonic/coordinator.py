import asyncio
import json

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .pyevonic import Device as EvonicDevice, Evonic, EvonicError

from .const import DOMAIN, LOGGER, SCAN_INTERVAL


class EvonicCoordinator(DataUpdateCoordinator[EvonicDevice]):
    config_entry: ConfigEntry

    def __init__(self, hass, *, entry):
        self.evonic = Evonic(
            entry.data[CONF_HOST], session=async_get_clientsession(hass)
        )
        self._ws_task: asyncio.Task | None = None
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> EvonicDevice:
        try:
            device = await self.evonic.get_device()
        except EvonicError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error
        except Exception as error:
            raise UpdateFailed(f"Unexpected error communicating with Evonic device: {error}") from error

        self._ensure_ws_listener()
        return device

    def _ensure_ws_listener(self):
        """Start the WebSocket listener if not already running."""
        if self._ws_task is None or self._ws_task.done():
            self._ws_task = self.hass.async_create_task(self._ws_listener())

    async def _ws_listener(self):
        """Background task: listen for real-time state pushes over WebSocket."""
        while True:
            try:
                await self.evonic._ws_connect()
                LOGGER.debug("WebSocket listener active on %s:81", self.evonic.host)
                await self.evonic._ws_send("cmd", "get modules")
                await self.evonic._ws_send("cmd", "get effectList")

                while self.evonic._ws is not None and not self.evonic._ws.closed:
                    msg = await self.evonic._ws.receive()

                    if msg.type == aiohttp.WSMsgType.TEXT:
                        try:
                            data = json.loads(msg.data)
                            if self.data is not None:
                                self.data.update_from_dict(data)
                                self.async_set_updated_data(self.data)
                        except json.JSONDecodeError:
                            pass
                    elif msg.type in (
                        aiohttp.WSMsgType.CLOSED,
                        aiohttp.WSMsgType.ERROR,
                        aiohttp.WSMsgType.CLOSING,
                    ):
                        LOGGER.debug("WebSocket disconnected, will reconnect")
                        self.evonic._ws = None
                        break

            except asyncio.CancelledError:
                raise
            except Exception as err:
                LOGGER.debug("WebSocket listener error: %s", err)
                self.evonic._ws = None

            await asyncio.sleep(5)

    def stop_ws_listener(self):
        """Cancel the WebSocket listener task."""
        if self._ws_task is not None and not self._ws_task.done():
            self._ws_task.cancel()
