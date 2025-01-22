import random
from ..weather.weather import Weather
from ..hvac.hvac import HVAC
class Room:
    heigth = 0
    width = 0
    length = 0
    Temperature = 0

    def __init__(self, height, width, length, temperature):
        self.height = height
        self.width = width
        self.length = length
        self.temperature = temperature

    def setTemperature(self, temperature):
        self.temperature = temperature

    
#per il momento la perdita di temperatura è costante e converge su quella ambiente
def loseTemp(weather : Weather,hvac: HVAC):
    if(weather.degrees >= hvac.getTemperature_Internal()):
        hvac.setTemperature_Internal(hvac.getTemperature_Internal() + abs(random.gauss(0.005, 0.05)))
    else :
        hvac.setTemperature_Internal(hvac.getTemperature_Internal() - abs(random.gauss(0.005, 0.05)))