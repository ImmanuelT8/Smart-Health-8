import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
import numpy as np
from PySide6.QtGui import Qt
import time


uiclass, baseclass = uic.loadUiType("plotter_live_window.ui")

class PlotterWindow(QMainWindow, uiclass):
    def __init__(self, df):
        super().__init__()
        self.plot_item = None
        self.setupUi(self)
        self.actionAktualisieren.triggered.connect(self.update_button_plotter)

        self.data = np.random.normal(size=100)  # Beispiel für zufällige Daten
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(800)  # Aktualisierung alle 50 Millisekunden

    def plot(self, df):
        self.plot_item = self.graphWidget.plot(self.data, pen='w')  # Erstellen des Plot-Items


    def update_plot_data(self):
        from safe_to_excel import df
        spo2_list = df['Red'].tail(100).astype(float)  # Gibt die letzten 100 Werte aus
        spo2_list.reset_index(drop=True, inplace=True)  # Setze den Index zurück

        index = 0  # Startindex für den Datenabruf
        while index < 100:
            data_point = spo2_list[index]  # Datenpunkt für den aktuellen Index

            print(f"Datenpunkt {index + 1}: {data_point}")  # Datenpunkt printen

            self.data = np.roll(self.data, -1)
            self.data[-1] = data_point
            self.plot_item.setData(y=self.data)  # Aktualisieren der Daten des Plot-Items

            pg.QtCore.QCoreApplication.processEvents()  # Aktualisieren des Plot-Widgets
            time.sleep(0.017)  # Pause von 10 Millisekunden

            # pg.QtCore.QTimer.singleShot(50,
           # pg.QtCore.QCoreApplication.instance().quit)  # Warten auf Timer-Timeout (50 ms)

            index += 1

        # Nachdem alle 100 Datenpunkte abgearbeitet wurden
        # Aktualisieren Sie das DataFrame `df` und laden Sie neue Daten
        from safe_to_excel import df
        spo2_list = df['Red'].tail(100).astype(float)  # Gibt die letzten 100 Werte aus
        spo2_list.reset_index(drop=True, inplace=True)  # Setze den Index zurück

        index = 0  # Setze den Index auf 0 für den nächsten Durchlauf



    def update_button_plotter(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self.update_button_plotter()
        else:
            super().keyPressEvent(event)
