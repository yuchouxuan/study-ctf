from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt as qt
import Colordef as col
import math
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter
class FrameBase(QtWidgets.QFrame):
    name="test"
from math import *

class myPainter(QtGui.QPainter):
    def begin(self, a0 ) -> bool:
        super().begin(a0)
        super().setRenderHint(QtGui.QPainter.Antialiasing)
    def drawText(self,x,y,s):
        super().drawText(int(x),int(y),s)
    def drawArc(self, x,y,w,h ,a0,a1):
        super().drawArc(int(x),int(y),int(w),int(h),int(a0),int(a1))
    def drawEllipse(self, a0, a1, a2, a3):
        super().drawEllipse(int(a0),int(a1),int(a2),int(a3))
    def drawRect(self,a0,a1,a2,a3):
        super().drawRect(int(a0),int(a1),int(a2),int(a3))

    def drawPoint(self,x,y):
        super().drawPoint(int(x),int(y))

    def dl(self,x1, x2, x3, x4):
        super().drawLine(int(x1), int(x2), int(x3), int(x4))
    def drawLine(self, x1, y1,x2,y2, arror=0,asize=15):

        if arror == 0 :
            self.dl(x1, y1, x2, y2)
        else:
            self.dl(x1, y1, x2, y2)
            dx = x2-x1
            dy = y2 -y1
            r = math.sqrt((dx)**2 + (dy)**2)
            if r < 2 :
                return
            alpha0 = math.asin(dy/r)  # 原线角
            if dx < 0 :
                alpha0 = math.pi-alpha0

            a1 = alpha0 +0.2
            a2 = alpha0 - 0.2
            if arror == 1:
                ax = x1+(dx) /2
                ay = y1+(dy) / 2
            if arror == 2:
                ax = x2
                ay = y2
            p1x = ax-asize*math.cos(a1)
            p1y = ay-asize*math.sin(a1)
            p2x = ax - asize * math.cos(a2)
            p2y = ay - asize * math.sin(a2)

            self.dl(ax, ay, p1x, p1y)
            self.dl(ax, ay, p2x, p2y)

#带灯的按钮
class ButLight(QtWidgets.QPushButton):
    select = False
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        super().paintEvent(a0)
        qp = myPainter()
        qp.begin(self)
        if self.select:
            pen = QtGui.QPen(col.cRed2,2)
        else:
            pen = QtGui.QPen(col.cGreen2, 2)
        qp.setPen(pen)
        qp.drawLine( self.width()*0.2, self.height()-4,self.width()*0.8, self.height()-4 )
        qp.end()

#坐标轴
class CroDBase(QtWidgets.QLabel):
    x0 = 0
    y0 = 0
    xmax = 10
    ymax = 10
    dx= 0
    dy = 0
    xmr = 0
    ymr = 0
    xmir=0
    ymir=0
    def paintBeg(self,x0=0,y0=0,anzoom=True) -> myPainter:
        w = self.width()
        h = self.height()
        self.dx = w/2/self.xmax
        self.dy = h / 2 / self.ymax
        if anzoom:
            self.dx = min(self.dx,self.dy)
            self.dy = self.dx

        self.xmr = w / 2 / self.dx+x0
        self.ymr =(h / 2 / self.dx - y0)

        self.xmir =  -(w / 2 / self.dx+x0)
        self.ymir = -(h / 2 / self.dy+y0)

        self.x0 = w / 2 + self.dx*x0
        self.y0 = h / 2 - self.dx*y0

        self.qp = myPainter()
        self.qp.begin(self)
        return self.qp
    def drwCord(self): #画坐标轴
        qp = self.qp
        p = qp.pen()
        qp.setPen(qt.white)
        qp.drawLine(0,self.y0,self.width(),self.y0,arror=2 )
        qp.drawText(self.width() -10,self.y0+20,'X')
        qp.drawLine(self.x0, self.height(),self.x0 , 0, arror=2)
        qp.drawText(self.x0+10  , 10 , 'Y')
        qp.drawText(self.x0 + 10,self.y0+20, '0')
        #刻度 -x
        qp.setPen(col.cgray3)
        dx =10 ** int(math.log10(self.xmax*5) -1 )

        x = self.x0
        cont = 1
        while x < self.width():
            x += dx *self.dx
            qp.drawLine(x,self.y0, x, self.y0-5)
            qp.drawText(x, self.y0+20, '{}'.format(dx*cont) )
            cont+=1
        x = self.x0
        cont = -1
        while x >0 :
            x -= dx *self.dx
            qp.drawLine(x,self.y0, x, self.y0-5)
            qp.drawText(x, self.y0+20, '{}'.format(dx*cont) )
            cont-=1
        # 刻度-y
        dy = 10 ** int(math.log10(self.ymax*5) - 1)
        y = self.y0
        cont = 1
        while y >0 :
            y -= dy * self.dy
            qp.drawLine(self.x0,  y, self.x0-5, y)
            qp.drawText(self.x0+5,y+5 , '{}'.format(dy * cont))
            cont += 1
        y = self.y0
        cont = -1
        while y < self.height() :
            y += dy * self.dy
            qp.drawLine(self.x0,  y, self.x0-5, y)
            qp.drawText(self.x0+5,y+5 , '{}'.format(dy * cont))
            cont -= 1
        qp.setPen(p)

    def Point(self,cx,cy,size = 5, col=qt.white,line=False,cod=False):
        x = self.x0 + cx * self.dx
        y = self.y0 - cy * self.dy
        qp = self.qp
        p = qp.pen()
        qp.setPen(QtGui.QPen(col,size,qt.SolidLine,qt.RoundCap))
        qp.drawPoint(x,y)
        if(line):
            self.qp.setPen(QtGui.QPen(col, 1, qt.DotLine, qt.FlatCap))
            qp.drawLine(x,y,x,self.y0)
            qp.drawLine(self.x0, y, x, y)
        if(cod):
            qp.drawText(x+3,y,'({0},{1})'.format(cx,cy))
        qp.setPen(p)

    def Text (self,x,y,txt,col = qt.white, fz = 11, rank=0):
        x = self.x0 + x * self.dx
        y = self.y0 - y * self.dy
        qp = self.qp
        p = qp.pen()
        f = QtGui.QFont()
        s = f.pointSizeF()
        f.setPointSize(fz)
        qp.setFont(f)
        qp.setPen(col)
        qp.translate(x,y)
        r = math.degrees(math.atan(rank))
        qp.rotate(-r)
        qp.drawText(-fz,0-fz,txt)
        qp.resetTransform()

        f.setPointSize(int(s))
        qp.setFont(f)
        qp.setPen(p)

    def Line(self,cx0,cy0, cx1,cy1 ,size = 2, col=qt.red, style = qt.SolidLine, unlim= True,arror=False):
        x0 = self.x0 + cx0 * self.dx
        y0 = self.y0 - cy0 * self.dy
        x1 = self.x0 + cx1 * self.dx
        y1 = self.y0 - cy1 * self.dy
        dx = x1 - x0
        dy = y1 - y0
        #平行于y轴
        qp = self.qp
        qp.setPen(QtGui.QPen(col, size, style, qt.FlatCap))
        if dx == 0:
            if unlim :
                if y0 > y1:
                    qp.drawLine(x1,0,x1,self.height(),arror)
                else :
                    qp.drawLine(x1, self.height(), x1, 0, arror)
            else :
                qp.drawLine(x0, y0, x1, y1, arror)
        else : # 不平行
            qp.drawLine(x0, y0, x1, y1, arror)
            if unlim:
                k = dy / dx
                qp.drawLine(x0, y0, 0, y0-x0/self.dx*self.dy *k )
                qp.drawLine(x1, y1, self.width(), y1 + (self.width()-x1)/ self.dx * self.dy * k)

    def paintEnd(self):
        try:self.qp.end()
        except: pass


class RCroDBase(CroDBase):

    rmax = 10
    dr = 10

    def paintBeg(self, x0=0, y0=0) -> myPainter:
        super().paintBeg(x0,y0,True)
        self.dr = min(self.dx,self.dy)
    def drwCord(self): #画坐标轴
        qp = self.qp
        p = qp.pen()
        qp.setPen(qt.white)
        qp.drawLine(self.x0,self.y0,self.width(),self.y0,arror=2 )
        qp.drawText(self.width() -10,self.y0+20,'R')
        #刻度 -x
        qp.setPen(col.cgray3)
        dx =10 ** int(math.log10(self.rmax*5) -1 )
        x = self.x0 -  dx *self.dr
        cont = 0
        while x < self.width():
            x += dx *self.dr
            qp.drawLine(x,self.y0, x, self.y0-5)
            qp.drawText(x, self.y0+20, '{}'.format(dx*cont) )
            cont+=1
        qp.setPen(p)

    def Point(self, r, z, size=5, col=qt.white, line=False, cod=False):
        x = self.x0 + r*math.cos(z) * self.dx
        y = self.y0 - r*math.sin(z) * self.dy
        qp = self.qp
        p = qp.pen()
        qp.setPen(QtGui.QPen(col, size, qt.SolidLine, qt.RoundCap))
        qp.drawPoint(x, y)
        if (line):
            self.qp.setPen(QtGui.QPen(col, 1))
            qp.drawLine(self.x0, self.y0, x, y,arror=2,asize=10)
        if (cod):
            qp.drawText(x + 3, y, '({:5.2f},{:5.2f})'.format(r, z))
        qp.setPen(p)
    def Text(self,r,z,txt,col = qt.white, fz = 11, rank=0):
        super().Text(r*cos(z),r*sin(z),txt,col,fz,rank=rank)

    def Line(self,r0,z0, r1,z1 ,size = 2, col=qt.red, style = qt.SolidLine, unlim= True,arror=False):
        super().Line(self, r0*cos(z0), r0*sin(z0), r1*cos(z1), r1*sin(z1), size, col, style, unlim, arror)


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.paintBeg()
        self.drwCord()
        self.paintEnd()