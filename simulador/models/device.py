class Device:
    def __init__(self, name, expected_consumption, sensor):
        self.name = name
        self.expected_consumption = expected_consumption
        self.sensor = sensor
        self.history = []  # last 24 hours (1440 min simulated)
