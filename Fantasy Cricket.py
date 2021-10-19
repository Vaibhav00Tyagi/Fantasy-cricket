#importing required pyqt5 modules
from PyQt5 import QtCore, QtGui, QtWidgets

#connecting to our database and creating a cursor
import sqlite3
myplayer=sqlite3.connect("resources\Fantasy Cricket.db")            
player_cur=myplayer.cursor()                          
 #cursor to be used for importing and exporting data

#declaraing the Main Window class
class Ui_MainWindow(object):
    #available_points=1000
    used_points=0                 #initialising class attributes
    bat=0
    bowl=0
    ar=0
    wk=0

#function to reset the window 
    def initialize(self):                              
        self.centralwidget.setEnabled(True)
        self.bat=0
        self.bowl=0
        self.ar=0
        self.wk=0
        self.available_points=1000
        self.used_points=0
        self.lcd1.display(self.bat)
        self.lcd2.display(self.bowl)
        self.lcd3.display(self.ar)
        self.lcd4.display(self.wk)
        self.lcd5.display(self.available_points)
        self.lcd6.display(self.used_points)
        self.LW1.clear()
        self.LW2.clear()
        self.T1.clear()

#function to update the team value according to the player selected
    def update_point(self,item,ls):
        sql="select value from Stats where player_name ='"+item+"';"
        player_cur.execute(sql)
        result=player_cur.fetchall()
        for record in result:
            if ls==self.LW1:
                self.available_points-=record[0]
                self.used_points+=record[0]                #if player is selected
                self.lcd5.display(self.available_points)
                self.lcd6.display(self.used_points)
            else:
                self.available_points+=record[0]
                self.used_points-=record[0]                #if player is de-selected
                self.lcd5.display(self.available_points)
                self.lcd6.display(self.used_points)

#function to update the number of players selected in each category
    def update_number(self,item,ls):
        sql="select role from Stats where player_name ='"+item+"';"
        player_cur.execute(sql)
        result=player_cur.fetchall()
        for record in result:
            if record[0]=="batsman":                        #if batsman is selected
                if ls==self.LW1:
                    self.bat+=1
                else:
                    self.bat-=1
            if record[0]=="bowler":                         #if bowler is selected  
                if ls==self.LW1:
                    self.bowl+=1
                else:
                    self.bowl-=1
            if record[0]=="all-rounder":                    #if an all-rounder is selected
                if ls==self.LW1:
                    self.ar+=1
                else:
                    self.ar-=1
            if record[0]=="wicket-keeper":                  #if wicket-keeper is selected 
                if ls==self.LW1:
                    self.wk+=1
                else:
                    self.wk-=1
        self.lcd1.display(self.bat)
        self.lcd2.display(self.bowl)                        #updating counter of categories
        self.lcd3.display(self.ar)
        self.lcd4.display(self.wk)

#function to determine the category of players to be showen in the available players list          
    def checkstate(self):
        self.LW1.clear()
        if self.R1.isChecked()==True:
            self.role="batsman"
            
        if self.R2.isChecked()==True:
            self.role="bowler"
            
        if self.R3.isChecked()==True:
            self.role="all-rounder"
            
        if self.R4.isChecked()==True:
            self.role="wicket-keeper"
        self.list_item()

#function to sort players and make them exclusive in available players list
#it checks if the player is selected or not 
    def list_item(self):
        sql="select player_name from Stats where role='"+self.role+"';"
        player_cur.execute(sql)
        result=player_cur.fetchall()
        
        for record in result:
            flag=1
            if self.LW2.count()>0:
                for i in range(self.LW2.count()):
                    if self.LW2.item(i).text() == record[0]:
                        flag=0
                        break
            if flag==1:
                self.LW1.addItem(record[0])

#function to add players in selected player list, according to the team selected by user in open menu
    def open_team(self,item):
        self.T1.setText(item)
        sql="select * from teams where team_name='"+item+"';"
        player_cur.execute(sql)
        result=player_cur.fetchall()
        for record in result:
            ls=record[1].split(",")
            self.available_points=1000-record[2]
            self.used_points=record[2]
            self.LW2.addItems(ls)
            self.lcd5.display(self.available_points)
            self.lcd6.display(self.used_points)
            for player in ls:
                self.update_number(player,self.LW1)

#function to ask for name of the team
    def new_team(self):
        from resources.namediag import Ui_Dialog
        class Dialog(QtWidgets.QDialog, Ui_Dialog):
            def __init__(self, parent=None):
                QtWidgets.QDialog.__init__(self, parent)
                self.setupUi(self)
                self.lineEdit.clear()
                    
        nameDialog = Dialog()
        nameDialog.exec_()
        text=nameDialog.lineEdit.text()
        self.T1.setText(text)

#function to check whether a team with same name pre-exists or not
    def name_check(self,text,points,players):
        sql="select team_name from teams;"
        player_cur.execute(sql)
        result=player_cur.fetchall()
        for record in result:
            if text==record[0]:
                from resources.save_dialog import Ui_Dialog
                class Dialog(QtWidgets.QDialog, Ui_Dialog):
                    def same_name(self,players,points):
                        sql="update teams set players='"+players+"',team_value="+str(points)+" where team_name ='"+text+"';"
                        player_cur.execute(sql)
                        myplayer.commit()
                    def __init__(self, parent=None):
                        QtWidgets.QDialog.__init__(self, parent)
                        self.setupUi(self)
                        self.B1.clicked.connect(lambda:self.same_name(players,points))
                    
                saveDialog = Dialog()
                saveDialog.exec_()
                return 1
        else:
            return 0
        
#function defining the working of menu 
    def menufunction(self,action):
        
        #if new-team action is selected then control reaches here 
        if action.text()== "New Team":
            self.initialize()
            self.new_team()
            
        #if open-team action is selected this is executed
        if action.text()== "Open Team":
            self.initialize()
            self.centralwidget.setEnabled(True)
            from resources.open_diag import Ui_Dialog
            class Dialog(QtWidgets.QDialog, Ui_Dialog):
                def __init__(self, parent=None):
                    QtWidgets.QDialog.__init__(self, parent)
                    self.setupUi(self)
                    sql="select team_name from teams;"
                    player_cur.execute(sql)
                    result=player_cur.fetchall()
                    for record in result:
                        self.LW1.addItem(record[0])
            openDialog = Dialog()
            openDialog.exec_()
            
            item=openDialog.LW1.selectedItems()
            if len(item)>0:
                text=item[0].text()
                self.open_team(text)
        
        #if save-team action is selected this is executed
        if action.text()== "Save Team":
            text=[]
            flag=0
            points=self.used_points
            
            for i in range(self.LW2.count()):
                text.append(self.LW2.item(i).text())
            players=",".join(text)
            
            text=self.T1.text()
            
            if len(text)==0:
                flag=2
                self.new_team()
            else:
                flag=self.name_check(text,points,players)
            
            if flag==0:
                sql="insert into teams values ('"+self.T1.text()+"','"+players+"',"+str(self.used_points)+");"
                player_cur.execute(sql)
                myplayer.commit()
                self.initialize()
        
        #if evaluate team action is selected this is executed 
        if action.text()== "Evaluate Team":
            self.initialize()
            from resources.evaluate import Ui_Form
            Form = QtWidgets.QDialog()
            ui = Ui_Form()
            ui.setupUi(Form)
            Form.show()
            Form.exec_()
        
        #if Quit action is choosen then control reaches here
        if action.text()== "Quit":
            from resources.quit_diag import Ui_Dialog
            class Dialog(QtWidgets.QDialog, Ui_Dialog):
                def __init__(self, parent=None):
                    QtWidgets.QDialog.__init__(self, parent)
                    self.setupUi(self)
                    self.pushButton.clicked.connect(MainWindow.close)
                    
            quitDialog = Dialog()
            quitDialog.exec_()

#this function moves players from available players list to selected players
    def removelist1(self, item):
        
        #this part checks if wicket-keeper criteria is maintained
        if self.wk>=1 and self.R4.isChecked()==True:
            from resources.wk_dialog import Ui_Dialog
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.show()
            Dialog.exec_()
        
        #this part adds the players to selected players list if a valid selection is made
        elif len(self.LW2)<11 and self.available_points>45:
             self.LW1.takeItem(self.LW1.row(item))
             self.LW2.addItem(item.text())
             self.update_point(item.text(),self.LW1)
             self.update_number(item.text(),self.LW1)
             
        #this part prompts if selection criteria is violated
        else:
            from resources.teamfull import Ui_Dialog
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.show()
            Dialog.exec_()

#this function moves player to available player list, when a de-selection is made
    def removelist2(self, item):
        self.LW2.takeItem(self.LW2.row(item))
        self.LW1.addItem(item.text())
        self.update_point(item.text(),self.LW2)
        self.update_number(item.text(),self.LW2)

#this part creates the interface of the Main-Window along with its resources
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1055, 891)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources\img2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 3, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 3, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 2, 2, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.L3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L3.setFont(font)
        self.L3.setObjectName("L3")
        self.gridLayout.addWidget(self.L3, 1, 4, 2, 1)
        self.L4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L4.setFont(font)
        self.L4.setObjectName("L4")
        self.gridLayout.addWidget(self.L4, 1, 7, 2, 1)
        self.L5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L5.setFont(font)
        self.L5.setObjectName("L5")
        self.gridLayout.addWidget(self.L5, 1, 10, 2, 1)
        self.lcd2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcd2.setDigitCount(2)
        self.lcd2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd2.setObjectName("lcd2")
        self.gridLayout.addWidget(self.lcd2, 1, 5, 2, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 6, 1, 1)
        self.lcd3 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcd3.setDigitCount(2)
        self.lcd3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd3.setObjectName("lcd3")
        self.gridLayout.addWidget(self.lcd3, 1, 8, 2, 1)
        self.L1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L1.sizePolicy().hasHeightForWidth())
        self.L1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("LEMON MILK")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.L1.setFont(font)
        self.L1.setStyleSheet("background-color: rgb(44, 199, 255)")
        self.L1.setObjectName("L1")
        self.gridLayout.addWidget(self.L1, 0, 1, 1, 12)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 2, 9, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 2, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 2, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem8, 2, 13, 1, 1)
        self.lcd1 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd1.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcd1.setDigitCount(2)
        self.lcd1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd1.setObjectName("lcd1")
        self.gridLayout.addWidget(self.lcd1, 1, 2, 2, 1)
        self.L2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L2.setFont(font)
        self.L2.setObjectName("L2")
        self.gridLayout.addWidget(self.L2, 1, 1, 2, 1)
        self.lcd4 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd4.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcd4.setDigitCount(2)
        self.lcd4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd4.setObjectName("lcd4")
        self.gridLayout.addWidget(self.lcd4, 1, 11, 2, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 2, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem9, 1, 15, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem10, 1, 2, 1, 1)
        self.T1 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.T1.sizePolicy().hasHeightForWidth())
        self.T1.setSizePolicy(sizePolicy)
        self.T1.setObjectName("T1")
        self.gridLayout_2.addWidget(self.T1, 1, 14, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem11, 1, 4, 1, 1)
        self.L7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L7.setFont(font)
        self.L7.setObjectName("L7")
        self.gridLayout_2.addWidget(self.L7, 0, 10, 1, 3)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem12, 1, 13, 1, 1)
        self.LW1 = QtWidgets.QListWidget(self.centralwidget)
        self.LW1.setObjectName("LW1")
        self.gridLayout_2.addWidget(self.LW1, 2, 0, 1, 8)
        self.R1 = QtWidgets.QRadioButton(self.centralwidget)
        self.R1.setObjectName("R1")
        self.gridLayout_2.addWidget(self.R1, 1, 1, 1, 1)
        self.R3 = QtWidgets.QRadioButton(self.centralwidget)
        self.R3.setObjectName("R3")
        self.gridLayout_2.addWidget(self.R3, 1, 5, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem13, 1, 11, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem14, 1, 6, 1, 1)
        self.L8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.L8.setFont(font)
        self.L8.setObjectName("L8")
        self.gridLayout_2.addWidget(self.L8, 1, 12, 1, 1)
        self.arrow = QtWidgets.QLabel(self.centralwidget)
        self.arrow.setText("")
        self.arrow.setPixmap(QtGui.QPixmap("resources\img.png"))
        self.arrow.setObjectName("arrow")
        self.gridLayout_2.addWidget(self.arrow, 2, 8, 1, 1)
        self.lcd5 = QtWidgets.QLCDNumber(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("LEMON MILK Bold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.lcd5.setFont(font)
        self.lcd5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd5.setSmallDecimalPoint(False)
        self.lcd5.setDigitCount(4)
        self.lcd5.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd5.setProperty("intValue", 1000)
        self.lcd5.setObjectName("lcd5")
        self.gridLayout_2.addWidget(self.lcd5, 0, 4, 1, 1)
        self.R2 = QtWidgets.QRadioButton(self.centralwidget)
        self.R2.setObjectName("R2")
        self.gridLayout_2.addWidget(self.R2, 1, 3, 1, 1)
        self.R4 = QtWidgets.QRadioButton(self.centralwidget)
        self.R4.setObjectName("R4")
        self.gridLayout_2.addWidget(self.R4, 1, 7, 1, 1)
        self.L6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.L6.setFont(font)
        self.L6.setObjectName("L6")
        self.gridLayout_2.addWidget(self.L6, 0, 0, 1, 4)
        self.LW2 = QtWidgets.QListWidget(self.centralwidget)
        self.LW2.setObjectName("LW2")
        self.gridLayout_2.addWidget(self.LW2, 2, 9, 1, 7)
        self.lcd6 = QtWidgets.QLCDNumber(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("LEMON MILK Bold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.lcd6.setFont(font)
        self.lcd6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd6.setDigitCount(4)
        self.lcd6.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd6.setProperty("intValue", 0)
        self.lcd6.setObjectName("lcd6")
        self.gridLayout_2.addWidget(self.lcd6, 0, 13, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 2, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem15, 3, 1, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem16, 3, 3, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem17, 4, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1055, 26))
        self.menubar.setObjectName("menubar")
        self.menuManage_Teams = QtWidgets.QMenu(self.menubar)
        self.menuManage_Teams.setObjectName("menuManage_Teams")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Team = QtWidgets.QAction(MainWindow)
        self.actionNew_Team.setObjectName("actionNew_Team")
        self.actionOpen_Team = QtWidgets.QAction(MainWindow)
        self.actionOpen_Team.setObjectName("actionOpen_Team")
        self.actionSave_Team = QtWidgets.QAction(MainWindow)
        self.actionSave_Team.setObjectName("actionSave_Team")
        self.actionEvaluate_Team = QtWidgets.QAction(MainWindow)
        self.actionEvaluate_Team.setObjectName("actionEvaluate_Team")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuManage_Teams.addAction(self.actionNew_Team)
        self.menuManage_Teams.addAction(self.actionOpen_Team)
        self.menuManage_Teams.addAction(self.actionSave_Team)
        self.menuManage_Teams.addAction(self.actionEvaluate_Team)
        self.menuManage_Teams.addAction(self.actionQuit)
        self.menubar.addAction(self.menuManage_Teams.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #this connects the actions triggered in main menu to menufunction
        self.menuManage_Teams.triggered[QtWidgets.QAction].connect(self.menufunction)
        
        #these 2 statements moves players across two lists on double-clicking
        self.LW1.itemDoubleClicked.connect(self.removelist1)
        self.LW2.itemDoubleClicked.connect(self.removelist2)
        
        #these 4 statements connect to checkstate function on toggling with radio-buttons
        self.R1.toggled.connect(self.checkstate)
        self.R2.toggled.connect(self.checkstate)
        self.R3.toggled.connect(self.checkstate)
        self.R4.toggled.connect(self.checkstate)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fantasy Cricket"))
        self.L3.setText(_translate("MainWindow", "Bowlers (BOWL)"))
        self.L4.setText(_translate("MainWindow", "Allrounders (AR)"))
        self.L5.setText(_translate("MainWindow", "Wicket-Keeper (WK)"))
        self.L1.setText(_translate("MainWindow", "YOUR SELECTIONS :"))
        self.L2.setText(_translate("MainWindow", "Batsmen (BAT)"))
        self.L7.setText(_translate("MainWindow", "Points Used"))
        self.R1.setText(_translate("MainWindow", "BAT"))
        self.R3.setText(_translate("MainWindow", "AR"))
        self.L8.setText(_translate("MainWindow", "Team Name"))
        self.R2.setText(_translate("MainWindow", "BOW"))
        self.R4.setText(_translate("MainWindow", "WK "))
        self.L6.setText(_translate("MainWindow", "Points Available"))
        self.menuManage_Teams.setTitle(_translate("MainWindow", "Manage Teams"))
        self.actionNew_Team.setText(_translate("MainWindow", "New Team"))
        self.actionOpen_Team.setText(_translate("MainWindow", "Open Team"))
        self.actionSave_Team.setText(_translate("MainWindow", "Save Team"))
        self.actionEvaluate_Team.setText(_translate("MainWindow", "Evaluate Team"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

#this part creates the mainWindow object and launches it to make a functioning GUI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

#this closes the connection with the Fantasy Cricket database
myplayer.close()
