# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainGUI(object):
    def setupUi(self, mainGUI):
        mainGUI.setObjectName("mainGUI")
        mainGUI.resize(600, 800)
        mainGUI.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.reactor = QtWidgets.QLabel(mainGUI)
        self.reactor.setGeometry(QtCore.QRect(10, 110, 571, 421))
        self.reactor.setText("")
        self.reactor.setPixmap(QtGui.QPixmap("D:/jarvis-virtual assistant/gui-gifs/SVKl.gif"))
        self.reactor.setScaledContents(True)
        self.reactor.setObjectName("reactor")
        self.jarvis = QtWidgets.QLabel(mainGUI)
        self.jarvis.setGeometry(QtCore.QRect(40, 10, 511, 101))
        self.jarvis.setText("")
        self.jarvis.setPixmap(QtGui.QPixmap("D:/jarvis-virtual assistant/gui-gifs/attachment_97425804 (1).jpeg"))
        self.jarvis.setScaledContents(True)
        self.jarvis.setObjectName("jarvis")
        self.output = QtWidgets.QPlainTextEdit(mainGUI)
        self.output.setGeometry(QtCore.QRect(10, 540, 581, 251))
        self.output.setPlainText("")
        self.output.setObjectName("output")

        self.retranslateUi(mainGUI)
        QtCore.QMetaObject.connectSlotsByName(mainGUI)

    def retranslateUi(self, mainGUI):
        _translate = QtCore.QCoreApplication.translate
        mainGUI.setWindowTitle(_translate("mainGUI", "mainGUI"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainGUI = QtWidgets.QWidget()
    ui = Ui_mainGUI()
    ui.setupUi(mainGUI)
    mainGUI.show()
    sys.exit(app.exec_())