[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# Evonic Fires

[Home Assistant Community Thread](https://community.home-assistant.io/t/evonic-fires-custom-integration/457118)

Unofficial Evonic Fires integration for bringing your Evonic Fire into Home Assistant.  Also supports electric fires from European Home and Element4

Supports the following features:

- Power On/Off
- Feature Lighting On/Off
- Lighting Effects
- Heater On/Off
- Heater Target Temperature
- Current Ambient Temperature

![Overview](docs/images/img_1.png)

If you like this component, please give it a star on [github](https://github.com/greghesp/hacs-evonic).

##  Supported Fires

This has currently only been tested using the following devices:

- Evonic Linnea
- Evonic E1250

This Custom Component may work for more devices. Please let me know if it supports your fire, or raise an issue or PR

## Usage

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=greghesp&repository=ha-evonic&category=Integration)

To install, search for `Evonic` in the HACS default repositories, or click the badge above.

As this integration does not use cloud services, there isn't currenty a way to get the device IP address automatically (coming soon)
It is also recommend to give your fire a static IP address to prevent the connection for breaking in the event the fires IP address changes.

## Release Notes
**0.1.3**
- Added last ping sensor

**0.1.2**
- Sensor bug fix
