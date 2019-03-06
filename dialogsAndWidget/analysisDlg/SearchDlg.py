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
import re
from PyQt5.QtWidgets import (QDialog,QApplication)
from PyQt5.QtCore import pyqtSignal, pyqtSlot,Qt
from PyQt5.QtGui import *
import ui_searchDlg

MAC = 'qt_mac_set_native_menubar' in dir()

class SearchDlg(QDialog,ui_searchDlg.Ui_SearchDlg):
    def __init__(self,dict_type,type_available=[],parent=None):
        print("INTEGRATIVE DICTIONARY MUST CONTAIN DICT OF TYPES")
        super(SearchDlg,self).__init__(parent)
        self.Analysis = None
        self.dict_type = dict_type
        self.type_available = type_available
        self.dict_type = self.checkAvailableAnalysis()
        self.__index=0
        self.__firstSearchClick = True
        self.selectedAnalysis = None
        self.setupUi(self)
        self.updateUi()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Select Analysis')
        self.setObjectName('Select Analysis')
        
        if not MAC:
            self.searchPushButton.setFocusPolicy(Qt.NoFocus)
            self.okPushButton.setFocusPolicy(Qt.NoFocus)
        self.comboBox_types.addItem('All')
        for anType in list(self.dict_type.keys()):
            self.comboBox_types.addItem(anType)
        temp_data_list = []
        for anType in list(self.dict_type.keys()):
            for anName in self.dict_type[anType]:
                for datatype in self.dict_type[anType][anName]:
                    if not datatype in temp_data_list and datatype in self.type_available:
                        temp_data_list += [datatype]
        self.comboBox_types.addItems(temp_data_list)
        
        self.analysisList.currentRowChanged[int].connect(self.updateUi)
#        self.connect(self.analysisList,SIGNAL('currentRowChanged (int)'),self.updateUi)
        
        
    def updateUi(self):
        # selezione lista a seconda del dato cercato
        enable1 = self.analysisList.currentRow() >= 0
        self.okPushButton.setEnabled(enable1)
        if enable1:
            self.okPushButton.setFocus()
    
    def checkAvailableAnalysis(self):
        dict_anal = {}
        # controllo analisi singolo e gruppo
        for anType in ['Single','Group']:
            dict_anal[anType] = {}
            for anName in list(self.dict_type[anType].keys()):
                for dataType in self.dict_type[anType][anName]:
                    if dataType in self.type_available:
                        dict_anal[anType][anName] = self.dict_type[anType][anName]
                        break
            # rimuovo tipo se non ho analisi disponibili
            if not list(dict_anal[anType].keys()):
                dict_anal.pop(anType)
        dict_anal['Integrative'] = {}
        for anName in self.dict_type['Integrative']:
            for anName in list(self.dict_type['Integrative'].keys()):
                bool_add = True
                for dtype in list(self.dict_type['Integrative'][anName].keys()):
                    tmp = False
                    for mytype in self.type_available:
                        if mytype in self.dict_type['Integrative'][anName][dtype]:
                            tmp = True
                            break
                    bool_add *= tmp
                if bool_add:
                    dict_anal['Integrative'][anName] = self.dict_type['Integrative'][anName]
        print(dict_anal)
        return dict_anal
        
#    @pyqtSignal("int")
    @pyqtSlot("int")
    def on_comboBox_types_currentIndexChanged(self,i):
        self.analysisList.clear()
        filter_analysis = self.comboBox_types.itemText(i)
        if filter_analysis in ['Single','Group','Integrative']:
            self.filter_per_analysis_type(filter_analysis)
        else:
            self.filter_per_data_type(filter_analysis)
        self.analysisList.sortItems()
    

    
    def  filter_per_analysis_type(self,filter_analysis):
        for anName in self.dict_type[filter_analysis]:
            self.analysisList.addItem(anName)
    
    def filter_per_data_type(self,filter_analysis):
        bool_all = filter_analysis == 'All'
        for anType in list(self.dict_type.keys()):
            for anName in self.dict_type[anType]:
                if bool_all or filter_analysis in self.dict_type[anType][anName]:
                    self.analysisList.addItem(anName)
        
    
    @pyqtSlot()
    def on_searchPushButton_clicked(self):
        item_list = []
        for ind in range(self.analysisList.count()):
            item_list += [self.analysisList.item(ind).text()]
        
        if self.__firstSearchClick:
            self.__Matching_Row = []
            regex = self.makeRegex()
            for Row in range(len(item_list)):
                if regex.search(item_list[Row]) is not None:
                    self.__Matching_Row = self.__Matching_Row + [Row]
        self.self__firstSearchClick = False
        if self.__Matching_Row != []:
            self.__index = (self.__index)%len(self.__Matching_Row)
            RowToFocus = self.__Matching_Row[self.__index]
            self.analysisList.setCurrentRow(RowToFocus)
            self.__index += 1
        else:
            self.analysisList.setCurrentRow(-1)
        
    def makeRegex(self):
        
        findText = str(self.searchAnalisisLineEdit.text())
        
        findText = re.escape(findText)
        flags = re.MULTILINE | re.DOTALL | re.UNICODE
        
        flags |= re.IGNORECASE 
        
        
        return re.compile(findText,flags)
    
    def accept(self):
        Row = self.analysisList.currentRow()
        if Row !=-1:
            self.selectedAnalysis = self.analysisList.item(Row).text()
            for dtype in list(self.dict_type.keys()):
                if self.selectedAnalysis in self.dict_type[dtype]:
                    break
            self.selectedDataTypes = self.dict_type[dtype][self.selectedAnalysis]
            self.selectedType = dtype
        QDialog.accept(self)
    
def main():
    import sys
    text=['Actogram','Sleep time course','GR Sleep time course','Matte','Switch Latency']
    app = QApplication(sys.argv)
    form = SearchDlg({'Single':{'Actogram':['TSE','AM-Micro'],
                                     'Sleep Time Course':['SleepSign']},
                            'Group':{'GR Sleep time course':['SleepSign','BK'],
                                     'Switch Latency':['TSE']},
                            'Integrative':{'Matte':{'dato1':['TSE','AM-Micro'],'dato2':['Plx']}}},
        type_available = ['BK','Plx','AM-Micro'])
    form.exec_()
    print(form.selectedAnalysis,form.selectedDataTypes,form.selectedType)
if __name__ == "__main__":
    main()
    
    #form.show()
    #print app.exec_()
