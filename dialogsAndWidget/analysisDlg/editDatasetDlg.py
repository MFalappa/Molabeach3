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
import sys,os
edit_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'edit')
libraries_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')

sys.path.append(edit_dir)
sys.path.append(libraries_dir)

from ui_editDlg import Ui_DialogEdit
from Modify_Dataset_GUI import DatasetContainer_GUI

from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.QtCore import Qt,pyqtSignal

from editLauncher import launchEditFun


class editDlg(QDialog,Ui_DialogEdit):
    errorImport = pyqtSignal(str,name='editErrorSignal')
    def __init__(self, parent=None):
        
        super(editDlg, self).__init__(parent)
        self.setupUi(self)
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
        
        self.descr_dict = {}
        self.show_dict = {}
        self.path_dict = {}
        self.populateCombo()
        self.textBrowser_descr.setText(self.descr_dict[str(self.comboBox.currentText())]) 
        
        self.comboBox.currentIndexChanged[str].connect(self.setDescription)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_Edit.clicked.connect(self.editFunction)
        
#        self.connect(self.comboBox,pyqtSignal('currentIndexChanged (const QString&)'),self.setDescription)

    
    def editFunction(self):
        showed_name = self.comboBox.currentText()
        launchEditFun(self.parent, self.show_dict[showed_name])
        
    def setDescription(self,funName):
        self.textBrowser_descr.setText(self.descr_dict[funName])
        
    def populateCombo(self):
        edit_fld = os.path.abspath(os.path.join(os.path.realpath(__file__),'../../..'))
        fh = open(os.path.join(edit_fld,'edit','editFunctions.py'),'U')
        line = fh.readline()
        while line:
            if line.startswith(('def ','def\t')):
                funName = (line[3:].replace(' ','')).replace('\t','')
                funName = funName.split('(')[0]
                if funName == 'main' or funName == 'create_laucher':
                    line = fh.readline()
                    continue
#                self.comboBox.addItem(funName)
                line = fh.readline()
                if '\"\"\"' in line:
                    descr_str = line.split('\"\"\"')[1]
                    line = fh.readline()
                    while not '\"\"\"' in line:
                        descr_str += line
                        line = fh.readline()
                    descr_str += line.split('\"\"\"')[0]
                    descr_str = descr_str.replace('\n',' ')
                    self.descr_dict[descr_str.split('==')[1]] = descr_str.split('==')[0]
                    
                    self.show_dict[descr_str.split('==')[1]] = funName
                    self.comboBox.addItem(descr_str.split('==')[1])
                    
                    
#                else:
#                    self.descr_dict[funName] = ''
            line = fh.readline()
        fh.close()

def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = editDlg()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()
    