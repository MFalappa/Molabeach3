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

# BUG1 settato con 1min di ritardo rispetto a quanto voluto
# BUG2 timer key error
from ui_setupLightCycle import Ui_Dialog
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import datetime
class setupLightCycle(QDialog,Ui_Dialog):
    applyTimerSchedule = pyqtSignal(dict, dict, dict, name='setupLightTimers')
    def __init__(self, boxid, list_box, parent=None):
        super(setupLightCycle, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonApply.setEnabled(False)
        self.checkDict = {}
        self.comboDict = {}
        self.idList = list_box
        for k in self.idList:
            self.checkDict[k] = QCheckBox('Box %d'%(k+1))
            self.comboDict[k] = QComboBox()
            self.comboDict[k].addItems(['On','Off'])
            hlayout = QHBoxLayout()
            hlayout.addWidget(self.checkDict[k])
            hlayout.addWidget(self.comboDict[k])
            self.verticalLayout_6.addLayout(hlayout)
            if k == boxid:
                self.checkDict[k].setChecked(True)
        spacerItem = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.verticalLayout_6.addSpacerItem(spacerItem)
        
        self.lightDurDict = {0:self.spinBoxL1,
                             1:self.spinBoxL2,
                             2:self.spinBoxL3,
                             3:self.spinBoxL4,
                             4:self.spinBoxL5,
                             5:self.spinBoxL6,
                             6:self.spinBoxL7,
                             7:self.spinBoxL8,
                             8:self.spinBoxL9,
                             9:self.spinBoxL10,
                             10:self.spinBoxL11,
                             11:self.spinBoxL12,
                             12:self.spinBoxL13,
                             13:self.spinBoxL14,
                             14:self.spinBoxL15
                             }
        self.darkDurDict =  {0:self.spinBoxD1,
                             1:self.spinBoxD2,
                             2:self.spinBoxD3,
                             3:self.spinBoxD4,
                             4:self.spinBoxD5,
                             5:self.spinBoxD6,
                             6:self.spinBoxD7,
                             7:self.spinBoxD8,
                             8:self.spinBoxD9,
                             9:self.spinBoxD10,
                             10:self.spinBoxD11,
                             11:self.spinBoxD12,
                             12:self.spinBoxD13,
                             13:self.spinBoxD14,
                             14:self.spinBoxD15
                             }
        self.timeEdit.setTime(QTime(20,0,0))
        self.connect(self.checkBoxSelectAll,SIGNAL('stateChanged(int)'),self.select_all_clicked)
        for k in self.checkDict.keys():
            self.connect(self.checkDict[k],SIGNAL('stateChanged(int)'),self.checkEnableApply)
        for k in self.darkDurDict.keys():
            self.darkDurDict[k].setRange(0,24*60*10)
            self.connect(self.darkDurDict[k],SIGNAL('valueChanged (int)'),self.checkEnableApply)
        for k in self.lightDurDict.keys():
            self.lightDurDict[k].setRange(0,24*60*10)
            self.connect(self.lightDurDict[k],SIGNAL('valueChanged (int)'),self.checkEnableApply)
        self.connect(self.spinBoxCL,SIGNAL('valueChanged (int)'),self.checkEnableApply)
        self.connect(self.calendarWidget,SIGNAL('selectionChanged ()'),self.checkEnableApply)
        self.connect(self.pushButtonApply,SIGNAL('clicked()'), self.applyCycle)
        self.connect(self.pushButton,SIGNAL('clicked()'),self.reject)
        self.spinBoxCL.setRange(1,15)
      
    def applyCycle(self):
#==============================================================================
#         FIX THIS
#==============================================================================
        loopMinutes = {}
        lightStatus = {}
        switchTime = {}
        selectedDate = self.calendarWidget.selectedDate()
        selectedTime = self.timeEdit.time()
        lswitch = QDateTime(selectedDate,selectedTime).toPyDateTime()
        for box in self.idList:
            list_light = []
            if self.checkDict[box].isChecked():
                boolean = self.comboDict[box].currentText() == 'Off'
                lightStatus[box] = boolean
                for k in range(self.spinBoxCL.value()):
                    dark_dur = self.darkDurDict[k].value()
                    light_dur = self.lightDurDict[k].value()
                    if boolean:
                        list_light += [light_dur,dark_dur]
                    else:
                        list_light += [dark_dur,light_dur]
                loopMinutes[box] = list_light
                switchTime[box] = lswitch
        self.applyTimerSchedule.emit(loopMinutes,lightStatus,switchTime)
        self.close()

    
    def select_all_clicked(self,tof):
        if tof:
            for Id in self.idList:
                self.checkDict[Id].setChecked(True)
        else:
            for Id in self.idList:
                self.checkDict[Id].setChecked(False)
        self.checkEnableApply()
    
    def checkEnableApply(self):
        selectedDate = self.calendarWidget.selectedDate()
        selectedTime = self.timeEdit.time()
        lswitch = QDateTime(selectedDate,selectedTime).toPyDateTime()
        now = QDateTime.currentDateTime().toPyDateTime()
        booleanStart = now < lswitch
        booleanSet = False
        for k in self.checkDict.keys():
            if self.checkDict[k].isChecked():
                booleanSet = True
                break
        booleanDuration = True
        for k in range(self.spinBoxCL.value()):
            if (not self.darkDurDict[k].value()) or (not self.darkDurDict[k].value()):
                booleanDuration = False
                break
        if booleanDuration * booleanSet * booleanStart:
            self.pushButtonApply.setEnabled(True)
        else:
            self.pushButtonApply.setEnabled(False)
            
def main():
    import sys
    app = QApplication(sys.argv)
    form = setupLightCycle(3,5)
    form.show()
    app.exec_()
if __name__=='__main__':
    main()