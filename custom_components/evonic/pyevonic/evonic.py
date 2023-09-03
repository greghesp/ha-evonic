"""Asynchronous Python client for Evonic Fires."""
from __future__ import annotations

import asyncio
import json
import socket
import logging
from dataclasses import dataclass

import aiohttp
import async_timeout
from yarl import URL

from .models import Device

from .exceptions import (
    EvonicError,
    EvonicConnectionError,
    EvonicConnectionClosed,
    EvonicUnsupportedFeature,
    EvonicConnectionTimeoutError
)

LOGGER = logging.getLogger(__name__)


@dataclass
class Evonic:
    """Main class for handling connections with Evonic Fires."""

    host: str
    request_timeout: float = 8.0
    session: aiohttp.client.ClientSession | None = None

    _close_session: bool = False
    _device: Device | None = None

    async def http_request(self, uri, method, data, host=None, scheme=None):
        """ Sends a http request to the Evonic Fire

        Args:
            uri: The URI endpoint to send request to
            method: HTTP Method
            data: Request Content
            host:? Domain to call
            scheme:? http vs https

        Raises:
            EvonicError:  Received an unexpected response from the Evonic Fire
            EvonicConnectionTimeoutError: A timeout occurred while communicating with the Evonic Fire
            EvonicConnectionError:  A error occurred while communicating with the Evonic Fire
        """

        if host is None:
            host = self.host

        if scheme is None:
            scheme = "http"

        LOGGER.debug(uri)
        # url = URL.build(scheme=scheme, host=host, path=uri)
        url = f"http://{host}{uri}"

        if self.session is None:
            LOGGER.debug("No session exists, using ClientSession")
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(method, url, json=data)
                LOGGER.debug(f"Request Response from {url}:")
                LOGGER.debug(await response.text(encoding="latin-1"))

            content_type = response.headers.get("Content-Type", "")

            # If response is not 200, log error
            if (response.status // 100) in [4, 5]:
                contents = await response.read()
                response.close()

                if content_type == "application/json":
                    raise EvonicError(json.loads(contents.decode("utf8")))
                raise EvonicError(response.status, {"message": contents.decode("utf8")})

            return response

        except asyncio.TimeoutError as exception:
            raise EvonicConnectionTimeoutError(
                f"Timeout occurred while connecting to Evonic device at {self.host}") from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise EvonicConnectionError(
                f"Error occurred while communicating with Evonic device at {self.host}") from exception

    async def power(self, cmd):
        """ Controls the main lighting for the Evonic Fire.

        Args:
            cmd: The state to activate on this Fire. Can be "on", "off" or "toggle"

        Raises:
            EvonicError:  Command is not valid
        """

        if cmd not in ["on", "off", "toggle"]:
            raise EvonicError("Command not valid. Must be one of 'on', 'off' or 'toggle'")

        if cmd == "off":
            voice_command = "Fire_OFF"
        elif cmd == "on":
            voice_command = "Fire_ON"
        else:
            voice_command = "Fire_ON/OFF"

        return await self.http_request(f"/voice?command={voice_command}", "GET", None)

    async def set_effect(self, effect):
        """ Set an effect on Evonic Fire.

        Args:
            effect: The effect to active on this Evonic Fire

        Raises:
            EvonicUnsupportedFeature: Not a valid effect for this device
        """
        # Check effect is available for this device
        if effect not in self._device.effects.available_effects:
            raise EvonicUnsupportedFeature("Not a valid effect for this device")

        await self.http_request(f"/voice?command={effect}", "GET", None)
        return await self.get_device()

    async def toggle_feature_light(self):
        """ Toggles the feature light of an Evonic Fire

        Raises:
            EvonicUnsupportedFeature: Feature Light is not supported on this device
        """

        if "light_box" not in self._device.info.modules:
            raise EvonicUnsupportedFeature("Feature Light is not supported on this device")

        return await self.http_request(f"/voice?command=Featurelight_NOT", "GET", None)

    async def set_temperature(self, temp):
        """ Sets the heater temperature on an Evonic Fire

        Raises:
            EvonicUnsupportedFeature: Temperature Control is not supported on this device
        """

        if "temperature" not in self._device.info.modules:
            raise EvonicUnsupportedFeature("Temperature Control is not supported on this device")

        if not isinstance(temp, int):
            raise EvonicError("temp must be an Integer")

        if self._device.climate.fahrenheit:
            LOGGER.debug("Temperature is set to Fahrenheit")
            # Must be 50 - 90
            if temp not in range(49, 91):
                raise EvonicError(f"{temp} is not a valid value. Must be between 50 - 90")

        else:
            LOGGER.debug("Temperature is set to Celsius")
            # Must be 11 - 32
            if temp not in range(10, 33):
                raise EvonicError(f"{temp} is not a valid value. Must be between 11 - 32")

        return await self.http_request(f"/cmd?command=templevel {temp}", "GET", None)

    async def heater_power(self, cmd):
        """ Controls the Heater for the Evonic Fire.

        Args:
            cmd: The state to activate on this Fire. Can be "on", "off" or "toggle"

        Raises:
            EvonicError:  Command is not valid
        """

        if cmd not in ["on", "off", "toggle"]:
            raise EvonicError("Command not valid. Must be one of 'on', 'off' or 'toggle'")

        if cmd == "off":
            voice_command = "Heater_OFF"
        elif cmd == "on":
            voice_command = "Heater_ON"
        else:
            voice_command = "Heater_NOT"

        return await self.http_request(f"/voice?command={voice_command}", "GET", None)

    async def get_device(self):
        """Get the device information.

        Raises:
            EvonicConnectionError:  Unable to connect to device
        """

        if self._device is None:
            await self.get_config()

        try:
            response = await self.http_request("/config.live.json", "GET", None)
            self._device.update_from_dict(data=await response.json())

            setup_response = await self.http_request("/config.setup.json", "GET", None)

            self._device.update_from_dict(data=await setup_response.json())

        except EvonicError as err:
            raise EvonicConnectionError("Unable to connect to device") from err

        return self._device

    async def get_config(self):
        """Get the initial device configuration.

        Raises:
            EvonicConnectionError:  Unable to connect to device
        """

        if self._device is None:
            try:
                response = await self.http_request("/modules.json", "GET", None)
                response_data = await response.json()
                if self._device is None:
                    self._device = Device(response_data)
                self._device.update_from_dict(data=response_data)

                opt_response = await self.http_request("/config.options.json", "GET", None)
                self._device.update_from_dict(data=await opt_response.json())

                admin_response = await self.http_request("/config.admin.json", "GET", None)

                admin_response_data = await admin_response.json(encoding="latin-1")
                # Delete erroneous key
                del admin_response_data['AT+RFID']
                self._device.update_from_dict(data=admin_response_data)

                await self.__available_effects()
            except EvonicError as err:
                raise EvonicConnectionError("Unable to connect to device") from err

        return self._device

    async def __available_effects(self):
        """ Returns a list of available effects for each Evonic Fire type.
        Information pulled from /options.htm
        """

        paid = None

        if self._device is None:
            raise Exception("No device initialised")

        try:
            LOGGER.debug("Requesting paid effects")
            response = await self.http_request(f"/effect/payed/{self._device.info.email}/{self._device.info.configs}",
                                               "GET",
                                               None,
                                               "evoflame.co.uk", "https")
            paid = await response.json()

        except EvonicError as err:
            raise EvonicConnectionError("Unable to connect to device") from err

        configs = self._device.info.configs
        default_effects = ["Vero", "Ignite", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange",
                           "Green", "Blue", "Violet", "White"]

        if configs in ["1800", "ds1030", "hal800", "hal1030", "hal1500", "hal2400", "halev4",
                       "halev8", "irpanel", "v630", "v730", "v1030"]:
            default_effects.insert(0, "Eos")

        if configs in ["ilusion2", "alisio1150", "alisio1550", "alisio1850", "alisio850"]:
            default_effects = ["Ilusion", "Aurora", "Patriot", "Verona", "Charm", "Viva", "Cocktail", "Campfire"]

        if configs in ["alente", "e1030", "e1250", "e1500", "e1800", "e2400", "e500", "e800"] and configs != "1800":
            default_effects = ["Evoflame", "Party"]

        if configs in ["sl600", "sl700", "sl1000", "sl1250", "sl1500"]:
            default_effects = ["Ignite", "Fiesta"]

        if configs in ["video"]:
            default_effects = ["Low", "Medium", "High"]

        supported_effects = [*default_effects, *paid.get("effect")]
        LOGGER.debug(f"Supported effects {supported_effects}")

        self._device.update_from_dict({"available_effects": supported_effects})
        return

    async def __aenter__(self):
        """Async enter.

        Returns:
            The Evonic object.
        """
        return self

    async def __aexit__(self, *_exc_info):
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
