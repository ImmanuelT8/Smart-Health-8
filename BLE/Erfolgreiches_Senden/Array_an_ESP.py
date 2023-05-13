import asyncio
import bleak
import struct

# MAC address of the ESP32
mac_address = 'CC:50:E3:9C:15:02'  # Replace with the MAC address of your ESP32


UUID3 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def run():
    # Connect to the ESP32 device
    async with bleak.BleakClient(mac_address) as client:
        # Send parameter to ESP32

        parameter = 5
        int_parameter = int(parameter)
        await client.write_gatt_char(UUID3, int_parameter.to_bytes(4, byteorder='little'))


        # Receive data from ESP32 via   BLE


        while True:
            data = await client.read_gatt_char(UUID3)
            if data:
                value = int.from_bytes(data, byteorder='little')  # Convert bytes to integer
                print(f"Received data: {value}")


asyncio.run(run())

