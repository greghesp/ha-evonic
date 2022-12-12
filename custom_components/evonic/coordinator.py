import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyevonic import Device as EvonicDevice, Evonic, EvonicConnectionClosed, EvonicError

from .const import DOMAIN, LOGGER, SCAN_INTERVAL


class EvonicCoordinator(DataUpdateCoordinator[EvonicDevice]):
    """Class to manage fetching Evonic data."""
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, *, entry: ConfigEntry) -> None:
        self.evonic = Evonic(
            entry.data[CONF_HOST], session=async_get_clientsession(hass)
        )
        self.unsub: CALLBACK_TYPE | None = None
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    @callback
    def use_websocket(self) -> None:
        async def listen() -> None:
            """Listen for state changes via WebSocket."""
            try:
                await self.evonic.connect()
            except EvonicError as err:
                self.logger.info(err)
                if self.unsub:
                    self.unsub()
                    self.unsub = None
                return

            try:
                await self.evonic.listen(callback=self.async_set_updated_data)
            except EvonicConnectionClosed as err:
                self.last_update_success = False
                self.logger.info(err)
            except EvonicError as err:
                self.last_update_success = False
                self.async_update_listerners()
                self.logger.error(err)

            await self.evonic.disconnect()
            if self.unsub:
                self.unsub()
                self.unsub = None

        async def close_websocket(_: Event) -> None:
            """Close WebSocket connection."""
            self.unsub = None
            await self.evonic.disconnect()

        # Clean disconnect WebSocket on Home Assistant shutdown
        self.unsub = self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, close_websocket
        )

        asyncio.create_task(listen())

    async def _async_update_data(self) -> EvonicDevice:
        """Fetch data from Evonic."""
        try:
            device = await self.evonic.get_device()
            LOGGER.debug(device.__dict__)
        except EvonicError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error

        if not self.evonic.connected and not self.unsub:
            self.use_websocket()

        return device