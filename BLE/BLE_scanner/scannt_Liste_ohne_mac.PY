import tkinter as tk
from bleak import BleakScanner
import asyncio

async def show_devices(device_listbox=None):
    device_list = await BleakScanner.discover()
    device_names = [str(d.name) for d in device_list]
    if device_listbox is not None:
        device_listbox.delete(0, tk.END)
        for i, name in enumerate(device_names):
            device_listbox.insert(i, name)

def update_list(device_names):
    print(device_names)

root = tk.Tk()
root.geometry("300x300")

device_listbox = tk.Listbox(root)
device_listbox.pack()

devices_button = tk.Button(root, text="Show Devices", command=lambda: asyncio.run(show_devices(device_listbox)))
devices_button.pack(pady=50)

root.mainloop()
