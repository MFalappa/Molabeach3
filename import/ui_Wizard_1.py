# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Wizard_1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_newAnalysis(object):
    def setupUi(self, newAnalysis):
        newAnalysis.setObjectName("newAnalysis")
        newAnalysis.resize(556, 435)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(newAnalysis)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_3.addWidget(self.radioButton)
        self.radioButton_1 = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setObjectName("radioButton_1")
        self.verticalLayout_3.addWidget(self.radioButton_1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_3.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_3.addWidget(self.radioButton_3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(newAnalysis)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.textEdit = QtWidgets.QTextEdit(newAnalysis)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_analysis = QtWidgets.QLineEdit(newAnalysis)
        self.lineEdit_analysis.setObjectName("lineEdit_analysis")
        self.horizontalLayout_3.addWidget(self.lineEdit_analysis)
        self.pushButton_analysis = QtWidgets.QPushButton(newAnalysis)
        self.pushButton_analysis.setObjectName("pushButton_analysis")
        self.horizontalLayout_3.addWidget(self.pushButton_analysis)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEdit_plotting = QtWidgets.QLineEdit(newAnalysis)
        self.lineEdit_plotting.setObjectName("lineEdit_plotting")
        self.horizontalLayout_5.addWidget(self.lineEdit_plotting)
        self.pushButton_plotting = QtWidgets.QPushButton(newAnalysis)
        self.pushButton_plotting.setObjectName("pushButton_plotting")
        self.horizontalLayout_5.addWidget(self.pushButton_plotting)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.pushButton_2 = QtWidgets.QPushButton(newAnalysis)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_6.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(newAnalysis)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_5)

        self.retranslateUi(newAnalysis)
        QtCore.QMetaObject.connectSlotsByName(newAnalysis)

    def retranslateUi(self, newAnalysis):
        _translate = QtCore.QCoreApplication.translate
        newAnalysis.setWindowTitle(_translate("newAnalysis", "New analysis wizard"))
        self.groupBox.setTitle(_translate("newAnalysis", "Analysis Type:"))
        self.radioButton.setText(_translate("newAnalysis", "Behaviour"))
        self.radioButton_1.setText(_translate("newAnalysis", "Sleep"))
        self.radioButton_2.setText(_translate("newAnalysis", "Spike"))
        self.radioButton_3.setText(_translate("newAnalysis", "Integrative"))
        self.label_3.setText(_translate("newAnalysis", "Analysis name alias:"))
        self.label_4.setText(_translate("newAnalysis", "Analysisi description:"))
        self.label_2.setText(_translate("newAnalysis", "Path to analysis function:"))
        self.pushButton_analysis.setText(_translate("newAnalysis", "Browse..."))
        self.label.setText(_translate("newAnalysis", "Path to plotting function:"))
        self.pushButton_plotting.setText(_translate("newAnalysis", "Browse..."))
        self.pushButton_2.setText(_translate("newAnalysis", "Cancel"))
        self.pushButton.setText(_translate("newAnalysis", "Continue"))

