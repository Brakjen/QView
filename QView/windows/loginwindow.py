from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from ui_files.ui_loginwindow import Ui_LoginWindow

color_window_background = '#663d0042'
color_background = '#663d0042'
color_radiobutton_checked = 'black'
color_radiobutton_unchedked = 'transparent'
color_text = '#cd7fd4'

styleSheet = f"""
LoginWindow {{
    background: {color_window_background};
    border: 3px solid black
}}

QPushButton {{
    background-color: {color_background};
    color: {color_text};
    border: 1px solid;
    border-top-color: {color_text};
    border-left-color: {color_text};
    width: 80px;
}}

QPushButton:pressed {{
    background-color: {color_background};
    color: {color_text};
    border: 1px solid;
    border-bottom-color: {color_text};
    border-right-color: {color_text}
}}

QLabel {{
    color: {color_text};
}}

QRadioButton {{
    color: {color_text};
}}

QRadioButton::indicator::checked {{
    background-color: {color_radiobutton_checked};
    border: 1px solid {color_text};
}}

QRadioButton::indicator::unchecked {{
    background-color: transparent;
    border: 1px solid {color_text};
}}

QLineEdit {{
    background: transparent;
    color: {color_text};
    border: 1px solid black;
    border-radius: 10px
}}

QLineEdit:focus {{
    border: 1px solid {color_text};
}}
"""


class LoginWindow(qtw.QFrame):
    """Class for displaying the login window. Emits a signal with the
    login credentials whenever the user clicks on the login button.
    The application quits when the user clicks on the quit button."""
    signalLoginRequest = qtc.Signal(str, str, str)

    def __init__(self):
        qtw.QFrame.__init__(self)
        self.setWindowFlag(qtc.Qt.FramelessWindowHint)

        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Log in')

        self.ui.buttonQuit.clicked.connect(qtc.QCoreApplication.quit)
        self.ui.buttonLogin.clicked.connect(self.onClickedLogin)
        self.ui.lineEditPassword.returnPressed.connect(self.onClickedLogin)

        self.setStyleSheet(styleSheet)
        self.ui.lineEditPassword.setAttribute(qtc.Qt.WA_MacShowFocusRect, 0)
        self.ui.lineEditUsername.setAttribute(qtc.Qt.WA_MacShowFocusRect, 0)

        self.radios = {
            'fram': self.ui.radioFram,
            'saga': self.ui.radioSaga,
            'betzy': self.ui.radioBetzy
        }

    def onClickedLogin(self):
        """Collect credentials and emit signal for login request"""
        username = self.ui.lineEditUsername.text()
        password = self.ui.lineEditPassword.text()
        cluster = self.getSelectedCluster()
        self.ui.lineEditPassword.clear()

        self.signalLoginRequest.emit(username, password, cluster)

    def getSelectedCluster(self):
        """Radio buttons are mutually exclusive, so return
        the one that is active."""
        for cluster, radio in self.radios.items():
            if radio.isChecked():
                return cluster

    def mousePressEvent(self, event):
        """Override default mousePressEvent
        (to allow for moving the window)"""
        self.origin = event.pos()

    def mouseMoveEvent(self, event):
        """Override default mouseMoveEvent
        (to allow for moving the window)"""
        x = event.globalX()
        y = event.globalY()
        x0 = self.origin.x()
        y0 = self.origin.y()
        self.move(x - x0, y - y0)
