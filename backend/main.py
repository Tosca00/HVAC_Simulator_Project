from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from src.tests.parametrizedArray import setupArrFromJSON,printArr
#from .simulation import Simulation

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def save_data(data: dict):
    with open("data.json", "w") as f:
        json.dump(data, f)
    param_arr = setupArrFromJSON("data.json")
    return {"message": "Data saved successfully"}



@app.get("/simulate")
def run_simulation():
    setupArrFromJSON("data.json")