from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
import paramiko as pmk
import traceback
import socket
from pathlib import Path

from helpers import getHostname

tempDIr = Path(Path.cwd()).joinpath('tmp')


class SSHClient(qtc.QObject):
    """Class for sending commands to the remote cluster. Inherits from
    QObject to allow for emitting signals
    """
    signalBackendError = qtc.Signal(list)
    signalBackendWarning = qtc.Signal(str)
    signalLoginSuccessful = qtc.Signal(str, str)

    def __init__(self, defaults):
        qtc.QObject.__init__(self)
        # FIXME: More general path handling
        self.tmp = tempDIr
        if not self.tmp.exists():
            print(f'Making temporary directory: {self.tmp}')
            self.tmp.mkdir()
        self.ssh_client = pmk.SSHClient()
        self.ssh_client.set_missing_host_key_policy(pmk.MissingHostKeyPolicy)
        self.currentCluster = None

        self.defaults = defaults

    def executeCommand(self, cmd):
        """Wrapper around the exec_command from SSHClient.
        If network (ssh) problem      : emit SSHCommandError.
        If error in remote execution  : emit RemoteCommandError"""
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            out = stdout.read()
            err = stderr.read()
            if err:
                self.signalBackendError.emit(['The following command failed on remote cluster:',
                                              cmd,
                                              err.decode('utf-8')])
                return
            else:
                self.data = out.decode('utf-8')
                return out.decode('utf-8')
        except Exception:
            self.signalBackendError.emit(['Could not execute the following command',
                                         cmd,
                                         traceback.format_exc()])

    def authorize(self, user, pwd, host):
        """Try to connect. Exceptions captured in main."""
        try:
            self.ssh_client.connect(username=user, password=pwd, hostname=getHostname(host))
            self.signalLoginSuccessful.emit(user, host)

            # Set up SFT protocol
            self.sftp_client = self.setupSFTP()

        except pmk.ssh_exception.AuthenticationException as e:
            self.signalBackendError.emit(['Login failed',
                                         str(e),
                                         traceback.format_exc()])
        except socket.gaierror as e:
            self.signalBackendError.emit(['Login failed',
                                          str(e),
                                          traceback.format_exc()])

    def isAlive(self):
        """Check if ssh connection is alive"""
        try:
            self.ssh_client.exec_command('pwd', timeout=5)
            return True
        except Exception:
            return False

    def setupSFTP(self):
        try:
            sftp = pmk.SFTP.from_transport(self.ssh_client.get_transport())
            return sftp
        except Exception as e:
            self.signalBackendError.emit(['Error in setting up SFT protocol',
                                          str(e),
                                          traceback.format_exc()])

    def getFileContents(self, paths):
        """Locate and open remote file. Return file contents as string."""
        try:
            path = Path(paths[0])
        except IndexError:
            return
        try:
            destination = self.tmp.joinpath(Path(path).stem)
            self.sftp_client.get(path.__str__(), destination)
            with open(destination) as f:
                contents = f.read()
            return contents
        except PermissionError as e:
            self.signalBackendError.emit(['Permission denied',
                                          str(e),
                                          traceback.format_exc()])
        except FileNotFoundError as e:
            self.signalBackendError.emit(['File not found',
                                          str(e),
                                          traceback.format_exc()])

    def downloadToTemp(self, path):
        try:
            dest = self.tmp.joinpath(path.stem)
            self.sftp_client.get(path.__str__(), dest)
            return dest
        except FileNotFoundError as e:
            self.signalBackendWarning.emit('File not found')
        except PermissionError as e:
            self.signalBackendWarning.emit('Permission denied')

    def getAllUsernames(self):
        return self.executeCommand('ls /cluster/home').split()

