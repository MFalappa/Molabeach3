# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchDlg.ui'
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

class Ui_SearchDlg(object):
    def setupUi(self, SearchDlg):
        SearchDlg.setObjectName(_fromUtf8("SearchDlg"))
        SearchDlg.resize(456, 386)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(SearchDlg)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(SearchDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.searchAnalisisLineEdit = QtGui.QLineEdit(SearchDlg)
        self.searchAnalisisLineEdit.setObjectName(_fromUtf8("searchAnalisisLineEdit"))
        self.horizontalLayout.addWidget(self.searchAnalisisLineEdit)
        self.searchPushButton = QtGui.QPushButton(SearchDlg)
        self.searchPushButton.setObjectName(_fromUtf8("searchPushButton"))
        self.horizontalLayout.addWidget(self.searchPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.analysisList = QtGui.QListWidget(SearchDlg)
        self.analysisList.setObjectName(_fromUtf8("analysisList"))
        self.verticalLayout.addWidget(self.analysisList)
        self.comboBox_types = QtGui.QComboBox(SearchDlg)
        self.comboBox_types.setObjectName(_fromUtf8("comboBox_types"))
        self.verticalLayout.addWidget(self.comboBox_types)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.okPushButton = QtGui.QPushButton(SearchDlg)
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout_2.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(SearchDlg)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_2.addWidget(self.cancelPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.label.setBuddy(self.searchAnalisisLineEdit)

        self.retranslateUi(SearchDlg)
        QtCore.QObject.connect(self.okPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), SearchDlg.accept)
        QtCore.QObject.connect(self.cancelPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), SearchDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(SearchDlg)
        SearchDlg.setTabOrder(self.searchAnalisisLineEdit, self.searchPushButton)

    def retranslateUi(self, SearchDlg):
        SearchDlg.setWindowTitle(_translate("SearchDlg", "Dialog", None))
        self.label.setText(_translate("SearchDlg", "&Search Analysis:", None))
        self.searchPushButton.setText(_translate("SearchDlg", "Search", None))
        self.okPushButton.setText(_translate("SearchDlg", "Ok", None))
        self.cancelPushButton.setText(_translate("SearchDlg", "Cancel", None))

