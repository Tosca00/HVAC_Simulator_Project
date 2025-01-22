class Weather:
    degrees = 0
    humidity = 0
    pressure = 0
    wind = 0

    def __init__(self, degrees, humidity, pressure, wind):
        self.degrees = degrees
        self.humidity = humidity
        self.pressure = pressure
        self.wind = wind
    def getDegrees(self):
        return self.degrees