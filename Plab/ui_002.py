from FrameBase import  *
import numpy as np
class Ghp(CroDBase):
    angs = 0
    angn=0
    E0=0
    g=9.8
    l=10
    t=0
    dt =100
    steps=None
    def co(self):
        pts = 2000
        ang = np.linspace( np.radians(self.angs),0,pts )
        dang = ang[-2]
        K = 2*self.g / self.l
        t= dang / np.sqrt(K*(np.cos(ang[1:])-np.cos(np.radians(self.angs))))
        dt = sum(t)/100
        self.dt = dt *1000
        self.steps =[self.angs]
        sut = 0
        cont = 0
        for i in range(100):
            timen = i * dt
            while sut < timen:
                sut += t[cont]
                cont +=1
            self.steps.append(self.angs-np.degrees(cont*dang))
        for i in self.steps[::-1]:
            self.steps.append(-i)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = self.paintBeg()
        qp.setPen(col.cgray)
        w = self.width()
        h =  self.height() -20
        ox = w//2
        oy = 20
        qp.drawRect(0,0,self.width(),self.height())

        pen = QtGui.QPen(col.cw3, 10,qt.SolidLine,qt.RoundCap)
        qp.setPen(pen)
        qp.drawPoint(ox, oy)
        pen = QtGui.QPen(col.cw3, 2, qt.SolidLine, qt.RoundCap)
        qp.setPen(pen)

        ang = 0
        if self.t < 200 :
            ang =self.steps[self.t]
        else :
            ang = self.steps[399-self.t]
        ang = np.radians(ang)
        l = (min(ox,h) )/10 * self.l -20
        rpx = ox + l*np.sin(ang)
        rpy = oy + l*np.cos(ang)
        qp.drawLine(ox,oy,rpx,rpy)
        pen.setColor(qt.red)

        qp.setPen(QtGui.QPen(col.cgray3,1,qt.DashLine))
        qp.drawLine(ox, 0, ox,oy+l )
        qp.setPen(qt.yellow)
        qp.drawArc(ox-l/4,oy-l/4,l/2,l/2,270*16,np.degrees(ang)*16)

        qp.drawText(ox-40,oy+l/8+8 ,f'β={np.degrees(ang):5.2f}°')

        qp.setPen(pen)
        qp.setBrush(col.cRed3)
        qp.drawEllipse(rpx-10,rpy-10,20,20)

        h = self.l-self.l*np.cos(ang)
        h0= self.l -self.l*np.cos(np.radians(self.angs))
        dh = h0 -h

        v = np.sqrt(2*self.g*dh)
        qp.setPen(col.cYellow3)
        qp.translate(rpx, rpy)
        qp.rotate(-np.degrees(ang))
        qp.drawText(-30, -15, f'v={v:5.3f}m/s')
        qp.resetTransform()

        qp.setPen(QtGui.QPen(col.cOrange3,4))

        vmax = l /20
        if self.t <= 200:
            qp.drawLine(rpx,rpy,rpx-np.cos(ang)*v*vmax,rpy+np.sin( ang)*v*vmax,arror=2)
        else:
            qp.drawLine(rpx, rpy, rpx + np.cos(ang)*v*vmax, rpy - np.sin( ang)*v*vmax,arror=2)

        pen = QtGui.QPen(col.cgray2, 1 )
        qp.setPen(pen)
        qp.drawLine(10, oy + l, w - 10, oy + l)

        pen = QtGui.QPen(col.cYellow3, 1, qt.DotLine, qt.RoundCap)
        qp.setPen(pen)
        qp.drawLine(60, rpy, rpx, rpy)
        qp.drawLine( 70, oy + l ,70, rpy,arror=2)
        qp.drawText(60,rpy-10,f'h={h:5.3f}m')

        Ea = v ** 2 / 2 + self.g * h
        Eg = self.g*h
        Ev = v**2 /2
        T=self.dt*0.402
        qp.setBrush(col.cgray3)
        qp.setPen(col.cgray3)
        qp.drawRect(w -180,10,150,20)
        qp.drawRect(w - 180, 40, 150, 20)
        qp.drawRect(w - 180, 70, 150, 20)
        qp.drawRect(w - 180, 100, 150, 20)
        qp.drawRect(w - 180, 130, 150, 20)
        qp.drawRect(w - 180, 160, 150, 20)
        qp.drawRect(w - 180, 190, 150, 20)
        qp.drawRect(w - 180, 220, 150, 20)
        qp.setBrush(col.cOrange2)
        qp.drawRect(w - 179, 192, 150*Eg/Ea, 16)
        qp.setBrush(col.cRed2)
        qp.drawRect(w - 179, 222, 150*Ev/Ea, 16)

        qp.setPen(qt.black)
        qp.drawText(w-170,25,    f'Time  :{self.dt*self.t/1000:7.3f}s')
        qp.drawText(w - 170, 55, f'Height:{h:7.3f}m')
        qp.drawText(w - 170, 85, f'v     :{v:7.3f}m/s')
        qp.drawText(w - 170, 115, f'Fenc  :{1/T:7.3f}Hz')
        qp.drawText(w - 170, 145, f'Peri  :{T:7.3f}s')
        qp.drawText(w - 170, 175, f'E     :{Ea:7.3f}J')
        qp.drawText(w - 170, 205, f'Eg    :{Eg:7.3f}J')
        qp.drawText(w - 170, 235, f'Ev    :{Ev:7.3f}J')


        qp.setPen(QtGui.QPen(col.cGreen3,2))
        g =l/3
        G =g * np.sin(ang)
        alp = ang -np.pi/2
        gpy =rpy +  np.cos(alp)*G
        gpx = rpx+ np.sin(alp)*G
        qp.drawLine(rpx, rpy,gpx ,gpy, arror=2,asize=5)
        qp.drawLine(rpx, rpy, rpx, rpy+g, arror=2,asize=5)
        G = g * np.cos(ang)
        lpx = rpx -  np.sin(ang)*G
        lpy =  rpy- np.cos(ang)*G
        qp.drawLine(rpx, rpy,lpx ,lpy, arror=2,asize=5)
        qp.setPen(QtGui.QPen(col.cGreen3,1,qt.DotLine))
        qp.drawLine(gpx, gpy, rpx, rpy + g)
        qp.drawLine(gpx, gpy, lpx, lpy)


        self.paintEnd()
        super(Ghp, self).paintEvent(a0)



class Ui_Form(FrameBase):
    name = "运动-能量守恒"
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1004, 749)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.img = Ghp(Form)
        self.img.setObjectName("img")
        self.verticalLayout.addWidget(self.img)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(0, 60))
        self.label.setMaximumSize(QtCore.QSize(80, 60))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.ang = QtWidgets.QDial(Form)
        self.ang.setMinimumSize(QtCore.QSize(0, 60))
        self.ang.setMaximumSize(QtCore.QSize(60, 60))
        self.ang.setMinimum(1)
        self.ang.setMaximum(90)
        self.ang.setProperty("value", 45)
        self.ang.setObjectName("ang")
        self.horizontalLayout.addWidget(self.ang)
        self.lcda = QtWidgets.QLCDNumber(Form)
        self.lcda.setMinimumSize(QtCore.QSize(100, 0))
        self.lcda.setMaximumSize(QtCore.QSize(100, 40))
        self.lcda.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lcda.setSmallDecimalPoint(True)
        self.lcda.setDigitCount(2)
        self.lcda.setProperty("value", 45.0)
        self.lcda.setObjectName("lcda")
        self.horizontalLayout.addWidget(self.lcda)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(120, 0))
        self.label_2.setMaximumSize(QtCore.QSize(120, 60))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.dial = QtWidgets.QDial(Form)
        self.dial.setMinimumSize(QtCore.QSize(60, 60))
        self.dial.setMaximumSize(QtCore.QSize(60, 60))
        self.dial.setMinimum(10)
        self.dial.setMaximum(100)
        self.dial.setProperty("value", 50)
        self.dial.setObjectName("dial")
        self.horizontalLayout.addWidget(self.dial)
        self.lcdl = QtWidgets.QLCDNumber(Form)
        self.lcdl.setMinimumSize(QtCore.QSize(100, 0))
        self.lcdl.setMaximumSize(QtCore.QSize(100, 40))
        self.lcdl.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lcdl.setDigitCount(3)
        self.lcdl.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdl.setProperty("value", 5.0)
        self.lcdl.setObjectName("lcdl")
        self.horizontalLayout.addWidget(self.lcdl)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(50, 0))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.run = ButLight(Form)
        self.run.setMinimumSize(QtCore.QSize(120, 50))
        self.run.setMaximumSize(QtCore.QSize(120, 50))
        self.run.setObjectName("run")
        self.horizontalLayout.addWidget(self.run)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tline = QtWidgets.QSlider(Form)
        self.tline.setOrientation(QtCore.Qt.Horizontal)
        self.tline.setObjectName("tline")
        self.tline.setRange(0,399)
        self.verticalLayout.addWidget(self.tline)
        self.verticalLayout.setStretch(0, 100)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.dial.valueChanged.connect(self.vc)
        self.ang.valueChanged.connect(self.vc)
        self.tline.valueChanged.connect(self.tc)
        self.run.clicked.connect(self.Run)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeo)
        self.vc()
    def Run(self):
        if self.run.select:
            self.run.select = False
            self.timer.stop()
        else:
            self.timer.start(int(self.img.dt*2))
            self.run.select=True
    def timeo(self):
        if self.run.select :
            self.tline.setValue((self.img.t+1)%400)
            pass
        else:
            self.timer.stop()
        self.update()

    def vc(self):
        self.timer.stop()
        self.lcdl.setProperty("value",self.dial.value()/10)
        self.img.l=self.dial.value()/10
        self.lcda.setProperty("value",self.ang.value())
        self.img.angs = self.ang.value()
        self.run.select = False
        self.img.co()
        self.update()
    def tc(self):
        self.img.t = self.tline.value()
        self.img.update()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "初始角度："))
        self.label_2.setText(_translate("Form", "摆长："))
        self.run.setText(_translate("Form", "RUN\n2倍慢镜头"))
