import pandas as pd
import asyncio
import threading
from bleak import BleakClient
import numpy
from datetime import datetime
import logging

Dateiname = 0
ble_thread = None  # Globale Variable für den BLEThread
start_after_stopp = False

# Konfiguration des Loggers
logging.basicConfig(filename='error.log', level=logging.ERROR)

first_run_file = True
second_run_file = False

address = "CC:50:E3:9C:15:02"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")  # Variable mit Datum und Uhrzeit erzeugen
filename = f"{dt_string}.xlsx"  # Datei mit Name und Datum erzeugen

# Ein neues DataFrame erstellen
df = pd.DataFrame(columns=["Red", "IR"])

spo2_list = []
ir_list = []

first_run = True


class BLEThread(threading.Thread):
    exit_flag = False  # Klassenattribut exit_flag

    def __init__(self, address):
        threading.Thread.__init__(self)
        self.address = address
    async def handle_uuid1_notify(self, sender, data):
        spo2_values = numpy.frombuffer(data, dtype=numpy.uint32)
        for spo2_value in spo2_values:
            spo2_list.append(spo2_value)  # füge den empfangenen Wert der Liste hinzu

    async def handle_uuid2_notify(self, sender, data):
        ir_values = numpy.frombuffer(data, dtype=numpy.uint32)
        for ir_value in ir_values:
            if ir_value:
                ir_list.append(ir_value)  # füge den empfangenen Wert der Liste hinzu

        if len(spo2_list) == 100 and len(ir_list) == 100:
            global df, first_run, second_run, second_run_file, start_after_stopp
            new_data_available = True
            print("Start after stopp =", start_after_stopp)

            if first_run or start_after_stopp:
                df = pd.DataFrame({'Red': spo2_list, 'IR': ir_list})
                df.to_excel(filename, index=False)
                start_after_stopp = False
                first_run = False

            elif new_data_available:
                new_data = pd.DataFrame({'Red': spo2_list, 'IR': ir_list})
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_excel(filename, index=False)

                global first_run_file
                global Dateiname
                global second_run_file
                if first_run_file or second_run_file:
                    print("Im Loop first run file oder second run file")
                    print(filename)
                    Dateiname = filename
                    first_run_file = False

            spo2_list.clear()  # Die Liste leeren, um sie mit neuen Werten zu füllen
            ir_list.clear()

    async def read_data(self):
        UUID1 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
        UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"
        print ("...")


        async with BleakClient(self.address) as client:
            services = client.services
            for service in services:
                characteristics = service.characteristics

                logging.error('Ein Fehler ist aufgetreten: %s')

                for characteristic in characteristics:
                    if characteristic.uuid == UUID1:
                        await client.start_notify(characteristic.handle, self.handle_uuid1_notify)
                    elif characteristic.uuid == UUID2:
                        await client.start_notify(characteristic.handle, self.handle_uuid2_notify)
            while True:
                if self.exit_flag:  # Überprüfen des Exit-Flags
                    break  # Schleife beenden, wenn das Exit-Flag gesetzt ist
                await asyncio.sleep(1)

    def close(self):
        self.exit_flag = True
        print("Exit Flag auf True gesetzt in close")

    def restart(self):
        global start_after_stopp
        print("Start after Stopp auf True gesetzt in restart")
        start_after_stopp = True

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)  # Setzen des Event-Loops für den aktuellen Thread
        task = loop.create_task(self.read_data())  # Erstellen der Task für den asynchronen Code
        loop.run_until_complete(task)  # Ausführen der Task

        # Überprüfen des Exit-Flags, um die Schleife zu beenden
        if self.exit_flag:
            loop.close()  # Schließen des Event-Loops
            print("Exit Flag auf True innerhalb des BLE Threads. Beginne return")
            return


def start_threads():
    global ble_thread
    ble_thread = BLEThread(address)
    ble_thread.start()


def close_threads():
    global exit_flag
    exit_flag = True
    print("Exit Flag auf True gestellt")
    global ble_thread
    # Warten, bis die Threads beendet sind
    ble_thread.close()
    ble_thread.join()

def restart_ble_thread():
    global ble_thread
    ble_thread.close()  # Beenden Sie den aktuellen BLEThread
    ble_thread.join()   # Warten Sie, bis der Thread beendet ist
    ble_thread = BLEThread(address)  # Erstellen Sie einen neuen BLEThread
    ble_thread.start()  # Starten Sie den neuen Thread

def update_filename():
    global Dateiname
    global second_run
    dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    # Extrahiere den Dateinamen ohne die Dateierweiterung
    file_prefix = dt_string.split(".")[0]
    # Extrahiere die Dateierweiterung
    file_extension = "xlsx"  # Dateierweiterung für Excel-Dateien
    # Füge die Zahl zum Dateinamen hinzu
    filename = f"{file_prefix}.{file_extension}"
    Dateiname = filename
    ble_thread.restart()
    



if __name__ == '__main__':
    start_threads()
