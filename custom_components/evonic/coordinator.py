import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .pyevonic import Device as EvonicDevice, Evonic, EvonicConnectionClosed, EvonicError

from .const import DOMAIN, LOGGER, SCAN_INTERVAL


class EvonicCoordinator(DataUpdateCoordinator[EvonicDevice]):
    config_entry: ConfigEntry

    def __init__(self, hass, *, entry):
        self.evonic = Evonic(
            entry.data[CONF_HOST], session=async_get_clientsession(hass)
        )
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> EvonicDevice:
        try:
            device = await self.evonic.get_device()
            LOGGER.debug(device.__dict__)
        except EvonicError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error

        return device
