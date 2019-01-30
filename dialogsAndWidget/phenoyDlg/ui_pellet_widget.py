# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pellet_widget.ui'
#
# Created: Tue Mar 24 10:54:07 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtWidgets.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_pellet_widget(object):
    def setupUi(self, pellet_widget):
        pellet_widget.setObjectName(_fromUtf8("pellet_widget"))
        pellet_widget.resize(223, 116)
        self.horizontalLayout = QtWidgets.QHBoxLayout(pellet_widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_pellet = QtWidgets.QGroupBox(pellet_widget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_pellet.setFont(font)
        self.groupBox_pellet.setObjectName(_fromUtf8("groupBox_pellet"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_pellet)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtWidgets.QLabel(self.groupBox_pellet)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_pelletnum = QtWidgets.QLabel(self.groupBox_pellet)
        self.label_pelletnum.setObjectName(_fromUtf8("label_pelletnum"))
        self.horizontalLayout_2.addWidget(self.label_pelletnum)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.groupBox_pellet)

        self.retranslateUi(pellet_widget)
        QtCore.QMetaObject.connectSlotsByName(pellet_widget)

    def retranslateUi(self, pellet_widget):
        pellet_widget.setWindowTitle(_translate("pellet_widget", "Form", None))
        self.groupBox_pellet.setTitle(_translate("pellet_widget", "Pellet / Trial  Side", None))
        self.label_2.setText(_translate("pellet_widget", "Tot Pellet: ", None))
        self.label_pelletnum.setText(_translate("pellet_widget", "TextLabel", None))

