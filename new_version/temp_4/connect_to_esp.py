# -*- coding: latin-1 -*-
 
# esp_connect.py
 
from ast import Try
import asyncio
from PyQt6.QtCore import QThread, pyqtSignal
from bleak import BleakClient  # BLE Libary
import numpy
import os
import data_manager
 
class ESPConnectThread(QThread):
    connected = pyqtSignal(bool)  # Signal, das gesendet wird, wenn die Verbindung hergestellt ist
    connection_failed = pyqtSignal(bool)  # Signal, das gesendet wird, wenn die Verbindung fehlgeschlagen ist
    disconnection = pyqtSignal(bool)
 
    def __init__(self, address,  pulse_live_window=None):
        super().__init__()  # Ein Aufruf des Konstruktors der Basisklasse QThread und Zuweisung der Adresse des ESP32-Geräts zur Instanzvariablen address.
        self.address = address
        self.client = None  # Definition des client-Attributs
        self.exit_flag = None
        self._is_connected = False
        self.red_list = []
        self.ir_list = []
        self.folder_path = "data"
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        self.filename = None
        self.full_path = None
        self.pulse_live_window = pulse_live_window
 
 
    def run(self):  # Die run-Methode, die den Code enthält, der im Thread ausgeführt wird.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_to_esp())
        loop.close()
 
    async def handle_uuid1_notify(self, sender, data):
        print("UUID 1 notify")
        np_red_values = numpy.frombuffer(data, dtype=numpy.uint32)  # Daten werden in ein Numpy Array convertiert
        self.red_list.extend(np_red_values.tolist())
        await self.check_and_append_data()
 
    async def handle_uuid2_notify(self, sender, data):
        print("UUID 2 notify")
        np_ir_values = numpy.frombuffer(data, dtype=numpy.uint32)  # Daten werden in ein Numpy Array convertiert
        self.ir_list.extend(np_ir_values.tolist())
        await self.check_and_append_data()
 
    async def check_and_append_data(self):
        if data_manager.is_data_available(self.red_list, self.ir_list):
            if not self._is_connected:
                self._is_connected = True  # Setzen der internen Variable auf True
                self.connected.emit(True)  # Senden des pyqt Signals, dass die Verbindung besteht
                self.filename, self.full_path = data_manager.generate_timestamped_filename(self.folder_path)
 
            # Verwenden der ausgelagerten Funktion zum Erstellen oder Aktualisieren der Excel-Datei
            data_manager.create_or_update_excel_file(self.folder_path, self.filename, self.red_list, self.ir_list)
 
            # Daten an das Pulse Live-Fenster senden, wenn es existiert
            if self.pulse_live_window:
                self.pulse_live_window.add_data(self.ir_list)
             
 
            # Leeren der Listen nach dem Speichern der Daten
            self.red_list.clear()
            self.ir_list.clear()
 
    async def connect_to_esp(self):  # Methode zur Verbindungsherstellung mit dem ESP
        print("Connect to device ...")
        UUID1 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
        UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"
 
        try:
            async with BleakClient(self.address) as client:  # Verbindung mit dem ESP herstellen
                services = client.services
                for service in services:
                    characteristics = service.characteristics
                    for characteristic in characteristics:
                        if characteristic.uuid == UUID1:
                            await client.start_notify(characteristic.handle, self.handle_uuid1_notify)
                        elif characteristic.uuid == UUID2:
                            await client.start_notify(characteristic.handle, self.handle_uuid2_notify)
 
                while True:
                    if self.exit_flag:  # Überprüfen des Exit-Flags
                        break  # Schleife beenden, wenn das Exit-Flag gesetzt ist
 
                    if not client.is_connected:
                        print("Lost connection")
                        self._is_connected = False
                        self.disconnection.emit(True)  # Senden des Signals, dass die Verbindung getrennt ist
                        break
 
                    await asyncio.sleep(1)
 
        except Exception as e:
            print("Connection failed")
            self.connection_failed.emit(True)  # Sendet das pyqt Signal Verbindung gescheitert
            self._is_connected = False  # Setzt die Variable die prüft ob sich schon verbunden wurde auf false
 
    def disconnect(self):
        print("Device disconnected")
        self.exit_flag = True
        self.disconnection.emit(True)  # Sendet das Signal disconnection
