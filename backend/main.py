from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
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
    return {"message": "Data saved successfully"}


@app.get("/simulate")
def run_simulation():
    #sim_instance = Simulation()
    #result = sim_instance.run_simulation_parameterized()
    return {"message": "testing"}