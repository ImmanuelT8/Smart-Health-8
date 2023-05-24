# -*- coding: latin-1 -*-

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtGui
# Import der UpdateWindow-Klasse

# Erstellen Sie eine Instanz der QApplication
app = QApplication(sys.argv)

# Laden Sie die UI-Datei
ui_file = "qt1.ui"  # Geben Sie den Pfad zur UI-Datei an
ui = uic.loadUi(ui_file)

ui_file = "live_window.ui"  # Geben Sie den Pfad zur UI-Datei an


# Zugriff auf das QLabel-Objekt mit dem Objektnamen "logo"
logo_label = ui.logo

# Setzen des Pixmaps für das QLabel
logo_label.setPixmap(QtGui.QPixmap("logo.png"))

# Zugriff auf den Button mit dem Objektnamen "Start"
Start = ui.Start

# Zugriff auf den Button mit dem Objektnamen "Start"
Einstellungen = ui.Einstellungen

# Neues QMainWindow-Objekt für das Einstellungen-Fenster
einstellungen_window = QMainWindow()
einstellungen_window_ui = uic.loadUi(ui_file)
einstellungen_window.setCentralWidget(einstellungen_window_ui)



# Funktion, die aufgerufen wird, wenn der Button gedrückt wird
def Start_clicked():
    print("Start Button wurde gedrückt")


def open_new_window():
    new_window = QMainWindow()
    new_window_ui = uic.loadUi("live_window.ui")
    new_window.setCentralWidget(new_window_ui)
    new_window.show()


# Funktion, die aufgerufen wird, wenn der Button gedrückt wird
def Einstellungen_clicked():
    print("Einstellungen Button gedrückt")
    einstellungen_window.show()


# Signal-Slot-Verbindung für den Button
Start.clicked.connect(Start_clicked)

# Signal-Slot-Verbindung für den Button
Einstellungen.triggered.connect(Einstellungen_clicked)

# Erstellen Sie eine Instanz des QMainWindow
window = QMainWindow()
window.setCentralWidget(ui)

# Zeigen Sie das Hauptfenster an
window.show()

# Starten Sie die Ereignisschleife der Anwendung
app.exec()
