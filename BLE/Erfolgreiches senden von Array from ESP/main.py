import asyncio
from bleak import BleakClient

address = "CC:50:E3:9C:15:02"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


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
        await client.start_notify(SPO2_UUID, notification_handler)
        # Wait for notifications
        while True:
            await asyncio.sleep(1)

async def notification_handler(sender, data):
    spo2_value = int.from_bytes(data, byteorder='little')
    print("Red: {0}".format(spo2_value))




async def main(address):
    await read_spo2(address)

asyncio.run(main(address))

