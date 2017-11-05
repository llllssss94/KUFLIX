# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recentList.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_recentList_Form(object):
    def setupUi(self, recentList_Form):
        recentList_Form.setObjectName("recentList_Form")
        recentList_Form.resize(362, 504)
        self.recentList_label = QtWidgets.QLabel(recentList_Form)
        self.recentList_label.setGeometry(QtCore.QRect(10, 10, 341, 81))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.recentList_label.setFont(font)
        self.recentList_label.setAlignment(QtCore.Qt.AlignCenter)
        self.recentList_label.setObjectName("recentList_label")
        self.listWidget = QtWidgets.QListWidget(recentList_Form)
        self.listWidget.setGeometry(QtCore.QRect(10, 90, 341, 401))
        self.listWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)

        self.retranslateUi(recentList_Form)
        QtCore.QMetaObject.connectSlotsByName(recentList_Form)

    def retranslateUi(self, recentList_Form):
        _translate = QtCore.QCoreApplication.translate
        recentList_Form.setWindowTitle(_translate("recentList_Form", "recentList"))
        self.recentList_label.setText(_translate("recentList_Form", "RECENT LIST"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("recentList_Form", "hhh"))
        self.listWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    recentList_Form = QtWidgets.QDialog()
    ui = Ui_recentList_Form()
    ui.setupUi(recentList_Form)
    recentList_Form.show()
    sys.exit(app.exec_())

