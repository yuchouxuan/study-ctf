
from FrameBase import  *

class Ghp(QtWidgets.QLabel):
    alpha = math.radians(2)
    alphad = 2
    lx = 0
    r = 10
    qpen0 = QtGui.QPen(col.cw,2,qt.SolidLine,qt.FlatCap)
    qpen1 = QtGui.QPen(col.cw, 1,qt.DashDotLine, qt.FlatCap)
    qpin  = QtGui.QPen(col.cGreen3, 2,qt.SolidLine, qt.FlatCap)
    qpout = QtGui.QPen(col.cGreen2, 2, qt.SolidLine, qt.FlatCap)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        w = self.width()-5
        h = self.height()-3
        o = (0,int(h))

        if w * math.tan(self.alpha) <= (h -40):
            lp = w, w * math.tan(self.alpha)
        else:
            lp = (h-40)/ math.tan(self.alpha),h-40

        p0 =  QtCore.QPoint(*o) #起点
        p1 =  QtCore.QPoint(int(lp[0]),int(h-lp[1])) # 高点
        p2 =  QtCore.QPoint(int(lp[0]),int(h)) #右点
        mb = QtGui.QPolygon([p0,p1,p2])

        x = lp[0] * self.lx+5
        y = x * math.tan(self.alpha)
        x -= self.r * math.sin(self.alpha)
        y += self.r * math.cos(self.alpha)
        x = int(lp[0]-x)
        y = int(h - lp[1]+y)-self.r*2

        qp = myPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QBrush(qt.white,qt.SolidPattern))
        qp.drawPolygon(mb)
        pen = QtGui.QPen(col.cGreen3,5,qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(col.cGreen3)
        qp.drawEllipse(x-self.r,y-self.r ,self.r*2-2,self.r * 2-2)

        qp.drawText(20,40,"Deg=%d°"%self.alphad)
        qp.drawText(20,70,"S={:7.3f}m".format(self.lx*20))

        dy = lp[1] / 10
        dx = lp[0] / 10
        pts = [(o[0] + dx * i,  o[1] - dy * i+3) for i in range(10)][::-1]

        penr = QtGui.QPen(qt.black, 5, qt.SolidLine,qt.RoundCap)
        pen = QtGui.QPen(qt.red, 5, qt.SolidLine,qt.RoundCap)
        qp.setPen(pen)
        for i in range(10):
            if (i+1) / 10 > self.lx:
                qp.setPen(penr)
            qp.drawPoint(*pts[i])

        qp.end()
        super(Ghp, self).paintEvent(a0)
    pass


class Ui_Form(FrameBase):
    def setupUi(self, Form):
        self.name='运动-斜面'
        Form.setObjectName("Form")
        Form.resize(992, 748)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.m_img = Ghp(Form)
        self.m_img.setObjectName("m_img")
        self.horizontalLayout_2.addWidget(self.m_img)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_2.addWidget(self.line_3)
        self.ang = QtWidgets.QSlider(Form)
        self.ang.setMinimum(2)
        self.ang.setMaximum(30)
        self.ang.setOrientation(QtCore.Qt.Vertical)
        self.ang.setObjectName("ang")
        self.horizontalLayout_2.addWidget(self.ang)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.time = QtWidgets.QSlider(Form)
        self.time.setMaximum(100)
        self.time.setOrientation(QtCore.Qt.Horizontal)
        self.time.setObjectName("time")
        self.horizontalLayout.addWidget(self.time)
        self.lcd = QtWidgets.QLCDNumber(Form)
        self.lcd.setDigitCount(7)
        self.lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd.setObjectName("lcd")
        self.horizontalLayout.addWidget(self.lcd)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.table = QtWidgets.QTextBrowser(Form)
        self.table.setObjectName("table")
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.run_but) # type: ignore
        self.ang.valueChanged.connect(self.update)
        self.time.valueChanged.connect(self.update)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.l = 20
        self.qtimer = QTimer()
        self.qtimer.timeout.connect(self.run_timeer)
        self.alpha = math.radians(self.ang.value())
        self.a = 9.8* math.sin(self.alpha)
        self.timeAll = math.sqrt(2*self.l/self.a)


    def run_timeer(self):
        if self.time.value()==100:
            self.qtimer.stop()
        else:
            self.time.setValue(self.time.value()+1)
            self.update()
    def run_but(self):
        dt = int(self.timeAll / 100*1000)
        self.time.setValue(0)
        self.qtimer.start(dt)


    def update(self):
        self.alpha = math.radians(self.ang.value())
        self.m_img.alphad = self.ang.value()
        self.a = 9.8* math.sin(self.alpha)
        self.timeAll = math.sqrt(2*self.l/self.a)
        self.timeNow = self.timeAll /100 * self.time.value()
        self.lcd.setProperty("value", self.timeNow)

        sout = "计时数据：\n"
        sout += '- ' *26 +'\n'
        format = '{:4} | {:10} | {:10} | {:10} |\n'
        sout += format.format('编号','距离','时间','速度')
        timelist = [ math.sqrt(2*self.l*i/10/self.a) for  i in range(1,11)]
        sout += '- ' * 26 + '\n'

        format = '{:6} | {:-11.3f}m | {:-11.3f}s | {:-9.3f}m/s |\n'
        for i in range(len(timelist)):
            if self.timeNow >= timelist[i] :
                sout += format.format(i+1, self.l*(i+1)/10,timelist[i], timelist[i]*self.a)
                sout += '- ' * 26 + '\n'
        self.table.setText(sout)

        self.m_img.alpha = self.alpha
        self.m_img.lx =  self.a * self.timeNow**2 /2 / self.l




        super(Ui_Form, self).update()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        # self.m_img.setText(_translate("Form", "TextLabel"))
        self.label_2.setText(_translate("Form", "时间线："))
        self.pushButton.setText(_translate("Form", "Run"))
