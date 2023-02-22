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

    _client: aiohttp.ClientWebSocketResponse | None = None
    _close_session: bool = False
    _device: Device | None = None

    @property
    def connected(self) -> bool:
        """Return if we are connect to the WebSocket of an Evonic Fire.

        Returns:
            True if connected to the Websocket of an Evonic Fire,
            otherwise False
        """

        LOGGER.info(f"PYEVONIC: Client Connected: {self._client is not None and not self._client.closed}")

        return self._client is not None and not self._client.closed

    async def connect(self):
        """ Connect to the WebSocket of an Evonic Fire

        Raises:
            EvonicConnectionError: Error occurred while communicating with Evonic Fire via Websocket
        """

        LOGGER.debug("PYEVONIC: Called 'connect'")


        if self.connected:
            LOGGER.debug("Already Connected")
            return

        if self.session is None:
            LOGGER.debug("No session exists, using ClientSession")
            self.session = aiohttp.ClientSession()

        url = URL.build(scheme="ws", host=self.host, port=81)

        try:
            await self.request("/modules.json", "GET", None)
            await self.request("/config.options.json", "GET", None)
            await self.request("/config.admin.json", "GET", None)
            await self.__available_effects()
            LOGGER.debug(f"Connecting Websocket to: {url}")
            self._client = await self.session.ws_connect(url=url)
            await self.__send_cmd("get config.setup")
            return self._client, self.session

        except (
                aiohttp.WSServerHandshakeError,
                aiohttp.ClientConnectionError,
                aiohttp.ClientError,
                aiohttp.ClientPayloadError,
                ConnectionResetError,
                socket.gaierror,
        ) as exception:
            raise EvonicConnectionError(
                "Error occurred while communicating with Evonic device"
                f" on WebSocket at {self.host}"
            ) from exception

    async def listen(self, callback):
        """ Listen for events on the Evonic Fire WebSocket

        Args:
            callback: Method to call when an update is received from the Evonic Fire

        Raises:
            EvonicError: Not connected to the WebSocket
            EvonicConnectionError: An connection error occurred while connected
                to the Evonic Fire
            EvonicConnectionClosed: The WebSocket connection to the Evonic Fire has been closed.
        """
        LOGGER.debug("PYEVONIC: Called 'listen'")

        if not self._client:
            raise EvonicError("Not connected to a Evonic Fire WebSocket")

        while not self._client.closed:
            message = await self._client.receive()

            if message.type == aiohttp.WSMsgType.ERROR:
                raise EvonicConnectionError(self._client.exception())

            if message.type == aiohttp.WSMsgType.TEXT:
                message_data = message.json()

                if self._device is None:
                    LOGGER.debug("No Device exists, creating new instance")
                    self._device = Device(message_data)

                device = self._device.update_from_dict(message_data)
                LOGGER.debug(f"Message type is TEXT: {message_data}")
                callback(device)

            if message.type in (
                    aiohttp.WSMsgType.CLOSE,
                    aiohttp.WSMsgType.CLOSED,
                    aiohttp.WSMsgType.CLOSING,
            ):
                LOGGER.error(f"Connection to the Evonic WebSocket on {self.host} has been closed")
                raise EvonicConnectionClosed(
                    f"Connection to the Evonic WebSocket on {self.host} has been closed"
                )

    async def disconnect(self):
        """Disconnect from the WebSocket of an Evonic Fire."""
        if not self._client or not self.connected:
            LOGGER.debug("Cannot disconnect Websocket, as no client connection exists")
            return

        await self._client.close()

    async def request(self, uri, method, data, host=None, scheme=None):
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

        LOGGER.debug("PYEVONIC: Called 'request'")

        if host is None:
            host = self.host

        if scheme is None:
            scheme = "http"

        url = URL.build(scheme=scheme, host=host, path=uri)

        if self.session is None:
            LOGGER.debug("No session exists, using ClientSession")
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(method, url, json=data)
                LOGGER.debug(f"PYEVONIC: Request Response from {url}")

            content_type = response.headers.get("Content-Type", "")
            if (response.status // 100) in [4, 5]:
                contents = await response.read()
                response.close()

                if content_type == "application/json":
                    raise EvonicError(json.loads(contents.decode("utf8")))
                raise EvonicError(response.status, {"message": contents.decode("utf8")})

            if "application/json" in content_type:
                response_data = await response.json()

                if method == "GET" and uri == "/modules.json":
                    if self._device is None:
                        self._device = Device(response_data)
                    self._device.update_from_dict(data=response_data)

                elif method == "GET" and (uri == "/config.options.json" or uri == "/config.admin.json"):
                    self._device.update_from_dict(data=response_data)

                else:
                    response_data = await response.json()

        except asyncio.TimeoutError as exception:
            raise EvonicConnectionTimeoutError(
                f"Timeout occurred while connecting to Evonic device at {self.host}") from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise EvonicConnectionError(
                f"Error occurred while communicating with Evonic device at {self.host}") from exception

        return response_data

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

        return await self.__send_voice(voice_command)

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

        return await self.__send_voice(effect)

    async def toggle_feature_light(self):
        """ Toggles the feature light of an Evonic Fire

        Raises:
            EvonicUnsupportedFeature: Feature Light is not supported on this device
        """

        if "light_box" not in self._device.info.modules:
            raise EvonicUnsupportedFeature("Feature Light is not supported on this device")

        return await self.__send_voice("Light_box")

    async def set_light_brightness(self, rgb_id, brightness):
        """ Sets the brightness of each RGB strip

        Args:
            rgb_id: The ID of the RGB element
            brightness: Integer of brightness between 0 - 255

        Raises:
            EvonicUnsupportedFeature: RGB ID is not supported on this device
            EvonicError: Speed is not a valid value
        """

        if rgb_id not in self._device.info.modules:
            raise EvonicUnsupportedFeature(f"{rgb_id} is not supported on this device")

        if not isinstance(brightness, int):
            raise EvonicError("speed must be an Integer")

        # Must be 0 - 255
        if brightness not in range(-1, 256):
            raise EvonicError(f"{brightness} is not a valid value. Must be between 0 - 255")

        return await self.__send_cmd(f"rgb set {rgb_id[-1]} - - {brightness} -")

    async def set_animation_speed(self, rgb_id, speed):
        """ Sets the animation speed of each RGB strip

        Args:
            rgb_id: The ID of the RGB element
            speed: Integer of speed between 0 - 255

        Raises:
            EvonicUnsupportedFeature: RGB ID is not supported on this device
            EvonicError: Speed is not a valid value
        """

        if rgb_id not in self._device.info.modules:
            raise EvonicUnsupportedFeature(f"{rgb_id} is not a support RGB ID on this device")

        if not isinstance(speed, int):
            raise EvonicError("speed must be an Integer")

        # Must be 0 - 255
        if speed not in range(-1, 256):
            raise EvonicError(f"{speed} is not a valid value. Must be between 0 - 255")

        return await self.__send_cmd(f"rgb set {rgb_id[-1]} - {speed} - -")

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

        return await self.__send_cmd(f"templevel {temp}")

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
            voice_command = "Heater_ON_/_OFF"

        return await self.__send_voice(voice_command)

    async def get_device(self):
        """Get the initial device information.

        Raises:
            EvonicConnectionError:  Unable to connect to device
        """
        
        LOGGER.debug("PYEVONIC: Called 'get_device'")

        if self._device is None:
            try:
                await self.request("/modules.json", "GET", None)
            except EvonicError as err:
                raise EvonicConnectionError("Unable to connect to device") from err
        return self._device

    async def get_modules(self):
        """Get the modules via Websocket.

        Raises:
            EvonicConnectionError:  Unable to connect to device
        """
        LOGGER.debug("PYEVONIC: Called 'get_modules'")
        return await self.__send_cmd("get modules")

    async def __send_voice(self, cmd):
        """ Sends a command via Websocket Client.

        Args:
            cmd: The value of the voice field to send
        """

        if self._client is None:
            raise Exception("Connect first")

        LOGGER.debug(f"Sending voice command: {cmd}")
        return await self._client.send_str(f'{{"voice":"{cmd}"}}')

    async def __send_cmd(self, cmd):
        """ Sends a command to the WebSocket of an Evonic Fire

        Args:
            cmd: The cmd value to send
        """

        if self._client is None:
            raise Exception("Connect first")

        LOGGER.debug(f"Sending standard command: {cmd}")
        return await self._client.send_str(f'{{"cmd":"{cmd}"}}')

    async def __available_effects(self):
        """ Returns a list of available effects for each Evonic Fire type.
        Information pulled from /options.htm
        """

        if self._device is None:
            raise Exception("No device initialised")

        try:
            LOGGER.debug("Requesting paid effects")
            payed = await self.request(f"/effect/payed/{self._device.info.email}/{self._device.info.configs}", "GET",
                                       None,
                                       "evoflame.co.uk", "https")

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

        supported_effects = [*default_effects, *payed.get("effect")]
        LOGGER.debug(f"Supported effects {supported_effects}")

        self._device.update_from_dict({"available_effects": supported_effects})
        return

    async def close(self) -> None:
        """Close open client (WebSocket) session."""

        LOGGER.info("Closing Websocket Session")

        await self.disconnect()
        if self.session and self._close_session:
            await self.session.close()

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