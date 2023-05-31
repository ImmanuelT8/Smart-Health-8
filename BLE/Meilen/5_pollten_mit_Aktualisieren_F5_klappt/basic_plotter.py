import sys
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow


uiclass, baseclass = pg.Qt.loadUiType("plotter_window.ui")

class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plot(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Hours
            [30, 32, 34, 32, 33, 31, 29, 32, 35, 45],  # Temperature
        )

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)

plotter_window = QMainWindow()

app = pg.Qt.QtGui.QApplication([])
window = MainWindow()
window.show()
pg.Qt.QtGui.QApplication.instance().exec_()
