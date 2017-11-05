# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subscribeList.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_subscribeListForm(object):
    def setupUi(self, subscribeListForm):
        subscribeListForm.setObjectName("subscribeListForm")
        subscribeListForm.resize(363, 505)
        self.subscribeList_label = QtWidgets.QLabel(subscribeListForm)
        self.subscribeList_label.setGeometry(QtCore.QRect(10, 0, 341, 81))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.subscribeList_label.setFont(font)
        self.subscribeList_label.setAlignment(QtCore.Qt.AlignCenter)
        self.subscribeList_label.setObjectName("subscribeList_label")
        self.subList = QtWidgets.QListWidget(subscribeListForm)
        self.subList.setGeometry(QtCore.QRect(10, 80, 341, 411))
        self.subList.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.subList.setObjectName("subList")
        item = QtWidgets.QListWidgetItem()
        self.subList.addItem(item)

        self.retranslateUi(subscribeListForm)
        QtCore.QMetaObject.connectSlotsByName(subscribeListForm)

    def retranslateUi(self, subscribeListForm):
        _translate = QtCore.QCoreApplication.translate
        subscribeListForm.setWindowTitle(_translate("subscribeListForm", "subscribeList"))
        self.subscribeList_label.setText(_translate("subscribeListForm", "SUBSCRIBE LIST"))
        __sortingEnabled = self.subList.isSortingEnabled()
        self.subList.setSortingEnabled(False)
        item = self.subList.item(0)
        item.setText(_translate("subscribeListForm", "oh"))
        self.subList.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    subscribeListForm = QtWidgets.QDialog()
    ui = Ui_subscribeListForm()
    ui.setupUi(subscribeListForm)
    subscribeListForm.show()
    sys.exit(app.exec_())

