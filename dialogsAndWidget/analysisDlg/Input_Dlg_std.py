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
#from __future__ import division
#from __future__ import print_function
#from __future__ import unicode_literals
#from future_builtins import *
import sys,sip,os
lib_dir = os.path.join(os.path.abspath(os.path.join(os.path.realpath(__file__),'../../..')),'libraries')
sys.path.append(lib_dir)
from Modify_Dataset_GUI import OrderedDict
import urllib2
from PyQt4.QtCore import (Qt, SIGNAL, SLOT,QTime)
from PyQt4.QtGui import (QApplication, QComboBox, QDialog,
        QSpinBox, QLabel, QHBoxLayout,QGridLayout, QFont, QDialogButtonBox,
        QVBoxLayout, QSpacerItem, QSizePolicy,QListWidget, QRadioButton,
        QCheckBox, QDoubleSpinBox,QLineEdit,QPushButton,QFileDialog,QTimeEdit)
from Modify_Dataset_GUI import OrderedDict,DatasetContainer_GUI
from MyDnDDialog import MyDnDListWidget
import numpy as np
from widgetSleepRecordingPhase import widgetSleepRecordingPhase
#sip.setapi('QString', 2)
#sip.setapi('QStringList', 2)
#sip.setapi('QVariant', 2)

class comboBoxAutonomice(object):
    def __init__(self, comboBox, valueList):
        if comboBox.count() != len(valueList):
            raise ValueError,'comboBox and valueList must have same number of \
                                items'
        self._comboBox = comboBox
        self._valueList = valueList
    def selectedValue(self):
        ind = self._comboBox.currentIndex()
        return self._valueList[ind]
    def currentIndex(self):
        return self._comboBox.currentIndex()
    def currentText(self):
        return self._comboBox.currentText()
    def setCurrentIndex(self, index):
        return self._comboBox.setCurrentIndex(index)
    def itemText(self, index):
        return self._comboBox.itemText(index)

class inputDialog(QDialog):
    """
    QDialog for obtaining the correct input dialog.
    
    Input:  -DataName=loaded dataset names list
            -combobox=list of 2-dim tuple. One with combobox label, the other with
                combobox values
            
    
    """
    def __init__(self,DataName, comboBox=None, TimeSpinBoxLabel=None,
                 DoubleSpinBox=None, LineEdit=None, SpinBox=None,
                 NewDataLineEdit=None,DatasetNum=1, ActivityList=None,
                 folderSave = False,RadioButton=None, Range=None,TimeRange=None, PhaseSel=None,parent=None):
        super(inputDialog,self).__init__(parent)
        print 'init started'
        self.ComboBox=OrderedDict()
        self.HourSpinBox=OrderedDict()
        self.MinuteSpinbox=OrderedDict()
        self.DoubleSpinBox=OrderedDict()
        self.LineEdit=OrderedDict()
        self.SpinBox=OrderedDict()
        self.Range_0 = OrderedDict()
        self.Range_1 = OrderedDict()
        self.TimeRange_0 = OrderedDict()
        self.TimeRange_1 = OrderedDict()
        self.PhaseSel = OrderedDict()
        self.DatasetNum = DatasetNum
        self.folderSave = folderSave
        self.RadioChoice = None
        if ActivityList:
            self.ActivityListBool = True
        else:
            self.ActivityListBool = False
        VLayout = QVBoxLayout() 
        indexCombo = 0
        indexSpacer = 0
        if DataName is not None:
            
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            DataLabel=QLabel(u'Selected Dataset: ')
            Data_Name=QLabel(u'%s'%DataName)
            Data_Name.setFont(font)
            HLayout = QHBoxLayout()
            HLayout.addWidget(DataLabel)
            HLayout.addWidget(Data_Name)
            VLayout.addLayout(HLayout)
            spacerItem = QSpacerItem(40,20, QSizePolicy.Expanding,\
                QSizePolicy.Minimum)
            VLayout.addSpacerItem(spacerItem)
            indexSpacer +=1
            
        if not PhaseSel is None:
            self.PhaseSel[0] = widgetSleepRecordingPhase(PhaseSel[0], PhaseSel[1])
            VLayout.addWidget(self.PhaseSel[0])
        
        if not TimeRange is None:
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            idx = 0
            for tr in TimeRange:
                label = QLabel(tr[0])
                label.setFont(font)
                self.TimeRange_0[idx] = QTimeEdit()
                self.TimeRange_1[idx] = QTimeEdit()
                
                self.TimeRange_0[idx].setTime(QTime(tr[1][0],tr[1][1],tr[1][2]))
                self.TimeRange_1[idx].setTime(QTime(tr[2][0],tr[2][1],tr[2][2]))
                label2 = QLabel('-')
                spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                hlayout = QHBoxLayout()
                hlayout.addWidget(label)
                hlayout.addWidget(self.TimeRange_0[idx])
                hlayout.addWidget(label2)
                hlayout.addWidget(self.TimeRange_1[idx])
                hlayout.addSpacerItem(spacerItem)
                VLayout.addLayout(hlayout)
                idx += 1
            
        if RadioButton is not None:
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            Label = QLabel(RadioButton[0])
            Label.setFont(font)
            indexRadio = 0
            RadioLayout = QVBoxLayout()
            HLayout = QHBoxLayout()
            spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            HLayout.addWidget(Label)
            HLayout.addSpacerItem(spacerItem)
            RadioLayout.addLayout(HLayout)
            self.RadioList = []
            for string in RadioButton[1:]:
                self.RadioList += [string]
                RadioButtons = QRadioButton()
                Label = QLabel(string)
                spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                HLayout = QHBoxLayout()
                HLayout.addSpacerItem(spacerItem)
                HLayout.addWidget(Label)
                HLayout.addWidget(RadioButtons)
                RadioLayout.addLayout(HLayout)
                self.connect(RadioButtons,SIGNAL('clicked()'),
                             lambda x=indexRadio : self.setRadioChoice(x))
                if indexRadio == 0:
                    RadioButtons.setChecked(True)
                    self.RadioChoice = string
                indexRadio += 1
            spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            RadioLayout.addSpacerItem(spacerItem)
            VLayout.addLayout(RadioLayout)
        if comboBox is not None:
            
            for indexCombo in range(len(comboBox)):
                ComboLabel = QLabel(unicode(comboBox[indexCombo][0]))
                print indexCombo ,comboBox[indexCombo]
                thisCombo = QComboBox()
                thisCombo.addItems(comboBox[indexCombo][1])
                thisCombo.setCurrentIndex(comboBox[indexCombo][3])
                self.ComboBox[indexCombo] = comboBoxAutonomice(\
                    thisCombo, comboBox[indexCombo][2])
                HLayout = QHBoxLayout()
                HLayout.addWidget(ComboLabel)
                HLayout.addWidget(thisCombo)
                VLayout.addLayout(HLayout)

        if TimeSpinBoxLabel is not None:
            
            for indexSpin in range(len(TimeSpinBoxLabel)):
                if TimeSpinBoxLabel[indexSpin] is not None:
                    self.HourSpinBox[indexSpin] = QSpinBox()
                    self.HourSpinBox[indexSpin].setRange(0,24)
                    self.HourSpinBox[indexSpin].setValue(TimeSpinBoxLabel[indexSpin][1])
                    self.MinuteSpinbox[indexSpin] = QSpinBox()
                    self.MinuteSpinbox[indexSpin].setRange(0,59)
                    self.MinuteSpinbox[indexSpin].setValue(TimeSpinBoxLabel[indexSpin][2])
                    SpinLabel = QLabel(unicode(TimeSpinBoxLabel[indexSpin][0]))
                    SeparatorLabel=QLabel(u':')
                    HLayout2 = QHBoxLayout()
                    HLayout2.addWidget(SpinLabel)
                    HLayout2.addWidget(self.HourSpinBox[indexSpin])
                    HLayout2.addWidget(SeparatorLabel)
                    HLayout2.addWidget(self.MinuteSpinbox[indexSpin])
                    HLayout2.addStretch()
                    VLayout.addLayout(HLayout2)
                    
                else:
                    
                    spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    VLayout.addItem(spacerItem)
                    indexSpacer+=1
        if Range is not None:
            indexRange = 0
            for RangeTuple in Range:
                self.Range_0[indexRange] = QDoubleSpinBox()
                self.Range_0[indexRange].setRange(RangeTuple[1][0],
                                                  RangeTuple[1][1])
                self.Range_0[indexRange].setValue(RangeTuple[2])
                self.Range_0[indexRange].setDecimals(4)
                self.Range_1[indexRange] = QDoubleSpinBox()
                self.Range_1[indexRange].setRange(RangeTuple[1][0],
                                                  RangeTuple[1][1])
                self.Range_1[indexRange].setValue(RangeTuple[3])
                self.Range_1[indexRange].setDecimals(4)
                
                Label_0 = QLabel(RangeTuple[0])
                Label_1 = QLabel(' , ')
                Label_2 = QLabel(') ')
                Label_3 = QLabel('(')
                spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding,
                                       QSizePolicy.Minimum)
                HLayout = QHBoxLayout()
                HLayout.addWidget(Label_0)
                HLayout.addSpacerItem(spacerItem)
                HLayout.addWidget(Label_3)
                HLayout.addWidget(self.Range_0[indexRange])
                HLayout.addWidget(Label_1)
                HLayout.addWidget(self.Range_1[indexRange])
                HLayout.addWidget(Label_2)
                indexRange += 1
                VLayout.addLayout(HLayout)
                
                
        if DoubleSpinBox is not None:
            try:        
                for indexDoubleSpin in range(len(DoubleSpinBox)):
                    self.DoubleSpinBox[indexDoubleSpin] = QDoubleSpinBox()
                    self.DoubleSpinBox[indexDoubleSpin].setRange(\
                        DoubleSpinBox[indexDoubleSpin][1][0],
                        DoubleSpinBox[indexDoubleSpin][1][1])
                    self.DoubleSpinBox[indexDoubleSpin].setDecimals(4)
                    DoubleSpinLabel = QLabel(DoubleSpinBox[indexDoubleSpin][0])
                    HLayout = QHBoxLayout()
                    HLayout.addWidget(DoubleSpinLabel)
                    HLayout.addStretch()
                    HLayout.addWidget(self.DoubleSpinBox[indexDoubleSpin])
                    VLayout.addLayout(HLayout)
                    try:
                        self.DoubleSpinBox[indexDoubleSpin].setValue(DoubleSpinBox[indexDoubleSpin][2])
                    except:
                        pass
            except IndexError:
                pass
        if not SpinBox is None:
            for indexSpinBox in range(len(SpinBox)):
                self.SpinBox[indexSpinBox] = QSpinBox()
                self.SpinBox[indexSpinBox].setRange(1,16)
                if len(SpinBox[indexSpinBox])==2 or len(SpinBox[indexSpinBox])==3:
                    if len(SpinBox[indexSpinBox])==3:
                        self.SpinBox[indexSpinBox].setRange(SpinBox[indexSpinBox][1][0],
                                                            SpinBox[indexSpinBox][1][1])
                    self.SpinBox[indexSpinBox].setValue(SpinBox[indexSpinBox][2])
                IntSpinLabel = QLabel(u'%s'%SpinBox[indexSpinBox][0])
                HLayout = QHBoxLayout()
                HLayout.addWidget(IntSpinLabel)
                HLayout.addWidget(self.SpinBox[indexSpinBox])
                HLayout.addStretch()
                VLayout.addLayout(HLayout)

        if not LineEdit is None:
            for indexLineEdit in range(len(LineEdit)):
                self.LineEdit[indexLineEdit] = QLineEdit()
                LineEditLabel = QLabel(u'%s'%LineEdit[indexLineEdit])
                HLayout = QHBoxLayout()
                HLayout.addWidget(LineEditLabel)
                HLayout.addWidget(self.LineEdit[indexLineEdit])
                HLayout.addStretch()
                VLayout.addLayout(HLayout)
          
        self.ButtonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        
        
        
        if not ActivityList is None:
            if len(ActivityList)>0:
                Grid=QGridLayout()
                LabelActivityList=QLabel('All Time Stamps:')
                LabelActivitySelected=QLabel('Time stamps to extract:')
                self.activityListWiget=MyDnDListWidget()
                self.activitySelectedWidget=MyDnDListWidget()
                self.activityListWiget.addItems(ActivityList)
                self.activityListWiget.sortItems()
                Grid.addWidget(LabelActivityList,0,0)
                Grid.addWidget(LabelActivitySelected,0,1)
                Grid.addWidget(self.activityListWiget,1,0)
                Grid.addWidget(self.activitySelectedWidget,1,1)
                VLayout.addLayout(Grid)
                self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)
        
        if folderSave:
            self.saveCheckBox = QCheckBox('Save the output?')
            VLayout.addWidget(self.saveCheckBox)
            LabelSave = QLabel('Choose save directory:')
            self.LineEditFileSaveDir = QLineEdit()
            browseButton = QPushButton('Browse...')
            HLayout = QHBoxLayout()
            HLayout.addWidget(LabelSave)
            HLayout.addWidget(self.LineEditFileSaveDir)
            HLayout.addWidget(browseButton)
            VLayout.addLayout(HLayout)
            self.extensionCombo = QComboBox()
            self.extensionCombo.addItems(['.jpg','.png','.eps','.pgf',\
                                     '.ps','.svg','.svgz','.tif',\
                                     '.tiff'])
            extensionLabel = QLabel('Choose image extension')
            HLayout = QHBoxLayout()
            HLayout.addWidget(extensionLabel)
            HLayout.addWidget(self.extensionCombo)
            VLayout.addLayout(HLayout)
            spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding,\
                                    QSizePolicy.Minimum)
            VLayout.addSpacerItem(spacerItem)
            self.connect(browseButton,SIGNAL('clicked()'),self.getDir)
        
        if NewDataLineEdit:
            LabelNewData = QLabel('<b>Dataset Names</b> (spearated by ;):')
            self.NewDataLineEdit=QLineEdit()
            HLayout=QHBoxLayout()
            HLayout.addWidget(LabelNewData)
            HLayout.addWidget(self.NewDataLineEdit)
            HLayout.addStretch()
            VLayout.addLayout(HLayout)
            
           
        if folderSave and NewDataLineEdit:
            self.connect(self.NewDataLineEdit,SIGNAL('textEdited (const QString&)'),
                         lambda par=None,ToF=False, ToF2 = True:\
                         self.enableOk(par,BoolData=ToF,BoolSave=ToF2))
            self.connect(self.LineEditFileSaveDir, SIGNAL('textChanged (const QString&)'),
                     lambda par=None,ToF=False, ToF2 = True:\
                     self.enableOk(par,BoolData=ToF,BoolSave=ToF2))
            self.connect(self.saveCheckBox,SIGNAL('stateChanged (int)'),
                         lambda ToF=False, ToF2 = True:\
                         self.enableOk(BoolData=ToF,BoolSave=ToF2))
            if self.ActivityListBool:
                self.connect(self.activitySelectedWidget,SIGNAL('dropped()'),
                             lambda ToF=True,ToF2 = True:\
                             self.enableOk(BoolData=ToF,BoolSave=ToF2))
                self.connect(self.activitySelectedWidget,SIGNAL('dragged()'),
                             lambda ToF=True,ToF2 = True:\
                             self.enableOk(BoolData=ToF,BoolSave=ToF2))
        elif folderSave:
            print 'folderSave Connect'
            self.connect(self.LineEditFileSaveDir, SIGNAL('textChanged (const QString&)'),
                     lambda par=None,ToF=True, ToF2 = True:\
                     self.enableOk(par,BoolData=ToF,BoolSave=ToF2))
            self.connect(self.saveCheckBox,SIGNAL('stateChanged (int)'),
                         lambda par=None,ToF=True, ToF2 = True:\
                         self.enableOk(par,BoolData=ToF,BoolSave=ToF2))
            if self.ActivityListBool:
                self.connect(self.activitySelectedWidget,SIGNAL('dropped()'),
                             lambda ToF=True,ToF2 = True:\
                             self.enableOk(BoolData=ToF,BoolSave=ToF2))
                self.connect(self.activitySelectedWidget,SIGNAL('dragged()'),
                             lambda ToF=True,ToF2 = True:\
                             self.enableOk(BoolData=ToF,BoolSave=ToF2))
                         
        elif NewDataLineEdit:
            self.connect(self.NewDataLineEdit,SIGNAL('textEdited (const QString&)'),
                         lambda par=None,ToF=False, ToF2 = False:\
                         self.enableOk(par,BoolData=ToF,BoolSave=ToF2))
            if self.ActivityListBool:
                self.connect(self.activitySelectedWidget,SIGNAL('dropped()'),
                             lambda ToF=True,ToF2 = False:\
                             self.enableOk(BoolData=ToF,BoolSave=ToF2))
                self.connect(self.activitySelectedWidget,SIGNAL('dragged()'),
                             lambda ToF=True,ToF2 = False:\
                             self.enableOk(BoolData=ToF,BoolSave=ToF2))
        elif self.ActivityListBool:
            self.connect(self.activitySelectedWidget,SIGNAL('dropped()'),
                         lambda ToF=True,ToF2 = False:\
                         self.enableOk(BoolData=ToF,BoolSave=ToF2))
            self.connect(self.activitySelectedWidget,SIGNAL('dragged()'),
                         lambda ToF=True,ToF2 = False:\
                         self.enableOk(BoolData=ToF,BoolSave=ToF2))
        
        spacerItem=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        VLayout.addSpacerItem(spacerItem)
        VLayout.addWidget(self.ButtonBox)      
        self.setLayout(VLayout)
        
        self.connect(self.ButtonBox,SIGNAL('rejected()'),self,SLOT('reject()'))
        self.connect(self.ButtonBox,SIGNAL('accepted()'),self,SLOT('accept()'))
        self.setWindowTitle('Input Dialog')
        
        


    def reject(self):
        QDialog.reject(self)
        
    def accept(self):
#        for indexCombo in range(len(self.comboValueLists)):
#            Ind = self.ComboBox[indexCombo].currentIndex()
#            self.comboValues += [self.comboValueLists[indexCombo][Ind]]
        QDialog.accept(self)
        
    def createStdOutput(self):
       stdOutPut = OrderedDict()
       stdOutPut['Combo'] = []
       for key in self.ComboBox.keys():
           stdOutPut['Combo'] += [self.ComboBox[key].selectedValue()]
       
       stdOutPut['DoubleSpinBox'] = []
       for key in self.DoubleSpinBox.keys():
           stdOutPut['DoubleSpinBox'] += [self.DoubleSpinBox[key].value()]
       
       stdOutPut['TimeSpinBox'] = []
       for key in self.HourSpinBox.keys():
           stdOutPut['TimeSpinBox'] += [(self.HourSpinBox[key].value(),\
                                self.MinuteSpinbox[key].value())]
       stdOutPut['SpinBox'] = []
       for key in self.SpinBox.keys():
           stdOutPut['SpinBox'] += [self.SpinBox[key].value()]
       
       stdOutPut['LineEdit'] = []
       for key in self.LineEdit.keys():
           stdOutPut['LineEdit'] += [unicode(self.LineEdit[key].text())]
           
       stdOutPut['RadioButton'] = []
       if self.RadioChoice:
           stdOutPut['RadioButton'] = [self.RadioChoice]

       stdOutPut['Range'] = []
       for  key in self.Range_0.keys():
           stdOutPut['Range'] += [(self.Range_0[key].value(),
                                         self.Range_1[key].value())]
       stdOutPut['PhaseSel'] = []
       for  key in self.PhaseSel.keys():
           stdOutPut['PhaseSel'] += [self.PhaseSel[key].phase_dict]
           
       stdOutPut['TimeRange'] = []
       for  key in self.TimeRange_0.keys():
           stdOutPut['TimeRange'] += [(self.TimeRange_0[key].time().toPyTime(),
                                       self.TimeRange_1[key].time().toPyTime())]
           
       if self.folderSave:
           print 'Adding SavingDetails to stdOutput'
           stdOutPut['SavingDetails'] = []
           if self.saveCheckBox.isChecked():
               Dir = unicode(self.LineEditFileSaveDir.text())
               row = self.extensionCombo.currentIndex()
               ext = unicode(self.extensionCombo.itemText(row))
               stdOutPut['SavingDetails'] += [Dir,ext]
               
       return stdOutPut
       
    def getDir(self):
       Dir = QFileDialog.getExistingDirectory(self,'Select a directory:','.')
       self.LineEditFileSaveDir.setText(Dir)
     
    def setRadioChoice(self, x):
        self.RadioChoice = self.RadioList[x]
       
    def enableOk(self, signalParam = None, BoolData = None,\
                 BoolSave = False):
        OkToContinue = True
        if BoolSave:
            dirString = unicode(self.LineEditFileSaveDir.text())
            OkToContinue =  (os.path.exists(dirString) and\
                            os.path.isdir(dirString)) or\
                            (not self.saveCheckBox.isChecked())
            if not OkToContinue:
                self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)
        if BoolData == True:
            try:
                if not self.activitySelectedWidget.count():
                    self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)
            
                else:
                    try:
                        DataNames=unicode(self.NewDataLineEdit.text()).split(';')
                        try:
                            while True:
                                DataNames.remove('')
                        except ValueError:
                            pass
                        if len(DataNames)==self.DatasetNum and OkToContinue:
                            self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)
                    except:
                        if OkToContinue:
                            self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)        
            except AttributeError:
                if OkToContinue:
                    self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)
        else:
        
            DataNames=unicode(self.NewDataLineEdit.text()).split(';')
            
            try:
                while True:
                    DataNames.remove('')
            except ValueError:
                pass
            
            if len(DataNames)==self.DatasetNum:
                try:
                    if self.activitySelectedWidget.count() and OkToContinue:  
                        self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)
                except:
                    if OkToContinue:
                        self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)                
            else:
                self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)
       
   
        
def main():
    app = QApplication(sys.argv)

    
    
    Hours=[]
    for h in range(24):
        Hours+=['%d h'%h]
    
    timeSpinBox = [None,('Ora1:',0,0),('Ora 2:',24,0),None,('Ora 3:',1,0)]
    
    Label = ['Max trial duration:']
    Range = [(0,10000)]
    doubleSpinBox = (Label,Range)
    
    
 
    Hours=[]
    Hours1=[]
    for h in range(24):
        Hours+=['%d:00'%h]
        Hours1+=['%d h'%h]
    doubleSpinBox=[(u'Short Signal:',(0,20),1),(u'Long Signal:',(5,30),11),(u'Trial Duration:',(15,10000),100)]
    comboBox=[('Epoch type:', ['Sleep', 'Rem', 'NRem', 'Wake'], [[2, 3], [2], [3], [1]], 0), 
              ('Statistical index:', ['Mean', 'Median'], ['Mean', 'Median'], 0), 
              ('Dark phase start:', ["0", "1", "2", "3", "4", "5","6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], 20)]
    timeSpinBox=[None,('Starting Time:',0,0),('Ending Time',24,0),None]
#    LineEdit=['Entrare il patronimico:']
    SpinBox=[('Hour binning:', (1, 24), 1), ('Epoch duration:', (1, 60), 4), ('Tick number:', (1, 100), 10)]
    RadioButton = ['Scgli quello che ti pare:','Attraversamento polli',
                   'Catch me if you can\'t','Zoolander']
    

    Range = None#[('Range:',(2,20),10.5,15)]#,('Range1:',(0,10000),11.5,100.3)]
    SAVE = True
    ##
    RadioButton =  None
    comboBox = None
    SpinBox = None#[(u'Insert an integer:',(0,10),9)]
    doubleSpinBox = [('Insert a float:',(0,10),5.5)]#None
    timeSpinBox = None
#    Range = None
    SAVE = False
    lineEdit = None#['Insert text:']
    
#==============================================================================
#     Phase Selection
#==============================================================================
    dc = DatasetContainer_GUI()
    dd = np.load('C:\Users\ebalzani\Desktop\Data\Sleep\\workspace_2017-5-15T14_16.phz')
    kl = []
    for key in dd.keys()[:3]:
        dc.add(dd[key].all())
        kl += [key]
    kl = np.sort(kl)
    PhaseSel = [dc, kl]
#==============================================================================
#    comboBox = [('Hour Bins:',["1 hour","2 hours","3 hours"],[3600,7200,10800],1)]
    ##
    form = inputDialog(None,comboBox,timeSpinBox,doubleSpinBox,lineEdit,SpinBox,False,3,
                       ActivityList=None,folderSave=SAVE,RadioButton=RadioButton,
                       Range = Range,PhaseSel=PhaseSel)
    

    form.show()
    
    app.exec_()
    
#    String = form.ComboBox[0]._comboBox.itemText(\
#        form.ComboBox[0]._comboBox.currentIndex())
#    if String == u'Left':
#          S='l'
#    else:
#        S='r'
#    t0,t1,tend=(form.DoubleSpinBox[0].value(),form.DoubleSpinBox[1].value(),
#                form.DoubleSpinBox[2].value())
#    t_first=form.HourSpinBox[1].value()*3600+form.MinuteSpinbox[1].value()*60
#    t_last=form.HourSpinBox[2].value()*3600+form.MinuteSpinbox[2].value()*60
#   
#    print(form.ComboBox[0].selectedValue(),form.ComboBox[1].selectedValue())
    stdOutPut = form.createStdOutput()
    print stdOutPut
if __name__ == '__main__':
    main()