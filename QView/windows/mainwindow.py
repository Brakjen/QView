from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from ui_files.ui_mainwindow import Ui_MainWindow
from widgets.centralwidget import CentralWidget

from backend.commandhandler import CommandHandler
import resources.files


class MySSHToolBar(qtw.QToolBar):
    signalQueueRequest = qtc.Signal()
    signalHistoryRequest = qtc.Signal()
    signalTopRequest = qtc.Signal()
    signalOpenPathRequest = qtc.Signal(str)
    signalOpenUserFileRequest = qtc.Signal(str)
    signalKillSelectedRequest = qtc.Signal()
    signalKillAllRequest = qtc.Signal()
    signalSCFPlotRequest = qtc.Signal()
    signalGeomPlotRequest = qtc.Signal()

    def __init__(self, parent):
        qtw.QToolBar.__init__(self, parent)
        self.setIconSize(qtc.QSize(35, 50))

        self.actionQueue = qtg.QAction(qtg.QIcon(':/icons/getqueue'), 'Queue', self)
        self.actionHistory = qtg.QAction(qtg.QIcon(':/icons/gethistory'), 'History', self)
        self.actionTop = qtg.QAction(qtg.QIcon(':/icons/gettop'), 'Top', self)
        self.actionStderr = qtg.QAction(qtg.QIcon(':/icons/error'), 'Error', self)
        self.actionStdOut = qtg.QAction(qtg.QIcon(':/icons/log'), 'Log', self)
        self.actionCommand = qtg.QAction(qtg.QIcon(':/icons/command'), 'Command', self)
        self.actionOutput = qtg.QAction(qtg.QIcon(':/icons/output'), 'Output', self)
        self.actionInput = qtg.QAction(qtg.QIcon(':/icons/input'), 'Input', self)
        self.actionSCFPlot = qtg.QAction('SCF Conv.', self)
        self.actionGeometryPlot = qtg.QAction(qtg.QIcon(':/icons/geomconv'), 'Geom. Conv.', self)
        self.actionKillSelectedJob = qtg.QAction(qtg.QIcon(':/icons/killsel'), 'Kill Sel.', self)
        self.actionKillAllJobs = qtg.QAction(qtg.QIcon(':/icons/killall'), 'Kill All', self)

        self.addAction(self.actionQueue)
        self.addAction(self.actionHistory)
        self.addAction(self.actionTop)
        self.addSeparator()
        self.addAction(self.actionInput)
        self.addAction(self.actionOutput)
        self.addSeparator()
        self.addAction(self.actionStderr)
        self.addAction(self.actionStdOut)
        self.addAction(self.actionCommand)
        self.addSeparator()
        self.addAction(self.actionSCFPlot)
        self.addAction(self.actionGeometryPlot)
        self.addSeparator()
        self.addAction(self.actionKillSelectedJob)
        self.addAction(self.actionKillAllJobs)

        self.actionQueue.triggered.connect(self.signalQueueRequest.emit)
        self.actionHistory.triggered.connect(self.signalHistoryRequest.emit)
        self.actionTop.triggered.connect(self.signalTopRequest.emit)
        self.actionStderr.triggered.connect(lambda: self.signalOpenPathRequest.emit('stderr'))
        self.actionStdOut.triggered.connect(lambda: self.signalOpenPathRequest.emit('stdout'))
        self.actionCommand.triggered.connect(lambda: self.signalOpenPathRequest.emit('command'))

        self.actionOutput.triggered.connect(lambda: self.signalOpenUserFileRequest.emit('output'))
        self.actionInput.triggered.connect(lambda: self.signalOpenUserFileRequest.emit('input'))

        self.actionKillSelectedJob.triggered.connect(self.signalKillSelectedRequest.emit)
        self.actionKillAllJobs.triggered.connect(self.signalKillAllRequest.emit)
        self.actionSCFPlot.triggered.connect(self.signalSCFPlotRequest.emit)
        self.actionGeometryPlot.triggered.connect(self.signalGeomPlotRequest.emit)


class MySystemToolBar(qtw.QToolBar):
    signalToggleIconHelp = qtc.Signal(int)
    signalLogoutRequest = qtc.Signal()

    def __init__(self, parent):
        qtw.QToolBar.__init__(self, parent)
        self.setIconSize(qtc.QSize(40, 40))

        actionQuit = qtg.QAction(qtg.QIcon(':/icons/quit'), 'Quit', self)
        actionLogout = qtg.QAction(qtg.QIcon(':/icons/logout'), 'Log out', self)
        actionToggleIconHelp = qtg.QAction(qtg.QIcon(':/icons/help'), 'Icon help', self)
        actionToggleIconHelp.setCheckable(True)

        self.addAction(actionQuit)
        self.addAction(actionLogout)
        self.addAction(actionToggleIconHelp)

        actionToggleIconHelp.triggered.connect(lambda isChecked: self.signalToggleIconHelp.emit(isChecked))
        actionQuit.triggered.connect(qtc.QCoreApplication.quit)
        actionLogout.triggered.connect(self.signalLogoutRequest.emit)


class MainWindow(qtw.QMainWindow):
    """Class for the main window. Some features come from QtDesigner,
    and some come from hand code."""
    signalInsertTableRequest = qtc.Signal(str)
    signalKillSelectedCommandRequest = qtc.Signal(str, list)
    signalKillAllCommandRequest = qtc.Signal(str)

    def __init__(self, defaults):
        qtw.QMainWindow.__init__(self)
        self.defaults = defaults
        self.commandHandler = CommandHandler()

        # Set up UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Add widget components
        self.central = CentralWidget(self)
        self.setCentralWidget(self.central)
        self.sshToolBar = MySSHToolBar(self)
        self.systemToolBar = MySystemToolBar(self)
        self.addToolBar(qtc.Qt.TopToolBarArea, self.sshToolBar)
        self.addToolBar(qtc.Qt.BottomToolBarArea, self.systemToolBar)

        # Make connections
        self.makeConnections()

        # Give table widget access to the system defaults
        self.central.tabTables.defaults = self.defaults

    def makeConnections(self):
        """Connect child widget signals to slots"""
        self.sshToolBar.signalQueueRequest.connect(self.onQueueRequest)
        self.sshToolBar.signalHistoryRequest.connect(self.onHitoryRequest)
        self.sshToolBar.signalTopRequest.connect(self.onTopRequest)
        self.ui.usernameLineEdit.returnPressed.connect(self.onQueueRequest)
        self.ui.pushButtonSearch.clicked.connect(self.findText)
        self.ui.tableWidgetMatches.itemClicked.connect(self.goToMatchedLine)
        self.ui.findLineEdit.returnPressed.connect(self.findText)

        self.systemToolBar.signalToggleIconHelp.connect(self.onToggleIconHelp)
        self.sshToolBar.signalKillSelectedRequest.connect(self.onKillSelectedRequest)
        self.sshToolBar.signalKillAllRequest.connect(lambda: self.signalKillAllCommandRequest.emit(
            self.commandHandler.killAllCommand(self.ui.usernameLineEdit.text())
        ))

    @qtc.Slot()
    def onKillSelectedRequest(self):
        sel = self.central.tabTables.getSelectedJobIDs()
        if not sel:
            return
        cmd = self.commandHandler.killSelectedCommand(sel)
        self.signalKillSelectedCommandRequest.emit(cmd, sel)


    @qtc.Slot(int)
    def onToggleIconHelp(self, showHelp):
        """Turn on and off the text below each icon."""
        if showHelp:
            self.systemToolBar.setToolButtonStyle(qtc.Qt.ToolButtonTextUnderIcon)
            self.sshToolBar.setToolButtonStyle(qtc.Qt.ToolButtonTextUnderIcon)
        else:
            self.systemToolBar.setToolButtonStyle(qtc.Qt.ToolButtonIconOnly)
            self.sshToolBar.setToolButtonStyle(qtc.Qt.ToolButtonIconOnly)

    @qtc.Slot()
    def onQueueRequest(self):
        username = self.ui.usernameLineEdit.text()
        filters = {'username': username,
                   'headers': self.defaults['queue_headers'] + self.defaults['queue_system_headers']}

        cmd = self.commandHandler.queueCommand(filters, self.defaults['queue_field_width'])
        self.signalInsertTableRequest.emit(cmd)

    @qtc.Slot()
    def onHitoryRequest(self):
        username = self.ui.usernameLineEdit.text()
        filters = {'username': username,
                   'headers': self.defaults['history_headers'] + self.defaults['history_system_headers']}

        cmd = self.commandHandler.historyCommand(filters)
        self.signalInsertTableRequest.emit(cmd)

    @qtc.Slot()
    def onTopRequest(self):
        cmd = self.commandHandler.topCommand()
        self.signalInsertTableRequest.emit(cmd)

    def findText(self):
        """A simple search feature for find text in file viewer

        1. Get file contents as list of strings
        2. Loop over all lines, trying to match query
        3. If match, store line and line index
        4. Put results into table for displaying
        """
        fileContents = self.central.tabFiles.toPlainText().splitlines()
        results = {}
        query = qtc.QRegularExpression(self.ui.findLineEdit.text())
        for i, line in enumerate(fileContents):
            match = query.match(line)
            if match.hasMatch():
                results[str(i)] = ' '.join(line.split())

        self.ui.tableWidgetMatches.setRowCount(len(results))
        rowCounter = 0
        for i, line in results.items():
            itemIndex = qtw.QTableWidgetItem(i)
            itemLine = qtw.QTableWidgetItem(line)

            self.ui.tableWidgetMatches.setItem(rowCounter, 0, itemIndex)
            self.ui.tableWidgetMatches.setItem(rowCounter, 1, itemLine)
            rowCounter += 1

    def goToMatchedLine(self, item):
        """Takes a table item as input from the itemClicked event."""
        lineNumber = int(self.ui.tableWidgetMatches.item(item.row(), 0).text())
        block = self.central.tabFiles.document().findBlockByLineNumber(lineNumber)
        cursor = qtg.QTextCursor(block)
        cursor.select(cursor.LineUnderCursor)
        self.central.tabFiles.setTextCursor(cursor)
        self.central.tabFiles.setFocus()

    def insertConvergenceData(self, data):
        """Insert dummy SCF data as demonstration."""
        self.ui.treeWidgetConvergence.clear()
        self.ui.treeWidgetConvergence.setHeaderLabels(['SCF iterations'])
        for iter in data.keys():
            iterNode = qtw.QTreeWidgetItem(self.ui.treeWidgetConvergence, [f'SCF Run: {iter}'])
            for e in data[iter]['Energy']:
                qtw.QTreeWidgetItem(iterNode, [f'Energy = {e}'])

        self.ui.treeWidgetConvergence.expandAll()
