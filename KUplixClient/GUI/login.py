# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_KUFLIX(object):
    def setupUi(self, KUFLIX):
        KUFLIX.setObjectName("KUFLIX")
        KUFLIX.resize(488, 295)
        self.centralwidget = QtWidgets.QWidget(KUFLIX)
        self.centralwidget.setObjectName("centralwidget")
        self.KUflix = QtWidgets.QLabel(self.centralwidget)
        self.KUflix.setGeometry(QtCore.QRect(10, 10, 271, 101))
        font = QtGui.QFont()
        font.setPointSize(43)
        font.setBold(True)
        font.setWeight(75)
        self.KUflix.setFont(font)
        self.KUflix.setAlignment(QtCore.Qt.AlignCenter)
        self.KUflix.setObjectName("KUflix")
        self.version = QtWidgets.QLabel(self.centralwidget)
        self.version.setGeometry(QtCore.QRect(360, 40, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.version.setFont(font)
        self.version.setObjectName("version")
        self.id = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.id.setGeometry(QtCore.QRect(20, 120, 271, 41))
        self.id.setObjectName("id")
        self.passwd = QtWidgets.QTextEdit(self.centralwidget)
        self.passwd.setGeometry(QtCore.QRect(20, 190, 271, 41))
        self.passwd.setObjectName("passwd")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(350, 120, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.login.setFont(font)
        self.login.setObjectName("login")
        self.join = QtWidgets.QPushButton(self.centralwidget)
        self.join.setGeometry(QtCore.QRect(350, 190, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.join.setFont(font)
        self.join.setObjectName("join")
        KUFLIX.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(KUFLIX)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 488, 23))
        self.menubar.setObjectName("menubar")
        KUFLIX.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(KUFLIX)
        self.statusbar.setObjectName("statusbar")
        KUFLIX.setStatusBar(self.statusbar)

        self.retranslateUi(KUFLIX)
        QtCore.QMetaObject.connectSlotsByName(KUFLIX)

    def retranslateUi(self, KUFLIX):
        _translate = QtCore.QCoreApplication.translate
        KUFLIX.setWindowTitle(_translate("KUFLIX", "KUFLIX"))
        self.KUflix.setText(_translate("KUFLIX", "KUFLIX"))
        self.version.setText(_translate("KUFLIX", "Ver.1.0"))
        self.login.setText(_translate("KUFLIX", "로그인"))
        self.join.setText(_translate("KUFLIX", "회원가입"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KUFLIX = QtWidgets.QMainWindow()
    ui = Ui_KUFLIX()
    ui.setupUi(KUFLIX)
    KUFLIX.show()
    sys.exit(app.exec_())

