from FrameBase import  *

class Ghp(CroDBase):
    x1 =0
    y1=0
    x2 = 1
    y2 = 1
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.xmax =max( math.fabs(self.x1) ,math.fabs(self.y1),math.fabs(self.x2) ,math.fabs(self.y2))*1.5+1
        self.ymax = self.xmax
        qp = self.paintBeg()
        self.drwCord()
        if self.x1==self.x2 :
            qp.drawText( 20,20,"无法构建方程")
            return
        qp.drawText(30, 30, '(x - x1)/(x2-x1) =(y - y1)/(y2-y1)')
        self.Point(self.x1,self.y1,col=col.cGreen2,line=True,cod=True)
        self.Point(self.x2, self.y2, col=col.cRed2, line=True, cod=True)
        self.Line(self.x1,self.y1,self.x2,self.y2,col=col.cYellow2)
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        k  = dy / dx
        dis = 'y = '
        if k == 0:
            dis += f'{self.y1:4.2f}'
        else :
            dis +=f'{k:4.2f}'
            if(self.x1 == 0):
                dis +='x'
            else:
                dis +=f'(x{-self.x1:+4.2f})'
            if self.y2 != 0 :
                dis +=f'{self.y2:+4.2f}'
        self.Text(self.x1, self.y1, dis, col=col.cYellow2, rank=k)
        self.paintEnd()
        super(Ghp, self).paintEvent(a0)
    pass

class Ui_Form(FrameBase):
    name = "数学-一次函数\n\n两点式方程"
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1052, 789)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.img =Ghp(Form)
        self.img.setText("")
        self.img.setObjectName("img")
        self.verticalLayout.addWidget(self.img)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setMinimumSize(QtCore.QSize(150, 0))
        self.label_4.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.x1 = QtWidgets.QDoubleSpinBox(Form)
        self.x1.setDecimals(7)
        self.x1.setMinimum(-2000.0)
        self.x1.setMaximum(2000.0)
        self.x1.setSingleStep(0.1)
        self.x1.setObjectName("x1")
        self.horizontalLayout.addWidget(self.x1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(150, 0))
        self.label_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.y1 = QtWidgets.QDoubleSpinBox(Form)
        self.y1.setDecimals(7)
        self.y1.setMinimum(-200.0)
        self.y1.setMaximum(200.0)
        self.y1.setSingleStep(0.1)
        self.y1.setObjectName("y1")
        self.horizontalLayout.addWidget(self.y1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setMinimumSize(QtCore.QSize(150, 0))
        self.label_5.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setMinimumSize(QtCore.QSize(150, 0))
        self.label_7.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.x2 = QtWidgets.QDoubleSpinBox(Form)
        self.x2.setDecimals(7)
        self.x2.setMinimum(-2000.0)
        self.x2.setMaximum(2000.0)
        self.x2.setSingleStep(0.1)
        self.x2.setProperty("value", 1.0)
        self.x2.setObjectName("x2")
        self.horizontalLayout_2.addWidget(self.x2)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setMinimumSize(QtCore.QSize(150, 0))
        self.label_8.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.y2 = QtWidgets.QDoubleSpinBox(Form)
        self.y2.setDecimals(7)
        self.y2.setMinimum(-2000.0)
        self.y2.setMaximum(2000.0)
        self.y2.setSingleStep(0.1)
        self.y2.setProperty("value", 1.0)
        self.y2.setObjectName("y2")
        self.horizontalLayout_2.addWidget(self.y2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 10)

        self.x2.valueChanged.connect(self.vc)
        self.y2.valueChanged.connect(self.vc)
        self.x1.valueChanged.connect(self.vc)
        self.y1.valueChanged.connect(self.vc)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def vc(self):
        self.img.x1 = self.x1.value()
        self.img.y1 = self.y1.value()
        self.img.x2 = self.x2.value()
        self.img.y2 = self.y2.value()

        super().update()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "点坐标 "))
        self.label_4.setText(_translate("Form", "x1="))
        self.label_3.setText(_translate("Form", "y1="))
        self.label_7.setText(_translate("Form", "x2="))
        self.label_8.setText(_translate("Form", "y2="))
