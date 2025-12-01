class Analyzer:
    def detect_anomaly(self, measurement, expected):
        difference = measurement.power - expected

        if measurement.power > expected * 1.35:
            severity = difference / expected
            return True, severity 

        return False, 0.0
