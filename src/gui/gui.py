from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import ctypes
import cv2
import numpy as np
import sys
import time

class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() 

        # Import GUI XML layout
        self.ui = uic.loadUi("gui.ui", self)
        
        self.setWindowTitle("Fracture Monitoring") 

        # Setting the icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # To get mouse events, I need to set mouse tracking functionality to True
        self.setMouseTracking(True)

        # When "Import video path" button clicked, execute the following:
        self.pushButton_1.clicked.connect(self.videoPathDialog)
        self.pushButton_2.clicked.connect(self.getFrame)
        self.pushButton_4.clicked.connect(self.reset)

        # Disable "Import frames button" - one cannot upload frames if no path was given
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)

        # This applies for threads
        # th = Thread(self)
        # th.changePixmap.connect(self.setImage)
        # th.start()
        # self.show()

    # It works!
    def mousePressEvent(self, eventQMouseEvent):
        self.evt = eventQMouseEvent.button()
        print(self.evt)

    def mouseMoveEvent(self, eventQMouseEvent):
        self.x, self.y = eventQMouseEvent.x(), eventQMouseEvent.y()
        cvImg = np.zeros((900,900), dtype=np.uint8)
        cv2.circle(cvImg, (449,449), 100, 255, -1)
        cv2.putText(cvImg, "x at {}, y at {}".format(self.x, self.y), (375,455), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        height, width = cvImg.shape
        bytearr = cvImg.data
        qImg = QtGui.QImage(bytearr, width, height, QtGui.QImage.Format_Indexed8)
        # self.setPixmap(QtGui.QPixmap.fromImage(qImg))
        self.label_3.setPixmap(QtGui.QPixmap.fromImage(qImg))
    
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
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
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