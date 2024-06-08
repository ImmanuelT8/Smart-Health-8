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

        self.main_buffer = []  # Hauptpuffer für zusätzliche Datenpunkte
        self.plot_buffer = []  # Puffer für die zu plottenden Datenpunkte
        self.plot_item = self.graphWidget.plot(pen='w')
        self.graphWidget.setXRange(0, 500)

        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_next_data)
        self.timer.start(20)  # Timer-Intervall auf 20 ms gesetzt

        self.last_data_time = time.monotonic()
        self.total_delay = 0

    def add_data(self, new_data):
        self.main_buffer.extend(new_data)
        current_time = time.monotonic()
        self.total_delay += current_time - self.last_data_time
        self.last_data_time = current_time
        print(f"Data added: {new_data}, Buffer length: {len(self.main_buffer)}")

    def plot_next_data(self):
        if len(self.plot_buffer) < 500:
            if self.main_buffer:
                next_data = self.main_buffer[:min(100, len(self.main_buffer))]
                self.plot_buffer.extend(next_data)
                self.main_buffer = self.main_buffer[len(next_data):]

                if len(self.plot_buffer) >= 500:
                    self.plot_data_and_pause()

    def plot_data_and_pause(self):
        self.plot_item.setData(self.plot_buffer[:500])
        self.plot_buffer = self.plot_buffer[500:]

        # Dynamische Skalierung der Y-Achse basierend auf den Daten
        y_min = min(self.plot_buffer)
        y_max = max(self.plot_buffer)
        self.graphWidget.setYRange(y_min - 10, y_max + 10)  # Puffer von 10 für besseren Abstand

        # Zeitverzögerung ausgeben
        print(f"Total delay: {self.total_delay:.4f} seconds")

        # Pause einlegen, basierend auf der Gesamtverzögerung
        data_handle_delay = self.total_delay - (len(self.plot_buffer) / 100) * 2  # 100 Daten alle 200ms
        if data_handle_delay > 0:
            time.sleep(data_handle_delay)

    def closeEvent(self, event):
        self.closed.emit()
        self.timer.stop()

if __name__ == "__main__":
    app = QApplication([])
    pulse_plotter_window = PulseWindow()
    pulse_plotter_window.showFullScreen()
    app.exec()
