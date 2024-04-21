import math
from PyQt5 import QtCore, QtGui, QtWidgets
from ButLeft import ButLeft
import ui_000,ui_001,ui_002,ui_010,ui_011,ui_012,ui_090,ui_092,ui_093,ui_094,ui_099
import glob
from FrameBase import RCroDBase,col
class Load(RCroDBase):
    qtimer = QtCore.QTimer()
    cont = 0
    def __init__(self):
        super().__init__()
        self.xmax=8
        self.ymax=8
        self.qtimer.timeout.connect(self.to)
        self.qtimer.start(100)

    def paintEvent(self,a0):
        self.paintBeg()
        self.drwCord()
        b=math.pi * 2 / 3
        # self.Line(0,0,3,math.radians(30),unlim=False)
        for i in range(0,360,2):
            z = math.pi/180*i
            self.Point(3- 4 * math.sin(z),z,5,col.cYellow,line=True)
            self.Point(3 - 8 * math.sin(z +b), z, 5,col.cOrange,line=True)
            self.Point(3 - 12 * math.sin(z + 2*b), z, 5, col.cGreen, line=True)
        z = math.pi / 180 *self.cont +math.pi/4
        self.Point(3 - 4 * math.sin(z),z, 10, col.cYellow2,line=True,cod=True)
        self.Point(3 - 8 * math.sin(z + b), z, 10, col.cOrange2,line=True,cod=True)
        self.Point(3 - 12 * math.sin(z + 2 * b), z, 5, col.cGreen2, line=True)
        # self.Text(r/2, z, 'r=5-4sin(z)',col=col.cgray2)
        self.cont = (self.cont+1)%360
        ft = self.font()
        ft.setPointSize(20)
        self.qp.setFont(ft)
        self.qp.drawText(self.x0-90,self.y0//5 ,"数理演示程序")
        self.paintEnd()
    def to(self):
       self.update()
    def __del__(self):
        self.qtimer.stop()
        supper().__del__()


class Ui_MainWindow(QtWidgets.QMainWindow):
    but={}
    uiclass = {}
    ucs = [ui_000,ui_001,ui_002,ui_010,ui_011,ui_012,ui_090,ui_092,ui_093,ui_094,ui_099]


    def btPress(self,name=''):

        for i in self.but:
            self.but[i].select = False
        self.but[name].select = True
        # print( self.uiclass[name])
        self.horizontalLayout.removeWidget(self.label)
        try: del self.label
        except : pass
        self.label = self.uiclass[name].Ui_Form(self.centralwidget)
        self.label.setupUi(self.label)
        self.horizontalLayout.addWidget(self.label)
        self.update()



    def add_but(self,name="Butt"):
        tbut = ButLeft(self.centralwidget)
        tbut.initBut(name)
        tbut.setMaximumWidth(150)
        tbut.setMinimumWidth(150)
        tbut.sig.connect(self.btPress)
        self.but[name] = tbut
        self.verticalLayout.addWidget(tbut)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 775)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.addLayout(self.verticalLayout)

        # 加载插件
        for i in self.ucs :
            try:
                tmp_frame = i.Ui_Form()
                tmp_frame.setupUi(tmp_frame)
                self.add_but(tmp_frame.name)
                self.uiclass[tmp_frame.name] = i
            except:pass


        self.label = Load()
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(0, 20)
        self.horizontalLayout.setStretch(1, 65535)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.btPress(self.but.keys()[0])


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "123"))
