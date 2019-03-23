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
                             QHBoxLayout,QVBoxLayout,QTableWidget,QSpacerItem,
                             QSizePolicy,QApplication)

from PyQt5.QtCore import (pyqtSignal,Qt)

from Modify_Dataset_GUI import DatasetContainer_GUI
#from importDataset import *
#from importLauncher import launchLoadingFun


class behavDlg(QDialog):
    closeSig = pyqtSignal(str,name='chooseAnalysiSig')
    startAnalysisSignal = pyqtSignal(dict, name='beahviorAnalysis')
#    def __init__(self,data,analysisDict,parent=None):
    def __init__(self,parent=None):
        super(behavDlg, self).__init__(parent)
#        self.analysisDict = analysisDict
        
        
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
        self.tableWidget = QTableWidget()

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
        self.path_dict = {}
        self.populateCombo()
        self.textBrowser_descr.setText(self.descr_dict[str(self.comboBox.currentText())]) 
        self.comboBox.currentIndexChanged[str].connect(self.showDescription)
        
        self.pushButton_run.setEnabled(False)
        self.pushButton_run.clicked.connect(self.runAnalysis)
        self.pushButton_cancel.clicked.connect(self.closeTab)

    
    def checkfile(self):
        print('qui ci va la tabella')
        self.pushButton_run.setEnabled(True)

    def runAnalysis(self):
        selectedAnalysis = self.comboBox.currentText()
        for typeOfAnalysis in list(self.analysisDict.keys()):
            if selectedAnalysis in list(self.analysisDict[typeOfAnalysis].keys()):
                acceptedTypes = self.analysisDict[typeOfAnalysis][selectedAnalysis]
                break
        dictSelection = {'anType': typeOfAnalysis, 'dataType': acceptedTypes, 'analysisName': selectedAnalysis}
        self.startAnalysisSignal.emit(dictSelection)

    def showDescription(self,funName):
        self.textBrowser_descr.setText(self.descr_dict[funName])
        
    def populateCombo(self):
        fh = open(os.path.join(libraries_fld,'Analyzing_GUI.py'))
        line = fh.readline()

        while line:
            if line.startswith(('def ','def\t')):
                funName = (line[3:].replace(' ','')).replace('\t','')
                funName = funName.split('(')[0]
                if funName == 'main' or funName == 'create_laucher':
                    line = fh.readline()
                    continue
                self.comboBox.addItem(funName)
                line = fh.readline()
                if '\"\"\"' in line:
                    descr_str = line.split('\"\"\"')[1]
                    line = fh.readline()
                    while not '\"\"\"' in line:
                        descr_str += line
                        line = fh.readline()
                    descr_str += line.split('\"\"\"')[0]
                    descr_str = descr_str.replace('\n',' ')
                    self.descr_dict[funName] = descr_str
                else:
                    self.descr_dict[funName] = ''
            line = fh.readline()
        fh.close()

    def closeTab(self):
        self.close()
        self.closeSig.emit('chooseAnalysiSig')
        super(behavDlg, self).close()
        
def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = behavDlg()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()
    