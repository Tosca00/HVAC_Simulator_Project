import paho.mqtt.client as mqtt
from src.lib.agent.Agent import *
import asyncio
import json

mqtt_broker = "mosquitto"
mqtt_port = 1883
client = mqtt.Client("Simulation_Data")


def connectClient():
    client.connect(mqtt_broker, mqtt_port, 60)
    return 0

async def async_connectClient():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, connectClient)

def publish_data(agent: Agent):
    agent_data = json.dumps(agent.__dict__)
    client.publish("v1/gateway/telemetry", agent_data)