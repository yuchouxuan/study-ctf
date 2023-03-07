from head import *
from ui_title import uiTitle
import random
class Ui_b(QtWidgets.QFrame):
    qp = QPainter()
    def __init__(self,t):
        super().__init__(t)
        self.setMinimumSize(300,300)

    def setupUi(self,):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMidLineWidth(300)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate


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


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # super().paintEvent(a0)

        qp = self.qp
        qp.begin(self)
        self.FillBox(3,3,self.width()-6,self.height()-6,QColor(0,0,0,0),2,cwhite[2])
        # self.FillRoundedRect(20,20,50,20,cred[-1] )
        # for i in range(0,32,1):
        #     qp.setPen(createpen(cwhite[0]))
        #     qp.drawLine(10, 100 + i, 10 +100, 100 + i)
        #     qp.setPen(createpen(cwhite[3]))
        #     qp.drawLine(10,100+i,10+random.randint(0,100),100+i)
        qp.end()
        pass