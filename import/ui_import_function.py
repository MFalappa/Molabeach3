# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_function.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(587, 492)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 14, 560, 459))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_detected = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_detected.setFont(font)
        self.label_detected.setObjectName(_fromUtf8("label_detected"))
        self.verticalLayout_2.addWidget(self.label_detected)
        self.textBrowser_inputDetected = QtGui.QTextBrowser(self.widget)
        self.textBrowser_inputDetected.setObjectName(_fromUtf8("textBrowser_inputDetected"))
        self.verticalLayout_2.addWidget(self.textBrowser_inputDetected)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_status = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_status.setFont(font)
        self.label_status.setObjectName(_fromUtf8("label_status"))
        self.horizontalLayout_4.addWidget(self.label_status)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton_refresh = QtGui.QPushButton(self.widget)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout_4.addWidget(self.pushButton_refresh)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.textBrowser_status = QtGui.QTextBrowser(self.widget)
        self.textBrowser_status.setObjectName(_fromUtf8("textBrowser_status"))
        self.verticalLayout.addWidget(self.textBrowser_status)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.listWidget_inputType = QtGui.QListWidget(self.widget)
        self.listWidget_inputType.setObjectName(_fromUtf8("listWidget_inputType"))
        self.horizontalLayout_6.addWidget(self.listWidget_inputType)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_addType = QtGui.QPushButton(self.widget)
        self.pushButton_addType.setObjectName(_fromUtf8("pushButton_addType"))
        self.horizontalLayout.addWidget(self.pushButton_addType)
        self.pushButton_remove = QtGui.QPushButton(self.widget)
        self.pushButton_remove.setObjectName(_fromUtf8("pushButton_remove"))
        self.horizontalLayout.addWidget(self.pushButton_remove)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.splitter = QtGui.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget1 = QtGui.QWidget(self.splitter)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_Cancel = QtGui.QPushButton(self.widget1)
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.horizontalLayout_3.addWidget(self.pushButton_Cancel)
        self.pushButton_Continue = QtGui.QPushButton(self.widget1)
        self.pushButton_Continue.setObjectName(_fromUtf8("pushButton_Continue"))
        self.horizontalLayout_3.addWidget(self.pushButton_Continue)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.horizontalLayout_2.addWidget(self.splitter)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_detected.setText(_translate("Dialog", "Detected Input", None))
        self.label_status.setText(_translate("Dialog", "Status", None))
        self.pushButton_refresh.setText(_translate("Dialog", "Refresh", None))
        self.label.setText(_translate("Dialog", "Input Type", None))
        self.pushButton_addType.setText(_translate("Dialog", "Add", None))
        self.pushButton_remove.setText(_translate("Dialog", "Remove", None))
        self.pushButton_Cancel.setText(_translate("Dialog", "Cancel", None))
        self.pushButton_Continue.setText(_translate("Dialog", "Continue", None))

