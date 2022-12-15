from typing_extensions import Self
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import ImageResourceFile
import numpy as np
import subprocess
import time
import cv2
import sys

DURATION_INT = 20

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        self.cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class Thread2(QThread):
    timer_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.timer = QTimer()
        self.timer.start(20000)
        
    def run(self):
        print("Hello World")
        self.timer.timeout.connect(self.timer_finished)

    def stop(self):
        print("World Hello")
        self._run_flag = False
        self.wait()

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.time_left_int = DURATION_INT
        self.widget_counter_int = 0

        self.setWindowTitle("Qt live label demo")
        self.disply_width = 1920
        self.display_height = 1080
        
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(64)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image_label.resize(self.disply_width, self.display_height)

        self.textLabel = QLabel('Smile! Your Picture will be taken in: ')
        self.textLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.textLabel.setFont(font)
        self.textLabel.setMaximumHeight(100)
        
        self.time_passed_qll = QtWidgets.QLabel()
        self.time_passed_qll.setFont(font)
        self.time_passed_qll.setMaximumHeight(100)

        vbox = QVBoxLayout()
        container = QWidget()
        container.setStyleSheet("background-color: #FFD200;")

        hbox = QHBoxLayout(container)
        hbox.addWidget(self.textLabel)
        hbox.addWidget(self.time_passed_qll)
        vbox.addWidget(self.image_label)
        
        vbox.addWidget(container)

        self.setLayout(vbox)

        self.setStyleSheet("background-color: #003E7E;")

        self.showFullScreen()

        self.thread = VideoThread()

        self.thread.change_pixmap_signal.connect(self.update_image)

        self.thread.start()
            
        self.thread2 = Thread2()
        self.currentWindow = 1
        self.thread2.timer_finished.connect(self.capturePicture)
        self.thread2.start()

        self.timer_start()
        self.update_gui()

    def timer_start(self):
        self.time_left_int = DURATION_INT

        self.my_qtimer = QtCore.QTimer(self)
        self.my_qtimer.timeout.connect(self.timer_timeout)
        self.my_qtimer.start(1000)

        self.update_gui()

    def timer_timeout(self):
        self.time_left_int -= 1

        if self.time_left_int == 0:
            self.widget_counter_int = (self.widget_counter_int + 1) % 4
            self.time_left_int = DURATION_INT

        self.update_gui()

    def update_gui(self):
        self.time_passed_qll.setText(str(self.time_left_int))

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        self.time_passed_qll.setText(str(self.time_left_int))
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(1280, 720)
        return QPixmap.fromImage(p)
    
    def capturePicture(self):

        Window.stylizedWin1 = Window()
        Ui_StyleWindowOne.ui1 = Ui_StyleWindowOne()
        Ui_StyleWindowOne.ui1.setupUi(Window.stylizedWin1)

        Window.stylizedWin2 = Window()
        Ui_StyleWindowTwo.ui2 = Ui_StyleWindowTwo()
        Ui_StyleWindowTwo.ui2.setupUi(Window.stylizedWin2)

        if self.currentWindow == 1:
            ret,frame = self.thread.cap.read()
            cv2.imwrite('images/Camera Photo/Input Picture.jpg',frame)

            subprocess.Popen(
                'python "Program Actions/evaluate.py" \
                --checkpoint "Checkpoints/wave.ckpt" \
                --in-path "Images/Camera Photo/Input Picture.jpg" \
                --out-path "Images/Stylized Pictures/Stylized Great Wave.jpg"')

            subprocess.Popen(
                'python "Program Actions/evaluate.py" \
                --checkpoint "Checkpoints/la_muse.ckpt" \
                --in-path "Images/Camera Photo/Input Picture.jpg" \
                --out-path "Images/Stylized Pictures/Stylized La Muse.jpg"')

            subprocess.Popen(
                'python "Program Actions/evaluate.py" \
                --checkpoint "Checkpoints/rain_princess.ckpt" \
                --in-path "Images/Camera Photo/Input Picture.jpg" \
                --out-path "Images/Stylized Pictures/Stylized Rain Princess.jpg"')

            subprocess.Popen(
                'python "Program Actions/evaluate.py" \
                --checkpoint "Checkpoints/scream.ckpt" \
                --in-path "Images/Camera Photo/Input Picture.jpg" \
                --out-path "Images/Stylized Pictures/Stylized Scream.jpg"')

            subprocess.Popen(
                'python "Program Actions/evaluate.py" \
                --checkpoint "Checkpoints/udnie.ckpt" \
                --in-path "Images/Camera Photo/Input Picture.jpg" \
                --out-path "Images/Stylized Pictures/Stylized Udnie.jpg"')

            subprocess.Popen(
                'python "Program Actions/evaluate.py" \
                --checkpoint "Checkpoints/wreck.ckpt" \
                --in-path "Images/Camera Photo/Input Picture.jpg" \
                --out-path "Images/Stylized Pictures/Stylized Wreck.jpg"')

        App.changeWindow(self)
    
    def changeWindow(self):
        
        if self.currentWindow == 1:
            creditsWin.showFullScreen()
            self.currentWindow = 2

        elif self.currentWindow == 2:
            Window.stylizedWin1.showFullScreen()
            creditsWin.showMinimized()
            self.currentWindow = 3

        elif self.currentWindow == 3:
            Window.stylizedWin2.showFullScreen()
            Window.stylizedWin1.showMinimized()
            self.currentWindow = 4

        elif self.currentWindow == 4:
            a.showFullScreen()
            Window.stylizedWin2.showMinimized()
            self.currentWindow = 1

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

class Ui_StyleWindowOne(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setMinimumSize(QtCore.QSize(1920, 1080))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ArtWithMachineLearningLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(36)
        self.ArtWithMachineLearningLabel.setFont(font)
        self.ArtWithMachineLearningLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ArtWithMachineLearningLabel.setObjectName("ArtWithMachineLearningLabel")
        self.verticalLayout_2.addWidget(self.ArtWithMachineLearningLabel)
        self.OriginalStyleLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(36)
        self.OriginalStyleLabel.setFont(font)
        self.OriginalStyleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OriginalStyleLabel.setObjectName("OriginalStyleLabel")
        self.verticalLayout_2.addWidget(self.OriginalStyleLabel)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMinimumSize(QtCore.QSize(426, 0))
        self.label_3.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.LaMuseLabel = QtWidgets.QLabel(self.centralwidget)
        self.LaMuseLabel.setMinimumSize(QtCore.QSize(426, 0))
        self.LaMuseLabel.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(24)
        self.LaMuseLabel.setFont(font)
        self.LaMuseLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LaMuseLabel.setObjectName("LaMuseLabel")
        self.horizontalLayout_4.addWidget(self.LaMuseLabel)
        self.RainPrincessLabel = QtWidgets.QLabel(self.centralwidget)
        self.RainPrincessLabel.setMinimumSize(QtCore.QSize(426, 0))
        self.RainPrincessLabel.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(24)
        self.RainPrincessLabel.setFont(font)
        self.RainPrincessLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RainPrincessLabel.setObjectName("RainPrincessLabel")
        self.horizontalLayout_4.addWidget(self.RainPrincessLabel)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(426, 0))
        self.label.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView_Scream_Stylized_16 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_16.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_16.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_16.setStyleSheet("border-image: url(:/Logo/Logos/index.png);")
        self.graphicsView_Scream_Stylized_16.setObjectName("graphicsView_Scream_Stylized_16")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_16)
        self.graphicsView_Scream_Stylized_18 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_18.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_18.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_18.setStyleSheet("Border-image: url(:/Resized/Resized Pictures/La Muse - Resized.jpg)")
        self.graphicsView_Scream_Stylized_18.setObjectName("graphicsView_Scream_Stylized_18")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_18)
        self.graphicsView_Scream_Stylized_15 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_15.setMinimumSize(QtCore.QSize(384, 216))
        self.graphicsView_Scream_Stylized_15.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_15.setStyleSheet("Border-image: url(:/Resized/Resized Pictures/Rain Princess - Resized.jpg)")
        self.graphicsView_Scream_Stylized_15.setObjectName("graphicsView_Scream_Stylized_15")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_15)
        self.graphicsView_Scream_Stylized_20 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_20.setMinimumSize(QtCore.QSize(384, 216))
        self.graphicsView_Scream_Stylized_20.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_20.setStyleSheet("border-image: url(:/Resized/Resized Pictures/Scream - Resized.jpg);")
        self.graphicsView_Scream_Stylized_20.setObjectName("graphicsView_Scream_Stylized_20")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_20)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.YourStylizedResultsLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(36)
        self.YourStylizedResultsLabel.setFont(font)
        self.YourStylizedResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.YourStylizedResultsLabel.setObjectName("YourStylizedResultsLabel")
        self.verticalLayout.addWidget(self.YourStylizedResultsLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView_Scream_Stylized_13 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_13.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_13.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_13.setStyleSheet("border-image: url(Images/Camera Photo/Input Picture.jpg);")
        self.graphicsView_Scream_Stylized_13.setObjectName("graphicsView_Scream_Stylized_13")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_13)
        self.graphicsView_Scream_Stylized_19 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_19.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_19.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_19.setStyleSheet("border-image: url(Images/Stylized Pictures/Stylized La Muse.jpg);")
        self.graphicsView_Scream_Stylized_19.setObjectName("graphicsView_Scream_Stylized_19")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_19)
        self.graphicsView_Scream_Stylized_17 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_17.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_17.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_17.setStyleSheet("border-image: url(Images/Stylized Pictures/Stylized Rain Princess.jpg);")
        self.graphicsView_Scream_Stylized_17.setObjectName("graphicsView_Scream_Stylized_17")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_17)
        self.graphicsView_Scream_Stylized_14 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_14.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_14.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_14.setStyleSheet("border-image: url(Images/Stylized Pictures/Stylized Scream.jpg);")
        self.graphicsView_Scream_Stylized_14.setObjectName("graphicsView_Scream_Stylized_14")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_14)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ArtWithMachineLearningLabel.setText(_translate("MainWindow", "Art With Machine Learning"))
        self.OriginalStyleLabel.setText(_translate("MainWindow", "Original Styles"))
        self.label_3.setText(_translate("MainWindow", "<html><center>Your Next Three Results Will Be<br> Ready In 20 Seconds</cenmter></html>"))
        self.LaMuseLabel.setText(_translate("MainWindow", "Picasso\'s\n"
"La Muse"))
        self.RainPrincessLabel.setText(_translate("MainWindow", "Leonid Afremov\'s\n"
"Rain Princess"))
        self.label.setText(_translate("MainWindow", "Edvard Munch\'s\n"
"The Scream"))
        self.YourStylizedResultsLabel.setText(_translate("MainWindow", "Your Stylized Results!"))

class Ui_StyleWindowTwo(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setMinimumSize(QtCore.QSize(1920, 1080))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ArtWithMachineLearningLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(36)
        self.ArtWithMachineLearningLabel.setFont(font)
        self.ArtWithMachineLearningLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ArtWithMachineLearningLabel.setObjectName("ArtWithMachineLearningLabel")
        self.verticalLayout_2.addWidget(self.ArtWithMachineLearningLabel)
        self.OriginalStyleLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(36)
        self.OriginalStyleLabel.setFont(font)
        self.OriginalStyleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OriginalStyleLabel.setObjectName("OriginalStyleLabel")
        self.verticalLayout_2.addWidget(self.OriginalStyleLabel)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMinimumSize(QtCore.QSize(426, 0))
        self.label_3.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.LaMuseLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LaMuseLabel.sizePolicy().hasHeightForWidth())
        self.LaMuseLabel.setSizePolicy(sizePolicy)
        self.LaMuseLabel.setMinimumSize(QtCore.QSize(426, 0))
        self.LaMuseLabel.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(24)
        self.LaMuseLabel.setFont(font)
        self.LaMuseLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LaMuseLabel.setObjectName("LaMuseLabel")
        self.horizontalLayout_4.addWidget(self.LaMuseLabel)
        self.RainPrincessLabel = QtWidgets.QLabel(self.centralwidget)
        self.RainPrincessLabel.setMinimumSize(QtCore.QSize(426, 0))
        self.RainPrincessLabel.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(24)
        self.RainPrincessLabel.setFont(font)
        self.RainPrincessLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RainPrincessLabel.setObjectName("RainPrincessLabel")
        self.horizontalLayout_4.addWidget(self.RainPrincessLabel)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(426, 0))
        self.label.setMaximumSize(QtCore.QSize(426, 16777215))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView_Scream_Stylized_16 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_16.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_16.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_16.setStyleSheet("border-image: url(:/Logo/Logos/College of Engineering Logo.png);")
        self.graphicsView_Scream_Stylized_16.setObjectName("graphicsView_Scream_Stylized_16")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_16)
        self.graphicsView_Scream_Stylized_18 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_18.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_18.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_18.setStyleSheet("border-image: url(:/Original/Original Pictures/Shipwreck_turner.jpg);")
        self.graphicsView_Scream_Stylized_18.setObjectName("graphicsView_Scream_Stylized_18")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_18)
        self.graphicsView_Scream_Stylized_15 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_15.setMinimumSize(QtCore.QSize(384, 216))
        self.graphicsView_Scream_Stylized_15.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_15.setStyleSheet("border-image: url(:/Original/Original Pictures/Udnie.jpg);")
        self.graphicsView_Scream_Stylized_15.setObjectName("graphicsView_Scream_Stylized_15")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_15)
        self.graphicsView_Scream_Stylized_20 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_20.setMinimumSize(QtCore.QSize(384, 216))
        self.graphicsView_Scream_Stylized_20.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_20.setStyleSheet("border-image: url(:/Original/Original Pictures/Great Wave - Original.jpg);")
        self.graphicsView_Scream_Stylized_20.setObjectName("graphicsView_Scream_Stylized_20")
        self.horizontalLayout.addWidget(self.graphicsView_Scream_Stylized_20)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.YourStylizedResultsLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(36)
        self.YourStylizedResultsLabel.setFont(font)
        self.YourStylizedResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.YourStylizedResultsLabel.setObjectName("YourStylizedResultsLabel")
        self.verticalLayout.addWidget(self.YourStylizedResultsLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView_Scream_Stylized_13 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_13.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_13.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_13.setStyleSheet("border-image: url(Images/Camera Photo/Input Picture.jpg);")
        self.graphicsView_Scream_Stylized_13.setObjectName("graphicsView_Scream_Stylized_13")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_13)
        self.graphicsView_Scream_Stylized_19 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_19.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_19.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_19.setStyleSheet("border-image: url(Images/Stylized Pictures/Stylized Wreck.jpg);")
        self.graphicsView_Scream_Stylized_19.setObjectName("graphicsView_Scream_Stylized_19")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_19)
        self.graphicsView_Scream_Stylized_17 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_17.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_17.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_17.setStyleSheet("border-image: url(Images/Stylized Pictures/Stylized Udnie.jpg);")
        self.graphicsView_Scream_Stylized_17.setObjectName("graphicsView_Scream_Stylized_17")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_17)
        self.graphicsView_Scream_Stylized_14 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Scream_Stylized_14.setMinimumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_14.setMaximumSize(QtCore.QSize(426, 240))
        self.graphicsView_Scream_Stylized_14.setStyleSheet("border-image: url(Images/Stylized Pictures/Stylized Great Wave.jpg);")
        self.graphicsView_Scream_Stylized_14.setObjectName("graphicsView_Scream_Stylized_14")
        self.horizontalLayout_2.addWidget(self.graphicsView_Scream_Stylized_14)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ArtWithMachineLearningLabel.setText(_translate("MainWindow", "Art With Machine Learning"))
        self.OriginalStyleLabel.setText(_translate("MainWindow", "Original Styles"))
        self.label_3.setText(_translate("MainWindow", "<html><center>The Camera Window Will<br>Open In 20 Seconds</cenmter></html>"))
        self.LaMuseLabel.setText(_translate("MainWindow", "J. M. W. Turner\'s\n"
"The Shipwreck of The Minotaur"))
        self.RainPrincessLabel.setText(_translate("MainWindow", "Francis Picabia\'s\n"
"Udnie"))
        self.label.setText(_translate("MainWindow", "Hokusai\'s\n"
"Great Wave"))
        self.YourStylizedResultsLabel.setText(_translate("MainWindow", "Your Stylized Results!"))

class CreditsWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("GUI Layout/CreditsWindow.ui", self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    
    stylizedWin1 = Window()
    ui1 = Ui_StyleWindowOne()
    ui1.setupUi(stylizedWin1)
    
    stylizedWin2 = Window()
    ui2 = Ui_StyleWindowTwo()
    ui2.setupUi(stylizedWin2)
    
    creditsWin = CreditsWindow()
    
    a.show()
    sys.exit(app.exec_())
