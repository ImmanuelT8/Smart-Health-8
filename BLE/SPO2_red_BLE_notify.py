import asyncio
from bleak import BleakClient

address = "CC:50:E3:9C:15:02"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

async def read_spo2(address):
    SPO2_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    async with BleakClient(address) as client:
        while True:  # run in an infinite loop
            spo2_data = await client.read_gatt_char(SPO2_UUID)
            spo2_value = int.from_bytes(spo2_data, byteorder='little')
            print("SPO2: {0}".format(spo2_value))
            await asyncio.sleep(1)  # wait for 1 second

async def main(address):
    await read_spo2(address)

asyncio.run(main(address))
