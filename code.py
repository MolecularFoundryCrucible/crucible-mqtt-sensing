import time
import ssl
import wifi
import socketpool
import board
import os
import adafruit_bme680
from adafruit_minimqtt import adafruit_minimqtt

#---mqtt settings---
SENSOR_ID = "bme688-001"
TOPIC_HUMIDITY = f"cruxtel/mf/inorganic/spinbot/env/lq/{SENSOR_ID}/humidity" # relative hum, %
TOPIC_TEMP = f"cruxtel/mf/inorganic/spinbot/env/lq/{SENSOR_ID}/temperature" # deg C

PUBLISH_INTERVAL = 30  # seconds

# --- Set up I2C and sensor ---
i2c = board.I2C()  # uses board.SCL, board.SDA
bme688 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# --- Connect to WiFi ---
print("Connecting to WiFi...")
wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
print(f"Connected! IP: {wifi.radio.ipv4_address}")

# --- Set up MQTT client ---
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

mqtt_client = adafruit_minimqtt.MQTT(
    broker=os.getenv("MQTT_BROKER"),
    port=int(os.getenv("MQTT_PORT")),
    username=os.getenv("MQTT_USERNAME"),
    password=os.getenv("MQTT_PASSWORD"),
    socket_pool=pool,
    ssl_context = ssl_context,
    is_ssl = True,
    client_id=f"cruxtel-{SENSOR_ID}",
)

def connect_mqtt():
    print("Connecting to MQTT broker...")
    mqtt_client.connect()
    print("Connected to MQTT broker!")

try:
    connect_mqtt()
except Exception as e:
    print(f"Raw error: {type(e).__name__}: {e}")
    raise

# --- Main loop ---
while True:
    try:
        # minimqtt needs regular servicing to keep the connection alive
        mqtt_client.loop()

        humidity = bme688.humidity
        temperature = bme688.temperature

        print(f"Humidity: {humidity:.1f}%  Temperature: {temperature:.1f} C")

        mqtt_client.publish(TOPIC_HUMIDITY, f"{humidity:.2f}", retain= True)
        mqtt_client.publish(TOPIC_TEMP, f"{temperature:.2f}", retain=True)

        time.sleep(PUBLISH_INTERVAL)

    except (ConnectionError, OSError) as e:
        print(f"Connection issue: {e}. Reconnecting...")
        try:
            wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
            connect_mqtt()
        except Exception as reconnect_error:
            print(f"Reconnect failed: {reconnect_error}")
            time.sleep(5)




