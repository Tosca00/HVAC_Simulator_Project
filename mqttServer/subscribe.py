import paho.mqtt.client as mqtt
from fastapi import FastAPI
import asyncio

app = FastAPI()

# Define the MQTT server details
MQTT_BROKER = "localhost"
MQTT_PORT = 1883  # Standard MQTT port
MQTT_TOPIC = "v1/gateway/telemetry"

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop in a separate thread
def start_mqtt():
    client.loop_forever()

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_mqtt)

@app.post("/")
async def read_root():
    return {"message": "MQTT Subscriber is running"}