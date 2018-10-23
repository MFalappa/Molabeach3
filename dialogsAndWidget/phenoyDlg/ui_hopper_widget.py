# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hopper_widget.ui'
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

class Ui_hopper_widget(object):
    def setupUi(self, hopper_widget):
        hopper_widget.setObjectName(_fromUtf8("hopper_widget"))
        hopper_widget.resize(196, 169)
        self.verticalLayout = QtGui.QVBoxLayout(hopper_widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_hopper = QtGui.QGroupBox(hopper_widget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_hopper.setFont(font)
        self.groupBox_hopper.setObjectName(_fromUtf8("groupBox_hopper"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_hopper)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_empty = QtGui.QLabel(self.groupBox_hopper)
        self.label_empty.setObjectName(_fromUtf8("label_empty"))
        self.verticalLayout_2.addWidget(self.label_empty)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(self.groupBox_hopper)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.label_light = QtGui.QLabel(self.groupBox_hopper)
        self.label_light.setAlignment(QtCore.Qt.AlignCenter)
        self.label_light.setObjectName(_fromUtf8("label_light"))
        self.horizontalLayout_4.addWidget(self.label_light)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.groupBox_hopper)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.label_noise = QtGui.QLabel(self.groupBox_hopper)
        self.label_noise.setAlignment(QtCore.Qt.AlignCenter)
        self.label_noise.setObjectName(_fromUtf8("label_noise"))
        self.horizontalLayout_3.addWidget(self.label_noise)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(self.groupBox_hopper)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_NP = QtGui.QLabel(self.groupBox_hopper)
        self.label_NP.setAlignment(QtCore.Qt.AlignCenter)
        self.label_NP.setObjectName(_fromUtf8("label_NP"))
        self.horizontalLayout_2.addWidget(self.label_NP)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.groupBox_hopper)

        self.retranslateUi(hopper_widget)
        QtCore.QMetaObject.connectSlotsByName(hopper_widget)

    def retranslateUi(self, hopper_widget):
        hopper_widget.setWindowTitle(_translate("hopper_widget", "Form", None))
        self.groupBox_hopper.setTitle(_translate("hopper_widget", "Hopper Status:", None))
        self.label_empty.setText(_translate("hopper_widget", "Empty", None))
        self.label_2.setText(_translate("hopper_widget", "Light:", None))
        self.label_light.setText(_translate("hopper_widget", "TextLabel", None))
        self.label.setText(_translate("hopper_widget", "Noise:", None))
        self.label_noise.setText(_translate("hopper_widget", "TextLabel", None))
        self.label_4.setText(_translate("hopper_widget", "Nose-Poke:", None))
        self.label_NP.setText(_translate("hopper_widget", "TextLabel", None))

