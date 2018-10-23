# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mergedlg.ui'
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

class Ui_SelectDataset(object):
    def setupUi(self, SelectDataset):
        SelectDataset.setObjectName(_fromUtf8("SelectDataset"))
        SelectDataset.resize(597, 348)
        self.horizontalLayout_4 = QtGui.QHBoxLayout(SelectDataset)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelAllDataset = QtGui.QLabel(SelectDataset)
        self.labelAllDataset.setObjectName(_fromUtf8("labelAllDataset"))
        self.verticalLayout.addWidget(self.labelAllDataset)
        self.listWidgetAllDataset = QtGui.QListWidget(SelectDataset)
        self.listWidgetAllDataset.setObjectName(_fromUtf8("listWidgetAllDataset"))
        self.verticalLayout.addWidget(self.listWidgetAllDataset)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.labelDatasetToMerge = QtGui.QLabel(SelectDataset)
        self.labelDatasetToMerge.setObjectName(_fromUtf8("labelDatasetToMerge"))
        self.verticalLayout_2.addWidget(self.labelDatasetToMerge)
        self.listWidgetSelected = QtGui.QListWidget(SelectDataset)
        self.listWidgetSelected.setObjectName(_fromUtf8("listWidgetSelected"))
        self.verticalLayout_2.addWidget(self.listWidgetSelected)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButtonUp = QtGui.QPushButton(SelectDataset)
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.verticalLayout_3.addWidget(self.pushButtonUp)
        self.pushButtonAdd = QtGui.QPushButton(SelectDataset)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.verticalLayout_3.addWidget(self.pushButtonAdd)
        self.pushButtonNext = QtGui.QPushButton(SelectDataset)
        self.pushButtonNext.setObjectName(_fromUtf8("pushButtonNext"))
        self.verticalLayout_3.addWidget(self.pushButtonNext)
        self.pushButtonRemove = QtGui.QPushButton(SelectDataset)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.verticalLayout_3.addWidget(self.pushButtonRemove)
        self.pushButtonDown = QtGui.QPushButton(SelectDataset)
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.verticalLayout_3.addWidget(self.pushButtonDown)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.labelMergedName = QtGui.QLabel(SelectDataset)
        self.labelMergedName.setObjectName(_fromUtf8("labelMergedName"))
        self.horizontalLayout_2.addWidget(self.labelMergedName)
        self.lineEditMergedName = QtGui.QLineEdit(SelectDataset)
        self.lineEditMergedName.setObjectName(_fromUtf8("lineEditMergedName"))
        self.horizontalLayout_2.addWidget(self.lineEditMergedName)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonOk = QtGui.QPushButton(SelectDataset)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.pushButtonCancel = QtGui.QPushButton(SelectDataset)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.labelAllDataset.setBuddy(self.listWidgetAllDataset)
        self.labelDatasetToMerge.setBuddy(self.listWidgetSelected)
        self.labelMergedName.setBuddy(self.lineEditMergedName)

        self.retranslateUi(SelectDataset)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), SelectDataset.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectDataset)
        SelectDataset.setTabOrder(self.listWidgetAllDataset, self.listWidgetSelected)
        SelectDataset.setTabOrder(self.listWidgetSelected, self.lineEditMergedName)
        SelectDataset.setTabOrder(self.lineEditMergedName, self.pushButtonUp)
        SelectDataset.setTabOrder(self.pushButtonUp, self.pushButtonRemove)
        SelectDataset.setTabOrder(self.pushButtonRemove, self.pushButtonDown)

    def retranslateUi(self, SelectDataset):
        SelectDataset.setWindowTitle(_translate("SelectDataset", "Dialog", None))
        self.labelAllDataset.setText(_translate("SelectDataset", "&Select  dataset:", None))
        self.labelDatasetToMerge.setText(_translate("SelectDataset", "&Dataset to merge:", None))
        self.pushButtonUp.setText(_translate("SelectDataset", "Up", None))
        self.pushButtonAdd.setText(_translate("SelectDataset", "Add", None))
        self.pushButtonNext.setText(_translate("SelectDataset", "Next", None))
        self.pushButtonRemove.setText(_translate("SelectDataset", "Remove", None))
        self.pushButtonDown.setText(_translate("SelectDataset", "Down", None))
        self.labelMergedName.setText(_translate("SelectDataset", "&Dataset Names (separated by ;):", None))
        self.pushButtonOk.setText(_translate("SelectDataset", "Ok", None))
        self.pushButtonCancel.setText(_translate("SelectDataset", "Cancel", None))

