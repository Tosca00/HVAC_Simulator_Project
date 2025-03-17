from enum import Enum
from src.lib.hvac.hvac_exception import HVACException
from ..weather.weather import Weather
from ..room.roomGeometry import *
import numpy as np
class HVAC:

    class POWER_Mode:
        DELTA_TEMP_HIGH = 5
        DELTA_TEMP_MEDIUM = 2
        DELTA_TEMP_LOW = 0.5
        def __init__(self):
            pass
    class HVAC_Mode(Enum):
        HEATING = 0
        COOLING = 1
        NO_MODE = 2

    class HVAC_State(Enum):
        OFF = 0
        ON = 1
        INACTIVE = 2

    class HVAC_AirFlowLevel(Enum):
        LOW = 0
        MEDIUM = 1
        HIGH = 2
        AUTO = 3

    def __init__(self):
        self.power_consumption = 0 #kW
        self.state = self.HVAC_State.OFF
        self.mode = self.HVAC_Mode.HEATING
        self.t_int = 21 #°C
        self.setpoint = 18 #°C
        self.peak_power = 1000 #W
        self.BTUs = 9000 #BTUs
        self.tempDiff = 2
        self.efficiency = 0.98 #% eddicienza generale
        self.eer = 3.00 #standards eer
        self.cop = 3.00 #standards cop
        self.Power_Watt = self.BTUs / (3.412* self.eer) #W inizializzato in modalità raffreddamento
        self.faulty = False #se il sistema è guasto
        self.air_flow = 0.18 #m^3/s
        self.supply_air_temp = 0 #°C #per semplicitá si assume che l'aria in uscita sia a temperatura ambiente
        self.air_flow_level = self.HVAC_AirFlowLevel.HIGH
        self.fan_power_watt = 50  # Default per velocità minima
        self.isFanAuto = True
        self.compressor_power = 0 #kW
        self.energyClassCooling = self.calculateEnergyClass_Cooling()
        self.energyClassHeating = self.calculateEnergyClass_Heating()
        

    #set di due funzioni, generano la classe energetica in base al cop o eer
    def calculateEnergyClass_Heating(self):
        if self.cop < 1.20:
            return "G"
        elif self.cop < 1.40:
            return "F"
        elif self.cop < 1.60:
            return "E"
        elif self.cop < 1.80:
            return "D"
        elif self.cop < 2.00:
            return "C"
        elif self.cop < 2.30:
            return "B"
        elif self.cop < 2.60:
            return "A"
        elif self.cop < 3.10:
            return "A+"
        elif self.cop < 3.60:
            return "A++"
        else:
            return "A+++"
    def calculateEnergyClass_Cooling(self):
        if self.eer < 1.40:
            return "G"
        elif self.eer < 1.60:
            return "F"
        elif self.eer < 1.80:
            return "E"
        elif self.eer < 2.10:
            return "D"
        elif self.eer < 2.40:
            return "C"
        elif self.eer < 2.60:
            return "B"
        elif self.eer < 3.10:
            return "A"
        elif self.eer < 3.60:
            return "A+"
        elif self.eer < 4.10:
            return "A++"
        else:
            return "A+++"


    #setters e getters
    @property
    def t_int(self):
        return self._t_int

    @t_int.setter
    def t_int(self, value):
        self._t_int = round(value, 4)

    #getters and setters
    def getTemperature_Internal(self):
        return self.t_int
    def setTemperature_Internal(self, t_int):
        self.t_int = round(t_int,4)
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
    
    
    #spegne il sistema
    def TurnOff(self):
        self.state = self.HVAC_State.OFF
        self.setHVACMode(self.HVAC_Mode.NO_MODE)
        self.power_consumption = 0

    #accende il sistema
    def TurnOn(self,HVAC_Mode):
        self.state = self.HVAC_State.ON
        self.setHVACMode(HVAC_Mode)
        self.Power_Watt = self.BTUs / (3.412* self.eer) #W inizializzato in modalità raffreddamento, perchè se offre 2 modalità diverse potrebbe avere efficienze diverse
        if HVAC_Mode == self.HVAC_Mode.HEATING:
            self.Power_Watt = self.BTUs / (3.412* self.cop)

    #sistema inattivo
    def setInactive(self):
        self.state = self.HVAC_State.INACTIVE
        self.power_consumption = 0
    

    #per il cambio manuale della velocità della ventola, piú alta é la velocitá piú aria viene immessa
    def changeFanPower(self, HVAC_AirFlowLevel):
        if HVAC_AirFlowLevel == self.HVAC_AirFlowLevel.LOW:
            self.fan_power_watt = 50
            self.air_flow = 0.08
            self.air_flow_level = self.HVAC_AirFlowLevel.LOW
        elif HVAC_AirFlowLevel == self.HVAC_AirFlowLevel.MEDIUM:
            self.fan_power_watt = 100
            self.air_flow = 0.13
            self.air_flow_level = self.HVAC_AirFlowLevel.MEDIUM
        elif HVAC_AirFlowLevel == self.HVAC_AirFlowLevel.HIGH:
            self.fan_power_watt = 150
            self.air_flow = 0.18
            self.air_flow_level = self.HVAC_AirFlowLevel.HIGH
        elif HVAC_AirFlowLevel == self.HVAC_AirFlowLevel.AUTO:
            self.isFanAuto = True


    #deprecata
    #definisce il ciclo di funzionamento del sistema HVAC nel primo caso d'uso, ormai obsoleta
    def HVAC_Working(self,deltaTemp,setpoint):
        self.t_int += round(deltaTemp,1)
        self.setpoint = setpoint

    #deprecata
    #stampa lo stato attuale del sistema HVAC, solo se acceso, utilizzata nei primi casi d'uso
    def PrintStatus(self):
        print(f"current setpoint : {str(self.getSetpoint())} °C")
        print(f"temperature : {str(self.getTemperature_Internal())} °C")
        if self.getHVAC_State() == self.HVAC_State.OFF and self.getHVACMode() != self.HVAC_Mode.NO_MODE:
            raise HVACException("HVAC is OFF but has a mode set")
        else:
            print(f"State : {str(self.getHVAC_State())} -- Mode : {str(self.getHVACMode())}")

    

    #definisce le soglie di temperatura per il cambio di modalitá del COMPRESSORE
    def changePower(self):
        powerFactor = 1
        if self.getTemperature_Internal() > self.getSetpoint() and self.getHVACMode() == self.HVAC_Mode.HEATING:
            powerFactor = 0.5
        elif self.getTemperature_Internal() < self.getSetpoint() and self.getHVACMode() == self.HVAC_Mode.COOLING:
            powerFactor = 0.5
        return powerFactor
    
    #gestisce la ventilazione se il sistema è impostato su modalità automatica
    def fanAuto(self):
        if self.getTemperature_Internal() < (self.getSetpoint() - 2) and self.getHVACMode() == self.HVAC_Mode.HEATING:
            self.changeFanPower(self.HVAC_AirFlowLevel.HIGH)
        elif self.getTemperature_Internal() < (self.getSetpoint() - 1) and self.getHVACMode() == self.HVAC_Mode.HEATING:
            self.changeFanPower(self.HVAC_AirFlowLevel.MEDIUM)
        elif self.getTemperature_Internal() > self.getSetpoint() and self.getHVACMode() == self.HVAC_Mode.HEATING:
            self.changeFanPower(self.HVAC_AirFlowLevel.LOW)

        if self.getTemperature_Internal() > (self.getSetpoint() + 2) and self.getHVACMode() == self.HVAC_Mode.COOLING:
            self.changeFanPower(self.HVAC_AirFlowLevel.HIGH)
        elif self.getTemperature_Internal() > (self.getSetpoint() + 1) and self.getHVACMode() == self.HVAC_Mode.COOLING:
            self.changeFanPower(self.HVAC_AirFlowLevel.MEDIUM)
        elif self.getTemperature_Internal() < self.getSetpoint() and self.getHVACMode() == self.HVAC_Mode.COOLING:
            self.changeFanPower(self.HVAC_AirFlowLevel.LOW)


    '''
    funzione principale di gestione:
    controllando prima lo stato, modalità e temperature interne, decide se accendere, spegnere o mantenere attivo il sistema HVAC
    altrimenti se il sistema è acceso e la modalità è impostata, calcola il deltaT e lo applica alla temperatura interna
    '''
    def CoolingOrHeating(self, room):
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
        if not self.faulty: #se il sistema è guasto non deve essere immessa temperatura
            if self.isFanAuto: #per controllo automatico della ventola
                self.fanAuto()
            #print(f"fan level : {HVAC.HVAC_AirFlowLevel(self.air_flow_level).name}")
            #print(f"compressor power : {self.compressor_power} W -- fan power : {self.fan_power_watt} W")
            if self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.HEATING:
                deltaT = self.ChangeTemp(room)
                self.setTemperature_Internal(self.getTemperature_Internal() + deltaT)
            elif self.getHVAC_State() == self.HVAC_State.ON and self.getHVACMode() == self.HVAC_Mode.COOLING:
                deltaT = self.ChangeTemp(room)
                self.setTemperature_Internal(self.getTemperature_Internal() - deltaT)


    #deprecata
    #deduce il consumo istantaneo del sistema HVAC,utilizzata nelle prime versioni, ormai obsoleta
    def calculate_consumption(self):
        if self.getHVAC_State() == HVAC.HVAC_State.ON:
            if self.getHVACMode() == HVAC.HVAC_Mode.HEATING:
                delta_temp = abs(self.getTemperature_Internal() - self.getSetpoint() + self.tempDiff)
            else:
                delta_temp = abs(self.getTemperature_Internal() - self.getSetpoint() - self.tempDiff)
            delta_temp_max = 3.5  # soglia introdotta per evitare che il sistema consumi troppo
            
            if delta_temp < delta_temp_max:
                effective_power = delta_temp / delta_temp_max
            else:
                effective_power = 1  # 100% power
            instantaneous_power = self.peak_power * effective_power
            self.setPowerConsumption(instantaneous_power)
            return round(instantaneous_power, 2)
        else:
            return 0 #hvac è spento
        

    #deprecata
    #deduce il cambio di temperatura del sistema HVAC, utilizzata nelle prime versioni, ormai obsoleta    
    def UpdateTemp(self, room: Room):
        consumption = self.calculate_consumption()
        power_factor = consumption / 1000.0
        temp_change = self.changeTemp(room) * power_factor

        if self.getHVAC_State() == self.HVAC_State.ON:
            if self.getHVACMode() == self.HVAC_Mode.HEATING:
                self.setTemperature_Internal(self.getTemperature_Internal() + temp_change)
            elif self.getHVACMode() == self.HVAC_Mode.COOLING:
                self.setTemperature_Internal(self.getTemperature_Internal() - temp_change)


    #setta i parametri del sistema HVAC in base a un array parametrizzato, per il formato fare riferimento al file parametrizedArray.py
    def setHvac(self,parametrized_array:np.array,position):
        if position > len(parametrized_array):
            raise IndexError("Position out of bound")
        self.setSetpoint(parametrized_array[position][1])
        if parametrized_array[position][2] == "HEATING":
            self.setHVACMode(self.HVAC_Mode.HEATING)
        elif parametrized_array[position][2] == "COOLING":
            self.setHVACMode(self.HVAC_Mode.COOLING)
        else:
            self.setHVACMode(self.HVAC_Mode.NO_MODE)
        if parametrized_array[position][3] == "ON" and self.getHVAC_State() == self.HVAC_State.OFF:
                self.TurnOn(self.getHVACMode())
        if parametrized_array[position][3] == "OFF":
                self.TurnOff()

    #funzione principale per il cambio di temperatura del sistema HVAC, rappresenta una semplificazione della legge del bilancio termico
    def ChangeTemp(self, room: Room):

        #differenza di temperatura
        temp_diff = self.getTemperature_Internal() - Weather.degrees

        # Potenza del compressore, aggiustata in base alla temperatura interna
        self.compressor_power = self.Power_Watt * self.changePower()

        #energia totale immessa
        Q_In = (self.compressor_power + self.fan_power_watt) * self.efficiency 

        #energia totale dispersa
        Q_Out = room.heatLossCoefficient * room.wallsArea * temp_diff

        # Massa d'aria immessa effettiva
        air_mass_flow = self.air_flow * Weather.rho

        #l'aria immessa deve essere piú calda di quella interna per riscaldare, piú fredda per raffreddare
        #si è scelto un approccio semplicistico con soglia fissa
        self.supply_air_temp = self.getTemperature_Internal() + 8
        if self.getHVACMode() == self.HVAC_Mode.COOLING:
            self.supply_air_temp = self.getTemperature_Internal() - 8

        #print(f"supply air temp : {self.supply_air_temp}")

        # energia aria immessa
        W_s = air_mass_flow * Weather.specific_heat * (self.supply_air_temp - self.getTemperature_Internal())

        # Se il sistema è in modalità raffreddamento, l'energia immessa è negativa
        if self.getHVACMode() == self.HVAC_Mode.COOLING:
            W_s = -W_s


        #considera l'energia immessa e dispersa
        Q_eff = Q_In + W_s - Q_Out

        #print(f"walls area : {room.wallsArea}")
        #print(f"room heat loss coefficient : {room.heatLossCoefficient}")
        #print(f"room heat capacity : {room.heatCapacity}")

        # Cambio di temperatura effettivo
        delta_temp_effective = Q_eff / room.heatCapacity

        # cosumo totale per l'intera iterazione
        self.power_consumption = self.compressor_power + self.fan_power_watt

        #print(f"deltatemp effective : {delta_temp_effective}")

        return delta_temp_effective
            
