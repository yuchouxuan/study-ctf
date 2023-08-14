import numpy as np

from FrameBase import  *
class Ghp(CroDBase):
    fn =''
    k = 1
    q = 1
    a = 0
    b = 0
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:

        lx = []
        ly = []
        qp = self.paintBeg()
        self.drwCord()
        x_ang = np.linspace(self.xmir,self.xmr,self.width())
        for x in x_ang:
            lx.append(x)
            try:
                y = eval(self.fn)

                if  y < 2*self.ymr and y >2*self.ymir :
                    ly.append(y)
                else:
                    ly.append(None)
            except:
                ly.append(None)
        lx2=[]
        ly2=[]
        for x1 in x_ang:
            x = x1*self.q + self.a
            lx2.append(x1)
            try:
                y = self.k * eval(self.fn) +self.b
                if y < 2*self.ymr and y >2* self.ymir:
                    ly2.append(y)
                else:
                    ly2.append(None)
            except:
                ly2.append(None)

        f1 = self.fn.replace('**','^')
        self.Text(-self.xmr*0.9,self.ymax*0.9,'y1='+f1, col = col.cGreen3 ,fz=11)
        if self.k != 1 :
            f2 = f'y2={self.k:5.2f}*('
        else :
            f2 = 'y2='
        if self.a == 0 and self.q == 1  :
            f2 +=f1
        else:
            t = f1.replace('(x)','x')
            f2 += t.replace('x', f'(x{self.a:+5.2f})')
            if self.q !=1:
                f2 = f2.replace('x', f'{self.q:5.2f}x')
        if self.b != 0:
            f2 += f'{self.b:+5.2f}'
        f2+=')'
        self.Text(-self.xmr*0.9, self.ymax * 0.8 , f2, col=col.cRed3, fz=11)

        for i in range(1,len(lx)):
            if ly[i] != None and ly[i-1]!=None:
                self.Line(lx[i-1],ly[i-1],lx[i],ly[i],4,col.cGreen,unlim=False)

        for i in range(1,len(lx2)):
            if ly2[i] != None and ly2[i-1]!=None:
                try:
                    self.Line(lx2[i-1],ly2[i-1],lx2[i],ly2[i],1,col.cRed3,unlim=False)
                except: pass

        self.paintEnd()
        super(Ghp, self).paintEvent(a0)
    pass

class Ui_Form(FrameBase):
    name = "数学-函数\n\n平移拉伸"
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1052, 789)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.img = Ghp(Form)
        self.img.xmax = 10
        self.img.ymax = 10
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
        self.fn = QtWidgets.QLineEdit(Form)
        self.fn.setObjectName("fn")
        self.fn.setText('3*sin(x)')
        self.horizontalLayout.addWidget(self.fn)
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

        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.k = QtWidgets.QDoubleSpinBox(Form)
        self.k.setMinimum(-5)
        self.k.setMaximum(5)
        self.k.setSingleStep(0.01)
        self.k.setValue(1)
        self.k.setObjectName("k")
        self.horizontalLayout_2.addWidget(self.k)

        self.label_k = QtWidgets.QLabel(Form)

        self.label_k.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_k.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_k.setObjectName("label_k")
        self.horizontalLayout_2.addWidget(self.label_k)
        self.q = QtWidgets.QDoubleSpinBox(Form)
        self.q.setMinimum(-5)
        self.q.setMaximum(5)
        self.q.setSingleStep(0.01)
        self.q.setValue(1)
        self.q.setObjectName("q")
        self.horizontalLayout_2.addWidget(self.q)

        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.a = QtWidgets.QDoubleSpinBox(Form)
        self.a.setMinimum(-10)
        self.a.setMaximum(10)
        self.a.setSingleStep(0.05)
        self.a.setObjectName("a")
        self.horizontalLayout_2.addWidget(self.a)
        self.label_10 = QtWidgets.QLabel(Form)

        self.label_10.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.b = QtWidgets.QDoubleSpinBox(Form)
        self.b.setMinimum(-10)
        self.b.setMaximum(10)
        self.b.setSingleStep(0.05)
        self.b.setObjectName("b")
        self.horizontalLayout_2.addWidget(self.b)

        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 100)
        self.retranslateUi(Form)

        self.k.valueChanged.connect(self.vc)
        self.a.valueChanged.connect(self.vc)
        self.b.valueChanged.connect(self.vc)
        self.fn.returnPressed.connect(self.vc)
        self.q.valueChanged.connect(self.vc)
        self.vc()
        QtCore.QMetaObject.connectSlotsByName(Form)
    def vc(self):
        self.img.fn = self.fn.text()
        self.img.k = self.k.value()
        self.img.a = self.a.value()
        self.img.b = self.b.value()
        self.img.q = self.q.value()
        self.update()

        pass
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "原函数：\n乘法用*表示 乘方 用**表示"))
        self.label_4.setText(_translate("Form", "f(x)="))
        self.label_5.setText(_translate("Form", "变换"))
        self.label_7.setText(_translate("Form", "g(x)=k(f(qx+a))+b"))
        self.label_8.setText(_translate("Form", "k="))
        self.label_k.setText(_translate("Form", "q="))
        self.label_9.setText(_translate("Form", "a="))
        self.label_10.setText(_translate("Form", "b="))
