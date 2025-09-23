# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Rescale_A_Dataset.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TimeScaledlg(object):
    def setupUi(self, TimeScaledlg):
        TimeScaledlg.setObjectName("TimeScaledlg")
        TimeScaledlg.resize(581, 318)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(TimeScaledlg)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.previewLabel = QtWidgets.QLabel(TimeScaledlg)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.previewLabel.setFont(font)
        self.previewLabel.setObjectName("previewLabel")
        self.horizontalLayout_5.addWidget(self.previewLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget = QtWidgets.QTableWidget(TimeScaledlg)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.tableWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelText1 = QtWidgets.QLabel(TimeScaledlg)
        self.labelText1.setObjectName("labelText1")
        self.horizontalLayout_2.addWidget(self.labelText1)
        self.scaleLabel = QtWidgets.QLabel(TimeScaledlg)
        self.scaleLabel.setObjectName("scaleLabel")
        self.horizontalLayout_2.addWidget(self.scaleLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(TimeScaledlg)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(TimeScaledlg)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(TimeScaledlg)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(TimeScaledlg)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(TimeScaledlg)
        QtCore.QMetaObject.connectSlotsByName(TimeScaledlg)

    def retranslateUi(self, TimeScaledlg):
        _translate = QtCore.QCoreApplication.translate
        TimeScaledlg.setWindowTitle(_translate("TimeScaledlg", "Dialog"))
        self.previewLabel.setText(_translate("TimeScaledlg", "Dataset Preview:"))
        self.labelText1.setText(_translate("TimeScaledlg", "Old rescaling factor:"))
        self.scaleLabel.setText(_translate("TimeScaledlg", "TextLabel"))
        self.label.setText(_translate("TimeScaledlg", "New rescaling factor:"))
        self.pushButton.setText(_translate("TimeScaledlg", "Preview"))
        self.pushButton_2.setText(_translate("TimeScaledlg", "Apply"))

