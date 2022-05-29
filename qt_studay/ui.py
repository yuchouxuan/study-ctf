# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore,QtWidgets
from a  import Ui_Dialog

app = QtWidgets.QApplication([])
dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(dialog)
dialog.show()
ui.b_exit.clicked.connect(app.exit,0)
app.exec_()