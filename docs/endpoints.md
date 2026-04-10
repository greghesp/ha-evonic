# Evonic Device Endpoints

The device exposes two control interfaces:

- **WebSocket** on port 81 — used by the native web UI for real-time bidirectional communication
- **HTTP** on port 80 — confirmed local endpoints for commands (e.g. `/cmd`, `/voice`); also used for reading config JSON files and triggering firmware upgrades

Both interfaces are real device endpoints. The HTTP endpoints are also used by the Alexa integration but are not exclusive to it.

For a full breakdown of which features are supported per device model, see [device-features.md](device-features.md).

---

## WebSocket Connection

```
ws://{device_ip}:81
Protocol: arduino
```

Messages are JSON objects sent as text frames. The top-level key determines the message type.

---

## WebSocket — Outbound Commands (HA → Device)

### `cmd` — Control Commands

Send as: `{"cmd": "<command string>"}`

| Command | Description | Notes |
|---|---|---|
| `get modules` | Request module/capability list | Returns `module` array in response |
| `get config.setup` | Request setup configuration | Returns device config, effects, settings |
| `get config.live` | Request live state | Returns current fire state |
| `get effectList` | Request custom effect list | Returns `effectList` array |
| `templevel {value}` | Set target temperature | `value`: 11–32 (°C) or 50–90 (°F) |
| `shimout {value} {channel}` | Set shimmer output brightness | `value`: 0–1023, `channel`: 0–3 |
| `rgb set {ch} - - {brightness} -` | Set RGB channel brightness | `ch`: 0–3, `brightness`: 0–255 |
| `rgb set {ch} - {speed} - -` | Set RGB channel speed | `ch`: 0–3, `speed`: 0–255 |
| `motor {value} 0` | Set flame motor speed | `value`: 0–1023 |
| `step {value} 0` | Set stepper motor position | `value`: 0–1023, requires `step0` module |
| `param send volume {value}` | Set volume level | `value`: 0–10, requires `volume` module |
| `param not pwrswitch` | Toggle heater power (2kW / 4kW) | Requires `pwrswitch` module |
| `ml set {n} {rrggbb} - {brightness}` | Set mood light colour and brightness | `n`: channel, `rrggbb`: hex string, `brightness`: 0–100 |
| `ml set {n} - {speed} -` | Set mood light speed | `n`: channel, `speed`: 1–31 |
| `ml set {n} - - - {effectId}` | Set mood light effect mode | `n`: channel, see Mood Light Effects table |
| `ml not {n}` | Toggle mood light on/off | `n`: channel (0, 1, 2…) |
| `ml name {n} {name}` | Rename a mood light | `name`: alphanumeric, max 10 chars |
| `mldel {n}` | Delete a mood light | `n`: channel |
| `save mail {email}` | Save registered email to device | Used during provisioning |
| `save pass {password}` | Save account password to device | Used during provisioning |
| `save ssid {ssid}` | Save WiFi SSID to device | Used during provisioning |
| `save ssidPass {password}` | Save WiFi password to device | Used during provisioning |
| `reboot ok` | Reboot the device | Same effect as `GET /restart?device=ok` |
| `get timer.save` | Request the full timer list | Returns `timer` array and current `time` |
| `time {datetime}` | Set the RTC clock | `datetime`: formatted string e.g. `Dec 25 2023 07:30:00 GMT+0000` (from `Date.toString()`) |
| `set_chanal_rcp {channel}` | Set remote control pairing channel | `channel`: 1–128 |
| `effect_next` | Cycle to next effect | |
| `effect_last` | Cycle to previous effect | |
| `save_effect` | Persist the current effect to storage | |

#### Mood Light Effect IDs

| ID | Effect |
|---|---|
| `0` | Cross fade |
| `11` | Strobe flash |
| `19` | Jumping change |
| `60` | Colour (activates colour picker mode) |

#### RGB Channel Mapping

| Channel | Zone |
|---|---|
| 0 | Flame (rgb0) |
| 1 | Log / Top (rgb1) |
| 2 | Ember / FuelBed (rgb2) |
| 3 | Additional zone (rgb3) |

---

### `voice` — Voice/Toggle Commands

Send as: `{"voice": "<command>"}`

| Command | Description | Notes |
|---|---|---|
| `Fire_NOT` | Toggle fire on/off | Used by options UI |
| `Fire_ON/OFF` | Toggle fire on/off | Used by homepage UI — may be equivalent to `Fire_NOT` |
| `Heater_NOT` | Toggle heater on/off | Used by options UI |
| `Heater_ON_/_OFF` | Toggle heater on/off | Used by homepage UI — may be equivalent to `Heater_NOT` |
| `Light_box` | Toggle feature light box | Requires `light_box` module |
| `Relay1_NOT` | Toggle relay 1 | Requires `econtrol` config |
| `Relay2_NOT` | Toggle relay 2 | Requires `econtrol` config |
| `Relay3_NOT` | Toggle relay 3 | Requires `econtrol` config |
| `volume` | Apply/commit volume change | Send after `param send volume` |
| `{EffectName}` | Activate a named effect | e.g. `Vero`, `Ignite`, `Eos` |
| `Fire_ON` | Turn fire on | Used by timer scheduler |
| `Fire_OFF` | Turn fire off | Used by timer scheduler |
| `Heater_ON` | Turn heater on | Used by timer scheduler |
| `Heater_OFF` | Turn heater off | Used by timer scheduler |
| `Fire_Heater_ON` | Turn fire and heater on simultaneously | |
| `Featurelight_NOT` | Toggle feature light | Same as `Light_box` on most models |
| `Moodlight_ON` | Turn mood light on | Requires `ml0`/`ml1` module |
| `Moodlight_OFF` | Turn mood light off | Requires `ml0`/`ml1` module |
| `effect_next` | Cycle to next effect | |
| `effect_last` | Cycle to previous effect | |
| `upgrade_stable` | Trigger OTA upgrade (stable channel) | Requires `upgrade` module |
| `upgrade_beta` | Trigger OTA upgrade (beta channel) | Requires `admin` module |
| `upgrade_alpha` | Trigger OTA upgrade (alpha channel) | Requires `admin` module |

---

### `effect` — Set Effect

Send as: `{"effect": "<EffectName>"}`

Sets the active effect by name. Used for effects from the custom `effectList` (all-caps names indicate user-created effects).

---

### Remote Control & IR Button Mapping

The physical RF remote and IR remote send `voice` commands using hex codes. The device's scenary file maps these to actions. The full mapping from `scenaryrcp.txt` and `scenaryir.txt`:

| RCP Code | IR Code | Action |
|----------|---------|--------|
| `rcp04on` | `E0E040BF` / `E0E06798` | Toggle fire on/off |
| `rcp02on` | `E0E058A7` | Toggle feature light |
| `rcp01on` | `E0E06F90` | RGB0 brightness up (+16) |
| `rcp03on` | `E0E04BB4` | RGB0 brightness down (−16) |
| `rcp0Aon` | `E0E09D62` | RGB1 brightness up (+16) |
| `rcp0Bon` | `E0E01AE5` | RGB1 brightness down (−16) |
| `rcp05on` | `E0E006F9` | Temperature up (+1) |
| `rcp09on` | `E0E08679` | Temperature down (−1) |
| `rcp13on` | `E0E0CF30` | Thermostat minimum |
| `rcp12on` | `E0E02FD0` | Thermostat mid |
| `rcp11on` | `E0E03DC2` | Thermostat maximum |
| `rcp06on` | `E0E016E9` | Toggle heater on/off |
| `rcp08on` | `E0E046B9` | Heater timer up (+15 min) |
| `rcp07on` | `E0E0A659` | Heater timer down (−15 min) |
| `rcp0Con` | `E0E09E61` | Toggle fuelbed RGB (rgb not 1) |
| `rcp0Don` | `E0E008F7` | Next effect |
| `rcp0Fon` | `E0E048B7` | Previous effect |
| `rcp0Eon` | `E0E0E01F` | Volume up (+1) |
| `rcp10on` | `E0E0D02F` | Volume down (−1) |

> These codes arrive at the device as `voice` commands and are processed by the scenary engine. They are not typically sent from Home Assistant directly.

---

## WebSocket — Inbound State (Device → HA)

The device pushes state updates as JSON objects. Fields present depend on what changed or was requested.

### Fire & Heater State

| Field | Type | Description |
|---|---|---|
| `Fire` / `fire` | `0` or `1` | Fire on/off |
| `Heater` / `heater` | `0` or `1` | Heater on/off |
| `pwrswitch` | `0` or `1` | Heater power mode (0=2kW, 1=4kW) |
| `heaterTime` | int | Heater timer remaining in minutes (0=no timer) |
| `Relay1` / `relay1` | `0` or `1` | Relay 1 state (econtrol config) |
| `Relay2` / `relay2` | `0` or `1` | Relay 2 state (econtrol config) |
| `Relay3` / `relay3` | `0` or `1` | Relay 3 state (econtrol config) |
| `linkrcp` | `0` or `1` | Remote control pairing detected (1=pair pending) |

### Temperature

| Field | Type | Description |
|---|---|---|
| `templevel` | int | Target temperature (setpoint) |
| `temperature` | int | Actual sensor temperature. `-127` or `127` = sensor error |
| `fahrenheit` | `0` or `1` | Temperature unit (0=°C, 1=°F) |

### Lighting

| Field | Type | Description |
|---|---|---|
| `pinout3` | `0` or `1` | Feature light box state |
| `Moodlight` | `0` or `1` | Mood light on/off state |
| `alarmtemperature` | `0` or `1` | Temperature alarm active (overheating protection triggered) |
| `brightnessRGB0` | 0–255 | Flame zone brightness |
| `brightnessRGB1` | 0–255 | Log/Top zone brightness |
| `brightnessRGB2` | 0–255 | Ember/FuelBed zone brightness |
| `brightnessRGB3` | 0–255 | Additional zone brightness |
| `speedRGB0` | 0–255 | Flame zone speed |
| `speedRGB1` | 0–255 | Log/Top zone speed |
| `speedRGB2` | 0–255 | Ember/FuelBed zone speed |
| `speedRGB3` | 0–255 | Additional zone speed |
| `shimout0`–`shimout3` | 0–1023 | Shimmer output levels |
| `motor0` | 0–1023 | Flame motor speed |
| `step0` | 0–1023 | Stepper motor position |

### Effects

| Field | Type | Description |
|---|---|---|
| `effect` | string | Currently active effect name |
| `effectList` | array | Device custom effect list (all-caps = user created) |

### Power & Energy

| Field | Type | Description |
|---|---|---|
| `powerLed` | int | LED power draw (watts) |
| `powerHeater` | int | Heater power draw (watts) |
| `cost` | float | Energy cost rate (£/kWh) |

### Media / Volume

| Field | Type | Description |
|---|---|---|
| `volume` | 0–10 | Current volume level |

### Settings State (returned from `get config.setup`)

| Field | Type | Description |
|---|---|---|
| `ssid` | string | Current WiFi SSID the device is connected to |
| `ssidPass` | string | WiFi password |
| `ssidApPass` | string | Access point password |
| `timeZone` | int | Current GMT offset (e.g. `1` for GMT+1) |
| `checkboxIP` | `0` or `1` | Static IP enabled |
| `ip` | string | Device IP address |
| `getway` | string | Default gateway |
| `subnet` | string | Subnet mask |
| `dns` | string | DNS server |
| `autopower` | `0` or `1` | Auto power-on enabled |
| `rcp` | `0` or `1` | Remote control enabled |
| `shop` | `0` or `1` | Work mode (0=home, 1=shop/display) |
| `setIndex` | string | Active UI skin file (`index.htm` or `index2.htm`) |
| `cost` | float | Energy cost per kWh |
| `rcpParing` | string/int | Remote pairing state: `start`, channel number (int), `done`, or `error` |
| `message` | string | Status or error message from device (e.g. login errors) |

### Timers

| Field | Type | Description |
|---|---|---|
| `time` | string | Current device time as `HH:MM:SS` |
| `timer` | array | List of timer objects (see Timer Object below) |

#### Timer Object

Timers are stored in pairs sharing the same `id` — one entry for the ON time, one for the OFF time.

| Field | Type | Description |
|---|---|---|
| `id` | int | Timer pair identifier (random, shared between ON and OFF entries) |
| `day` | string | 7-character bitmask (index 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat). `1`=active, `0`=inactive |
| `time1` | string | Trigger time as `HH:MM:SS` |
| `com1` | string | Command to execute, prefixed with `voice ` (e.g. `voice Fire_ON`, `voice Heater_OFF`) |
| `run1` | `0` or `1` | Whether this entry has already fired today |
| `active` | `0` or `1` | Whether this timer is enabled |

**Example timer pair:**
```json
[
  { "id": 4521, "day": "1111100", "time1": "07:30:00", "com1": "voice Fire_ON",  "run1": 0, "active": 1 },
  { "id": 4521, "day": "1111100", "time1": "22:00:00", "com1": "voice Fire_OFF", "run1": 0, "active": 1 }
]
```

### Mood Lights (ml0, ml1)

Each mood light channel reports its own state fields. Replace `0` with the channel number.

| Field | Type | Description |
|---|---|---|
| `stateMl0` | `0` or `1` | Mood light on/off |
| `colorMl0` | string | Current colour as hex string |
| `brightnessMl0` | 1–100 | Brightness percentage |
| `speedMl0` | 1–31 | Animation speed |
| `modeMl0` | int | Effect mode ID (0, 11, 19, 60 — see Mood Light Effects table) |
| `typeMl0` | int | Light type. `65` = single colour only (no effects) |
| `ml0` | string | Mood light name/label |

### Diagnostics

| Field | Type | Description |
|---|---|---|
| `dbm` | int | WiFi signal strength in dBm (e.g. `-60`). `0` = wired LAN |
| `heap` | int | Free heap memory on ESP8266 (bytes) |
| `vcc` | float | Supply voltage (e.g. `3.30`) |

### Device Info (returned on full config load)

| Field | Type | Description |
|---|---|---|
| `SSDP` | string | Device SSDP identifier |
| `configs` | string | Device configuration/model variant |
| `module` | array | Enabled hardware modules |
| `buildData` | string | Firmware build filename (e.g. `2024-02-26generic.bin`) |
| `product` | string | Product name |
| `mail` | string | Registered email (used for paid effects lookup) |
| `lang` | string | UI language code |
| `logo` | int | Brand logo variant (0=Evonic, 1=Element4, 2=European Home, 3=Regency, 4=Ortal, 5=Aura, 6=Micon, -1=none) |

---

## Module Keys

The `module` array from `get modules` controls which features are available. Known keys:

| Key | Feature Enabled |
|---|---|
| `admin` | Admin UI, alpha firmware update controls |
| `upgrade` | OTA upgrade check against evoflame.co.uk |
| `volume` | Audio/volume control |
| `step0` | Stepper motor (flame height) |
| `pwrswitch` | Dual power switch (2kW / 4kW) |
| `light_box` | Feature light box |
| `rgb0` | Flame zone RGB lighting |
| `rgb1` | Log/Top zone RGB lighting |
| `rgb2` | Ember/FuelBed zone RGB lighting |
| `rgb3` | Additional RGB zone |
| `ml0` | Mood light channel 0 |
| `ml1` | Mood light channel 1 |
| `shop` | Paid content / shop access |
| `timers` | Timer/schedule functionality |
| `rcp` | Remote control pairing |
| `pult` | Remote control (shows remote icon instead of brightness) |
| `rcp` | Remote control pairing support |
| `cost` | Energy cost tracking (shows cost field in settings) |
| `moodlight` | Mood light discovery (shows search button in settings) |
| `ntp` | NTP time sync (shows time sync in settings) |
| `rtc` | RTC hardware clock (shows time sync in settings) |
| `eth` | Ethernet module present |

> **Note:** `econtrol` is a `configs` value (not a module key) that indicates an external relay controller. It hides the effects/brightness UI and shows relay toggle buttons instead.

---

## Local HTTP Endpoints

All requests are `GET` to `http://{device_ip}/`.

### Read Endpoints

| Endpoint | Description | Response |
|---|---|---|
| `/modules.json` | Device capabilities and identity | JSON object with `module`, `SSDP`, `configs`, `product`, `buildData`, `mail` etc. |
| `/config.live.json` | Current live state | JSON with `Fire`, `Heater`, `effect`, `templevel`, `brightnessRGB*`, `speedRGB*` etc. |
| `/config.setup.json` | Device setup/configuration | JSON with `effect` (current effect string), settings |
| `/config.options.json` | Options configuration | JSON with device options |
| `/config.admin.json` | Admin configuration | JSON (latin-1 encoded), contains `AT+RFID` and other admin fields |
| `/lang/lang.{code}.json` | UI language strings | JSON key/value pairs, e.g. `lang.en.json` |

### Control Endpoints

| Endpoint | Description | Notes |
|---|---|---|
| `GET /voice?command={command}` | Send a voice/toggle command | See voice commands table above |
| `GET /cmd?command={command}` | Send a control command | See cmd commands table above |
| `GET /cmd?command=zone {offset}` | Set timezone offset | `offset`: GMT hours offset (e.g. `1` for GMT+1) |
| `GET /cmd?command=search_ml` | Scan for mood light devices | |
| `GET /cmd?command=search_audio` | Scan for audio devices | |
| `GET /restart?device=ok` | Reboot the device | Equivalent to `reboot ok` WebSocket command |
| `GET /config?restore=ok` | Factory reset the device | Clears all settings and returns to AP mode |
| `GET /auth?pass={password}` | Authenticate for admin access | Returns `allowed` or error string |
| `GET /setscenary` | Reload and apply the active scenary file | Call after writing to the scenary file via `/edit` |

### Admin Endpoints

Require admin authentication (`GET /auth?pass={password}` first).

| Endpoint | Description |
|---|---|
| `GET /admin/config?rfc={rfc}&ssdp={ssdp}&logo={logo}&configs={model}&restore=ok` | Save admin config (device name, brand logo, model variant) |
| `GET /admin/device?rfc={rfc}&ssdp={ssdp}&logo={logo}&configs={model}&restore=ok` | Alternative admin device save endpoint |

| Parameter | Type | Description |
|---|---|---|
| `rfc` | string | Device RFC/identifier |
| `ssdp` | string | Device SSDP name |
| `logo` | int | Brand logo index (0=Evonic, 1=Element4, 2=European Home, 3=Regency, 4=Ortal, 5=Aura, 6=Micon) |
| `configs` | string | Device model variant (e.g. `hal1500`) — determines scenary, effects, and UI |
| `restore` | `ok` | Must be `ok` to apply changes |

### Device Settings Endpoints

#### Save Device Settings
```
GET /device
```
Saves one or more device settings. Parameters can be combined in a single request.

| Parameter | Type | Description |
|---|---|---|
| `ssdp` | string | Device name (3–20 alpha chars, used for Alexa/Google Home) |
| `shop` | `0` or `1` | Work mode (0=home, 1=shop/display) |
| `fahrenheit` | `0` or `1` | Temperature unit |
| `cost` | float | Energy cost per kWh |
| `rcp` | `0` or `1` | Remote control enabled |
| `autopower` | `0` or `1` | Auto power-on enabled |
| `mail` | string | Account email |
| `pass` | string | Account password (URL encoded) |
| `space` | string | Always `home` in current firmware |

#### Save WiFi Connection
```
GET /ssid
```

| Parameter | Type | Description |
|---|---|---|
| `ssid` | string | WiFi network name (URL encoded) |
| `ssidPass` | string | WiFi password (URL encoded) |
| `ip` | string | Static IP address (if `checkboxIP=1`) |
| `subnet` | string | Subnet mask |
| `getway` | string | Default gateway |
| `dns` | string | DNS server |
| `checkboxIP` | `0` or `1` | 0=DHCP, 1=static IP |

#### Save Access Point Settings
```
GET /ssidap
```

| Parameter | Type | Description |
|---|---|---|
| `ssidAP` | string | AP network name |
| `ssidApPass` | string | AP password (min 3 chars) |

#### Set Language
```
GET /lang?set={langCode}
```
Supported codes seen: `en`, `ru`, `de`, `fr`, `nl`. Requires a reboot to take full effect.

#### Set UI Skin
```
GET /skins?set={skin}
```
| Value | Description |
|---|---|
| `index.htm` | Single-device UI |
| `index2.htm` | Multi-device UI |

Applied to all discovered devices on the local network simultaneously.

### Network & Discovery

| Endpoint | Description | Response |
|---|---|---|
| `GET /wifi.scan.json` | Scan for available WiFi networks | `{ "networks": [{ "ssid": "Name", "dbm": -65 }] }` sorted by signal strength |

### Discovery

| Endpoint | Description | Response |
|---|---|---|
| `GET /ssdp.list.json` | Local SSDP device list | JSON object mapping SSDP names to IP addresses. Used by the homepage to discover all fireplaces on the network |

### Scenes

| Endpoint | Description | Response format |
|---|---|---|
| `GET /scenary.save.txt` | Saved scene list | Plain text. Each scene is a line starting with `if voice = {commandName}` |

### Timers

| Endpoint | Description |
|---|---|
| `GET /timer.save.json` | Read the full timer list from device filesystem |
| `GET /settimer` | Signal the device to reload and apply the saved timer schedule. Always call after writing to `timer.save.json` |
| `POST /edit` | Write a file to the device filesystem (SPIFFS/LittleFS). Used to save updated timer JSON back to the device |

#### `POST /edit` — Filesystem Write

Writes any file to the device filesystem. Used by the timer UI to save changes.

**Content-Type:** `multipart/form-data`

| Form field | Value |
|---|---|
| `data` | File content as a `Blob` with `type: text/json`, filename set to `/{filename}` (e.g. `/timer.save.json`) |

**Timer save workflow:**
1. `GET /timer.save.json` — read current timers
2. Modify the JSON in memory
3. `POST /edit` — write updated JSON back (filename: `/timer.save.json`)
4. `socket('cmd', 'get timer.save')` — reload timer list over WebSocket
5. `GET /settimer` — apply the new schedule

### Firmware Upgrade

| Endpoint | Description |
|---|---|
| `GET /upgrade?build={build_file}&spiffs={spiffs_file}` | Trigger OTA firmware upgrade. Filenames supplied by the upgrade check endpoint. Takes up to 10 minutes — do not power off during upgrade. |

---

## Remote Endpoint — Paid Effects

```
GET https://evoflame.co.uk/effect/payed/{email}/{configs}
```

Returns effects unlocked for the registered device account.

**Response:**
```json
{
  "effect": ["Christmas", "Rainbow", "ColorSparks", "Nikola", "Dream"]
}
```

Returns an empty `effect` array if no paid effects are registered, or if the email/configs combination is not found.

---

## Remote Endpoints — evoflame.co.uk

### Firmware Update Check

```
GET https://evoflame.co.uk/upgrade/{email}/{model}/{ssdp}?v={random}
```

| Parameter | Description |
|---|---|
| `email` | Registered account email |
| `model` | Device model/buildData string |
| `ssdp` | Device SSDP identifier |

**Response:**
```json
{
  "message": "<optional HTML message to display>",
  "upgrade": ["{spiffs_filename}", "{build_filename}"],
  "type": "important|beta|standard"
}
```

If `upgrade[1]` version is newer than the device's current `buildData`, an update is available. `type: important` forces a modal prompt.

---

### Release Notes

```
GET https://evoflame.co.uk/release/{version}.json/{model}
```

**Response:**
```json
{
  "release": "What's new text (may contain \\r\\n line breaks)"
}
```

---

### Cloud Device Control

Requires an `Auth: {token}` request header. Token obtained from `/ssdp.list.json`.

```
GET https://{server}/web/{ssdp}/{command}/{param}
```

| Command | Param | Description |
|---|---|---|
| `power` | `Fire_NOT` | Toggle fire on/off |
| `power` | `Heater_NOT` | Toggle heater on/off |
| `tempset` | `{temperature}` | Set target temperature |
| `effectset` | `{effectName}` | Set active effect |

**Response:** Device state object (same structure as WebSocket inbound state).

---

### SSDP Device List (Cloud)

```
GET https://evoflame.co.uk/ssdp.list.json/{token}
GET /ssdp.list.json/{token}   (local relay)
```

**Response:**
```json
{
  "server": "hostname",
  "token": "auth_token",
  "email": "user@example.com",
  "lang": "en",
  "list": [...]
}
```

---

## Default Effects by Config Variant

These are the built-in effects per device type, before paid effects are appended. The `s` suffix variants (e.g. `electra1500s`) share the same effects as their non-`s` counterpart. See [device-features.md](device-features.md) for the full per-model feature matrix.

| Config(s) | Default Effects |
|---|---|
| `evonicfires`, `1800`, `dh1500`, `hal800`, `hal1030`, `hal1500`, `hal2400`, `halev4`, `halev8`, `v630`, `v730`, `v1030` | Eos, Ignite, Vero, Breathe, Spectrum, Embers, Odyssey, Aurora, Red, Orange, Green, Blue, Violet, White |
| `ds1030` | Eos, Ignite, Vero, Breathe, Spectrum, Embers, Odyssey, Aurora, Red, Orange, **Yellow**, Green, Blue, Violet, White |
| `alisio850`, `alisio1150`, `alisio1550`, `alisio1850` | Ilusion, Aurora, Patriot, Verona, Charm, Viva, Cocktail, Campfire, Royal, Scarlett, Lava, Magma |
| `ilusion2` | Ilusion, Aurora, Patriot, Verona, Charm, Viva, Cocktail, Campfire |
| `e500`, `e800`, `e1030`, `e1250`, `e1500`, `e1800`, `e2400` | Evoflame, Party |
| `alente` | Eseries, Party |
| `sl600`, `sl700`, `sl1000`, `sl1250`, `sl1500` | Ignite, Fiesta |
| `electra1030`, `electra1250`, `electra1350`, `electra1500`, `electra1800`, `chin1800`, `rot1250`, `rot1500` | Gold, Orbit, Ignite, Vero, Spectrum, Embers, Red, Green, Blue, Violet, White |
| `electrac1`, `electrac600` | Gold, Ignite, Vero, Spectrum, Embers, Red, Green, Blue, Violet, White |
| `aurac1`, `aurac1s` | Gold |
| `sf1`, `sf1-40`, `sf2`, `sf3` | Low, Medium, High |
| `video`, `videonew` | Amsterdam, London, NewYork |
| All others (fallback) | Vero, Ignite, Breathe, Spectrum, Embers, Odyssey, Aurora, Red, Orange, Green, Blue, Violet, White |

> **Note:** Config types `eseries` and `ilusion` (v1) hide the effects picker entirely in the native UI.
> Config types `sf*` use flame intensity presets (Low/Medium/High) rather than colour effects, and have no effect cycling or brightness control.
> Config type `videonew` uses a simplified UI with no navigation or brightness controls.
