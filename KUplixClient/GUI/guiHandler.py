from PyQt5 import QtCore, QtGui, QtWidgets
from GUI import join, login, service, subscribeList, recentList

class guiHandler(object):
    def __init__(self, Form, system):
        self.searchEnable = 0 #0 is unavailable
        self.system = system
        self.Form = Form
        ui = login.Ui_KUFLIX()
        ui.setupUi(Form)
        ui.join.clicked.connect(lambda: self.goToJoin())
        ui.login.clicked.connect(lambda: self.login(ui))

    def login(self, ui):
        id = ui.id.toPlainText()
        passwd = ui.passwd.toPlainText()
        if self.system.loginRequest(self.system.protocolGenerator(0, 0, [id, passwd])) != "nop":
            self.loginSuccess()
        # login fail popup

    def join(self, ui):
        id = ui.joinINPUTID.toPlainText()
        passwd = ui.joinINPUTPASSWD.toPlainText()
        name = ui.joinINPUTNAME.toPlainText()
        age = ui.joinINPUTAGE.toPlainText()
        if self.system.loginRequest(self.system.protocolGenerator(0, 1, [id, passwd, name, age])) != "nop":
            self.joinSave()
        # join fail popup

    def loginSuccess(self):
        ui = service.Ui_service()
        ui.setupUi(self.Form)

        ui.ID_lable.setText(self.system.id)
        ui.NAME_lable.setText(self.system.name)
        ui.RANK_label.setText(self.system.name)
        ui.thumnail1.setText(self.system.tmList[0])
        ui.thumnail2.setText(self.system.tmList[1])
        ui.thumnail3.setText(self.system.tmList[2])
        ui.thumnail4.setText(self.system.tmList[3])
        ui.thumnail5.setText(self.system.tmList[4])
        ui.thumnail6.setText(self.system.tmList[5])
        ui.thumnail7.setText(self.system.tmList[6])
        ui.thumnail8.setText(self.system.tmList[7])
        ui.thumnail9.setText(self.system.tmList[8])
        ui.thumnail10.setText(self.system.tmList[9])
        ui.thumnail11.setText(self.system.tmList[10])
        ui.thumnail12.setText(self.system.tmList[11])


        ui.logout.clicked.connect(lambda: self.goBack())
        ui.menu.activated.connect(lambda: self.hadleCombo(ui))
        ui.searchButton.clicked.connect(lambda: self.requestSearch(ui))
        self.searchEnable = 1

    def requestSearch(self, ui):
        keyword = ui.search.toPlainText()
        self.system.searchList = []
        result = self.system.mainRequest(self.system.protocolGenerator(1, 2, [keyword, self.system.uid]))
        ui.searchResult.clear()
        for i in range(0, result.__len__()):
            ui.searchResult.append(result[i][2])

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
        self.searchEnable = 0

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