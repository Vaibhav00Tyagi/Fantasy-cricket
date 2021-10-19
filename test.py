# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:33:12 2020

@author: Vaibhav Tyagi
"""
from PyQt5 import QtWidgets
from project_main import Ui_MainWindow
from quit_diag import Ui_Dialog

class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(w.close)
        

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionQuit.triggered.connect(self.onClicked)

    def onClicked(self):
        updateDialog = Dialog()
        updateDialog.exec_()
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
