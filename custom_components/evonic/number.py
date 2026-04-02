from __future__ import annotations

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.number import NumberEntity, NumberMode

from .coordinator import EvonicCoordinator
from .const import DOMAIN
from .models import EvonicEntity

PARALLEL_UPDATES = 1

_ZONE_NAMES = {
    "flame": "Flame",
    "top": "Log",
    "ember": "FuelBed",
}

_ZONE_MODULE_KEYS = {
    "flame": "rgb0",
    "top": "rgb1",
    "ember": "rgb2",
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: EvonicCoordinator = hass.data[DOMAIN][entry.entry_id]
    create_supported_entities(coordinator, async_add_entities)


class EvonicZoneStrength(EvonicEntity, NumberEntity):
    """Speed/strength control for a lighting zone."""

    _attr_native_min_value = 0
    _attr_native_max_value = 240
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:speedometer"

    def __init__(self, coordinator: EvonicCoordinator, zone: str) -> None:
        super().__init__(coordinator=coordinator)
        self._zone_param = zone
        self._speed_attr = f"{zone}_speed"
        self._effect_attr = f"{zone}_effect"
        self._attr_name = f"{_ZONE_NAMES[zone]} Strength"
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_{zone}_strength"

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data.info.on)

    @property
    def native_value(self) -> float | None:
        val = getattr(self.coordinator.data.light, self._speed_attr, None)
        return float(val) if val is not None else None

    async def async_set_native_value(self, value: float) -> None:
        current_effect = getattr(self.coordinator.data.light, self._effect_attr, None)
        await self.coordinator.evonic.set_zone_speed(
            self._zone_param, int(value), current_effect
        )
        await self.coordinator.async_request_refresh()


class EvonicFlameMotorSpeed(EvonicEntity, NumberEntity):
    """Motor speed control for the flame zone."""

    _attr_native_min_value = 0
    _attr_native_max_value = 1023
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:engine"
    _attr_name = "Flame Motor Speed"

    def __init__(self, coordinator: EvonicCoordinator) -> None:
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_flame_motor_speed"

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data.info.on)

    @property
    def native_value(self) -> float | None:
        val = self.coordinator.data.light.flame_motor_speed
        return float(val) if val is not None else None

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.evonic.set_flame_motor_speed(int(value))
        await self.coordinator.async_request_refresh()


@callback
def create_supported_entities(
    coordinator: EvonicCoordinator, async_add_entities: AddEntitiesCallback
) -> None:
    supported_features = coordinator.data.info.modules
    entities_to_add: list = []

    if supported_features:
        for zone, module_key in _ZONE_MODULE_KEYS.items():
            if module_key in supported_features:
                entities_to_add.append(EvonicZoneStrength(coordinator, zone))

        if "step0" in supported_features:
            entities_to_add.append(EvonicFlameMotorSpeed(coordinator))

    if entities_to_add:
        async_add_entities(entities_to_add)
