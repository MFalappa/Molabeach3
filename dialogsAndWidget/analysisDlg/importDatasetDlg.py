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
import_fld = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'import')
libraries_fld = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')

sys.path.append(import_fld)
sys.path.append(libraries_fld)


from PyQt5.QtWidgets import (QDialog,QFileDialog,QApplication,QListWidgetItem)
from PyQt5.QtCore import (pyqtSignal,Qt)
from PyQt5.QtGui import QIcon

from Modify_Dataset_GUI import DatasetContainer_GUI
from ui_importDlg import Ui_Dialog
#from importDataset import *
from importLauncher import launchLoadingFun


class importDlg(QDialog,Ui_Dialog):
    errorImport = pyqtSignal(str,name='importErrorSignal')
    def __init__(self, parent=None):
        
        super(importDlg, self).__init__(parent)
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
        self.setupUi(self)
        self.descr_dict = {}
        self.path_dict = {}
        self.populateCombo()
        self.textBrowser_descr.setText(self.descr_dict[str(self.comboBox.currentText())]) 
        
        self.comboBox.currentIndexChanged[str].connect(self.setDescription)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.getFiles)
        self.pushButton_load.clicked.connect(self.loadData)
        
#        self.connect(self.comboBox,pyqtSignal('currentIndexChanged (const QString&)'),self.setDescription)
#        self.connect(self.pushButton_cancel,pyqtSignal('clicked()'),self.close)
#        self.connect(self.pushButton,pyqtSignal('clicked()'),self.getFiles)
#        self.connect(self.pushButton_load,pyqtSignal('clicked()'),self.loadData)
        
        self.pushButton_load.setEnabled(False)
        
    def getFiles(self):
        print('questo non funzion')
        dire = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"../..")))
        Qfnames,_ = QFileDialog.getOpenFileNames(self,
                    "Phenopy - Load Dataset", dire)
        self.listWidget.clear()
        self.pushButton_load.setEnabled(False)
        for name in Qfnames:
            item = QListWidgetItem()
            self.path_dict[os.path.basename(name)] = name
            item.setText(os.path.basename(name))
            item.setIcon(QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)),"images","table.png")))
            self.listWidget.addItem(item)
            self.pushButton_load.setEnabled(True)
    
    def loadData(self):
        items = [self.listWidget.item(i) for i in range(self.listWidget.count())]
        for item in items:
            path = self.path_dict[item.text()]
            try:
                imported = launchLoadingFun(path,self.comboBox.currentText())
            except IndexError as e:
                print(e)
                self.errorImport.emit('Import of %s failed. %s'%(item.text(),e))
                continue
            if self.parent:
                try:
                    self.parent.lock.lockForWrite()
                    self.data_container.add(imported)
                finally:
                    self.parent.lock.unlock()
                    
            else:
                self.data_container.add(imported)
                
                     
    def setDescription(self,funName):
        self.textBrowser_descr.setText(self.descr_dict[funName])
        
    def populateCombo(self):
        fh = open(os.path.join(import_fld,'importDataset.py'))
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

def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = importDlg()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()
    