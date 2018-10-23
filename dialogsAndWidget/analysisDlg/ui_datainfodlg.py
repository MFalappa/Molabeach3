# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'datainfodlg.ui'
#
# Created: Fri Jan 10 10:03:12 2014
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_InfoDlg(object):
    def setupUi(self, InfoDlg):
        InfoDlg.setObjectName(_fromUtf8("InfoDlg"))
        InfoDlg.resize(590, 403)
        InfoDlg.setToolTip(_fromUtf8(""))
        InfoDlg.setSizeGripEnabled(False)
        self.horizontalLayout_6 = QtGui.QHBoxLayout(InfoDlg)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(InfoDlg)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.labelName = QtGui.QLabel(InfoDlg)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout.addWidget(self.labelName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tableWidgetData = QtGui.QTableWidget(InfoDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetData.sizePolicy().hasHeightForWidth())
        self.tableWidgetData.setSizePolicy(sizePolicy)
        self.tableWidgetData.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidgetData.setObjectName(_fromUtf8("tableWidgetData"))
        self.tableWidgetData.setColumnCount(0)
        self.tableWidgetData.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tableWidgetData)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.textBrowser = QtGui.QTextBrowser(InfoDlg)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.horizontalLayout_2.addWidget(self.textBrowser)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(InfoDlg)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.listWidgetTypes = QtGui.QListWidget(InfoDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetTypes.sizePolicy().hasHeightForWidth())
        self.listWidgetTypes.setSizePolicy(sizePolicy)
        self.listWidgetTypes.setMinimumSize(QtCore.QSize(100, 50))
        self.listWidgetTypes.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listWidgetTypes.setObjectName(_fromUtf8("listWidgetTypes"))
        self.horizontalLayout_5.addWidget(self.listWidgetTypes)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.pushButtonEdit = QtGui.QPushButton(InfoDlg)
        self.pushButtonEdit.setObjectName(_fromUtf8("pushButtonEdit"))
        self.horizontalLayout_4.addWidget(self.pushButtonEdit)
        self.pushButtonRestore = QtGui.QPushButton(InfoDlg)
        self.pushButtonRestore.setObjectName(_fromUtf8("pushButtonRestore"))
        self.horizontalLayout_4.addWidget(self.pushButtonRestore)
        self.pushButtonClose = QtGui.QPushButton(InfoDlg)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.horizontalLayout_4.addWidget(self.pushButtonClose)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.retranslateUi(InfoDlg)
        QtCore.QMetaObject.connectSlotsByName(InfoDlg)

    def retranslateUi(self, InfoDlg):
        InfoDlg.setWindowTitle(_translate("InfoDlg", "Info", None))
        self.label.setText(_translate("InfoDlg", "Dataset:", None))
        self.labelName.setText(_translate("InfoDlg", "TextLabel", None))
        self.label_2.setText(_translate("InfoDlg", "Data Types:", None))
        self.pushButtonEdit.setText(_translate("InfoDlg", "Edit Types", None))
        self.pushButtonRestore.setText(_translate("InfoDlg", "Restore Types", None))
        self.pushButtonClose.setText(_translate("InfoDlg", "Close", None))

