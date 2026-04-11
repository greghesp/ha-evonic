"""Unofficial Evonic Fires Evoflame integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .const import DOMAIN, LOGGER
from .coordinator import EvonicCoordinator

PLATFORMS = (
    Platform.LIGHT,
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.NUMBER,
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Evoflame Fire from a config entry."""
    coordinator = EvonicCoordinator(hass, entry=entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]

    return unload_ok
