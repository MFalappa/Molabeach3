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
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QVBoxLayout,QLineEdit,QAbstractItemView,
                             QScrollArea,QWidget,QFormLayout,QPushButton,QSpacerItem,
                             QSizePolicy,QApplication)
from PyQt5.QtCore import QObject
from ui_data_type_selection import Ui_Dialog
import numpy as np
import sys,os
phenopy_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(phenopy_dir)
from MyDnDDialog import MyDnDListWidget


class layout_container(QObject):
    def __init__(self, method):
        super(layout_container,self).__init__()
        self.hlayout_dict = {}
        self.vlayout_dict = {}
        self.widget_dict = {}
        self.method = method
#        self.rownum = 0
                
    def addHLayout(self,row):
        self.hlayout_dict[row]  = QHBoxLayout()
#        self.rownum += 1
    
    def addVLayout(self,row,col,name = 'Group 0'):
#        if row >= self.rownum:
#            raise ValueError, 'h must be < %d, the number of hlayouts'%self.rownum
        if col > 3:
            raise ValueError('col must be between 1 and 3')
        if row not in self.vlayout_dict:
            self.vlayout_dict[row] = {}
            self.widget_dict[row] = {}
        self.vlayout_dict[row][col] = QVBoxLayout()
        self.widget_dict[row][col] = {}
        self.widget_dict[row][col][0] = QLineEdit(name)
        self.widget_dict[row][col][1] = MyDnDListWidget()
        model = self.widget_dict[row][col][1].model()
        model.rowsInserted.connect(self.method)
        model.rowsRemoved.connect(self.method)
        self.widget_dict[row][col][1].setDragDropMode(QAbstractItemView.DragDrop)
        self.vlayout_dict[row][col].addWidget(self.widget_dict[row][col][0])
        self.vlayout_dict[row][col].addWidget(self.widget_dict[row][col][1])
        self.hlayout_dict[row].addLayout(self.vlayout_dict[row][col])
        self.method()
        
    def remove_widget(self,row,col):
        self.vlayout_dict[row][col].removeWidget(self.widget_dict[row][col][1])
        self.vlayout_dict[row][col].removeWidget(self.widget_dict[row][col][0])
        self.widget_dict[row].pop(col)
    
    def removeVLayout(self,row,col):
        list_item = []
        listwidget = self.widget_dict[row][col][1]
        while listwidget.count():
            list_item += [listwidget.takeItem(0)]
        while self.vlayout_dict[row][col].count():
            child = self.vlayout_dict[row][col].takeAt(0)
            child.widget().deleteLater()
        self.vlayout_dict[row].pop(col)
        self.widget_dict[row].pop(col)
        return list_item
        
    def removeHLayout(self,row):
        list_item = []
        for col in np.sort(list(self.vlayout_dict[row].keys())):
            list_item += self.removeVLayout(row,col)
        self.vlayout_dict.pop(row)
        self.hlayout_dict.pop(row)
        self.widget_dict.pop(row)
        self.method()
        return list_item
            
    def getLastRow(self):
        return max(self.hlayout_dict.keys())
    
    def getLastElement(self):
        max_row = self.getLastRow()
        return max_row, max(self.vlayout_dict[max_row].keys()) 
    
    def getGroupName(self,row,col):
        return self.widget_dict[row][col][0].text()
    
    def get_dict_type(self):
        dict_res = {}
        for row in list(self.widget_dict.keys()):
            for col in list(self.widget_dict[row].keys()):
                key = self.widget_dict[row][col][0].text()
                dict_res[key] = []
                for itemNum in range(self.widget_dict[row][col][1].count()):
                    item = self.widget_dict[row][col][1].item(itemNum)
                    dict_res[key] += [item.text()]
        return dict_res
        
    
    def __repr__(self):
        string =  'WIDGET DICT\n'
        for i in list(self.widget_dict.keys()):
            string += '\t%d:\n'%i
            for j in list(self.widget_dict[i].keys()):
                string += '\t\t%d: '%j+'widgets' + '\n'
        string += 'vlayout DICT\n'
        for i in list(self.vlayout_dict.keys()):
            string +=  '\t%d:\n'%i
            for j in list(self.vlayout_dict[i].keys()):
                string += '\t\t%d: '%j+ 'vlaout' + '\n'
        string += 'hlayout DICT\n'
        for i in list(self.hlayout_dict.keys()):
            string += '\t%d:'%i + '%s'%self.hlayout_dict[i]+'\n'
        return string
            
class data_type_selection(QDialog, Ui_Dialog):
    def __init__(self, type_list, parent=None):
        super(data_type_selection,self).__init__(parent)
        self.setupUi(self)
        self.spinBox_typeNum.setRange(2,len(type_list))
        self.spinBox_typeNum.setValue(2)
        self.dict_group_types = {}
        self.listWidget_allTypes = MyDnDListWidget()
        for types in type_list:
            self.listWidget_allTypes.addItem(types)
        self.verticalLayout.addWidget(self.listWidget_allTypes)
        self.scrollArea = QScrollArea()
        self.verticalLayout.addWidget(self.scrollArea)
        
        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        
        
        
        self.pushButtonContinue = QPushButton('Continue')
        self.setup_ScrollArea()
        pushButtonCancel  = QPushButton('Cancel')
        spacerItem = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        buttonLayout = QHBoxLayout()
        buttonLayout.addSpacerItem(spacerItem)
        buttonLayout.addWidget(pushButtonCancel)
        buttonLayout.addWidget(self.pushButtonContinue)
        self.verticalLayout.addLayout(buttonLayout)
        
        self.spinBox_typeNum.valueChanged[int].connect(self.spinBoxChanged)
        pushButtonCancel.clicked.connect(self.spinBoxChanged)
        self.pushButtonContinue.clicked.connect(self.spinBoxChanged)
       
    
    def setup_ScrollArea(self):
        self.layout_container = layout_container(self.checkOk)
        tot_vals = self.spinBox_typeNum.value()
        num_rows = int(np.ceil(tot_vals / 3.))
        grnum = 0
        for row in range(num_rows):
            self.layout_container.addHLayout(row)
            for col in range(3*row, min(tot_vals,3*(row+1))):
                col = col - 3 * row
                self.layout_container.addVLayout(row,col,'Group %d'%grnum)
                grnum += 1
            self.scrollLayout.addRow(self.layout_container.hlayout_dict[row])

    def spinBoxChanged(self,value):
        print('Changed Value', value)
        max_num = 3 * self.layout_container.getLastRow() + self.layout_container.getLastElement()[1] +1
        print(max_num)
        if value < max_num:
            self.removeLastLists(list(range(value, max_num)))
        elif value > max_num:
            self.addLists(list(range(max_num,value)))
    
    def addLists(self, labels):
        rows = np.array(labels) // 3
        cols = np.array(labels) % 3
        max_row, last_col = self.layout_container.getLastElement()
        grnum = 3 * max_row + last_col + 1
        for k in range(cols.shape[0]):
            if cols[k] == 0:
                self.layout_container.addHLayout(rows[k])
                self.scrollLayout.addRow(self.layout_container.hlayout_dict[rows[k]])
            self.layout_container.addVLayout(rows[k],cols[k],'Group %d'%grnum)
            grnum += 1   
            
    def getTypesAndAccept(self):
        self.dict_res = self.layout_container.get_dict_type()
        self.accept()
        
    def checkOk(self):
        print('checking')
        dict_res = self.layout_container.get_dict_type()
        for key in list(dict_res.keys()):
            if not dict_res[key]:
                self.pushButtonContinue.setEnabled(False)
                return
        self.pushButtonContinue.setEnabled(True)
    
    def removeLastLists(self, labels):
        list_item = []
        rows = np.array(labels) // 3
        cols = np.array(labels) % 3
        for k in range(cols.shape[0])[::-1]:
            if cols[k] == 0:
                list_item += self.layout_container.removeHLayout(rows[k])
            else:
                list_item += self.layout_container.removeVLayout(rows[k],cols[k])
        for item in list_item:
            self.listWidget_allTypes.addItem(item)
    
        
def main():
    import sys
    app = QApplication(sys.argv)
    form = data_type_selection(['Tipo 1','Tipo 2','Tipo 3','Tipo 4','Tipo 5','Tipo 6','a','b','c','d'])
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()