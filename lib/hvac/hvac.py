from enum import Enum
from lib.room.roomInit import *

class HVAC:

    room = createRoom(4, 3, 4)

    class HVAC_Mode(Enum):
        HEATING = 0
        COOLING = 1

    class HVAC_State(Enum):
        OFF = 0
        ON = 1

    def __init__(self):
        self.power_consumption = 0 #kW
        self.state = self.HVAC_State.OFF
        self.mode = self.HVAC_Mode.HEATING
        self.t_int = 18 #°C
        self.setpoint = 5 #°C
        peak_power = 800 #W

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
    def getHVAC_State(self):
        return self.state
    def setHVAC_State(self, state):
        self.state = state
    def getHVACMode(self):
        return self.mode
    def setHVACMode(self, mode):
        self.mode = mode
    
    #da definire meglio, per il momento basiche
    def TurnOff(self):
        self.state = self.HVAC_State.OFF
        self.power_consumption = 0
        print("HVAC is now OFF")
    def TurnOn(self):
        self.state = self.HVAC_State.ON
        print("HVAC is now ON")

    #definisce il ciclo di funzionamento del sistema HVAC nel primo caso d'uso
    def HVAC_Working(self,deltaTemp,setpoint):
        self.t_int += round(deltaTemp,1)
        self.setpoint = setpoint

    #stampa lo stato attuale del sistema HVAC, solo se acceso
    def PrintStatus(self):
        if self.state == self.HVAC_State.ON:
            print("current setpoint : " + str(self.getSetpoint()) + "°C")
            print("temperature : " + str(self.getTemperature_Internal())+ "°C")
        else:
            print("Cannot print status: HVAC is OFF")

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
    '''

    #nota: al momento si puó utilzzare solo in modalitá riscaldamento
    def thermalWorking(self, deltaTemp, setpoint):
        tempDiff = 1
        if self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.HEATING:
            if self.getTemperature_Internal() >= self.getSetpoint():
                self.TurnOff()
        elif self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.COOLING:
            if self.getTemperature_Internal() <= self.getSetpoint():
                self.TurnOff()
        elif self.getHVAC_State() == self.HVAC_State.OFF:
                if self.getTemperature_Internal() <= self.getSetpoint() - tempDiff:
                    self.TurnOn()
                    self.setHVACMode(self.HVAC_Mode.HEATING)
                elif self.getTemperature_Internal() >= self.getSetpoint() + tempDiff:
                    self.TurnOn()
                    self.setHVACMode(self.HVAC_Mode.COOLING)
        if self.getHVACMode() == self.HVAC_Mode.HEATING:
            self.setTemperature_Internal(self.getTemperature_Internal() + deltaTemp)
        elif self.getHVACMode() == self.HVAC_Mode.COOLING:
            self.setTemperature_Internal(self.getTemperature_Internal() - deltaTemp)