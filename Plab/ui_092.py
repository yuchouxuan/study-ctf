import math
from FrameBase import  *

class Ghp(CroDBase):
    x1 =0
    y1=0
    k=1
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.xmax =max( math.fabs(self.x1) ,math.fabs(self.y1))*1.5+1
        self.ymax = self.xmax
        qp = self.paintBeg()
        self.drwCord()
        x2 = self.x1 + 1
        y2 = self.k + self.y1
        qp.drawText(30, 30, 'y = (x - x0)k + y1')
        self.Point(self.x1,self.y1,col=col.cGreen2,line=True,cod=True)
        self.Line(self.x1,self.y1,x2,y2,col=col.cYellow2)

        dis = 'y = '
        if self.k == 0:
            dis += f'{self.y1}'
        else:
            if self.k!=1:
                dis += f'{self.k:0.3}'
            if self.x1 == 0:
                dis += 'x '
            else :
                dis += f'(x {self.x1:+0}) '
            if self.y1 != 0 : dis +=f'{self.y1:+0}'
        self.Text(self.x1,self.y1,dis,col = col.cYellow2,rank=self.k)
        self.paintEnd()
        super(Ghp, self).paintEvent(a0)
    pass


class Ui_Form(FrameBase):
    name="数学-一次函数\n\n点斜式方程"
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1052, 789)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = Ghp(Form)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
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
        self.x1.setObjectName("x1")
        self.horizontalLayout.addWidget(self.x1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(150, 0))
        self.label_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.y1 = QtWidgets.QDoubleSpinBox(Form)
        self.y1.setObjectName("y1")
        self.horizontalLayout.addWidget(self.y1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setMinimumSize(QtCore.QSize(150, 0))
        self.label_5.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setMinimumSize(QtCore.QSize(150, 0))
        self.label_7.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.k = QtWidgets.QDoubleSpinBox(Form)
        self.k.setValue(1)
        self.k.setObjectName("k")
        self.horizontalLayout_2.addWidget(self.k)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 10)
        self.k.valueChanged.connect(self.vc)
        self.x1.valueChanged.connect(self.vc)
        self.y1.valueChanged.connect(self.vc)
        self.x1.setMinimum(-10000)
        self.y1.setMinimum(-10000)
        self.k.setMinimum(-10000)
        self.k.setSingleStep(0.01)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def vc(self):
        self.label_6.x1 = self.x1.value()
        self.label_6.y1 = self.y1.value()
        self.label_6.k = self.k.value()
        super().update()




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "方程参数："))
        self.label_2.setText(_translate("Form", "点坐标 "))
        self.label_4.setText(_translate("Form", "x1="))
        self.label_3.setText(_translate("Form", "y1="))
        self.label_5.setText(_translate("Form", "斜率"))
        self.label_7.setText(_translate("Form", "k="))

