from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt as qt
from PyQt5.QtGui import *
from PyQt5.QtCore import QRect

cred    = [QColor(255, 64, 64, i)     for i in (16,32,64,128,192,255)]
cblue  = [QColor(128, 200, 255, i)   for i in (16,32,64,128,192,255)]
cgreen  = [QColor(128, 255, 146, i)   for i in (16,32,64,128,192,255)]
cyellow = [QColor(255, 255, 128, i)   for i in (16,1632,64,128,192,255)]
corange = [QColor(255, 128, 0, i)   for i in (16,32,64,128,192,255)]
cvio    = [QColor(255, 0, 255, i)   for i in (16,32,64,128,192,255)]
cgray   = [QColor(128, 128, 128, i) for i in (16,32,64,128,192,255)]
cwhite  = [QColor(255, 255, 255, i) for i in (16,32,64,128,192,255)]
cblack  = [QColor(0, 0, 0, i)       for i in (16,32,64,128,192,255)]



def createpen(col: QColor, w: int = 1, co=qt.RoundCap, ls=qt.SolidLine):
    return QPen(col, w, ls, co)


fonts = []
def loadFonts():
    fList = []
    fList.extend(
    QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont('font/AGENCYR.TTF')))
    fList.extend(QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont('font/agora.ttf')))
    fList.extend(QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont('font/Cyberiada_Light.ttf')))
    fList.extend(QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont('font/DIGITAL-Regular.ttf')))

    print('载入字体:', fList)

    for i in fList:
        fonts.append(QFont(i))






