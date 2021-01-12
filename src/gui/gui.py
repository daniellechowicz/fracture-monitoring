from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import sys, time

class Appli(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() 

        # Import GUI XML layout
        self.ui = uic.loadUi("gui.ui", self)
        
        self.setWindowTitle("Fracture Monitoring") 

        # Setting the icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # When "Import video path" button clicked, execute the following:
        self.pushButton_1.clicked.connect(self.videoPathDialog)
        
    def videoPathDialog(self, dir=None):
        if dir is None:
            dir = "./"

        self.videoPath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import video path...", str(dir))
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Appli()
    mainWindow.show()
    sys.exit(app.exec_())