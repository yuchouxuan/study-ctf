from FrameBase import  *
import math
class Ghp(QtWidgets.QLabel):

    qpen0 = QtGui.QPen(col.cw,2,qt.SolidLine,qt.FlatCap)
    qpen1 = QtGui.QPen(col.cw, 1,qt.DashDotLine, qt.FlatCap)
    qpin  = QtGui.QPen(col.cGreen3, 2,qt.SolidLine, qt.FlatCap)
    qpout = QtGui.QPen(col.cGreen2, 2, qt.SolidLine, qt.FlatCap)
    tim=0
    vx0 =0
    vy0=0
    g=9.8

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        r = 5
        w = self.width()
        dp = w /130
        h = self.height()
        qp = myPainter()
        qp.begin(self)

        qp.drawRect(0,0,w,h)
        pen = QtGui.QPen(col.cgray3,3)
        qp.setPen(pen)
        for i in range(self.tim+1):
            ta = self.vy0 / self.g *2
            tn = ta/100*i
            vx = self.vx0
            vy = self.vy0 - self.g * tn
            x = vx*tn *dp +5
            y = h - (self.vy0 * tn - self.g * tn**2 /2) *dp   -5
            qp.drawPoint(x,y)
        qp.setBrush(qt.white)
        qp.drawEllipse(x-r,y-r,r*2,r*2)
        qp.setBrush(col.cgray3)
        qp.setPen(col.cgray3)
        qp.drawRect(w -200 , 20 , 150,20)
        qp.drawRect(w - 200, 50, 150, 20)
        qp.drawRect(w -200 , 80 , 150,20)
        qp.drawRect(w - 200, 110, 150, 20)
        qp.drawRect(w - 200, 140, 150, 20)
        qp.setPen(qt.black)
        qp.drawText(w -180 ,35 ,  'X:    %10.5fm'%(vx*tn *dp))
        qp.drawText(w - 180, 65,  'Y:    %10.5fm' % (self.vy0 * tn - self.g * tn**2 /2))
        qp.drawText(w - 180, 95,  'Vx:   %8.3fm/s' % (vx))
        qp.drawText(w - 180, 125, 'Vy:   %8.3fm/s' % (vy))
        qp.drawText(w - 180, 155, 'Time: %10.5fs' % (tn))

        gpen = QtGui.QPen(col.cGreen, 1)
        qp.setPen(gpen)
        qp.drawLine(x,y,x +vx*5 ,y ,arror=2)
        qp.drawLine(x, y, x , y - vy*5, arror=2)
        rpen = QtGui.QPen(qt.red, 1)
        qp.setPen(rpen)
        qp.drawLine(x, y, x +vx*5, y - vy * 5, arror=2)

        qp.end()
        super(Ghp, self).paintEvent(a0)
    pass
class Ui_Form(FrameBase):
    name="运动-斜抛运动"
    g = 9.8
    auto = False
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1016, 775)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 =Ghp(Form)
        self.label_3.setMinimumSize(QtCore.QSize(500, 500))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.r_ang = QtWidgets.QDial(Form)
        self.r_ang.setMinimum(1)
        self.r_ang.setMaximum(900)
        self.r_ang.setValue(450)
        self.r_ang.setObjectName("r_ang")
        self.verticalLayout_2.addWidget(self.r_ang)
        self.l_ang = QtWidgets.QLCDNumber(Form)
        self.l_ang.setDigitCount(7)
        self.l_ang.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.l_ang.setObjectName("l_ang")
        self.verticalLayout_2.addWidget(self.l_ang)
        self.line = QtWidgets.QFrame(Form)
        self.line.setMinimumSize(QtCore.QSize(0, 80))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.r_v = QtWidgets.QDial(Form)
        self.r_v.setMinimum(1)
        self.r_v.setMinimumWidth(100)
        self.r_v.setMaximum(1000)
        self.r_v.setValue(500)
        self.r_v.setObjectName("r_v")
        self.verticalLayout_2.addWidget(self.r_v)
        self.l_v = QtWidgets.QLCDNumber(Form)
        self.l_v.setDigitCount(7)
        self.l_v.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.l_v.setObjectName("l_v")
        self.verticalLayout_2.addWidget(self.l_v)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.pushButton = ButLight(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 80))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.setStretch(7, 100)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 100)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.time = QtWidgets.QSlider(Form)
        self.time.setOrientation(QtCore.Qt.Horizontal)
        self.time.setObjectName("time")
        self.time.setMaximum(100)
        self.verticalLayout_3.addWidget(self.time)
        self.verticalLayout_3.setStretch(0, 100)
        self.r_ang.valueChanged.connect(self.reBuild)
        self.r_v.valueChanged.connect(self.reBuild)
        self.time.valueChanged.connect(self.reBuild)
        self.label_3.g=self.g
        self.pushButton.clicked.connect(self.run)
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.timerup)
        self.reBuild()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def reBuild(self):
        g=self.g
        v = self.r_v.value()/20
        a = self.r_ang.value()/10
        self.l_v.setProperty('value',v)
        self.l_ang.setProperty('value',a)
        vx = v * math.cos(math.radians(a))
        vy = v * math.sin(math.radians(a))
        self.label_3.vx0 = vx
        self.label_3.vy0 = vy
        self.label_3.tim = self.time.value()
        self.update()

    def timerup(self):
        if self.time.value() <100:
            self.time.setValue(self.time.value()+1)
            self.reBuild()
        else:
            self.Timer.stop()
            self.auto = False
            self.pushButton.select = False
            self.pushButton.update()

    def run(self):
        if not self.auto :
            a = self.r_v.value() *2.5
            self.time.setValue(0)
            self.Timer.start(int(a//50))
            self.pushButton.select = True
            self.auto=True

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "角度"))
        self.label_2.setText(_translate("Form", "初速度"))
        self.label_5.setText(_translate("Form", " "))
        self.pushButton.setText(_translate("Form", "RUN"))
        self.label_4.setText(_translate("Form", "时间线"))
