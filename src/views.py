from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
from pyqtgraph import PlotWidget

from models import Data, Video

import cv2
import numpy as np
import os
import sys
import pyqtgraph as pg
import time

class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() 

        # Import GUI XML layout
        self.ui = uic.loadUi("layout — kopia.ui", self)
        
        self.setWindowTitle("Fracture Monitoring") 

        # Setting the icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # Buttons' callbacks
        self.pushButton_1.clicked.connect(self.videoPathDialog)
        self.pushButton_2.clicked.connect(self.importData)
        self.pushButton_3.clicked.connect(self.markPoints)
        self.pushButton_4.clicked.connect(self.reset)
        self.pushButton_5.clicked.connect(self.start)

        # Disable "Mark points", "Reset", "Start" and "Stop" buttons
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)

        # Adjust graphs
        self.setupGraphs()

    def setupGraphs(self):
        self.graphicsView_1.setBackground("w")
        self.graphicsView_1.setLabel("left", "<span style=\"color: black; font-size: 12px\">Standard travel [mm]</span>")
        self.graphicsView_1.setLabel("bottom", "<span style=\"color: black; font-size: 12px\">Time [s]</span>")

        self.graphicsView_2.setBackground("w")
        self.graphicsView_2.setLabel("left", "<span style=\"color: black; font-size: 12px\">Standard force [N]</span>")
        self.graphicsView_2.setLabel("bottom", "<span style=\"color: black; font-size: 12px\">Time [s]</span>")
    
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

    def importData(self, dir=None):
        if dir is None:
            dir = "./"

        self.csvDataPath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import CSV file path...", str(dir))

        if self.csvDataPath == "":
            # Show a message box
            self.showMessageBox(text="Incorrect path was given - please try again")
        else:
            # Disable "Import file path" button
            # Enable "Mark points" and "Reset" buttons
            self.pushButton_2.setEnabled(False)

            # Data import
            self.stdTravel, self.stdForce, self.t = Data(self.csvDataPath).upload()

            # Data plot
            pen1 = pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.SolidLine)
            pen2 = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.SolidLine)
            self.graphicsView_1.plot(self.t, self.stdTravel, pen=pen1)
            self.graphicsView_2.plot(self.t, self.stdForce, pen=pen2)

    def markPoints(self):
        self.video = Video(self.videoPath, "Initial frame")
        self.video.markPoints()

        if self.video.getPoints() == None:
            # Show a message box
            self.showMessageBox(text="No points were marked - please try again")
        else:
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
            ret, frame, ts, _ = self.video.getFrame(timestamp=True)
            
            # Get points' coordinates
            p1, p2, p3, p4 = self.video.getOldPoints()

            # Update LCD displays (coordinates are numpy arrays)
            # Since these are numpy arrays, add [0]
            self.p1x.display(p1[0][0]); self.p1y.display(p1[0][1])
            self.p2x.display(p2[0][0]); self.p2y.display(p2[0][1])
            self.p3x.display(p3[0][0]); self.p3y.display(p3[0][1])
            self.p4x.display(p4[0][0]); self.p4y.display(p4[0][1])

            # Update progress bar
            progress = int(100*ts/max(self.t))
            if self.progressBar.value() is not progress:
                self.progressBar.setValue(progress)

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