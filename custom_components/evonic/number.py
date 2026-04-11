from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import UnitOfTemperature

from .coordinator import EvonicCoordinator
from .const import DOMAIN, CONF_TEMP_OFFSET
from .models import EvonicEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: EvonicCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([EvonicTemperatureOffset(coordinator)])


class EvonicTemperatureOffset(EvonicEntity, NumberEntity):
    """A number entity that lets the user apply a temperature offset.

    The offset is stored in config entry options so it survives restarts.
    When changed, all coordinator entities are signalled to re-render
    immediately so the climate entity reflects the new value without
    waiting for the next poll cycle.
    """

    _attr_name = "Offset"
    _attr_icon = "mdi:thermometer-check"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_native_min_value = -10
    _attr_native_max_value = 10
    _attr_native_step = 1
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: EvonicCoordinator) -> None:
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_temp_offset"

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit matching the device's temperature setting."""
        if self.coordinator.data.climate.fahrenheit:
            return UnitOfTemperature.FAHRENHEIT
        return UnitOfTemperature.CELSIUS

    @property
    def native_value(self) -> float:
        """Return the current offset from config entry options."""
        return float(self.coordinator.config_entry.options.get(CONF_TEMP_OFFSET, 0))

    async def async_set_native_value(self, value: float) -> None:
        """Persist the new offset, recalculate the device setpoint, and update all entities."""
        new_offset = int(value)

        # Re-send the target temperature with the new offset applied so the
        # device setpoint stays consistent with the user's intended HA target.
        target_temp = self.coordinator.data.climate.target_temp
        if isinstance(target_temp, int):
            fahrenheit = self.coordinator.data.climate.fahrenheit
            # Convert device target (always Celsius) to the display unit
            ha_target = round(target_temp * 9 / 5 + 32) if fahrenheit else target_temp
            # Apply new offset and convert back to Celsius for the device
            device_target = ha_target - new_offset
            if fahrenheit:
                device_target = round((device_target - 32) * 5 / 9)
            await self.coordinator.evonic.set_temperature(device_target)

        self.hass.config_entries.async_update_entry(
            self.coordinator.config_entry,
            options={
                **self.coordinator.config_entry.options,
                CONF_TEMP_OFFSET: new_offset,
            },
        )
        # Signal all coordinator-backed entities (including the climate entity)
        # to re-read their state with the new offset, without a full API poll.
        self.coordinator.async_update_listeners()
