
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(636, 554)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 3, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 0, 2, 1)
        self.B2 = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.B2.setFont(font)
        self.B2.setObjectName("B2")
        self.gridLayout.addWidget(self.B2, 3, 2, 1, 1)
        self.B1 = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.B1.setFont(font)
        self.B1.setObjectName("B1")
        self.gridLayout.addWidget(self.B1, 3, 1, 1, 1)
        self.LW1 = QtWidgets.QListWidget(Dialog)
        self.LW1.setObjectName("LW1")
        self.gridLayout.addWidget(self.LW1, 2, 1, 1, 2)
        self.L1 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.L1.setFont(font)
        self.L1.setObjectName("L1")
        self.gridLayout.addWidget(self.L1, 1, 1, 1, 2)
        
        self.B1.clicked.connect(Dialog.close)
        self.B2.clicked.connect(Dialog.close)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "OPEN"))
        self.B2.setText(_translate("Dialog", "cancel"))
        self.B1.setText(_translate("Dialog", "OK"))
        self.L1.setText(_translate("Dialog", "Available Teams "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

