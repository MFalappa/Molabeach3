# -*- coding: utf-8 -*-
"""
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

Copyright (C) 2017 FONDAZIONE ISTITUTO ITALIANO DI TECNOLOGIA
                   E. Balzani, M. Falappa - All rights reserved

@author: edoardo.balzani87@gmail.com; mfalappa@outlook.it

                                Publication:
         An approach to monitoring home-cage behavior in mice that 
                          facilitates data sharing
                          
        DOI: 10.1038/nprot.2018.031
          
"""
from PyQt5.QtWidgets import (QLabel,QWidget,QVBoxLayout,QSpacerItem,
                             QSizePolicy,QHBoxLayout,QGroupBox,QApplication,QDateTimeEdit)
from PyQt5.QtCore import (pyqtSignal,QDateTime,QSize,Qt,QMetaObject)
from PyQt5.QtGui import QFont,QPixmap,QImage




def _fromUtf8(s):
    return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)
import sys
import os
path_img = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'images')

from setupLightCycle import setupLightCycle


class doubleClickGroupBox(QGroupBox):
    doubleClickSignal = pyqtSignal(int,name='boxDoubleClicked')
    def __init__(self,box,string,parent=None):
        super(doubleClickGroupBox,self).__init__(string,parent=parent)
        self.box = box
    def mouseDoubleClickEvent(self,event):
        self.doubleClickSignal.emit(self.box)
        
class house_light(QWidget):
    updateDictSignal = pyqtSignal(dict, dict,dict, name='updateDict')
    def __init__(self, boxId, totBox, parent=None):
        super(house_light, self).__init__(parent)
        self.boxIdx = boxId
        self.cycleSet = False
        self.isRecording = False
        self.totBox = totBox
        self.setObjectName(_fromUtf8("house_light"))
        self.resize(521, 298)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_hopper = doubleClickGroupBox(self.boxIdx,'House Light - Box %d'%(boxId+1))

        # group box hopper
        
        
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_hopper.setFont(font)
        self.groupBox_hopper.setObjectName(_fromUtf8("groupBox_hopper"))
#        self.groupBox_hopper.doubleClickSignal.connect(self.setupLightCycle)
        # Layout cloned from .ui code
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_hopper)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_info = QLabel(self.groupBox_hopper)
        self.label_info.setObjectName(_fromUtf8("label_info"))
        self.horizontalLayout.addWidget(self.label_info)
        self.isSetLabel = QLabel(self.groupBox_hopper)
        self.isSetLabel.setObjectName(_fromUtf8("isSetLabel"))
        self.horizontalLayout.addWidget(self.isSetLabel)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_light = QLabel(self.groupBox_hopper)
        self.label_light.setAlignment(Qt.AlignCenter)
        self.label_light.setObjectName(_fromUtf8("label_light"))
        self.verticalLayout.addWidget(self.label_light)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_switch = QLabel(self.groupBox_hopper)
        self.label_switch.setObjectName(_fromUtf8("label_switch"))
        self.horizontalLayout_2.addWidget(self.label_switch)
        self.dateTimeEdit = QDateTimeEdit(self.groupBox_hopper)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.horizontalLayout_2.addWidget(self.dateTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addWidget(self.groupBox_hopper)

        self.retranslateUi(house_light)
        QMetaObject.connectSlotsByName(self)
        #############################
    
        
#        specerItem = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.lightOff = QPixmap.fromImage(QImage(os.path.join(path_img,'LightOff_50.png')))
        self.lightOff = self.lightOff.scaled(QSize(60,60))
        self.lightOn = QPixmap.fromImage(QImage(os.path.join(path_img,'LightOn_50.png')))
        self.lightOn = self.lightOn.scaled(QSize(60,60))

        self.redCircle = QPixmap.fromImage(QImage(os.path.join(path_img,'redCircle.png')))
        self.redCircle = self.redCircle.scaled(QSize(20,20))
        self.greenCircle = QPixmap.fromImage(QImage(os.path.join(path_img,'greenCircle.png')))
        self.greenCircle = self.greenCircle.scaled(QSize(20,20))
        self.recCircle = QPixmap.fromImage(QImage(os.path.join(path_img,'recCircle.png')))
        self.recCircle = self.recCircle.scaled(QSize(20,20))
        
        self.label_light.setPixmap(self.lightOff)
        self.font = QFont('',8)

        self.label_info.setPixmap(self.redCircle)
        self.isSetLabel.setText('Light cycle not set')
        
        self.dateTimeEdit.setReadOnly(True)
        
#        self.label_info.setFixedHeight(10)
#==================empty============================================================
#     SET ALL FONTS TO REDUCE FONTSIZE
#==============================================================================
        
        self.groupBox_hopper.setStyleSheet("QGroupBox { background-color: rgb(255, 255,\
            255); border:1px solid rgb(83, 84, 84); }")
       
        self.groupBox_hopper.setFixedSize(250, 169)

#        QTimer.singleShot(5100,lambda x = 'Off': self.set_icon_light(x))
#        print 'GB size',self.groupBox_hopper.size()
    
    def retranslateUi(self, house_light):
        self.setWindowTitle(_translate("house_light", "Form", None))
        self.groupBox_hopper.setTitle(_translate("house_light", "House Light - Box", None))
        self.label_info.setText(_translate("house_light", "Empty", None))
        self.isSetLabel.setText(_translate("house_light", "TextLabel", None))
        self.label_light.setText(_translate("house_light", "TextLabel", None))
        self.label_switch.setText(_translate("house_light", "Next Switch:", None))
        
    def set_icon_light(self, On_Off):
        if On_Off is 'Off':
            self.label_light.setPixmap(self.lightOff)
        else:
            self.label_light.setPixmap(self.lightOn)
    
    def set_cycle(self, boolean,dTime):
        if boolean:
            self.isSetLabel.setText('Light cycle set')
            self.label_info.setPixmap(self.greenCircle)
            self.setDateTimeEdit(dTime)
            self.cycleSet = True # cycle of timer set or not
        else:
            self.isSetLabel.setText('Light cycle not set')
            self.label_info.setPixmap(self.redCircle)
            self.cycleSet = False
    
    def setDateTimeEdit(self, dTime):
        qdtime = QDateTime(dTime.year, dTime.month, dTime.day, dTime.hour, dTime.minute, dTime.second)
        self.dateTimeEdit.setDateTime(qdtime)
        
    def set_recording(self, boolean):
        if boolean:
            self.isSetLabel.setText('Recording')
            self.label_info.setPixmap(self.recCircle)
            self.isRecording = True # cycle of timer set or not
        else:
            self.isSetLabel.setText('Light cycle not set')
            self.label_info.setPixmap(self.redCircle)
            self.isRecording = False
            self.cycleSet = False
        
    def analyze_ARDUINO_msg(self, msg):
        pass
        
    def setupLightCycle(self, box_list):
        form = setupLightCycle(self.boxIdx, box_list, parent = self)
        form.applyTimerSchedule.connect(self.updateBox)
        form.show()
    
    def updateBox(self,loopMinutes,lightStatus,switchTime):
        self.updateDictSignal.emit(loopMinutes,lightStatus,switchTime)
            

def main():
    app = QApplication(sys.argv)
    form = house_light(1,16)
    form.show()
    app.exec_()
    print(form.groupBox_hopper.size())
if __name__ == '__main__':
    main()
