from PyQt5 import QtCore, QtGui, QtWidgets
from GUI import join, login, service, subscribeList, recentList
import hashlib

class guiHandler(object):
    def __init__(self, Form, system):
        self.searchEnable = 0 #0 is unavailable
        self.system = system
        self.Form = Form
        self.searchList = []
        self.subList = []
        self.recentList = []
        ui = login.Ui_KUFLIX()
        ui.setupUi(Form)
        ui.join.clicked.connect(lambda: self.goToJoin())
        ui.login.clicked.connect(lambda: self.login(ui))

    def login(self, ui):
        id = ui.id.toPlainText()
        passwd = ui.passwd.toPlainText()
        passwd = hashlib.sha256(bytes(passwd, "utf-8")).hexdigest()
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

        print(self.system.tmList)

        ui.ID_lable.setText(self.system.id)
        ui.NAME_lable.setText(self.system.name)
        ui.RANK_label.setText(self.system.rank)
        ui.t_label1.setText(self.system.tmList[1][0])
        ui.t_label2.setText(self.system.tmList[2][0])
        ui.t_label3.setText(self.system.tmList[3][0])
        ui.t_label4.setText(self.system.tmList[4][0])
        ui.t_label5.setText(self.system.tmList[5][0])
        ui.t_label6.setText(self.system.tmList[6][0])
        ui.t_label7.setText(self.system.tmList[7][0])
        ui.t_label8.setText(self.system.tmList[8][0])
        ui.t_label9.setText(self.system.tmList[9][0])
        ui.t_label10.setText(self.system.tmList[10][0])
        ui.t_label11.setText(self.system.tmList[11][0])
        ui.t_label12.setText(self.system.tmList[12][0])


        ui.logout.clicked.connect(lambda: self.goBack())
        ui.menu.activated.connect(lambda: self.hadleCombo(ui))
        ui.searchButton.clicked.connect(lambda: self.requestSearch(ui))
        ui.thumnail1.clicked.connect(lambda: self.thumnailStart(self.system.tmList[1][1]))
        ui.thumnail2.clicked.connect(lambda: self.thumnailStart(self.system.tmList[2][1]))
        ui.thumnail3.clicked.connect(lambda: self.thumnailStart(self.system.tmList[3][1]))
        ui.thumnail4.clicked.connect(lambda: self.thumnailStart(self.system.tmList[4][1]))
        ui.thumnail5.clicked.connect(lambda: self.thumnailStart(self.system.tmList[5][1]))
        ui.thumnail6.clicked.connect(lambda: self.thumnailStart(self.system.tmList[6][1]))
        ui.thumnail7.clicked.connect(lambda: self.thumnailStart(self.system.tmList[7][1]))
        ui.thumnail8.clicked.connect(lambda: self.thumnailStart(self.system.tmList[8][1]))
        ui.thumnail9.clicked.connect(lambda: self.thumnailStart(self.system.tmList[9][1]))
        ui.thumnail10.clicked.connect(lambda: self.thumnailStart(self.system.tmList[10][1]))
        ui.thumnail11.clicked.connect(lambda: self.thumnailStart(self.system.tmList[11][1]))
        ui.thumnail12.clicked.connect(lambda: self.thumnailStart(self.system.tmList[12][1]))

        ui.thumnail1.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/101.png")))
        ui.thumnail1.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail2.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/102.png")))
        ui.thumnail2.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail3.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/103.png")))
        ui.thumnail3.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail4.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/104.png")))
        ui.thumnail4.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail5.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/105.png")))
        ui.thumnail5.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail6.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/106.png")))
        ui.thumnail6.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail7.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/107.png")))
        ui.thumnail7.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail8.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/108.png")))
        ui.thumnail8.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail9.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/109.png")))
        ui.thumnail9.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail10.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/110.png")))
        ui.thumnail10.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail11.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/111.png")))
        ui.thumnail11.setIconSize(QtCore.QSize(151, 121))
        ui.thumnail12.setIcon(QtGui.QIcon(QtGui.QPixmap("./thumnails/112.png")))
        ui.thumnail12.setIconSize(QtCore.QSize(151, 121))




        self.searchEnable = 1

    def getIndexinSearch(self, ui):
        if self.searchList.__len__() > 0:
            index = self.searchList[ui.searchResult.currentRow()][1]
            print(index)
            if index.find('Found') <= 0:
                self.thumnailStart(index)

    def getIndexinRecent(self, ui):
        if self.recentList.__len__() > 0:
            index = str(int(self.recentList[ui.listWidget.currentRow()][3]) + 1)
            print(index)
            if index.find('Found') <= 0:
                self.thumnailStart(index)

    def getIndexinSub(self, ui):
        if self.subList.__len__() > 0:
            index = str(int(self.subList[ui.subList.currentRow()][3]) + 1)
            print(index)
            if index.find('Found') <= 0:
                self.thumnailStart(index)

    def thumnailStart(self, index):
        self.system.startPlayer(index)

    def requestSearch(self, ui):
        keyword = ui.search.toPlainText()
        self.searchList = []
        result = self.system.mainRequest(self.system.protocolGenerator(1, 2, [keyword]))
        print(result)
        ui.searchResult.clear()
        for i in range(0, result.__len__()):
            ui.searchResult.addItem(result[i][2])
            self.searchList.append(result[i])
        ui.searchResult.doubleClicked.connect(lambda: self.getIndexinSearch(ui))

    def hadleCombo(self, ui):
        if ui.menu.currentIndex() != 1:
            self.goSubList()
        else:
            self.goRecentList()

    def goSubList(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = subscribeList.Ui_subscribeListForm()
        dialog.ui.setupUi(dialog)
        #get list from system DB and add Item to List
        self.getList("1", dialog.ui)

        dialog.ui.subList.doubleClicked.connect(lambda: self.getIndexinSub(dialog.ui))

        dialog.exec_()
        dialog.show()

    def goRecentList(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = recentList.Ui_recentList_Form()
        dialog.ui.setupUi(dialog)
        # get list from system DB and add Item to List
        self.getList("0", dialog.ui)

        dialog.ui.listWidget.doubleClicked.connect(lambda: self.getIndexinRecent(dialog.ui))

        dialog.exec_()
        dialog.show()

    def getList(self, types = "0", ui = None):
        if types == "0":
            self.recentList = []
            result = self.system.mainRequest(self.system.protocolGenerator(1, 4, ["200"]))
            print(result)
            ui.listWidget.clear()
            for i in range(0, result.__len__()):
                item = result[i][1] + " || " + result[i][2]
                self.recentList.append(result[i])
                ui.listWidget.addItem(item)
        else:
            self.subList = []
            result = self.system.mainRequest(self.system.protocolGenerator(1, 4, ["300"]))
            print(result)
            ui.subList.clear()
            for i in range(0, result.__len__()):
                self.subList.append(result[i])
                item = result[i][1]
                ui.subList.addItem(item)

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