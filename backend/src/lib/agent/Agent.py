from ..hvac.hvac import HVAC  # Replace with actual class names
from ..room.roomGeometry import Room,loseTemp  # Replace with actual class names
from ..weather.weather import Weather  # Replace with actual class names


#semplice sistema dizionario per mappare le classi
#delle varie componenti del sistema HVAC
class Agent():

    classes_dict = {
    'HVAC': HVAC,
    'Room': Room,
    'Weather': Weather
    }

    def tick(self):
        self.classes_dict["HVAC"].CoolingOrHeating(self.classes_dict["Room"])
        loseTemp(self.classes_dict["Weather"], self.classes_dict["HVAC"])