from PyQt5 import QtCore, QtGui, QtWidgets
from GUI import join, login, service, subscribeList, recentList

class guiHandler(object):
    def __init__(self, Form, system):
        self.system = system
        self.Form = Form
        ui = login.Ui_KUFLIX()
        ui.setupUi(Form)
        ui.join.clicked.connect(lambda: self.goToJoin())
        ui.login.clicked.connect(lambda: self.login(ui))

    def login(self, ui):
        id = ui.id.toPlainText()
        passwd = ui.passwd.toPlainText()
        self.system.request(self.system.protocolGenerator(0, [id, passwd]))
        self.loginSuccess()

    def join(self, ui):
        id = ui.joinINPUTID.toPlainText()
        passwd = ui.joinINPUTPASSWD.toPlainText()
        name = ui.joinINPUTNAME.toPlainText()
        age = ui.joinINPUTAGE.toPlainText()
        self.system.request(self.system.protocolGenerator(1, [id, passwd, name, age]))
        self.joinSave()

    def loginSuccess(self):
        ui = service.Ui_service()
        ui.setupUi(self.Form)
        ui.logout.clicked.connect(lambda: self.goBack())
        ui.menu.activated.connect(lambda: self.hadleCombo(ui))

    def hadleCombo(self, ui):
        if ui.menu.currentIndex() != 1:
            self.goSubList()
        else:
            self.goRecentList()

    def goSubList(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = subscribeList.Ui_subscribeListForm()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def goRecentList(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = recentList.Ui_recentList_Form()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def goToJoin(self):
        ui = join.Ui_Join()
        ui.setupUi(self.Form)
        ui.joinSave.clicked.connect(lambda: self.join(ui))
        ui.joinCancel.clicked.connect(lambda : self.goBack())

    def joinSave(self):
        ui = login.Ui_KUFLIX()
        ui.setupUi(self.Form)
        ui.join.clicked.connect(lambda: self.goToJoin())
        ui.login.clicked.connect(lambda: self.login(ui))

    def goBack(self):
        ui = login.Ui_KUFLIX()
        ui.setupUi(self.Form)
        ui.join.clicked.connect(lambda : self.goToJoin())
        ui.login.clicked.connect(lambda: self.login(ui))

def startProgram(object):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    handle = guiHandler(Form, object)
    Form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    handle = guiHandler()
    Form.show()
    sys.exit(app.exec_())