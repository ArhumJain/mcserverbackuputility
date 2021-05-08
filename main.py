from PyQt5 import QtCore, QtGui, QtWidgets
from ui import ui
import sys
class BackupUtility(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BackupUtility, self).__init__(parent)
        self.setupUi(self)
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = BackupUtility()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()