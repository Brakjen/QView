from PySide6 import QtWidgets as qtw


class ErrorDialog(qtw.QMessageBox):
    def __init__(self, title='Error', text=None, informative=None, detailed=None):
        qtw.QMessageBox.__init__(self)

        self.setWindowTitle(title)
        self.setText(text)
        self.setInformativeText(informative)
        self.setDetailedText(detailed)
        self.setIcon(self.Critical)
        self.exec_()
