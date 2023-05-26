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


from datetime import datetime

table = PrettyTable()
table.field_names = ["Wert 1", "Wert 2"]

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")  # Variable mit Datum und Uhrzeit erzeugen

filename = f"{dt_string}.xlsx"  # Datei mit Name und Datum erzeugen

# Ein neues Sheet erstellen und es zum Writer hinzufügen
df = pd.DataFrame(columns=["Red", "IR"])

spo2_list = []
ir_list = []

first_run = True


#### Einstellunen für Updater und Basis ###

# Erstellen Sie eine Instanz der QApplication
app = QApplication(sys.argv)

# Laden Sie die UI-Datei
ui_file = "qt1.ui"  # Geben Sie den Pfad zur UI-Datei an
ui = uic.loadUi(ui_file)

# Zugriff auf das QLabel-Objekt mit dem Objektnamen "logo"
logo_label = ui.logo

# Setzen des Pixmaps für das QLabel
logo_label.setPixmap(QtGui.QPixmap("logo.png"))

# Zugriff auf den Button mit dem Objektnamen "Start" und andere
Start = ui.Start
Plotter = ui.Plotter
Einstellungen = ui.Einstellungen




# Neues QMainWindow-Objekt für das Einstellungen-Fenster
einstellungen_window = QMainWindow()
einstellungen_window_ui = uic.loadUi("einstellungen_window.ui")
einstellungen_window.setCentralWidget(einstellungen_window_ui)


# Neues QMainWindow-Objekt für das Plotter-Fenster
plotter_window = QMainWindow()
plotter_window_ui = uic.loadUi("plotter_window.ui")
plotter_window.setCentralWidget(plotter_window_ui)


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


### Einstellungen für Daten via Array empfangen ###

table = PrettyTable()
table.field_names = ["Wert 1", "Wert 2"]

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")  # Variable mit Datum und Uhrzeit erzeugen

filename = f"{dt_string}.xlsx"  # Datei mit Name und Datum erzeugen

# Ein neues Sheet erstellen und es zum Writer hinzufügen
df = pd.DataFrame(columns=["Red", "IR"])

spo2_list = []
ir_list = []

first_run = True


# Klasse für das Updaten des ESP
class Worker(QThread):
    completed = pyqtSignal()
    received = pyqtSignal(str)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def do_work():
            try:
                self.received.emit("Suche Gerät")  # Text "Suche Geräte" anzeigen
                print("Suche Gerät")
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

                # Daten vom ESP32 über BLE empfangen
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
                self.received.emit("Gerät nicht gefunden")
                einstellungen_window_ui.Parameter_Update_Text.setStyleSheet("color: red;")
                Parameter_Update_Text = "Gerät nicht gefunden"


            self.completed.emit()

        loop.run_until_complete(do_work())

    async def connect_client(self, client):
        await client.connect()

    async def disconnect_client(self, client):
        await client.disconnect()

"""
# Klasse für das Empfangen der ESP Daten als Array

class Worker_Daten_Array(QThread):
    completed = pyqtSignal()
    received = pyqtSignal(str)

    def __init__(self, address):
        super().__init__()
        self.address = address

    async def handle_uuid1_notify(self, sender, data):
        spo2_values = numpy.frombuffer(data, dtype=numpy.uint32)
        print("Red: {0}".format(spo2_values))

        for spo2_value in spo2_values:
            table.add_row([spo2_value, ""])
            spo2_list.append(spo2_value)

    async def handle_uuid2_notify(self, sender, data):
            ir_values = numpy.frombuffer(data, dtype=numpy.uint32)
            print("IR: {0}".format(ir_values))
            for ir_value in ir_values:
            
                if ir_value:
                    table.add_row(["", ir_value])
                    ir_list.append(ir_value)

                if len(spo2_list) == 100 and len(ir_list) == 100:
                    global df, first_run

                    new_data_available = True

                    if first_run:
                        df = pd.DataFrame({'Red': spo2_list, 'IR': ir_list})
                        df.to_excel(filename, index=False)
                    else:
                        new_data = pd.DataFrame({'Red': spo2_list, 'IR': ir_list})
                        df = pd.concat([df, new_data], ignore_index=True)
                        df.to_excel(filename, index=False)

                        print(df.head())

                    spo2_list.clear()
                    ir_list.clear()
    async def read_data(self):
                    UUID1 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
                    UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"
                    print("read data start")

                    async with BleakClient(self.address) as client:
                        print ("asnc bleak läuft")
                        services = await client.get_services()
                        for service in services:
                            characteristics = service.characteristics
                            for characteristic in characteristics:
                                if characteristic.uuid == UUID1:
                                    await client.start_notify(characteristic.handle, self.handle_uuid1_notify)
                                elif characteristic.uuid == UUID2:
                                    await client.start_notify(characteristic.handle, self.handle_uuid2_notify)
                        while True:
                            await asyncio.sleep(1)


    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

  

        async def do_work():

             try:

                def print_table():
                    print(table)

                self.received.emit("Suche Gerät")  # Text "Suche Geräte" anzeigen
                print("Suche Gerät")

               
                


                #def run_read_data(self):
                    #asyncio.run(read_data(self))

                # async def run_read_data(self):
                #    await read_data(self)


                client = bleak.BleakClient(mac_address)
                await self.connect_client(client)  # Verbindung herstellen
                print("vor read")
               # run_read_data(self)
                await self.read_data()


       

             except Exception as e:
                 Start.setEnabled(True)
                 print("Nicht verbunden")
                 Main_Connect_Text.setStyleSheet("color: red;")
                 self.received.emit("Gerät nicht gefunden")  # Text "Gerät nicht gefunden" anzeigen




        loop.run_until_complete(do_work())

    async def connect_client(self, client):
        print("connect client gestartet")
        await client.connect()

    async def disconnect_client(self, client):
        await client.disconnect()

"""   #Versuch die Funktion array safe to Excel im Hauptprogramm zu öffnen






def update_progress(progress_bar):
    current_value = progress_bar.value()
    if current_value < progress_bar.maximum():
        progress_bar.setValue(current_value + 1)
        # Fügen Sie hier Ihren eigenen Aktualisierungscode hinzu
        # z.B. Datenverarbeitung oder andere Aktionen
        # Hier wird der Wert des Fortschrittsbalkens um 1 erhöht
        # und der Aktualisierungsprozess kann fortgesetzt werden
        update_progress(progress_bar)  # Rufen Sie die Methode erneut auf, um den Fortschritt weiter zu aktualisieren

# Funktion, die aufgerufen wird, wenn der Button "Start" gedrückt wird
"""
def Start_clicked():
    print("Start Button wurde gedrückt")
    Start.setEnabled(False)
    # Setze die Textfarbe auf Schwarz, wenn das Einstellungen-Fenster geöffnet wird
    Main_Connect_Text.setStyleSheet("color: black;")

    global current_worker_data_array
    current_worker_data_array = Worker_Daten_Array(mac_address)
    current_worker_data_array.received.connect(Main_Connect_Text.setText)  # Verbinden Sie das Signal mit der Methode setText()
    current_worker_data_array.start()

"""  

# Definieren Sie die Funktion für den Button-Click-Event
def run_safe_to_excel_skript():
    # Hier können Sie Ihren Skriptaufruf einfügen
    subprocess.call(["python", "safe_to_excel.py"]) 
    

def Start_clicked():
    print("Start Button wurde gedrückt")
    run_safe_to_excel_skript()




def Plotter_clicked():
    print("Plotter Button wurde gedrückt")
    plotter_window.show()


# Funktion, die aufgerufen wird, wenn der Button "Einstellungen" gedrückt wird
def Einstellungen_clicked():
    print("Einstellungen Button gedrückt")
    einstellungen_window.show()
    


def Update_clicked():
    global current_worker
    # Setze die Textfarbe auf Schwarz, wenn das Einstellungen-Fenster geöffnet wird
    einstellungen_window_ui.Parameter_Update_Text.setStyleSheet("color: black;")

    if current_worker is not None:
        current_worker.quit()
        current_worker.wait()
    current_worker = Worker(einstellungen_window_ui.Parameter_Update_Text) # Übergeben Sie das Label-Objekt
    current_worker.received.connect(einstellungen_window_ui.Parameter_Update_Text.setText)  # Verbinden Sie das Signal mit der Methode setText()
    current_worker.start()









# Signal-Slot-Verbindungen
Start.clicked.connect(Start_clicked)                   
Plotter.clicked.connect(Plotter_clicked)
Einstellungen.triggered.connect(Einstellungen_clicked)
einstellungen_window_ui.Update.clicked.connect(Update_clicked) #Slot für Fenster Einstellungen Button Update  
Parameter_Update_Text = einstellungen_window_ui.Parameter_Update_Text # Verbindung zu dem Text- Label beim Updaten der Parameter im Fenster Einstellungen
Main_Connect_Text = ui.Main_Connect_Text # Verbindung zu dem Text- Label beim Updaten der Parameter im Fenster Einstellungen




# Erstellen Sie eine Instanz des QMainWindow
window = QMainWindow()
window.setCentralWidget(ui)

# Zeigen Sie das Hauptfenster an
window.show()

# Starten Sie die Ereignisschleife der Anwendung
sys.exit(app.exec())

