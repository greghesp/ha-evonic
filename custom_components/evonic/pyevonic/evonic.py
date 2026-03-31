"""Asynchronous Python client for Evonic Fires."""
from __future__ import annotations

import asyncio
import json
import socket
import logging
from dataclasses import dataclass

import aiohttp
import async_timeout

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
    _ws: aiohttp.ClientWebSocketResponse | None = None

    async def _ws_connect(self):
        """Establish a WebSocket connection to the fireplace on port 81."""
        if self._ws is not None and not self._ws.closed:
            return

        if self.session is None:
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                self._ws = await self.session.ws_connect(
                    f"ws://{self.host}:81",
                    protocols=["arduino"],
                )
            LOGGER.debug("WebSocket connected to %s:81", self.host)
        except asyncio.TimeoutError as exception:
            raise EvonicConnectionTimeoutError(
                f"Timeout connecting WebSocket to Evonic device at {self.host}"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror, OSError) as exception:
            raise EvonicConnectionError(
                f"Error connecting WebSocket to Evonic device at {self.host}"
            ) from exception

    async def _ws_send(self, msg_type: str, command: str):
        """Send a JSON command over WebSocket.

        The fireplace expects messages like: {"voice":"Fire_ON"} or {"cmd":"templevel 25"}
        """
        await self._ws_connect()

        message = json.dumps({msg_type: command}, separators=(",", ":"))
        LOGGER.debug("WebSocket send to %s: %s", self.host, message)

        try:
            await self._ws.send_str(message)
        except Exception as exception:
            self._ws = None
            raise EvonicConnectionError(
                f"Error sending WebSocket command to Evonic device at {self.host}"
            ) from exception

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

        url = f"{scheme}://{host}{uri}"

        if self.session is None:
            LOGGER.debug("No session exists, using ClientSession")
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(method, url, json=data)

            if (response.status // 100) in [4, 5]:
                contents = await response.read()
                response.close()
                content_type = response.headers.get("Content-Type", "")

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

        await self._ws_send("voice", voice_command)

    async def set_effect(self, effect):
        """ Set an effect on Evonic Fire.

        Args:
            effect: The effect to active on this Evonic Fire

        Raises:
            EvonicUnsupportedFeature: Not a valid effect for this device
        """
        if effect not in self._device.effects.available_effects:
            raise EvonicUnsupportedFeature("Not a valid effect for this device")

        await self._ws_send("voice", effect)
        self._device.light.effect = effect
        return await self.get_device()

    async def toggle_feature_light(self):
        """ Toggles the feature light of an Evonic Fire

        Raises:
            EvonicUnsupportedFeature: Feature Light is not supported on this device
        """

        if "light_box" not in self._device.info.modules:
            raise EvonicUnsupportedFeature("Feature Light is not supported on this device")

        await self._ws_send("voice", "Featurelight_NOT")

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

        await self._ws_send("cmd", f"templevel {temp}")

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

        await self._ws_send("voice", voice_command)

    async def get_device(self):
        """Get the device information.

        Raises:
            EvonicConnectionError:  Unable to connect to device
        """

        if self._device is None:
            await self.get_config()

        try:
            response = await self.http_request("/config.live.json", "GET", None)
            self._device.update_from_dict(data=await response.json(content_type=None))

            setup_response = await self.http_request("/config.setup.json", "GET", None)
            setup_data = await setup_response.json(content_type=None)
            setup_data.pop("effect", None)
            self._device.update_from_dict(data=setup_data)

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
                response_data = await response.json(content_type=None)
                self._device = Device(response_data)

                opt_response = await self.http_request("/config.options.json", "GET", None)
                self._device.update_from_dict(data=await opt_response.json(content_type=None))

                admin_response = await self.http_request("/config.admin.json", "GET", None)

                admin_response_data = await admin_response.json(content_type=None, encoding="latin-1")
                admin_response_data.pop('AT+RFID', None)
                self._device.update_from_dict(data=admin_response_data)

                await self.__available_effects()
            except EvonicError as err:
                raise EvonicConnectionError("Unable to connect to device") from err

        return self._device

    async def __available_effects(self):
        """ Returns a list of available effects for each Evonic Fire type.
        Information pulled from /options.htm
        """

        paid_effects = []

        if self._device is None:
            raise Exception("No device initialised")

        try:
            LOGGER.debug("Requesting paid effects")
            response = await self.http_request(f"/effect/payed/{self._device.info.email}/{self._device.info.configs}",
                                               "GET",
                                               None,
                                               "evoflame.co.uk", "https")
            paid = await response.json(content_type=None)
            paid_effects = paid.get("effect") or []

        except Exception as err:
            LOGGER.warning("Failed to fetch paid effects from evoflame.co.uk, continuing with defaults: %s", err)

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

        supported_effects = [*default_effects, *paid_effects]
        LOGGER.debug(f"Supported effects {supported_effects}")

        self._device.update_from_dict({"available_effects": supported_effects})
        return

    async def __aenter__(self):
        """Async enter.

        Returns:
            The Evonic object.
        """
        return self

    async def close(self) -> None:
        """Close WebSocket and aiohttp session."""
        if self._ws is not None and not self._ws.closed:
            await self._ws.close()
            self._ws = None
        if self._close_session and self.session:
            await self.session.close()

    async def __aexit__(self, *_exc_info):
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
