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
from lib.hvac.hvacTypes import HVAC


#aux variables for debugging 
debugLists = False
debugGraphs = True

def main():
        #basic variables
        hvac = HVAC()
        time_refresh = 1 #seconds
        timer_threshold = 20 #seconds
        consumptionPerDeltaT = []

        #for graphs
        setpoints = []
        temperatures = []

        #control variables
        deltaTemp = 0.2 #quanto cambia la temperatura interna in deltaT
        deltaConsumption = 1.2 #quanta energia consuma il condizionatore in deltaT, in kW
        setpoint = 22 
        hvac.setPowerConsumption(deltaConsumption)
        
        startTimer = round(time.time(),0)
        consumtionTimer = time.time()
        startTime = time.gmtime()
        print("SIMULATION START TIME : " + str(startTime.tm_hour+1) + ":" + str(startTime.tm_min) + ":" + str(startTime.tm_sec))
        try:
            time_counter = 0
            while True: #perchè la simulazione è continua
                if time_counter < timer_threshold:
                    print(f"timer : {time_counter:.6f}")
                temperatures.append(hvac.getTemperature_Internal())
                setpoints.append(hvac.getSetpoint())
                #calculate consumption
                timerAux = time.time() - consumtionTimer
                consumptionPerDeltaT.append(CalculateConsumption(hvac,timerAux))
                consumtionTimer = time.time()

                if hvac.getHVAC_State() == HVAC.HVAC_State.ON and hvac.getTemperature_Internal() >= hvac.getSetpoint():
                    hvac.TurnOff()
                    break
                if time_counter > timer_threshold: #nel caso d'uso il sistema si accende dopo una soglia (60 secondi)
                    if hvac.getHVAC_State() == HVAC.HVAC_State.OFF:
                        hvac.TurnOn()
                    oldTemp = hvac.getTemperature_Internal()
                    hvac.HVAC_Working(deltaTemp,setpoint)
                    newTemp = hvac.getTemperature_Internal()
                    hvac.PrintStatus()
                time.sleep(time_refresh) #per aggiornare il sistema a intervalli deltaT
                time_counter = (round(time.time(),0) - startTimer)
        except KeyboardInterrupt :
            print("SIMULATION INTERRUPTED BY USER COMMAND")
            exit()
            pass

        print("estimated power consumption is : " + str(np.sum(consumptionPerDeltaT)) + " kW/h")
        print("total time elapsed : " + str(time_counter))
        print("SIMULATION END TIME : " + str(time.gmtime().tm_hour+1) + ":" + str(time.gmtime().tm_min) + ":" + str(time.gmtime().tm_sec))

        #set variables for debugging
        if debugGraphs :
            drawTemperatureGraph(temperatures,setpoints)
            drawPowerConsumptionGraph(consumptionPerDeltaT)
        if debugLists :
            print("----------------------------")
            print(consumptionPerDeltaT)


def CalculateConsumption(hvac, time):
    if(hvac.getHVAC_State() == HVAC.HVAC_State.ON):
        deltaTemp = abs(hvac.getTemperature_Internal() - hvac.getSetpoint())
        deltaTempMax = 15 #da approfondire, indica quando il sistema raggiunge la portata massima di capacità, per esempio se Temp > 15°C allora consumi e inefficienza massima
        absortion = (hvac.power_consumption * 1000) * (deltaTemp/deltaTempMax)
        consumption_joule = absortion * time
        consumption = consumption_joule / (3.6 * 10**6)
        return consumption
    else:
        return 0


   
def drawPowerConsumptionGraph(consumptionPerDeltaT):
    plt.figure(figsize=(8,4))
    plt.plot(consumptionPerDeltaT, label='Power Consumption',color='green')
    plt.xlabel('Time')
    plt.ylabel('Power Consumption')
    plt.title('Power Consumption')
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