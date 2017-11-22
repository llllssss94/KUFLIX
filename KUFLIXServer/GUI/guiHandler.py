from PyQt5 import QtCore, QtGui, QtWidgets
from GUI import server

class guiHandler(QtWidgets.QMainWindow):
    def __init__(self, Form, system, parent = None):
        super(guiHandler, self).__init__(parent)
        self.searchEnable = 0 #0 is unavailable
        self.system = system
        self.system.mainLoop()
        self.Form = Form
        ui = server.Ui_KUFLIXserver()
        ui.setupUi(Form)
        ui.uploadButton.clicked.connect(lambda: self.upload())
        ui.deleteButton.clicked.connect(lambda: self.delete())
        self.refresh(ui)

    def upload(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie", QtCore.QDir.homePath())
        if fileName != '':
            self.system.uploadNewContents(fileName)

    def delete(self):
        cid = "3"
        self.system.deleteContents(cid)

    def refresh(self, ui):
        result = self.system.getContentsList()

        for i in range(0, result.__len__()):
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