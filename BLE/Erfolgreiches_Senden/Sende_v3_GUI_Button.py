import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal as Signal

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


class Worker(QThread):
    completed = Signal()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def do_work():
            try:
                client = bleak.BleakClient(mac_address)
                await self.connect_client(client)  # Verbindung herstellen

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

                await self.disconnect_client(client)  # Verbindung trennen
            except Exception as e:
                print("Nicht verbunden")
                print(e)

            self.completed.emit()

        loop.run_until_complete(do_work())

    async def connect_client(self, client):
        await client.connect()

    async def disconnect_client(self, client):
        await client.disconnect()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(100, 100, 300, 50)
        self.setWindowTitle('QThread Demo')

        self.widget = QWidget()
        layout = QVBoxLayout()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        self.btn_start = QPushButton('Start', clicked=self.start)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_start)

        self.worker = Worker()
        self.worker.completed.connect(self.complete)

        self.show()

    def start(self):
        self.btn_start.setEnabled(False)
        self.worker.start()

    def complete(self):
        self.progress_bar.setValue(100)
        self.btn_start.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
