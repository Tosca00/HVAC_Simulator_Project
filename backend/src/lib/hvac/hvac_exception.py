class HVACException(Exception):
    def __init__(self, message="Sensor error occurred"):
        self.message = message
        super().__init__(self.message)