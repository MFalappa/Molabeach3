#!/usr/bin/env python
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.


# modified by Matteo in 2019 to adapt to python3




import sys
from PyQt5.QtCore import (QPluginLoader)
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                         QLabel, QLineEdit,QListWidgetItem, QGridLayout, 
                         QDialogButtonBox,QComboBox)

from PyQt5.QtGui import QIcon,QFont
from copy import copy

from MyDnDDialog import MyDnDListWidget

QPlugin = QPluginLoader("qico5.dll")
class CreateGroupsDlg(QDialog):
# rimuovere anDict, e' obsoleto
    def __init__(self, GroupNumber=2, DataList=[],DataContainer=None,
                 TypeList=['All'],SetIndex=-1,
                           dataLim=None, groupName=None, dataName=None,
                           parent=None):
        super(CreateGroupsDlg, self).__init__(parent)
    
        VLayout = QVBoxLayout()
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        string = ''
        if dataName:
            string += ' %s'%dataName
        titleLabel = QLabel('All Dataset:' + string)
        titleLabel.setFont(font)
        VLayout.addWidget(titleLabel)
        self.dataListWidget = MyDnDListWidget()
        self.AllDataList=copy(DataList)
        self.dataLim = dataLim
        if not 'All' in  TypeList:
            TypeList += ['All']
        self.DataContainer=DataContainer
        for data in DataList:
            item = QListWidgetItem(data)
            item.setIcon(QIcon('images/table.png'))
            self.dataListWidget.addItem(item)
   
        self.dataListWidget.sortItems()
        VLayout.addWidget(self.dataListWidget)
        self.groupListWidget = {}
        self.lineEditWidget = {}
        grid = QGridLayout()
        row = 0
        for i in range(GroupNumber):
            
            column = i%4
            
            if i%4==0 and i!=0:
                row+=2
            self.groupListWidget[i] = MyDnDListWidget()
            if not groupName:
                self.lineEditWidget[i] = QLineEdit('Group %d'%(i+1))
            else:
                self.lineEditWidget[i] = QLineEdit(groupName[i])
                self.lineEditWidget[i].setReadOnly(True)
            grid.addWidget(self.groupListWidget[i],row+1,column,1,1)
            grid.addWidget(self.lineEditWidget[i],row,column,1,1)
            if not groupName:
                self.lineEditWidget[i].editingFinished.connect(lambda number = i : self.updateEdit(number))
#                self.connect(self.lineEditWidget[i],
#                             SIGNAL('editingFinished()'),
#                             lambda number = i : self.updateEdit(number))
        self.filterComboBox=QComboBox()
        self.filterComboBox.addItems(TypeList)
        comboLabel=QLabel()
        comboLabel.setText('Filter Per Data Type')
        VLayout.addLayout(grid)
        self.ButtonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)        
        HLayout=QHBoxLayout()
        HLayout.addWidget(comboLabel)
        HLayout.addWidget(self.filterComboBox)
        HLayout.addStretch()
        VLayout.addLayout(HLayout)
        VLayout.addWidget(self.ButtonBox)
        self.setLayout(VLayout)
        
        self.ButtonBox.accepted.connect(self.accept)
        self.ButtonBox.rejected.connect(self.reject)

        
        
        self.filterComboBox.currentIndexChanged[int].connect(self.refreshDataList)
#        self.connect(self.filterComboBox,SIGNAL('currentIndexChanged(int)'),
#                         self.refreshDataList)
        
        self.filterComboBox.setCurrentIndex(0)
        self.refreshDataList()
        
#        self.dataListWidget.dropEvent(lambda Key=None:self.enableOk(Key))
        
        self.dataListWidget.dropped.connect(lambda Key=None:self.enableOk(Key))
        self.dataListWidget.dragged.connect(self.startDrag)
#        self.connect(self.dataListWidget,SIGNAL('dropped()'),lambda Key=None:self.enableOk(Key))
#        self.connect(self.dataListWidget,SIGNAL('dragged()'),self.startDrag)
        for key in list(self.groupListWidget.keys()):
            
            self.groupListWidget[key].dropped.connect(lambda Key=key:self.refreshAllData(Key))
            self.groupListWidget[key].dragged.connect(lambda Key=key:self.enableOk(Key))
#            self.connect(self.groupListWidget[key],SIGNAL('dropped()'), lambda Key=key:self.refreshAllData(Key))
#            self.connect(self.groupListWidget[key],SIGNAL('dragged()'),lambda Key=key:self.enableOk(Key))    
        self.setWindowTitle("Select Groups")
        
        
    def startDrag(self):
        print('Start Moving')
        for Key in list(self.groupListWidget.keys()):
            try:
                last = self.groupListWidget[Key].count()-1
                lastItemText= str(self.groupListWidget[Key].item(last).text())
                self.AllDataList.remove(lastItemText)
                print( self.AllDataList)    
            except (ValueError,AttributeError):
                pass
        
    
    def enableOk(self,ThisKey):
        print('Entered here',type(ThisKey))
        if ThisKey != None:
            if self.dataLim != None and self.dataLim[ThisKey] != -1 and\
                self.groupListWidget[ThisKey].count() > self.dataLim[ThisKey]:
                item = self.groupListWidget[ThisKey].takeItem(\
                    self.groupListWidget[ThisKey].count()-1)
                self.dataListWidget.addItem(item)
                print('added an item to datalistwidget')
                return
            print('matte',ThisKey )
            itemInd = self.groupListWidget[ThisKey].count() - 1
            item = self.groupListWidget[ThisKey].item(itemInd)
            try:
                print(str(item.text()))
                self.AllDataList.remove(str(item.text()))
                print('Done removing')
            except (ValueError, AttributeError):
                pass
        else:
            self.refreshAllData(None)
        for key in list(self.groupListWidget.keys()):
            print(self.groupListWidget[key].count())
            if not self.groupListWidget[key].count():
                self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(False)
                return
        self.ButtonBox.button(self.ButtonBox.Ok).setEnabled(True)
                
    def updateEdit(self,number):
        Name = self.lineEditWidget[number].text()
        if not Name:
            self.lineEditWidget[number].setText('Group %d'%(number+1))
            
    def refreshDataList(self):
        self.dataListWidget.clear()
        Type=self.filterComboBox.currentText()
        if Type == 'All':
            for data in self.AllDataList:
                item = QListWidgetItem(data)
                item.setIcon(QIcon('images/table.png'))
                self.dataListWidget.addItem(item)
        else:
            for data in self.AllDataList:
                if Type in self.DataContainer._DatasetContainer_GUI__Datas[data].Types:
                        item = QListWidgetItem(data)
                        item.setIcon(QIcon('images/table.png'))
                        self.dataListWidget.addItem(item)
        self.dataListWidget.sortItems()
    
    def returnSelectedNames(self):
        selectedDatas = {}
        for k in list(self.groupListWidget.keys()):
            grName = str(self.lineEditWidget[k].text())
            item = self.groupListWidget[k].takeItem(0)
            selectedDatas[grName] = []
            while item:
                selectedDatas[grName] += [str(item.text())]
                item = self.groupListWidget[k].takeItem(0)
        return selectedDatas
        
    def refreshAllData(self, Key):
        if Key is None:
            for k in range(self.dataListWidget.count()):
                itemText = str(self.dataListWidget.item(k).text())
                try:
                    self.AllDataList.remove(itemText)
                except ValueError:
                    pass
                self.AllDataList.append(itemText)
        else:
            self.enableOk(Key)
            
            
def main():
    app = QApplication(sys.argv)
    Data=[]
    for i in range(1,13):
        Data+=['Cage %d'%i]
    form = CreateGroupsDlg(3,Data)
    form.show()
    
    app.exec_()
    print(form.lineEditWidget[2].text())

if __name__ == '__main__':
    main()
