import random
from ..weather.weather import Weather
import math
class Room:
    height = 0
    width = 0
    length = 0
    Temperature = 0
    volume = 0
    heatCapacity = 0
    heatLossCoefficient = 0
    wallsArea = 0

    def __init__(self, height : float, width: float, length:float, temperature,heatLossCoefficient, weather : Weather):
        self.height = height
        self.width = width
        self.length = length
        self.temperature = temperature
        self.heatLossCoefficient = heatLossCoefficient
        self.volume = self.calculateVolume()
        self.heatCapacity = self.hCapacity(weather)
        self.wallsArea = 2 * (self.height * self.width + self.height * self.length + self.width * self.length)

    def setTemperature(self, temperature):
        self.temperature = temperature

    def calculateVolume(self):
        return self.height * self.width * self.length

    def hCapacity(self,weather : Weather):
        return self.volume * weather.specific_heat * weather.rho

    
#per il momento la perdita di temperatura è costante e converge su quella ambiente
def loseTemp(weather: Weather, hvac):
    if hvac.getHVAC_State() != hvac.HVAC_State.ON:
        diff = hvac.getTemperature_Internal() - weather.degrees
        decay_factor = 0.1 / (1 + abs(diff))  # Larger diff => slower drop, smaller diff => faster drop
        adjusted_diff = diff * (1 - decay_factor)
        hvac.setTemperature_Internal(weather.degrees + adjusted_diff)