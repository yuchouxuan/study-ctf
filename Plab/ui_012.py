import math

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
        ox = w-40
        oy = h -40

        zoom  = (ox/self.L)
        df = zoom * self.F
        dw = zoom *self.W
        wh = int(oy*0.8)
        Objl=int(oy*0.7)
        Vl = int(df*self.W/(self.F + self.W) )
        Vh = int ( Objl *self.F / (self.F+self.W ) )

        qp = myPainter()
        qp.begin(self)
        qp.setPen(col.cGreen2)
        qp.drawLine(0,oy,w,oy)
        qp.drawLine(ox-df  , oy , ox -df , oy-5)
        qp.drawText(ox-df ,oy+20,'F')

        qp.setPen(QtGui.QPen(qt.white,3))
        qp.drawLine(ox , h , ox, h - wh)
        qp.drawLine( ox, h - wh, ox-10, h - wh-40)
        qp.drawLine( ox, h - wh, ox+10, h - wh-40)

        qp.setPen(QtGui.QPen(qt.red, 2))
        qp.drawLine(ox - dw, oy , ox-dw,  oy-Objl)
        qp.drawLine( ox - dw, oy - Objl, ox - dw-5, oy - Objl+20)
        qp.drawLine( ox - dw, oy - Objl, ox - dw+5, oy - Objl+20)

        qp.setPen(QtGui.QPen(qt.red, 2,qt.DotLine))
        qp.drawLine(ox - Vl, oy , ox - Vl, oy-Vh )
        qp.drawLine(ox - Vl, oy-Vh, ox - Vl-5, oy - Vh+20)
        qp.drawLine(ox - Vl, oy-Vh, ox - Vl+5, oy - Vh+20)

        qp.setPen(QtGui.QPen(qt.gray))
        qp.drawLine( ox - dw, oy - Objl ,ox , oy,arror=1)
        qp.drawLine( ox - dw, oy - Objl,ox , oy-Objl, arror=1)
        qp.drawLine(ox, oy - Objl,ox+40, oy-Objl-40*(Objl/df),arror=1)

        qp.setPen(QtGui.QPen(col.cgray2, 1,qt.DotLine))
        qp.drawLine(ox-df, oy , ox , oy - Objl)

        qp.end()
        super(Ghp, self).paintEvent(a0)
    pass

class Ui_Form(FrameBase):
    name = "光学-凹透镜成像"
    def update(self):
        self.F = 2+ self.dF.value()/10
        self.W = 1+self.horizontalSlider.value()/10
        self.lcdw.setProperty("value",  self.W)
        self.lcdf.setProperty("value",  self.F)
        self.img.W =self.W
        self.img.F = self.F
        fdbs =  self.F/(self.F+self.W)
        self.lcdfd.setProperty('value',fdbs)
        self.lscx.setProperty('value', fdbs * self.W)
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
