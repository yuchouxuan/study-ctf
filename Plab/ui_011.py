from FrameBase import  *

class Ghp(QtWidgets.QLabel):

    qpen0 = QtGui.QPen(col.cw,2,qt.SolidLine,qt.FlatCap)
    qpen1 = QtGui.QPen(col.cw, 1,qt.DashDotLine, qt.FlatCap)
    qpin  = QtGui.QPen(col.cGreen3, 2,qt.SolidLine, qt.FlatCap)
    qpout = QtGui.QPen(col.cGreen2, 2, qt.SolidLine, qt.FlatCap)
    F = 5
    W =30
    L =100
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:

        w = self.width()
        h = self.height()
        o = (w//2,h//2)
        zoom  = (w/2/self.L)
        df = zoom * self.F
        dw = zoom *self.W
        wh = h//6

        qp = myPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setPen(col.cGreen2)
        qp.drawLine(0,h//2,w,h//2)
        qp.drawLine(w//2 -df  ,h // 2 , w//2 -df , h // 2-5)
        qp.drawText(w//2 -df  ,h // 2+20,'F')
        qp.drawLine(w // 2 - 2*df, h // 2 , w // 2 - 2*df, h // 2 - 5)
        qp.drawText(w // 2 - 2*df-5, h // 2 + 20, '2F')

        qp.drawLine(w//2 +df  ,h // 2 , w//2 +df , h // 2-5)
        qp.drawText(w//2 +df  ,h // 2+20,'F')
        qp.drawLine(w // 2 + 2*df, h // 2 , w // 2 + 2*df, h // 2 - 5)
        qp.drawText(w // 2 + 2*df-5, h // 2 + 20, '2F')

        qp.setPen(QtGui.QPen(qt.white,3))
        hlj = h // 4
        hm = h//2
        qp.drawLine(w // 2  , hm +hlj , w//2 , hm-hlj)
        qp.drawLine(w // 2, hm + hlj, w // 2 +5, hm + hlj -20 )
        qp.drawLine(w // 2, hm + hlj, w // 2 - 5, hm + hlj - 20)

        qp.drawLine(w // 2, hm - hlj, w // 2 +5, hm - hlj +20 )
        qp.drawLine(w // 2, hm - hlj, w // 2 - 5, hm - hlj + 20)




        qp.setPen(col.cRed3)
        qp.drawLine(w // 2-dw , h//2 , w // 2-dw, h//2 - wh,arror=2)


        if  self.F-self.W ==0  :
            qp.drawText(30,30,"无法成像")
        else:
            xj = self.F * self.W /(self.W -self.F) *zoom
            db =  self.F/math.fabs(self.F-self.W)
            if xj > 0 :
                qp.drawText(30, 30, "实像")
                qp.drawLine(w // 2 + xj , h // 2 , w // 2 + xj , h // 2 + wh * db,arror=2)
                pen_dot = QtGui.QPen(col.cgray3,1)
                qp.setPen(pen_dot)
                qp.drawLine( w // 2-dw, h//2 - wh, w // 2 + xj , h // 2 + wh * db,arror=1)
                qp.drawLine(w // 2 - dw, h // 2 - wh, w // 2 , h // 2 - wh ,arror=1)
                qp.drawLine( w // 2, h // 2 - wh ,  w // 2 + xj , h // 2 + wh * db,arror=1)
            else :
                qp.drawText(30, 30, "虚像")
                pen_dot = QtGui.QPen(col.cRed3,2,qt.DotLine)
                qp.setPen(pen_dot)
                qp.drawLine(w // 2 + xj, h // 2, w // 2 + xj, h // 2 - wh * db,arror=2)
                pen_dot = QtGui.QPen(col.cgray3,1)
                qp.setPen(pen_dot)
                qp.drawLine(w // 2 - dw, h // 2 - wh, w // 2 +dw , h // 2 +wh ,arror=1)
                qp.drawLine(w // 2 - dw, h // 2 - wh, w // 2, h // 2 - wh,arror=1)
                qp.drawLine(w // 2, h // 2 - wh, w // 2 + df, h // 2 ,arror=1)
                pen_dot = QtGui.QPen(col.cgray3,2,qt.DotLine)
                qp.setPen(pen_dot)
                qp.drawLine(w // 2 - dw, h // 2 - wh,  w // 2 + xj, h // 2 - wh * db)
                qp.drawLine(w // 2, h // 2 - wh,  w // 2 + xj, h // 2 - wh * db)
        qp.end()
        super(Ghp, self).paintEvent(a0)
    pass

class Ui_Form(FrameBase):
    name = "光学-凸透镜成像"
    def update(self):
        self.F = 5+ self.dF.value()/20
        self.W = 1+self.horizontalSlider.value()/10
        self.lcdw.setProperty("value",  self.W)
        self.lcdf.setProperty("value",  self.F)
        self.img.W =self.W
        self.img.F = self.F
        if self.F-self.W != 0:
            fdbs =  self.F/math.fabs(self.F-self.W)
            self.lcdfd.setProperty('value',fdbs)
            self.lscx.setProperty('value', fdbs*self.W)
        else:
            self.lcdfd.setProperty('value', 0)
            self.lscx.setProperty('value', 0)

        super(Ui_Form, self).update()

    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(864, 751)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.img =Ghp(Form)
        self.img.setObjectName("img")
        self.horizontalLayout_2.addWidget(self.img)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.llllllll1 = QtWidgets.QLabel(Form)
        self.llllllll1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.llllllll1.setObjectName("llllllll1")
        self.verticalLayout.addWidget(self.llllllll1)
        self.dF = QtWidgets.QDial(Form)
        self.dF.setMaximum(999)
        self.dF.setValue(300)
        self.dF.valueChanged.connect(self.update)

        self.dF.setObjectName("dF")
        self.verticalLayout.addWidget(self.dF)
        self.lcdf = QtWidgets.QLCDNumber(Form)
        self.lcdf.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdf.setObjectName("lcdf")
        self.verticalLayout.addWidget(self.lcdf)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lscx = QtWidgets.QLCDNumber(Form)
        self.lscx.setDigitCount(7)
        self.lscx.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lscx.setObjectName("lscx")
        self.verticalLayout.addWidget(self.lscx)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.lcdfd = QtWidgets.QLCDNumber(Form)
        self.lcdfd.setDigitCount(7)
        self.lcdfd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdfd.setObjectName("lcdfd")
        self.verticalLayout.addWidget(self.lcdfd)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 10)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setMaximum(940)
        self.horizontalSlider.setValue(290)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.lcdw = QtWidgets.QLCDNumber(Form)
        self.lcdw.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdw.setObjectName("lcdw")
        self.horizontalLayout.addWidget(self.lcdw)
        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 10)
        self.horizontalSlider.valueChanged.connect(self.update)

        self.F = 5
        self.L = 100
        self.W = 1+ self.horizontalSlider.value()/10
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.update()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        # self.img.setText(_translate("Form", "img"))
        self.llllllll1.setText(_translate("Form", "焦距"))
        self.label_2.setText(_translate("Form", "像距"))
        self.label_4.setText(_translate("Form", "放大倍数"))
