# -*- coding: latin-1 -*-
import sys
from PyQt6 import uic
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread, pyqtSignal
import asyncio
import bleak

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
Einstellungen = ui.Einstellungen

# Neues QMainWindow-Objekt für das Einstellungen-Fenster
einstellungen_window = QMainWindow()
einstellungen_window_ui = uic.loadUi("live_window.ui")
einstellungen_window.setCentralWidget(einstellungen_window_ui)

# Speichern Sie eine Referenz auf den aktuellen Worker-Thread
current_worker = None

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

# Klasse für das Updaten des ESP
class Worker(QThread):
    completed = pyqtSignal()
    received = pyqtSignal(str)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def do_work():
            try:
                client = bleak.BleakClient(mac_address)
                await self.connect_client(client)  # Verbindung herstellen

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

                await self.disconnect_client(client)  # Verbindung trennen
            except Exception as e:
                print("Nicht verbunden")
                print(e)
                self.received.emit("Gerät nicht gefunden")

            self.completed.emit()

        loop.run_until_complete(do_work())

    async def connect_client(self, client):
        await client.connect()

    async def disconnect_client(self, client):
        await client.disconnect()

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
def Start_clicked():
    print("Start Button wurde gedrückt")
    # Starten Sie den QThread
    worker = Worker()
    worker.start()

# Funktion, die aufgerufen wird, wenn der Button "Einstellungen" gedrückt wird
def Einstellungen_clicked():
    print("Einstellungen Button gedrückt")
    einstellungen_window.show()

    global current_worker
    if current_worker is not None:
        current_worker.quit()  # Beenden Sie den vorherigen Worker-Thread
        current_worker.wait()  # Warten Sie, bis der Worker-Thread beendet ist
    einstellungen_window.show()

def Update_clicked():
    global current_worker
    if current_worker is not None:
        current_worker.quit()  # Beenden Sie den vorherigen Worker-Thread
        current_worker.wait()  # Warten Sie, bis der Worker-Thread beendet ist

    current_worker = Worker()
    update_progress(einstellungen_window_ui.progressBar)  # Aktualisieren Sie den Fortschrittsbalken im Einstellungsfenster
    current_worker.start()

# Signal-Slot-Verbindung für den Button "Start"
Start.clicked.connect(Start_clicked)

# Signal-Slot-Verbindung für den Button "Einstellungen"
Einstellungen.triggered.connect(Einstellungen_clicked)

einstellungen_window_ui.Update.clicked.connect(Update_clicked)

# Erstellen Sie eine Instanz des QMainWindow
window = QMainWindow()
window.setCentralWidget(ui)

# Zeigen Sie das Hauptfenster an
window.show()

# Starten Sie die Ereignisschleife der Anwendung
sys.exit(app.exec())

