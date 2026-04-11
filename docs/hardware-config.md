# Hardware Configuration Reference

Derived from firmware `configs/*.txt` files on the device SPIFFS filesystem.
These files define the physical hardware wiring, LED configuration, and enabled
modules for each device model.

> **Note:** These configs were extracted from a live device and may reflect
> user modifications rather than factory defaults. In particular, `ADMIN` mode
> is not enabled by default on any retail model — it must be manually enabled.

## Universal GPIO Pin Mapping

The following GPIO assignments are **identical across all models**:

| GPIO | Function | Notes |
|------|----------|-------|
| GPIO14 | Fire relay output | Active high, starts OFF |
| GPIO12 | Heater relay output | Active high, starts OFF |
| GPIO15 | Feature light (Lightbox) output | Starts ON; absent on `s`-suffix and some models |
| GPIO1 | LED segment 0 (flame zone) | WS2812 data pin |
| GPIO3 | LED segment 1 (log/top zone) | WS2812 data pin; GRID type on `ilusion` |
| GPIO2 | DS18B20 temperature sensor | 1-Wire |
| GPIO4 | RF remote (RCP) TX | JDY-40 module, 9600 baud |
| GPIO5 | RF remote (RCP) RX | JDY-40 module, 9600 baud |
| GPIO16 | Buzzer | |

## LED Strip Types

| Type | Description |
|------|-------------|
| `RGB` | WS2812/NeoPixel addressable LED strip. Parameters: pin, segment, LED count, start state, default colour, speed, brightness, dynamic |
| `GRID` | WS2812 2D matrix panel (used by Ilusion series). Same parameters as RGB |
| `SHIMOUT` | PWM dimmer output for non-addressable LEDs (used by E-Series). Parameters: pin, channel, brightness, inversion, name |

## Per-Model Hardware Configuration

The main variable between models is the LED count per segment, which scales with
the physical width of the firebox. All other GPIO assignments remain constant.

### Aura

#### `aurac1`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 4 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 40 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `aurac1s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 4 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 40 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `cost` (energy tracking)


### Element4 Electra

#### `electra1030`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 8 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 53 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `electra1030s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 8 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 53 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `electra1250`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 10 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 68 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `electra1250s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 10 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 68 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `electra1350`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 6 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 43 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `electra1350s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 6 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 43 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `electra1500`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 12 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 80 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `electra1500s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 12 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 80 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `electra1800`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 14 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 90 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `electra1800s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 14 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 90 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `electra850s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 8 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 53 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)


### Element4 Electrac

#### `electrac1`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 4 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 40 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `electrac1s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 4 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 40 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `electrac600`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 6 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 22 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `electrac600s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 6 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 22 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)


### European Home

#### `e1030`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 41 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 41 | `#ff4800` | 90 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `e1250`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 63 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 63 | `#ff4800` | 90 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `e1500`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 67 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 67 | `#ff4800` | 90 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `e1800`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 87 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 87 | `#ff4800` | 90 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `e2400`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 128 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 128 | `#ff4800` | 90 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `e500`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 23 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 23 | `#ff4800` | 90 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `e800`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 33 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 33 | `#ff4800` | 90 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)


### European Home E-Series

#### `eseries`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**Shimmer outputs (PWM):**

| Channel | GPIO | Name | Default Brightness | Inverted |
|---------|------|------|--------------------|----------|
| #0 | GPIO15 | Led24 | 1023 | Yes |

**Power:** Heater 1513W · LED 39W

**Modules:** `cost` (energy tracking)


### Evonic (Generic)

#### `evonicfires`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 23 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 26 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

**Admin mode:** Enabled


### Evonic 1800

#### `1800`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 104 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 104 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)


### Evonic Alente

#### `alente`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 66 | `#ff4800` | 87 | 255 | 49 |
| 1 | GPIO3 | 70 | `#ff4800` | 89 | 255 | 49 |

**Power:** Heater 1513W · LED 23W

**Modules:** `cost` (energy tracking)


### Evonic Chin

#### `chin1800`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 14 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 99 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `chin1800s`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 14 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 99 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)


### Evonic DS

#### `ds1030`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 41 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 56 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)


### Evonic HAL

#### `hal1030`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 41 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 56 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `hal1500`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 68 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 84 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `hal2400`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 128 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 128 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `hal800`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 33 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 43 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `halev4`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 16 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 16 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `halev8`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 30 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 30 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `shop` (paid effects), `cost` (energy tracking)


### Evonic Ilusion

#### `ilusion`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED grid (WS2812 matrix):**

| Segment | GPIO | LED Count |
|---------|------|-----------|
| 0 | GPIO3 | 512 |

**Power:** Heater 1500W · LED 20W

**Modules:** `cost` (energy tracking)

#### `ilusion2`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 256 | `#ff5000` | 40 | 255 | 16 |
| 1 | GPIO3 | 88 | `#FF2500` | 100 | 170 | 16 |

**Power:** Heater 1500W · LED 20W

**Modules:** `shop` (paid effects), `cost` (energy tracking)


### Evonic ROT

#### `rot1250`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 10 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 68 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `rot1500`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 12 | `#ff5000` | 200 | 255 | 0 |
| 1 | GPIO3 | 80 | `#ff5000` | 200 | 255 | 0 |

**Power:** Heater 1513W · LED 28W

**Modules:** `shop` (paid effects), `cost` (energy tracking)


### Evonic SL

#### `sl1000`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 41 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 41 | `#ff4800` | 140 | 255 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `sl1250`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 63 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 63 | `#ff4800` | 140 | 255 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `sl1500`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 67 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 67 | `#ff4800` | 140 | 255 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `sl600`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 23 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 23 | `#ff4800` | 140 | 255 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)

#### `sl700`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 23 | `#ff4800` | 90 | 255 | 49 |
| 1 | GPIO3 | 23 | `#ff4800` | 140 | 255 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `cost` (energy tracking)


### Evonic V-Series

#### `v1030`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 41 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 56 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `v630`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 23 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 33 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)

#### `v730`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO15 | Lightbox | #3 | ON | No |
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 23 | `#0000ff` | 220 | 255 | 55 |
| 1 | GPIO3 | 33 | `#ff2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 23W

**Modules:** `light_box` (feature light), `shop` (paid effects), `cost` (energy tracking)


### Micon Alisio

#### `alisio1150`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 256 | `#ff5000` | 40 | 255 | 16 |
| 1 | GPIO3 | 55 | `#FF2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 19W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `alisio1550`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 256 | `#ff5000` | 40 | 255 | 16 |
| 1 | GPIO3 | 82 | `#FF2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 19W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `alisio1850`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 256 | `#ff5000` | 40 | 255 | 16 |
| 1 | GPIO3 | 88 | `#FF2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 19W

**Modules:** `shop` (paid effects), `cost` (energy tracking)

#### `alisio850`

**Output pins:**

| GPIO | Name | Output # | Start State | Inverted |
|------|------|----------|-------------|----------|
| GPIO14 | Fire | #1 | OFF | No |
| GPIO12 | Heater | #2 | OFF | No |

**LED strips (WS2812):**

| Segment | GPIO | LED Count | Default Colour | Speed | Brightness | Dynamic |
|---------|------|-----------|---------------|-------|------------|---------|
| 0 | GPIO1 | 256 | `#ff5000` | 40 | 255 | 16 |
| 1 | GPIO3 | 40 | `#FF2500` | 100 | 170 | 16 |

**Power:** Heater 1513W · LED 19W

**Modules:** `shop` (paid effects), `cost` (energy tracking)


---

## Config File Format Reference

The `configs/*.txt` files are the firmware boot configuration. Each directive
maps directly to hardware initialisation code in the ESP8266 firmware.

```
// Comments are ignored
PINOUT <gpio> <output_number> <start_state> <inverted> <name>
RGB    <gpio> <segment> <led_count> <start_state> <hex_color> <speed> <brightness> <dynamic>
GRID   <gpio> <segment> <led_count> <start_state> <hex_color> <speed> <brightness> <dynamic>
SHIMOUT <gpio> <channel> <brightness> <inverted> <name>
DS18B20 <gpio>                    // 1-Wire temperature sensor
RCP    <baud> <tx_gpio> <rx_gpio> <set_gpio>   // RF remote (JDY-40)
BUZZER <gpio>
NTP    <server1> <server2>
ALEXA                             // Enable cloud/Alexa/Google control
TIMERS                            // Enable timer scheduler
MOODLIGHT                         // Enable mood light discovery
UPGRADE                           // Enable OTA upgrade check
ADMIN                             // Enable admin mode (# prefix to disable)
mADD   <module_key>               // Enable a firmware module
param add <key> <value>           // Set a default parameter value
```