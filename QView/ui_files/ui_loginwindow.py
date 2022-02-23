# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_loginwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.resize(259, 278)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginWindow.sizePolicy().hasHeightForWidth())
        LoginWindow.setSizePolicy(sizePolicy)
        LoginWindow.setMouseTracking(False)
        LoginWindow.setWindowOpacity(1.000000000000000)
        LoginWindow.setAutoFillBackground(True)
        LoginWindow.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(LoginWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(20, 20, 20, 20)
        self.label_4 = QLabel(LoginWindow)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_4)

        self.label = QLabel(LoginWindow)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.lineEditUsername = QLineEdit(LoginWindow)
        self.lineEditUsername.setObjectName(u"lineEditUsername")
        self.lineEditUsername.setClearButtonEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEditUsername)

        self.label_2 = QLabel(LoginWindow)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.lineEditPassword = QLineEdit(LoginWindow)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.setClearButtonEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEditPassword)

        self.label_3 = QLabel(LoginWindow)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.label_3)

        self.radioFram = QRadioButton(LoginWindow)
        self.radioFram.setObjectName(u"radioFram")
        self.radioFram.setChecked(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.radioFram)

        self.radioSaga = QRadioButton(LoginWindow)
        self.radioSaga.setObjectName(u"radioSaga")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.radioSaga)

        self.radioBetzy = QRadioButton(LoginWindow)
        self.radioBetzy.setObjectName(u"radioBetzy")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.radioBetzy)

        self.buttonQuit = QPushButton(LoginWindow)
        self.buttonQuit.setObjectName(u"buttonQuit")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.buttonQuit)

        self.buttonLogin = QPushButton(LoginWindow)
        self.buttonLogin.setObjectName(u"buttonLogin")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.buttonLogin)


        self.verticalLayout.addLayout(self.formLayout)

        QWidget.setTabOrder(self.lineEditUsername, self.lineEditPassword)
        QWidget.setTabOrder(self.lineEditPassword, self.radioFram)
        QWidget.setTabOrder(self.radioFram, self.radioSaga)
        QWidget.setTabOrder(self.radioSaga, self.radioBetzy)
        QWidget.setTabOrder(self.radioBetzy, self.buttonLogin)
        QWidget.setTabOrder(self.buttonLogin, self.buttonQuit)

        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p><span style=\" font-size:18pt;\">SLURM QueueViewer</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p>Sigma2 username</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("LoginWindow", u"Username", None))
        self.lineEditUsername.setText("")
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p>Sigma2 password</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("LoginWindow", u"Password", None))
        self.lineEditPassword.setText("")
        self.lineEditPassword.setPlaceholderText("")
        self.label_3.setText(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Select HPC Cluster</span></p></body></html>", None))
        self.radioFram.setText(QCoreApplication.translate("LoginWindow", u"Fram", None))
        self.radioSaga.setText(QCoreApplication.translate("LoginWindow", u"Saga", None))
        self.radioBetzy.setText(QCoreApplication.translate("LoginWindow", u"Betzy", None))
#if QT_CONFIG(tooltip)
        self.buttonQuit.setToolTip(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p>Quit application</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.buttonQuit.setText(QCoreApplication.translate("LoginWindow", u"Quit", None))
#if QT_CONFIG(tooltip)
        self.buttonLogin.setToolTip(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p>Pass credentials to SSH</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.buttonLogin.setText(QCoreApplication.translate("LoginWindow", u"Log in", None))
    # retranslateUi

