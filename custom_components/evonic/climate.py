from __future__ import annotations

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import UnitOfTemperature
from .coordinator import EvonicCoordinator
from .const import DOMAIN
from .models import EvonicEntity
from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature
)
from homeassistant.components.climate.const import HVACMode

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
        self._attr_hvac_modes = [
            HVACMode.HEAT,
            HVACMode.OFF
        ]
        self._update_temperature_unit()

    @callback
    def _handle_coordinator_update(self) -> None:
        self._update_temperature_unit()
        super()._handle_coordinator_update()

    def _update_temperature_unit(self) -> None:
        if self.coordinator.data.climate.fahrenheit:
            self._attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
            self._attr_min_temp = 50.0
            self._attr_max_temp = 90.0
        else:
            self._attr_temperature_unit = UnitOfTemperature.CELSIUS
            self._attr_min_temp = 11.0
            self._attr_max_temp = 32.0

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
    def current_temperature(self) -> float | None:
        """Return the current temperature in the device's unit."""
        if not isinstance(self.coordinator.data.climate.current_temp, int):
            return None
        return float(self.coordinator.data.climate.current_temp)

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature in the device's unit.
        The device always stores the target in Celsius, so convert to
        Fahrenheit when the device is in Fahrenheit mode."""
        if not isinstance(self.coordinator.data.climate.target_temp, int):
            return None
        temp = float(self.coordinator.data.climate.target_temp)
        if self.coordinator.data.climate.fahrenheit:
            return round(temp * 9 / 5 + 32, 1)
        return temp

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature. HA sends in the entity's declared unit,
        but the device always expects Celsius for the setpoint."""
        if "temperature" not in kwargs:
            raise ValueError(f"Expected attribute 'temperature'")

        temp = round(kwargs["temperature"])
        if self.coordinator.data.climate.fahrenheit:
            temp = round((temp - 32) * 5 / 9)

        await self.coordinator.evonic.set_temperature(temp)
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