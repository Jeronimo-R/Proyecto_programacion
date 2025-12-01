class Dashboard:
    def show_report(self, devices):
        print("\n===== GENERAL DASHBOARD =====")

        for device in devices:
            daily_consumption = sum(m.power for m in device.history) / 60

            monthly_consumption = sum(device.monthly_history)

            print(f"\nDevice: {device.name}")
            print(f"Daily consumption: {daily_consumption:.2f} Wh")
            print(f"Monthly consumption: {monthly_consumption:.2f} Wh")
            print(f"Estimated daily cost (COP): {(daily_consumption / 1000) * 750:.2f}")
            print(f"Estimated monthly cost (COP): {(monthly_consumption / 1000) * 750:.2f}")
            print("-" * 40)
