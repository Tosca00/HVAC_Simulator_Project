import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from backend.src.lib.hvac.hvac import HVAC
from backend.src.lib.room.roomGeometry import *
from backend.src.lib.weather import Weather
from backend.src.lib.agent.Agent import *
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import pytz
import datetime, timedelta
from backend.src.data import *
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from backend.src.tests.parametrizedArray import *

class Simulation:

    #aux variables for debugging 
    debugLists = False
    debugGraphs = True

    def __init__(self):
        self.hvac = HVAC()
        self.weather = Weather(25,50,80,70,1.225,)
        self.room = Room(4,3,5,25,0.2,self.weather)
        self.agent = Agent()

    def run_simulation_parameterized(self):
        #at start time hvac and room temperature are the same
        self.hvac.setTemperature_Internal(self.room.temperature)

        #initialize dataframe
        df = pd.DataFrame(columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp', 'Mode',"Ambient_Temperature"])

        #initialize clock for simulation
        clock_tz = pytz.timezone('Europe/Rome')
        rome_date = datetime.datetime.now(clock_tz)
        print(f"SIMULATION START TIME : {rome_date.strftime('%Y-%m-%d %H:%M:%S')}")

        #initialize agent
        agent = Agent()
        agent.classes_dict['HVAC'] = self.hvac
        agent.classes_dict['Room'] = self.room
        agent.classes_dict['Weather'] = self.weather

        startTime = datetime.datetime.strptime(parametrized_array[0][0], '%Y-%m-%d %H:%M:%S')

        #set the hvac with the parameters of the first row of the array
        try:
            self.hvac.setHvac(parametrized_array,0)
            check_array_params(parametrized_array)
        except ValueError as e:
            print(e)
            exit()

        i = 0
        try:
            while startTime <= datetime.datetime.strptime(parametrized_array[len(parametrized_array)-1][0], '%Y-%m-%d %H:%M:%S'):
                if parametrized_array[i][0] == startTime.strftime('%Y-%m-%d %H:%M:%S'):
                    print(f"found date : {i} of {len(parametrized_array)-1}")
                    self.hvac.setHvac(parametrized_array,i)
                    i += 1
                #timerAux = time.time() - consumtionTimer
                consumtionTimer = time.time()
                agent.tick()
                #print(f"temperature : {str(hvac.getTemperature_Internal())} °C")
                df = pd.concat([df, pd.DataFrame([[self.hvac.getTemperature_Internal(), self.hvac.getSetpoint(), self.hvac.getPowerConsumption(), startTime, self.hvac.getHVACMode(),self.weather.getDegrees()]], columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp','Mode',"Ambient_Temperature"])], ignore_index=True)
                startTime += datetime.timedelta(seconds=1)
                #print(f"date : {startTime.strftime('%Y-%m-%d %H:%M:%S')}")
                
        except KeyboardInterrupt :
            print("SIMULATION INTERRUPTED BY USER COMMAND")
            exit()

        print(f"found {i} dates.")
        # Create and save DataFrame after the simulation loop ends
        #print(f"total time elapsed : {str(time_counter)} seconds")
        df.to_csv('backend/src/data.csv', index=False)
        print(f"startTime valude : {parametrized_array[len(parametrized_array)-1][0]}")
        #print(f"room temperature : {str(room.temperature)} °C")
        if self.debugGraphs:
            plot_temperaturesAndSetpoint(df)
            plot_powerConsumption(df)
            print(df)

       
        if self.debugLists :
            print("----------------------------")        


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