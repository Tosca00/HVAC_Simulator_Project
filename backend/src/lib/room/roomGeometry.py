import random
from ..weather.weather import Weather
import math

#in future versioni si pensava di calcolare il calore trasmesso dalle persone e dispositivi nella stanza
class Lamp:
    wattage = 0

    def __init__(self,wattage):
        self.wattage = wattage


class Room:
    height = 0
    width = 0
    length = 0
    temperature = 0
    volume = 0
    heatCapacity = 0
    heatLossCoefficient = 0
    wallsArea = 0
    people = 0
    lamps = []

    def __init__(self, height : float, width: float, length:float, temperature,heatLossCoefficient, weather : Weather):
        self.height = height
        self.width = width
        self.length = length
        self.temperature = temperature
        self.heatLossCoefficient = heatLossCoefficient
        self.volume = self.calculateVolume()
        self.heatCapacity = self.hCapacity(weather)
        self.wallsArea = 2 * (self.height * self.width + self.height * self.length + self.width * self.length)

    def __init__(self, height : float, width: float, length:float,heatLossCoefficient: float,weather : Weather, temperature = 0):
        self.height = height
        self.width = width
        self.length = length
        self.heatLossCoefficient = heatLossCoefficient
        self.volume = self.calculateVolume()
        self.heatCapacity = self.hCapacity(weather)
        self.wallsArea = 2 * (self.height * self.width + self.height * self.length + self.width * self.length)


    #setters e getters
    def setTemperature(self, temperature):
        self.temperature = temperature

    def calculateVolume(self):
        return self.height * self.width * self.length

    def hCapacity(self,weather : Weather):
        return self.volume * weather.specific_heat * weather.rho
    
    def transmissionLoad(self, weather: Weather, hvac):
        return self.heatLossCoefficient * self.wallsArea * (hvac.getTemperature_Internal() - weather.degrees)
    
    def addPerson(self):
        self.people += 1
    def RemovePerson(self):
        if(self.people > 0):
            self.people -= 1
        else:
            print("Room is already empty")

    #tra i vari tipi di dispersione di calore si vogliono ricreare in particolare le dispersioni dovute a persone e lampade
    def InternalLoadPeople(self,time):
        personaHeatAverage = 105 #W
        return self.people * time * personaHeatAverage
    def InternalLoadLight(self,time):
        return sum([lamp.wattage for lamp in self.lamps]) * time
        
    
#per il momento la perdita di temperatura è esponenziale e converge su quella ambiente
def loseTemp(weather: Weather, hvac):
    diff = hvac.getTemperature_Internal() - weather.degrees
    decay_factor = 0.001  # controlla il rateo di convergenza
    adjusted_diff = diff * math.exp(-decay_factor)
    hvac.setTemperature_Internal(weather.degrees + adjusted_diff)