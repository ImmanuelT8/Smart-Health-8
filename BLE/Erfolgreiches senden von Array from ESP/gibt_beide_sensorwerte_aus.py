import asyncio              # Importieren Sie asyncio für asynchrone Programmierung
from bleak import BleakClient    # Importieren Sie BleakClient, um eine Verbindung mit Bluetooth LE-Geräten herzustellen
import numpy               # Importieren Sie numpy für die Verarbeitung von Daten in Arrays


address = "CC:50:E3:9C:15:02"    # Geben Sie die Adresse des BLE-Geräts an, das Sie verbinden möchten
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"    # Geben Sie die UUID für die erste Charakteristik an
MODEL_NBR_UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"    # Geben Sie die UUID für die zweite Charakteristik an


# Definieren Sie die Funktion "read_data", um Daten von beiden Charakteristiken zu lesen.

async def read_data(address):
    async with BleakClient(address) as client:   # Verbinde dich mit dem BLE-Gerät
        # Abonniere beide Charakteristiken, um über Änderungen benachrichtigt zu werden
        await client.start_notify("beb5483e-36e1-4688-b7f5-ea07361b26a8", notification_handler)
        await client.start_notify("beb5483e-36e1-4688-b7f5-ea07361b26a9", notification_handler)
        # Warte auf Daten, die über die Charakteristiken gesendet werden
        while True:
            await asyncio.sleep(1)


# Definieren Sie die Funktion "notification_handler", um Benachrichtigungen über Datenänderungen in den Charakteristiken zu erhalten

async def notification_handler(sender, data):
    # Daten in numpy-Array umwandeln
    values = numpy.frombuffer(data, dtype=numpy.uint32)
    if sender == "beb5483e-36e1-4688-b7f5-ea07361b26a8":
        print("SPO2 Werte:")   # Wenn die Daten aus der ersten Charakteristik stammen, drucke "SPO2 Werte:"
        print(values)          # Gib die Daten aus der ersten Charakteristik aus
    elif sender == "beb5483e-36e1-4688-b7f5-ea07361b26a9":
        print("IR Werte:")     # Wenn die Daten aus der zweiten Charakteristik stammen, drucke "IR Werte:"
        print(values)          # Gib die Daten aus der zweiten Charakteristik aus


# Definieren Sie die Hauptfunktion "main", um das Lesen von Daten und die Verarbeitung von Benachrichtigungen zu initiieren

async def main(address):
    await read_data(address)

# Führen Sie die Hauptfunktion "main" aus, um das BLE-Gerät zu verbinden und Daten zu lesen.

asyncio.run(main(address))
