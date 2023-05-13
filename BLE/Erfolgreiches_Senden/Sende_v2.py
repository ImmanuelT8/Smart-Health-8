import asyncio
import bleak
import struct

# Werte definieren
Variable1 = 60
Variable2 = "SAMPLEAVG_4"
Variable3 = "MODE_MULTILED"
Variable4 = "SAMPLERATE_200"
Variable5 = "PULSEWIDTH_411"
Variable6 = "ADCRANGE_16384"

# MAC address of the ESP32
mac_address = 'CC:50:E3:9C:15:02'  # Replace with the MAC address of your ESP32


UUID3 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def run():
    # Connect to the ESP32 device
    async with bleak.BleakClient(mac_address) as client:

        # String erstellen
        str_parameters = f"{Variable1},{Variable2},{Variable3},{Variable4},{Variable5},{Variable6}"


        # Byte-Array erstellen
        byte_array = str_parameters.encode('ascii')

        print("Sende Werte")
        # Array senden
        await client.write_gatt_char(UUID3, byte_array)


        # Receive data from ESP32 via BLE
        received = False  # Variable to indicate whether data has been received


        while not received:
            data = await client.read_gatt_char(UUID3)
            if data:
                value = data.decode('utf-8')
                print(f"{value}")
                received = True


asyncio.run(run())
