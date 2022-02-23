import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
import traceback
import pandas as pd
import json
from pathlib import Path

from windows.loginwindow import LoginWindow
from windows.mainwindow import MainWindow
from dialogs.errordialog import ErrorDialog
from dialogs.notimplemented import NotImplementedDialog
from dialogs.warningdialog import WarningDialog

from backend.ssh_client import SSHClient
from backend.tableparser import TableParser

from output_parsers.orca import OrcaOutput
from output_parsers.mrchem import MRChemOutput

from helpers import *


class QView(qtw.QApplication):
    """Main application class. Control login logic and
    connect signals to slots."""
    def __init__(self):
        qtw.QApplication.__init__(self)
        self.defaults = self.setDefaults()
        self.ssh = SSHClient(self.defaults)

        # Instantiate the windows
        self.loginWindow = LoginWindow()
        self.loginUi = self.loginWindow.ui
        self.mainWindow = MainWindow(self.defaults)

        # Make login window visible to user
        self.loginWindow.show()

        # Set up connection
        self.makeConnections()

    def makeConnections(self):
        # Logging in / logging out
        self.loginWindow.signalLoginRequest.connect(lambda user, pwd, host: self.ssh.authorize(user, pwd, host))
        self.ssh.signalLoginSuccessful.connect(self.onLoginSuccessful)
        self.mainWindow.systemToolBar.signalLogoutRequest.connect(self.onLogoutRequest)

        # Execute remote commands
        self.mainWindow.signalInsertTableRequest.connect(self.onInsertTableRequest)
        self.mainWindow.signalKillSelectedCommandRequest.connect(self.onKillSelectedCommandRequest)
        self.mainWindow.signalKillAllCommandRequest.connect(self.onKillAllCommandRequest)
        self.mainWindow.sshToolBar.signalSCFPlotRequest.connect(self.onDisplaySCFPlotRequest)
        self.mainWindow.sshToolBar.signalGeomPlotRequest.connect(self.onDisplayGeomPlotRequest)

        # Backend error handling
        self.ssh.signalBackendError.connect(self.onBackendError)

        # Files
        self.mainWindow.sshToolBar.signalOpenPathRequest.connect(lambda path_type: self.mainWindow.central.tabTables.getSelectedPaths(path_type))
        self.mainWindow.central.tabTables.signalOpenFilePathsRequest.connect(self.onOpenFilePathRequest)
        self.mainWindow.sshToolBar.signalOpenUserFileRequest.connect(self.onOpenUserFileRequest)

        # General interactions
        self.mainWindow.central.tabTables.signalCellClickedEvent.connect(self.onCellClickedEvent)

    @qtc.Slot(list)
    def onBackendError(self, params):
        """Open an error dialog with information about what process that failed."""
        text, informative, detailed = params
        return ErrorDialog(title='Backend Error',
                           text=text,
                           informative=informative,
                           detailed=detailed)

    @qtc.Slot(str, str)
    def onLoginSuccessful(self, user, host):
        self.loginWindow.close()
        self.mainWindow.show()
        self.mainWindow.ui.usernameLineEdit.setText(user)
        self.setupAutoCompletetions()
        self.ssh.currentCluster = host

        # Fetch queue at login
        self.mainWindow.sshToolBar.signalQueueRequest.emit()

    @qtc.Slot()
    def onLogoutRequest(self):
        self.ssh.ssh_client.close()
        self.mainWindow.hide()
        self.loginWindow.show()

    @qtc.Slot(str)
    def onInsertTableRequest(self, cmd):
        """Send command to cluster, and get stdout back. Determine what type of table it is and insert"""
        stdout = self.ssh.executeCommand(cmd)
        if stdout is None:
            return
        parser = TableParser(stdout, self.defaults['queue_field_width'])

        if cmd.startswith('squeue'):
            self.mainWindow.central.tabTables.setViewMode('queue')
            data = parser.parseQueue()
            headers = self.defaults['queue_headers']

            # Check if queue data is empty
            if not data:
                self.mainWindow.central.tabTables.insertDummyData(headers)
                return

            # Prescreen to get rid of deviant rows, by matching the number of cols in each row
            # to the number of header items
            data = [row for row in data if len(row) == len(headers)+len(self.defaults['queue_system_headers'])]

            # Pass data to widget
            self.mainWindow.central.tabTables.setRawTableContents(data)
            self.mainWindow.central.tabTables.insertData(headers)

        elif cmd.startswith('sacct'):
            self.mainWindow.central.tabTables.setViewMode('history')
            data = parser.parseHistory()
            headers = self.defaults['history_headers']
            if not data:
                self.mainWindow.central.tabTables.insertDummyData(headers)
                return
            self.mainWindow.central.tabTables.setRawTableContents(data)
            self.mainWindow.central.tabTables.insertData(headers)

        elif cmd.startswith('top'):
            self.mainWindow.central.tabTables.setViewMode('top')
            stdout = self.ssh.executeCommand(cmd)
            data = parser.parseTop()

            self.mainWindow.central.tabTables.setRawTableContents(data[1:])
            self.mainWindow.central.tabTables.insertData(data[0])

        self.mainWindow.central.tabTables.colorCodeTable(cmd)

        # Change active tab to the Table Viewer (index 0)
        self.mainWindow.central.setCurrentIndex(0)

    @qtc.Slot(list)
    def onOpenFilePathRequest(self, paths):
        """Get the file contents for the paths, and insert into file viewer."""
        contents = self.ssh.getFileContents(paths)
        self.mainWindow.central.tabFiles.insertFileContents(contents)

        # Change the active tab to File Viewer (index 1)
        if contents is not None:
            self.mainWindow.central.setCurrentIndex(1)

    def setDefaults(self):
        """Set default settings to be used by the application"""
        d = {
            'queue_headers': ["JOBID", "NAME", "TIMELIMIT", "TIMELEFT", "REASONLIST"],
            'queue_system_headers': ["STDOUT", "STDERR", "COMMAND", "USERNAME", "STATE", "WORKDIR"],
            'queue_field_width': 200,
            'history_headers': ['JOBID', 'JOBNAME', 'EXITCODE', 'ELAPSED', 'END', 'MAXRSS', 'AVERSS', 'STATE'],
            'history_system_headers': ['USER'],
            'scratch_area': Path('/cluster/work/jobs'),
            'extension_inputfile': '.inp',
            'extension_outputfile': '.out'
        }
        return d

    def setupAutoCompletetions(self):
        usernames = self.ssh.getAllUsernames()
        usernameCompleter = qtw.QCompleter(usernames)
        self.mainWindow.ui.usernameLineEdit.setCompleter(usernameCompleter)

    def resolveUserFilePathFromSelected(self, ftype):
        scratch = Path(self.defaults['scratch_area'])
        jobnames = self.mainWindow.central.tabTables.getSelectedJobNames()
        pids = self.mainWindow.central.tabTables.getSelectedJobIDs()
        ext = self.defaults[f'extension_{ftype}file']
        paths = [scratch.joinpath(pid, name+ext) for name, pid in zip(jobnames, pids)]

        return paths

    def resolveUserFilePath(self, jobname, pid, ftype):
        return Path(self.defaults['scratch_area'].joinpath(pid, jobname+self.defaults[f'extension_{ftype}file']))

    @qtc.Slot(str)
    def onOpenUserFileRequest(self, ftype):
        paths = self.resolveUserFilePathFromSelected(ftype)
        contents = self.ssh.getFileContents(paths)
        self.mainWindow.central.tabFiles.insertFileContents(contents)

        # Open File Viewer tab
        if contents is not None:
            self.mainWindow.central.setCurrentIndex(1)

    @qtc.Slot(str, str)
    def onCellClickedEvent(self, pid, jobname):
        path = Path(self.defaults['scratch_area']).joinpath(pid, jobname+self.defaults['extension_outputfile'])
        dest = self.ssh.downloadToTemp(path)

        if dest is None:
            return

        isGaussian, isORCA, isMRChem = determineQMCode(dest)
        if isGaussian:
            pass
        elif isORCA:
            output = OrcaOutput(dest)
        elif isMRChem:
            output = MRChemOutput(dest)
        else:
            ErrorDialog(text='Could not determine which QM software that generated the output file. Only Gaussian, ORCA, and MRChem are currently supported.')

        self.mainWindow.insertConvergenceData(output.getSCFRuns())

    @qtc.Slot(str)
    def onKillSelectedCommandRequest(self, cmd, pids):
        q = WarningDialog(text='Are you sure you want to kill the jobs?',
                          informative=', '.join(pids))
        if q.result():
            self.ssh.executeCommand(cmd)
            self.mainWindow.sshToolBar.signalQueueRequest.emit()

    @qtc.Slot(str)
    def onKillAllCommandRequest(self, cmd):
        q = WarningDialog(text='Are you sure you want to kill ALL jobs? No extra warning!')
        if q.result():
            self.ssh.executeCommand(cmd)
            self.mainWindow.sshToolBar.signalQueueRequest.emit()

    @qtc.Slot()
    def onDisplaySCFPlotRequest(self):
        try:
            paths = self.resolveUserFilePathFromSelected('output')
            dest = self.ssh.downloadToTemp(paths[0])
            isGaussian, isORCA, isMRChem = determineQMCode(dest)
        except (TypeError, IndexError):
            return

        if isMRChem:
            return MRChemOutput(dest).plotSCFConvergence()
        else:
            NotImplementedDialog(informative='Currently only MRChem is supported for SCF plots.')

    @qtc.Slot()
    def onDisplayGeomPlotRequest(self):
        try:
            paths = self.resolveUserFilePathFromSelected('output')
            dest = self.ssh.downloadToTemp(paths[0])
            isGaussian, isORCA, isMRChem = determineQMCode(dest)
        except (TypeError, IndexError):
            return ErrorDialog(title='Geometry Plot Error',
                               text='Error occurred when downloading output file',
                               informative=None,
                               detailed=None)

        if isMRChem:
            NotImplementedDialog(informative='Geometry convergence plots not currently supported for MRChem.')
        elif isGaussian:
            NotImplementedDialog(informative='Geometry convergence plots not currently supported for Gaussian.')
        elif isORCA:
            return OrcaOutput(dest).plotGeometryConvergence()


if __name__ == '__main__':
    app = QView()
    app.exec_()
    clearDir(app.ssh.tmp)