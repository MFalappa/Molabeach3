# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sleep_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 633)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(60, 15, 501, 316))
        self.tabWidget.setStyleSheet("background: rgba(252, 44, 7, 133)")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setStyleSheet("background: rgb(234, 231, 255)")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.diurnal_ratio_wake = QtWidgets.QCheckBox(self.tab)
        self.diurnal_ratio_wake.setObjectName("diurnal_ratio_wake")
        self.verticalLayout.addWidget(self.diurnal_ratio_wake)
        self.diurnal_ratio_sleep = QtWidgets.QCheckBox(self.tab)
        self.diurnal_ratio_sleep.setObjectName("diurnal_ratio_sleep")
        self.verticalLayout.addWidget(self.diurnal_ratio_sleep)
        self.diurnal_ratio_nrem = QtWidgets.QCheckBox(self.tab)
        self.diurnal_ratio_nrem.setObjectName("diurnal_ratio_nrem")
        self.verticalLayout.addWidget(self.diurnal_ratio_nrem)
        self.diurnal_ratio_rem = QtWidgets.QCheckBox(self.tab)
        self.diurnal_ratio_rem.setObjectName("diurnal_ratio_rem")
        self.verticalLayout.addWidget(self.diurnal_ratio_rem)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setStyleSheet("background: rgb(234, 231, 255)")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.timecourse_wake = QtWidgets.QCheckBox(self.tab)
        self.timecourse_wake.setObjectName("timecourse_wake")
        self.verticalLayout_3.addWidget(self.timecourse_wake)
        self.timecourse_sleep = QtWidgets.QCheckBox(self.tab)
        self.timecourse_sleep.setObjectName("timecourse_sleep")
        self.verticalLayout_3.addWidget(self.timecourse_sleep)
        self.timecourse_nrem = QtWidgets.QCheckBox(self.tab)
        self.timecourse_nrem.setObjectName("timecourse_nrem")
        self.verticalLayout_3.addWidget(self.timecourse_nrem)
        self.timecourse_rem = QtWidgets.QCheckBox(self.tab)
        self.timecourse_rem.setObjectName("timecourse_rem")
        self.verticalLayout_3.addWidget(self.timecourse_rem)
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_3.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_3.addWidget(self.checkBox_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setStyleSheet("background: rgb(234, 231, 255)")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.cycle_sleep = QtWidgets.QCheckBox(self.tab)
        self.cycle_sleep.setObjectName("cycle_sleep")
        self.verticalLayout_4.addWidget(self.cycle_sleep)
        self.cycle_nrem = QtWidgets.QCheckBox(self.tab)
        self.cycle_nrem.setObjectName("cycle_nrem")
        self.verticalLayout_4.addWidget(self.cycle_nrem)
        self.cycle_rem = QtWidgets.QCheckBox(self.tab)
        self.cycle_rem.setObjectName("cycle_rem")
        self.verticalLayout_4.addWidget(self.cycle_rem)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setStyleSheet("background: rgb(234, 231, 255)")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.power_wake = QtWidgets.QCheckBox(self.tab)
        self.power_wake.setObjectName("power_wake")
        self.verticalLayout_2.addWidget(self.power_wake)
        self.power_nrem = QtWidgets.QCheckBox(self.tab)
        self.power_nrem.setObjectName("power_nrem")
        self.verticalLayout_2.addWidget(self.power_nrem)
        self.power_rem = QtWidgets.QCheckBox(self.tab)
        self.power_rem.setObjectName("power_rem")
        self.verticalLayout_2.addWidget(self.power_rem)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.show_resalts = QtWidgets.QCheckBox(self.tab)
        self.show_resalts.setObjectName("show_resalts")
        self.verticalLayout_5.addWidget(self.show_resalts)
        self.save_as_excel = QtWidgets.QCheckBox(self.tab)
        self.save_as_excel.setObjectName("save_as_excel")
        self.verticalLayout_5.addWidget(self.save_as_excel)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setStyleSheet("background: rgb(255, 255, 255)")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setStyleSheet("background: rgb(4, 69, 255)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.tabWidget.addTab(self.tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Diurnal ratio"))
        self.diurnal_ratio_wake.setText(_translate("MainWindow", "Wake"))
        self.diurnal_ratio_sleep.setText(_translate("MainWindow", "Total Sleep"))
        self.diurnal_ratio_nrem.setText(_translate("MainWindow", "Non REM"))
        self.diurnal_ratio_rem.setText(_translate("MainWindow", "REM"))
        self.label_4.setText(_translate("MainWindow", "Time course"))
        self.timecourse_wake.setText(_translate("MainWindow", "Wake"))
        self.timecourse_sleep.setText(_translate("MainWindow", "Total Sleep"))
        self.timecourse_nrem.setText(_translate("MainWindow", "Non REM"))
        self.timecourse_rem.setText(_translate("MainWindow", "REM"))
        self.checkBox.setText(_translate("MainWindow", "Delta power"))
        self.checkBox_2.setText(_translate("MainWindow", "Theta power"))
        self.label_2.setText(_translate("MainWindow", "Cycles duration"))
        self.cycle_sleep.setText(_translate("MainWindow", "Total Sleep"))
        self.cycle_nrem.setText(_translate("MainWindow", "Non REM"))
        self.cycle_rem.setText(_translate("MainWindow", "REM"))
        self.label_3.setText(_translate("MainWindow", "Power density"))
        self.power_wake.setText(_translate("MainWindow", "Wake"))
        self.power_nrem.setText(_translate("MainWindow", "Non REM"))
        self.power_rem.setText(_translate("MainWindow", "REM"))
        self.show_resalts.setText(_translate("MainWindow", "Show results"))
        self.save_as_excel.setText(_translate("MainWindow", "Save excel"))
        self.pushButton.setText(_translate("MainWindow", "Close"))
        self.pushButton_2.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Sleep Analysis"))
