from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys


COP_PER_KWH = 750  # Colombian pesos per kWh


class DashboardCard(QFrame):
    def __init__(self, title, value, unit):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border-radius: 12px;
                padding: 10px;
                border: 1px solid #e0e0e0;
            }
        """)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10))
        title_label.setStyleSheet("color: #555;")

        self.value_label = QLabel(f"{value} {unit}")
        self.value_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.value_label.setStyleSheet("color: #1976d2;")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

        self.setLayout(layout)


class EnergyChart(FigureCanvasQTAgg):
    def __init__(self, x, y, title):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

        self.ax.plot(x, y, marker="o")
        self.ax.set_title(title)
        self.ax.set_xlabel("Hour")
        self.ax.set_ylabel("Consumption (Wh)")
        self.ax.grid(True)
        self.fig.tight_layout()


class MainWindow(QWidget):
    def __init__(self, device_manager):
        super().__init__()
        self.device_manager = device_manager

        self.setWindowTitle("Home Energy Panel")
        self.resize(1300, 750)

        self.chart = None
        self.selected_device = None
        self.apply_style()
        self.build_ui()

        # Real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.realtime_update)
        self.timer.start(1000)  # 1 second = 1 minute simulated

    def apply_style(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ffffff"))
        self.setPalette(palette)

    def build_ui(self):
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.build_sidebar(), 1)
        main_layout.addLayout(self.build_dashboard(), 4)
        self.setLayout(main_layout)

    def build_sidebar(self):
        layout = QVBoxLayout()

        title = QLabel("Devices")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.device_list = QListWidget()
        for d in self.device_manager.get_all():
            self.device_list.addItem(QListWidgetItem(d.name))

        self.device_list.itemClicked.connect(self.show_device_info)

        self.device_info = QLabel("Select a device")
        self.device_info.setFont(QFont("Segoe UI", 11))
        self.device_info.setStyleSheet("padding: 10px;")

        layout.addWidget(title)
        layout.addWidget(self.device_list)
        layout.addWidget(self.device_info)

        return layout

    def build_dashboard(self):
        layout = QVBoxLayout()

        header = QLabel("Home Energy Panel")
        header.setFont(QFont("Segoe UI", 28, QFont.Bold))
        header.setStyleSheet("padding: 10px; color: #2c3e50;")

        cards = QHBoxLayout()
        self.card_current = DashboardCard("Current Consumption", 0, "W")
        self.card_daily = DashboardCard("Daily Consumption", 0, "Wh")
        self.card_monthly = DashboardCard("Monthly Consumption", 0, "Wh")

        cards.addWidget(self.card_current)
        cards.addWidget(self.card_daily)
        cards.addWidget(self.card_monthly)

        self.chart_layout = QVBoxLayout()

        layout.addWidget(header)
        layout.addLayout(cards)
        layout.addLayout(self.chart_layout)

        return layout

    def realtime_update(self):
        # generate 1 new minute of data for each device
        for d in self.device_manager.get_all():
            m = d.sensor.generate_measurement()
            d.history.append(m)

            if len(d.history) > 1440:
                d.history.pop(0)

        self.update_dashboard()
        self.update_chart()
        self.update_device_info()

    def update_dashboard(self):
        devices = self.device_manager.get_all()

        current_total = sum(d.history[-1].power for d in devices if d.history)
        daily_total = sum(sum(m.power * (1 / 60) for m in d.history) for d in devices)
        monthly_total = sum(d.sensor.accumulated_energy for d in devices)

        self.card_current.value_label.setText(f"{current_total:.2f} W")
        self.card_daily.value_label.setText(f"{daily_total:.2f} Wh")
        self.card_monthly.value_label.setText(f"{monthly_total:.2f} Wh")

    def update_chart(self):
        if self.chart:
            self.chart.setParent(None)

        devices = self.device_manager.get_all()

        x = list(range(1, 25))
        y = []

        for d in devices:
            hourly = [0] * 24
            for m in d.history:
                hour_index = m.timestamp.hour
                hourly[hour_index] += m.power * (1 / 60)

            y.append(hourly)

        y_total = [sum(values) for values in zip(*y)]

        self.chart = EnergyChart(x, y_total, "Daily Consumption (Wh)")
        self.chart_layout.addWidget(self.chart)

    def show_device_info(self):
        name = self.device_list.currentItem().text()
        self.selected_device = self.device_manager.find(name)
        self.update_device_info()

    def update_device_info(self):
        if not self.selected_device:
            return

        d = self.selected_device

        if not d.history:
            return

        last = d.history[-1]

        cost = (d.sensor.accumulated_energy / 1000) * COP_PER_KWH

        self.device_info.setText(
            f"Device: {d.name}\n"
            f"Voltage: {last.voltage} V\n"
            f"Current: {last.current} A\n"
            f"Power: {last.power} W\n"
            f"Energy: {d.sensor.accumulated_energy:.2f} Wh\n"
            f"Cost approx: {cost:.2f} COP"
        )


def start_gui(device_manager):
    app = QApplication(sys.argv)
    win = MainWindow(device_manager)
    win.show()
    sys.exit(app.exec_())
