from PyQt5 import QtCore, QtGui, QtWidgets
from Colordef import *
class ButLeft(QtWidgets.QPushButton):
    sig = QtCore.pyqtSignal(str)
    select = False
    def initBut(self,name):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setObjectName(name)
        self.setText(name)
        self.name=name
        self.clicked.connect(self.clk)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        super().paintEvent(a0)
        qp = QPainter()
        qp.begin(self)
        qp.setPen(createpen(cgray, 4, qt.FlatCap))
        qp.drawLine(self.width() - 5, int(self.height() * .2), self.width() - 5, int(self.height() * .8))
        if self.select:
            qp.setPen(createpen(cGreen3,2,qt.FlatCap))
            qp.drawLine(self.width() - 5, int(self.height() * .2), self.width() - 5, int(self.height() * .8))
        qp.end()

    def clk(self) -> None:
        self.sig.emit(self.name)
