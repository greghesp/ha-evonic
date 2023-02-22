from __future__ import annotations

from typing import Any

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import datetime as dt
from homeassistant.helpers.typing import StateType

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .coordinator import EvonicCoordinator
from .const import DOMAIN, LOGGER
from .models import EvonicEntity
from .pyevonic import Device as EvonicDevice
from homeassistant.const import (
    POWER_WATT,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)


@dataclass
class EvonicSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[EvonicDevice], datetime | StateType]


@dataclass
class EvonicSensorEntityDescription(
    SensorEntityDescription, EvonicSensorEntityDescriptionMixin
):
    """Describes Evonic sensor entity."""

    exists_fn: Callable[[EvonicDevice], bool] = lambda _: True


SENSORS: tuple[EvonicSensorEntityDescription, ...] = (
    EvonicSensorEntityDescription(
        key="wifi_signal",
        name="Wi-Fi Signal",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.network.signal_strength
    ),
    EvonicSensorEntityDescription(
        key="current_heater_usage",
        name="Heater Usage",
        native_unit_of_measurement=POWER_WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.info.heater_power if device.climate.heating else 0,
    ),
    EvonicSensorEntityDescription(
        key="current_led_usage",
        name="LED Usage",
        native_unit_of_measurement=POWER_WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.info.led_power if device.info.on else 0,
    ),
    EvonicSensorEntityDescription(
        key="current_total_usage",
        name="Total Usage",
        native_unit_of_measurement=POWER_WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: (device.info.led_power if device.info.on else 0) + (
            device.info.heater_power if device.climate.heating else 0),
    ),
    EvonicSensorEntityDescription(
        key="cost_per_hour",
        name="Cost per Hour",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: calculate_cost(device)
    ),
    EvonicSensorEntityDescription(
        key="cost_per_kwh",
        name="Cost per kWh",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.MONETARY,
        value_fn=lambda device: device.info.cost if device.info.cost else 0,
    ),
    EvonicSensorEntityDescription(
        key="last_ping",
        name="Last Ping",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda device: get_timestamp(device.info.last_ping),
    ),
)


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Evonic sensor based on a config entry."""
    coordinator: EvonicCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        EvonicSensorEntity(coordinator, description)
        for description in SENSORS
        if description.exists_fn(coordinator.data)
    )


def calculate_cost(device):
    if device.climate.heating:
        watt = device.info.heater_power + device.info.led_power
        calc = watt / 1000 * device.info.cost
        return round(calc, 3)
    elif device.info.on:
        watt = device.info.led_power
        calc = watt / 1000 * device.info.cost
        return round(calc, 3)
    else:
        return 0


def get_timestamp(time):
    if time is None:
        return dt.datetime.now().astimezone()

    datetime_object = dt.datetime.strptime(time, '%H:%M:%S')
    return dt.datetime.combine(date=dt.date.today(), time=datetime_object.time(), tzinfo=dt.datetime.now().astimezone().tzinfo)

class EvonicSensorEntity(EvonicEntity, SensorEntity):
    """Defines a Evonic sensor entity."""

    entity_description: EvonicSensorEntityDescription

    def __init__(
            self,
            coordinator: EvonicCoordinator,
            description: EvonicSensorEntityDescription,
    ) -> None:
        """Initialize a Evonic sensor entity."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.network.mac}_{description.key}"

    @property
    def native_value(self) -> datetime | StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
