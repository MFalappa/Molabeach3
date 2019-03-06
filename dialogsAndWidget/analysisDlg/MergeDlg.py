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
lib_dir = os.path.join(os.path.abspath(os.path.join(os.path.realpath(__file__),'../../..')),'libraries')
sys.path.append(lib_dir)
from PyQt5.QtWidgets import QDialog,QListWidgetItem,QAbstractItemView,QApplication
from PyQt5.QtCore import Qt,pyqtSlot
from PyQt5.QtGui import QIcon
import ui_mergedlg
from Modify_Dataset_GUI import DatasetContainer_GUI

MAC = 'qt_mac_set_native_menubar' in dir()

class MergeDlg(QDialog,ui_mergedlg.Ui_SelectDataset):
    def __init__(self, SelectedType = 'TSE', DataContainer=None, parent=None):
        super(MergeDlg,self).__init__(parent)
        self.NextString = '----------'
        self.setupUi(self)
        self.updateUi()
        # filter for type
        for dataName, Dataset in DataContainer:
            for Type in DataContainer[dataName].Types:
                if Type == SelectedType:                
                    item = QListWidgetItem(dataName)
                    item.setIcon(QIcon('images/table.png'))
                    self.listWidgetAllDataset.addItem(item)
        self.listWidgetAllDataset.sortItems()
        self.listWidgetAllDataset.setCurrentRow(0)
        self.listWidgetAllDataset.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidgetSelected.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        if not MAC:
            self.pushButtonAdd.setFocusPolicy(Qt.NoFocus)
            self.pushButtonCancel.setFocusPolicy(Qt.NoFocus)
            self.pushButtonDown.setFocusPolicy(Qt.NoFocus)
            self.pushButtonUp.setFocusPolicy(Qt.NoFocus)
            self.pushButtonRemove.setFocusPolicy(Qt.NoFocus)
            self.pushButtonOk.setFocusPolicy(Qt.NoFocus)
            self.pushButtonNext.setFocusPolicy(Qt.NoFocus)
        
        self.listWidgetAllDataset.currentRowChanged[int].connect(self.updateUi)
        self.listWidgetSelected.currentRowChanged[int].connect(self.updateUi)
        self.lineEditMergedName.textEdited[str].connect(self.updateUi)
        self.pushButtonOk.clicked.connect(self.createMergeDictionary)
#        self.connect(self.listWidgetAllDataset,SIGNAL('currentRowChanged (int)'),self.updateUi)
#        self.connect(self.listWidgetSelected,SIGNAL('currentRowChanged (int)'),self.updateUi)
#        self.connect(self.lineEditMergedName,SIGNAL('textEdited (const QString&)'),self.updateUi)
#        self.connect(self.pushButtonOk,SIGNAL('clicked()'),self.createMergeDictionary)
        self.updateUi()
        
    def updateUi(self):
        enable =  self.listWidgetSelected.currentRow() != -1 
        enable1  = self.listWidgetAllDataset.currentRow() != -1
        self.pushButtonRemove.setEnabled(enable)
        self.pushButtonAdd.setEnabled(enable1)
        BreakItems = self.listWidgetSelected.findItems(self.NextString,
                                                       Qt.MatchExactly)
        try:
            LastBreakRow = self.listWidgetSelected.row(BreakItems[-1])
            if LastBreakRow+1 == self.listWidgetSelected.count():
               NumDatasetToMerge = len(BreakItems) 
            else:
                NumDatasetToMerge = len(BreakItems)+1
        except IndexError:
            NumDatasetToMerge = 1
        
        DataNames=str(self.lineEditMergedName.text()).split(';')
        
        try:
            while True:
                DataNames.remove('')
        except ValueError:
            pass
        
        if enable and len(DataNames)==NumDatasetToMerge:
            self.pushButtonOk.setEnabled(True)
            
        else:
            self.pushButtonOk.setEnabled(False)
        
    
    @pyqtSlot()
    def on_pushButtonAdd_clicked(self):
        Items = self.listWidgetAllDataset.selectedItems()
        last = self.listWidgetSelected.count()
        if last != 0:
            lastItem = self.listWidgetSelected.item(last-1)
            print(str(lastItem.text()))
            if str(lastItem.text()) != self.NextString:
                if self.DataTypeDict[str(lastItem.text())] !=\
                    self.DataTypeDict[str(Items[0].text())]:
                    return
        for i in range(len(Items)):
            Item = self.listWidgetAllDataset.takeItem(self.listWidgetAllDataset.row(Items[i]))
            self.listWidgetSelected.addItem(Item)
            self.listWidgetSelected.setCurrentItem(Item)
        
            
    
    @pyqtSlot()
    def on_pushButtonRemove_clicked(self):
        Items = self.listWidgetSelected.selectedItems()
        for i in Items:
            Item = self.listWidgetSelected.takeItem(self.listWidgetSelected.row(i))
            if i.text() == self.NextString:
                continue
            self.listWidgetAllDataset.addItem(Item)
            self.listWidgetAllDataset.setCurrentItem(Item)
            self.listWidgetAllDataset.sortItems()
    
    @pyqtSlot()
    def on_pushButtonUp_clicked(self):
        Row= self.listWidgetSelected.currentRow()
        Item = self.listWidgetSelected.takeItem(Row)
        self.listWidgetSelected.insertItem(Row-1,Item)
        self.listWidgetSelected.setCurrentRow(self.listWidgetSelected.row(Item))
    
    @pyqtSlot()
    def on_pushButtonDown_clicked(self):
        Row= self.listWidgetSelected.currentRow()
        Item = self.listWidgetSelected.takeItem(Row)
        self.listWidgetSelected.insertItem(Row+1,Item)
        self.listWidgetSelected.setCurrentRow(self.listWidgetSelected.row(Item))
    
    @pyqtSlot()
    def on_pushButtonNext_clicked(self):
        BreakItems = self.listWidgetSelected.findItems(self.NextString,
                                                       Qt.MatchExactly)
        
        NumElements = self.listWidgetSelected.count()
        if NumElements>1:
            try:
                if NumElements-self.listWidgetSelected.row(BreakItems[-1])>2:
                    self.listWidgetSelected.addItem(self.NextString)
            except IndexError:
                self.listWidgetSelected.addItem(self.NextString)

    def createMergeDictionary(self):
        list_names = self.lineEditMergedName.text().split(';')
        ind_data = 0
        self.mergeDict = {}
        for name in list_names:
            self.mergeDict[name] = []
        for row in range(self.listWidgetSelected.count()):
            item_text = self.listWidgetSelected.item(row).text()
            if item_text == self.NextString:
                ind_data += 1
            else:
                self.mergeDict[list_names[ind_data]] += [item_text]
        self.accept()
        

def main():        

    import sys
    import numpy as np
    text=['Ciao Come va','ciao come va','analizzo','canalizzo','analizzom'
        ,'diario','polli','aviario','----------','Ciccio']
    dc = DatasetContainer_GUI()
    tmp = np.load('/Users/Matte/Desktop/Paper marta/data/Sleep phz/baseline/PWS_22.phz')
    for key in list(tmp.keys()):
        dc.add(tmp[key].all())
    app = QApplication(sys.argv)
    form = MergeDlg(DataContainer=dc)
    form.show()
    app.exec_()
    try:
        return form.mergeDict
    except:
        pass
if __name__ == "__main__":
    md = main()