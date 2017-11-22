# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_KUFLIXserver(object):
    def setupUi(self, KUFLIXserver):
        KUFLIXserver.setObjectName("KUFLIXserver")
        KUFLIXserver.resize(351, 535)
        self.centralwidget = QtWidgets.QWidget(KUFLIXserver)
        self.centralwidget.setObjectName("centralwidget")
        self.contentsList = QtWidgets.QLabel(self.centralwidget)
        self.contentsList.setGeometry(QtCore.QRect(20, 10, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.contentsList.setFont(font)
        self.contentsList.setAlignment(QtCore.Qt.AlignCenter)
        self.contentsList.setObjectName("contentsList")
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadButton.setGeometry(QtCore.QRect(10, 440, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.uploadButton.setFont(font)
        self.uploadButton.setObjectName("uploadButton")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(180, 440, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName("deleteButton")
        self.itemList = QtWidgets.QListWidget(self.centralwidget)
        self.itemList.setGeometry(QtCore.QRect(10, 70, 331, 351))
        self.itemList.setObjectName("itemList")
        KUFLIXserver.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(KUFLIXserver)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 351, 23))
        self.menubar.setObjectName("menubar")
        KUFLIXserver.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(KUFLIXserver)
        self.statusbar.setObjectName("statusbar")
        KUFLIXserver.setStatusBar(self.statusbar)

        self.retranslateUi(KUFLIXserver)
        QtCore.QMetaObject.connectSlotsByName(KUFLIXserver)

    def retranslateUi(self, KUFLIXserver):
        _translate = QtCore.QCoreApplication.translate
        KUFLIXserver.setWindowTitle(_translate("KUFLIXserver", "KUFLIXserver"))
        self.contentsList.setText(_translate("KUFLIXserver", "Contents List"))
        self.uploadButton.setText(_translate("KUFLIXserver", "등록"))
        self.deleteButton.setText(_translate("KUFLIXserver", "삭제"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KUFLIXserver = QtWidgets.QMainWindow()
    ui = Ui_KUFLIXserver()
    ui.setupUi(KUFLIXserver)
    KUFLIXserver.show()
    sys.exit(app.exec_())

