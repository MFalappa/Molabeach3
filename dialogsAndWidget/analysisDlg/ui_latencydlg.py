# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'latencydlg.ui'
#
# Created: Tue Jan 14 12:23:27 2014
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

class Ui_ExtractLatency(object):
    def setupUi(self, ExtractLatency):
        ExtractLatency.setObjectName(_fromUtf8("ExtractLatency"))
        ExtractLatency.resize(653, 462)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ExtractLatency)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(ExtractLatency)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.label_2 = QtGui.QLabel(ExtractLatency)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(ExtractLatency)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.InOutAllCombo = QtGui.QComboBox(ExtractLatency)
        self.InOutAllCombo.setObjectName(_fromUtf8("InOutAllCombo"))
        self.InOutAllCombo.addItem(_fromUtf8(""))
        self.InOutAllCombo.addItem(_fromUtf8(""))
        self.InOutAllCombo.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.InOutAllCombo)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(ExtractLatency)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.timeStampsComboBox0 = QtGui.QComboBox(ExtractLatency)
        self.timeStampsComboBox0.setObjectName(_fromUtf8("timeStampsComboBox0"))
        self.horizontalLayout.addWidget(self.timeStampsComboBox0)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(ExtractLatency)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.timeStampsComboBox1 = QtGui.QComboBox(ExtractLatency)
        self.timeStampsComboBox1.setObjectName(_fromUtf8("timeStampsComboBox1"))
        self.horizontalLayout_4.addWidget(self.timeStampsComboBox1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_6 = QtGui.QLabel(ExtractLatency)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(ExtractLatency)
        self.doubleSpinBox.setMaximum(99999.99)
        self.doubleSpinBox.setProperty("value", 30.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.horizontalLayout_5.addWidget(self.doubleSpinBox)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ExtractLatency)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ExtractLatency)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExtractLatency.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExtractLatency.reject)
        QtCore.QMetaObject.connectSlotsByName(ExtractLatency)

    def retranslateUi(self, ExtractLatency):
        ExtractLatency.setWindowTitle(_translate("ExtractLatency", "Extract Latency", None))
        self.label.setText(_translate("ExtractLatency", "Selected Dataset:", None))
        self.label_2.setText(_translate("ExtractLatency", "Dataset", None))
        self.label_5.setText(_translate("ExtractLatency", "Extract from:", None))
        self.InOutAllCombo.setItemText(0, _translate("ExtractLatency", "All Dataset", None))
        self.InOutAllCombo.setItemText(1, _translate("ExtractLatency", "Inside Trial", None))
        self.InOutAllCombo.setItemText(2, _translate("ExtractLatency", "Outside Trial", None))
        self.label_3.setText(_translate("ExtractLatency", "Trial Start:", None))
        self.label_4.setText(_translate("ExtractLatency", "Trial End:", None))
        self.label_6.setText(_translate("ExtractLatency", "Max Trial Duration", None))

