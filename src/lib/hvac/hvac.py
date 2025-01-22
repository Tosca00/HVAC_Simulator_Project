from enum import Enum
from src.lib.hvac.hvac_exception import HVACException
from ..weather.weather import Weather
import random

class HVAC:

    class HVAC_Mode(Enum):
        HEATING = 0
        COOLING = 1
        NO_MODE = 2

    class HVAC_State(Enum):
        OFF = 0
        ON = 1
        INACTIVE = 2

    def __init__(self):
        self.power_consumption = 0 #kW
        self.state = self.HVAC_State.OFF
        self.mode = self.HVAC_Mode.HEATING
        self.t_int = 21 #°C
        self.setpoint = 5 #°C
        self.peak_power = 1000 #W
        self.BTUs = 8000 #BTUs
        self.tempDiff = 2
        self.deltaEn = 0.1 #kWh

    @property
    def t_int(self):
        return self._t_int

    @t_int.setter
    def t_int(self, value):
        self._t_int = round(value, 2)

    #getters and setters
    def getTemperature_Internal(self):
        return self.t_int
    def setTemperature_Internal(self, t_int):
        self.t_int = round(t_int,2)
    def getSetpoint(self):
        return self.setpoint
    def setSetpoint(self, setpoint):
        self.setpoint = setpoint
    def getPowerConsumption(self):
        return self.power_consumption
    def setPowerConsumption(self, power_consumption):
        self.power_consumption = power_consumption 
    def getHVAC_State(self):
        return self.state
    def setHVAC_State(self, state):
        self.state = state
    def getHVACMode(self):
        return self.mode
    def setHVACMode(self, mode):
        self.mode = mode
    def setDeltaTemp(self,deltaTemp):
        self.deltaTemp = deltaTemp
    def getDeltaTemp(self):
        return self.deltaTemp
    #da definire meglio, per il momento basiche
    def TurnOff(self):
        self.state = self.HVAC_State.OFF
        self.setHVACMode(self.HVAC_Mode.NO_MODE)
        self.power_consumption = 0
        print("HVAC is now OFF")
    def TurnOn(self,HVAC_Mode):
        self.state = self.HVAC_State.ON
        self.setHVACMode(HVAC_Mode)
        print("HVAC is now ON")

    def setInactive(self):
        self.state = self.HVAC_State.INACTIVE
        self.power_consumption = 0
    

    #definisce il ciclo di funzionamento del sistema HVAC nel primo caso d'uso
    def HVAC_Working(self,deltaTemp,setpoint):
        self.t_int += round(deltaTemp,1)
        self.setpoint = setpoint

    #stampa lo stato attuale del sistema HVAC, solo se acceso
    def PrintStatus(self):
        print(f"current setpoint : {str(self.getSetpoint())} °C")
        print(f"temperature : {str(self.getTemperature_Internal())} °C")

        if self.getHVAC_State() == self.HVAC_State.OFF and self.getHVACMode() != self.HVAC_Mode.NO_MODE:
            raise HVACException("HVAC is OFF but has a mode set")
        else:
            print(f"State : {str(self.getHVAC_State())} -- Mode : {str(self.getHVACMode())}")

        
    '''
    secondo caso d'uso, da approfondire
    serve a decidere se il sistema deve raffreddare o riscaldare, oltre che rispettare una soglia di differenza dall'obbiettivo
    perché per esempio se la temperatura obbiettivo fosse 22°C e il sistema si spegnesse subito, il sistema si accenderebbe e spegnerebbe continuamente

    descrizione algoritmo:
        - definire un differenziale di temperatura da quella obbiettivo (tempDiff)
        - se il sistema é acceso e sta riscaldando
            - se la temperatura interna é maggiore o uguale a quella obbiettivo
                - spegni il sistema
        -altrimenti se il sistema é acceso e sta raffreddando
             -se la temperatura interna é minore o uguale a quella obbiettivo
                - spegni il sistema
        - altrimenti se il sistema é spento
            - se la temperatura interna é maggiore o uguale a quella obbiettivo - il differenziale
                - accendi il sistema e imposta modalitá riscaldamento
            - altrimenti se la temperatura interna é minore o uguale a quella obbiettivo + il differenziale
                - accendi il sistema e imposta modalitá raffreddamento
        - se la modalitá é riscaldamento
            - aumenta la temperatura interna di deltaTemp
        - altrimenti se la modalitá é raffreddamento
            - diminuisci la temperatura interna di deltaTemp
   

    #nota: al momento si puó utilzzare solo in modalitá riscaldamento
    def thermalWorking(self, deltaTemp, setpoint):
        tempDiff = 2 #differenziale di temperatura dal setpoint
        if self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.HEATING:
            if self.getTemperature_Internal() >= self.getSetpoint() + tempDiff:
                self.TurnOff()
        elif self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.COOLING:
            if self.getTemperature_Internal() <= self.getSetpoint() - tempDiff:
                self.TurnOff()
        elif self.getHVAC_State() == self.HVAC_State.OFF:
                if self.getTemperature_Internal() <= self.getSetpoint() - tempDiff:
                    self.TurnOn()
                    self.setHVACMode(self.HVAC_Mode.HEATING)
                elif self.getTemperature_Internal() >= self.getSetpoint() + tempDiff:
                    self.TurnOn()
                    self.setHVACMode(self.HVAC_Mode.COOLING)
        if self.getHVACMode() == self.HVAC_Mode.HEATING and self.getHVAC_State() == self.HVAC_State.ON:
            self.setTemperature_Internal(self.getTemperature_Internal() + deltaTemp)
        elif self.getHVACMode() == self.HVAC_Mode.COOLING and self.getHVAC_State() == self.HVAC_State.ON:
            self.setTemperature_Internal(self.getTemperature_Internal() - deltaTemp)

 '''

    def CoolingOrHeating(self, deltaTemp, setpoint):
        random_variation = abs(random.gauss(0.003,0.01))  # aggiunta varianza

        if self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.HEATING:
            if self.getTemperature_Internal() >= self.getSetpoint() + self.tempDiff:
                self.setInactive()
        elif self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.COOLING:
            if self.getTemperature_Internal() <= self.getSetpoint() - self.tempDiff:
                self.setInactive()
        elif self.getHVAC_State() == self.HVAC_State.INACTIVE:
            if self.getHVACMode() == self.HVAC_Mode.HEATING:
                if self.getTemperature_Internal() <= self.getSetpoint():
                    self.TurnOn(self.HVAC_Mode.HEATING)
            elif self.getHVACMode() == self.HVAC_Mode.COOLING:
                if self.getTemperature_Internal() >= self.getSetpoint():
                    self.TurnOn(self.HVAC_Mode.COOLING)
        if self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.HEATING:
            self.setTemperature_Internal(self.getTemperature_Internal() + deltaTemp + random_variation)
        elif self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.COOLING:
            self.setTemperature_Internal(self.getTemperature_Internal() - deltaTemp - random_variation)

    def calculate_consumption(self, delta_t):
        if self.getHVAC_State() == HVAC.HVAC_State.ON:
            if self.getHVACMode() == HVAC.HVAC_Mode.HEATING:
                delta_temp = abs(self.getTemperature_Internal() - self.getSetpoint() + self.tempDiff)
            else:
                delta_temp = abs(self.getTemperature_Internal() - self.getSetpoint() - self.tempDiff)
            delta_temp_max = 3  # soglia introdotta per evitare che il sistema consumi troppo
            
            if delta_temp < delta_temp_max:
                absorption_efficiency = delta_temp / delta_temp_max
            else:
                absorption_efficiency = 1  # 100% power

            random_efficiency_variation = min(abs(random.gauss(0.95, 0.02)),1)
            instantaneous_power = self.peak_power * absorption_efficiency * random_efficiency_variation

            return round(instantaneous_power, 2)
        else:
            return 0 #hvac è spento
        

    def setHvac(self,parametrized_array,position):
                if position > len(parametrized_array):
                    raise IndexError("Position out of bound")
                self.setSetpoint(parametrized_array[position][1])
                match parametrized_array[position][2]:
                    case "HEATING":
                        self.setHVACMode(self.HVAC_Mode.HEATING)
                    case "COOLING":
                        self.setHVACMode(self.HVAC_Mode.COOLING)
                if parametrized_array[position][3] == "ON" and self.getHVAC_State() == self.HVAC_State.OFF:
                        self.TurnOn(self.getHVACMode())
                if parametrized_array[position][3] == "OFF":
                        self.TurnOff()