import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QTimer, Qt, QThread
import time
import numpy as np

uiclass, baseclass = uic.loadUiType("pulse_live_window.ui")



class Worker(QThread):
    data_processed = pyqtSignal(list)

    def __init__(self, consumer_buffer):
        super().__init__()
        self.consumer_buffer = consumer_buffer

    def run(self):
        while self.consumer_buffer:
            data = [self.consumer_buffer.pop(0)]  # Datum in eine Liste verpacken
            self.data_processed.emit(data)
            time.sleep(0.005)

class PulseWindow(baseclass, uiclass):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graphWidget.setXRange(0, 500)
        
        self.data = np.zeros(500)  # Initialisierung als 1D-ndarray

        self.plot_item = self.graphWidget.plot(pen='w')
        self.main_buffer = []  
        self.consumer_buffer = []  
        self.current_index = 0

    def add_data(self, new_data):
        self.main_buffer.extend(new_data)
        print("Data received at", time.monotonic(), ":", new_data)
        print("Total number of data in buffer:", len(self.main_buffer))

        if len(self.main_buffer) >= 500:
            self.consumer_buffer.extend(self.main_buffer[:500])
            del self.main_buffer[:500]  
            print("consumer_buffer load 500 numbers")
            self.start_plotting()

    def start_plotting(self):
        self.worker = Worker(self.consumer_buffer)
        self.worker.data_processed.connect(self.process_next_data)
        self.worker.start()
  
    def process_next_data(self, data):
        # Konvertierung von list zu ndarray
        print("was sit data? data ist: ", data)

        # Extrahiere das einzelne Element aus der Liste
        value = data[0]  

        # Füge das neue Element am Ende hinzu und entferne das erste Element
        self.data = np.append(self.data[1:], value)  

        print("Index:", self.current_index)
        start_time = time.monotonic()
        if self.current_index == 0:
            print(f"Consumer buffer processing started at: {start_time}")

        # Daten an den Plot übergeben
        self.plot_item.setData(self.data)
        print(f"Plotted value: {value} at index: {self.current_index}")

        self.current_index += 1

        # Überprüfen, ob der Index 500 erreicht hat
        if self.current_index == 500:
            end_time = time.monotonic()
            duration = end_time - start_time
            print(f"Consumer buffer processing ended at: {end_time}")
            print(f"Processing duration: {duration} seconds")
            print("consumer_buffer consumed")
            self.consumer_buffer = []  # Puffer leeren


    def closeEvent(self, event):
        self.closed.emit()

if __name__ == "__main__":
    app = QApplication([])
    pulse_plotter_window = PulseWindow()
    pulse_plotter_window.showFullScreen()
    app.exec()
