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

async def async_connectClient():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, connectClient)

def publish_data(agent: Agent,clock):
    timestamp = clock.strftime('%Y-%m-%d %H:%M:%S')
    
    if agent.classes_dict['HVAC'].getHVACMode() == HVAC.HVAC_Mode.HEATING:
        mode = "HEATING"
    elif agent.classes_dict['HVAC'].getHVACMode() == HVAC.HVAC_Mode.COOLING:
        mode = "COOLING"
    else:
        mode = "NO_MODE"

    if agent.classes_dict['HVAC'].getHVAC_State() == HVAC.HVAC_State.OFF:
        status = "OFF"
    elif agent.classes_dict['HVAC'].getHVAC_State() == HVAC.HVAC_State.ON:
        status = "ON"
    else:
        status = "INACTIVE"

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
                    "mode":mode,
                    "status": status,
                    "power": agent.classes_dict['HVAC'].getPowerConsumption()
                }
            }
        ]
    }
    client.publish("v1/gateway/telemetry", json.dumps(agent_data))


def disconnectClient():
    client.disconnect()
    return 0