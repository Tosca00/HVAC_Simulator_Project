#utilizzato per definire eccezioni personalizzate per il modulo HVAC

class HVACException(Exception):
    def __init__(self, message="Sensor error occurred"):
        self.message = message
        super().__init__(self.message)