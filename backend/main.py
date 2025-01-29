from fastapi import FastAPI
#from .simulation import Simulation

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "HVAC Sim API"}

@app.get("/simulate")
def run_simulation():
    #sim_instance = Simulation()
    #result = sim_instance.run_simulation_parameterized()
    return {"message": "testing"}