from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic

from models import Video

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

        # Buttons' callbacks
        self.pushButton_1.clicked.connect(self.videoPathDialog)
        self.pushButton_3.clicked.connect(self.markPoints)
        self.pushButton_4.clicked.connect(self.reset)

        # Disable "Mark points", "Reset", "Start" and "Stop" buttons
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
    
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
            # Show a message box
            self.showMessageBox(text="Incorrect path was given - please try again")
        else:
            # Disable "Import video path" button
            # Enable "Mark points button"
            self.pushButton_1.setEnabled(False)
            self.pushButton_3.setEnabled(True)

    def importData(self):
        pass

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
        
    def reset(self):
        # Change buttons' states accordingly
        self.pushButton_1.setEnabled(True)
        self.pushButton_2.setEnabled(False)

        # Adjust labels
        self.label_2.clear()
        self.label_2.setText("Import frames again")
        
        # Clear video's path
        self.videoPath = ""

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = UserInterface()
    mainWindow.show()
    sys.exit(app.exec_())