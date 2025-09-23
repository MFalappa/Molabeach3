
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


from PyQt5.QtWidgets import (QDialog,QFileDialog,QApplication,QListWidgetItem)
from PyQt5.QtCore import (pyqtSignal,Qt)
from PyQt5.QtGui import QIcon

from Modify_Dataset_GUI import DatasetContainer_GUI
from ui_sleep_gui import Ui_Dialog
#from importDataset import *
#from importLauncher import launchLoadingFun


class sleepDlg(QDialog,Ui_Dialog):
    closeSig = pyqtSignal(str,name='chooseAnalysiSig')
    errorChoose = pyqtSignal(str,name='analysisErrorSignal')
    def __init__(self,data,analysisDict,parent=None):
#    def __init__(self,parent=None):
        super(sleepDlg, self).__init__(parent)
        self.setupUi(self)
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
        
        

        
        self.pushButton_run.setEnabled(False)
        self.pushButton_run.clicked.connect(self.runAnalysis)
        self.pushButton_cancel.clicked.connect(self.closeTab)
        
        self.checkBox_save_excel.clicked.connect(self.closeTab)
        self.checkBox_show_results.clicked.connect(self.closeTab)
#        self.checkBox.clicked.connect(self.closeTab) sono le opzioni che dovebbero comparire 
        #alla selezione dell'analisi specifica

        

       
    def checkfile(self):
        print('qui ci va la tabella')
        self.pushButton_run.setEnabled(True)
    
    def runAnalysis(self):
        print('qui faccio partire le analisi')
        print('se ho capito bene guarda cosa c è nella tabella')
        print('guarda l analisi selezionata e i parametri (es sleep, rem wake.)')
        print('e manda tutto a phenopy che lancia effettivamente l analisi')
                     
    def showDescription(self,funName):
        self.textBrowser_descr.setText(self.descr_dict[funName])
        
    def populateCombo(self):
        fh = open(os.path.join(libraries_fld,'Analyzing_GUI.py'))
        line = fh.readline()

        while line:
            if line.startswith(('def ','def\t')):
                print('here sholde be placed the check for the analysis..if sleep continue')
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
        super(sleepDlg, self).close()
        
def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = sleepDlg()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()
    