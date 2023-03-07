

from PyQt5 import QtCore, QtGui, QtWidgets
from uiFrame_block import Block
from f1 import Ui_b



class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        # MainWindow.setMinimumSize(800,600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Gad = QtWidgets.QGridLayout()
        self.Gad.setColumnStretch(1,1)
        self.Gad.setColumnStretch(2,1)
        self.Gad.setRowStretch(1,1 )
        self.Gad.setRowStretch(2, 1)
        self.Gad.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.Gad.setHorizontalSpacing(2)
        self.Gad.setVerticalSpacing(2)
        self.Gad.setObjectName("Gad")

        self.l1 = Block()
        self.l1.setObjectName("l1")
        self.Gad.addWidget(self.l1, 1, 1, 1, 1)

        self.l2 = Block()
        self.l2.setObjectName("l2")
        self.Gad.addWidget(self.l2, 1, 2, 1, 1)

        self.l3 =  Block()
        self.l3.setObjectName("l3")
        self.Gad.addWidget(self.l3, 2, 1, 1, 1)

        self.l4 = Block()
        self.l4.setObjectName("l4")
        self.Gad.addWidget(self.l4, 2, 2, 1, 1)

        self.horizontalLayout_2.addLayout(self.Gad)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
