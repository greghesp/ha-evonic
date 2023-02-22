import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .pyevonic import Device as EvonicDevice, Evonic, EvonicConnectionClosed, EvonicError

from .const import DOMAIN, LOGGER, SCAN_INTERVAL


class EvonicCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Evonic data."""
    config_entry: ConfigEntry

    def __init__(self, hass, *, entry: ConfigEntry) -> None:
        self.evonic = Evonic(
            entry.data[CONF_HOST], session=async_get_clientsession(hass)
        )
        self.hass = hass
        self.use_websocket()
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    @callback
    def use_websocket(self) -> None:
        async def listen() -> None:
            """Listen for state changes via WebSocket."""
            try:
                self.logger.debug("Connecting to websocket")
                await self.evonic.connect()
            except EvonicError as err:
                self.logger.error(err)
                return

            try:
                self.logger.debug("Listening to websocket")
                await self.evonic.listen(callback=self.async_set_updated_data)
            except EvonicConnectionClosed as err:
                self.last_update_success = False
                self.logger.error(err)
            except EvonicError as err:
                self.last_update_success = False
                self.async_update_listeners()
                self.logger.error(err)

        async def close_websocket(_: Event) -> None:
            """Close WebSocket connection."""
            LOGGER.debug("Calling close_websocket")
            await self.evonic.disconnect()

        # Clean disconnect WebSocket on Home Assistant shutdown
        self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, close_websocket
        )

        asyncio.create_task(listen())

    async def _async_update_data(self) -> EvonicDevice:
        """Fetch data from Evonic."""

        self.logger.debug("Calling _async_update_data")

        try:
            device = await self.evonic.get_device()
            self.logger.debug(f"Got device data successfully: {device.__dict__}")
        except EvonicError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error
        return device
