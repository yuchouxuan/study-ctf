import math
from FrameBase import  *

class Ghp(QtWidgets.QLabel):
    ang=0
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        w = self.width()
        h = self.height()
        qp = myPainter()
        qp.begin(self)
        r = h / 6
        pen = QtGui.QPen(col.cGreen,1,qt.SolidLine,qt.FlatCap)
        qp.setPen(pen)
        x10 = 10+r
        y10 = r+20
        xStart =  x10*2 +50 # 右侧坐标轴起点
        x_range = (w - xStart)/2 # 右侧坐标轴范围(半轴)
        y20 = r + 20
        x20 = xStart + x_range


        x30 = x20
        y30 = h - 20 - r
        dx = x_range/math.pi/2

        #单位圆坐标轴
        qp.drawLine(0,r+20,r*2+50 ,r+20 ,arror=2)
        qp.drawText(r * 2  , r + 30, '1')
        qp.drawText(10, r + 30, '-1')
        qp.drawText( r*2+45 ,r+30 ,'x')
        qp.drawLine(r+10, y30 - r , r+10, 0, arror=2)
        qp.drawText(r+15, 10 ,'y')
        qp.drawText(r + 15, 20, '1')
        qp.drawText(r + 15, r*2+10, '-1')

        #右侧坐标轴 sin
        qp.drawLine(xStart,y20,w,y20,arror=2)
        qp.drawLine(xStart+x_range, y20+r+30, xStart+x_range , 0, arror=2)

        #下方坐标轴 cos
        qp.drawLine(xStart, y30, w, y30, arror=2)
        qp.drawLine(xStart + x_range,h, xStart + x_range, y30-r-30, arror=2)

        #曲线
        pen = QtGui.QPen(col.cgray2,3,qt.SolidLine,qt.FlatCap)
        qp.setPen(pen)
        for i in range(0,720,3):
            alpha = (i-360)/180 *math.pi
            qp.drawPoint(dx*alpha + x20, y20 - math.sin(math.radians(i))*r  )
            qp.drawPoint(dx * alpha + x30, y30 - math.cos(math.radians(i)) * r)


        #单位圆
        pen = QtGui.QPen(col.cgray3,3,qt.SolidLine,qt.FlatCap)
        qp.setPen(pen)
        qp.drawArc(10,20,2*r,2*r,0,360*16)

        # 箭头
        pen = QtGui.QPen(col.cRed2, 3, qt.SolidLine, qt.FlatCap)
        qp.setPen(pen)
        qp.drawLine(x10,y10, x10+r*math.cos(self.ang),y10-r*math.sin(self.ang) ,arror=2)
        # 大点
        pen = QtGui.QPen(col.cRed3, 6, qt.SolidLine, qt.RoundCap)
        qp.setPen(pen)
        qp.drawPoint(dx*self.ang + x20, y10-r*math.sin(self.ang))
        qp.drawPoint(dx * self.ang + x20, y30 - r * math.cos(self.ang))

        #绿色虚线
        pen = QtGui.QPen(col.cGreen2, 1, qt.DotLine, qt.FlatCap)
        qp.setPen(pen)
        qp.drawLine(x10,y10-r*math.sin(self.ang),dx*self.ang + x20, y10-r*math.sin(self.ang))
        rl = r * (1 - math.cos(self.ang))
        qp.drawLine(x10+r*math.cos(self.ang), y30-r+rl/2,  x10+r*math.cos(self.ang),y10-r*math.sin(self.ang))
        qp.drawLine(x10+r/2,y30 , xStart,y30)
        qp.drawLine(x10 , y30-r/2, x10, y30-2*r)
        qp.drawArc(x10 + r * math.cos(self.ang), y30 -  r, rl, rl, 180 * 16, 90 * 16)
        qp.drawArc(x10, y30 - r, r, r, 180 * 16, 90 * 16)
        qp.drawLine(x10 + r * math.cos(self.ang) + math.fabs(rl)/2 , y30 - r * math.cos(self.ang), dx * self.ang + x20, y30 - r * math.cos(self.ang))



        #红色虚线
        pen = QtGui.QPen(col.cRed3, 1, qt.DotLine, qt.FlatCap)
        qp.setPen(pen)
        qp.drawLine(x10,  y10 - r * math.sin(self.ang), x10 + r * math.cos(self.ang), y10 - r * math.sin(self.ang))
        qp.drawLine(x10 + r * math.cos(self.ang), y10, x10 + r * math.cos(self.ang), y10 - r * math.sin(self.ang))
        qp.drawLine(dx * self.ang + x20, y20, dx * self.ang + x20, y20 - r * math.sin(self.ang))
        qp.drawLine(dx * self.ang + x20, y30 - r * math.cos(self.ang),dx * self.ang + x20, y30 )


        qp.end()
        super(Ghp, self).paintEvent(a0)
    pass


class Ui_Form(FrameBase):
    name = "数学-三角函数"
    ang = 0
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1060, 787)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.img1 = Ghp(Form)
        self.img1.setMinimumSize(QtCore.QSize(400, 300))
        self.img1.setText("")
        self.img1.setObjectName("img1")
        self.horizontalLayout.addWidget(self.img1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.r_d = QtWidgets.QDial(Form)
        self.r_d.setMinimum(-360)
        self.r_d.setMaximum(360)
        self.r_d.setValue(0)
        self.r_d.setPageStep(1)
        self.r_d.setTracking(False)
        self.r_d.setOrientation(QtCore.Qt.Horizontal)
        self.r_d.setInvertedAppearance(False)
        self.r_d.setInvertedControls(False)
        self.r_d.setWrapping(True)
        self.r_d.setObjectName("r_d")
        self.verticalLayout.addWidget(self.r_d)
        self.l_deg = QtWidgets.QLCDNumber(Form)
        self.l_deg.setMinimumSize(QtCore.QSize(0, 0))
        self.l_deg.setDigitCount(7)
        self.l_deg.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.l_deg.setObjectName("l_deg")
        self.verticalLayout.addWidget(self.l_deg)
        self.line = QtWidgets.QFrame(Form)
        self.line.setMinimumSize(QtCore.QSize(0, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.l_sin = QtWidgets.QLCDNumber(Form)
        self.l_sin.setDigitCount(7)
        self.l_sin.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.l_sin.setObjectName("l_sin")
        self.verticalLayout.addWidget(self.l_sin)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.l_cos = QtWidgets.QLCDNumber(Form)
        self.l_cos.setDigitCount(7)
        self.l_cos.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.l_cos.setObjectName("l_cos")
        self.verticalLayout.addWidget(self.l_cos)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setMinimumSize(QtCore.QSize(0, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.bt1 =ButLight(Form)
        self.bt1.setMinimumSize(QtCore.QSize(60, 80))
        self.bt1.setObjectName("bt1")
        self.verticalLayout.addWidget(self.bt1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.verticalLayout.setStretch(10, 100)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1000)

        self.retranslateUi(Form)
        self.r_d.valueChanged.connect(self.vc)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.timerup)
        self.bt1.clicked.connect(self.btdown)
        self.vc()
    def btdown(self):
        if not self.bt1.select :
            self.bt1.select = True
            self.Timer.start(50)
        else :
            self.bt1.select = False
            self.Timer.stop()
        self.update()

    def timerup(self):
        self.r_d.setValue(self.r_d.value()+5)
        self.vc()


    def vc(self):
        self.ang = self.r_d.value()
        ra = math.pi / 180 *self.ang
        self.l_deg.setProperty('value', self.ang)
        self.l_sin.setProperty('value', math.sin(ra))
        self.l_cos.setProperty('value', math.cos(ra))
        self.img1.ang = ra
        self.update()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "角度 x"))
        self.label_2.setText(_translate("Form", "正弦 sin(x)"))
        self.label_3.setText(_translate("Form", "余弦 cos(x)"))
        self.bt1.setText(_translate("Form", "RUN"))
