import pandas as pd
import asyncio
import threading
from bleak import BleakClient
import numpy
from datetime import datetime
import logging
Dateiname = 0

# Konfiguration des Loggers
logging.basicConfig(filename='error.log', level=logging.ERROR)

first_run_file = True

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
            global df, first_run
            new_data_available = True

            if first_run:
                df = pd.DataFrame({'Red': spo2_list, 'IR': ir_list})
                df.to_excel(filename, index=False)
            elif new_data_available:
                new_data = pd.DataFrame({'Red': spo2_list, 'IR': ir_list})
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_excel(filename, index=False)

                global first_run_file
                global Dateiname
                if first_run_file:
                    print(filename)
                    Dateiname = filename
                    first_run_file = False

            spo2_list.clear()  # Die Liste leeren, um sie mit neuen Werten zu füllen
            ir_list.clear()

    async def read_data(self):
        UUID1 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
        UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"

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
                await asyncio.sleep(1)

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.read_data())


def start_threads():
    ble_thread = BLEThread(address)
    ble_thread.start()


if __name__ == '__main__':
    start_threads()

while first_run:
    first_run = False  # Flag auf False setzen, um den Code beim nächsten Durchlauf nicht erneut auszuführen