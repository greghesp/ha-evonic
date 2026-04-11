[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/greghesp/ha-evonic/total?style=for-the-badge)

![GitHub Release Date](https://img.shields.io/github/release-date/greghesp/ha-evonic?style=for-the-badge&label=Latest%20Release) [![GitHub Release](https://img.shields.io/github/v/release/greghesp/ha-evonic?style=for-the-badge)](https://github.com/greghesp/ha-evonic/releases)

# Evonic Fires for Home Assistant

Unofficial local integration for Evonic electric fires, and compatible fires from European Home and Element4.

[Home Assistant Community Thread](https://community.home-assistant.io/t/evonic-fires-custom-integration/457118) · [Report an Issue](https://github.com/greghesp/ha-evonic/issues)

> **Local only** — this integration communicates directly with your fire over your local network. No cloud account or internet connection is required.

---

## Entities

| Entity | Type | Description |
|---|---|---|
| Fire Lighting | Light | Power on/off and lighting effect selection |
| Feature Light | Light | Feature/accent lighting on/off (if supported by model) |
| Heater | Climate | Heater on/off and target temperature (°C or °F) |
| Current Temperature | Climate | Ambient temperature reading |
| Wi-Fi Signal | Sensor (diagnostic) | Device Wi-Fi signal strength in dBm |
| Heater Usage | Sensor (diagnostic) | Current heater power draw in Watts |
| LED Usage | Sensor (diagnostic) | Current LED power draw in Watts |
| Total Usage | Sensor (diagnostic) | Combined heater + LED power draw in Watts |
| Cost per Hour | Sensor (diagnostic) | Running cost based on configured kWh rate |
| Cost per kWh | Sensor (diagnostic) | Configured electricity rate |

Entities are only created if the feature is supported by your specific model — for example, `Feature Light` will not appear on models without a lightbox, and `Heater` will not appear on models without a temperature sensor.

---

## Installation

### HACS (recommended)

1. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) in HACS
2. Search for **Evonic** and install
3. Restart Home Assistant

### Manual

1. Copy the `custom_components/evonic` folder into your `config/custom_components/` directory
2. Restart Home Assistant

---

## Setup

1. In Home Assistant, go to **Settings → Devices & Services → Add Integration**
2. Search for **Evonic**
3. Enter the IP address of your fire

Since this integration connects locally, it is strongly recommended to assign your fire a **static IP address** (via your router's DHCP reservation) to prevent the connection breaking if the IP changes.

To change the IP address later, go to the integration's options via **Settings → Devices & Services → Evonic → Configure**.

---

## Lighting Effects

Available effects are fetched directly from the device, so the effect list will always reflect what is actually loaded — including any effects purchased through the Evonic app. Effects purchased via the app will appear automatically once synced to the device.

---

## Supported Devices

This integration supports any Evonic fire (and compatible European Home / Element4 fire) running the Evonic WiFi firmware. The following model families are known to be compatible:

**Evonic**
- Halo (800, 1030, 1500, 2400, EV4, EV8)
- Alisio (850, 1150, 1550, 1850)
- Electra (850S, 1030, 1030S, 1250, 1250S, 1350, 1350S, 1500, 1500S, 1800, 1800S, C1, C1S, C600, C600S)
- eSeries (500, 800, 1030, 1250, 1500, 1800, 2400)
- Ilusion / Ilusion 2
- SL Series (600, 700, 1000, 1250, 1500)
- V Series (630, 730, 1030)
- Video (DS1030)

**European Home / Element4**
- Alente, Aurora C1, Chinook 1800, Rotary (1250, 1500), SF Series

If your model is not listed, it may still work. Please [open an issue](https://github.com/greghesp/ha-evonic/issues) to let us know.

---

If you find this integration useful, please give it a star on [GitHub](https://github.com/greghesp/hacs-evonic).
