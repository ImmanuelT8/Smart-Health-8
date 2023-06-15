import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QDialog
from PyQt6.QtGui import QAction

from PyQt6 import uic
import numpy as np
import time
from PyQt6 import QtWidgets, uic
import sys
from PyQt6.QtCore import Qt


SAMPE_ARRAY = 100


# Laden der UI-Datei für das Einstellung Fenster im Liveplotter
uiclass, baseclass = uic.loadUiType("plotter_live_window.ui")


# Laden der UI-Datei für das Einstellungsfenster das in dem  Liveplotter Fenster - Menü geöfnet wird
einstellung_ui_file = "liveplotter_einstellungen.ui"
einstellung_ui, einstellung_base = uic.loadUiType(einstellung_ui_file)


# Laden der UI-Datei für das Einstellungsfenster das in dem  Liveplotter Fenster - Menü geöfnet wird
filter_ir_ui_file = "filter_live_plotter_ir.ui"
filter_ir_ui, filter_ir_base = uic.loadUiType(filter_ir_ui_file)


class FilterIRWindow(filter_ir_base, filter_ir_ui):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("filter_live_plotter_ir.ui")
        self.setupUi(self)







class LiveplotterEinstellungenWindow(einstellung_base, einstellung_ui):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("liveplotter_einstellungen.ui")
        self.setupUi(self)
        self.actionIR.triggered.connect(self.filter_ir_fenster_clicked)
        self.ui.menubar.addAction(self.actionIR)  # Hinzufügen der Aktion zum Menü


    def filter_ir_fenster_clicked(self):
        print("Filter IR gedrückt")
        self.filter_ir_fenster = FilterIRWindow()
        self.filter_ir_fenster.show()


class PlotterWindow(baseclass, uiclass):
    def __init__(self, df):
        super().__init__()
        # Laden der UI-Datei
 
        ui_file = "plotter_live_window.ui"
        ui = uic.loadUi(ui_file)
        self.plot_item = None
        self.setupUi(self)
        self.actionAktualisieren.triggered.connect(self.update_button_plotter)
        self.data = np.random.normal(size=SAMPE_ARRAY)  # Beispiel für zufällige Daten
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(800)  # Aktualisierung alle 50 Millisekunden
        self.liveplotterEinstellungen.triggered.connect(self.einstellungen_klicked)




    def plot(self, df):
        self.plot_item = self.graphWidget.plot(self.data, pen='w')  # Erstellen des Plot-Items


    def update_plot_data(self):
        from safe_to_excel import df
        spo2_list = df['Red'].tail(SAMPE_ARRAY).astype(float)  # Gibt die letzten 100 Werte aus
        spo2_list.reset_index(drop=True, inplace=True)  # Setze den Index zurück

        index = 0  # Startindex für den Datenabruf
        while index < SAMPE_ARRAY:
            data_point = spo2_list[index]  # Datenpunkt für den aktuellen Index

            print(f"Datenpunkt {index + 1}: {data_point}")  # Datenpunkt printen

            self.data = np.roll(self.data, -1)
            self.data[-1] = data_point
            self.plot_item.setData(y=self.data)  # Aktualisieren der Daten des Plot-Items

            pg.QtCore.QCoreApplication.processEvents()  # Aktualisieren des Plot-Widgets
            time.sleep(0.017)  # Pause von 10 Millisekunden

            index += 1

        # Nachdem alle 100 Datenpunkte abgearbeitet wurden
        # Aktualisiert das DataFrame `df` und ladet neue Daten
        from safe_to_excel import df
        spo2_list = df['Red'].tail(SAMPE_ARRAY).astype(float)  # Gibt die letzten 100 Werte aus
        spo2_list.reset_index(drop=True, inplace=True)  # Setze den Index zurück

        index = 0  # Setze den Index auf 0 für den nächsten Durchlauf



    def update_button_plotter(self):
        einstellungs_fenster = LiveplotterEinstellungenWindow()
        einstellungs_fenster.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self.update_button_plotter()
        else:
            super().keyPressEvent(event)


    def einstellungen_klicked(self):
        print("Einstellungen in Liveplotter gedrückt")
        self.einstellungs_fenster = LiveplotterEinstellungenWindow()
        self.einstellungs_fenster.show()


    def filter_ir_fenster_clicked(self):
            print("Filter IR gedrückt")
            filter_ir_fenster.show()  # Anzeigen des Plotter-Fensters



            


