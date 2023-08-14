from  PyQt5.QtCore import Qt as qt
from PyQt5.QtGui import QPen,QFont,QColor,QPainter

cRed1 = QColor(255,0,0,32)
cGreen1 = QColor(100,255,0,32)
cYellow1 = QColor(255,255,0,32)
cOrange1 = QColor(255,128,0,32)
cVio1 = QColor(255,0,255,32)
cgray1 = QColor(128,128,128,32)
cw1 = QColor(255,255,255,32)
cb1 = QColor(0,0,0,32)

cRed = QColor(255,0,0,64)
cGreen = QColor(100,255,0,64)
cYellow = QColor(255,255,0,64)
cOrange = QColor(255,128,0,64)
cVio = QColor(255,0,255,64)
cgray = QColor(128,128,128,64)
cw = QColor(255,255,255,64)
cb = QColor(0,0,0,64)

cRed2 = QColor(255,0,0,128)
cGreen2 = QColor(100,255,0,128)
cYellow2 = QColor(255,255,0,128)
cOrange2 = QColor(255,128,0,128)
cVio2 = QColor(255,0,255,128)
cgray2 = QColor(128,128,128,128)
cw2 = QColor(255,255,255,128)
cb2 = QColor(0,0,0,128)

cRed3 = QColor(255,0,0,255)
cGreen3 = QColor(100,255,0,255)
cYellow3 = QColor(255,255,0,255)
cOrange3 = QColor(255,128,0,255)
cVio3 = QColor(255,0,255,255)
cgray3 = QColor(128,128,128,255)
cw3 = QColor(255,255,255,255)
cb3 = QColor(0,0,0,255)



def createpen(col:QColor,w:int=1,co=qt.RoundCap,ls=qt.SolidLine):
    return QPen(col,w,ls,co)