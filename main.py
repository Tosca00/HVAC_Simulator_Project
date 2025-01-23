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
from src.lib.room.roomGeometry import *
from src.lib.weather import Weather
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import pytz
import datetime, timedelta
from src.data import *
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from src.tests.parametrizedArray import *


#aux variables for debugging 
debugLists = False
debugGraphs = True


def buttonOnOff(hvac: HVAC):
    if hvac.getHVAC_State() == HVAC.HVAC_State.OFF:
        hvac.TurnOn()
    else:
        hvac.TurnOff()

#semplice funzione una finestra grafica, usata in un thread per non bloccare il main


def modify_setpoint(hvac):
    def apply_changes():
        input_value = entry.get()
        if input_value:
            try:
                new_setpoint, new_mode = input_value.split()
                new_setpoint = int(new_setpoint)
                hvac.setSetpoint(new_setpoint)

                if new_mode.upper() == "COOLING":
                    hvac.setHVACMode(hvac.HVAC_Mode.COOLING)
                elif new_mode.upper() == "HEATING":
                    hvac.setHVACMode(hvac.HVAC_Mode.HEATING)
                elif new_mode.upper() == "OFF":
                    hvac.setHVACMode(hvac.HVAC_Mode.OFF)
                else:
                    messagebox.showerror("Error", "Invalid mode. Use COOLING, HEATING, or OFF.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Enter setpoint and mode separated by a space.")
        else:
            messagebox.showerror("Error", "Input cannot be empty.")

    root = tk.Tk()
    root.title("HVAC Control")
    root.geometry("300x200")

    label = tk.Label(root, text="Setpoint and Mode (e.g., '23 COOLING')", font=("Arial", 10))
    label.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 12), width=25)
    entry.pack(pady=5)

    button_apply = tk.Button(root, text="Apply", command=apply_changes, fg="blue", font=("Arial", 12), width=10)
    button_apply.pack(pady=5)

    button_toggle = tk.Button(root, text="Turn On/Off", command=lambda: buttonOnOff(hvac), fg="green", font=("Arial", 12), width=15)
    button_toggle.pack(pady=5)

    root.mainloop()

def main():
        #basic variables
        hvac = HVAC()
        time_refresh = 1 #seconds

        weather = Weather(20,50,80,70,1.225,)
        room = Room(4,3,5,25,0.2,weather)

        #control variables
        deltaTemp = 0.002 #quanto cambia la temperatura interna in deltaT
        setpoint = 22
        temperature = 25
        room.setTemperature(temperature)
        hvac.setTemperature_Internal(temperature)
        hvac.setDeltaTemp(deltaTemp)

        startTimer = round(time.time(),0)
        consumtionTimer = time.time()

        #sp_thread = threading.Thread(target=modify_setpoint, args=(hvac,), daemon=True)
        #sp_thread.start()

        df = pd.DataFrame(columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp', 'Mode',"Ambient_Temperature"])

        clock_tz = pytz.timezone('Europe/Rome')
        rome_date = datetime.datetime.now(clock_tz)
        print(f"SIMULATION START TIME : {rome_date.strftime('%Y-%m-%d %H:%M:%S')}")
       
        '''
        try:
            time_counter = 0
            while True: #perchè la simulazione è continua
                timerAux = time.time() - consumtionTimer
                consumtionTimer = time.time()
             
                df = pd.concat([df, pd.DataFrame([[hvac.getTemperature_Internal(), hvac.getSetpoint(), hvac.calculate_consumption(timerAux), datetime.datetime.now(clock_tz).strftime('%Y-%m-%d %H:%M:%S'), hvac.getHVACMode()]], columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp','Mode'])], ignore_index=True)
                df.to_csv('src/data.csv', index=False)

                hvac.CoolingOrHeating(deltaTemp,setpoint)
                if hvac.getHVAC_State() != hvac.HVAC_State.ON:
                    loseTemp(weather,hvac)
                print(f"watts : {str(df.tail(1)['Watts'].values)} W")
                hvac.PrintStatus()
                
                time.sleep(time_refresh) #per aggiornare il sistema a intervalli deltaT
                time_counter = (round(time.time(),0) - startTimer)
        except KeyboardInterrupt :
            print("SIMULATION INTERRUPTED BY USER COMMAND")
            exit_command = True
            pass
        
        '''
        
        startTime = datetime.datetime.strptime(parametrized_array[0][0], '%Y-%m-%d %H:%M:%S')
        hvac.setHvac(parametrized_array,0)
        try:
            check_array_params(parametrized_array)
        except ValueError as e:
            print(e)
            exit()
        i = 0
        try:
            while startTime <= datetime.datetime.strptime(parametrized_array[len(parametrized_array)-1][0], '%Y-%m-%d %H:%M:%S'):
                if parametrized_array[i][0] == startTime.strftime('%Y-%m-%d %H:%M:%S'):
                    print(f"found date : {i} of {len(parametrized_array)-1}")
                    hvac.setHvac(parametrized_array,i)
                    i += 1
                timerAux = time.time() - consumtionTimer
                consumtionTimer = time.time()
                hvac.CoolingOrHeating(room)
                
                loseTemp(weather,hvac)
                #print(f"temperature : {str(hvac.getTemperature_Internal())} °C")
                df = pd.concat([df, pd.DataFrame([[hvac.getTemperature_Internal(), hvac.getSetpoint(), hvac.getPowerConsumption(), startTime, hvac.getHVACMode(),weather.getDegrees()]], columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp','Mode',"Ambient_Temperature"])], ignore_index=True)
                startTime += datetime.timedelta(seconds=1)
                #print(f"date : {startTime.strftime('%Y-%m-%d %H:%M:%S')}")
                
        except KeyboardInterrupt :
            print("SIMULATION INTERRUPTED BY USER COMMAND")
            exit()
            pass

        print(f"found {i} dates.")
        # Create and save DataFrame after the simulation loop ends
        #print(f"total time elapsed : {str(time_counter)} seconds")
        df.to_csv('src/data.csv', index=False)
        print(f"startTime valude : {parametrized_array[len(parametrized_array)-1][0]}")
        #print(f"room temperature : {str(room.temperature)} °C")


        '''
        print(f"SIMULATION END TIME: {rome_date.strftime('%Y-%m-%d %H:%M:%S')}")

        max_watt_row = df.loc[df['Watts'].idxmax()]
        max_watt_time = datetime.datetime.strptime(max_watt_row['Timestamp'], '%Y-%m-%d %H:%M:%S')
        max_watt_time = clock_tz.localize(max_watt_time)
        print(f"maximum consumption is {max_watt_row['Watts']} W reached at {max_watt_time.strftime('%Y-%m-%d %H:%M:%S')}")
        '''
        if debugGraphs:
            plot_temperaturesAndSetpoint(df)
            plot_powerConsumption(df)
            print(df)

       
        if debugLists :
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

def convert_to_gmt(date_string, date_format='%Y-%m-%d %H:%M:%S'):
            local = datetime.datetime.strptime(date_string, date_format)
            gmt = local.astimezone(pytz.utc)
            return gmt.strftime(date_format)


if __name__ == "__main__":
        main()