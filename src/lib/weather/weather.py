class Weather:
    degrees = 0
    humidity = 0
    pressure = 0
    wind = 0
    rho = 0 #densità dell'aria
    specific_heat = 1005 #J/(kg*K) calore specifico dell'aria --- costante



    def __init__(self, degrees, humidity, pressure, wind,rho):
        self.degrees = degrees
        self.humidity = humidity
        self.pressure = pressure
        self.wind = wind
        self.rho = rho
    def getDegrees(self):
        return self.degrees