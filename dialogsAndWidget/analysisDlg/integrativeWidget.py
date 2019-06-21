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
sys.path.append(libraries_fld)


from PyQt5.QtWidgets import (QDialog,QLabel,QComboBox,QTextBrowser,QPushButton,
                             QHBoxLayout,QVBoxLayout,QSpacerItem,
                             QSizePolicy,QApplication)

from PyQt5.QtCore import (pyqtSignal,Qt)

from Modify_Dataset_GUI import DatasetContainer_GUI
from changeLabelshow import info_label
from tableGrouping import TableWidget
from integrativeLabelPairing import intLabelPairing_dlg
#from importDataset import *
#from importLauncher import launchLoadingFun


class integrativeDlg(QDialog):
    closeSig = pyqtSignal(str,name='closeSig')
    runAnalysisSig = pyqtSignal(dict, name='integrative')
    def __init__(self,data,analysisDict,parent=None):
        super(integrativeDlg, self).__init__(parent)
        
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
            
        label = QLabel('<b>Data to analyze (Type I):</b>')
        self.tableWidget1 = TableWidget(0, 0,'input_table', self)
        
        label4 = QLabel('<b>Data to analyze (Type II):</b>')
        self.tableWidget2 = TableWidget(0, 0,'input_table', self)

        label1 = QLabel('<b>Choose analysis function:</b>')
        self.comboBox = QComboBox()
        
        label2 = QLabel('<b>Analysis description:</b>')
        self.textBrowser_descr = QTextBrowser()
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.pushButton_cancel = QPushButton("Close")
        self.pushButton_run = QPushButton("Run")

        vLayout_l = QVBoxLayout()
        vLayout_l.addWidget(label)
        vLayout_l.addWidget(self.tableWidget1)
        vLayout_l.addWidget(label4)
        vLayout_l.addWidget(self.tableWidget2)
        
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
        self.path_dict = {}
        self.populateCombo()
        self.textBrowser_descr.setText(self.descr_dict[str(self.comboBox.currentText())]) 
        self.comboBox.currentIndexChanged[str].connect(self.showDescription)
        
        self.pushButton_run.setEnabled(False)
        self.pushButton_run.clicked.connect(self.runAnalysis)
        self.pushButton_cancel.clicked.connect(self.closeTab)
        
        self.tableWidget1.element_in.connect(self.checkfile)
        self.tableWidget2.element_in.connect(self.checkfile)
    
    def checkfile(self):
        if bool(self.tableWidget1.dict_elemenet) and  bool(self.tableWidget2.dict_elemenet):
            for gr in self.tableWidget1.dict_elemenet.keys():
                if gr in self.tableWidget2.dict_elemenet:
                    if len(self.tableWidget2.dict_elemenet[gr]) == len(self.tableWidget1.dict_elemenet[gr]):
                         self.pushButton_run.setEnabled(True)
                    else:
                        self.pushButton_run.setEnabled(False)
                        break
                else:
                    self.pushButton_run.setEnabled(False)
                    break
        else:
            self.pushButton_run.setEnabled(False)
            
            
    def runAnalysis(self):
        selectedAnalysis = self.comboBox.currentText()
        for typeOfAnalysis in list(self.analysisDict.keys()):
            if selectedAnalysis in list(self.analysisDict[typeOfAnalysis].keys()):
                acceptedTypes = self.analysisDict[typeOfAnalysis][selectedAnalysis]
                break
            
            
        dlg = intLabelPairing_dlg(self.tableWidget1.dict_elemenet,self.tableWidget2.dict_elemenet,parent=self)
        dlg.exec_()

        if bool(dlg.pairedLabel):
            dictSelection = {'anType': typeOfAnalysis,
                             'dataType': acceptedTypes, 
                             'analysisName': selectedAnalysis,
                             'Groups' : self.tableWidget1.dict_elemenet,
                             'Pairing' : dlg.pairedLabel}
            
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
                                
                label, description, type_func = info_label(funName)
                if type_func == 'Integrative':
                    self.comboBox.addItem(label)
                    self.descr_dict[label] = description
                
                line = fh.readline()
            else:
                line = fh.readline()
                
        fh.close()

    def closeTab(self):
        self.close()
        self.closeSig.emit('closeSig')
        super(integrativeDlg, self).close()
        
def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = integrativeDlg()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()
    