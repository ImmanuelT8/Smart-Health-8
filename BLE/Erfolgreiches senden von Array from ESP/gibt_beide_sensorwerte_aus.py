import asyncio
from bleak import BleakClient
import numpy

address = "CC:50:E3:9C:15:02"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
MODEL_NBR_UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"


async def read_data(address):
    async with BleakClient(address) as client:
        # Abonniere beide Charakteristiken
        await client.start_notify("beb5483e-36e1-4688-b7f5-ea07361b26a8", notification_handler)
        await client.start_notify("beb5483e-36e1-4688-b7f5-ea07361b26a9", notification_handler)
        # Warte auf Daten
        while True:
            await asyncio.sleep(1)


async def notification_handler(sender, data):
    # Daten in numpy-Array umwandeln
    values = numpy.frombuffer(data, dtype=numpy.uint32)
    if sender == "beb5483e-36e1-4688-b7f5-ea07361b26a8":
        print("SPO2 Werte:")
        print(values)
    elif sender == "beb5483e-36e1-4688-b7f5-ea07361b26a9":
        print("IR Werte:")
        print(values)


async def main(address):
    await read_data(address)

asyncio.run(main(address))
