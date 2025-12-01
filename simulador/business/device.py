class Device:
    def __init__(self, name, expected_consumption, sensor):
        self.name = name
        self.expected_consumption = expected_consumption
        self.sensor = sensor

        self.history = []          # last 24h (1440 min)
        self.monthly_history = []  # one entry per simulated day

    def add_measurement(self, m):
        self.history.append(m)
        if len(self.history) > 1440:
            self.history.pop(0)

    def close_day(self):
        daily_wh = sum(m.power * (1 / 60) for m in self.history)
        self.monthly_history.append(daily_wh)
        self.history.clear()
