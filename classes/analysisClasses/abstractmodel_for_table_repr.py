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
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
sys.path.append(lib_dir)
from PyQt5.QtWidgets import (QTableView,QWidget,QDialog,QApplication,
                             QHBoxLayout,QPushButton)
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import pandas as pd
import numpy as np
from copy import copy
from Modify_Dataset_GUI import EEG_Data_Struct

class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None
        
    def insertRows(self, position, newdata, index=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(),position,position+len(newdata.values)-1)
        self._data =self._data.append(newdata)
        self.endInsertRows()
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            try:
                self._data.set_value(self._data.index[index.row()],self._data.columns[index.column()],value)
                self.dataChanged.emit(index, index)
            except Exception as e:
                print(e)
                return False
        return False
    
    

class StructuredNumpyModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return len(self._data.dtype.names)
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data[self._data.dtype.names[index.column()]][index.row()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.dtype.names[col]
        return None
    
    def insertRows(self, position, newdata, index=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(),position,position+newdata.shape[0]-1)
        self._data = np.hstack((self._data,newdata))
        self.endInsertRows()

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
    
            row = index.row()
            column = index.column()
            try:
                self._data[self._data.dtype.names[column]][row] = value
                self.dataChanged.emit(index, index)
            except Exception as e:
                print(e)
                return False
        return False
        
class MyTableView(QTableView):
    def __init__(self,model,data,nrows,adjust_every=100,parent=None):
        super(MyTableView,self).__init__(parent)
        self.adjust_every = adjust_every
        model = model(data[:adjust_every])
        self.setModel(model)
        self.data = data
        self.nrows = nrows
        self.irange = (0,min(adjust_every,self.model().rowCount()))
        self.verticalScrollBar().valueChanged.connect(self.adjustTable)
        
    def adjustTable(self,val):
        MAX = self.verticalScrollBar().maximum()
        if val == MAX and self.irange[1] <= self.nrows:
            self.irange = (self.irange[0] + self.adjust_every,self.irange[1] + self.adjust_every)
            newdata = self.data[self.irange[0]:self.irange[1]]
            position = self.model().rowCount()
            self.model().insertRows(position,newdata)
    
    def setItem(self,row,col,value):
        while row > self.irange[0] + self.adjust_every:
            self.irange = (self.irange[0] + self.adjust_every, self.irange[1] + self.adjust_every)
            newdata = self.data[self.irange[0]:self.irange[1]]
            position = self.model().rowCount()
            self.model().insertRows(position,newdata)
        index = self.model().index(row,col)
        self.model().setData(index,value)
        self.scrollTo(index)
    
    def getData(self):
        return self.model()._data
        

class TableView_excelFile(QWidget):
    def __init__(self,excel,parent=None):
        super(TableView_excelFile,self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        hlayout = QtGui.QHBoxLayout()
        self.dict_excel = {}
        self.dict_nrows = {}
        self.list_sheet = excel.sheet_names
        combo = QtGui.QComboBox()
        for key in excel.sheet_names:
            self.dict_excel[key] = excel.parse(sheetname=key)
            self.dict_nrows[key] = self.dict_excel[key].shape[0]
            combo.addItem(key)
        self.tableWidget = table_view_setter(self.dict_excel[self.list_sheet[0]])[0]
        self.model = self.tableWidget.model
        hspacer = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        label = QtGui.QLabel('%s:'%self.list_sheet[0])
        hlayout.addWidget(label)
        hlayout.addSpacerItem(hspacer)
        layout.addLayout(hlayout)
        layout.addWidget(self.tableWidget)
        hspacer = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        layout.addWidget(combo)
        self.setLayout(layout)
        self.connect(combo,QtCore.SIGNAL('currentIndexChanged (const QString&)'),self.switch_table)
        
    def switch_table(self,string):
        model = PandasModel(self.dict_excel[string])
        self.tableWidget.setModel(model)
        self.irange = (0,min(100,self.tableWidget.model().rowCount()))
        self.tableWidget.nrows = self.dict_nrows[string]
        self.tableWidget.data = self.dict_excel[string]
        

class TableView_dictionary(QWidget):
    def __init__(self,dictionary,parent=None):
        super(TableView_dictionary,self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        hlayout = QtGui.QHBoxLayout()
        self.dict_excel = dictionary
        self.dict_nrows = {}
        self.list_sheet = list(dictionary.keys())
        combo = QtGui.QComboBox()
        for key in self.list_sheet:
            try:
                self.dict_nrows[key] = self.dict_excel[key].shape[0]
            except:
                self.dict_nrows[key] = 0
            combo.addItem(key)
        self.tableWidget = table_view_setter(self.dict_excel[self.list_sheet[0]])[0]
        if not self.tableWidget:
            data = np.zeros(0, dtype={'names':('unkown',),'formats':(int,)})
            self.tableWidget = table_view_setter(data)[0]
        hspacer = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        label = QtGui.QLabel('%s:'%self.list_sheet[0])
        hlayout.addWidget(label)
        hlayout.addSpacerItem(hspacer)
        layout.addLayout(hlayout)
        layout.addWidget(self.tableWidget)
        hspacer = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        layout.addWidget(combo)
        self.setLayout(layout)
        self.connect(combo,QtCore.SIGNAL('currentIndexChanged (const QString&)'),self.switch_table)
        
    def switch_table(self,string):
        if type(self.dict_excel[string]) == pd.DataFrame:
            model = PandasModel(self.dict_excel[string])
        elif type(self.dict_excel[string]) == np.ndarray and self.dict_excel[string].dtype.names:
            model = StructuredNumpyModel(self.dict_excel[string])
        else:
            data = np.zeros(0, dtype={'names':('unkown',),'formats':(int,)})
            model = StructuredNumpyModel(data)
        self.tableWidget.setModel(model)
        self.irange = (0,min(100,self.tableWidget.model().rowCount()))
        self.tableWidget.nrows = self.dict_nrows[string]
        self.tableWidget.data = self.dict_excel[string]      
    
    
        
        
def table_view_setter(data):
    data = copy(data)
    if type(data) == EEG_Data_Struct:
        data = data.reconstructDataMatrix()
    if type(data) is pd.DataFrame:
        model = PandasModel
        nrows = data.shape[0]
    elif type(data) is np.ndarray and data.dtype.names:
        model = StructuredNumpyModel
        nrows = data.shape[0]
    elif type(data) is dict:
        return TableView_dictionary(data),''
    elif type(data) is pd.ExcelFile:
        return TableView_excelFile(data),''
    else:
        return False, 'Unsupported data format for viewing %s'%(type(data))        
    
    return MyTableView(model,data,nrows),''
    
class prova(QDialog):
    def __init__(self,df,adjust_every=100,parent=None):
        super(prova,self).__init__(parent)
        table, string = table_view_setter(df)
        if not table:
            return string
          
        layout = QHBoxLayout()
        self.tw = table
        layout.addWidget(self.tw)
        button = QPushButton('Test')
        layout.addWidget(button)
        self.setLayout(layout)
        button.clicked.connect(self.test)
    def test(self):
        self.tw.setItem(1,1,np.inf)
        
def main():
    import sys
    app = QApplication(sys.argv)
#    excel = pd.ExcelFile('C:\Users\ebalzani\IIT\Dottorato\Tracking\Lab book  Cancedda\\Final DREADDs huddling analyses up to p10_8_11_16.xlsx')
#    widget = TableView_excelFile(excel)
#    widget.show()
#    app.exec_()
#==============================================================================
#     Dizionario
#==============================================================================
#    d ={}
#    for key in excel.sheet_names:
#        d[key] = excel.parse(key)
#    d[key] = np.array(d[key])
#    d['Edo'] = {}
#    d['Mat'] = np.arange(5)
#    widget = TableView_dictionary(d)
#
#    widget.show()
#    app.exec_()
#==============================================================================
    
    
#==============================================================================
#   excel file 
#==============================================================================
#    widget = TableView_excelFile(excel)
#    widget.show()
#    app.exec_()
#==============================================================================
   
   
#==============================================================================
# Pandas dataframe
#==============================================================================
#    model = PandasModel
#    df = pd.ExcelFile('C:\Users\ebalzani\IIT\Dottorato\Tracking\Lab book  Cancedda\\time_course_npy\\subjective_tc_time_spent_togheter_control.xls').parse()
#    form = prova(df)
#    print form.exec_()
#==============================================================================

#==============================================================================
#   numpy array structured
#==============================================================================
    import numpy as np
    df = np.ones(1000,dtype={'names':('a','b'),'formats':('S120',float)})
    df['b'] = np.random.uniform(size=1000)
    df['a'] = 'sciamalaya!'
    model = StructuredNumpyModel
    form = prova(df)
    form.show()
    res = app.exec_()
    
#    print res
if __name__ == '__main__':
    main()