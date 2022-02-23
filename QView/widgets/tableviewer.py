from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
import pandas as pd
from pathlib import Path

styleSheet = """
TableViewer {
    background-color: black;
    alternate-background-color: #1c1c1c;
    color: white
}
TableViewer::item:selected {
    background-color: #486b68
}
QHeaderView {
    background-color: black;
    padding: 4px;
    border: 1px solid #a6009b;
    color: #a6009b;
    font-size: 12pt;
    font: bold
}
QHeaderView::section:vertical {
    font-size: 10pt
}
QTableCornerButton::section {
    background-color: black;
    border: 1px solid #a6009b
}
"""


class TableViewer(qtw.QTableWidget):
    signalOpenFilePathsRequest = qtc.Signal(list)
    signalJobNamesReady = qtc.Signal(list)
    signalCellClickedEvent = qtc.Signal(str, str)

    def __init__(self, parent):
        qtw.QTableWidget.__init__(self, parent)
        self.defaults = {}
        self.viewMode = 'queue'
        self.rawTableContents = None
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
        self.setStyleSheet(styleSheet)
        self.verticalHeader().setFixedWidth(60)
        self.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)

        self.cellClicked.connect(self.onCellClicked)

    def onCellClicked(self, row, col):
        if self.viewMode == 'queue':
            jobstate = self.getJobState(row)
            idx = self.getPathIndex('stdout')
            jobname = Path(self.rawTableContents[row][idx]).stem
            pid = self.rawTableContents[row][0]

            if jobstate == 'RUNNING':
                self.signalCellClickedEvent.emit(pid, jobname)

    def setViewMode(self, mode):
        self.viewMode = mode

    def setRawTableContents(self, data):
        self.rawTableContents = data

    def insertDummyData(self, headers):
        """If the queue is empty, then just insert the headers"""
        self.clear()
        ncols = len(headers)
        self.setColumnCount(ncols)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(headers)
        self.resizeRowsToContents()

    def insertData(self, headers):
        """Method for insert data into the table. Takes as input a
        pandas DataFrame. Emits signal when changed"""
        self.clear()

        nrows = len(self.rawTableContents)
        ncols = len(headers)

        self.setRowCount(nrows)
        self.setColumnCount(ncols)

        self.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(self.rawTableContents):
            for j, col in enumerate(row):
                item = qtw.QTableWidgetItem(self.rawTableContents[i][j])
                self.setItem(i, j, item)

        # FIXME: Sometimes the resizing does not take place. Have to get the same table twice for effect to take place
        self.resizeRowsToContents()
        self.resizeColumnsToContents()

    def getJobState(self, row):
        """Find the column where the state is, and return the value"""
        # Get column index where states are stored
        # return the status at given row
        for i, el in enumerate(self.rawTableContents[0]):
            if el in ['RUNNING', 'PENDING', 'COMPLETED', 'TIMEOUT', 'CANCELLED']:
                return self.rawTableContents[row][i]

    def getCPULoad(self, row):
        """Find the column where %CPU is, then return the value."""
        for i in range(self.columnCount()):
            label = self.horizontalHeaderItem(i).text()
            if label.lower() == '%cpu':
                return int(float(self.item(row, i).text()))

    def colorCodeTable(self, cmd):
        colorRunning = '#34a374'
        colorPending = '#f58f00'
        colorCompleted = '#0069e0'
        colorCancelled = '#c700ac'
        colorTimeouted = '#c40000'
        colorHeavyCPU = '#c40000'
        colorMediumCPU = '#0069e0'
        colorLightCPU = '#00ba57'

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if cmd.startswith('squeue') or cmd.startswith('sacct'):
                    st = self.getJobState(i).upper()
                    if 'RUNNING' in st:
                        self.item(i, j).setForeground(qtg.QColor(colorRunning))
                    elif 'PENDING' in st:
                        self.item(i, j).setForeground(qtg.QColor(colorPending))
                    elif 'COMPL' in st:
                        self.item(i, j).setForeground(qtg.QColor(colorCompleted))
                    elif 'TIMEO' in st:
                        self.item(i, j).setForeground(qtg.QColor(colorTimeouted))
                    elif 'CANCEL' in st:
                        self.item(i, j).setForeground(qtg.QColor(colorCancelled))

                elif cmd.startswith('top'):
                    load = self.getCPULoad(i)
                    if load > 80:
                        self.item(i, j).setForeground(qtg.QColor(colorHeavyCPU))
                    elif load > 40:
                        self.item(i, j).setForeground(qtg.QColor(colorMediumCPU))
                    else:
                        self.item(i, j).setForeground(qtg.QColor(colorLightCPU))

    def getSelectedRowIndeces(self):
        """Wrapper around getting the selected row indeces. Return unique row indeces."""
        return set([item.row() for item in self.selectedIndexes()])

    def getSelectedJobIDs(self):
        """Get unique jobids for currently selected rows."""
        if self.viewMode != 'top':
            pids = [self.item(row, 0).text() for row in self.getSelectedRowIndeces()]
            return pids

    def getPathIndex(self, path_type):
        """Use system queue headers to deduce at which col index the passed path type is located"""
        if self.viewMode == 'queue':
            for i, h in enumerate(self.defaults['queue_system_headers']):
                if h.lower() == path_type:
                    return i + len(self.defaults['queue_headers'])

    def getSelectedPaths(self, path_type):
        """Return list of paths of passed type associated with selected rows.
        Only supports these files types:
            - stderr: SLURM error file
            - stdout: SLURM log file
            - command: SLURM sbatch file"""
        if path_type not in ['stderr', 'stdout', 'command']:
            return

        paths = []
        idx = self.getPathIndex(path_type)
        if idx is None:
            return []
        for row in self.getSelectedRowIndeces():
            d = self.rawTableContents[row][idx]
            paths.append(d)
        self.signalOpenFilePathsRequest.emit(paths)

    def getSelectedJobNames(self):
        """Return the job names for the selected rows. Assume the name is the same as for stdout file."""
        names = []
        idx = self.getPathIndex('stdout')
        if idx is None:
            return []
        for row in self.getSelectedRowIndeces():
            n = Path(self.rawTableContents[row][idx])
            names.append(n.stem)
        return names
