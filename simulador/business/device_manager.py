class DeviceManager:
    def __init__(self, devices=None):
        self.devices = devices if devices else []
        self.minute_counter = 0
        self.simulated_minutes = 0
        self.day_length = 1440  # 24 hours

    def get_all(self):
        return self.devices

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, name):
        self.devices = [d for d in self.devices if d.name != name]

    def find(self, name):
        for d in self.devices:
            if d.name == name:
                return d
        return None

    # 1 tick = 1 simulated minute
    def tick(self):
        self.minute_counter += 1
        self.simulated_minutes += 1

        for d in self.devices:
            d.add_measurement(d.sensor.generate_measurement())

        # Close simulated day
        if self.minute_counter >= self.day_length:
            for d in self.devices:
                d.close_day()
            self.minute_counter = 0
