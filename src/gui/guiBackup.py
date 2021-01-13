from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic

from models import Video

import ctypes
import cv2
import numpy as np
import os
import sys
import time

# Define static strings containing root and filename.
# Change these strings to indicate where the videos are.
ROOT = "F:\\02 Work\\07 Babu\\PRF\\Videos\\PRF0.1"
FILENAME1 = "testVideo1.mp4"

class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() 

        # Import GUI XML layout
        self.ui = uic.loadUi("guiLight.ui", self)
        
        self.setWindowTitle("Fracture Monitoring") 

        # Setting the icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # To get mouse events, I need to set mouse tracking functionality to True
        self.setMouseTracking(True)

        # When "Import video path" button clicked, execute the following:
        # self.pushButton_1.clicked.connect(self.videoPathDialog)
        self.pushButton_1.clicked.connect(self.videoPathDialog)
        self.pushButton_2.clicked.connect(self.markPoints)
        self.pushButton_4.clicked.connect(self.reset)
        self.pushButton_5.clicked.connect(self.videoStart)

        # Disable "Import frames button" - one cannot upload frames if no path was given
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)

    # This applies for threads
    def videoStart(self):
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()

    def mousePressEvent(self, eventQMouseEvent):
        self.evt = eventQMouseEvent.button()
        # print(self.evt)
    
    def showMessageBox(self, text, altText=None, dtlText=None):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        msg.setWindowTitle("Fracture Monitoring")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setText(text)
        
        if altText is not None:
            msg.setInformativeText(altText)
        
        if dtlText is not None:
            msg.setDetailedText(dtlText)
        
        retval = msg.exec_()

    def videoPathDialog(self, dir=None):
        if dir is None:
            dir = "./"

        self.videoPath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import video path...", str(dir))

        if self.videoPath == "":
            ctypes.windll.user32.MessageBoxW(0, "Incorrect path was given - please try again", "Warning", 0)
        else:
            # Disable the button
            self.pushButton_1.setEnabled(False)
            self.pushButton_2.setEnabled(True)

    def markPoints(self):
        self.video = Video(self.videoPath, "Initial frame")
        self.video.markPoints()
        p1, p2, p3, p4 = self.video.getPoints()

        # Disable "Mark points" button
        # Enable "Reset" and "Start" buttons
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)

        # Show a message box
        self.showMessageBox(text="Points have been saved",
            altText=None,
            dtlText="P1: {}\nP2: {}\nP3: {}\nP4: {}".format(p1, p2, p3, p4))

    # This applies for threads                
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_3.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def getFrame(self):
        cap = cv2.VideoCapture(self.videoPath)
        ret, frame = cap.read()
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            p = convertToQtFormat.scaled(668, 348)#, QtCore.Qt.KeepAspectRatio)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(p))
            
            # Change buttons' states accordingly
            self.pushButton_2.setEnabled(False)
            self.pushButton_4.setEnabled(True)

    def reset(self):
        # Change buttons' states accordingly
        self.pushButton_1.setEnabled(True)
        self.pushButton_2.setEnabled(False)

        # Adjust labels
        self.label_2.clear()
        self.label_2.setText("Import frames again")
        
        # Clear video's path
        self.videoPath = ""


# This applies for threads
class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)

    def run(self):
        while True:
            frame = self.video.getFrame()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = UserInterface()
    mainWindow.show()
    sys.exit(app.exec_())