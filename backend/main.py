from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from src.tests.parametrizedArray import setupArrFromJSON,printArr
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
import time

app = FastAPI()

#Define the parameterized array
#param_arr: np.array = np.empty((0, 4), dtype=object)



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
    hvac_settings = data.get("hvac_settings")
    setpoint = hvac_settings["setpoint"]
    isOn = hvac_settings["isOn"]
    mode = hvac_settings["selectedMode"]
    arrayParam = []
    arrayParam.append([0,setpoint, mode, isOn])
    hvac.setHvac(arrayParam,0)
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
    return {"message": "Efficiency anomaly restored successfully"}

@app.post("/efficiencyAnomaly")
def efficiencyAnomaly():
    hvac.efficiency = 0.2
    return {"message": "Efficiency anomaly set successfully"}

@app.post("/thresholdAnomaly")
def thresholdAnomaly():
    hvac.tempDiff = 4
    return {"message": f"Threshold anomaly set to {hvac.tempDiff}"}

@app.post("/restoreThreshAnomaly")
def restoreThreshAnomaly():
    hvac.tempDiff = 2
    return {"message": f"Threshold anomaly restored to {hvac.tempDiff}"}


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
    
@app.post("/restoreFaultAnomaly")
def restoreFaultAnomaly():
    hvac.faulty = False
    return {"message": f"Fault anomaly restored to {hvac.faulty}"}

@app.post("/faultAnomaly")
def faultAnomaly():
    hvac.faulty = True
    return {"message": f"Fault anomaly set to {hvac.faulty}"}

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
async def save_data(data: dict):
    return {"message": "dafault address"}

interrupt_signal = threading.Event()

@app.post("/interrupt")
def interrupt_simulation(data: dict):
    global interrupt_signal
    interrupt_signal.set()
    return {"message": "Simulation interrupted"}

@app.post("/simulateRealTime")
def run_simulation():
    sim = Simulation()
    initializeRoom()
    initializeWeather()
    interrupt_signal.clear()
    sim.run_simulation_realtime(hvac, room, weather, interrupt_signal)

    # Read the content of the CSV file
    csv_content = []
    with open("./src/data_realtime.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_content.append(row)
    
    return {"message": "Simulation completed successfully", "csv_content": csv_content}

@app.post("/simulateParameterized")
def run_simulation():
    sim = Simulation()
    initializeRoom()
    initializeWeather()

    sim.run_simulation_parameterized(param_arr, hvac, room, weather)	

    # Read the content of the CSV file
    csv_content = []
    with open("./src/data.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_content.append(row)
    
    return {"message": "Simulation completed successfully", "csv_content": csv_content}
