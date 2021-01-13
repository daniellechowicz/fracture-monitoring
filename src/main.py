from PyQt5.QtWidgets import QApplication
from views import UI_Window
from models import Camera

if __name__ == '__main__':

    camera = Camera(0)

    app = QApplication([])
    startWindow = UI_Window(camera)
    startWindow.show()
    app.exit(app.exec_())