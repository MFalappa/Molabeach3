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
import os,sys 
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses')
sys.path.append(classes_dir)

from PyQt5.QtWidgets import (QDialog,QHeaderView,QTableWidgetItem,QApplication)
from PyQt5.QtCore import Qt,pyqtSignal
from ui_set_receiver import Ui_SetReceivers

from validate_email import validate_email

class set_receiver_dlg(QDialog,Ui_SetReceivers):
    cellChanged = pyqtSignal(int, int, name='cellChanged')
    def __init__(self,receivers, pdict,parent=None):
        super(set_receiver_dlg,self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['Receivers'])
        self.tableWidget.horizontalHeader()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.receivers = ['']*30
        self.receivers[:len(receivers)] = receivers
        self.true_receivers = receivers
        self.pdict = pdict
        self.buttonBox.button(self.buttonBox.Ok).setText('Apply')
        if len(receivers) == 0:
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
        else:
            for k in range(len(receivers)):
                item = QTableWidgetItem(receivers[k])
                self.tableWidget.setItem(k,0,item)
        
        
#        bisogna sistemare questa connection e quella dentro ui_set_receiver
#        self.trigger.connect(self.handle_trigger)
#        self.connect(self.tableWidget,SIGNAL('cellChanged(int,int)'),
#                     self.check_receivers)
        
        self.cellChanged.connect(self.tableWidget,self.check_receivers)
                
    def check_receivers(self):
        item = self.tableWidget.currentItem()
        row = self.tableWidget.currentRow()
        self.receivers[row] = item.text()
        for rec in self.receivers:
            if validate_email(rec):
                self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)
                continue
            else:
                if len(rec) == 0:
                    continue
                self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
                return
    def accept(self):
        self.true_receivers = []
        for rec in self.receivers:
            if len(rec)>0:
                self.true_receivers += [rec]
        self.pdict['receivers'] = self.receivers
        super(set_receiver_dlg,self).accept()
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    form = set_receiver_dlg(['ciccio@iit.it'],['matteo'])
    ans = form.exec_()
