from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS, TEMP_FAHRENHEIT
from .coordinator import EvonicCoordinator
from .const import DOMAIN, LOGGER
from .models import EvonicEntity
from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature
)
from homeassistant.components.climate.const import (
    FAN_ON,
    FAN_OFF,
    HVACMode
)

PARALLEL_UPDATES = 1


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: EvonicCoordinator = hass.data[DOMAIN][entry.entry_id]
    create_supported_entities(coordinator, async_add_entities)


class EvonicHeater(EvonicEntity, ClimateEntity):
    """ Defined the Climate Heater """

    _attr_name = "Heater"

    def __init__(self, coordinator: EvonicCoordinator) -> None:
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_heater"
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
        if self.coordinator.data.climate.fahrenheit:
            self._attr_temperature_unit = TEMP_FAHRENHEIT
        else:
            self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_hvac_modes = [
            HVACMode.HEAT,
            HVACMode.OFF
        ]

    # HVAC Control

    @property
    def hvac_mode(self) -> HVACMode:
        """ Return hvac operation"""
        if self.coordinator.data.climate.heating:
            return HVACMode.HEAT
        else:
            return HVACMode.OFF

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """ Set new hvac mode """
        if hvac_mode not in self._attr_hvac_modes:
            raise ValueError(f"Unsupported HVAC mode: {hvac_mode}")

        if hvac_mode == HVACMode.HEAT:
            await self.coordinator.evonic.heater_power("on")
        if hvac_mode == HVACMode.OFF:
            await self.coordinator.evonic.heater_power("off")

        await self.coordinator.async_request_refresh()

    @property
    def current_temperature(self) -> float:
        """ Return the current temperature"""
        if not isinstance(self.coordinator.data.climate.current_temp, int):
            return 0
        return float(self.coordinator.data.climate.current_temp)

    @property
    def target_temperature(self) -> float | None:
        """ Return the target temperature"""
        if not isinstance(self.coordinator.data.climate.target_temp, int):
            return 0
        return float(self.coordinator.data.climate.target_temp)

    async def async_set_temperature(self, **kwargs) -> None:
        """ Set new target temperature"""
        if ATTR_TEMPERATURE not in kwargs:
            raise ValueError(f"Expected attribute {ATTR_TEMPERATURE}")

        await self.coordinator.evonic.set_temperature(round(kwargs[ATTR_TEMPERATURE]))
        await self.coordinator.async_request_refresh()

@callback
def create_supported_entities(
        coordinator: EvonicCoordinator,
        async_add_entities: AddEntitiesCallback
) -> None:
    supported_features = coordinator.data.info.modules
    entities_to_add: list = []

    if "temperature" in supported_features:
        entities_to_add.append(EvonicHeater(coordinator))

    async_add_entities(entities_to_add)