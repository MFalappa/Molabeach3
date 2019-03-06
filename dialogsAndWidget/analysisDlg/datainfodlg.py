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
import sys,os
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','analysisClasses')
sys.path.append(classes_dir)
sys.path.append(lib_dir)

from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QPushButton,QVBoxLayout,
                             QTextBrowser,QTextEdit,QListWidget,QSpacerItem,QSizePolicy,
                             QApplication)
from PyQt5.QtCore import Qt,QReadWriteLock
from PyQt5.QtGui import QFont

from MyDnDDialog import MyDnDListWidget
from copy import copy
from abstractmodel_for_table_repr import table_view_setter
from Modify_Dataset_GUI import *
from Analyzing_GUI import *
import ui_datainfodlg

MAC = 'qt_mac_set_native_menubar' in dir()


class EditTypesDlg(QDialog):
    def __init__(self,Dataset,AllTypes=[],lock=None,parent=None):
        super(EditTypesDlg,self).__init__(parent)
        self.__Dataset=Dataset
        self.lock = lock
        self.__TypeList = self.__Dataset.Types
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        LabelDataType = QLabel('Dataset Type',parent=self)
        LabelDataType.setFont(font)
        LabelRestOfTypes = QLabel('Other Types',parent=self)
        LabelRestOfTypes.setFont(font)
        self.listDataType = MyDnDListWidget(parent=self)
        self.listRestOfTypes = MyDnDListWidget(parent=self)
        self.applyButton = QPushButton('Apply',parent=self)
        closeButton = QPushButton('Close',parent=self)
        Hlayout1 = QHBoxLayout()
        Vlayout1 = QVBoxLayout()
        Vlayout2 = QVBoxLayout()
        Vlayout1.addWidget(LabelDataType)
        Vlayout1.addWidget(self.listDataType)
        Vlayout2.addWidget(LabelRestOfTypes)
        Vlayout2.addWidget(self.listRestOfTypes)
        Hlayout1.addLayout(Vlayout1)
        Hlayout1.addLayout(Vlayout2)
        Hlayout2=QHBoxLayout()
        Hlayout2.addStretch()
        Hlayout2.addWidget(self.applyButton)
        Hlayout2.addWidget(closeButton)
        layout = QVBoxLayout()
        layout.addLayout(Hlayout1)
        layout.addLayout(Hlayout2)
        for Type in Dataset.Types:
            try:
                while True:
                    AllTypes.remove(Type)
            except ValueError:
                pass              
        self.__RestOfType = AllTypes
        self.listDataType.addItems(Dataset.Types)
        self.listRestOfTypes.addItems(AllTypes)
        self.setLayout(layout)
        closeButton.clicked.connect(self.close)
        self.applyButton.clicked.connect(self.Apply)

        self.connect(self.listRestOfTypes,SIGNAL('dropped()'),lambda TorF=False: self.enableApply(TorF))
        self.connect(self.listDataType,SIGNAL('dropped()'),lambda TorF=True: self.enableApply(TorF))
       
        
    def Apply(self):
        ItemList=[]
        
        MaxInd=self.listDataType.count()
        for ind in range(MaxInd):
            Item = self.listDataType.item(ind)
            ItemList+=[str(Item.text())]
        RestList=[]
        MaxInd=self.listRestOfTypes.count()
        for ind in range(MaxInd):
            Item = self.listRestOfTypes.item(ind)
            RestList+=[str(Item.text())]
        
        self.__RestOfType = RestList
        self.__TypeList = ItemList
        try:
            self.lock.lockForWrite()
            self.__Dataset.Types = ItemList
        finally:
            self.lock.unlock()
        self.emit(SIGNAL('updateTypes()'))
    
    def close(self):
        self.listDataType.clear()
        self.listRestOfTypes.clear()
        self.listDataType.addItems(self.__TypeList)
        self.listRestOfTypes.addItems(self.__RestOfType)
        super(EditTypesDlg,self).close()
        
    
        
    def enableApply(self,TorF):
        if TorF:
            self.applyButton.setEnabled(True)
            #print('Metto un Tipo')
        else:
            #print('Tolgo Un Tipo')
            if not self.listDataType.count()-1:
                self.applyButton.setEnabled(False)
            
class datainfodlg(QDialog):
    def __init__(self,Dataset,TimeStamps=None,Path=None,TypeList=[],lock=None,parent=None):
        super(datainfodlg,self).__init__(parent)
        self.textBrowser = QTextBrowser()
        self.textBrowser.setLineWrapMode(QTextEdit.NoWrap)
        self.labelName = QLabel()
        self.labelName.setText(Dataset.Label)
        labelTypes = QLabel('Data Types:')
        self.listWidgetTypes = QListWidget()
        for TYPE in Dataset.Types:
            self.listWidgetTypes.addItem(TYPE)
        pushButtonEdit = QPushButton('Edit Types')
        pushButtonRestore = QPushButton('Restore Types')
        pushButtonClose = QPushButton('Close')
        self.__Dataset = Dataset.Dataset
        self.__CompleteData = Dataset
        self.__TypeList = copy(TypeList)
        self.__OriginalTypes = copy(Dataset.Types)
        self.lock = lock
        try:
            lock.lockForRead()
            Path = self.__CompleteData.Path
            self.tableView, string = table_view_setter(Dataset.Dataset)
        finally:
            lock.unlock()
        if not self.tableView:
            self.tableView = QTextBrowser()
            self.tableView.setText(string)
        

        self.dialog = EditTypesDlg(Dataset=Dataset,AllTypes=self.__TypeList,lock=lock,parent=self)
        if not MAC:
            pushButtonClose.setFocusPolicy(Qt.NoFocus)
            pushButtonEdit.setFocusPolicy(Qt.NoFocus)
            pushButtonRestore.setFocusPolicy(Qt.NoFocus)
            
        try:
            self.updateTypes()
            self.information(Path)
        except Exception as e:
            print(('Unable to collect dataset info. %s'%e))
            self.reject()
            
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        spaceritem = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        hlayout.addWidget(self.labelName)
        
        hlayout.addSpacerItem(spaceritem)
        vlayout.addLayout(hlayout)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.tableView)
        hlayout.addWidget(self.textBrowser)
        vlayout.addLayout(hlayout)
        
        hlayout = QHBoxLayout()
        spaceritem = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        hlayout.addWidget(labelTypes)
        hlayout.addSpacerItem(spaceritem)
        vlayout.addLayout(hlayout)
        
        v2layout = QVBoxLayout()
        spaceritem = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        v2layout.addSpacerItem(spaceritem)
        h2layout = QHBoxLayout()
        h2layout.addWidget(pushButtonEdit)
        h2layout.addWidget(pushButtonRestore)
        h2layout.addWidget(pushButtonClose)
        v2layout.addLayout(h2layout)
        
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.listWidgetTypes)
        hlayout.addLayout(v2layout)
        vlayout.addLayout(hlayout)
        
        self.setLayout(vlayout)
        
        self.dialog.updateTypes.connect(self.updateTypes)
        pushButtonEdit.clicked.connect(self.pushButtonEdit_clicked)
        pushButtonRestore.clicked.connect(self.pushButtonRestore_clicked)
        pushButtonClose.clicked.connect(self.close)
     
        
    
    
    def updateTypes(self):
        self.listWidgetTypes.clear()
        self.listWidgetTypes.addItems(list(self.__CompleteData.Types))
       
    
    def information(self,path):
        self.textBrowser.setText('Path: %s'%path)
        pass
    
    def pushButtonEdit_clicked(self):
        self.dialog.show()
        
    def pushButtonRestore_clicked(self):
        try:
            self.lock.lockForWrite()
            self.__CompleteData.Types = self.__OriginalTypes
        finally:
            self.lock.unlock()
        self.listWidgetTypes.clear()
        self.listWidgetTypes.addItems(self.__OriginalTypes)
        
def main():
    import sys
    import numpy as np
    app = QApplication(sys.argv)
    lock = QReadWriteLock()
    datas = np.load('/Users/Matte/Scuola/Dottorato/Projects/Pace/pitolisant/prova_binned.phz')
    data_1 = datas['WT_5075_BL_cFFT.txt'].all()
    
#    data_1.Dataset = ['ciaspole']
    dlg = datainfodlg(data_1,TimeStamps=None,TypeList=['Ciao','Cacao'],lock=lock)
    dlg.show()
    app.exec_()
    
if __name__ == '__main__':
    main()