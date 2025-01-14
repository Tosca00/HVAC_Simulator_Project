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
from lib.hvac.hvac import HVAC
from lib.room.init import *
import tkinter as tk
from tkinter import simpledialog
import pytz
import datetime


#aux variables for debugging 
debugLists = False
debugGraphs = True

#semplice funzione una finestra grafica, usata in un thread a parte per non bloccare il main
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

        #control variables
        deltaTemp = 0.05 #quanto cambia la temperatura interna in deltaT
        deltaConsumption = 1.2 #quanta energia consuma il condizionatore in deltaT, in kW
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


        clock_tz = pytz.timezone('Europe/Rome')
        rome_time = datetime.datetime.now(clock_tz)
        print(f"SIMULATION START TIME : {rome_time.strftime('%Y-%m-%d %H:%M:%S')}")
       
        try:
            time_counter = 0
            while True: #perchè la simulazione è continua
                #vettori per grafici
                temperatures.append(hvac.getTemperature_Internal())
                setpoints.append(hvac.getSetpoint())
                #calculate consumption per deltaT
                timerAux = time.time() - consumtionTimer
                watts.append(hvac.calculate_consumption(timerAux))
                consumtionTimer = time.time()

                hvac.CoolingOrHeating(deltaTemp,setpoint)
                if hvac.getHVAC_State() == HVAC.HVAC_State.OFF:
                    hvac.setTemperature_Internal(hvac.getTemperature_Internal() - loseTemp())
                print(f"watts : {str(watts[-1])} W")
                hvac.PrintStatus()
                time.sleep(time_refresh) #per aggiornare il sistema a intervalli deltaT
                time_counter = (round(time.time(),0) - startTimer)
        except KeyboardInterrupt :
            print("SIMULATION INTERRUPTED BY USER COMMAND")
            exit_command = True
            pass

        print(f"total time elapsed : {str(time_counter)} seconds")
        print(f"SIMULATION END TIME: {rome_time.strftime('%Y-%m-%d %H:%M:%S')}")

        max_watt_time = startTimer + watts.index(max(watts)) * time_refresh
        rome_tz = pytz.timezone('Europe/Rome')
        max_watt_time_rome = pytz.utc.localize(datetime.datetime.fromtimestamp(max_watt_time)).astimezone(rome_tz)
        print(f"maximum consumption is {str(max(watts))} W reached at {max_watt_time_rome.strftime('%Y-%m-%d %H:%M:%S')}")

        #set variables for debugging
        if debugGraphs and exit_command == True:
            drawTemperatureGraph(temperatures,setpoints)
            drawPowerConsumptionGraph(watts)
        if debugLists :
            print("----------------------------")
            print(watts)


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