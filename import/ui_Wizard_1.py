# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Wizard_1.ui'
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

class Ui_newAnalysis(object):
    def setupUi(self, newAnalysis):
        newAnalysis.setObjectName(_fromUtf8("newAnalysis"))
        newAnalysis.resize(501, 392)
        self.horizontalLayout_8 = QtGui.QHBoxLayout(newAnalysis)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_1 = QtGui.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setObjectName(_fromUtf8("radioButton_1"))
        self.verticalLayout.addWidget(self.radioButton_1)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.verticalLayout.addWidget(self.radioButton_2)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_analysis = QtGui.QLineEdit(newAnalysis)
        self.lineEdit_analysis.setObjectName(_fromUtf8("lineEdit_analysis"))
        self.horizontalLayout_2.addWidget(self.lineEdit_analysis)
        self.pushButton_analysis = QtGui.QPushButton(newAnalysis)
        self.pushButton_analysis.setObjectName(_fromUtf8("pushButton_analysis"))
        self.horizontalLayout_2.addWidget(self.pushButton_analysis)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(newAnalysis)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lineEdit_plotting = QtGui.QLineEdit(newAnalysis)
        self.lineEdit_plotting.setObjectName(_fromUtf8("lineEdit_plotting"))
        self.horizontalLayout_4.addWidget(self.lineEdit_plotting)
        self.pushButton_plotting = QtGui.QPushButton(newAnalysis)
        self.pushButton_plotting.setObjectName(_fromUtf8("pushButton_plotting"))
        self.horizontalLayout_4.addWidget(self.pushButton_plotting)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.pushButton_2 = QtGui.QPushButton(newAnalysis)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_7.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(newAnalysis)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_7.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)

        self.retranslateUi(newAnalysis)
        QtCore.QMetaObject.connectSlotsByName(newAnalysis)

    def retranslateUi(self, newAnalysis):
        newAnalysis.setWindowTitle(_translate("newAnalysis", "New analysis wizard", None))
        self.groupBox.setTitle(_translate("newAnalysis", "Analysis Type:", None))
        self.radioButton.setText(_translate("newAnalysis", "Single subject", None))
        self.radioButton_1.setText(_translate("newAnalysis", "Group", None))
        self.radioButton_2.setText(_translate("newAnalysis", "Integrative", None))
        self.label_2.setText(_translate("newAnalysis", "Path to analysis function:", None))
        self.pushButton_analysis.setText(_translate("newAnalysis", "Browse...", None))
        self.label.setText(_translate("newAnalysis", "Path to plotting function:", None))
        self.pushButton_plotting.setText(_translate("newAnalysis", "Browse...", None))
        self.pushButton_2.setText(_translate("newAnalysis", "Cancel", None))
        self.pushButton.setText(_translate("newAnalysis", "Continue", None))

