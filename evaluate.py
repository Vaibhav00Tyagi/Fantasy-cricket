""" This module is for executing the evaluation Window"""

#importing required pyqt5 modules
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

#connecting to our database and creating a cursor
myplayer=sqlite3.connect("resources\Fantasy Cricket.db")
player_cur=myplayer.cursor()

#declaring the form class whose object will create evaluation window
class Ui_Form(object):
    team_score=0
    def player_score(self,player):
        score=0
        if player[2]>0:
            score=int(player[1]/2)
            if player[1]>100:
                score+=10
            if player[1]>50:
                score+=5
            st_rate=player[1]/player[2]*100
            if st_rate>100:
                score+=4
            elif st_rate>=80:
                score+=2
            else:
                score+=0
        score+=player[3]
        score+=player[4]*2
        score+=player[9]*10
        score+=player[10]*10
        score+=player[11]*10
        score+=player[8]*10
        if player[5]>0:
            if player[8]>=5:
                score+=10
            if player[8]>=3:
                score+=5
            economy=player[7]/player[5]
            if economy>4.5:
                score+=0
            elif economy>=3.5:
                score+=4
            elif economy>=2:
                score+=7
            elif economy<2:
                score+=10
        self.team_score+=score
        self.LW2.addItem(str(score))
        
#this function calculates and displayes the score of individual players
    def calculate_score(self):
        self.LW1.clear()
        self.LW2.clear()
        self.team_score=0
        team_name=self.combo1.currentText()
        match=self.combo2.currentText()
        
        #this part checks if proper selection was made or not
        if team_name=="---TEAMS---" or match=="---MATCHES---":
            from resources.cal_dialog import Ui_Dialog
            class Dialog(QtWidgets.QDialog, Ui_Dialog):
                def __init__(self, parent=None):
                    QtWidgets.QDialog.__init__(self, parent)
                    self.setupUi(self)
                    
            nameDialog = Dialog()
            nameDialog.exec_()

#this part extracts the name of team players and displays them against their name
        else:
            sql="select players from teams where team_name='"+team_name+"';"
            player_cur.execute(sql)
            result=player_cur.fetchall()
            for record in result:
                ls=record[0].split(",")
                
                #if team length is less than 11 players then error will be raised
                if len(ls)<11:
                    from resources.team_diag import Ui_Dialog
                    class Dialog(QtWidgets.QDialog, Ui_Dialog):
                        def __init__(self, parent=None):
                            QtWidgets.QDialog.__init__(self, parent)
                            self.setupUi(self)
                    
                    teamDialog = Dialog()
                    teamDialog.exec_()
                    
                #when everything is fine score will be updated
                else:
                    self.LW1.addItems(ls)
                    for player in ls:
                        sql="select * from "+match+" where player_name = '"+player+"';"
                        player_cur.execute(sql)
                        result=player_cur.fetchall()
                        for record in result:
                            self.player_score(record)
            self.lcd1.display(self.team_score)

#this part adds entities in the team and matches menu
    def add_teams(self):
        self.combo1.addItem("---TEAMS---")
        self.combo2.addItem("---MATCHES---")
        sql="select team_name from teams;"
        player_cur.execute(sql)
        result=player_cur.fetchall()
        for record in result:
            self.combo1.addItem(record[0])
        sql="SELECT name FROM sqlite_master WHERE type='table';"
        player_cur.execute(sql)
        result=player_cur.fetchall()
        for record in result:
            if "match" in record[0]:
                self.combo2.addItem(record[0])
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(707, 705)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.B1 = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.B1.setFont(font)
        self.B1.setObjectName("B1")
        self.gridLayout_2.addWidget(self.B1, 5, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 5, 3, 1, 8)
        self.LW2 = QtWidgets.QListWidget(Form)
        self.LW2.setObjectName("LW2")
        self.gridLayout_2.addWidget(self.LW2, 4, 3, 1, 8)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.combo1 = QtWidgets.QComboBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.combo1.setFont(font)
        self.combo1.setObjectName("combo1")
        self.gridLayout.addWidget(self.combo1, 1, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 5, 1, 1)
        self.L1 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("LEMON MILK Bold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.L1.setFont(font)
        self.L1.setAlignment(QtCore.Qt.AlignCenter)
        self.L1.setObjectName("L1")
        self.gridLayout.addWidget(self.L1, 0, 0, 1, 6)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 3, 1, 1)
        self.combo2 = QtWidgets.QComboBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.combo2.setFont(font)
        self.combo2.setObjectName("combo2")
        self.gridLayout.addWidget(self.combo2, 1, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 10)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem4, 0, 11, 6, 1)
        self.LW1 = QtWidgets.QListWidget(Form)
        self.LW1.setObjectName("LW1")
        self.gridLayout_2.addWidget(self.LW1, 4, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 5, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 2, 1, 1, 10)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem7, 0, 0, 6, 1)
        self.line = QtWidgets.QFrame(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.line.setFont(font)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 1, 1, 10)
        self.L2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("LEMON MILK Bold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L2.setFont(font)
        self.L2.setObjectName("L2")
        self.gridLayout_2.addWidget(self.L2, 3, 1, 1, 1)
        self.L3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("LEMON MILK Bold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L3.setFont(font)
        self.L3.setObjectName("L3")
        self.gridLayout_2.addWidget(self.L3, 3, 3, 1, 1)
        self.lcd1 = QtWidgets.QLCDNumber(Form)
        self.lcd1.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcd1.sizePolicy().hasHeightForWidth())
        self.lcd1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lcd1.setFont(font)
        self.lcd1.setStyleSheet("color: rgb(0, 85, 255)")
        self.lcd1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd1.setDigitCount(4)
        self.lcd1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd1.setObjectName("lcd1")
        self.gridLayout_2.addWidget(self.lcd1, 3, 4, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem8, 4, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.add_teams()
        self.B1.clicked.connect(self.calculate_score)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Team Evaluation"))
        self.B1.setText(_translate("Form", "Calculate Score"))
        self.L1.setText(_translate("Form", "Evaluate the Performance of your Fantasy Team"))
        self.L2.setText(_translate("Form", "Players"))
        self.L3.setText(_translate("Form", "Points"))

#this part creates the Ui_form object and launches it to make a functioning GUI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

