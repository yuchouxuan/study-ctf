
from head import *

class Title(QtWidgets.QLabel):
    qp = QPainter()
    ip=""

    def __init__(self,tit='192.168.0.0'):
        super().__init__()
        self.setObjectName(f'TITLE_{tit}'.replace('.','_'))
        self.setText(tit)
        self.ip = tit
        self.setupUi(self)
        print(self.objectName())

    def setbkc(self,stats = 0 ):
        styles = [
            "Title#"+self.objectName()+"{color:rgb(0,0,0,192);background-color:rgb(255, 64, 64,192);}",
            "Title#" + self.objectName() + "{background-color:rgb(128, 255, 146,64);}",
            "Title#" + self.objectName() + "{background-color:rgb(255, 128, 0,64);}",
            "Title#" + self.objectName() + "{background-color:rgb(255, 255, 255,64);}"
        ]
        self.setStyleSheet(styles[stats])
    def setupUi(self, Form):
        fonts[0].setPointSize(18)
        self.setFont(fonts[0])
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setbkc(3)


class Block(QtWidgets.QFrame):
    qp = QPainter()
    def __init__(self):
        super().__init__()
        self.setupUi(self)


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.WindowModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumWidth(300)

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = Title('192.168.0.0')
        self.label.setbkc(0)
        self.verticalLayout.addWidget(self.label)

        self.label2 = Title('192.168.0.2')
        self.verticalLayout.addWidget(self.label2)
        self.verticalLayout.setStretch(1, 100)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def FillBox(self,x,y,w,h,color:QColor,dot=0,dotcol=None):
        qp=self.qp
        if dot > 2:
            dcent = dot // 2
            if dotcol == None:
                dotcol = QColor(color)
                color = QColor(color)
                color.setAlpha(color.alpha()//2)
            qp.fillRect(x, y, x + dot, y + dot, dotcol)
            qp.fillRect(x + w-dot , y, x + w, y+dot , dotcol)
            qp.fillRect(x, y + h-dot , x + dot, y + h - dot, dotcol)
            qp.fillRect(x + w-dot,y + h-dot, x + w , y + h - dot, dotcol)

        else:
            dcent = 0
        qp.setPen(createpen(dotcol))
        qp.drawRect(x + dcent, y + dcent, x + w - dcent, y + h - dcent)
        qp.fillRect(x+dcent,y+dcent,x+w-dcent,y+h-dcent,color)

    def FillRoundedRect(self,x,y,w,h,color=QColor(255,255,255,16),bound=False,color2=None):
        qp=self.qp
        path = QtGui.QPainterPath()
        if color2==None :
            color2 = color
        path.addRoundedRect(x, y, w, h, 3,3)
        qp.fillPath(path, color)
        pen = qp.pen()
        qp.setPen(color2)
        if bound==True:
            qp.drawPath(path)
        qp.setPen(pen)

    # stat 0-4: r,g,b
    def DrawSqireLight(self, x, y, w,text='', stat=0,):
        if isinstance('',text):
            text = [text,'']

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = self.qp
        qp.begin(self)
        self.FillBox(3, 3, self.width() - 6, self.height() - 6, QColor(0, 0, 0, 0), 2, cwhite[2])
        # self.FillRoundedRect(20,20,50,20,cred[-1] )
        # for i in range(0,32,1):
        #     qp.setPen(createpen(cwhite[0]))
        #     qp.drawLine(10, 100 + i, 10 +100, 100 + i)
        #     qp.setPen(createpen(cwhite[3]))
        #     qp.drawLine(10,100+i,10+random.randint(0,100),100+i)
        qp.end()