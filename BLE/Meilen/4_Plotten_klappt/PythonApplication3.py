# -*- coding: latin-1 -*-
import sys
from PyQt6 import uic
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread, pyqtSignal
import asyncio
import bleak
import pandas as pd
import asyncio
import threading
import numpy
from prettytable import PrettyTable
from bleak import BleakClient
from PyQt6 import QtGui
import subprocess
import time
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import pyqtgraph as pg
from safe_to_excel import spo2_list, ir_list
import plotter





import safe_to_excel
from safe_to_excel import filename

from datetime import datetime



# Erstellen Sie eine Instanz der QApplication
app = QApplication(sys.argv)

# Laden Sie die UI-Datei
ui_file = "qt1.ui"  # Geben Sie den Pfad zur UI-Datei an
ui = uic.loadUi(ui_file)



# Zugriff auf das QLabel-Objekt mit dem Objektnamen "logo"
logo_label = ui.logo

# Setzen des Pixmaps f?r das QLabel
logo_label.setPixmap(QtGui.QPixmap("logo.png"))

# Zugriff auf den Button mit dem Objektnamen "Start" und andere
Start = ui.Start
Stopp = ui.Stopp 
Plotter = ui.Plotter 
Trainiere = ui.Trainiere
Einstellungen = ui.Einstellungen
actionRohdaten = ui.actionRohdaten




# Neues QMainWindow-Objekt f?r das Einstellungen-Fenster
einstellungen_window = QMainWindow()
einstellungen_window_ui = uic.loadUi("einstellungen_window.ui")
einstellungen_window.setCentralWidget(einstellungen_window_ui)



# Neues QMainWindow-Objekt f?r das Tabellen-Fenster (Rohdatein)
rohdaten_window = QMainWindow()
rohdaten_window_ui = uic.loadUi("rohdaten_window.ui")
rohdaten_window.setCentralWidget(rohdaten_window_ui)


# Speichern Sie eine Referenz auf den aktuellen Worker-Thread
current_worker = None
current_worker_data_array = None


# Werte definieren
Variable1 = 50
Variable2 = "SAMPLEAVG_4"
Variable3 = "MODE_MULTILED"
Variable4 = "SAMPLERATE_200"
Variable5 = "PULSEWIDTH_411"
Variable6 = "ADCRANGE_16384"

# MAC-Adresse des ESP32
mac_address = 'CC:50:E3:9C:15:02'  # Ersetzen Sie dies durch die MAC-Adresse Ihres ESP32
UUID3 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"





# Klasse f?r das Updaten des ESP
class Worker(QThread):
    completed = pyqtSignal()
    received = pyqtSignal(str)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def do_work():
            try:
                self.received.emit("Suche Ger?t")  # Text "Suche Ger?te" anzeigen
                print("Suche Ger?t")
                einstellungen_window_ui.Update.setEnabled(False)


                client = bleak.BleakClient(mac_address)
                await self.connect_client(client)  # Verbindung herstellen

                update_progress(einstellungen_window_ui.progressBar)  # Aktualisieren Sie den Fortschrittsbalken im Einstellungsfenster

                # String erstellen
                str_parameters = f"{Variable1},{Variable2},{Variable3},{Variable4},{Variable5},{Variable6}"

                # Byte-Array erstellen
                byte_array = str_parameters.encode('ascii')

                print("Sende Werte")
                # Array senden
                await client.write_gatt_char(UUID3, byte_array)

                # Daten vom ESP32 ?ber BLE empfangen
                received = False  # Variable, um anzuzeigen, ob Daten empfangen wurden

                while not received and not self.isInterruptionRequested():
                    data = await client.read_gatt_char(UUID3)
                    if data:
                        value = data.decode('utf-8')
                        print(f"{value}")
                        received = True
                        self.received.emit(value)
                        einstellungen_window_ui.Update.setEnabled(True) #Schaltet den Update Button wieder ein

                await self.disconnect_client(client)  # Verbindung trennen
            except Exception as e:
                print("Nicht verbunden")
                einstellungen_window_ui.Update.setEnabled(True) #Schaltet den Update Button wieder ein

                print(e)
                self.received.emit("Ger?t nicht gefunden")
                einstellungen_window_ui.Parameter_Update_Text.setStyleSheet("color: red;")
                Parameter_Update_Text = "Ger?t nicht gefunden"


            self.completed.emit()

        loop.run_until_complete(do_work())

    async def connect_client(self, client):
        await client.connect()

    async def disconnect_client(self, client):
        await client.disconnect()


# Q Thread der das Skript safe to excel ?ffnet und handhabt

class SafeToExcelThread(QThread): 
    completed = pyqtSignal()

    def run(self):

        safe_to_excel.start_threads()





        self.completed.emit()


class PruefeDateinameThread(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, dateiname):
        super().__init__()
        self.dateiname = dateiname

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.pruefe_dateiname(self.dateiname))
        loop.close()
        self.finished.emit(True)

    async def pruefe_dateiname(self, Dateiname):
        

        
        from safe_to_excel import Dateiname



        if Dateiname == 0:
            safe_to_excel.start_threads() 
        

        else:
            Start.setEnabled(False)
            Stopp.setEnabled(True)
            Plotter.setEnabled(True)
            Trainiere.setEnabled(True)

        await asyncio.sleep(17)  # 30 Sekunden warten
        from safe_to_excel import Dateiname


        print (Dateiname)
        if Dateiname != 0:
            print ("Datei angelegt")

            Start.setEnabled(False)
            Stopp.setEnabled(True)
            Plotter.setEnabled(True)
            Trainiere.setEnabled(True)

        else:
            Start.setEnabled(True)


        await asyncio.sleep(5)  # Beispiel: 5 Sekunden warten
        # F?hren Sie Ihre ?berpr?fungen durch und senden Sie das Ergebnis zur?ck
        is_valid = True  # Beispiel: Dateiname ist g?ltig

        self.finished.emit(is_valid)


def update_progress(progress_bar):
    current_value = progress_bar.value()
    if current_value < progress_bar.maximum():
        progress_bar.setValue(current_value + 1)
        # F?gen Sie hier Ihren eigenen Aktualisierungscode hinzu
        # z.B. Datenverarbeitung oder andere Aktionen
        # Hier wird der Wert des Fortschrittsbalkens um 1 erh?ht
        # und der Aktualisierungsprozess kann fortgesetzt werden
        update_progress(progress_bar)  # Rufen Sie die Methode erneut auf, um den Fortschritt weiter zu aktualisieren



# Erstellen Sie eine globale Variable f?r den SafeToExcelThread
global safe_to_excel_thread
safe_to_excel_thread = None
    
# Funktion, um den SafeToExcelThread zu starten
def run_safe_to_excel_skript():
    global safe_to_excel_thread

    # Beenden Sie den SafeToExcelThread, falls er bereits l?uft
    if safe_to_excel_thread is not None:
        safe_to_excel_thread.quit()
        safe_to_excel_thread.wait()

    # Erstellen und starten Sie den neuen SafeToExcelThread
    safe_to_excel_thread = SafeToExcelThread()
    safe_to_excel_thread.completed.connect(on_safe_to_excel_completed)
    safe_to_excel_thread.start()

# Funktion, die aufgerufen wird, wenn der SafeToExcelThread abgeschlossen ist
def on_safe_to_excel_completed():
    print("Der Vorgang 'safe_to_excel' wurde abgeschlossen")
    

async def pruefe_dateiname(Dateiname):

   
    
    if Dateiname == 0:
        safe_to_excel.start_threads()
        

    else:
        Start.setEnabled(False)
        Stopp.setEnabled(True)
        Plotter.setEnabled(True)
        Trainiere.setEnabled(True)
   

    await asyncio.sleep(30)  # 30 Sekunden warten

    from safe_to_excel import Dateiname
    print (Dateiname)
    if Dateiname != 0:
        print ("Datei angelegt")
        Start.setEnabled(False)
        Stopp.setEnabled(True)
        Plotter.setEnabled(True)
        Trainiere.setEnabled(True)
    
       




    else:
        print("Gerät nicht gefunden")
        Start.setEnabled(True)


  # Event-Schleife erstellen
loop = asyncio.get_event_loop()    

def Start_clicked():

    Start.setEnabled(False)
    print("Start Button wurde gedr?ckt")
    from safe_to_excel import Dateiname

    global pruefe_dateiname_thread
    pruefe_dateiname_thread = None


    # Beenden Sie den SafeToExcelThread, falls er bereits l?uft
    if pruefe_dateiname_thread is not None:
       pruefe_dateiname_thread.quit()
       pruefe_dateiname_thread.wait()

    # Erstellen und starten Sie den neuen SafeToExcelThread
    pruefe_dateiname_thread = PruefeDateinameThread(Dateiname)
    pruefe_dateiname_thread.start()


    # Funktion in der Event-Schleife ausf?hren
   # loop.run_until_complete(pruefe_dateiname(Dateiname))
     # asyncio.create_task(pruefe_dateiname(Dateiname)) 

 
def Rohdaten_clicked():
    rohdaten_window.show()








    
from safe_to_excel import df
'''

class PlotterWindow(QMainWindow):
    def __init__(self, df):
        from safe_to_excel import df

        super().__init__()
        self.ui = uic.loadUi("plotter_window.ui")
        self.graphWidget = self.ui.graphWidget 
        self.setCentralWidget(self.ui)
        spo2_list = df['Red'][:100].astype(float)
    

    def plot(self, spo2_list):
        self.graphWidget.plot(spo2_list.values)
        print("plotter gestartet df =")
        print (df)
'''




def printplot():
    print("Update gedrückt")





def Plotter_clicked():
    global plotter_window
    from safe_to_excel import df
    print (df)
    from plotter import PlotterWindow
    plotter_window = PlotterWindow(df)

    # Überprüfen, ob das Plotter-Fenster bereits erstellt wurde
    if plotter_window is None:
        # Erstellen Sie eine Instanz des Plotter-Fensters und übergeben Sie den df-Parameter
        plotter_window = PlotterWindow(df)

        plotter_window_ui = plotter_window.ui  # Erhalten Sie eine Referenz auf die UI des Plotter-Fensters

    plotter_window.plot(df)  # Aufruf der plot-Funktion, um den Graphen anzuzeigen

    plotter_window.show()  # Zeigen Sie das Plotter-Fenster an

def Plotter_aktualisieren():
    print("aktualisieren Plotter gedrückt")



# Funktion, die aufgerufen wird, wenn der Button "Einstellungen" gedr?ckt wird
def Einstellungen_clicked():
    print("Einstellungen Button gedr?ckt")
    einstellungen_window.show()
    

def Update_clicked():
    global current_worker
    # Setze die Textfarbe auf Schwarz, wenn das Einstellungen-Fenster ge?ffnet wird
    einstellungen_window_ui.Parameter_Update_Text.setStyleSheet("color: black;")

    if current_worker is not None:
        current_worker.quit()
        current_worker.wait()
    current_worker = Worker(einstellungen_window_ui.Parameter_Update_Text) # ?bergeben Sie das Label-Objekt
    current_worker.received.connect(einstellungen_window_ui.Parameter_Update_Text.setText)  # Verbinden Sie das Signal mit der Methode setText()
    current_worker.start()

actionScanner = ui.actionScanner

def actionScanner_clicked():
    print("Dateiname")

def updatethetable():
    print("starte update")
    from safe_to_excel import Dateiname

    Datei_pandas = pd.read_excel(Dateiname, engine='openpyxl')

    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(Datei_pandas.columns)
    table_view = rohdaten_window_ui.RohdatenTableView
    table_view.setModel(model)

    # F?ge die Datenzeilen hinzu
    for row in range(Datei_pandas.shape[0]):
        data_row = [QStandardItem(str(item)) for item in Datei_pandas.iloc[row]]
        model.appendRow(data_row)
       # Verkn?pfe den TableView mit dem Frame in der UI
        table_view = rohdaten_window_ui.RohdatenTableView
        table_view.setModel(model)


# Signal-Slot-Verbindungen
Start.clicked.connect(Start_clicked)                   
Plotter.clicked.connect(Plotter_clicked)
Einstellungen.triggered.connect(Einstellungen_clicked)
einstellungen_window_ui.Update.clicked.connect(Update_clicked) #Slot f?r Fenster Einstellungen Button Update  
Parameter_Update_Text = einstellungen_window_ui.Parameter_Update_Text # Verbindung zu dem Text- Label beim Updaten der Parameter im Fenster Einstellungen
Main_Connect_Text = ui.Main_Connect_Text # Verbindung zu dem Text- Label beim Updaten der Parameter im Fenster Einstellungen
actionScanner.triggered.connect(actionScanner_clicked)
actionRohdaten.triggered.connect(Rohdaten_clicked)
rohdaten_window_ui.updateTable.clicked.connect(updatethetable) 





# Erstellen Sie eine Instanz des QMainWindow
window = QMainWindow()
window.setCentralWidget(ui)

# Zeigen Sie das Hauptfenster an
window.show()

# Starten Sie die Ereignisschleife der Anwendung
sys.exit(app.exec())