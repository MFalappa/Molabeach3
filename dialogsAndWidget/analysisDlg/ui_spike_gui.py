# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spike_gui.ui'
#
# Created: Mon Jun 19 17:37:42 2017
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1055, 860)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(11, 12, 1001, 751))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_13.setMargin(0)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.scrollArea = QtGui.QScrollArea(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMaximumSize(QtCore.QSize(300, 780))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 278, 747))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_16 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
        self.label_11 = QtGui.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.verticalLayout_16.addWidget(self.label_11)
        self.treeWidget_channel = QtGui.QTreeWidget(self.scrollAreaWidgetContents)
        self.treeWidget_channel.setEnabled(True)
        self.treeWidget_channel.setMaximumSize(QtCore.QSize(300, 1000))
        self.treeWidget_channel.setObjectName(_fromUtf8("treeWidget_channel"))
        self.treeWidget_channel.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_16.addWidget(self.treeWidget_channel)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton_save = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.horizontalLayout_4.addWidget(self.pushButton_save)
        self.verticalLayout_16.addLayout(self.horizontalLayout_4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_13.addWidget(self.scrollArea)
        self.verticalLayout_17 = QtGui.QVBoxLayout()
        self.verticalLayout_17.setObjectName(_fromUtf8("verticalLayout_17"))
        self.scrollArea_2 = QtGui.QScrollArea(self.widget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 708, 708))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.tabWidget = QtGui.QTabWidget(self.scrollAreaWidgetContents_3)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 741, 341))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 105, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.tabWidget.setPalette(palette)
        self.tabWidget.setStyleSheet(_fromUtf8("background-color: rgb(65, 105, 255);\n"
""))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.layoutWidget = QtGui.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 462, 180))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_12.setMargin(0)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.verticalLayout_30 = QtGui.QVBoxLayout()
        self.verticalLayout_30.setObjectName(_fromUtf8("verticalLayout_30"))
        self.verticalLayout_27 = QtGui.QVBoxLayout()
        self.verticalLayout_27.setObjectName(_fromUtf8("verticalLayout_27"))
        self.Waveforms = QtGui.QLabel(self.layoutWidget)
        self.Waveforms.setObjectName(_fromUtf8("Waveforms"))
        self.verticalLayout_27.addWidget(self.Waveforms)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioButton_singleWaforms = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_singleWaforms.setObjectName(_fromUtf8("radioButton_singleWaforms"))
        self.verticalLayout_2.addWidget(self.radioButton_singleWaforms)
        self.radioButton_mean = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_mean.setObjectName(_fromUtf8("radioButton_mean"))
        self.verticalLayout_2.addWidget(self.radioButton_mean)
        self.verticalLayout_27.addLayout(self.verticalLayout_2)
        self.verticalLayout_30.addLayout(self.verticalLayout_27)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_30.addItem(spacerItem1)
        self.horizontalLayout_12.addLayout(self.verticalLayout_30)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem2)
        self.groupBox_3 = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_29 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_29.setObjectName(_fromUtf8("verticalLayout_29"))
        self.radioButton = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.verticalLayout_29.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.verticalLayout_29.addWidget(self.radioButton_2)
        self.horizontalLayout_12.addWidget(self.groupBox_3)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem3)
        self.groupBox_4 = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_28 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_28.setObjectName(_fromUtf8("verticalLayout_28"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_20 = QtGui.QLabel(self.groupBox_4)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.horizontalLayout_7.addWidget(self.label_20)
        self.comboBox_unit1 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_unit1.setObjectName(_fromUtf8("comboBox_unit1"))
        self.horizontalLayout_7.addWidget(self.comboBox_unit1)
        self.verticalLayout_28.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_21 = QtGui.QLabel(self.groupBox_4)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.horizontalLayout_8.addWidget(self.label_21)
        self.comboBox_unit2 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_unit2.setObjectName(_fromUtf8("comboBox_unit2"))
        self.horizontalLayout_8.addWidget(self.comboBox_unit2)
        self.verticalLayout_28.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_22 = QtGui.QLabel(self.groupBox_4)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.horizontalLayout_9.addWidget(self.label_22)
        self.comboBox_unit3 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_unit3.setObjectName(_fromUtf8("comboBox_unit3"))
        self.horizontalLayout_9.addWidget(self.comboBox_unit3)
        self.verticalLayout_28.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_23 = QtGui.QLabel(self.groupBox_4)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.horizontalLayout_10.addWidget(self.label_23)
        self.comboBox_unit4 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_unit4.setObjectName(_fromUtf8("comboBox_unit4"))
        self.horizontalLayout_10.addWidget(self.comboBox_unit4)
        self.verticalLayout_28.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_24 = QtGui.QLabel(self.groupBox_4)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.horizontalLayout_11.addWidget(self.label_24)
        self.comboBox_unit5 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_unit5.setObjectName(_fromUtf8("comboBox_unit5"))
        self.horizontalLayout_11.addWidget(self.comboBox_unit5)
        self.verticalLayout_28.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12.addWidget(self.groupBox_4)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_date_time = QtGui.QWidget()
        self.tab_date_time.setObjectName(_fromUtf8("tab_date_time"))
        self.layoutWidget1 = QtGui.QWidget(self.tab_date_time)
        self.layoutWidget1.setGeometry(QtCore.QRect(11, 10, 655, 289))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.groupBox = QtGui.QGroupBox(self.layoutWidget1)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.radioButton_nothing = QtGui.QRadioButton(self.groupBox)
        self.radioButton_nothing.setObjectName(_fromUtf8("radioButton_nothing"))
        self.verticalLayout_5.addWidget(self.radioButton_nothing)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.radioButton_sleep = QtGui.QRadioButton(self.groupBox)
        self.radioButton_sleep.setObjectName(_fromUtf8("radioButton_sleep"))
        self.verticalLayout_5.addWidget(self.radioButton_sleep)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem5)
        self.radioButton_behaviour = QtGui.QRadioButton(self.groupBox)
        self.radioButton_behaviour.setObjectName(_fromUtf8("radioButton_behaviour"))
        self.verticalLayout_5.addWidget(self.radioButton_behaviour)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem6)
        self.radioButton_external = QtGui.QRadioButton(self.groupBox)
        self.radioButton_external.setObjectName(_fromUtf8("radioButton_external"))
        self.verticalLayout_5.addWidget(self.radioButton_external)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.verticalLayout_23 = QtGui.QVBoxLayout()
        self.verticalLayout_23.setObjectName(_fromUtf8("verticalLayout_23"))
        self.groupBox_2 = QtGui.QGroupBox(self.layoutWidget1)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.radioButton_psth = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_psth.setObjectName(_fromUtf8("radioButton_psth"))
        self.verticalLayout_3.addWidget(self.radioButton_psth)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem7)
        self.radioButton_raster = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_raster.setObjectName(_fromUtf8("radioButton_raster"))
        self.verticalLayout_3.addWidget(self.radioButton_raster)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem8)
        self.radioButton_raw = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_raw.setObjectName(_fromUtf8("radioButton_raw"))
        self.verticalLayout_3.addWidget(self.radioButton_raw)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_23.addWidget(self.groupBox_2)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_23.addItem(spacerItem9)
        self.horizontalLayout_6.addLayout(self.verticalLayout_23)
        self.verticalLayout_24 = QtGui.QVBoxLayout()
        self.verticalLayout_24.setObjectName(_fromUtf8("verticalLayout_24"))
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_9.addWidget(self.label_4)
        self.label_19 = QtGui.QLabel(self.layoutWidget1)
        self.label_19.setText(_fromUtf8(""))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.verticalLayout_9.addWidget(self.label_19)
        self.doubleSpinBox_binning = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.doubleSpinBox_binning.setObjectName(_fromUtf8("doubleSpinBox_binning"))
        self.verticalLayout_9.addWidget(self.doubleSpinBox_binning)
        self.verticalLayout_24.addLayout(self.verticalLayout_9)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_24.addItem(spacerItem10)
        self.horizontalLayout_6.addLayout(self.verticalLayout_24)
        self.verticalLayout_25 = QtGui.QVBoxLayout()
        self.verticalLayout_25.setObjectName(_fromUtf8("verticalLayout_25"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_range = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_range.setFont(font)
        self.label_range.setObjectName(_fromUtf8("label_range"))
        self.verticalLayout.addWidget(self.label_range)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_min = QtGui.QLabel(self.layoutWidget1)
        self.label_min.setObjectName(_fromUtf8("label_min"))
        self.verticalLayout_7.addWidget(self.label_min)
        self.doubleSpinBox_min = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.doubleSpinBox_min.setObjectName(_fromUtf8("doubleSpinBox_min"))
        self.verticalLayout_7.addWidget(self.doubleSpinBox_min)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label_max = QtGui.QLabel(self.layoutWidget1)
        self.label_max.setObjectName(_fromUtf8("label_max"))
        self.verticalLayout_8.addWidget(self.label_max)
        self.doubleSpinBox_max = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.doubleSpinBox_max.setObjectName(_fromUtf8("doubleSpinBox_max"))
        self.verticalLayout_8.addWidget(self.doubleSpinBox_max)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_25.addLayout(self.verticalLayout)
        spacerItem11 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_25.addItem(spacerItem11)
        self.horizontalLayout_6.addLayout(self.verticalLayout_25)
        self.verticalLayout_26 = QtGui.QVBoxLayout()
        self.verticalLayout_26.setObjectName(_fromUtf8("verticalLayout_26"))
        self.verticalLayout_22 = QtGui.QVBoxLayout()
        self.verticalLayout_22.setObjectName(_fromUtf8("verticalLayout_22"))
        self.verticalLayout_12 = QtGui.QVBoxLayout()
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.label_6 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_12.addWidget(self.label_6)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_10.addWidget(self.label_2)
        self.timeEdit_start_spike = QtGui.QTimeEdit(self.layoutWidget1)
        self.timeEdit_start_spike.setObjectName(_fromUtf8("timeEdit_start_spike"))
        self.verticalLayout_10.addWidget(self.timeEdit_start_spike)
        self.horizontalLayout_2.addLayout(self.verticalLayout_10)
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_11.addWidget(self.label_3)
        self.timeEdit__end_spike = QtGui.QTimeEdit(self.layoutWidget1)
        self.timeEdit__end_spike.setObjectName(_fromUtf8("timeEdit__end_spike"))
        self.verticalLayout_11.addWidget(self.timeEdit__end_spike)
        self.horizontalLayout_2.addLayout(self.verticalLayout_11)
        self.verticalLayout_12.addLayout(self.horizontalLayout_2)
        self.verticalLayout_22.addLayout(self.verticalLayout_12)
        self.verticalLayout_13 = QtGui.QVBoxLayout()
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_13.addWidget(self.label_7)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_14 = QtGui.QVBoxLayout()
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_14.addWidget(self.label_8)
        self.timeEdit_start_sleep = QtGui.QTimeEdit(self.layoutWidget1)
        self.timeEdit_start_sleep.setObjectName(_fromUtf8("timeEdit_start_sleep"))
        self.verticalLayout_14.addWidget(self.timeEdit_start_sleep)
        self.horizontalLayout_3.addLayout(self.verticalLayout_14)
        self.label_9 = QtGui.QLabel(self.layoutWidget1)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        self.verticalLayout_15 = QtGui.QVBoxLayout()
        self.verticalLayout_15.setObjectName(_fromUtf8("verticalLayout_15"))
        self.label_10 = QtGui.QLabel(self.layoutWidget1)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_15.addWidget(self.label_10)
        self.timeEdit__end_sleep = QtGui.QTimeEdit(self.layoutWidget1)
        self.timeEdit__end_sleep.setObjectName(_fromUtf8("timeEdit__end_sleep"))
        self.verticalLayout_15.addWidget(self.timeEdit__end_sleep)
        self.horizontalLayout_3.addLayout(self.verticalLayout_15)
        self.verticalLayout_13.addLayout(self.horizontalLayout_3)
        self.verticalLayout_22.addLayout(self.verticalLayout_13)
        self.verticalLayout_19 = QtGui.QVBoxLayout()
        self.verticalLayout_19.setObjectName(_fromUtf8("verticalLayout_19"))
        self.label_15 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.verticalLayout_19.addWidget(self.label_15)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout_20 = QtGui.QVBoxLayout()
        self.verticalLayout_20.setObjectName(_fromUtf8("verticalLayout_20"))
        self.label_16 = QtGui.QLabel(self.layoutWidget1)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_20.addWidget(self.label_16)
        self.timeEdit_start_sleep_3 = QtGui.QTimeEdit(self.layoutWidget1)
        self.timeEdit_start_sleep_3.setObjectName(_fromUtf8("timeEdit_start_sleep_3"))
        self.verticalLayout_20.addWidget(self.timeEdit_start_sleep_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_20)
        self.label_17 = QtGui.QLabel(self.layoutWidget1)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_5.addWidget(self.label_17)
        self.verticalLayout_21 = QtGui.QVBoxLayout()
        self.verticalLayout_21.setObjectName(_fromUtf8("verticalLayout_21"))
        self.label_18 = QtGui.QLabel(self.layoutWidget1)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.verticalLayout_21.addWidget(self.label_18)
        self.timeEdit__end_sleep_3 = QtGui.QTimeEdit(self.layoutWidget1)
        self.timeEdit__end_sleep_3.setObjectName(_fromUtf8("timeEdit__end_sleep_3"))
        self.verticalLayout_21.addWidget(self.timeEdit__end_sleep_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_21)
        self.verticalLayout_19.addLayout(self.horizontalLayout_5)
        self.verticalLayout_22.addLayout(self.verticalLayout_19)
        self.verticalLayout_26.addLayout(self.verticalLayout_22)
        spacerItem12 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_26.addItem(spacerItem12)
        self.horizontalLayout_6.addLayout(self.verticalLayout_26)
        self.tabWidget.addTab(self.tab_date_time, _fromUtf8(""))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_17.addWidget(self.scrollArea_2)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem13)
        self.pushButton_cancel = QtGui.QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout_14.addWidget(self.pushButton_cancel)
        self.pushButton_done = QtGui.QPushButton(self.widget)
        self.pushButton_done.setObjectName(_fromUtf8("pushButton_done"))
        self.horizontalLayout_14.addWidget(self.pushButton_done)
        self.verticalLayout_17.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_13.addLayout(self.verticalLayout_17)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1055, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_11.setText(_translate("MainWindow", "Select Channel:", None))
        self.pushButton_save.setText(_translate("MainWindow", "Save", None))
        self.Waveforms.setText(_translate("MainWindow", "Waveforms", None))
        self.radioButton_singleWaforms.setText(_translate("MainWindow", "Single waveforms", None))
        self.radioButton_mean.setText(_translate("MainWindow", "Mean", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Cluster", None))
        self.radioButton.setText(_translate("MainWindow", "PCA", None))
        self.radioButton_2.setText(_translate("MainWindow", "LDA", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Color", None))
        self.label_20.setText(_translate("MainWindow", "Unit 1", None))
        self.label_21.setText(_translate("MainWindow", "Unit 2", None))
        self.label_22.setText(_translate("MainWindow", "Unit 3", None))
        self.label_23.setText(_translate("MainWindow", "Unit 4", None))
        self.label_24.setText(_translate("MainWindow", "Unit 5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Sorting", None))
        self.groupBox.setTitle(_translate("MainWindow", "Events", None))
        self.radioButton_nothing.setText(_translate("MainWindow", "None", None))
        self.radioButton_sleep.setText(_translate("MainWindow", "Sleep", None))
        self.radioButton_behaviour.setText(_translate("MainWindow", "Behaviour", None))
        self.radioButton_external.setText(_translate("MainWindow", "External trigger", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Plot", None))
        self.radioButton_psth.setText(_translate("MainWindow", "PSTH", None))
        self.radioButton_raster.setText(_translate("MainWindow", "Raster", None))
        self.radioButton_raw.setText(_translate("MainWindow", "Raw", None))
        self.label_4.setText(_translate("MainWindow", "Binning", None))
        self.label_range.setText(_translate("MainWindow", "Range", None))
        self.label_min.setText(_translate("MainWindow", "min", None))
        self.label.setText(_translate("MainWindow", "-", None))
        self.label_max.setText(_translate("MainWindow", "max", None))
        self.label_6.setText(_translate("MainWindow", "Spikes", None))
        self.label_2.setText(_translate("MainWindow", "Start", None))
        self.label_5.setText(_translate("MainWindow", "-", None))
        self.label_3.setText(_translate("MainWindow", "Stop", None))
        self.label_7.setText(_translate("MainWindow", "Sleep", None))
        self.label_8.setText(_translate("MainWindow", "Start", None))
        self.label_9.setText(_translate("MainWindow", "-", None))
        self.label_10.setText(_translate("MainWindow", "Stop", None))
        self.label_15.setText(_translate("MainWindow", "Behaviour", None))
        self.label_16.setText(_translate("MainWindow", "Start", None))
        self.label_17.setText(_translate("MainWindow", "-", None))
        self.label_18.setText(_translate("MainWindow", "Stop", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_date_time), _translate("MainWindow", "Single Unit", None))
        self.pushButton_cancel.setText(_translate("MainWindow", "Cancel", None))
        self.pushButton_done.setText(_translate("MainWindow", "Done", None))

