import asyncio
from bleak import BleakClient
import numpy

address = "CC:50:E3:9C:15:02"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
MODEL_NBR_UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"


# async def read_spo2(address):
#    SPO2_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#    async with BleakClient(address) as client:
#        while True:  # run in an infinite loop
#           spo2_data = await client.read_gatt_char(SPO2_UUID)
#           print("SPO2: {0}".format(spo2_value))
#           await asyncio.sleep(1)  # wait for 1 second



async def read_spo2(address):
    SPO2_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    async with BleakClient(address) as client:
        await client.start_notify(SPO2_UUID, notification_handler_spo2)
        # Wait for notifications
        while True:
            await asyncio.sleep(1)

async def read_ir(address):
    IR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a9"
    async with BleakClient(address) as client:
        await client.start_notify(IR_UUID, notification_handler_ir)
        # Wait for notifications
        while True:
            await asyncio.sleep(1)




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


#async def notification_handler2(sender, data):

#    spo2_value = numpy.frombuffer(data, dtype=numpy.uint32)
#    print("Rot Werte:")
#    print(spo2_value)


# async def notification_handler(sender, datair):

#    ir_value = numpy.frombuffer(datair, dtype=numpy.uint32)
#    print("IR Wert:")
#    print(ir_value)


async def notification_handler_spo2(sender, data):
    spo2_value = numpy.frombuffer(data, dtype=numpy.uint32)
    print("SPO2 Werte:")
    print(spo2_value)

async def notification_handler_ir(sender, dataIR):
    ir_value = numpy.frombuffer(dataIR, dtype=numpy.uint32)
    print("IR Werte:")
    print(ir_value)


async def main(address):
    await read_data(address)

asyncio.run(main(address))
