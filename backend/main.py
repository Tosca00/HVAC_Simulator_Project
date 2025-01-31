from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from .simulation import Simulation

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "HVAC Sim API"}

@app.get("/simulate")
def run_simulation():
    #sim_instance = Simulation()
    #result = sim_instance.run_simulation_parameterized()
    return {"message": "testing"}