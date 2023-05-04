import tkinter as tk
from bleak import BleakScanner
import asyncio


async def discover_devices():
    devices = await BleakScanner.discover()
    devices_with_mac = [(str(d.name), d.address) for d in devices]
    return devices_with_mac


async def show_devices(device_listbox=None):
    devices_with_mac = await discover_devices()
    device_listbox.delete(0, tk.END)
    for i, (name, mac) in enumerate(devices_with_mac):
        device_listbox.insert(i, f"{name} ({mac})")


root = tk.Tk()
root.geometry("600x600")

devices_button = tk.Button(root, text="Show Devices", command=lambda: asyncio.run(show_devices(device_listbox)))
devices_button.pack(pady=50)


device_listbox = tk.Listbox(root, width=70)

device_listbox.pack()

root.mainloop()
