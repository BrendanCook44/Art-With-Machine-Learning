import sys
from PyQt5.QtWidgets import QApplication,  QWidget,  QLabel, QMainWindow, QPushButton, QAction
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

class Win2(QMainWindow):
    def __init__(self):
        super(Win2, self).__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QVBoxLayout(central_widget)
        self.DescLabel = QLabel("Win2")
        lay.addWidget(self.DescLabel)