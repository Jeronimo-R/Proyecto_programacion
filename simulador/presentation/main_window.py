from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem,
    QFileDialog, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from utils.circuit_serializer import save_circuit, load_circuit
from utils.constants import COP_PER_KWH
from business.device_manager import DeviceManager
from presentation.device_form import DeviceForm


# ------------------------------
# Dashboard Card Component
# ------------------------------
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


# ------------------------------
# Chart Component
# ------------------------------
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


# ------------------------------
# MAIN WINDOW
# ------------------------------
class MainWindow(QWidget):
    def __init__(self, device_manager: DeviceManager):
        super().__init__()
        self.device_manager = device_manager

        self.setWindowTitle("Home Energy Panel")
        self.resize(1400, 800)

        self.selected_device = None
        self.chart = None

        self.apply_style()
        self.build_ui()

        # Timer 1 tick = 1 simulated minute
        self.timer = QTimer()
        self.timer.timeout.connect(self.realtime_update)
        self.timer.start(1000)
    def delete_selected_device(self):
        if not self.selected_device:
            return

        name = self.selected_device.name
        self.device_manager.remove_device(name)

        # eliminar de la lista GUI
        for i in range(self.device_list.count()):
            if self.device_list.item(i).text() == name:
                self.device_list.takeItem(i)
                break

        self.selected_device = None
        self.device_info.setText("Select a device")

        # Recargar dashboard
        self.update_dashboard()
        self.update_chart()

    # ------------------------------
    # Style
    # ------------------------------
    def apply_style(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ffffff"))
        self.setPalette(palette)

    # ------------------------------
    # UI Builder
    # ------------------------------
    def build_ui(self):
        main = QHBoxLayout()
        main.addLayout(self.build_sidebar(), 1)
        main.addLayout(self.build_dashboard(), 4)
        self.setLayout(main)

    # ------------------------------
    # SIDEBAR
    # ------------------------------
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

        from PyQt5.QtWidgets import QPushButton

        btn_add = QPushButton("Add Device")
        btn_add.clicked.connect(self.open_add_device_form)

        btn_edit = QPushButton("Edit Device")
        btn_edit.clicked.connect(self.open_edit_device_form)

        btn_delete = QPushButton("Delete Device")
        btn_delete.clicked.connect(self.delete_selected_device)

        btn_save = QPushButton("Save Circuit")
        btn_save.clicked.connect(self.save_circuit)

        btn_load = QPushButton("Load Circuit")
        btn_load.clicked.connect(self.load_circuit)

        layout.addWidget(title)
        layout.addWidget(self.device_list)
        layout.addWidget(self.device_info)
        layout.addWidget(btn_add)
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        layout.addWidget(btn_save)
        layout.addWidget(btn_load)

        return layout


    # ------------------------------
    # DASHBOARD
    # ------------------------------
    def build_dashboard(self):
        layout = QVBoxLayout()

        header = QLabel("Home Energy Panel")
        header.setFont(QFont("Segoe UI", 28, QFont.Bold))
        header.setStyleSheet("padding: 10px; color: #2c3e50;")
        layout.addWidget(header)

        # COP label fixed
        cop_label = QLabel(f"Energy Price: {COP_PER_KWH} COP/kWh")
        cop_label.setFont(QFont("Segoe UI", 12))
        cop_label.setStyleSheet("color: #444; padding-left: 12px;")
        layout.addWidget(cop_label)

        # Dashboard cards
        cards = QHBoxLayout()

        self.card_current = DashboardCard("Current Consumption", 0, "W")
        self.card_daily = DashboardCard("Daily Consumption", 0, "Wh")
        self.card_monthly = DashboardCard("Monthly Consumption", 0, "Wh")
        self.card_global_cost = DashboardCard("Global Cost", 0, "COP")

        cards.addWidget(self.card_current)
        cards.addWidget(self.card_daily)
        cards.addWidget(self.card_monthly)
        cards.addWidget(self.card_global_cost)

        layout.addLayout(cards)

        # Chart container
        self.chart_layout = QVBoxLayout()
        layout.addLayout(self.chart_layout)

        btn_month = QPushButton("Monthly History")
        btn_month.clicked.connect(self.open_monthly_history)

        layout.addWidget(btn_month)


        return layout

    # ------------------------------
    # REALTIME UPDATE LOOP
    # ------------------------------
    def realtime_update(self):
        self.device_manager.tick()
        self.update_dashboard()
        self.update_chart()
        self.update_device_info()

    # ------------------------------
    # Dashboard information
    # ------------------------------
    def update_dashboard(self):
        devices = self.device_manager.get_all()

        # Current power
        current_total = sum(d.history[-1].power for d in devices if d.history)

        # Daily Wh (from history)
        daily_total = sum(sum(m.power * (1 / 60) for m in d.history) for d in devices)

        # Monthly Wh (accumulated)
        monthly_total = sum(d.sensor.accumulated_energy for d in devices)

        # Global cost
        global_cost = sum(
            (d.sensor.accumulated_energy / 1000) * COP_PER_KWH
            for d in devices
        )

        self.card_current.value_label.setText(f"{current_total:.2f} W")
        self.card_daily.value_label.setText(f"{daily_total:.2f} Wh")
        self.card_monthly.value_label.setText(f"{monthly_total:.2f} Wh")
        self.card_global_cost.value_label.setText(f"{global_cost:,.2f} COP")

    # ------------------------------
    # Device info panel
    # ------------------------------
    def show_device_info(self):
        name = self.device_list.currentItem().text()
        self.selected_device = self.device_manager.find(name)
        self.update_device_info()

    def update_device_info(self):
        if not self.selected_device or not self.selected_device.history:
            return

        d = self.selected_device
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

    # ------------------------------
    # Daily Virtual Consumption Chart
    # ------------------------------
    def update_chart(self):
        if self.chart:
            self.chart.setParent(None)

        devices = self.device_manager.get_all()
        x = list(range(24))
        y_total = [0] * 24

        # Fill 24-hour chart using simulated minutes
        for d in devices:
            for index, m in enumerate(d.history):
                virtual_minute = (
                    self.device_manager.simulated_minutes - (len(d.history) - index)
                )
                if virtual_minute < 0:
                    continue

                virtual_hour = (virtual_minute // 60) % 24
                y_total[virtual_hour] += m.power * (1 / 60)

        self.chart = EnergyChart(x, y_total, "Daily Virtual Consumption (Wh)")
        self.chart_layout.addWidget(self.chart)

    # ------------------------------
    # Monthly History Window
    # ------------------------------
    def open_monthly_history(self):
        from presentation.monthly_history_window import MonthlyHistoryWindow
        win = MonthlyHistoryWindow(self.device_manager)
        win.exec_()


    # ------------------------------
    # Save / Load
    # ------------------------------
    def save_circuit(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Circuit", "", "JSON (*.json)")
        if filename:
            save_circuit(filename, self.device_manager)

    def load_circuit(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Circuit", "", "JSON (*.json)")
        if filename:
            new_manager = load_circuit(filename)
            if new_manager:
                self.device_manager = new_manager
                self.refresh_device_list()

    def refresh_device_list(self):
        self.device_list.clear()
        for d in self.device_manager.get_all():
            self.device_list.addItem(d.name)

    # ------------------------------
    # Add Device Form
    # ------------------------------
    def open_add_device_form(self):
        form = DeviceForm(self, self.refresh_device_list)  # ← FIX
        form.exec_()

        if getattr(form, "created_device", None):
            self.device_manager.add_device(form.created_device)
            self.device_list.addItem(QListWidgetItem(form.created_device.name))

    def open_edit_device_form(self):
        if not self.selected_device:
            return

        form = DeviceForm(self, self.refresh_device_list, device=self.selected_device)
        form.exec_()

        if getattr(form, "edited", False):
            self.refresh_device_list()
