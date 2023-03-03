
from mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from head import *

import qdarktheme


if __name__ == '__main__':

    palette = qdarktheme.load_palette()
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarktheme.load_stylesheet())
    app.setStyleSheet("* {background-color :rgb(0, 8, 8);color :rgb(200,200,200)}")
    loadFonts()

    mw = Ui_MainWindow()
    mw.setupUi(mw)
    mw.showMaximized()
    app.exec()