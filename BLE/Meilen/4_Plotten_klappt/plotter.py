import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow
import numpy as np
from PyQt6.QtCore import pyqtSignal




uiclass, baseclass = pg.Qt.loadUiType("plotter_window.ui")




class PlotterWindow(QMainWindow, uiclass):
    def __init__(self, df):
        super().__init__()

        self.setupUi(self)

    def plot(self, df):
        print("Daten des DF in Plotter Modul")
        print(df)
        spo2_list = df['Red'].astype(float) # Gibt alle Werte aus

        # spo2_list = df['Red'][:100].astype(float) #gibt die ersten 100 Werte aus
        # spo2_list = df['Red'].tail(10).astype(float)
        # spo2_list = df['Red'].tail(100).astype(float)

        print("spo2_list = ")
        print(spo2_list)
        spo2_list = spo2_list[np.isfinite(spo2_list)]  # Filtere ungültige Werte
        self.graphWidget.plot(spo2_list)

            # spo2_list = pd.Series(df['Red'][-100:]).astype(float)  # Die letzten 100 Werte aus dem DataFrame extrahieren
            # spo2_list = spo2_list.values.astype(float)  # Daten in Gleitkommazahlen umwandeln



