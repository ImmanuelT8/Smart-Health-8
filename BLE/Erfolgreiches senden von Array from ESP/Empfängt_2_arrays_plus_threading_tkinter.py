import asyncio
import threading
from tkinter import *
from bleak import BleakClient
import numpy

address = "CC:50:E3:9C:15:02"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


class BLEThread(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.address = address

    async def handle_uuid1_notify(self, sender, data):
        spo2_value = numpy.frombuffer(data, dtype=numpy.uint32)
        print("Red: {0}".format(spo2_value))

    async def handle_uuid2_notify(self, sender, data):
        ir_value = numpy.frombuffer(data, dtype=numpy.uint32)
        print("IR: {0}".format(ir_value))

    async def read_data(self):
        UUID1 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
        UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a9"
        async with BleakClient(self.address) as client:
            await client.start_notify(UUID1, self.handle_uuid1_notify)
            await client.start_notify(UUID2, self.handle_uuid2_notify)
            while True:
                await asyncio.sleep(1)

    def run(self):
        asyncio.run(self.read_data())


class TkinterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        tkFenster = Tk()
        tkFenster.title('BLE MAX30102')
        tkFenster.mainloop()


def start_threads():
    ble_thread = BLEThread(address)
    tkinter_thread = TkinterThread()

    ble_thread.start()
    tkinter_thread.start()


if __name__ == '__main__':
    start_threads()
