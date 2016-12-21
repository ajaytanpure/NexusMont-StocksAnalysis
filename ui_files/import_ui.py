# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Ajay\PycharmProjects\NexusMont\ui_files\import_ui.ui'
#
# Created: Sat May 23 20:09:46 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(QtGui.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(252, 250)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(250, 250))
        Dialog.setMaximumSize(QtCore.QSize(252, 250))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/stockmarket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vlayout = QtGui.QVBoxLayout()
        self.vlayout.setObjectName("vlayout")
        self.calendarWidget = QtGui.QCalendarWidget(Dialog)
        self.calendarWidget.setObjectName("calendarWidget")
        self.vlayout.addWidget(self.calendarWidget)
        self.start_import_button = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_import_button.sizePolicy().hasHeightForWidth())
        self.start_import_button.setSizePolicy(sizePolicy)
        self.start_import_button.setMaximumSize(QtCore.QSize(100, 50))
        self.start_import_button.setObjectName("start_import_button")
        self.vlayout.addWidget(self.start_import_button)
        self.status_lable = QtGui.QLabel(Dialog)
        self.status_lable.setObjectName("status_lable")
        self.vlayout.addWidget(self.status_lable)
        self.import_progressbar = QtGui.QProgressBar(Dialog)
        self.import_progressbar.setProperty("value", 24)
        self.import_progressbar.setObjectName("import_progressbar")
        self.vlayout.addWidget(self.import_progressbar)
        self.verticalLayout_2.addLayout(self.vlayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Importer", None, QtGui.QApplication.UnicodeUTF8))
        self.start_import_button.setText(QtGui.QApplication.translate("Dialog", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.status_lable.setText(QtGui.QApplication.translate("Dialog", "Status", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
