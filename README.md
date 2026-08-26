# Crucible MQTT Sensing

A CircuitPython template for publishing sensor readings from a
Wi-Fi-capable microcontroller to the crucible-printers MQTT broker over TLS. It handles Wi-Fi
and MQTT connection setup, periodic publishing, and reconnection on
failure — the specific board and sensor are just a starting example and can
be swapped out. Please reach out to timkodalle@lbl.gov for access details.

## How it works

`code.py` runs on boot and:

1. Connects to Wi-Fi using credentials from `settings.toml`.
2. Connects to an MQTT broker over SSL/TLS (via `adafruit_minimqtt`).
3. Every `PUBLISH_INTERVAL` seconds (default 30s), reads one or more values
   from a sensor and publishes each to its own MQTT topic.
4. On a connection/socket error, attempts to reconnect to Wi-Fi and the MQTT
   broker before resuming the publish loop.

### Example configuration

The included `code.py` is wired up as a working example using:

- An Adafruit Feather ESP32-S3 Reverse TFT
- A BME680/BME688 environmental sensor over I2C (`board.SCL` / `board.SDA`),
  publishing temperature and humidity to `sensors/temperature` and
  `sensors/humidity`

To adapt it to different hardware, swap the sensor library/import in
`lib/`, update the sensor read calls and topics in the main loop, and adjust
`client_id` accordingly. Anything CircuitPython-compatible with Wi-Fi
(ESP32, RP2040 with a Wi-Fi co-processor, etc.) should work.

## Repository layout

```
code.py                    Main application entry point (runs on boot)
settings.toml.template      Template for CircuitPython environment settings
boot_out.txt                Board/firmware info reported by CircuitPython
lib/                        CircuitPython libraries required by code.py
  adafruit_bme680.mpy
  adafruit_connection_manager.mpy
  adafruit_requests.mpy
  adafruit_ticks.mpy
  adafruit_minimqtt/
sd/                          Placeholder for SD card storage
```

## Setup

1. Copy the settings template and fill in your credentials:

   ```
   cp settings.toml.template settings.toml
   ```

   Edit `settings.toml` with your Wi-Fi and MQTT broker details.


2. Copy `code.py`, `settings.toml`, and the `lib/` directory onto the
   `CIRCUITPY` drive that appears when the board is plugged in via USB.

3. The board will automatically run `code.py` on boot/reset. Open a serial
   console to view connection status and sensor readings.

## Configuration

- `PUBLISH_INTERVAL` in `code.py` controls how often readings are published
  (seconds).
- `client_id` in the MQTT client setup identifies this device on the broker.
- MQTT topics are defined at the top of `code.py` (e.g. `TOPIC_HUMIDITY` and `TOPIC_TEMP`).

## Dependencies

The following CircuitPython libraries (bundled in `lib/`) are required:

- `adafruit_bme680`
- `adafruit_minimqtt`
- `adafruit_connection_manager`
- `adafruit_requests`
- `adafruit_ticks`
