class Analyzer:
    def detect_anomaly(self, measurement, expected):
        difference = measurement.power - expected

        if measurement.power > expected * 1.35:
            severity = difference / expected
            return True, severity

        return False, 0.0

    def recommend(self, device):
        """Basic rule-based suggestions."""
        daily = device.compute_daily_consumption()

        if daily > device.expected_consumption * 1.3:
            return "Daily usage is higher than expected. Check efficiency."

        if device.history and device.history[-1].power > device.expected_consumption * 1.5:
            return "Sudden peak detected. Verify device cycles."

        if len(device.monthly_history) >= 7:
            avg = sum(device.monthly_history[-7:]) / 7
            if daily > avg * 1.2:
                return "Today's usage is above the weekly average."

        return "Consumption within normal parameters."
