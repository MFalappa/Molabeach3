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
import sys,os

file_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(file_dir,'libraries'))

from future_builtins import *
import urllib2
from PyQt4.QtCore import (Qt, SIGNAL, SLOT)
from PyQt4.QtGui import (QApplication, QComboBox, QDialog,
        QSpinBox, QLabel, QHBoxLayout,QGridLayout, QFont, QPushButton,
        QVBoxLayout, QSpacerItem, QSizePolicy,QListWidget, QDoubleSpinBox,QTimeEdit,
        QLineEdit)
from Modify_Dataset_GUI import OrderedDict
from MyDnDDialog import MyDnDListWidget

class inputDialog_Wizard(QDialog):
    """
    QDialog for obtaining the correct input dialog.
    
    Input:  -DataName=loaded dataset names list
            -combobox=list of 2-dim tuple. One with combobox label, the other with
                combobox values
            
    
    """
    def __init__(self, InputName, Number, ButtonText = 'Continue',parent=None):
        super(inputDialog_Wizard,self).__init__(parent)
        Vlayout = QVBoxLayout()
        self.input = None
        label_Input = QLabel(InputName+' %d'%Number)
        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        label_Input.setFont(font)
        Vlayout.addWidget(label_Input)
        self.InputName = InputName
        if InputName == 'Combo':
            Label_1               = QLabel('Combobox label: ')
            self.Label_LineEdit   = QLineEdit()
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_1)
            Hlayout.addWidget(self.Label_LineEdit)
            self.connect(self.Label_LineEdit, SIGNAL('textEdited (const QString&)'),self.checkCombo)
            Vlayout.addLayout(Hlayout)
            Label_2               = QLabel('Item list (separated by , and string between \" \")): ')
            self.Itemlist   = QLineEdit()
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_2)
            Hlayout.addWidget(self.Itemlist)
            self.connect(self.Itemlist, SIGNAL('textEdited (const QString&)'),self.checkCombo)
            Vlayout.addLayout(Hlayout)
            Label_3               = QLabel('Item values (separated by , and string between \" \"):')
            self.Itemvalues = QLineEdit()
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_3)
            Hlayout.addWidget(self.Itemvalues)
            Vlayout.addLayout(Hlayout)
            self.connect(self.Itemvalues, SIGNAL('textEdited (const QString&)'),self.checkCombo)
            self.spinboxItemInd = QSpinBox()
            self.spinboxItemInd.setRange(0,1000)
            labelSpin = QLabel('Default combo index: ')
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(labelSpin)
            Hlayout.addWidget(self.spinboxItemInd)
            self.connect(self.spinboxItemInd, SIGNAL('valueChanged (int)'),self.checkCombo)
            Vlayout.addLayout(Hlayout)
            
        elif InputName == 'SpinBox':
            Label_1 = QLabel('Spinbox label: ')
            Label_2 = QLabel('Default Value: ')
            Label_3 = QLabel('Set range (integer separated by ,): ')
            self.Label_LineEdit = QLineEdit()
            self.spinboxItemInd = QSpinBox()
            self.rangeLineEdit  = QLineEdit()
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_1)
            Hlayout.addWidget(self.Label_LineEdit)
            Vlayout.addLayout(Hlayout)
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_3)
            Hlayout.addWidget(self.rangeLineEdit)
            Vlayout.addLayout(Hlayout)            
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_2)
            Hlayout.addWidget(self.spinboxItemInd)
            Vlayout.addLayout(Hlayout)
            self.connect(self.spinboxItemInd, SIGNAL('valueChanged (int)'),self.checkSpinBox)
            self.connect(self.Label_LineEdit, SIGNAL('textEdited (const QString&)'),self.checkSpinBox)
            self.connect(self.rangeLineEdit, SIGNAL('textEdited (const QString&)'),self.checkSpinBox)            
        
        elif InputName == 'DoubleSpinBox':
            Label_1 = QLabel('Spinbox label: ')
            Label_2 = QLabel('Default Value: ')
            Label_3 = QLabel('Set range (float separated by ,): ')
            self.Label_LineEdit = QLineEdit()
            self.spinboxItemInd = QDoubleSpinBox()
            self.spinboxItemInd.setMaximum(10**6)
            self.rangeLineEdit  = QLineEdit()
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_1)
            Hlayout.addWidget(self.Label_LineEdit)
            Vlayout.addLayout(Hlayout)
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_3)
            Hlayout.addWidget(self.rangeLineEdit)
            Vlayout.addLayout(Hlayout)            
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_2)
            Hlayout.addWidget(self.spinboxItemInd)
            Vlayout.addLayout(Hlayout)
            self.connect(self.spinboxItemInd, SIGNAL('valueChanged (double)'),self.checkDoubleSpinBox)
            self.connect(self.Label_LineEdit, SIGNAL('textEdited (const QString&)'),self.checkDoubleSpinBox)
            self.connect(self.rangeLineEdit, SIGNAL('textEdited (const QString&)'),self.checkDoubleSpinBox)            
        
        elif InputName == 'Range':
            Label_1 = QLabel('Range label: ')
            Label_2 = QLabel('Set range (float separated by ,): ')
            Label_3 = QLabel('Default Values: ')
            
            self.Label_LineEdit = QLineEdit()
            self.spinboxMin = QDoubleSpinBox()
            self.spinboxMax = QDoubleSpinBox()
            self.rangeLineEdit  = QLineEdit()
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_1)
            Hlayout.addWidget(self.Label_LineEdit)
            Vlayout.addLayout(Hlayout)
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_2)
            Hlayout.addWidget(self.rangeLineEdit)
            Vlayout.addLayout(Hlayout)            
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_3)
            Hlayout.addWidget(self.spinboxMin)
            Hlayout.addWidget(QLabel('-'))
            Hlayout.addWidget(self.spinboxMax)
            Vlayout.addLayout(Hlayout)
            self.connect(self.spinboxMin, SIGNAL('valueChanged (double)'),self.checkRange)
            self.connect(self.spinboxMax, SIGNAL('valueChanged (double)'),self.checkRange)

            self.connect(self.Label_LineEdit, SIGNAL('textEdited (const QString&)'),self.checkRange)
            self.connect(self.rangeLineEdit, SIGNAL('textEdited (const QString&)'),self.checkRange)            
        
        
        elif InputName == 'TimeRange':
            Label_1 = QLabel('Time range label: ')
            Label_3 = QLabel('Default Values: ')
            
            self.Label_LineEdit = QLineEdit()
            self.default0 = QTimeEdit()
            self.default1 = QTimeEdit()
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_1)
            Hlayout.addWidget(self.Label_LineEdit)
            Vlayout.addLayout(Hlayout)

            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_3)
            Hlayout.addWidget(self.default0)
            Hlayout.addWidget(QLabel('-'))
            Hlayout.addWidget(self.default1)
            Vlayout.addLayout(Hlayout)
            
            self.default0.timeChanged.connect(self.checkTimeRange)
            self.default1.timeChanged.connect(self.checkTimeRange)
            self.connect(self.Label_LineEdit, SIGNAL('textEdited (const QString&)'),self.checkTimeRange)
            
        elif InputName == 'LineEdit':
            Label_1 = QLabel('LineEdit label: ')
            self.Label_LineEdit = QLineEdit()

            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_1)
            Hlayout.addWidget(self.Label_LineEdit)
            Vlayout.addLayout(Hlayout)          
            self.connect(self.Label_LineEdit, SIGNAL('textEdited (const QString&)'),self.checkLineEdit)
       
        elif InputName == 'TimeSpinBox':
            Label_1 = QLabel('TimeSpinbox label: ')
            Label_2 = QLabel('Default Value: ')
            Label_3 = QLabel(' : ')
            self.Label_LineEdit = QLineEdit()
            self.spinboxItemInd = QSpinBox()
            self.spinboxHour    = QSpinBox()
            self.spinboxMinute  = QSpinBox()
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_1)
            Hlayout.addWidget(self.Label_LineEdit)
            Vlayout.addLayout(Hlayout)
            
            Hlayout = QHBoxLayout()
            Hlayout.addWidget(Label_2)
            Hlayout.addWidget(self.spinboxHour)
            Hlayout.addWidget(Label_3)
            Hlayout.addWidget(self.spinboxMinute)
            Vlayout.addLayout(Hlayout)  
            self.spinboxMinute.setRange(0,59)
            self.spinboxHour.setRange(0,23)
            self.connect(self.Label_LineEdit, SIGNAL('textEdited (const QString&)'),self.checkTimeSpinBox)
            self.connect(self.spinboxMinute, SIGNAL('valueChanged (int)'),self.checkTimeSpinBox)
            self.connect(self.spinboxHour, SIGNAL('valueChanged (int)'),self.checkTimeSpinBox)

        self.ButtonContinue = QPushButton(ButtonText)
        ButtonCancel = QPushButton('Cancel')
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(ButtonCancel)
        Hlayout.addWidget(self.ButtonContinue)
        self.ButtonContinue.setEnabled(False)
        Vlayout.addLayout(Hlayout)
        self.setLayout(Vlayout)
        self.connect(self.ButtonContinue, SIGNAL('clicked()'), self.accept)
        self.connect(ButtonCancel, SIGNAL('clicked()'), self.reject)
        
    def checkCombo(self):
        
        Itemvalues   = unicode(self.Itemvalues.text())
        Itemlist     = unicode(self.Itemlist.text())
        Combolabel   = unicode(self.Label_LineEdit.text())
        DefaultIndex = self.spinboxItemInd.value()
        if Itemvalues != '' and Itemlist != '' and Combolabel != '':
            tmp1   = Itemvalues.split(',')
            tmp2   = Itemlist.split(',')
            boolean = True
            for k in tmp1:
                try:
                    int(k)
                except ValueError:
                    x = (k.endswith('\'') or k.endswith('"')) and len(k) != 1
                    y = (k.startswith('\'') or k.startswith('"')) and len(k) != 1
                    boolean *= y and x
                    break
                if len(k)==0:
                    boolean *= 0
                    break
            for k in tmp2:
                try:
                    int(k)
                except ValueError:
                    x = (k.endswith('\'') or k.endswith('"')) and len(k) != 1
                    y = (k.startswith('\'') or k.startswith('"')) and len(k) != 1
                    boolean *= y and x
                    print(boolean)
                    break
                if len(k)==0:
                    boolean *= 0
                    break
            if self.spinboxItemInd.value() > min(len(tmp1),len(tmp2)-1):
                boolean *= 0
                
            if len(tmp1) == len(tmp2) and boolean:
                
                self.input = '(\'%s\',[%s],[%s],%d)'%(Combolabel,Itemlist,
                                                      Itemvalues,DefaultIndex)
                print(self.input)
                if tmp2[0][0] != '\'' and tmp2[0][0] != '\"':
                    newList = u''
                    for word in tmp2:
                         newList =  newList + '\'' + word + '\'' + ','
                    newList = newList.rstrip(',')
                    self.Itemlist.setText(newList)

                self.ButtonContinue.setEnabled(True)
            else:
                self.ButtonContinue.setEnabled(False)
        else:
            self.ButtonContinue.setEnabled(False)
            
    def checkSpinBox(self):
        Combolabel = unicode(self.Label_LineEdit.text())
        strRange = unicode(self.rangeLineEdit.text())
        Range = strRange.split(',')
        val = self.spinboxItemInd.value()
        print( Range)
        try:
            boolean = len(Range) == 2 and len(Combolabel) > 0\
                  and val<=float(Range[1]) and val >= float(Range[0])
        except ValueError:
            boolean = False
        if boolean:
            self.input = '(\'%s\',(%s),%d)'%(Combolabel,strRange,val)
            self.ButtonContinue.setEnabled(True)
            print( self.input)
        else:
            self.ButtonContinue.setEnabled(False)
    
    def checkDoubleSpinBox(self):
        Combolabel = unicode(self.Label_LineEdit.text())
        strRange = unicode(self.rangeLineEdit.text())
        Range = strRange.split(',')
        val = self.spinboxItemInd.value()
        print( Range)
        try:
            boolean = len(Range) == 2 and len(Combolabel) > 0\
                  and val<=float(Range[1]) and val >= float(Range[0])
        except ValueError:
            boolean = False
        if boolean:
            self.input = '(\'%s\',(%s),%f)'%(Combolabel,strRange,val)
            self.ButtonContinue.setEnabled(True)
            print( self.input)
        else:
            self.ButtonContinue.setEnabled(False)
            
    def checkLineEdit(self):
        lineEdit = unicode(self.Label_LineEdit.text())
        try:
            boolean = len(lineEdit) > 0 and lineEdit.find('\'') == -1
        except ValueError:
            boolean = False
        if boolean:
            self.input = '\'%s\''%(lineEdit)
            self.ButtonContinue.setEnabled(True)
            print( self.input)
        else:
            self.ButtonContinue.setEnabled(False)
    
    def checkTimeSpinBox(self):
        lineEdit = unicode(self.Label_LineEdit.text())
        h = self.spinboxHour.value()
        m = self.spinboxMinute.value()
        try:
            boolean = len(lineEdit) > 0 and lineEdit.find('\'') == -1
        except ValueError:
            boolean = False
        if boolean:
            ('Starting Time:',0,0)
            self.input = '(\'%s\',%d,%d)'%(lineEdit,h,m)
            self.ButtonContinue.setEnabled(True)
            print( self.input)
        else:
            self.ButtonContinue.setEnabled(False)
            
    def checkTimeRange(self):
        rangeLabel = unicode(self.Label_LineEdit.text())
        boolean = len(rangeLabel) > 0
        if boolean:
            time0 = self.default0.time().toPyTime()
            time1 = self.default1.time().toPyTime()
            self.input = '(\'%s\',[%i,%i,%i],[%i,%i,%i])'%(rangeLabel,time0.hour,time0.minute,time0.second,time1.hour,time1.minute,time1.second)
            print( self.input)
        self.ButtonContinue.setEnabled(boolean)
        
    def checkRange(self):
        rangeLabel = unicode(self.Label_LineEdit.text())
        strRange = unicode(self.rangeLineEdit.text())
        Range = strRange.split(',')
        MIN = self.spinboxMin.value()
        MAX = self.spinboxMax.value()
        try:
            boolean = MIN < MAX
            boolean *= len(Range) == 2
            boolean *= len(rangeLabel) > 0
            boolean *= MIN < float(Range[1])  and MIN > float(Range[0])
            boolean *= MAX < float(Range[1])  and MAX > float(Range[0])
        except:
            boolean = False
        if boolean:
            self.input = '(\'%s\',(%s),%f,%f)'%(rangeLabel,strRange,MIN,MAX)
            #('Range0:',(0,10000),1.5,21.3)
            self.ButtonContinue.setEnabled(True)
            print( self.input)
        else:
            self.ButtonContinue.setEnabled(False)
        

def main():
    app = QApplication(sys.argv)

    form = inputDialog_Wizard('Range',4)
    
    form.show()
    
    #print(form.exec_())
    app.exec_()
    print(form.input,type(form.input))
    



                
if __name__ == "__main__":       
    main()

