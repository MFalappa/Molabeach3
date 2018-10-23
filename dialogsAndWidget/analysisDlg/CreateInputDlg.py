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
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *


import sys,os
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
sys.path.append(lib_dir)
from Modify_Dataset_GUI import OrderedDict
import urllib2
from PyQt4.QtCore import (Qt, SIGNAL, SLOT)
from PyQt4.QtGui import (QApplication, QComboBox, QDialog,
        QSpinBox, QLabel, QHBoxLayout,QGridLayout, QFont, QDialogButtonBox,
        QVBoxLayout, QSpacerItem, QSizePolicy,QListWidget, QDoubleSpinBox,QLineEdit)
from MyDnDDialog import MyDnDListWidget
class inputDialog(QDialog):
    """
    QDialog for obtaining the correct input dialog.
    
    Input:  -DataName=loaded dataset names list
            -combobox=list of 2-dim tuple. One with combobox label, the other with
                combobox values
            
    
    """
    def __init__(self,DataName,comboBox=[],TimeSpinBoxLabel=[],DoubleSpinBox=[],
                 LineEdit=[],SpinBox=[],NewDataLineEdit=None,DatasetNum=1,
                ActivityList=[],parent=None):
        super(inputDialog,self).__init__(parent)
        

        
        ComboLabel,self.ComboBox=OrderedDict(),OrderedDict()
        self.HourSpinBox=OrderedDict()
        self.MinuteSpinbox=OrderedDict()
        self.DoubleSpinBox=OrderedDict()
        self.LineEdit=OrderedDict()
        self.SpinBox=OrderedDict()
        self.DatasetNum = DatasetNum
        
        IntSpinLabel,SpinLabel,SeparatorLabel,DoubleSpinLabel,LineEditLabel,spacerItem={},{},{},{},{},{}
        HLayout1,HLayout2,HLayout3,HLayout4,HLayout5=OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()
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
        
               
        
            HLayout0 = QHBoxLayout()
            HLayout0.addWidget(DataLabel)
            HLayout0.addWidget(Data_Name)
        
            VLayout.addLayout(HLayout0)
        
        
            spacerItem[indexSpacer] = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
            VLayout.addSpacerItem(spacerItem[indexSpacer])
            indexSpacer +=1
        if comboBox is not None:
            
            for indexCombo in range(len(comboBox)):
                ComboLabel[indexCombo] = QLabel(unicode(comboBox[indexCombo][0]))
                self.ComboBox[indexCombo] = QComboBox()
                print(comboBox[indexCombo][1])
                self.ComboBox[indexCombo].addItems(comboBox[indexCombo][1])
                self.ComboBox[indexCombo].setCurrentIndex(comboBox[indexCombo][2])
                HLayout1[indexCombo] = QHBoxLayout()
                HLayout1[indexCombo].addWidget(ComboLabel[indexCombo])
                HLayout1[indexCombo].addWidget(self.ComboBox[indexCombo])
                
                VLayout.addLayout(HLayout1[indexCombo])
            
           
          
        if TimeSpinBoxLabel is not None:    
            for indexSpin in range(len(TimeSpinBoxLabel)):
                if TimeSpinBoxLabel[indexSpin] is not None:
                    self.HourSpinBox[indexSpin] = QSpinBox()
                    self.HourSpinBox[indexSpin].setRange(0,24)
                    self.HourSpinBox[indexSpin].setValue(TimeSpinBoxLabel[indexSpin][1])
                    self.MinuteSpinbox[indexSpin] = QSpinBox()
                    self.MinuteSpinbox[indexSpin].setRange(0,59)
                    self.MinuteSpinbox[indexSpin].setValue(TimeSpinBoxLabel[indexSpin][2])
                    SpinLabel[indexSpin] = QLabel(unicode(TimeSpinBoxLabel[indexSpin][0]))
                    SeparatorLabel[indexSpin]=QLabel(u':')
                    
                    HLayout2[indexSpin] = QHBoxLayout()
                    HLayout2[indexSpin].addWidget(SpinLabel[indexSpin])
                    HLayout2[indexSpin].addWidget(self.HourSpinBox[indexSpin])
                    HLayout2[indexSpin].addWidget(SeparatorLabel[indexSpin])
                    HLayout2[indexSpin].addWidget(self.MinuteSpinbox[indexSpin])
                    HLayout2[indexSpin].addStretch()
                    VLayout.addLayout(HLayout2[indexSpin])
                    
                else:
                    spacerItem[indexSpacer]=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    VLayout.addItem(spacerItem[indexSpacer])
                    indexSpacer+=1
        if DoubleSpinBox is not None:
            try:        
                for indexDoubleSpin in range(len(DoubleSpinBox[0])):
                    self.DoubleSpinBox[indexDoubleSpin] = QDoubleSpinBox()
                    self.DoubleSpinBox[indexDoubleSpin].setRange(DoubleSpinBox[1][indexDoubleSpin][0],
                                                                 DoubleSpinBox[1][indexDoubleSpin][1])
                    self.DoubleSpinBox[indexDoubleSpin].setDecimals(2)
                    DoubleSpinLabel[indexDoubleSpin] = QLabel(DoubleSpinBox[0][indexDoubleSpin])
                    
                    HLayout3[indexDoubleSpin] = QHBoxLayout()
                    HLayout3[indexDoubleSpin].addWidget(DoubleSpinLabel[indexDoubleSpin])
                    HLayout3[indexDoubleSpin].addStretch()
                    HLayout3[indexDoubleSpin].addWidget(self.DoubleSpinBox[indexDoubleSpin])
                    
                    VLayout.addLayout(HLayout3[indexDoubleSpin])
                    try:
                        self.DoubleSpinBox[indexDoubleSpin].setValue(DoubleSpinBox[2][indexDoubleSpin])
                    except:
                        pass
            except IndexError:
                pass

        for indexSpinBox in range(len(SpinBox)):
            self.SpinBox[indexSpinBox] = QSpinBox()
            self.SpinBox[indexSpinBox].setRange(1,16)
            if len(SpinBox[indexSpinBox])==2 or len(SpinBox[indexSpinBox])==3:
                if len(SpinBox[indexSpinBox])==3:
                    self.SpinBox[indexSpinBox].setRange(SpinBox[indexSpinBox][2][0],
                                                        SpinBox[indexSpinBox][2][1])
                self.SpinBox[indexSpinBox].setValue(SpinBox[indexSpinBox][1])
                
            IntSpinLabel[indexSpinBox] = QLabel(u'%s'%SpinBox[indexSpinBox][0])
            HLayout5[indexSpinBox] = QHBoxLayout()
            HLayout5[indexSpinBox].addWidget(IntSpinLabel[indexSpinBox])
            
            HLayout5[indexSpinBox].addWidget(self.SpinBox[indexSpinBox])
            HLayout5[indexSpinBox].addStretch()
            VLayout.addLayout(HLayout5[indexSpinBox])
            
        for indexLineEdit in range(len(LineEdit)):
            self.LineEdit[indexLineEdit] = QLineEdit()
            LineEditLabel[indexLineEdit] = QLabel(u'%s'%LineEdit[indexLineEdit])
            HLayout4[indexLineEdit] = QHBoxLayout()
            HLayout4[indexLineEdit].addWidget(LineEditLabel[indexLineEdit])
            
            HLayout4[indexLineEdit].addWidget(self.LineEdit[indexLineEdit])
            HLayout4[indexLineEdit].addStretch()
            VLayout.addLayout(HLayout4[indexLineEdit])
          
        self.ButtonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        
        
        
        
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
            self.connect(self.activitySelectedWidget,SIGNAL('dropped()'),lambda ToF=True:self.enableOk(ToF=ToF))
            self.connect(self.activitySelectedWidget,SIGNAL('dragged()'),lambda ToF=True:self.enableOk(ToF=ToF))
            self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)
            
        if NewDataLineEdit:
            LabelNewData = QLabel('<b>Dataset Names</b> (spearated by ;):')
            self.NewDataLineEdit=QLineEdit()
            HLayout6=QHBoxLayout()
            HLayout6.addWidget(LabelNewData)
            
            HLayout6.addWidget(self.NewDataLineEdit)
            
            HLayout6.addStretch()
            VLayout.addLayout(HLayout6)
            self.connect(self.NewDataLineEdit,SIGNAL('textEdited (const QString&)'),lambda ToF=False:self.enableOk(ToF=ToF))
           
        spacerItem[indexSpacer]=QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        VLayout.addSpacerItem(spacerItem[indexSpacer])
#        
#        
#        
        VLayout.addWidget(self.ButtonBox)
#        
#        
        self.setLayout(VLayout)
        

        
        self.connect(self.ButtonBox,SIGNAL('rejected()'),self,SLOT('reject()'))
        self.connect(self.ButtonBox,SIGNAL('accepted()'),self,SLOT('accept()'))
        self.setWindowTitle('Input Dialog')

    def reject(self):
        QDialog.reject(self)
        
    def enableOk(self,ToF=None):
        
        if ToF is True:
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
                    if len(DataNames)==self.DatasetNum:
                        self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)
                except:    
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
                    if self.activitySelectedWidget.count():  
                        self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)
                except:
                    self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)                
            else:
                self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)
            
        
if __name__ == "__main__":       
    app = QApplication(sys.argv)

    
    
    Hours=[]
    for h in range(24):
        Hours+=['%d h'%h]
    comboBox=[(u'Dark Phase Start:',Hours,20),(u'Dark Phase Duration:',Hours,12)]
    
    timeSpinBox = [None,('Ora1:',0,0),('Ora 2:',24,0),None,('Ora 3:',1,0)]
    
    Label = ['Max trial duration:']
    Range = [(0,10000)]
    doubleSpinBox = (Label,Range)
    
    
 
    Hours=[]
    Hours1=[]
    for h in range(24):
        Hours+=['%d:00'%h]
        Hours1+=['%d h'%h]
    Label = [u'Short Signal:',u'Long Signal:',u'Trial Duration:']
    Range=[(0,20),(5,30),(15,10000)]
    doubleSpinBox = (Label,Range,(1,111,100))
    comboBox=[(u'Hopper Side:',['Left','Right'],0)]
    timeSpinBox=[None,('Starting Time:',0,0),('Ending Time',24,0),None]
    LineEdit=['Entrare il patronimico:']
    SpinBox=[('SpinnoBoxo',30,(-1,1000)),('We Guagliao',1),('Cose a caso',)]
    form = inputDialog(None,comboBox,timeSpinBox,doubleSpinBox,LineEdit,SpinBox,True,3,
                       ActivityList=['Ciao','Gatto','Ciccio'])
    
    form.show()
    
    #print(form.exec_())
    app.exec_()
    
    String = form.ComboBox[0].itemText(form.ComboBox[0].currentIndex())
    if String == u'Left':
          S='l'
    else:
        S='r'
    t0,t1,tend=(form.DoubleSpinBox[0].value(),form.DoubleSpinBox[1].value(),
                form.DoubleSpinBox[2].value())
    t_first=form.HourSpinBox[1].value()*3600+form.MinuteSpinbox[1].value()*60
    t_last=form.HourSpinBox[2].value()*3600+form.MinuteSpinbox[2].value()*60
    


