from dataclasses import dataclass
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
    on: str
    ssdp: str
    ssidAP: str
    configs: str
    product: str
    buildData: str
    last_ping: str
    modules: []
    email: str
    cost: float
    heater_power: int
    led_power: int
    flashChip: str

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
            cost=float(data.get('cost', 0)),
            heater_power=to_int(data.get('powerHeater')),
            led_power=to_int(data.get('powerLed')),
            flashChip=data.get('flashChip'),
        )

    def update_from_dict(self, data):
        self.on = data.get("Fire", self.on)
        self.ssdp = data.get('SSDP', self.ssdp)
        self.ssidAP = data.get('ssidAP', self.ssidAP)
        self.configs = data.get('configs', self.configs)
        self.product = data.get('product', self.product)
        self.buildData = data.get('buildData', self.buildData)
        self.last_ping = data.get('time', self.last_ping)
        self.modules = data.get('module', self.modules)
        self.email = data.get('mail', self.email)
        self.cost = float(data.get('cost', self.cost))
        self.heater_power = to_int(data.get('powerHeater', self.heater_power))
        self.led_power = to_int(data.get('powerLed', self.led_power))
        self.flashChip = data.get('flashChip', self.flashChip)


@dataclass
class Climate:
    current_temp: int
    target_temp: int
    heating: bool
    fahrenheit: bool

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
        self.heating = data.get('Heater', self.heating)
        self.fahrenheit = to_int(data.get('fahrenheit', self.fahrenheit))


@dataclass
class Effect:
    name: str


@dataclass
class Effects:
    available_effects: []

    @staticmethod
    def from_dict(data):
        return Effects(
            available_effects=data.get('available_effects')
        )

    def update_from_dict(self, data):
        self.available_effects = data.get('available_effects', self.available_effects)


@dataclass
class Light:
    effect: Effect
    feature_light: bool
    flame_brightness: int
    flame_speed: int
    fuelbed_brightness: int
    fuelbed_speed: int

    @staticmethod
    def from_dict(data):
        return Light(
            effect=data.get("effect"),
            feature_light=data.get("pinout3"),
            flame_brightness=to_int(data.get("brightnessRGB0")),
            flame_speed=to_int(data.get("speedRGB0")),
            fuelbed_brightness=to_int(data.get("brightnessRGB1")),
            fuelbed_speed=to_int(data.get("speedRGB1")),
        )

    def update_from_dict(self, data):
        self.effect = data.get("effect", self.effect)
        self.feature_light = data.get("pinout3", self.feature_light)
        self.flame_brightness = to_int(data.get("brightnessRGB0", self.flame_brightness))
        self.flame_speed = to_int(data.get("speedRGB0", self.flame_speed))
        self.fuelbed_brightness = to_int(data.get("brightnessRGB1", self.fuelbed_brightness))
        self.fuelbed_speed = to_int(data.get("speedRGB1", self.fuelbed_speed))


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