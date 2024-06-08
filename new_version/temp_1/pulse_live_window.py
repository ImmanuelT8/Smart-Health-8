import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QTimer
import time

uiclass, baseclass = uic.loadUiType("pulse_live_window.ui")

class PulseWindow(baseclass, uiclass):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data = [0] * 500
        self.data_buffer = []
        self.plot_item = self.graphWidget.plot(pen='w')
        self.graphWidget.setXRange(0, 500)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(200)  # Geändert auf 200 ms

        self.last_data_time = time.time()

    def add_data(self, new_data):
        self.data_buffer.extend(new_data)
        current_time = time.time()
        self.time_diff = current_time - self.last_data_time
        self.last_data_time = current_time

    def update_plot(self):
        if self.data_buffer:
            new_value = self.data_buffer.pop(0)
            self.data.append(new_value)
            if len(self.data) > 500:
                self.data.pop(0)
            self.plot_item.setData(self.data)

            # Dynamische Skalierung der Y-Achse basierend auf den Daten
            y_min = min(self.data)
            y_max = max(self.data)
            self.graphWidget.setYRange(y_min - 10, y_max + 10)  # Puffer von 10 für besseren Abstand

            QTimer.singleShot(200, self.update_plot)  # Geändert auf 200 ms
        else:
            # Berechnung der zusätzlichen Pause basierend auf der Zeitdifferenz und der Anzahl der verbleibenden Datenpunkte
            additional_pause = max(0, self.time_diff - (0.2 * len(self.data_buffer))) * 1000
            QTimer.singleShot(additional_pause, self.resume_plotting)

    def resume_plotting(self):
        self.timer.start(200)  # Geändert auf 200 ms

    def closeEvent(self, event):
        self.closed.emit()
        self.timer.stop()

if __name__ == "__main__":
    app = QApplication([])
    pulse_plotter_window = PulseWindow()
    pulse_plotter_window.showFullScreen()
    app.exec()
