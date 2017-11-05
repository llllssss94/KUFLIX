# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'join.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Join(object):
    def setupUi(self, Join):
        Join.setObjectName("Join")
        Join.resize(388, 518)
        self.centralwidget = QtWidgets.QWidget(Join)
        self.centralwidget.setObjectName("centralwidget")
        self.welcome = QtWidgets.QLabel(self.centralwidget)
        self.welcome.setGeometry(QtCore.QRect(20, 20, 311, 91))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.welcome.setFont(font)
        self.welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome.setObjectName("welcome")
        self.joinID = QtWidgets.QLabel(self.centralwidget)
        self.joinID.setGeometry(QtCore.QRect(60, 160, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.joinID.setFont(font)
        self.joinID.setAlignment(QtCore.Qt.AlignCenter)
        self.joinID.setObjectName("joinID")
        self.joinPASSWD = QtWidgets.QLabel(self.centralwidget)
        self.joinPASSWD.setGeometry(QtCore.QRect(30, 230, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.joinPASSWD.setFont(font)
        self.joinPASSWD.setObjectName("joinPASSWD")
        self.joinName = QtWidgets.QLabel(self.centralwidget)
        self.joinName.setGeometry(QtCore.QRect(60, 300, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.joinName.setFont(font)
        self.joinName.setObjectName("joinName")
        self.joinAge = QtWidgets.QLabel(self.centralwidget)
        self.joinAge.setGeometry(QtCore.QRect(60, 370, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.joinAge.setFont(font)
        self.joinAge.setObjectName("joinAge")
        self.joinINPUTID = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.joinINPUTID.setGeometry(QtCore.QRect(160, 150, 181, 41))
        self.joinINPUTID.setObjectName("joinINPUTID")
        self.joinINPUTPASSWD = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.joinINPUTPASSWD.setGeometry(QtCore.QRect(160, 220, 181, 41))
        self.joinINPUTPASSWD.setObjectName("joinINPUTPASSWD")
        self.joinINPUTNAME = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.joinINPUTNAME.setGeometry(QtCore.QRect(160, 300, 181, 41))
        self.joinINPUTNAME.setObjectName("joinINPUTNAME")
        self.joinINPUTAGE = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.joinINPUTAGE.setGeometry(QtCore.QRect(160, 370, 181, 41))
        self.joinINPUTAGE.setObjectName("joinINPUTAGE")
        self.joinSave = QtWidgets.QPushButton(self.centralwidget)
        self.joinSave.setGeometry(QtCore.QRect(60, 430, 87, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.joinSave.setFont(font)
        self.joinSave.setObjectName("joinSave")
        self.joinCancel = QtWidgets.QPushButton(self.centralwidget)
        self.joinCancel.setGeometry(QtCore.QRect(230, 430, 87, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.joinCancel.setFont(font)
        self.joinCancel.setObjectName("joinCancel")
        Join.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Join)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 388, 23))
        self.menubar.setObjectName("menubar")
        Join.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Join)
        self.statusbar.setObjectName("statusbar")
        Join.setStatusBar(self.statusbar)

        self.retranslateUi(Join)
        QtCore.QMetaObject.connectSlotsByName(Join)

    def retranslateUi(self, Join):
        _translate = QtCore.QCoreApplication.translate
        Join.setWindowTitle(_translate("Join", "Join"))
        self.welcome.setText(_translate("Join", "WELCOME TO\n"
" KUFLIX"))
        self.joinID.setText(_translate("Join", "ID"))
        self.joinPASSWD.setText(_translate("Join", "PASSWORD"))
        self.joinName.setText(_translate("Join", "이름"))
        self.joinAge.setText(_translate("Join", "나이"))
        self.joinSave.setText(_translate("Join", "저장"))
        self.joinCancel.setText(_translate("Join", "취소"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Join = QtWidgets.QMainWindow()
    ui = Ui_Join()
    ui.setupUi(Join)
    Join.show()
    sys.exit(app.exec_())

