from PyQt5 import QtCore, QtGui, QtWidgets
from ui import ui
from jproperties import Properties
import zipfile
import datetime
import sys
import csv
import os
class BackupUtility(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BackupUtility, self).__init__(parent)
        self.setupUi(self)
        self.browseButton.clicked.connect(self.browseBackupFolder)
        self.addServerButton.clicked.connect(self.addServer)
        self.makeBackupButton.clicked.connect(self.backup)
        with open("D:\\Programming\\PythonProjects\\mcserverbackuputility\\data\\backupsfolder.txt", "r") as f:
            self.backupFolder = f.read()
            self.folderPathLineEdit.setText(self.backupFolder)
        with open("D:\\Programming\\PythonProjects\\mcserverbackuputility\\data\\servers.csv") as f:
            reader = csv.reader(f)
            self.servers = dict(reader)
            for server in self.servers.keys():
                self.serverSelectComboBox.addItem(server)
    def browseBackupFolder(self):
        backupDir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select backups folder', "C://")
        self.folderPathLineEdit.setText(backupDir)
        self.backupFolder = backupDir
        with open("D:\\Programming\\PythonProjects\\mcserverbackuputility\\data\\backupsfolder.txt", "w") as f:
            f.write(self.backupFolder)
    def addServer(self):
        warn = QtWidgets.QMessageBox()
        warn.setWindowTitle("Warning")
        warn.setIcon(QtWidgets.QMessageBox.Warning)
        serverDir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select server folder', "C://")
        for key, value in self.servers.items():
            if value == serverDir:
                warn.setText(f'The selected folder is already registered under the name of "{key}"')
                warn.exec_()
                return None
        if serverDir != '':
            validServer = False
            for filename in os.listdir(serverDir):
                if filename == "server.properties":
                    validServer = True
            if validServer:
                getServerName = QtWidgets.QInputDialog()
                serverName = getServerName.getText(self, 'Server Name', 'Enter server name:')
                if serverName[1] == True:
                    self.serverSelectComboBox.addItem(serverName[0])
                    self.servers[serverName[0]] = serverDir
                    self.updateServerList()
                print(serverName)
            else:
                warn.setText("The selected directory is an invalid Minecraft server directory")
                warn.exec_()
    def backup(self):
        warn = QtWidgets.QMessageBox()
        warn.setWindowTitle("Warning")
        warn.setIcon(QtWidgets.QMessageBox.Warning)
        if self.backupFolder == '':
            warn.setText("Please register a backup folder to send backups to before attempting to make a backup")
            warn.exec_()
        elif not os.path.isdir(self.backupFolder):
            warn.setText("The currently registered backups directly was either moved or deleted. Please register a new backups directory.")
        else:
            serverName = self.serverSelectComboBox.currentText()
            dirToBackUp = self.servers[serverName]
            checkDir = os.path.isdir(f"{self.backupFolder}/{serverName}")
            if not checkDir:
                os.makedirs(f"{self.backupFolder}/{serverName}")
            checkDir = os.path.isdir(f"{self.backupFolder}/{serverName}/{datetime.date.today()}")
            if not checkDir:
                os.makedirs(f"{self.backupFolder}/{serverName}/{datetime.date.today()}")
            currentTime = datetime.datetime.now()
            currentTime = " ".join(datetime.datetime.strftime(currentTime, "%I:%M %p").split(" ")).replace(":", ";")
            zipf = zipfile.ZipFile(f"{self.backupFolder}/{serverName}/{datetime.date.today()}/{currentTime}.zip", 'a', zipfile.ZIP_DEFLATED)
            self.zipdir(dirToBackUp, zipf)
    def updateServerList(self):
        with open("D:\\Programming\\PythonProjects\\mcserverbackuputility\\data\\servers.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for key, value in self.servers.items():
                writer.writerow([key, value])
    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = BackupUtility()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()