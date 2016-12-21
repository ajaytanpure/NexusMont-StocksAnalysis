# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Ajay\PycharmProjects\NexusMont\ui_files\settings_ui.ui'
#
# Created: Sat Aug 01 21:31:59 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(QtGui.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 254)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/stockmarket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.horizontalLayout_4 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.reload_data_button = QtGui.QPushButton(Dialog)
        self.reload_data_button.setMinimumSize(QtCore.QSize(90, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.reload_data_button.setFont(font)
        self.reload_data_button.setObjectName("reload_data_button")
        self.gridLayout.addWidget(self.reload_data_button, 0, 0, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtGui.QLabel(Dialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalGroupBox = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox.setObjectName("horizontalGroupBox")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.before_radio = QtGui.QRadioButton(self.horizontalGroupBox)
        self.before_radio.setObjectName("before_radio")
        self.horizontalLayout_2.addWidget(self.before_radio)
        self.after_radio = QtGui.QRadioButton(self.horizontalGroupBox)
        self.after_radio.setObjectName("after_radio")
        self.horizontalLayout_2.addWidget(self.after_radio)
        self.verticalLayout_4.addWidget(self.horizontalGroupBox)
        self.delet_status = QtGui.QLabel(Dialog)
        self.delet_status.setText("")
        self.delet_status.setObjectName("delet_status")
        self.verticalLayout_4.addWidget(self.delet_status)
        self.dateEdit = QtGui.QDateEdit(Dialog)
        self.dateEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_4.addWidget(self.dateEdit)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 1, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.reload_status = QtGui.QLabel(Dialog)
        self.reload_status.setText("")
        self.reload_status.setObjectName("reload_status")
        self.verticalLayout_6.addWidget(self.reload_status)
        self.reload_status_bar = QtGui.QProgressBar(Dialog)
        self.reload_status_bar.setMaximumSize(QtCore.QSize(250, 16777215))
        self.reload_status_bar.setProperty("value", 24)
        self.reload_status_bar.setObjectName("reload_status_bar")
        self.verticalLayout_6.addWidget(self.reload_status_bar)
        self.gridLayout.addLayout(self.verticalLayout_6, 0, 1, 1, 1)
        self.delete_button = QtGui.QPushButton(Dialog)
        self.delete_button.setMinimumSize(QtCore.QSize(90, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.gridLayout.addWidget(self.delete_button, 1, 0, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "NexusSettings", None, QtGui.QApplication.UnicodeUTF8))
        self.reload_data_button.setText(QtGui.QApplication.translate("Dialog", "   Reload Data   ", None, QtGui.QApplication.UnicodeUTF8))
        self.before_radio.setText(QtGui.QApplication.translate("Dialog", "Before", None, QtGui.QApplication.UnicodeUTF8))
        self.after_radio.setText(QtGui.QApplication.translate("Dialog", "After", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setText(QtGui.QApplication.translate("Dialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
