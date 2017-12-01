from PyQt5 import QtCore, QtGui, QtWidgets
from GUI import server

class guiHandler(QtWidgets.QMainWindow):
    def __init__(self, Form, system, parent = None):
        super(guiHandler, self).__init__(parent)
        self.searchEnable = 0 #0 is unavailable
        self.system = system
        self.Form = Form
        ui = server.Ui_KUFLIXserver()
        ui.setupUi(Form)
        ui.uploadButton.clicked.connect(lambda: self.upload(ui))
        ui.deleteButton.clicked.connect(lambda: self.delete(ui))
        self.refresh(ui)
        self.system.startMainLoop()

    def upload(self, ui):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie", QtCore.QDir.homePath())
        if fileName != '':
            self.system.uploadNewContents(fileName)

        self.refresh(ui)

    def delete(self, ui):
        cid = str(self.contentsList[ui.itemList.currentRow()][0])

        self.system.deleteContents(cid)

        self.refresh(ui)

    def refresh(self, ui):
        result = self.system.getContentsList()

        self.contentsList = []

        ui.itemList.clear()

        for i in range(0, result.__len__()):
            self.contentsList.append(result[i])
            ui.itemList.addItem(result[i][1])


def startProgram(system):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    handle = guiHandler(Form, system)
    Form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    handle = guiHandler()
    Form.show()
    sys.exit(app.exec_())