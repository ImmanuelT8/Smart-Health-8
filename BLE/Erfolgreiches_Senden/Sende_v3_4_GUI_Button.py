import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar, QLineEdit
from PyQt6.QtCore import QThread, pyqtSignal as Signal, QTimer

import asyncio
import bleak

# Werte definieren
Variable1 = 50
Variable2 = "SAMPLEAVG_4"
Variable3 = "MODE_MULTILED"
Variable4 = "SAMPLERATE_200"
Variable5 = "PULSEWIDTH_411"
Variable6 = "ADCRANGE_16384"

# MAC-Adresse des ESP32
mac_address = 'CC:50:E3:9C:15:02'  # Ersetzen Sie dies durch die MAC-Adresse Ihres ESP32
UUID3 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class Worker(QThread):
    completed = Signal()
    received = Signal(str)

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

                # Daten vom ESP32 über BLE empfangen
                received = False  # Variable, um anzuzeigen, ob Daten empfangen wurden

                while not received:
                    data = await client.read_gatt_char(UUID3)
                    if data:
                        value = data.decode('utf-8')
                        print(f"{value}")
                        received = True
                        self.received.emit(value)

                await self.disconnect_client(client)  # Verbindung trennen
            except Exception as e:
                print("Nicht verbunden")
                print(e)
                self.received.emit("Gerät nicht gefunden")

            self.completed.emit()

        loop.run_until_complete(do_work())

    async def connect_client(self, client):
        await client.connect()

    async def disconnect_client(self, client):
        await client.disconnect()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('AH SPO2 Updater')

        self.widget = QWidget()
        layout = QVBoxLayout()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.mac_input = QLineEdit()
        self.mac_input.setText(mac_address)
        self.uuid_input = QLineEdit()
        self.uuid_input.setText(UUID3)

        self.variable1_input = QLineEdit()
        self.variable1_input.setText(str(Variable1))
        self.variable2_input = QLineEdit()
        self.variable2_input.setText(Variable2)
        self.variable3_input = QLineEdit()
        self.variable3_input.setText(Variable3)
        self.variable4_input = QLineEdit()
        self.variable4_input.setText(Variable4)
        self.variable5_input = QLineEdit()
        self.variable5_input.setText(Variable5)
        self.variable6_input = QLineEdit()
        self.variable6_input.setText(Variable6)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        self.btn_start = QPushButton('Parameter updaten', clicked=self.start)

        self.status_label = QLabel()

        layout.addWidget(QLabel("MAC-Adresse:"))
        layout.addWidget(self.mac_input)
        layout.addWidget(QLabel("UUID:"))
        layout.addWidget(self.uuid_input)
        layout.addWidget(QLabel("Led Helligkeit:"))
        layout.addWidget(self.variable1_input)
        layout.addWidget(QLabel("Probenanzahl:"))
        layout.addWidget(self.variable2_input)
        layout.addWidget(QLabel("Led Modus:"))
        layout.addWidget(self.variable3_input)
        layout.addWidget(QLabel("Abtastrate:"))
        layout.addWidget(self.variable4_input)
        layout.addWidget(QLabel("Pulsweite:"))
        layout.addWidget(self.variable5_input)
        layout.addWidget(QLabel("ADC Bereich:"))
        layout.addWidget(self.variable6_input)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.status_label)

        self.worker = Worker()
        self.worker.completed.connect(self.complete)
        self.worker.received.connect(self.update_status)

        self.show()

    def start(self):
        global Variable1, Variable2, Variable3, Variable4, Variable5, Variable6, mac_address, UUID3

        Variable1 = int(self.variable1_input.text())
        Variable2 = self.variable2_input.text()
        Variable3 = self.variable3_input.text()
        Variable4 = self.variable4_input.text()
        Variable5 = self.variable5_input.text()
        Variable6 = self.variable6_input.text()
        mac_address = self.mac_input.text()
        UUID3 = self.uuid_input.text()

        self.btn_start.setEnabled(False)
        self.progress_bar.setValue(0)
        self.worker.start()
        self.start_progress_timer()  # Starten des Fortschritts-Timers

    def complete(self):
        self.progress_bar.setValue(100)
        self.btn_start.setEnabled(True)

    def start_progress_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_progress)
        timer.start(100)  # Intervall des Timers in Millisekunden

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 3)

    def update_status(self, value):
        self.status_label.setText(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
