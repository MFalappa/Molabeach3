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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from difflib import SequenceMatcher
from MyDnDDialog import MyDnDListWidget
import os
import sys
image_fld = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'images')
lib_fld = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
sys.path.append(lib_fld)
from Modify_Dataset_GUI import DatasetContainer_GUI
import numpy as np
## TMP import
import pandas as pd

def matrix_matching(s_list1,s_list2):
    string_matcher = lambda s1,s2: SequenceMatcher(None,s1.upper(),s2.upper()).ratio()
    matrix = np.zeros((len(s_list1),len(s_list2)))
    j= 0
    for s1 in s_list1:
        i = 0
        for s2 in s_list2:
            matrix[j,i] = string_matcher(s1,s2)
            i += 1
        j += 1
    return matrix

def list_sort_index(matrix):
    if matrix.shape[1] != matrix.shape[0]:
        raise ValueError, 'matrix must be squared'
    k = 0
    isort_list = np.zeros(matrix.shape[1]) * np.nan
    while k < matrix.shape[1]:
        isort = np.where(matrix == np.max(matrix))
        isort_list[isort[1][0]] = isort[0][0]
        matrix[:,isort[1][0]] = -1
        matrix[isort[0][0],:] = -1
        k += 1
    return np.array(isort_list,dtype=int)

class pairDataDlg(QDialog):
    def __init__(self,dict_types,dataset_cont,lock,parent=None):
        super(pairDataDlg,self).__init__(parent)
        dataset_list = []
        try:
            lock.lockForRead()
            for name, tmp in dataset_cont:
                for key in  dict_types.keys():
                    if dataset_cont.dataType(name)[0] in dict_types[key]:
                        dataset_list += [name]
                        break
        finally:
            lock.unlock()
        self.dataset_cont = dataset_cont
        self.dict_types = dict_types
        self.lock = lock
        
        self.string_matcher = lambda s1,s2: SequenceMatcher(None,s1.upper(),s2.upper()).ratio()
        
        data_label = dict_types.keys()
        nrows = len(data_label) // 4 + (len(data_label)%4!=0) + 1
        ncols = min(4,len(data_label))
        print nrows,ncols
        
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget(scrollArea)
        scrollAreaWidgetContents.setGeometry(QRect(0, 0, 600, 732))
        scrollArea.setWidget(scrollAreaWidgetContents)
        layout = QGridLayout()
        
        self.pixmap = QPixmap(os.path.join(image_fld,'table.png'))
        self.pixmap = self.pixmap.scaledToHeight(self.pixmap.height()//20)
        
        self.list_all_data = MyDnDListWidget(parent=scrollAreaWidgetContents)
        self.max_sub_name_len = 0
        for name in dataset_list:
            item = QListWidgetItem()
            icon = QIcon(self.pixmap)
            item.setText(name)
            item.setIcon(icon)
            self.list_all_data.addItem(item)
            self.max_sub_name_len = max(self.max_sub_name_len,len(name))
            
        self.list_all_data.setIconSize(self.pixmap.size())
        selectDataLabel = QLabel('Selected Dataset:')
        spacerItem = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Maximum)
        hlayout = QHBoxLayout()
        hlayout.addWidget(selectDataLabel)
        hlayout.addSpacerItem(spacerItem)
        layout.addLayout(hlayout,1,1,1,ncols)
        layout.addWidget(self.list_all_data,2,1,1,ncols)
        
        self.dictListWidgetType = {}
        ind_lab = 0
        for label in data_label:
            vlayout = QVBoxLayout()
            hlayout = QHBoxLayout()
            spacerItem = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Maximum)
            hlayout.addWidget(QLabel(label,parent=scrollAreaWidgetContents))
            hlayout.addSpacerItem(spacerItem)
            vlayout.addLayout(hlayout)
            self.dictListWidgetType[label] = MyDnDListWidget(parent=scrollAreaWidgetContents)
            self.dictListWidgetType[label].setMinimumSize(200,150)
            vlayout.addWidget(self.dictListWidgetType[label])
            layout.addLayout(vlayout,3+ind_lab//ncols,1+ind_lab%ncols,1,1)
            self.connect(self.dictListWidgetType[label],SIGNAL('dropped()'),self.checkLists)
            ind_lab += 1
        # Create an empty pairMatrix
        print self.max_sub_name_len
        type_list = self.dictListWidgetType.keys()
        col_names = ['Subject_num']+ type_list
        col_types = [int] + ['S%d'%self.max_sub_name_len]*len(type_list)
        self.pairMatrix = np.zeros(0,dtype={'names':col_names,'formats':col_types})
                              
        scrollAreaWidgetContents.setLayout(layout)
        vlayout=QVBoxLayout()
        vlayout.addWidget(scrollArea)
        self.pushButtonSort = QPushButton('Automated Sorting')
        self.pushButtonContinue = QPushButton('Continue')
        self.pushButtonDivide = QPushButton('Divde x data-type')
        pushButtonAdd = QPushButton('Add & Clear')
        self.pushButtonContinue.setEnabled(False)
        spacerItem = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        hlayout = QHBoxLayout()
        hlayout.addSpacerItem(spacerItem)
        hlayout.addWidget(self.pushButtonDivide)
        hlayout.addWidget(self.pushButtonSort)
        hlayout.addWidget(pushButtonAdd)
        hlayout.addWidget(self.pushButtonContinue)
        vlayout.addLayout(hlayout)
        
        
        self.setLayout(vlayout)
        
        self.connect(self.pushButtonSort,SIGNAL('clicked()'),self.automaticSort)
        self.connect(self.list_all_data,SIGNAL('dropped()'),self.disableContinue)
        self.connect(self.pushButtonContinue,SIGNAL('clicked()'),self.continuePressed)
        self.connect(pushButtonAdd,SIGNAL('clicked()'),self.addPairedAndClear)
        self.connect(self.pushButtonDivide,SIGNAL('clicked()'),self.dividePerType)
    
    def dividePerType(self):
        for k in range(self.list_all_data.count()):
            name = self.list_all_data.item(k).text()
            dataType = self.dataset_cont.dataType(name)[0]
            for key in self.dictListWidgetType.keys():
                if dataType in self.dict_types[key]:
                    item = QListWidgetItem()
                    item.setText(name)
                    item.setIcon(QIcon(self.pixmap))
                    self.dictListWidgetType[key].addItem(item)
                    break
        self.list_all_data.clear()
        try:
            self.automaticSort()
        except ValueError:
            pass
        
    
    def automaticSort(self):
        self.checkLists()
#        if not self.pushButtonSort.isEnabled():
#            return
        first_list = self.dictListWidgetType.keys()[0]
        self.dictListWidgetType[first_list].sortItems(0)
#        expected_el = first_list.count()
#        for key in self.dictListWidgetType.keys()[1:]:
#            if expected_el != 
        
        text_items = []
        numel = self.dictListWidgetType[first_list].count()
        for el in xrange(numel):
            text_items += [self.dictListWidgetType[first_list].item(el).text()]
        
        for key in self.dictListWidgetType.keys()[1:]:
            key_text = []
            numel = self.dictListWidgetType[key].count()
            for el in xrange(numel):
                key_text += [self.dictListWidgetType[key].item(el).text()]
            print key
            sort_list = list_sort_index(matrix_matching(text_items,key_text))
            self.dictListWidgetType[key].clear()
            for label in np.array(key_text)[sort_list]:
                item = QListWidgetItem()
                item.setText(label)
                item.setIcon(QIcon(self.pixmap))
                self.dictListWidgetType[key].addItem(item)

    def checkLists(self):
        counts = np.zeros(len(self.dictListWidgetType.keys()),dtype=int)
        i = 0
        for key in self.dictListWidgetType.keys():
            counts[i] = self.dictListWidgetType[key].count()
            i += 1
        if counts[0] and np.prod(counts==counts[0]):
            self.pushButtonContinue.setEnabled(True)
#            self.pushButtonSort.setEnabled(True)
        else:
            self.pushButtonContinue.setEnabled(False)
#            self.pushButtonSort.setEnabled(False)
            
    def disableContinue(self):
        QTimer.singleShot(1,self.setContinueStatus)
        
    def setContinueStatus(self):
        counts = np.zeros(len(self.dictListWidgetType.keys()),dtype=int)
        i = 0
        for label in self.dictListWidgetType.keys():
            counts[i] = self.dictListWidgetType[label].count()
            i += 1
        if counts[0] and np.prod(counts == counts[0]):
            self.pushButtonContinue.setEnabled(True)
        else:
            self.pushButtonContinue.setEnabled(False)
    
    def create_dict_pairs(self):
        """
            Creates a numpy structured array, with data types as col name,
            a subject in each row. First column must be subject name.
        """
        type_list = self.dictListWidgetType.keys()
        col_names = ['Subject_num']+ type_list
        col_types = [int] + ['S%d'%self.max_sub_name_len]*len(type_list)
        num_el = self.dictListWidgetType[type_list[0]].count()
        pairMatrix = np.zeros(num_el,
                              dtype={'names':col_names,'formats':col_types})
        
        for key in type_list:
            for i in xrange(num_el):
                item = self.dictListWidgetType[key].item(i)
                pairMatrix[key][i] = item.text()
        pairMatrix['Subject_num'] = range(num_el)
        return pairMatrix
    
    def continuePressed(self):
        self.updatePairMatrix()
        self.accept()
    
    def updatePairMatrix(self):
        pairMatrix = self.create_dict_pairs()
        if self.pairMatrix.shape[0]:
            pairMatrix['Subject_num'] = pairMatrix['Subject_num'] + self.pairMatrix['Subject_num'][-1] + 1
        self.pairMatrix = np.hstack((self.pairMatrix,pairMatrix))
        
    def addPairedAndClear(self):
        self.updatePairMatrix()
        for key in self.dictListWidgetType.keys():
            self.dictListWidgetType[key].clear()
        
def main():
    app = QApplication(sys.argv)
    lock = QReadWriteLock()
    dc = DatasetContainer_GUI()
    datadict = np.load('C:\Users\ebalzani\Desktop\Data\\workspace_2017-7-4T14_56.phz')
#    datadict2 = np.load('C:\Users\ebalzani\Desktop\Data\Sleep\\workspace_2017-5-15T14_16.phz')
    print datadict.keys()
    th  = len(datadict.keys())//2
    i = 0
    for key in datadict.keys():
        tmp = datadict[key].all()
        if i  >= th:
            tmp.Types = ['Tipo B']
        dc.add(tmp)
        i += 1
    
    dialog = pairDataDlg({'Behavior': ['AM-Microsystems'],'Muzzum':['Tipo B']},dc,lock)
    dialog.show()
    app.exec_()
    print pd.DataFrame(dialog.pairMatrix)
    return dialog.pairMatrix
if __name__ == '__main__':
    pass
    pairedMatrix = main()
#    a=['aq21','rrrtew','chumbawamba']
#    b=['ciao','miao','awqa']
#    M = matrix_matching(a,b)
#    M[1,1] = 0.5
#    k = 0
#    isort_list = []
#    while k < M.shape[1]:
#        isort = np.where(M == np.max(M))
#        isort_list += [isort[1][0]]
#        M[isort] = -1
#        M[:,isort[1][0]] = -1
#        k+=1
#    print np.array(b)[isort_list]