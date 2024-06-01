import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QDialog
from PyQt6.QtGui import QAction

from PyQt6 import uic
import numpy as np
import time
from PyQt6 import QtWidgets, uic
import sys
from PyQt6.QtCore import Qt, pyqtSignal

SAMPE_ARRAY = 100

# Globale Variable zur Speicherung des aktuellen IR-Filters
current_filter_IR = "no_filter"

# Laden der UI-Datei für das Einstellung Fenster im Liveplotter
uiclass, baseclass = uic.loadUiType("plotter_live_window.ui")

# Laden der UI-Datei für das Einstellungsfenster das in dem  Liveplotter Fenster - Menü geöffnet wird
einstellung_ui_file = "liveplotter_einstellungen.ui"
einstellung_ui, einstellung_base = uic.loadUiType(einstellung_ui_file)

# Laden der UI-Datei für das Einstellungsfenster das in dem  Liveplotter Fenster - Menü geöffnet wird
filter_ir_ui_file = "filter_live_plotter_ir.ui"
filter_ir_ui, filter_ir_base = uic.loadUiType(filter_ir_ui_file)


class FilterIRWindow(filter_ir_base, filter_ir_ui):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("filter_live_plotter_ir.ui")
        self.setupUi(self)


class LiveplotterEinstellungenWindow(einstellung_base, einstellung_ui):
    checkbox_ir_state_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("liveplotter_einstellungen.ui")
        self.setupUi(self)
        self.actionIR.triggered.connect(self.filter_ir_fenster_clicked)
        self.ui.menubar.addAction(self.actionIR)  # Hinzufügen der Aktion zum Menü
        self.checkbox_ir.stateChanged.connect(self.plot_data_checkbox_ir_state_changed)

    def plot_data_checkbox_ir_state_changed(self, state):
        self.checkbox_ir_state_changed.emit(state)

    def filter_ir_fenster_clicked(self):
        print("Filter IR gedrückt")
        self.filter_ir_fenster = FilterIRWindow()
        self.filter_ir_fenster.show()
        self.filter_ir_fenster.pushButton.clicked.connect(self.apply_filters_IR)  # Verknüpfen des Buttons Update im Fenster IR Filter mit der Funktion die die Variable updatet

    def apply_filters_IR(self):
        global current_filter_IR
        print("Update Button in IR Filter geklickt")
        # Funktion zum Anwenden der ausgewählten Filter
        current_text = self.filter_ir_fenster.filter_ir_comobox_1.currentText()

        if current_text == "Mittelwertfilter":
            current_filter_IR = "mean_filter"
        else:
            current_filter_IR = "no_filter"

        print("Filter angewendet für IR:", current_filter_IR)


class PlotterWindow(baseclass, uiclass):
    def __init__(self, df):
        super().__init__()
        # Laden der UI-Datei
        ui_file = "plotter_live_window.ui"
        ui = uic.loadUi(ui_file)
        self.plot_item = None
        self.setupUi(self)
        self.actionAktualisieren.triggered.connect(self.update_button_plotter)
        self.data = [0] * SAMPE_ARRAY
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.timer_out)
        self.timer.start(800)  # Aktualisierung alle 50 Millisekunden
        self.liveplotterEinstellungen.triggered.connect(self.einstellungen_klicked)
        einstellungs_fenster = LiveplotterEinstellungenWindow()
        einstellungs_fenster.checkbox_ir_state_changed.connect(self.checkbox_ir_state_changed)
        self.checkbox_state_ir = False

    def checkbox_ir_state_changed(self, state):
        # Hier können Sie den Wert 'state' verwenden, der von der Checkbox im Einstellungsfenster übergeben wurde
        print("IR Checkbox Zustand geändert:", state)
        self.checkbox_state_ir = state

    def timer_out(self):
        global current_filter_IR
        print("timer out")
        if self.checkbox_state_ir:
            print("Aktueller Filter", current_filter_IR)
            self.update_plot_data()

    def plot_data_checkbox_ir_state_changed(self, state):
        if state:
            # Checkbox ist aktiviert, Live-Daten plotten
            print("IR Checkbox on, Program ist in Plotter Window plot_data_checkbox_ir_state_changed")
            self.update_plot_data()
        else:
            # Checkbox ist deaktiviert, Live-Daten nicht plotten
            pass

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
        self.einstellungs_fenster.checkbox_ir.stateChanged.connect(self.checkbox_ir_state_changed)
        self.einstellungs_fenster.show()plotter


# Wenn sich die Comobox (Dropdown Menü) im Fenster IR Filter verändert, dann printet er den ausgewählten Filter

class FilterIRWindow(filter_ir_base, filter_ir_ui):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("filter_live_plotter_ir.ui")
        self.setupUi(self)
        self.filter_ir_comobox_1.currentIndexChanged.connect(self.comboBox_changed)

    def comboBox_changed(self, index):
        current_text = self.filter_ir_comobox_1.currentText()
        if current_text == "Mittelwertfilter":
            print("Mittelwertfilter ausgewählt für IR ")
            # Hier kannst du die Daten mit dem Mittelwertfilter verarbeiten

        if current_text == "Kein Filter":
            print("Kein Filter ausgewählt für IR")
            # Hier kannst du die Daten mit dem Mittelwertfilter verarbeiten
