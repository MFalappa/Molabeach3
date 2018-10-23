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


import sys

from PyQt4.QtCore import ( SIGNAL)
from PyQt4.QtGui import (QApplication,QComboBox, QDialog, QLabel, QHBoxLayout,QGridLayout,QLineEdit)

from MyDnDDialog import MyDnDListWidget
import ui_latencydlg
class latencydlg(QDialog,ui_latencydlg.Ui_ExtractLatency):
    """
    QDialog for obtaining the correct input dialog.
    
    Input:  -DataName=loaded dataset names list
            -combobox=list of 2-dim tuple. One with combobox label, the other with
                combobox values
            
    
    """
    def __init__(self,DataName,DatasetNum=1,
                ActivityList=[],parent=None):
        super(latencydlg,self).__init__(parent)
        self.setupUi(self)
        self.DatasetNum=DatasetNum
        LabelTimeInterval=QLabel('Time Interval:')
        self.timeIntervalComboBox=QComboBox()
        self.timeIntervalComboBox.addItems(['5 min','10 min','15 min','20 min',
                                            '30 min','60 min'])
        self.timeIntervalComboBox.setCurrentIndex(self.timeIntervalComboBox.count()-1)
        Hlayout=QHBoxLayout()
        Hlayout.addWidget(LabelTimeInterval)
        Hlayout.addWidget(self.timeIntervalComboBox)
        Hlayout.addStretch()
        self.verticalLayout.addLayout(Hlayout)
        ActionALabel=QLabel('<b>Timestamp A:</b>')
        ActionBLabel=QLabel('<b>Timestamp B:</b>')
        AllActionLabel=QLabel('<b>All timestamps</b>')
        self.label_2.setText(DataName)
        self.listActionA=MyDnDListWidget()
        self.listActionB=MyDnDListWidget()
        self.listAllAction=MyDnDListWidget()
        self.listAllAction.addItems(ActivityList)
        self.listAllAction.sortItems()
        TimeStampsList=[]
        for ind in range(self.listAllAction.count()):
            item=self.listAllAction.item(ind)
            TimeStampsList+=[unicode(item.text())]
        self.timeStampsComboBox0.addItems(TimeStampsList)
        self.timeStampsComboBox1.addItems(TimeStampsList)
        try:
            On=TimeStampsList.index('Center Light On')
            Off=TimeStampsList.index('Center Light Off')
            self.timeStampsComboBox0.setCurrentIndex(On)
            self.timeStampsComboBox1.setCurrentIndex(Off)
        except ValueError:
            pass
        grid  = QGridLayout()  
        grid.addWidget(ActionALabel,0,0)
        grid.addWidget(ActionBLabel,0,2)
        grid.addWidget(AllActionLabel,0,1)
        grid.addWidget(self.listActionA,1,0)
        grid.addWidget(self.listAllAction,1,1)
        grid.addWidget(self.listActionB,1,2)
        self.verticalLayout.addLayout(grid)
        
        LabelNewData = QLabel('<b>Dataset Names</b> (spearated by ;):')
        self.NewDataLineEdit=QLineEdit()
        HLayout6=QHBoxLayout()
        HLayout6.addStretch()
        HLayout6.addWidget(LabelNewData)
        
        HLayout6.addWidget(self.NewDataLineEdit)
        self.verticalLayout.addLayout(HLayout6)
        self.verticalLayout.addWidget(self.buttonBox)
        self.connect(self.NewDataLineEdit,SIGNAL('textEdited (const QString&)'),self.enableOk)
        self.connect(self.listActionA,SIGNAL('dragged()'),self.enableOk)
        self.connect(self.listActionA,SIGNAL('dropped()'),lambda key='A':self.refreshTable(key))
        self.connect(self.listActionB,SIGNAL('dragged()'),self.enableOk)
        self.connect(self.listActionB,SIGNAL('dropped()'),lambda key='B':self.refreshTable(key))
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
    
    def enableOk(self):
        if self.listActionA.count() and self.listActionB.count():
            print('Check Datanames')
            try:
                DataNames=unicode(self.NewDataLineEdit.text()).split(';')
                print(DataNames)
                try:
                    while True:
                        
                        DataNames.remove('')
                except ValueError:
                    pass
                
                if len(DataNames)==self.DatasetNum:
                    self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)
                else:
                    self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            except:
                self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
                    
        elif not (self.listActionA.count() or self.listActionB.count()):
            self.listActionA.setAcceptDrops(True)
            self.listActionB.setAcceptDrops(True)
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
        elif not self.listActionB.count():
            self.listActionB.setAcceptDrops(True)
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
        elif not self.listActionA.count():
            self.listActionA.setAcceptDrops(True)
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
        self.listAllAction.sortItems()
        
    def refreshTable(self,AorB=None):
        if AorB == 'A':
            self.listActionA.setAcceptDrops(False)
            print(self.listActionA.count())
            self.enableOk()
        else:
            self.listActionB.setAcceptDrops(False)
            self.enableOk()
        print('Refresh List '+AorB)
        pass
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = latencydlg('Kobe B.',ActivityList=['ciao','come','va?'])
    form.show()
    app.exec_()        
        
