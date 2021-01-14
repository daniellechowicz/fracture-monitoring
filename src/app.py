from PyQt5 import QtWidgets
import sys

from views import UserInterface


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = UserInterface()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()