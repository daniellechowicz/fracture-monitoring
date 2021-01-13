from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic

from models import Video

import cv2
import numpy as np
import os
import sys
import time

class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() 

        # Import GUI XML layout
        self.ui = uic.loadUi("layout.ui", self)
        
        self.setWindowTitle("Fracture Monitoring") 

        # Setting the icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # Buttons' callbacks
        self.pushButton_1.clicked.connect(self.videoPathDialog)
        self.pushButton_3.clicked.connect(self.markPoints)
        self.pushButton_4.clicked.connect(self.reset)
        self.pushButton_5.clicked.connect(self.start)

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
            # Enable "Mark points" and "Reset" buttons
            self.pushButton_1.setEnabled(False)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)

    def importDataPath(self):
        pass

    def markPoints(self):
        self.video = Video(self.videoPath, "Initial frame")
        self.video.markPoints()
        self.p1, self.p2, self.p3, self.p4 = self.video.getPoints()

        # Disable "Mark points" button
        # Enable "Reset" and "Start" buttons
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)

        # Show a message box
        self.showMessageBox(text="Points have been saved",
            altText=None,
            dtlText="P1: {}\nP2: {}\nP3: {}\nP4: {}".format(self.p1, 
                                                            self.p2, 
                                                            self.p3, 
                                                            self.p4))
        
    def reset(self):
        # Disable "Mark points", "Reset", "Start" and "Stop" buttons
        # Enable "Import video path" button
        self.pushButton_1.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        
        # Clear video's path
        self.videoPath = ""

    def start(self):
        self.video.open()
        self.video.setPoints(self.p1, self.p2, self.p3, self.p4)
        while True:
            ret, frame = self.video.getFrame()
            if ret:
                cv2.imshow("f1", frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break
            else:
                break

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = UserInterface()
    mainWindow.show()
    sys.exit(app.exec_())