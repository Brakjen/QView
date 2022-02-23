from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg


class NotImplementedDialog(qtw.QMessageBox):
    def __init__(self, informative):
        qtw.QMessageBox.__init__(self, informative)

        self.setWindowTitle('Warning')
        self.setText('Not Implemented Yet')
        self.setInformativeText(informative)
        self.setIcon(self.Information)
        self.exec_()
