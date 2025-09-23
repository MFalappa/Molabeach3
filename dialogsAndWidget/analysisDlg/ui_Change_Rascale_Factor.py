# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Change_Rascale_Factor.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TimeScaledlg(object):
    def setupUi(self, TimeScaledlg):
        TimeScaledlg.setObjectName("TimeScaledlg")
        TimeScaledlg.resize(354, 173)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(TimeScaledlg)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.previewLabel = QtWidgets.QLabel(TimeScaledlg)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.previewLabel.setFont(font)
        self.previewLabel.setObjectName("previewLabel")
        self.horizontalLayout_3.addWidget(self.previewLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelText1 = QtWidgets.QLabel(TimeScaledlg)
        self.labelText1.setObjectName("labelText1")
        self.horizontalLayout.addWidget(self.labelText1)
        self.scaleLabel = QtWidgets.QLabel(TimeScaledlg)
        self.scaleLabel.setObjectName("scaleLabel")
        self.horizontalLayout.addWidget(self.scaleLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(TimeScaledlg)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(TimeScaledlg)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(TimeScaledlg)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_4.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(TimeScaledlg)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout_4.addWidget(self.pushButtonApply)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(TimeScaledlg)
        QtCore.QMetaObject.connectSlotsByName(TimeScaledlg)

    def retranslateUi(self, TimeScaledlg):
        _translate = QtCore.QCoreApplication.translate
        TimeScaledlg.setWindowTitle(_translate("TimeScaledlg", "Dialog"))
        self.previewLabel.setText(_translate("TimeScaledlg", "Change default rescaling factor:"))
        self.labelText1.setText(_translate("TimeScaledlg", "Old rescaling factor:"))
        self.scaleLabel.setText(_translate("TimeScaledlg", "TextLabel"))
        self.label.setText(_translate("TimeScaledlg", "New rescaling factor:"))
        self.pushButtonCancel.setText(_translate("TimeScaledlg", "Cancel"))
        self.pushButtonApply.setText(_translate("TimeScaledlg", "Apply"))

