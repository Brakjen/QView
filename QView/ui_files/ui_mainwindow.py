# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(952, 628)
        self.actionQueue = QAction(MainWindow)
        self.actionQueue.setObjectName(u"actionQueue")
        self.actionTop = QAction(MainWindow)
        self.actionTop.setObjectName(u"actionTop")
        self.actionHistory = QAction(MainWindow)
        self.actionHistory.setObjectName(u"actionHistory")
        self.actionInputFile = QAction(MainWindow)
        self.actionInputFile.setObjectName(u"actionInputFile")
        self.actionOutputFile = QAction(MainWindow)
        self.actionOutputFile.setObjectName(u"actionOutputFile")
        self.actionErrorFile = QAction(MainWindow)
        self.actionErrorFile.setObjectName(u"actionErrorFile")
        self.actionCommandFile = QAction(MainWindow)
        self.actionCommandFile.setObjectName(u"actionCommandFile")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 952, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidgetFilters = QDockWidget(MainWindow)
        self.dockWidgetFilters.setObjectName(u"dockWidgetFilters")
        self.dockWidgetFiltersContents = QWidget()
        self.dockWidgetFiltersContents.setObjectName(u"dockWidgetFiltersContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetFiltersContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.loggedInToLabel = QLabel(self.dockWidgetFiltersContents)
        self.loggedInToLabel.setObjectName(u"loggedInToLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.loggedInToLabel)

        self.loggedInToComboBox = QComboBox(self.dockWidgetFiltersContents)
        self.loggedInToComboBox.setObjectName(u"loggedInToComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.loggedInToComboBox)

        self.usernameLabel = QLabel(self.dockWidgetFiltersContents)
        self.usernameLabel.setObjectName(u"usernameLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.usernameLabel)

        self.usernameLineEdit = QLineEdit(self.dockWidgetFiltersContents)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.usernameLineEdit)

        self.jobStautsLabel = QLabel(self.dockWidgetFiltersContents)
        self.jobStautsLabel.setObjectName(u"jobStautsLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.jobStautsLabel)

        self.jobStautsComboBox = QComboBox(self.dockWidgetFiltersContents)
        self.jobStautsComboBox.setObjectName(u"jobStautsComboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.jobStautsComboBox)

        self.partitionLabel = QLabel(self.dockWidgetFiltersContents)
        self.partitionLabel.setObjectName(u"partitionLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.partitionLabel)

        self.partitionComboBox = QComboBox(self.dockWidgetFiltersContents)
        self.partitionComboBox.setObjectName(u"partitionComboBox")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.partitionComboBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.dockWidgetFilters.setWidget(self.dockWidgetFiltersContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetFilters)
        self.dockWidgetFindText = QDockWidget(MainWindow)
        self.dockWidgetFindText.setObjectName(u"dockWidgetFindText")
        self.dockWidgetFindTextContents = QWidget()
        self.dockWidgetFindTextContents.setObjectName(u"dockWidgetFindTextContents")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetFindTextContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(10, 10, 10, 10)
        self.findLabel = QLabel(self.dockWidgetFindTextContents)
        self.findLabel.setObjectName(u"findLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.findLabel)

        self.findLineEdit = QLineEdit(self.dockWidgetFindTextContents)
        self.findLineEdit.setObjectName(u"findLineEdit")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.findLineEdit)

        self.CheckBoxCaseSensitive = QCheckBox(self.dockWidgetFindTextContents)
        self.CheckBoxCaseSensitive.setObjectName(u"CheckBoxCaseSensitive")
        self.CheckBoxCaseSensitive.setChecked(True)

        self.formLayout_2.setWidget(1, QFormLayout.SpanningRole, self.CheckBoxCaseSensitive)

        self.pushButtonSearch = QPushButton(self.dockWidgetFindTextContents)
        self.pushButtonSearch.setObjectName(u"pushButtonSearch")

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.pushButtonSearch)

        self.tableWidgetMatches = QTableWidget(self.dockWidgetFindTextContents)
        if (self.tableWidgetMatches.columnCount() < 2):
            self.tableWidgetMatches.setColumnCount(2)
        font = QFont()
        font.setPointSize(13)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tableWidgetMatches.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.tableWidgetMatches.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidgetMatches.setObjectName(u"tableWidgetMatches")
        self.tableWidgetMatches.setStyleSheet(u"font-size: 9pt")
        self.tableWidgetMatches.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetMatches.setWordWrap(True)
        self.tableWidgetMatches.setCornerButtonEnabled(False)
        self.tableWidgetMatches.verticalHeader().setVisible(False)

        self.formLayout_2.setWidget(3, QFormLayout.SpanningRole, self.tableWidgetMatches)


        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.dockWidgetFindText.setWidget(self.dockWidgetFindTextContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetFindText)
        self.dockWidgetConvergence = QDockWidget(MainWindow)
        self.dockWidgetConvergence.setObjectName(u"dockWidgetConvergence")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.horizontalLayout = QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.treeWidgetConvergence = QTreeWidget(self.dockWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidgetConvergence.setHeaderItem(__qtreewidgetitem)
        self.treeWidgetConvergence.setObjectName(u"treeWidgetConvergence")

        self.horizontalLayout.addWidget(self.treeWidgetConvergence)

        self.dockWidgetConvergence.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetConvergence)
        self.dockWidgetPlotArea = QDockWidget(MainWindow)
        self.dockWidgetPlotArea.setObjectName(u"dockWidgetPlotArea")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.dockWidgetPlotArea.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetPlotArea)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionQueue.setText(QCoreApplication.translate("MainWindow", u"Queue", None))
        self.actionTop.setText(QCoreApplication.translate("MainWindow", u"Top", None))
        self.actionHistory.setText(QCoreApplication.translate("MainWindow", u"History", None))
        self.actionInputFile.setText(QCoreApplication.translate("MainWindow", u"InputFile", None))
        self.actionOutputFile.setText(QCoreApplication.translate("MainWindow", u"OutputFile", None))
        self.actionErrorFile.setText(QCoreApplication.translate("MainWindow", u"ErrorFile", None))
        self.actionCommandFile.setText(QCoreApplication.translate("MainWindow", u"CommandFile", None))
        self.dockWidgetFilters.setWindowTitle(QCoreApplication.translate("MainWindow", u"Queue and History Filters", None))
        self.loggedInToLabel.setText(QCoreApplication.translate("MainWindow", u"HPC Cluster", None))
        self.usernameLabel.setText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.jobStautsLabel.setText(QCoreApplication.translate("MainWindow", u"Job Stauts", None))
        self.partitionLabel.setText(QCoreApplication.translate("MainWindow", u"Partition", None))
        self.dockWidgetFindText.setWindowTitle(QCoreApplication.translate("MainWindow", u"Find Text in Files", None))
        self.findLabel.setText(QCoreApplication.translate("MainWindow", u"Find Text", None))
        self.CheckBoxCaseSensitive.setText(QCoreApplication.translate("MainWindow", u"Case Sensitive", None))
        self.pushButtonSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        ___qtablewidgetitem = self.tableWidgetMatches.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Line Number", None));
        ___qtablewidgetitem1 = self.tableWidgetMatches.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Matched Line", None));
        self.dockWidgetConvergence.setWindowTitle(QCoreApplication.translate("MainWindow", u"Convergence Inspector", None))
        self.dockWidgetPlotArea.setWindowTitle(QCoreApplication.translate("MainWindow", u"Plotting Area", None))
    # retranslateUi

