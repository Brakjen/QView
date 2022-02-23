from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

styleSheet = """
FileViewer {
    background-color: black;
    color: white;
    font-family: Courier
}
"""


class FileViewer(qtw.QPlainTextEdit):
    def __init__(self, parent):
        qtw.QPlainTextEdit.__init__(self, parent)
        self.setLineWrapMode(self.NoWrap)
        self.setStyleSheet(styleSheet)
        self.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)

        self.textChanged.connect(lambda: self.updateGeometry())

    def insertFileContents(self, contents):
        """Display the passed string."""
        self.clear()
        self.insertPlainText(contents)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
