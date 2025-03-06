import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from src.lib.hvac.hvac import HVAC
from src.lib.room.roomGeometry import *
from src.lib.weather import Weather
from src.lib.agent.Agent import *
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import pytz
import datetime
from src.data import *
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from src.tests.parametrizedArray import *


#classe contiene le due simulazioni, una in tempo reale e una parametrizzata
class Simulation:

    #variabili ausiliarie per il debug dei grafi e liste, utilizzate quando il codice era scritto interamente su python 
    debugLists = False
    debugGraphs = False

    #funzione per la simulazione in tempo reale
    async def run_simulation_realtime(self, hvac: HVAC, room: Room, weather: Weather, stop_signal: threading.Event, sendRowToClient, publishMQTT):
        #inizializzazioni
        room.setTemperature(weather.getDegrees())
        # at start time hvac and room temperature are the same
        hvac.setTemperature_Internal(room.temperature)
        df = pd.DataFrame(columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp', 'Mode', "Ambient_Temperature", "Fan_Level"])
        # initialize clock for simulation
        clock_tz = pytz.timezone('Europe/Rome')
        rome_date = datetime.datetime.now(clock_tz)
        print(f"SIMULATION START TIME : {rome_date.strftime('%Y-%m-%d %H:%M:%S')}")

        # initialize agent
        agent = Agent()
        agent.classes_dict['HVAC'] = hvac
        agent.classes_dict['Room'] = room
        agent.classes_dict['Weather'] = weather
        startTime = datetime.datetime.now(clock_tz)

        hvac.setTemperature_Internal(room.temperature)

        #creazione di array parametrizzati per la simulazione in tempo reale e setup
        data: dict
        with open("data.json", "r") as f:
            data = json.load(f)
        hvac_settings = data.get("hvac_settings")
        setpoint = hvac_settings["setpoint"]
        isOn = hvac_settings["isOn"]
        mode = hvac_settings["selectedMode"]
        fanMode = hvac_settings["selectedFanMode"]
        arrayParam = []
        arrayParam.append([0,setpoint, mode, isOn])

        hvac.setHvac(arrayParam,0)

        #in futuro sarebbe da implementare nella inizializzazione da array parametrico
        if fanMode != "AUTO":
            agent.classes_dict['HVAC'].isFanAuto = False
        
        enumFan = HVAC.HVAC_AirFlowLevel.LOW
        if fanMode == "HIGH":
            enumFan = HVAC.HVAC_AirFlowLevel.HIGH
        elif fanMode == "MEDIUM":
            enumFan = HVAC.HVAC_AirFlowLevel.MEDIUM
        
        agent.classes_dict['HVAC'].changeFanPower(enumFan)

        #ciclo di simulazione principale
        while not stop_signal.is_set():
            try:
                startTime = datetime.datetime.now(clock_tz).replace(microsecond=0, tzinfo=None)
                agent.tick()
                df = pd.concat([df, pd.DataFrame([[agent.classes_dict['HVAC'].getTemperature_Internal(), agent.classes_dict['HVAC'].getSetpoint(), agent.classes_dict['HVAC'].getPowerConsumption(), startTime, agent.classes_dict['HVAC'].getHVACMode().name, weather.getDegrees(), agent.classes_dict['HVAC'].air_flow_level.name]], columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp', 'Mode', "Ambient_Temperature","Fan_Level"])], ignore_index=True)
                await sendRowToClient(f"{agent.classes_dict['HVAC'].getTemperature_Internal()},{agent.classes_dict['HVAC'].getSetpoint()},{agent.classes_dict['HVAC'].getPowerConsumption()},{startTime},{agent.classes_dict['HVAC'].getHVACMode()},{weather.getDegrees()},{agent.classes_dict['HVAC'].state},{agent.classes_dict['HVAC'].air_flow_level.name}")
                await publishMQTT(agent,startTime)
                time.sleep(1)
            except KeyboardInterrupt:
                print("SIMULATION INTERRUPTED BY USER COMMAND")
                break

        print("SIMULATION ENDED")
        #salva dati su file csv al termine della simulazione
        df.to_csv('./src/data_realtime.csv', index=False)
        if self.debugGraphs:
            plot_temperaturesAndSetpoint(df)
            plot_powerConsumption(df)
        if self.debugLists:
            print(df)


    #funzione per la simulazione parametrizzata
    def run_simulation_parameterized(self,parametrized_array,hvac :HVAC,room :Room,weather :Weather, startDateProg :datetime.datetime, endDateProg :datetime.datetime,applyAnomlayProg: callable,progAnomalyName :str):
        
        #inizializzazioni
        #initialize room temperature
        room.setTemperature(weather.getDegrees())
        #at start time hvac and room temperature are the same
        hvac.setTemperature_Internal(room.temperature)

        #initialize dataframe
        df = pd.DataFrame(columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp', 'Mode',"Ambient_Temperature","Fan_Level"])

        #initialize clock for simulation
        clock_tz = pytz.timezone('Europe/Rome')
        rome_date = datetime.datetime.now(clock_tz)
        print(f"SIMULATION START TIME : {rome_date.strftime('%Y-%m-%d %H:%M:%S')}")

        #initialize agent
        agent = Agent()
        agent.classes_dict['HVAC'] = hvac
        agent.classes_dict['Room'] = room
        agent.classes_dict['Weather'] = weather

        startTime = datetime.datetime.strptime(parametrized_array[0][0], '%Y-%m-%d %H:%M:%S')

        #set the hvac with the parameters of the first row of the array
        try:
            hvac.setHvac(parametrized_array,0)
            check_array_params(parametrized_array)
        except ValueError as e:
            raise e

        #counter e ausiliarie per la durata dell'anomalia lossOfPower
        i = 0
        progLOP_counter = 0
        progLOP_canStart = False
        power_aux = hvac.Power_Watt
        
        #ciclo principale di simulazione
        try:
            while startTime <= datetime.datetime.strptime(parametrized_array[len(parametrized_array)-1][0], '%Y-%m-%d %H:%M:%S'): #finchè non si raggiunge l'ultima data programmata
                if parametrized_array[i][0] == startTime.strftime('%Y-%m-%d %H:%M:%S'): # se viene trovata una data programmata, cambio parametri hvac
                    hvac.setHvac(parametrized_array,i)
                    i += 1
                if startTime == startDateProg:
                    progLOP_canStart = True
                    applyAnomlayProg(True)
                if startTime == endDateProg:
                    applyAnomlayProg(False)

                #se l'anomalia è attiva, ogni 30 secondi cambia il consumo di energia a intervalli casuali
                if(progAnomalyName == "lossOfPower" and progLOP_canStart and progLOP_counter <= 30):     
                    rand = random.randint(0,1)
                    print(f"LOP anomaly active with counter {progLOP_counter} and rand : {rand}")
                    if(rand == 1):
                        agent.classes_dict['HVAC'].Power_Watt = power_aux / 2
                    else:
                        agent.classes_dict['HVAC'].Power_Watt = power_aux
                    progLOP_counter +=1
                else:
                    hvac.Power_Watt = power_aux
                    progLOP_canStart = False

                agent.tick()
                df = pd.concat([df, pd.DataFrame([[agent.classes_dict['HVAC'].getTemperature_Internal(), agent.classes_dict['HVAC'].getSetpoint(), agent.classes_dict['HVAC'].getPowerConsumption(), startTime, agent.classes_dict['HVAC'].getHVACMode().name, weather.getDegrees(),agent.classes_dict['HVAC'].air_flow_level.name]], columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp', 'Mode', "Ambient_Temperature","Fan_Level"])], ignore_index=True)
                
                startTime += datetime.timedelta(seconds=1)
                
        except KeyboardInterrupt :
            print("SIMULATION INTERRUPTED BY USER COMMAND")
            exit()

        #print(f"found {i} dates.")
        # Create and save DataFrame after the simulation loop ends
        #print(f"total time elapsed : {str(time_counter)} seconds")
        df.to_csv('./src/data.csv', index=False)
        #print(f"startTime value : {parametrized_array[len(parametrized_array)-1][0]}")
        #print(f"room temperature : {str(room.temperature)} °C")
        if self.debugGraphs:
            plot_temperaturesAndSetpoint(df)
            plot_powerConsumption(df)
            print(df)

        if self.debugLists :
            print("----------------------------")
        
        print("simulation ended")




#semplice generazione grafici in python, non più utilizzate
def plot_temperaturesAndSetpoint(df):
    df_copy = df.copy()
    df_copy['Timestamp'] = pd.to_datetime(df_copy['Timestamp'])
    df_copy.set_index('Timestamp', inplace=True)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=df_copy.index, y='Temperature', data=df_copy, label='Temperature', color='orange')
    sns.lineplot(x=df_copy.index, y='Setpoint', data=df_copy, label='Setpoint', color='blue')
    sns.lineplot(x=df_copy.index, y='Ambient_Temperature', data=df_copy, label='Ambient Temperature', color='green')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Temperature and Setpoint')
    plt.xticks(rotation=90)
    
    # Format the x-axis to show time properly
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    

def plot_powerConsumption(df):
    df_copy = df.copy()
    df_copy['Timestamp'] = pd.to_datetime(df_copy['Timestamp'])
    df_copy.set_index('Timestamp', inplace=True)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_copy, x=df_copy.index, y='Watts', color='green', label='Power Consumption')
    plt.title('Power Consumption Over Time')
    plt.xlabel('Time')
    plt.ylabel('Watts')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()