from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .coordinator import EvonicCoordinator
from .const import DOMAIN, LOGGER
from .models import EvonicEntity
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityFeature
)

PARALLEL_UPDATES = 1


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: EvonicCoordinator = hass.data[DOMAIN][entry.entry_id]

    create_supported_entities(coordinator, async_add_entities)


class EvonicFeatureLight(EvonicEntity, LightEntity):
    """ Defined the Feature Light """

    _attr_icon = "mdi:led-strip-variant"
    _attr_name = "Feature Light"

    def __init__(self, coordinator: EvonicCoordinator) -> None:
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_featurelight"

    @property
    def available(self) -> bool:
        if self.coordinator.data.info.on:
            return True
        return False

    @property
    def is_on(self) -> bool:
        """Return the state of the switch"""
        if not self.coordinator.data.info.on:
            return False
        return bool(self.coordinator.data.light.feature_light)

    async def async_turn_off(self) -> None:
        """ Turn off the power"""
        await self.coordinator.evonic.toggle_feature_light()

    async def async_turn_on(self) -> None:
        """ Turn on the power"""
        await self.coordinator.evonic.toggle_feature_light()


class EvonicFireLight(EvonicEntity, LightEntity):
    """ Define the Fire Light.  This is the fire 'power', as it must always be on, if the Heater is on"""

    def __init__(self, coordinator: EvonicCoordinator) -> None:
        super().__init__(coordinator=coordinator)

        self._attr_support_color_modes: set[ColorMode] = set()
        self._attr_support_color_modes.add(ColorMode.ONOFF)
        self._attr_icon = "mdi:led-strip-variant"
        self._attr_name = "Fire Lighting"
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_fire_light"

    @property
    def is_on(self) -> bool:
        """Return the state of the light"""
        return bool(self.coordinator.data.info.on)

    @property
    def effect(self) -> str | None:
        """ Returns the current effect """
        return self.coordinator.data.light.effect

    @property
    def effect_list(self) -> list[str]:
        """ Return a list of supported effects """

        # Sometimes available_effects is None
        # TODO: Figure this out ^
        if not type(self.coordinator.data.effects.available_effects):
            return ["Eos"]
        return self.coordinator.data.effects.available_effects

    async def async_turn_off(self) -> None:
        """ Turn off the power"""
        await self.coordinator.evonic.power("off")

    async def async_turn_on(self, **kwargs) -> None:
        """ Turn on the power"""
        await self.coordinator.evonic.power("on")

        if ATTR_EFFECT in kwargs:
            await self.coordinator.evonic.set_effect(kwargs[ATTR_EFFECT])


@callback
def create_supported_entities(
        coordinator: EvonicCoordinator,
        async_add_entities: AddEntitiesCallback
) -> None:
    supported_features = coordinator.data.info.modules
    entities_to_add: list = [EvonicFireLight(coordinator)]

    if "light_box" in supported_features:
        entities_to_add.append(EvonicFeatureLight(coordinator))

    async_add_entities(entities_to_add)
