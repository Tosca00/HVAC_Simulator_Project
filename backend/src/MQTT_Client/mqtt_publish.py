import paho.mqtt.client as mqtt
from src.lib.agent.Agent import *
from src.lib.hvac.hvac import HVAC
import asyncio
import json

mqtt_broker = "mosquitto"
mqtt_port = 1883
client = mqtt.Client("Simulation_Data")


def connectClient():
    client.connect(mqtt_broker, mqtt_port, 60)
    return 0

#necessità di funzione asincrona perchè eseguita in un thread separato
async def async_connectClient():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, connectClient)


def publish_data(agent: Agent,clock):
    timestamp = clock.strftime('%Y-%m-%d %H:%M:%S')

    agent_data = {
        "room": [
            {
                "ts": timestamp,
                "values": {
                    "temperature": agent.classes_dict['HVAC'].getTemperature_Internal()
                }
            }
        ],
        "environment": [
            {
                "ts": timestamp,
                "values": {
                    "temperature": agent.classes_dict["Weather"].getDegrees()
                }
            }
        ],
        "hvac": [
            {
                "ts": timestamp,
                "values": {
                    "setpoint": agent.classes_dict['HVAC'].getSetpoint(),
                    "mode":agent.classes_dict['HVAC'].mode.name,
                    "status": agent.classes_dict['HVAC'].state.name,
                    "power": agent.classes_dict['HVAC'].getPowerConsumption(),
                    "fan_level": agent.classes_dict['HVAC'].air_flow_level.name
                }
            }
        ]
    }
    client.publish("v1/gateway/telemetry", json.dumps(agent_data))


def disconnectClient():
    client.disconnect()
    return 0