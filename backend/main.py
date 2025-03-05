from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from src.tests.parametrizedArray import setupArrFromJSON
import numpy as np
from src.lib.room.roomGeometry import Room
from src.lib.weather.weather import Weather
from src.lib.hvac.hvac import HVAC
from simulation import Simulation
import csv
import threading
import random
import pytz
import datetime, timedelta
import asyncio
import time
from fastapi import WebSocket
import requests
from src.MQTT_Client.mqtt_publish import *


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def initializeWeather():
    with open("data.json", "r") as f:
        data = json.load(f)
    weather = Weather(data["weatherTemperature"])
    return weather

def initializeRoom():
    heatLossCoefficient = 0.8
    with open("data.json", "r") as f:
        data = json.load(f)
    roomData = data.get("room")
    room = Room(roomData["height"], roomData["width"], roomData["length"], heatLossCoefficient, weather)
    return room

def initializeSimType():
    with open("data.json", "r") as f:
        data = json.load(f)
    sim_type = data.get("simulationType")
    return sim_type

hvac: HVAC = HVAC()

@app.post("/changeHVACsettings")
def change_settings(data: dict):
    if websocket:
        hvac_settings = data.get("hvac_settings")
        setpoint = hvac_settings["setpoint"]
        isOn = hvac_settings["isOn"]
        mode = hvac_settings["selectedMode"]
        fanMode = hvac_settings["selectedFanMode"]
        arrayParam = []
        arrayParam.append([0,setpoint, mode, isOn])
        hvac.setHvac(arrayParam,0)
        if fanMode != "AUTO":
            hvac.isFanAuto = False
        else:
            hvac.isFanAuto = True
        
        if hvac.isFanAuto == False:
            enumFan = HVAC.HVAC_AirFlowLevel.LOW
            if fanMode == "HIGH":
                enumFan = HVAC.HVAC_AirFlowLevel.HIGH
            elif fanMode == "MEDIUM":
                enumFan = HVAC.HVAC_AirFlowLevel.MEDIUM
            hvac.changeFanPower(enumFan)
        
    return {"message": "HVAC settings changed successfully"}

@app.post("/setupRealTime")
def save_data_realtime(data: dict):
    with open("data.json", "w") as f:
        json.dump(data, f)
    global sim_type
    sim_type = initializeSimType()
    global weather
    global room
    weather = initializeWeather()
    room = initializeRoom()
    return {"message": "Data saved successfully"}

@app.post("/restoreEffAnomaly")
def restoreEffAnomaly():
    hvac.efficiency = 0.98
    return {"message": "Efficiency anomaly has been disabled."}

@app.post("/efficiencyAnomaly")
def efficiencyAnomaly():
    hvac.efficiency = 0.2
    return {"message": "Efficiency anomaly is active."}

@app.post("/thresholdAnomaly")
def thresholdAnomaly():
    hvac.tempDiff = 4
    return {"message": f"Threshold anomaly set to {hvac.tempDiff}."}

@app.post("/restoreThreshAnomaly")
def restoreThreshAnomaly():
    hvac.tempDiff = 2
    return {"message": f"Threshold anomaly restored to original value {hvac.tempDiff}."}


@app.post("/lossOfPowerAnomaly")
def lossOfPowerAnomaly():
    thread = threading.Thread(target=actuate_loss_of_power)
    thread.start()
    thread.join()
    return {"message": "Loss of power anomaly ended"}


# Main loss of power function
def actuate_loss_of_power():
    power_aux = hvac.Power_Watt
    for i in range(20):
        rand = random.randint(0, 1)
        if(rand == 1):
            hvac.Power_Watt = power_aux / 2
        else:
            hvac.Power_Watt = power_aux
        time.sleep(1)
        i+=1
    hvac.Power_Watt = power_aux


#default implementation of variables for anomaly programming on demand
startDateProg = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc).strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
endDateProg = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc).strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
progAnomalyName = "none"

@app.post("/sendEffAnomalyProg")
def sendEffAnomalyProg(data: dict):
    global startDateProg, endDateProg, progAnomalyName
    startDateProg = datetime.datetime.strptime(data["dateFrom"], '%Y-%m-%d %H:%M:%S')
    endDateProg = datetime.datetime.strptime(data["dateTo"], '%Y-%m-%d %H:%M:%S')
    progAnomalyName = "efficiency"
    print(f"date from {startDateProg} to {endDateProg}")


@app.post("/sendthresholdAnomalyProg")
def sendthresholdAnomalyProg(data: dict):
    global startDateProg, endDateProg, progAnomalyName
    startDateProg = datetime.datetime.strptime(data["dateFrom"], '%Y-%m-%d %H:%M:%S')
    endDateProg = datetime.datetime.strptime(data["dateTo"], '%Y-%m-%d %H:%M:%S')
    progAnomalyName = "threshold"
    print(f"date from {startDateProg} to {endDateProg}")


@app.post("/sendFaultAnomalyProg")
def sendFaultAnomalyProg(data: dict):
    global startDateProg, endDateProg, progAnomalyName
    startDateProg = datetime.datetime.strptime(data["dateFrom"], '%Y-%m-%d %H:%M:%S')
    endDateProg = datetime.datetime.strptime(data["dateTo"], '%Y-%m-%d %H:%M:%S')
    progAnomalyName = "fault"
    print(f"date from {startDateProg} to {endDateProg}")


@app.post("/sendLOPAnomalyProg")
def sendLOPAnomalyProg(data: dict):
    global startDateProg, progAnomalyName
    startDateProg = datetime.datetime.strptime(data["dateFrom"], '%Y-%m-%d %H:%M:%S')
    progAnomalyName = "lossOfPower"
    print(f"date from {startDateProg} to -----")
    
def applyAnomlayProg(isAnomalyActive: bool):
    if isAnomalyActive:
        if(progAnomalyName == "efficiency"):
            hvac.efficiency = 0.2
        elif(progAnomalyName == "threshold"):
            hvac.tempDiff = 4
        elif(progAnomalyName == "fault"):
            hvac.faulty = True
        
    else:
        if(progAnomalyName == "efficiency"):
            hvac.efficiency = 0.98
        elif(progAnomalyName == "threshold"):
            hvac.tempDiff = 2
        elif(progAnomalyName == "fault"):
            hvac.faulty = False


@app.post("/restoreFaultAnomaly")
def restoreFaultAnomaly():
    hvac.faulty = False
    return {"message": f"Fault anomaly has been disabled."}

@app.post("/faultAnomaly")
def faultAnomaly():
    hvac.faulty = True
    return {"message": f"Fault anomaly is active."}

@app.post("/setupParameterized")
def save_data_param(data: dict):
    with open("data.json", "w") as f:
        json.dump(data, f)
    global sim_type
    sim_type = initializeSimType()
    global param_arr
    param_arr = setupArrFromJSON("data.json")
    global weather
    global room
    weather = initializeWeather()
    room = initializeRoom()
    hvac = HVAC()
    return {"message": "Data saved successfully"}


@app.post("/")
async def save_data():
    return {"message": "dafault address"}

interrupt_signal = threading.Event()

@app.post("/interrupt")
def interrupt_simulation():
    global interrupt_signal
    interrupt_signal.set()
    return {"message": "Simulation interrupted"}


async def run_simulationRealTime():
    sim = Simulation()
    initializeRoom()
    initializeWeather()
    interrupt_signal.clear()
    
    await async_connectClient()
    if(isWebSocketOpen()is False):
        return {"message": "Websocket connection is not open, please open the connection and try again","isResCorrect": False}
    await sim.run_simulation_realtime(hvac, room, weather, interrupt_signal,sendRowToClient,send_post_call)
    
    # Read the content of the CSV file
    #await closeSocket()
    disconnectClient()
    csv_content = []
    with open("./src/data_realtime.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_content.append(row)
    return {"message": "Simulation completed successfully", "csv_content": csv_content}


@app.post("/simulateRealTime")
def simulationRoute():
    thread = threading.Thread(target=asyncio.run, args=(run_simulationRealTime(),))
    thread.start()
    return {"message": "Simulation started successfully"}

async def closeSocket():
    await websocket.close()

@app.post("/simulateParameterized")
def run_simulationParam():
    sim = Simulation()
    initializeRoom()
    initializeWeather()

    try:
        sim.run_simulation_parameterized(param_arr, hvac, room, weather,startDateProg,endDateProg,applyAnomlayProg,progAnomalyName)	
    except Exception as e:
        return {"message": f"{e}","isResCorrect": False}
    # Read the content of the CSV file
    csv_content = []
    with open("./src/data.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_content.append(row)
    
    return {"message": "Simulation completed successfully, download data using the following button", "csv_content": csv_content, "isResCorrect": True}

websocket : WebSocket = None
@app.websocket("/ws")
async def websocket_endpoint(stream: WebSocket):
    global websocket
    websocket = stream
    await websocket.accept()
    try:
        data = await websocket.receive_text()
    except Exception as e:
        print(f"Connection closed in exception: {e}")
    finally:
        print(f"Connection closed correctly")
        await websocket.close()

def isWebSocketOpen():
    return websocket is not None


async def sendRowToClient(message: str) -> None:
    print(f"Sending message: {message}")
    await websocket.send_text(message)
    

async def send_post_call(data: dict,clock):
    publish_data(data,clock)
    
