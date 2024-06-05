import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QDialog
from PyQt6.QtGui import QAction

from PyQt6 import uic
import numpy as np
import time
from PyQt6 import QtWidgets, uic
import sys
from PyQt6.QtCore import Qt, pyqtSignal
from filter_modul import smooth_data
import time
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtCore import QTimer
import asyncio
import threading

exit_flag = False

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
        exit_flag = False
        print("exit_flag INIT =",exit_flag)

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
        self.liveplotterEinstellungen.triggered.connect(self.einstellungen_klicked)
        einstellungs_fenster = LiveplotterEinstellungenWindow()
        einstellungs_fenster.checkbox_ir_state_changed.connect(self.checkbox_ir_state_changed)
        self.checkbox_state_ir = False

    
        self.data_updater = DataUpdater(df)  # Instanziierung der DataUpdater-Klasse
        self.data_updater.data_updated.connect(self.on_data_updated) # Verbindet die Funktion on_dat_updated mit data_updater
        self.data_updater.start()

         



        
     # Diese Methode wird aufgerufen, jedes Mal wenn das Signal data_updated von DataUpdater emittiert wird.  
     # Sie aktualisiert list_data_ir_puffer in PlotterWindow, so dass die neuesten Daten von DataUpdater verfügbar sind.   

    def on_data_updated(self):
            self.list_data_ir_puffer = self.data_updater.list_data_ir_puffer


    def closeEvent(self, event):
        print("close event")
        # Stoppen des DataUpdater-Threads beim Schließen des Fensters

        super().closeEvent(event)
        global exit_flag
        exit_flag = True
        print("exit_flag = ",exit_flag)
        time.sleep(1)
        self.data_updater.stop()
        self.data_updater.wait()
        time.sleep(1)
        


    def checkbox_ir_state_changed(self, state):
        # Hier können Sie den Wert 'state' verwenden, der von der Checkbox im Einstellungsfenster übergeben wurde
        print("IR Checkbox Zustand geändert:", state)
        self.checkbox_state_ir = state

        if state:  # Wenn die Checkbox aktiviert ist
            print("IR Checkbox aktiviert, Daten werden aktualisiert...")

             #Prüft ob der Aktuelle Filter für das IR Signal aus ist und plottet dann die Rohdaten
            if current_filter_IR == "no_filter":

                #self.update_plot_data_no_filter()
                # Die asynchrone Funktion
                async def test_async():
                    global exit_flag
                    exit_flag = False

                    print("exit_flag test_async =",exit_flag)

                    while self.checkbox_state_ir == 2:

                        self.data_to_plot_IR = self.data_updater.list_data_ir_puffer[:SAMPE_ARRAY]


                        if self.data_to_plot_IR: print("Daten zum Plotten:", self.data_to_plot_IR)

                         # Verzögerung von 1700 ms
                        time.sleep(0)

                       # Lösche die ersten 100 Datenpunkte
                        self.data_updater.list_data_ir_puffer = self.data_updater.list_data_ir_puffer[SAMPE_ARRAY:]

                        await asyncio.sleep(0.01)

                # Die Funktion, die in einem separaten Thread ausgeführt wird
                def run_async_function():
                    asyncio.run(test_async())

                # Starten des Threads
                _thread = threading.Thread(target=run_async_function)
                _thread.start()

            if current_filter_IR == "mean_filter":

                self.update_plot_data_mean_filter()



   


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

        
    
        #Updatet Plottdaten für IR Werte ohne Filter


        '''
    def update_plot_data_no_filter(self):
        global list_data_ir_puffer
        global SAMPE_ARRAY

        # Erhalte die ersten 100 Datenpunkte aus der Liste
        data_to_plot_IR = self.data_updater.list_data_ir_puffer[:SAMPE_ARRAY]


        index = 0  # Startindex für den Datenabruf
        for data_point_IR in data_to_plot_IR:  #data_point: Diese Variable repräsentiert jeden einzelnen Datenpunkt, der während der Iteration durch data_to_plot geplottet wird.
            print(f"Datenpunkt {index + 1}: {data_point_IR}")  # Datenpunkt printen

            self.data = np.roll(self.data, -1)
            self.data[-1] = data_point_IR
            self.plot_item.setData(y=self.data)  # Aktualisieren der Daten des Plot-Items

            pg.QtCore.QCoreApplication.processEvents()  # Aktualisieren des Plot-Widgets
            time.sleep(0.017)  # Pause von 10 Millisekunden

            index += 1


         # Entferne die geplotteten Datenpunkte aus der Liste
        self.data_updater.list_data_ir_puffer = self.data_updater.list_data_ir_puffer[SAMPE_ARRAY:]

        '''
        '''
    def update_plot_data_no_filter(self):
        global SAMPE_ARRAY

 

        while True:  # Schleife wird ausgeführt, solange die Checkbox aktiviert ist
            # Erhalte die ersten 100 Datenpunkte aus der Liste
            self.data_to_plot_IR = self.data_updater.list_data_ir_puffer[:SAMPE_ARRAY]
            print("Daten zum Plotten:", self.data_to_plot_IR)

            # Verzögerung von 1700 ms
            time.sleep(1.7)

            # Lösche die ersten 100 Datenpunkte
            self.data_updater.list_data_ir_puffer = self.data_updater.list_data_ir_puffer[SAMPE_ARRAY:]

            '''

   

    def update_plot_data_mean_filter(self):
        print("Update Plot Data Mittelwert")
        from safe_to_excel import df
        IR_raw_list = df['Red'].tail(SAMPE_ARRAY).astype(float)  # Gibt die letzten 100 Werte aus
        IR_raw_list.reset_index(drop=True, inplace=True)  # Setze den Index zurück, damit beginnen wir beim Index 0

        # Daten glätten, wobei der vorherige remainder verwendet wird
        IR_smooth_list, self.remainder = smooth_data(IR_raw_list, getattr(self, 'remainder', None))

        # Geplättete Daten plotten
        self.plot_smoothed_data(IR_smooth_list)

        
    # Funktion die die gefilterten IR Daten (Mittelwert) plottet

    def plot_smoothed_data(self, smoothed_data):
        index = 0  # Startindex für den Datenabruf
        while index < SAMPE_ARRAY:
            data_point = smoothed_data[index]  # Datenpunkt für den aktuellen Index

            print(f"Glätteter Datenpunkt {index + 1}: {data_point}")  # Datenpunkt printen

            self.data = np.roll(self.data, -1)  # Verschiebt oder rollt die Elemente des Arrays um eine Position
            self.data[-1] = data_point  # Setzt den Datenpunkt an das Ende des Arrays
            self.plot_item.setData(y=self.data)  # Aktualisieren der Daten des Plot-Items

            pg.QtCore.QCoreApplication.processEvents()  # Aktualisieren des Plot-Widgets
            time.sleep(0.017)  # Pause von 10 Millisekunden

            index += 1




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
        self.einstellungs_fenster.show()


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


class DataUpdater(QThread):
    data_updated = pyqtSignal()

    def __init__(self, df):
        super().__init__()
        self.df = df
        self.df_old = None  # DataFrame zur Überprüfung auf Änderungen
        self.list_data_ir_puffer = []  # Liste für neue Daten

    def run(self):
        print("DataUpdater Thread gestartet")  # Ausgabe, wenn der Thread gestartet wird

        while True:
            # Überprüfen, ob neue Daten verfügbar sind
            df_new = self.df_update()  # Aktualisiere den DataFrame
            if not df_new.equals(self.df_old):
                # Neue Daten vorhanden
                self.list_data_ir_puffer += df_new['Red'].tail(SAMPE_ARRAY).astype(float).tolist()
                self.df_old = df_new

                if len(self.list_data_ir_puffer) > 500:
                    print("Die Anzahl der Einträge in der Liste IR Puffer ist größer als 500.")

                # Signal senden, um anzuzeigen, dass neue Daten verfügbar sind
                self.data_updated.emit()

            time.sleep(0)  # Beispiel: Wartezeit von 0.1 Sekunden

    def df_update(self):
        from safe_to_excel import df
        return df.copy()




    def stop(self):

        
        self.running = False
        print("Date Updater Thread geschlossen")
        PlotterWindow.close()

        
