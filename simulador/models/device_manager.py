class DeviceManager:
    def __init__(self, devices):
        self.devices = devices

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
