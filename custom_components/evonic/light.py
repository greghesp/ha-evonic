from __future__ import annotations

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .coordinator import EvonicCoordinator
from .const import DOMAIN
from .models import EvonicEntity
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: EvonicCoordinator = hass.data[DOMAIN][entry.entry_id]

    create_supported_entities(coordinator, async_add_entities)


class EvonicFeatureLight(EvonicEntity, LightEntity):
    """Defined the Feature Light"""

    _attr_icon = "mdi:led-strip-variant"
    _attr_name = "Feature Light"
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(self, coordinator: EvonicCoordinator) -> None:
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_featurelight"

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data.info.on)

    @property
    def is_on(self) -> bool:
        """Return the state of the switch"""
        if not self.coordinator.data.info.on:
            return False
        return bool(self.coordinator.data.light.feature_light)

    async def async_turn_off(self) -> None:
        """Turn off the power"""
        if self.is_on:
            await self.coordinator.evonic.toggle_feature_light()
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self) -> None:
        """Turn on the power"""
        if not self.is_on:
            await self.coordinator.evonic.toggle_feature_light()
        await self.coordinator.async_request_refresh()


class EvonicFireLight(EvonicEntity, LightEntity):
    """Define the Fire Light.  This is the fire 'power', as it must always be on, if the Heater is on"""

    def __init__(self, coordinator: EvonicCoordinator) -> None:
        super().__init__(coordinator=coordinator)

        self._attr_color_mode = ColorMode.ONOFF
        self._attr_supported_color_modes = {ColorMode.ONOFF}
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
        """Returns the current effect"""
        return self.coordinator.data.light.effect

    @property
    def effect_list(self) -> list[str]:
        """Return a list of supported effects"""

        if not self.coordinator.data.effects.available_effects:
            return ["Eos"]
        return self.coordinator.data.effects.available_effects

    async def async_turn_off(self) -> None:
        """Turn off the power"""
        await self.coordinator.evonic.power("off")
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the power"""
        if not self.is_on:
            await self.coordinator.evonic.power("on")

        if ATTR_EFFECT in kwargs:
            await self.coordinator.evonic.set_effect(kwargs[ATTR_EFFECT])
            self.async_write_ha_state()

        await self.coordinator.async_request_refresh()


_ZONE_CONFIG = {
    "flame": {
        "name": "Flame Light",
        "icon": "mdi:fire",
        "brightness_attr": "flame_brightness",
        "effect_attr": "flame_effect",
        "effects_attr": "flame_effects",
        "zone_param": "flame",
        "module_key": "rgb0",
    },
    "top": {
        "name": "Log Light",
        "icon": "mdi:pine-tree",
        "brightness_attr": "top_brightness",
        "effect_attr": "top_effect",
        "effects_attr": "top_effects",
        "zone_param": "top",
        "module_key": "rgb1",
    },
    "ember": {
        "name": "FuelBed Light",
        "icon": "mdi:fireplace",
        "brightness_attr": "ember_brightness",
        "effect_attr": "ember_effect",
        "effects_attr": "ember_effects",
        "zone_param": "ember",
        "module_key": "rgb2",
    },
}


class EvonicZoneLight(EvonicEntity, LightEntity):
    """Per-zone lighting control (Flame, Log, or FuelBed)."""

    _attr_color_mode = ColorMode.RGB
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_supported_features = LightEntityFeature.EFFECT

    def __init__(self, coordinator: EvonicCoordinator, zone: str) -> None:
        super().__init__(coordinator=coordinator)
        cfg = _ZONE_CONFIG[zone]
        self._zone = zone
        self._zone_param = cfg["zone_param"]
        self._brightness_attr = cfg["brightness_attr"]
        self._effect_attr = cfg["effect_attr"]
        self._effects_attr = cfg["effects_attr"]
        self._color_attr = f"{cfg['zone_param']}_color"
        self._effect_prefix = f"{cfg['zone_param'].capitalize()}_"
        self._attr_name = cfg["name"]
        self._attr_icon = cfg["icon"]
        self._attr_unique_id = f"{coordinator.data.info.ssdp}_{zone}_zone_light"

    @staticmethod
    def _display_effect(name: str) -> str:
        """Map internal effect names to display names."""
        return "Colour" if name == "Color" else name

    @staticmethod
    def _internal_effect(name: str) -> str:
        """Map display names back to internal effect names."""
        return "Color" if name == "Colour" else name

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data.info.on)

    @property
    def brightness(self) -> int | None:
        return getattr(self.coordinator.data.light, self._brightness_attr, None)

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        hex_color = getattr(self.coordinator.data.light, self._color_attr, None)
        if not hex_color or len(hex_color) < 6:
            return None
        try:
            return (
                int(hex_color[0:2], 16),
                int(hex_color[2:4], 16),
                int(hex_color[4:6], 16),
            )
        except ValueError:
            return None

    @property
    def is_on(self) -> bool:
        if not self.coordinator.data.info.on:
            return False
        b = self.brightness
        return b is not None and b > 0

    @property
    def effect(self) -> str | None:
        raw = getattr(self.coordinator.data.light, self._effect_attr, None)
        if raw and raw.startswith(self._effect_prefix):
            return self._display_effect(raw[len(self._effect_prefix):])
        return raw

    @property
    def effect_list(self) -> list[str] | None:
        effects = getattr(self.coordinator.data.effects, self._effects_attr, None)
        if not effects:
            return None
        return [
            self._display_effect(
                e[len(self._effect_prefix):] if e.startswith(self._effect_prefix) else e
            )
            for e in effects
        ]

    async def async_turn_on(self, **kwargs) -> None:
        current_effect = getattr(self.coordinator.data.light, self._effect_attr, None)

        if ATTR_RGB_COLOR in kwargs:
            r, g, b = kwargs[ATTR_RGB_COLOR]
            hex_color = f"{r:02x}{g:02x}{b:02x}"
            await self.coordinator.evonic.set_zone_color(self._zone_param, hex_color)
            current_effect = f"{self._effect_prefix}Color"

        if ATTR_EFFECT in kwargs:
            internal = self._internal_effect(kwargs[ATTR_EFFECT])
            full_effect = f"{self._effect_prefix}{internal}"
            await self.coordinator.evonic.set_zone_effect(full_effect)
            current_effect = full_effect

        if ATTR_BRIGHTNESS in kwargs:
            await self.coordinator.evonic.set_zone_brightness(
                self._zone_param, kwargs[ATTR_BRIGHTNESS], current_effect
            )
        elif ATTR_EFFECT not in kwargs and ATTR_RGB_COLOR not in kwargs:
            await self.coordinator.evonic.set_zone_brightness(
                self._zone_param, 255, current_effect
            )

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        current_effect = getattr(self.coordinator.data.light, self._effect_attr, None)
        await self.coordinator.evonic.set_zone_brightness(
            self._zone_param, 0, current_effect
        )
        await self.coordinator.async_request_refresh()


@callback
def create_supported_entities(
    coordinator: EvonicCoordinator, async_add_entities: AddEntitiesCallback
) -> None:
    supported_features = coordinator.data.info.modules
    entities_to_add: list = [EvonicFireLight(coordinator)]

    if supported_features:
        if "light_box" in supported_features:
            entities_to_add.append(EvonicFeatureLight(coordinator))

        for zone, cfg in _ZONE_CONFIG.items():
            if cfg["module_key"] in supported_features:
                entities_to_add.append(EvonicZoneLight(coordinator, zone))

    async_add_entities(entities_to_add)
