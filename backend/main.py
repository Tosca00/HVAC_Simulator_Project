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

@app.post("/")
async def save_data(data: dict):
    with open("data.json", "w") as f:
        json.dump(data, f)
    global param_arr
    global weather
    global room
    global sim_type
    weather = initializeWeather()
    room = initializeRoom()
    sim_type = initializeSimType()
    param_arr = setupArrFromJSON("data.json")
    return {"message": "Data saved successfully"}



@app.post("/simulate")
def run_simulation():
    hvac = HVAC()
    sim = Simulation()
    initializeRoom()
    initializeWeather()
    #sim.run_simulation_parameterized(param_arr, hvac, room, weather)
    if sim_type == 0:
        #sim.run_simulation_parameterized(param_arr, hvac, room, weather)
        return {"message": "parameterized"}
    else:
        #sim.run_simulation_realtime(hvac, room, weather)
        return {"message": "realtime"}

    # Read the content of the CSV file
    csv_content = []
    with open("./src/data.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_content.append(row)
    
    return {"message": "Simulation completed successfully", "csv_content": csv_content}
