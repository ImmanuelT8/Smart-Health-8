import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
import numpy as np
from PySide6.QtGui import Qt


uiclass, baseclass = uic.loadUiType("plotter_window.ui")

class PlotterWindow(QMainWindow, uiclass):
    def __init__(self, df):
        super().__init__()
        self.plot_item = None
        self.setupUi(self)
        self.actionAktualisieren.triggered.connect(self.update_button_plotter)

    def plot(self, df):
        print("Daten des DF in Plotter Modul")
        print(df)
        spo2_list = df['Red'].astype(float) # Gibt alle Werte aus

        # spo2_list = df['Red'][:100].astype(float) #gibt die ersten 100 Werte aus
        # spo2_list = df['Red'].tail(100).astype(float) # gibt die letzten 100 Werte aus, klappt nicht

        print("spo2_list = ")
        print(spo2_list)
        print("letzte 100 Werte")
        letzte_werte = df['Red'].tail(50).astype(float)
        print(letzte_werte)
        self.plot_item = self.graphWidget.plot() # Erstellen des Graphen
        self.plot_item .setData(spo2_list)  # Aktualisieren der Daten des Graphen
        self.plot_item.setData(y=spo2_list)  # Aktualisiere die Daten des Graphen


    def update_button_plotter(self):

        # Aktualisiere den Plot mit den neuen Daten
        from safe_to_excel import df
        spo2_list = df['Red'].tail(50).astype(float)  # Gibt die letzten 100 Werte aus
        spo2_list.reset_index(drop=True, inplace=True)  # Setze den Index zurück
        self.plot_item.setData(y=np.array(spo2_list))  # Aktualisiere die Daten des Graphen
        print(df)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self.update_button_plotter()
        else:
            super().keyPressEvent(event)

