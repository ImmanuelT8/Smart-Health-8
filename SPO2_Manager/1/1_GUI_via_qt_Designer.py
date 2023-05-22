# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6 import QtGui
from resources_rc import *

# Erstellen Sie eine Instanz der QApplication
app = QApplication([])

# Laden Sie die UI-Datei
ui_file = "qt1.ui"  # Geben Sie den Pfad zur UI-Datei an
ui = uic.loadUi(ui_file)

# Zugriff auf das QLabel-Objekt mit dem Objektnamen "logo"
logo_label = ui.logo

# Setzen des Pixmaps für das QLabel
logo_label.setPixmap(QtGui.QPixmap("logo.png"))

# Erstellen Sie eine Instanz des QMainWindow
window = QMainWindow()
window.setCentralWidget(ui)

# Zeigen Sie das Hauptfenster an
window.show()

# Starten Sie die Ereignisschleife der Anwendung
app.exec()
