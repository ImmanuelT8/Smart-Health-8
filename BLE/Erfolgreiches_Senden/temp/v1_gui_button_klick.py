import asyncio
import bleak
import struct
import sys

from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QMenuBar, QMenu, QStatusBar, QComboBox, QWidget
from PyQt6.QtCore import Qt, QRect, QCoreApplication, QMetaObject
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
from pyqt6_tools.examples.exampleqmlitem import QtCore




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


# -*- coding: utf-8 -*-



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(547, 799)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setDockNestingEnabled(False)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionMAC_ndern = QAction(MainWindow)
        self.actionMAC_ndern.setObjectName(u"actionMAC_ndern")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(-20, 20, 601, 31))
        font = QFont()
        font.setFamilies([u"Segoe UI Variable"])
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(150, 110, 251, 41))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Light"])
        font1.setPointSize(16)
        self.textEdit.setFont(font1)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(150, 660, 241, 51))
        font2 = QFont()
        font2.setPointSize(16)
        self.pushButton.setFont(font2)
        self.textEdit_2 = QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(150, 200, 251, 41))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI Light"])
        font3.setPointSize(14)
        self.textEdit_2.setFont(font3)
        self.textEdit_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.textEdit_4 = QTextEdit(self.centralwidget)
        self.textEdit_4.setObjectName(u"textEdit_4")
        self.textEdit_4.setGeometry(QRect(150, 380, 251, 41))
        self.textEdit_4.setFont(font3)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(340, 720, 49, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(340, 160, 121, 16))
        font4 = QFont()
        font4.setPointSize(9)
        font4.setItalic(True)
        self.label_3.setFont(font4)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(290, 250, 191, 20))
        font5 = QFont()
        font5.setItalic(True)
        self.label_4.setFont(font5)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(250, 340, 261, 20))
        self.label_5.setFont(font5)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(260, 430, 201, 20))
        self.label_6.setFont(font5)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(250, 520, 211, 20))
        self.label_7.setFont(font5)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(150, 180, 161, 16))
        font6 = QFont()
        font6.setBold(False)
        font6.setUnderline(True)
        self.label_8.setFont(font6)
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(150, 270, 91, 16))
        self.label_9.setFont(font6)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(150, 360, 91, 16))
        font7 = QFont()
        font7.setBold(False)
        font7.setItalic(False)
        font7.setUnderline(True)
        self.label_10.setFont(font7)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(150, 450, 91, 16))
        self.label_11.setFont(font6)
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(150, 90, 91, 16))
        self.label_12.setFont(font6)
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(150, 540, 91, 16))
        self.label_13.setFont(font6)
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(250, 610, 211, 20))
        self.label_14.setFont(font5)
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(150, 470, 251, 41))
        self.comboBox.setFont(font3)
        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(150, 560, 251, 41))
        self.comboBox_2.setFont(font3)
        self.comboBox_3 = QComboBox(self.centralwidget)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(150, 290, 251, 41))
        self.comboBox_3.setFont(font3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 547, 22))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menuDatei.addAction(self.actionQuit)
        self.menuSetting.addAction(self.actionMAC_ndern)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionMAC_ndern.setText(QCoreApplication.translate("MainWindow", u"MAC \u00e4ndern", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"MAXIM 30102  BLE UPDATE ", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"50", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"senden", None))
        self.pushButton.clicked.connect(on_pushButton_click)
        self.textEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"SAMPLEAVG_4", None))
        self.textEdit_4.setPlaceholderText(QCoreApplication.translate("MainWindow", u"SAMPLERATE_100", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"0 - 50 mA", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"SAMPLEAVG_ (1-32)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Default: MODE_ MULTILED", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"SAMPLERATE_(50 - 400 Hz)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Default: PULSEWIDTH_411", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Probenmenge ", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Led Modus", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Abtastrate", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Pulsweite", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Led Helligkeit", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"ADC Bereich", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Default: ADCRANGE_16384", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"PULSEWIDTH_69", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"PULSEWIDTH_118", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"PULSEWIDTH_215", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"PULSEWIDTH_411", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"ADCRANGE_2048", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"ADCRANGE_4096", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"ADCRANGE_8192", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"ADCRANGE_16384", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"MODE_MULTILED", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("MainWindow", u"MODE_IR", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("MainWindow", u"MODE_RED", None))

        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
    # retranslateUi

def on_pushButton_click():
    print("Button wurde geklickt")



async def send_data():

    try:
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
    except Exception as e:
        print("Nicht verbunden")
        print(e)



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



app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())

app.exec()

asyncio.run(run())
