import paho.mqtt.client as mqtt
from src.lib.agent.Agent import *

mqtt_broker = "localhost"
mqtt_port = 1883
client = mqtt.Client("Simulation_Data")

def connectClient():
    if client.connect(mqtt_broker, mqtt_port,60) != 0:
        print("Could not connect to MQTT broker")
        exit()

def publish_data(agent: Agent):
    client.publish("v1/gateway/telemetry", agent)