'''
Simulatore HVAC

Obbiettivo prima release : 
                    inizializzazione variabili (basiche e di controllo),
                    1 minuto condizionatore spento,
                    dopo il primo minuto cambio setpoint,
                    al raggiungimento condizionatore si spegne

Bozza pseudocodice :
    Inizializzazione variabili : 
        T.Interna = 18 [C°]
        T.Setpoint = 5 [C°]
        Time_Refresh = 1 [s]
        Consumo = 0 [W]
        TotaleConsumo = 0 [W]
        Clock object
    while T.Interna <= T.Setpoint
        iterazione Time_Refresh
            if timer > 60 secondi
                aggiornare temperatura e consumo


Valori di controllo : 
    deltaEnergia -> Quanta energia consuma il condizionatore in deltaT
    deltaTemperatura -> Quanto cambia la temperatura interna in deltaT

Obiettivo seconda release :
    Inizializzazione variabili (basiche e di controllo),
    accendere il condizionatore a un orario specifico,
    setpoint 22 [C°], temperatura interna 21 [C°],
    Dopo un certo orario si cambia setpoint a 19 [C°], il condizionatore (dovrebbe) spegnersi (da verificare),
    implementare un modello per il contenimento e/o la riduzione della temperatura interna


    nota : condizionatore consuma fino a 800 watt in picco potenza
           potrebbe essere che con 600 watt la temperatura aumenti da 21 a 24 in 6 minuti

'''

import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from src.lib.hvac.hvac import HVAC
from src.lib.room.init import *
import tkinter as tk
from tkinter import simpledialog
import pytz
import datetime
from src.data import *
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates


#aux variables for debugging 
debugLists = False
debugGraphs = True

#semplice funzione una finestra grafica, usata in un thread per non bloccare il main
def modify_setpoint(hvac: HVAC):
    root = tk.Tk()
    root.withdraw()
    while True:
        new_setpoint = simpledialog.askinteger("Input", "Inserisci nuovo setpoint:") #il setpoint deve essere un intero 
        if new_setpoint is not None:
            hvac.setSetpoint(new_setpoint)
        else:
            break


def main():
        #basic variables
        hvac = HVAC()
        time_refresh = 1 #seconds

        #for graphs
        setpoints = []
        temperatures = []
        watts = []
        timestamps = []

        #control variables
        deltaTemp = 0.002 #quanto cambia la temperatura interna in deltaT
        deltaConsumption = 1.2 #quanta energia consuma il condizionatore in deltaT, in kW, al  momento non ha uno scopo ben definito
        setpoint = 22
        temperature = 21
        hvac.setPowerConsumption(deltaConsumption)
        hvac.setTemperature_Internal(temperature)
        hvac.setSetpoint(setpoint)

        startTimer = round(time.time(),0)
        consumtionTimer = time.time()
        startTime = time.gmtime()

        sp_thread = threading.Thread(target=modify_setpoint, args=(hvac,), daemon=True)
        sp_thread.start()

        df = pd.DataFrame(columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp', 'Mode'])

        clock_tz = pytz.timezone('Europe/Rome')
        rome_date = datetime.datetime.now(clock_tz)
        print(f"SIMULATION START TIME : {rome_date.strftime('%Y-%m-%d %H:%M:%S')}")
       
        try:
            time_counter = 0
            while True: #perchè la simulazione è continua
                timerAux = time.time() - consumtionTimer
                consumtionTimer = time.time()
                
                if hvac.getHVACMode() == hvac.HVAC_Mode.COOLING:
                    mode = "COOLING"
                elif hvac.getHVACMode() == hvac.HVAC_Mode.HEATING:
                    mode = "HEATING"
                else:
                    mode = "NO MODE" 
                df = pd.concat([df, pd.DataFrame([[hvac.getTemperature_Internal(), hvac.getSetpoint(), hvac.calculate_consumption(timerAux), datetime.datetime.now(clock_tz).strftime('%Y-%m-%d %H:%M:%S'), mode]], columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp','Mode'])], ignore_index=True)
                df.to_csv('src/data.csv', index=False)

                hvac.CoolingOrHeating(deltaTemp,setpoint)
                if hvac.getHVAC_State() == HVAC.HVAC_State.OFF:
                    hvac.setTemperature_Internal(hvac.getTemperature_Internal() - loseTemp())
                print(f"watts : {str(df.tail(1)['Watts'].values)} W")
                hvac.PrintStatus()
                
                time.sleep(time_refresh) #per aggiornare il sistema a intervalli deltaT
                time_counter = (round(time.time(),0) - startTimer)
        except KeyboardInterrupt :
            print("SIMULATION INTERRUPTED BY USER COMMAND")
            exit_command = True
            pass

        # Create and save DataFrame after the simulation loop ends
        print(f"total time elapsed : {str(time_counter)} seconds")
        print(f"SIMULATION END TIME: {rome_date.strftime('%Y-%m-%d %H:%M:%S')}")

        max_watt_row = df.loc[df['Watts'].idxmax()]
        max_watt_time = datetime.datetime.strptime(max_watt_row['Timestamp'], '%Y-%m-%d %H:%M:%S')
        max_watt_time = clock_tz.localize(max_watt_time)
        print(f"maximum consumption is {max_watt_row['Watts']} W reached at {max_watt_time.strftime('%Y-%m-%d %H:%M:%S')}")

        #set variables for debugging
        if debugGraphs and exit_command == True:
            '''
            drawTemperatureGraph(temperatures,setpoints)
            drawPowerConsumptionGraph(watts)
            '''
            plot_temperaturesAndSetpoint(df)
            plot_powerConsumption(df)
            print(df)

        if debugLists :
            print("----------------------------")
            print(watts)





def plot_temperaturesAndSetpoint(df):
    df_copy = df.copy()
    df_copy['Timestamp'] = pd.to_datetime(df_copy['Timestamp'])
    df_copy.set_index('Timestamp', inplace=True)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=df_copy.index, y='Temperature', data=df_copy, label='Temperature', color='orange')
    sns.lineplot(x=df_copy.index, y='Setpoint', data=df_copy, label='Setpoint', color='blue')
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



def drawPowerConsumptionGraph(watts):
    plt.figure(figsize=(8,4))
    plt.plot(watts, label='Power Consumption', color='green')
    plt.xlabel('Time (GMT)')
    plt.ylabel('Watts')
    plt.title('Power Consumption Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


def drawTemperatureGraph(temperatures,setpoints):
    plt.figure(figsize=(8,4))
    plt.plot(temperatures, label='Temperature',color='red')
    plt.plot(setpoints, label='Setpoint',color='blue')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature and setpoint')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
        main()