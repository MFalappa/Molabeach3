# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'behav_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(140, 40, 415, 299))
        self.tabWidget.setStyleSheet("background-color: rgba(27, 206, 10, 92);")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.error_rate_single = QtWidgets.QCheckBox(self.tab)
        self.error_rate_single.setObjectName("error_rate_single")
        self.verticalLayout.addWidget(self.error_rate_single)
        self.checkBox_ait = QtWidgets.QCheckBox(self.tab)
        self.checkBox_ait.setObjectName("checkBox_ait")
        self.verticalLayout.addWidget(self.checkBox_ait)
        self.checkBox_peak = QtWidgets.QCheckBox(self.tab)
        self.checkBox_peak.setObjectName("checkBox_peak")
        self.verticalLayout.addWidget(self.checkBox_peak)
        self.checkBox_raster = QtWidgets.QCheckBox(self.tab)
        self.checkBox_raster.setObjectName("checkBox_raster")
        self.verticalLayout.addWidget(self.checkBox_raster)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.error_rate_gruop = QtWidgets.QCheckBox(self.tab)
        self.error_rate_gruop.setObjectName("error_rate_gruop")
        self.verticalLayout_2.addWidget(self.error_rate_gruop)
        self.checkBox_switch = QtWidgets.QCheckBox(self.tab)
        self.checkBox_switch.setObjectName("checkBox_switch")
        self.verticalLayout_2.addWidget(self.checkBox_switch)
        self.checkBox_attentional = QtWidgets.QCheckBox(self.tab)
        self.checkBox_attentional.setObjectName("checkBox_attentional")
        self.verticalLayout_2.addWidget(self.checkBox_attentional)
        self.checkBox_food = QtWidgets.QCheckBox(self.tab)
        self.checkBox_food.setObjectName("checkBox_food")
        self.verticalLayout_2.addWidget(self.checkBox_food)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.checkBox_actogram = QtWidgets.QCheckBox(self.tab)
        self.checkBox_actogram.setObjectName("checkBox_actogram")
        self.verticalLayout_3.addWidget(self.checkBox_actogram)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBox_plot = QtWidgets.QCheckBox(self.tab)
        self.checkBox_plot.setObjectName("checkBox_plot")
        self.verticalLayout_4.addWidget(self.checkBox_plot)
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_4.addWidget(self.checkBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_run = QtWidgets.QPushButton(self.tab)
        self.pushButton_run.setStyleSheet("background:rgb(18, 64, 255)")
        self.pushButton_run.setObjectName("pushButton_run")
        self.horizontalLayout_3.addWidget(self.pushButton_run)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
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
        self.label.setText(_translate("MainWindow", "Single subject"))
        self.error_rate_single.setText(_translate("MainWindow", "Error Rate"))
        self.checkBox_ait.setText(_translate("MainWindow", "AIT"))
        self.checkBox_peak.setText(_translate("MainWindow", "Peak procedure"))
        self.checkBox_raster.setText(_translate("MainWindow", "Raster"))
        self.label_2.setText(_translate("MainWindow", "Groups"))
        self.error_rate_gruop.setText(_translate("MainWindow", "Error Rate"))
        self.checkBox_switch.setText(_translate("MainWindow", "Switch"))
        self.checkBox_attentional.setText(_translate("MainWindow", "Attentional"))
        self.checkBox_food.setText(_translate("MainWindow", "Food intake"))
        self.label_3.setText(_translate("MainWindow", "Circadian"))
        self.checkBox_actogram.setText(_translate("MainWindow", "Actogram"))
        self.checkBox_plot.setText(_translate("MainWindow", "Show results"))
        self.checkBox.setText(_translate("MainWindow", "Save as excel"))
        self.pushButton.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_run.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Behaviour analysis"))

