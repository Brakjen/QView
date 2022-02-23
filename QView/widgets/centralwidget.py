from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from widgets.fileviewer import FileViewer
from widgets.tableviewer import TableViewer


class CentralWidget(qtw.QTabWidget):
    """Class for holding the central widget in the application.
    Will hold tabs for different main viewers."""
    def __init__(self, parent):
        qtw.QTabWidget.__init__(self, parent)

        # Define tabs
        self.tabTables = TableViewer(self)
        self.tabFiles = FileViewer(self)

        # Add tabs
        self.addTab(self.tabTables, 'Table Viewer')
        self.addTab(self.tabFiles, 'File Viewer')
