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
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> EvonicDevice:
        try:
            device = await self.evonic.get_device()
        except EvonicError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error
        except Exception as error:
            raise UpdateFailed(f"Unexpected error communicating with Evonic device: {error}") from error

        return device
