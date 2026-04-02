from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import logging

LOGGER = logging.getLogger(__name__)


@dataclass
class Network:
    ip: str
    subnet: str
    ssidAP: str
    signal_strength: str
    mac: str

    @staticmethod
    def from_dict(data):
        return Network(
            ip=data.get('ip'),
            subnet=data.get('subnet'),
            ssidAP=data.get('ssidAP'),
            signal_strength=data.get('dbm'),
            mac=data.get("mac")
        )

    def update_from_dict(self, data):
        self.ip = data.get('ip', self.ip)
        self.subnet = data.get('subnet', self.subnet)
        self.ssidAP = data.get('ssidAP', self.ssidAP)
        self.signal_strength = data.get('dbm', self.signal_strength)
        self.mac = data.get('mac', self.mac)


@dataclass
class Info:
    on: Any
    ssdp: str | None
    ssidAP: str | None
    configs: str | None
    product: str | None
    buildData: str | None
    last_ping: str | None
    modules: list
    email: str | None
    cost: float
    heater_power: int
    led_power: int
    flashChip: str | None

    @staticmethod
    def from_dict(data):
        return Info(
            on=data.get("Fire"),
            ssdp=data.get("SSDP"),
            ssidAP=data.get('ssidAP'),
            configs=data.get('configs'),
            product=data.get('product'),
            buildData=data.get('buildData'),
            last_ping=data.get('time'),
            modules=data.get('module'),
            email=data.get('mail'),
            cost=float(data.get('cost') or 0),
            heater_power=to_int(data.get('powerHeater')),
            led_power=to_int(data.get('powerLed')),
            flashChip=data.get('flashChip'),
        )

    def update_from_dict(self, data):
        fire_val = data.get("Fire", data.get("fire"))
        if fire_val is not None:
            self.on = to_int(fire_val)
        self.ssdp = data.get('SSDP', self.ssdp)
        self.ssidAP = data.get('ssidAP', self.ssidAP)
        self.configs = data.get('configs', self.configs)
        self.product = data.get('product', self.product)
        self.buildData = data.get('buildData', self.buildData)
        self.last_ping = data.get('time', self.last_ping)
        self.modules = data.get('module', self.modules)
        self.email = data.get('mail', self.email)
        if isinstance(data.get('cost'), str):
            self.cost = float(0)
        else:
            self.cost = float(data.get('cost', self.cost))
        self.heater_power = to_int(data.get('powerHeater', self.heater_power))
        self.led_power = to_int(data.get('powerLed', self.led_power))
        self.flashChip = data.get('flashChip', self.flashChip)


@dataclass
class Climate:
    current_temp: int
    target_temp: int
    heating: Any
    fahrenheit: int

    @staticmethod
    def from_dict(data):
        return Climate(
            current_temp=to_int(data.get("temperature")),
            target_temp=to_int(data.get('templevel')),
            heating=data.get("Heater"),
            fahrenheit=to_int(data.get("fahrenheit")),
        )

    def update_from_dict(self, data):
        self.current_temp = to_int(data.get("temperature", self.current_temp))
        self.target_temp = to_int(data.get("templevel", self.target_temp))
        heater_val = data.get("Heater", data.get("heater"))
        if heater_val is not None:
            self.heating = to_int(heater_val)
        self.fahrenheit = to_int(data.get('fahrenheit', self.fahrenheit))


@dataclass
class Effects:
    available_effects: list | None
    flame_effects: list | None
    top_effects: list | None
    ember_effects: list | None

    @staticmethod
    def from_dict(data):
        return Effects(
            available_effects=data.get('available_effects'),
            flame_effects=data.get('flameList'),
            top_effects=data.get('topList'),
            ember_effects=data.get('emberList'),
        )

    def update_from_dict(self, data):
        self.available_effects = data.get('available_effects', self.available_effects)
        if 'flameList' in data:
            self.flame_effects = data['flameList']
        if 'topList' in data:
            self.top_effects = data['topList']
        if 'emberList' in data:
            self.ember_effects = data['emberList']


@dataclass
class Light:
    effect: str | None
    feature_light: Any
    flame_brightness: int
    flame_speed: int
    flame_effect: str | None
    flame_color: str | None
    top_brightness: int
    top_speed: int
    top_effect: str | None
    top_color: str | None
    ember_brightness: int
    ember_speed: int
    ember_effect: str | None
    ember_color: str | None
    flame_motor_speed: int

    @staticmethod
    def from_dict(data):
        return Light(
            effect=data.get("effect"),
            feature_light=data.get("pinout3"),
            flame_brightness=to_int(data.get("brightnessRGB0") or data.get("flameBrightness")),
            flame_speed=to_int(data.get("speedRGB0") or data.get("flameSpeed")),
            flame_effect=data.get("flame"),
            flame_color=data.get("flameColor"),
            top_brightness=to_int(data.get("brightnessRGB1") or data.get("topBrightness")),
            top_speed=to_int(data.get("speedRGB1") or data.get("topSpeed")),
            top_effect=data.get("top"),
            top_color=data.get("topColor"),
            ember_brightness=to_int(data.get("emberBrightness")),
            ember_speed=to_int(data.get("emberSpeed")),
            ember_effect=data.get("ember"),
            ember_color=data.get("emberColor"),
            flame_motor_speed=to_int(data.get("flameMotorSpeed")),
        )

    def update_from_dict(self, data):
        self.effect = data.get("effect", self.effect)
        self.feature_light = data.get("pinout3", self.feature_light)
        if "brightnessRGB0" in data:
            self.flame_brightness = to_int(data["brightnessRGB0"])
        if "flameBrightness" in data:
            self.flame_brightness = to_int(data["flameBrightness"])
        if "speedRGB0" in data:
            self.flame_speed = to_int(data["speedRGB0"])
        if "flameSpeed" in data:
            self.flame_speed = to_int(data["flameSpeed"])
        if "flame" in data:
            self.flame_effect = data["flame"]
        if "flameColor" in data:
            self.flame_color = data["flameColor"]
        if "brightnessRGB1" in data:
            self.top_brightness = to_int(data["brightnessRGB1"])
        if "topBrightness" in data:
            self.top_brightness = to_int(data["topBrightness"])
        if "speedRGB1" in data:
            self.top_speed = to_int(data["speedRGB1"])
        if "topSpeed" in data:
            self.top_speed = to_int(data["topSpeed"])
        if "top" in data:
            self.top_effect = data["top"]
        if "topColor" in data:
            self.top_color = data["topColor"]
        if "emberBrightness" in data:
            self.ember_brightness = to_int(data["emberBrightness"])
        if "emberSpeed" in data:
            self.ember_speed = to_int(data["emberSpeed"])
        if "ember" in data:
            self.ember_effect = data["ember"]
        if "emberColor" in data:
            self.ember_color = data["emberColor"]
        if "flameMotorSpeed" in data:
            self.flame_motor_speed = to_int(data["flameMotorSpeed"])


class Device:
    def __init__(self, data):
        self.info = Info.from_dict(data)
        self.climate = Climate.from_dict(data)
        self.network = Network.from_dict(data)
        self.light = Light.from_dict(data)
        self.effects = Effects.from_dict(data)

    def update_from_dict(self, data):
        self.info.update_from_dict(data)
        self.climate.update_from_dict(data)
        self.network.update_from_dict(data)
        self.light.update_from_dict(data)
        self.effects.update_from_dict(data)
        return self


def to_int(value) -> int:
    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        return int(value)
    else:
        return 0