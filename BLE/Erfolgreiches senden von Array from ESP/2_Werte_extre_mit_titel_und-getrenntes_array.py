
import asyncio
from bleak import BleakClient
import numpy               # Importieren Sie numpy für die Verarbeitung von Daten in Arrays


address = "CC:50:E3:9C:15:02"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)

        print("Model Number: {0}".format("".join(map(chr, model_number))))
        

async def handle_uuid1_notify(sender, data):
    spo2_value = numpy.frombuffer(data, dtype=numpy.uint32)
    print("Red: {0}".format(spo2_value))

async def handle_uuid2_notify(sender, data):
    ir_value = numpy.frombuffer(data, dtype=numpy.uint32)
    print("IR: {0}".format(ir_value))

async def read_data(address):
    UUID1 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"
    async with BleakClient(address) as client:
        await client.start_notify(UUID1, handle_uuid1_notify)
        await client.start_notify(UUID2, handle_uuid2_notify)
        while True:
            await asyncio.sleep(1)

async def main(address):
    await read_data(address)

asyncio.run(main(address))
