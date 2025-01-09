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
'''

import time
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

class HVACState(Enum):
    OFF = 0
    ON = 1

class HVAC:
    def __init__(self):
        self.power_consumption = 0
        self.state = HVACState.OFF
        self.t_int = 18
        self.setpoint = 5

    @property
    def t_int(self):
        return self._t_int

    @t_int.setter
    def t_int(self, value):
        self._t_int = round(value, 1)

    #getters and setters
    def getTemperature_Internal(self):
        return self.t_int
    def setTemperature_Internal(self, t_int):
        self.t_int = round(t_int,1)
    def getSetpoint(self):
        return self.setpoint
    def setSetpoint(self, setpoint):
        self.setpoint = setpoint
    def getPowerConsumption(self):
        return self.power_consumption
    def setPowerConsumption(self, power_consumption):
        self.power_consumption = power_consumption
    
    #da definire meglio, per il momento basiche
    def TurnOff(self):
        self.state = HVACState.OFF
        self.power_consumption = 0
        print("HVAC is now OFF")
    def TurnOn(self):
        self.state = HVACState.ON
        print("HVAC is now ON")

    #definisce il ciclo di funzionamento del sistema HVAC
    def HVAC_Working(self,deltaTemp,setpoint):
        self.t_int += round(deltaTemp,1)
        self.setpoint = setpoint

    #stampa lo stato attuale del sistema HVAC, solo se acceso
    def PrintStatus(self):
        if self.state == HVACState.ON:
            print("current setpoint : " + str(self.getSetpoint()) + "°C")
            print("temperature : " + str(self.getTemperature_Internal())+ "°C")
        else:
            print("Cannot print status: HVAC is OFF")


#aux variables for debugging 
debugLists = False
debugGraphs = True

def main():
        #basic variables
        hvac = HVAC()
        time_refresh = 1 #seconds
        timer_threshold = 60 #seconds
        consumptionPerDeltaT = []

        #for graphs
        setpoints = []
        temperatures = []

        #control variables
        deltaTemp = 0.2 #quanto cambia la temperatura interna in deltaT
        deltaConsumption = 1.2 #quanta energia consuma il condizionatore in deltaT, in kW
        setpoint = 22 
        hvac.setPowerConsumption(deltaConsumption)
        
        startTimer = time.time()
        consumtionTimer = time.time()
        startTime = time.gmtime()
        print("SIMULATION START TIME : " + str(startTime.tm_hour+1) + ":" + str(startTime.tm_min) + ":" + str(startTime.tm_sec))
        try:
            time_counter = 0
            while True: #perchè la simulazione è continua
                if time_counter < timer_threshold:
                    print(f"timer : {time_counter:.2f}")
                temperatures.append(hvac.getTemperature_Internal())
                setpoints.append(hvac.getSetpoint())
                #calculate consumption
                timerAux = time.time() - consumtionTimer
                consumptionPerDeltaT.append(CalculateConsumption(hvac,timerAux))
                consumtionTimer = time.time()

                if hvac.state == HVACState.ON and hvac.getTemperature_Internal() >= hvac.getSetpoint():
                    hvac.TurnOff()
                    break
                if time_counter > timer_threshold: #nel caso d'uso il sistema si accende dopo una soglia (60 secondi)
                    if hvac.state == HVACState.OFF:
                        hvac.TurnOn()
                    oldTemp = hvac.getTemperature_Internal()
                    hvac.HVAC_Working(deltaTemp,setpoint)
                    newTemp = hvac.getTemperature_Internal()
                    hvac.PrintStatus()
                time.sleep(time_refresh) #per aggiornare il sistema a intervalli deltaT
                time_counter = (int)(time.time() - startTimer)
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
    if(hvac.state == HVACState.ON):
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