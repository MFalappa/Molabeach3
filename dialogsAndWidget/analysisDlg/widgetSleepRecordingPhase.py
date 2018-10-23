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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
sys.path.append(lib_dir)
from Modify_Dataset_GUI import *
from ui_select_list_dlg import Ui_Dialog
from ui_widgetSleepRecordingPhase import Ui_Form
import numpy as np
import datetime as dt
from copy import copy

class widgetSleepRecordingPhase(QWidget,Ui_Form):
    enable_continue = pyqtSignal(bool,name='enableContinue')
    def __init__(self,Dataset,list_selected,parent=None):
        super(widgetSleepRecordingPhase,self).__init__(parent)
        
        self.tmp = 0
        self.setupUi(self)
        self.Dataset = Dataset
        self.list_selected = list_selected
        self.comboBox.addItems(self.list_selected)
                
        self.label_warning.setText('')
        
        self.setInitialPhase()
        self.setDateInitialTimes(self.list_selected[0],phase='bs')
        self.setDateInitialTimes(self.list_selected[0],phase='sd')
        self.setDateInitialTimes(self.list_selected[0],phase='rc')
        self.setDateInitialTimes(self.list_selected[0],phase='nm')
        self.setTimeLims(self.list_selected[0])
        
        
        self.checkBox_bs.setChecked(1)
        
        bs_func = lambda : self.checkerBoxChanged('BS')
        sd_func = lambda : self.checkerBoxChanged('SD')
        rc_func = lambda : self.checkerBoxChanged('RC')
        self.connect(self.checkBox_bs, SIGNAL('stateChanged (int)'), bs_func)
        self.connect(self.checkBox_sd, SIGNAL('stateChanged (int)'), sd_func)
        self.connect(self.checkBox_rc, SIGNAL('stateChanged (int)'), rc_func)
        
        bs0 = lambda dd:self.changeDate(dd,'bs0')
        bs1 = lambda dd:self.changeDate(dd,'bs1')
        self.dateTimeEdit_bs_0.dateTimeChanged.connect(bs0)
        self.dateTimeEdit_bs_1.dateTimeChanged.connect(bs1)
        
        sd0 = lambda dd:self.changeDate(dd,'sd0')
        sd1 = lambda dd:self.changeDate(dd,'sd1')
        self.dateTimeEdit_sd_0.dateTimeChanged.connect(sd0)
        self.dateTimeEdit_sd_1.dateTimeChanged.connect(sd1)
        
        rc0 = lambda dd:self.changeDate(dd,'rc0')
        rc1 = lambda dd:self.changeDate(dd,'rc1')
        self.dateTimeEdit_rc_0.dateTimeChanged.connect(rc0)
        self.dateTimeEdit_rc_1.dateTimeChanged.connect(rc1)
        
        nm0 = lambda dd:self.changeDate(dd,'nm0')
        nm1 = lambda dd:self.changeDate(dd,'nm1')
        self.dateTimeEdit_norm0.dateTimeChanged.connect(nm0)
        self.dateTimeEdit_norm1.dateTimeChanged.connect(nm1)
        
        self.connect(self.comboBox,SIGNAL("currentIndexChanged (const QString&)"),self.refreshDate)
        
        self.pushButton.clicked.connect(self.applyTo)
    
    
    def checkerBoxChanged(self,phase):
        """
            set new checkable state in the phase_dict for all subject
        """
        if phase == 'BS':
            isChecked = self.checkBox_bs.isChecked()
            idx = 0
        elif phase == 'SD':
            isChecked = self.checkBox_sd.isChecked()
            idx = 1
        else:
            isChecked = self.checkBox_rc.isChecked()
            idx = 2
        for label in self.list_selected:
            self.phase_dict[label]['isChecked'][idx] = isChecked
        self.checkPhases()
        
    def refreshDate(self,label):
        """
            Refresh with the info regarding the new subject
        """

        print self.phase_dict[label]
        self.setTimeLims(label)
        print self.phase_dict[label]
        isChecked = self.phase_dict[label][0]['isChecked']
        date0 = self.phase_dict[label][0]['dayStart']
        date1 = self.phase_dict[label][0]['dayEnd']
        qDate0 = QDateTime(date0.year,date0.month,date0.day,date0.hour,date0.minute,date0.second)
        qDate1 = QDateTime(date1.year,date1.month,date1.day,date1.hour,date1.minute,date1.second)
        self.dateTimeEdit_bs_0.setDateTime(qDate0)
        self.dateTimeEdit_bs_1.setDateTime(qDate1)
        self.checkBox_bs.setChecked(isChecked)
        
        isChecked = self.phase_dict[label][1]['isChecked']
        date0 = self.phase_dict[label][1]['dayStart']
        date1 = self.phase_dict[label][1]['dayEnd']
        qDate0 = QDateTime(date0.year,date0.month,date0.day,date0.hour,date0.minute,date0.second)
        qDate1 = QDateTime(date1.year,date1.month,date1.day,date1.hour,date1.minute,date1.second)
        self.dateTimeEdit_sd_0.setDateTime(qDate0)
        self.dateTimeEdit_sd_1.setDateTime(qDate1)
        self.checkBox_sd.setChecked(isChecked)
        
        isChecked = self.phase_dict[label][2]['isChecked']
        date0 = self.phase_dict[label][2]['dayStart']
        date1 = self.phase_dict[label][2]['dayEnd']
        qDate0 = QDateTime(date0.year,date0.month,date0.day,date0.hour,date0.minute,date0.second)
        qDate1 = QDateTime(date1.year,date1.month,date1.day,date1.hour,date1.minute,date1.second)
        self.dateTimeEdit_rc_0.setDateTime(qDate0)
        self.dateTimeEdit_rc_1.setDateTime(qDate1)
        self.checkBox_rc.setChecked(isChecked)
        
        date0 = self.phase_dict[label][0]['normStart']
        date1 = self.phase_dict[label][0]['normEnd']
        qDate0 = QDateTime(date0.year,date0.month,date0.day,date0.hour,date0.minute,date0.second)
        qDate1 = QDateTime(date1.year,date1.month,date1.day,date1.hour,date1.minute,date1.second)
        self.dateTimeEdit_norm0.setDateTime(qDate0)
        self.dateTimeEdit_norm1.setDateTime(qDate1)
       
    def setTimeLims(self,label):
        print self.tmp,'SETLIM'
        self.tmp+=1
        minDT = self.Dataset.takeDataset(label).Timestamp[0]
        maxDT = self.Dataset.takeDataset(label).Timestamp[-1]
        
        minDT = QDateTime(minDT)
        maxDT = QDateTime(maxDT)
                
        ph_dict = copy(self.phase_dict[label])
        
        self.dateTimeEdit_bs_0.setMinimumDateTime(minDT)
        self.dateTimeEdit_bs_1.setMinimumDateTime(minDT)
        self.dateTimeEdit_sd_0.setMinimumDateTime(minDT)
        self.dateTimeEdit_sd_1.setMinimumDateTime(minDT)
        self.dateTimeEdit_rc_0.setMinimumDateTime(minDT)
        self.dateTimeEdit_rc_1.setMinimumDateTime(minDT)
        self.dateTimeEdit_norm0.setMinimumDateTime(minDT)
        self.dateTimeEdit_norm1.setMinimumDateTime(minDT)
        
        self.dateTimeEdit_bs_0.setMaximumDateTime(maxDT)
        self.dateTimeEdit_bs_1.setMaximumDateTime(maxDT)
        self.dateTimeEdit_sd_0.setMaximumDateTime(maxDT)
        self.dateTimeEdit_sd_1.setMaximumDateTime(maxDT)
        self.dateTimeEdit_rc_0.setMaximumDateTime(maxDT)
        self.dateTimeEdit_rc_1.setMaximumDateTime(maxDT)
        self.dateTimeEdit_norm0.setMaximumDateTime(maxDT)
        self.dateTimeEdit_norm1.setMaximumDateTime(maxDT)
        
        self.phase_dict[label] = ph_dict
        
    def setInitialPhase(self):
        """
            Initial info values in phase_dict
        """
        self.phase_dict = {}
        for label in self.list_selected:
            self.phase_dict[label] = np.zeros(3,dtype={'names':('phase','dayStart','dayEnd','normStart','normEnd','isChecked'),
                                                        'formats':('S2',datetime.datetime,datetime.datetime,datetime.datetime,datetime.datetime,bool)})
            self.phase_dict[label]['phase'][0] = 'BS'
            self.phase_dict[label]['dayStart'][0] = self.Dataset.takeDataset(label).Timestamp[0]
            self.phase_dict[label]['dayEnd'][0] = self.Dataset.takeDataset(label).Timestamp[-1]
            self.phase_dict[label]['isChecked'][0] = True
            
            self.phase_dict[label]['phase'][1] = 'SD'
            self.phase_dict[label]['dayStart'][1] = self.Dataset.takeDataset(label).Timestamp[0]
            self.phase_dict[label]['dayEnd'][1] = self.Dataset.takeDataset(label).Timestamp[-1]
            self.phase_dict[label]['isChecked'][1] = False
            
            self.phase_dict[label]['phase'][2] = 'RC'
            self.phase_dict[label]['dayStart'][2] = self.Dataset.takeDataset(label).Timestamp[0]
            self.phase_dict[label]['dayEnd'][2] = self.Dataset.takeDataset(label).Timestamp[-1]
            self.phase_dict[label]['isChecked'][2] = False
            
            self.phase_dict[label]['normStart'][:] = self.Dataset.takeDataset(label).Timestamp[0]
            self.phase_dict[label]['normEnd'][:] = self.Dataset.takeDataset(label).Timestamp[-1]
            
    def setDateInitialTimes(self,label,phase):
        if phase == 'bs':
            dateTimeEdt_0 = self.dateTimeEdit_bs_0
            dateTimeEdt_1 = self.dateTimeEdit_bs_1
        elif phase == 'sd':
            dateTimeEdt_0 = self.dateTimeEdit_sd_0
            dateTimeEdt_1 = self.dateTimeEdit_sd_1
        elif phase == 'rc':
            dateTimeEdt_0 = self.dateTimeEdit_rc_0
            dateTimeEdt_1 = self.dateTimeEdit_rc_1
        elif phase == 'nm':
            dateTimeEdt_0 = self.dateTimeEdit_norm0
            dateTimeEdt_1 = self.dateTimeEdit_norm1
        date0 = self.Dataset.takeDataset(label).Timestamp[0]
        date1 = self.Dataset.takeDataset(label).Timestamp[-1]
        qDate0 = QDateTime(date0.year,date0.month,date0.day,date0.hour,date0.minute,date0.second)
        qDate1 = QDateTime(date1.year,date1.month,date1.day,date1.hour,date1.minute,date1.second)
        dateTimeEdt_0.setDateTime(qDate0)
        dateTimeEdt_1.setDateTime(qDate1)
        
    def changeDate(self,date,string=''):
        """
            Changes all the dates to the current available
        """
        if string == 'bs0':
            row = 0
            key = 'dayStart'
            dateTimeEdt = self.dateTimeEdit_bs_0
        elif string == 'bs1':
            row = 0
            key = 'dayEnd'
            dateTimeEdt = self.dateTimeEdit_bs_1
        elif string == 'sd0':
            row = 1
            key = 'dayStart'
            dateTimeEdt = self.dateTimeEdit_sd_0
        elif string == 'sd1':
            row = 1
            key = 'dayEnd'
            dateTimeEdt = self.dateTimeEdit_sd_1
        elif string == 'rc0':
            row = 2
            key = 'dayStart'
            dateTimeEdt = self.dateTimeEdit_rc_0
        elif string == 'rc1':
            row = 2
            key = 'dayEnd'
            dateTimeEdt = self.dateTimeEdit_rc_1
        elif string == 'nm0':
            row = range(3)
            key = 'normStart'
            dateTimeEdt = self.dateTimeEdit_norm0
        elif string == 'nm1':
            row = range(3)
            key = 'normEnd'
            dateTimeEdt = self.dateTimeEdit_norm1
        label = self.comboBox.currentText()
#        print label,row,key,string,dateTimeEdt.dateTime().toPyDateTime().isoformat()
#        print self.phase_dict[label][row][key],'\n'
        
        if type(row) == list:
            for k in row:
                self.phase_dict[label][row[k]][key] = dateTimeEdt.dateTime().toPyDateTime()
        else:
            self.phase_dict[label][row][key] = dateTimeEdt.dateTime().toPyDateTime()
        self.checkPhases()
        
    def checkPhases(self):
        """
            Check the following condition: 
                i. Date for each checked phase are temporally ordered and are in
                the limit of each dataset
        """
        checkFlag = True
        for label in self.list_selected:
#            st = self.Dataset.takeDataset(label).Timestamp[0]
#            en = self.Dataset.takeDataset(label).Timestamp[-1]
            
            bs_s = self.phase_dict[label][0]['dayStart']
            bs_e = self.phase_dict[label][0]['dayEnd']
            
            sd_s = self.phase_dict[label][1]['dayStart']
            sd_e = self.phase_dict[label][1]['dayEnd']
            
            rc_s = self.phase_dict[label][2]['dayStart']
            rc_e = self.phase_dict[label][2]['dayEnd']
            
            nm_s = self.phase_dict[label][2]['normStart']
            nm_e = self.phase_dict[label][2]['normEnd']
            
            if bs_e <= bs_s and self.checkBox_bs.isChecked():
                checkFlag = False
                warning = '%s: BS end date is set before BS start'%label
                break
            
            elif sd_s < bs_e and self.checkBox_sd.isChecked() and self.checkBox_bs.isChecked():
                checkFlag = False
                warning = '%s: SD start date is set before BS end'%label
                break
            
            elif sd_e <= sd_s and self.checkBox_sd.isChecked():
                checkFlag = False
                warning = '%s: SD end date is set before SD start'%label
                break
        
            elif rc_s < sd_e and self.checkBox_rc.isChecked() and self.checkBox_sd.isChecked():
                checkFlag = False
                warning = '%s: RC start date is set before SD end'%label
                break
            
            elif rc_e <= rc_s and self.checkBox_rc.isChecked():
                checkFlag = False
                warning = '%s: RC end date is set before RC start'%label
                break
            
            elif nm_e <= nm_s:
                checkFlag = False
                warning = '%s: Normalization end date is set before normalization start'%label
                break
            
            else:
                warning = ''
        self.label_warning.setText(warning)
        self.enable_continue.emit(checkFlag)
    
    def changeDates(self,name_list):
        print 'called change dates'
        for label in name_list:
            d0 = self.dateTimeEdit_bs_0.dateTime().toPyDateTime()
            d1 = self.dateTimeEdit_bs_1.dateTime().toPyDateTime()
            
            self.phase_dict[label]['phase'][0] = 'BS'
            self.phase_dict[label]['dayStart'][0] = d0
            self.phase_dict[label]['dayEnd'][0] = d1
            self.phase_dict[label]['isChecked'][0] = self.checkBox_bs.isChecked()
            
            d0 = self.dateTimeEdit_sd_0.dateTime().toPyDateTime()
            d1 = self.dateTimeEdit_sd_1.dateTime().toPyDateTime()
            
            self.phase_dict[label]['phase'][1] = 'SD'
            self.phase_dict[label]['dayStart'][1] = d0
            self.phase_dict[label]['dayEnd'][1] = d1
            self.phase_dict[label]['isChecked'][1] = self.checkBox_sd.isChecked()
            
            d0 = self.dateTimeEdit_rc_0.dateTime().toPyDateTime()
            d1 = self.dateTimeEdit_rc_1.dateTime().toPyDateTime()
            
            self.phase_dict[label]['phase'][2] = 'RC'
            self.phase_dict[label]['dayStart'][2] = d0
            self.phase_dict[label]['dayEnd'][2] = d1
            self.phase_dict[label]['isChecked'][2] = self.checkBox_rc.isChecked()
            
            d0 = self.dateTimeEdit_norm0.dateTime().toPyDateTime()
            d1 = self.dateTimeEdit_norm1.dateTime().toPyDateTime()
            
            self.phase_dict[label]['normStart'][:] = d0
            self.phase_dict[label]['normEnd'][:] = d1
            
            print label
    
    def applyTo(self):
        dlg = select_names_dlg(self.list_selected,parent=self)
        dlg.apply_signal.connect(self.changeDates)
        dlg.show()

class select_names_dlg(Ui_Dialog,QDialog):
    apply_signal = pyqtSignal(list, name='apply_signal')
    def __init__(self, IDList, parent=None, MODE=0 ):
        super(select_names_dlg, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.IDList = IDList
        self.mode = MODE
        self.apply_signal.connect(self.test)
        
        # CREATE A CHECKER BOX LIST
        self.dictChecker = {}
        self.box_group = QButtonGroup(parent=self)
        self.box_group.setExclusive(False)
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        for Id in self.IDList:
            self.dictChecker[Id] = QCheckBox("%s"%Id,parent=self.scrollAreaWidgetContents)
            self.box_group.addButton(self.dictChecker[Id])
            self.dictChecker[Id].setFont(font)
            self.verticalLayout_4.addWidget(self.dictChecker[Id])
            self.dictChecker[Id].setChecked(True)
        
        spaceritem = QSpacerItem(0,0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addSpacerItem(spaceritem)
        
        self.connect(self.pushButton_apply,SIGNAL('clicked()'),self.emit_signal_apply)
        self.connect(self.pushButton_close,SIGNAL('clicked()'),self.close)
        self.connect(self.checkBox_select_all,SIGNAL('clicked(bool)'),self.select_all_clicked)

    def select_all_clicked(self,tof):
        if tof:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(True)
        else:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(False)
                
    def box_checked(self,button):
        self.checkBox_select_all.setChecked(False)
    
    def emit_signal_apply(self):
        apply_list = []
        for name in self.IDList:
            if self.dictChecker[name].isChecked():
                apply_list += [name]
        self.apply_signal.emit(apply_list)
        
 
    
    def test(self,l):
        pass
#        print l

def main():

    dc = DatasetContainer_GUI()
    dd = np.load('C:\Users\ebalzani\Desktop\Data\Sleep\\workspace_2017-5-15T14_16.phz')
    kl = []
    for key in dd.keys()[:3]:
        dc.add(dd[key].all())
        kl += [key]
    kl = np.sort(kl)
    app = QApplication(sys.argv)
    dialog = widgetSleepRecordingPhase(dc,kl)
    dialog.show()
    app.exec_()

if __name__ == '__main__':
    main()