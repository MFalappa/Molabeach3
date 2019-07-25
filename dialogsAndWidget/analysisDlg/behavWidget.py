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
libraries_fld = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
classes_fld = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes')

sys.path.append(libraries_fld)
sys.path.append(os.path.join(classes_fld,'analysisClasses'))


from PyQt5.QtWidgets import (QDialog,QLabel,QComboBox,QTextBrowser,QPushButton,
                             QHBoxLayout,QVBoxLayout,QSpacerItem,
                             QSizePolicy,QApplication)

from PyQt5.QtCore import (pyqtSignal,Qt)

from Modify_Dataset_GUI import DatasetContainer_GUI
from tableGrouping import TableWidget
#from importDataset import *
#from importLauncher import launchLoadingFun


class behavDlg(QDialog):
    closeSig = pyqtSignal(str,name='closeSig')
    runAnalysisSig = pyqtSignal(dict, name='beahvior')
#    def __init__(self,parent=None):
    def __init__(self,data,analysisDict,parent=None):        
        super(behavDlg, self).__init__(parent)
        self.analysisDict = analysisDict
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        if parent:
            try:
                self.parent = parent
                self.parent.lock.lockForRead()
                self.data_container = parent.Dataset
            finally:
                self.parent.lock.unlock()
        else:
            self.parent = parent
            self.data_container = DatasetContainer_GUI()
            
        label = QLabel('<b>Behaviour data to analyze:</b>')
        self.tableWidget = TableWidget(0, 0,'input_table', self)
#        self.tableWidget = QTableWidget()

        label1 = QLabel('<b>Choose analysis function:</b>')
        self.comboBox = QComboBox()
        
        label2 = QLabel('<b>Analysis description:</b>')
        self.textBrowser_descr = QTextBrowser()
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.pushButton_cancel = QPushButton("Close")
        self.pushButton_run = QPushButton("Run")

        vLayout_l = QVBoxLayout()
        vLayout_l.addWidget(label)
        vLayout_l.addWidget(self.tableWidget)
        
        vLayout = QVBoxLayout()
        vLayout.addWidget(label1)
        vLayout.addWidget(self.comboBox)
        vLayout.addWidget(label2)
        vLayout.addWidget(self.textBrowser_descr)
        
        hLayout_b = QHBoxLayout()
        hLayout_b.addSpacerItem(spacerItem)
        hLayout_b.addWidget(self.pushButton_cancel)
        hLayout_b.addWidget(self.pushButton_run)
        
        vLayout_r = QVBoxLayout()
        vLayout_r.addLayout(vLayout)
        vLayout_r.addLayout(hLayout_b)
        
        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout_l)
        hLayout.addLayout(vLayout_r)
        
        self.setLayout(hLayout)
        
        self.descr_dict = {}
        self.show_dict = {} 
        self.path_dict = {}
        self.populateCombo()
        self.textBrowser_descr.setText(self.descr_dict[str(self.comboBox.currentText())]) 
        self.comboBox.currentIndexChanged[str].connect(self.showDescription)
        
        self.pushButton_run.setEnabled(False)
        self.pushButton_run.clicked.connect(self.runAnalysis)
        self.pushButton_cancel.clicked.connect(self.closeTab)
        self.tableWidget.element_in.connect(self.checkfile)

    
    def checkfile(self):
        if bool(self.tableWidget.dict_elemenet):
            self.pushButton_run.setEnabled(True)
        else:
            self.pushButton_run.setEnabled(False)

    def runAnalysis(self):
        showed_name = self.comboBox.currentText()
        selectedAnalysis = self.show_dict[showed_name]
        
        for typeOfAnalysis in list(self.analysisDict.keys()):
            if selectedAnalysis in list(self.analysisDict.keys()):
                acceptedTypes = self.analysisDict[typeOfAnalysis]['accepted_type']
                break
            
        dictSelection = {'anType': typeOfAnalysis, 
                         'dataType': acceptedTypes, 
                         'analysisName': selectedAnalysis, 
                         'Groups' : self.tableWidget.dict_elemenet,
                         'Pairing' : None }
        
        self.runAnalysisSig.emit(dictSelection)

    def showDescription(self,funName):
        self.textBrowser_descr.setText(self.descr_dict[funName])
        
    def populateCombo(self):
        fh = open(os.path.join(libraries_fld,'analysis_functions.py'))

        line = fh.readline()

        while line:
            if line.startswith(('def ','def\t')):
                funName = (line[3:].replace(' ','')).replace('\t','')
                funName = funName.split('(')[0]
                
                if funName == 'main' or funName == 'create_laucher':
                    line = fh.readline()
                    continue
                                
                label = self.analysisDict[funName]['label']
                description = self.analysisDict[funName]['description']
                type_func = self.analysisDict[funName]['type_func']
                
                if type_func == 'Behaviour':
                    self.comboBox.addItem(label)
                    self.descr_dict[label] = description
                    self.show_dict[label] = funName
                
                line = fh.readline()
            else:
                line = fh.readline()

        fh.close()

    def closeTab(self):
        self.close()
        self.closeSig.emit('closeSig')
        super(behavDlg, self).close()
        
        
#            Row = self.analysisList.currentRow()
#        if Row !=-1:
#            self.selectedAnalysis = self.analysisList.item(Row).text()
#            for dtype in self.dict_type.keys():
#                if self.dict_type[dtype].has_key(self.selectedAnalysis):
#                    break
#            self.selectedDataTypes = self.dict_type[dtype][self.selectedAnalysis]
#            self.selectedType = dtype
#        QDialog.accept(self)

def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = behavDlg()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()
    