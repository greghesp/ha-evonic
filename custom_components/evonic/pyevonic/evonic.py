"""Asynchronous Python client for Evonic Fires."""
from __future__ import annotations

# Built-in effects per model config, derived from docs/device-features.md.
# Used as the base effect list; any additional effects returned by /effect.json
# (e.g. purchased effects) are appended after these.
DEFAULT_EFFECTS: dict[str, list[str]] = {
    # Aura
    "aurac1":       ["Gold"],
    "aurac1s":      ["Gold"],
    # Element4 Electra
    "electra1030":  ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1030s": ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1250":  ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1250s": ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1350":  ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1350s": ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1500":  ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1500s": ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1800":  ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra1800s": ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electra850s":  ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    # Element4 Electrac
    "electrac1":    ["Gold", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electrac1s":   ["Gold", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electrac600":  ["Gold", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "electrac600s": ["Gold", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    # European Home
    "e1030":        ["Evoflame", "Party"],
    "e1250":        ["Evoflame", "Party"],
    "e1500":        ["Evoflame", "Party"],
    "e1800":        ["Evoflame", "Party"],
    "e2400":        ["Evoflame", "Party"],
    "e500":         ["Evoflame", "Party"],
    "e800":         ["Evoflame", "Party"],
    # Evonic Generic / 1800
    "evonicfires":  ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "1800":         ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    # Evonic Alente
    "alente":       ["Eseries", "Party"],
    # Evonic Chin
    "chin1800":     ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "chin1800s":    ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    # Evonic DH
    "dh1500":       ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    # Evonic DS
    "ds1030":       ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "White"],
    # Evonic HAL
    "hal1030":      ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "hal1500":      ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "hal2400":      ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "hal800":       ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "halev4":       ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "halev8":       ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    # Evonic Ilusion
    "ilusion2":     ["Ilusion", "Aurora", "Patriot", "Verona", "Charm", "Viva", "Cocktail", "Campfire"],
    # Evonic ROT
    "rot1250":      ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    "rot1500":      ["Gold", "Orbit", "Ignite", "Vero", "Spectrum", "Embers", "Red", "Green", "Blue", "Violet", "White"],
    # Evonic SF
    "sf1":          ["Low", "Medium", "High"],
    "sf1-40":       ["Low", "Medium", "High"],
    "sf2":          ["Low", "Medium", "High"],
    "sf3":          ["Low", "Medium", "High"],
    # Evonic SL
    "sl1000":       ["Ignite", "Fiesta"],
    "sl1250":       ["Ignite", "Fiesta"],
    "sl1500":       ["Ignite", "Fiesta"],
    "sl600":        ["Ignite", "Fiesta"],
    "sl700":        ["Ignite", "Fiesta"],
    # Evonic V-Series
    "v1030":        ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "v630":         ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    "v730":         ["Eos", "Ignite", "Vero", "Breathe", "Spectrum", "Embers", "Odyssey", "Aurora", "Red", "Orange", "Green", "Blue", "Violet", "White"],
    # Micon Alisio
    "alisio1150":   ["Ilusion", "Aurora", "Patriot", "Verona", "Charm", "Viva", "Cocktail", "Campfire", "Royal", "Scarlett", "Lava", "Magma"],
    "alisio1550":   ["Ilusion", "Aurora", "Patriot", "Verona", "Charm", "Viva", "Cocktail", "Campfire", "Royal", "Scarlett", "Lava", "Magma"],
    "alisio1850":   ["Ilusion", "Aurora", "Patriot", "Verona", "Charm", "Viva", "Cocktail", "Campfire", "Royal", "Scarlett", "Lava", "Magma"],
    "alisio850":    ["Ilusion", "Aurora", "Patriot", "Verona", "Charm", "Viva", "Cocktail", "Campfire", "Royal", "Scarlett", "Lava", "Magma"],
}

import asyncio
import json
import socket
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

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
    _effects_last_fetched: datetime | None = field(default=None, init=False)

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

        url = f"http://{host}{uri}"

        if self.session is None:
            LOGGER.debug("No session exists, using ClientSession")
            self.session = aiohttp.ClientSession()
            self._close_session = True

        LOGGER.debug("Sending HTTP %s request to %s", method, url)

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

            LOGGER.debug("HTTP request to %s completed with status %s", url, response.status)
            return response

        except asyncio.TimeoutError as exception:
            LOGGER.error("Timeout communicating with Evonic device at %s (url=%s)", self.host, url)
            raise EvonicConnectionTimeoutError(
                f"Timeout occurred while connecting to Evonic device at {self.host}") from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            LOGGER.error("Error communicating with Evonic device at %s (url=%s): %s", self.host, url, exception)
            raise EvonicConnectionError(
                f"Error occurred while communicating with Evonic device at {self.host}") from exception

    async def ws_request(self, uri):
        """Send a command to the Evonic Fire via WebSocket.

        Opens a connection, sends the command, then closes immediately.
        Only supports /voice and /cmd endpoints.

        Args:
            uri: The URI endpoint (e.g. /voice?command=Fire_ON)

        Raises:
            EvonicConnectionError: Unable to communicate via WebSocket
            EvonicConnectionTimeoutError: A timeout occurred while communicating
        """
        parsed = urlparse(uri)
        command_type = parsed.path.lstrip("/")  # "voice" or "cmd"
        params = parse_qs(parsed.query)
        command_value = params.get("command", [None])[0]

        if command_value is None:
            raise EvonicConnectionError(f"Cannot convert URI to WebSocket command: {uri}")

        message = json.dumps({command_type: command_value})
        ws_url = f"ws://{self.host}:81"

        if self.session is None:
            LOGGER.debug("No session exists, using ClientSession")
            self.session = aiohttp.ClientSession()
            self._close_session = True

        LOGGER.debug("Connecting to WebSocket at %s, sending: %s", ws_url, message)

        try:
            async with async_timeout.timeout(self.request_timeout):
                async with self.session.ws_connect(ws_url, protocols=["arduino"]) as ws:
                    await ws.send_str(message)
                    LOGGER.debug("WebSocket message sent to %s, closing connection", ws_url)
        except asyncio.TimeoutError as exception:
            LOGGER.error("Timeout connecting to Evonic device at %s via WebSocket", self.host)
            raise EvonicConnectionTimeoutError(
                f"Timeout occurred while connecting to Evonic device at {self.host} via WebSocket") from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            LOGGER.error("Error communicating with Evonic device at %s via WebSocket: %s", self.host, exception)
            raise EvonicConnectionError(
                f"Error occurred while communicating with Evonic device at {self.host} via WebSocket") from exception

    async def request(self, uri, method, data, host=None, scheme=None):
        """Send a request to the Evonic Fire, falling back to WebSocket if HTTP fails.

        Args:
            uri: The URI endpoint
            method: HTTP Method
            data: Request Content
            host: Domain to call (WebSocket fallback only used for local device requests)
            scheme: http vs https

        Returns:
            HTTP response if HTTP succeeded, None if WebSocket fallback was used.

        Raises:
            EvonicConnectionError: Both HTTP and WebSocket requests failed
        """
        try:
            return await self.http_request(uri, method, data, host, scheme)
        except (EvonicConnectionError, EvonicConnectionTimeoutError) as err:
            if host is not None:
                raise

            LOGGER.warning("HTTP request to %s failed, falling back to WebSocket: %s", uri, err)
            try:
                await self.ws_request(uri)
                LOGGER.debug("WebSocket fallback succeeded for %s", uri)
                return None
            except (EvonicConnectionError, EvonicConnectionTimeoutError) as ws_err:
                LOGGER.error(
                    "WebSocket fallback also failed for %s: %s", uri, ws_err)
                raise

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

        LOGGER.debug("Sending fire power command: %s", voice_command)
        return await self.request(f"/voice?command={voice_command}", "GET", None)

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

        LOGGER.debug("Setting effect: %s", effect)
        await self.request(f"/voice?command={effect}", "GET", None)
        self._device.light.effect = effect
        return await self.get_device()

    async def toggle_feature_light(self):
        """ Toggles the feature light of an Evonic Fire

        Raises:
            EvonicUnsupportedFeature: Feature Light is not supported on this device
        """

        if "light_box" not in self._device.info.modules:
            raise EvonicUnsupportedFeature("Feature Light is not supported on this device")

        LOGGER.debug("Toggling feature light")
        return await self.request(f"/voice?command=Featurelight_NOT", "GET", None)

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

        LOGGER.debug("Setting temperature to %s", temp)
        return await self.request(f"/cmd?command=templevel {temp}", "GET", None)

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

        LOGGER.debug("Sending heater power command: %s", voice_command)
        return await self.request(f"/voice?command={voice_command}", "GET", None)

    async def get_device(self):
        """Get the device information.

        Raises:
            EvonicConnectionError:  Unable to connect to device
        """

        if self._device is None:
            await self.get_config()

        LOGGER.debug("Fetching device state from %s", self.host)
        try:
            response = await self.http_request("/config.live.json", "GET", None)
            self._device.update_from_dict(data=await response.json(content_type=None))

            setup_response = await self.http_request("/config.setup.json", "GET", None)
            setup_data = await setup_response.json(content_type=None)
            setup_data.pop("effect", None)
            self._device.update_from_dict(data=setup_data)

        except EvonicError as err:
            raise EvonicConnectionError("Unable to connect to device") from err

        effects_stale = (
            self._effects_last_fetched is None or
            datetime.now() - self._effects_last_fetched > timedelta(hours=1)
        )
        if effects_stale:
            await self.__available_effects()

        return self._device

    async def get_config(self):
        """Get the initial device configuration.

        Raises:
            EvonicConnectionError:  Unable to connect to device
        """

        if self._device is None:
            LOGGER.debug("Fetching initial device configuration from %s", self.host)
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

            except EvonicError as err:
                raise EvonicConnectionError("Unable to connect to device") from err

        return self._device

    async def __available_effects(self):
        """ Returns a list of available effects for the device.

        Starts with the known built-in effects for the model (from DEFAULT_EFFECTS),
        then appends any additional effects returned by /effect.json that are not
        already in that list (e.g. purchased effects synced via the Evonic app).
        """

        if self._device is None:
            raise Exception("No device initialised")

        configs = self._device.info.configs
        base_effects = list(DEFAULT_EFFECTS.get(configs, []))
        LOGGER.debug("Base effects for configs=%s: %s", configs, base_effects)

        try:
            response = await self.request("/effect.json", "GET", None)
            data = await response.json(content_type=None)
            device_effects = data.get("effect") or []
            LOGGER.debug("Device effects response: %s", device_effects)
        except Exception as err:
            LOGGER.warning("Failed to fetch effects from device: %s", err)
            device_effects = []

        base_set = set(base_effects)
        extra_effects = [e for e in device_effects if e not in base_set]
        supported_effects = base_effects + extra_effects

        LOGGER.debug("Supported effects: %s", supported_effects)
        self._device.update_from_dict({"available_effects": supported_effects})
        self._effects_last_fetched = datetime.now()

    async def __aenter__(self):
        """Async enter.

        Returns:
            The Evonic object.
        """
        return self

    async def close(self) -> None:
        """Close the aiohttp session if it was created internally."""
        if self._close_session and self.session:
            await self.session.close()

    async def __aexit__(self, *_exc_info):
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
