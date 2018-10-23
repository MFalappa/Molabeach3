# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Change_Rascale_Factor.ui'
#
# Created: Tue May 27 16:42:26 2014
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

class Ui_TimeScaledlg(object):
    def setupUi(self, TimeScaledlg):
        TimeScaledlg.setObjectName(_fromUtf8("TimeScaledlg"))
        TimeScaledlg.resize(354, 173)
        self.verticalLayout_3 = QtGui.QVBoxLayout(TimeScaledlg)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.previewLabel = QtGui.QLabel(TimeScaledlg)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.previewLabel.setFont(font)
        self.previewLabel.setObjectName(_fromUtf8("previewLabel"))
        self.horizontalLayout_3.addWidget(self.previewLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelText1 = QtGui.QLabel(TimeScaledlg)
        self.labelText1.setObjectName(_fromUtf8("labelText1"))
        self.horizontalLayout.addWidget(self.labelText1)
        self.scaleLabel = QtGui.QLabel(TimeScaledlg)
        self.scaleLabel.setObjectName(_fromUtf8("scaleLabel"))
        self.horizontalLayout.addWidget(self.scaleLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(TimeScaledlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(TimeScaledlg)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pushButtonCancel = QtGui.QPushButton(TimeScaledlg)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout_4.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtGui.QPushButton(TimeScaledlg)
        self.pushButtonApply.setObjectName(_fromUtf8("pushButtonApply"))
        self.horizontalLayout_4.addWidget(self.pushButtonApply)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(TimeScaledlg)
        QtCore.QMetaObject.connectSlotsByName(TimeScaledlg)

    def retranslateUi(self, TimeScaledlg):
        TimeScaledlg.setWindowTitle(_translate("TimeScaledlg", "Dialog", None))
        self.previewLabel.setText(_translate("TimeScaledlg", "Change default rescaling factor:", None))
        self.labelText1.setText(_translate("TimeScaledlg", "Old rescaling factor:", None))
        self.scaleLabel.setText(_translate("TimeScaledlg", "TextLabel", None))
        self.label.setText(_translate("TimeScaledlg", "New rescaling factor:", None))
        self.pushButtonCancel.setText(_translate("TimeScaledlg", "Cancel", None))
        self.pushButtonApply.setText(_translate("TimeScaledlg", "Apply", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TimeScaledlg = QtGui.QDialog()
    ui = Ui_TimeScaledlg()
    ui.setupUi(TimeScaledlg)
    TimeScaledlg.show()
    sys.exit(app.exec_())

