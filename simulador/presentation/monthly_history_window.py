from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget
from PyQt5.QtGui import QFont
from utils.constants import COP_PER_KWH

class MonthlyHistoryWindow(QDialog):
    def __init__(self, device_manager):
        super().__init__()

        self.device_manager = device_manager

        self.setWindowTitle("Monthly Energy History")
        self.resize(400, 500)

        layout = QVBoxLayout()

        title = QLabel("Monthly Energy Consumption")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(title)

        self.list = QListWidget()
        layout.addWidget(self.list)

        total_month = 0

        for d in self.device_manager.get_all():
            m = d.sensor.accumulated_energy  # Wh acumulado
            cost = (m / 1000) * COP_PER_KWH

            total_month += m

            self.list.addItem(
                f"{d.name} → {m:.2f} Wh  |  {cost:.2f} COP"
            )

        total_cost = (total_month / 1000) * COP_PER_KWH

        summary = QLabel(
            f"\nTotal Monthly: {total_month:.2f} Wh\n"
            f"Total Cost: {total_cost:.2f} COP"
        )
        summary.setFont(QFont("Segoe UI", 12))
        layout.addWidget(summary)

        self.setLayout(layout)
