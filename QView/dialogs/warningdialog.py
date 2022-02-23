from PySide6 import QtWidgets as qtw


class WarningDialog(qtw.QMessageBox):
    def __init__(self, title='Warning', text=None, informative=None):
        qtw.QMessageBox.__init__(self)
        self.setStandardButtons(self.Yes | self.Cancel)
        self.setWindowTitle(title)
        self.setText(text)
        self.setInformativeText(informative)
        self.setIcon(self.Warning)

        self.ret = self.exec_()

    def result(self):
        if self.ret == self.Yes:
            return True
        else:
            return False