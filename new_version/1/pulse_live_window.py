import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QDialog
from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6 import uic
import numpy as np
from PyQt6.QtCore import pyqtSignal


# Laden der UI-Datei für das Einstellung Fenster im Liveplotter
uiclass, baseclass = uic.loadUiType("pulse_live_window.ui")

class PulseWindow(baseclass, uiclass):
    # Signal definieren
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Laden der UI-Datei
        self.setupUi(self)
        # Erstellen einer Liste mit 100 Nullen
        self.data = [0] * 100

        # Erstellen des Plot-Items
        self.plot_item = self.graphWidget.plot(self.data, pen='w')


        # Verbindung des Signals mit der closeEvent-Funktion
        self.closed.connect(self.closeEvent)

    def update_plot(self):
        self.plot_item.setData(self.data)

    def update_data(self, new_data):
        self.data = new_data
        self.plot_item.setData(self.data)



    # closeEvent-Funktion, die aufgerufen wird, wenn das Fenster geschlossen wird
    def closeEvent(self, event: QCloseEvent):
        # Signal emittieren, wenn das Fenster geschlossen wird
        print("pulse window cosed")
        self.closed.emit()

    def add_data(self, red_data, ir_data):
        # Neue Daten anzeigen (hier nur als Beispiel print)
        print(f"New red data: {red_data}")
        print(f"New IR data: {ir_data}")
        # Aktualisiere den Plot mit den neuen Daten
        self.data = red_data  # Beispielweise nur die roten Daten verwenden
        self.plot_item.setData(self.data)

