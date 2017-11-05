from PyQt5 import QtCore, QtGui, QtWidgets
import join, login, service, subscribeList, recentList

class guiHandler(object):
    def __init__(self):
        ui = login.Ui_KUFLIX()
        ui.setupUi(Form)
        ui.join.clicked.connect(lambda: self.goToJoin())
        ui.login.clicked.connect(lambda: self.loginSuccess())

    def loginSuccess(self):
        ui = service.Ui_service()
        ui.setupUi(Form)
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
        ui.setupUi(Form)
        ui.joinSave.clicked.connect(lambda: self.joinSave())
        ui.joinCancel.clicked.connect(lambda : self.goBack())

    def joinSave(self):
        ui = login.Ui_KUFLIX()
        ui.setupUi(Form)
        ui.join.clicked.connect(lambda: self.goToJoin())
        ui.login.clicked.connect(lambda: self.loginSuccess())

    def goBack(self):
        ui = login.Ui_KUFLIX()
        ui.setupUi(Form)
        ui.join.clicked.connect(lambda : self.goToJoin())
        ui.login.clicked.connect(lambda: self.loginSuccess())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    handle = guiHandler()
    Form.show()
    sys.exit(app.exec_())