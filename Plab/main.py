from MainWnd import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarktheme

if __name__ == '__main__':
    palette = qdarktheme.load_palette()
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarktheme.load_stylesheet())
    mw = Ui_MainWindow()
    mw.setupUi(mw)
    mw.show()
    app.exec()
