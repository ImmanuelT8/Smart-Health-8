# -*- coding: latin-1 -*-

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from connect_to_esp import ESPConnectThread
from pulse_live_window import PulseWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("main_window.ui", self)
        
        # Zugriff auf den Button und andere Elemente
        self.start_button = self.ui.Start
        self.stop_button = self.ui.Stopp 
        self.plotter_button = self.ui.Plotter
        self.training_button = self.ui.Trainiere

        #Zugriff auf drop down Menüpunkte 
        self.action_pulse_live = self.ui.actionPulse_live
        
        # Verbindung des Buttons mit der Funktion
        self.start_button.clicked.connect(self.start_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)
        self.action_pulse_live.triggered.connect(self.pulse_live_clicked)
        
        # Initialisiere das Pulse Live-Fenster
        self.pulse_live_window = None

    def start_clicked(self):
        print("Start button clicked")
        self.start_button.setEnabled(False)

        address = "CC:50:E3:9C:15:02"  # Hier die MAC-Adresse des ESP32 einsetzen
        self.thread = ESPConnectThread(address)
        self.thread.connected.connect(self.on_connected)
        self.thread.connection_failed.connect(self.on_connection_failed)
        self.thread.disconnection.connect(self.on_disconnected)
        self.thread.start()

    def stop_clicked(self):
        print("Stop button clicked")        
        self.thread.disconnect()

    def on_connected(self, success):
        if success:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.plotter_button.setEnabled(True)
            self.training_button.setEnabled(True)
        else:
            print("Connection to device failed")
            self.start_button.setEnabled(True)

    def on_connection_failed(self):
        self.start_button.setEnabled(True)

    def on_disconnected(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.plotter_button.setEnabled(False)
        self.training_button.setEnabled(False)

    def pulse_live_clicked(self):
        print("pulse live clicked")
        
        # Überprüfen, ob das Pulse Live-Fenster bereits erstellt wurde
        if not self.pulse_live_window:
            # Erstelle das Pulse Live-Fenster
            self.pulse_live_window = PulseWindow()
            self.pulse_live_window.show()
            # Verbinde das Schließen des Pulse Live-Fensters mit der Löschung der Instanzvariable
            self.pulse_live_window.closed.connect(self.clear_pulse_live_window)


    def pulse_live_clicked(self):
            print("pulse live clicked")
        
            if not self.pulse_live_window:
                self.pulse_live_window = PulseWindow()
                self.pulse_live_window.show()
                self.pulse_live_window.closed.connect(self.clear_pulse_live_window)

            # Aktualisieren Sie den Thread mit der neuen pulse_live_window-Instanz
            if self.thread:
                self.thread.pulse_live_window = self.pulse_live_window



    def clear_pulse_live_window(self):
        # Lösche das Pulse Live-Fenster, wenn es geschlossen wird
        self.pulse_live_window = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
