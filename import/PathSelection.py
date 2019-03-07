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

import ui_PathSelection
import sys
import os
from PyQt5.QtCore import (pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QDialog,QFileDialog)

class PathSelection(QDialog, ui_PathSelection.Ui_Dialog):
    def __init__(self,parent=None):
        super(PathSelection, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.setEnabled(False)

    @pyqtSlot()
    def on_pushButtonFolder_clicked(self):
        path = QFileDialog.getExistingDirectory(self, 
                                           "Select Phenopy Folder",
                                           ".")
        self.lineEdit_2.setText(path)
        
    @pyqtSlot()
    def on_pushButtonFunction_clicked(self):
        path,_ = QFileDialog.getOpenFileName(self, 
                                           "Select a Python File",
                                           ".", "Python files (*.py *.pyw)")
        self.lineEdit.setText(path)
    
    @pyqtSlot()
    def on_pushButtonFunction_2_clicked(self):
        path,_ = QFileDialog.getOpenFileName(self, 
                                           "Select a Python File",
                                           ".", "Python files (*.py *.pyw)")
        self.lineEdit_3.setText(path)
        
    @pyqtSlot(str)
    def on_lineEdit_textChanged(self,path):
        self.enableCreate()
        
    @pyqtSlot(str)
    def on_lineEdit_2_textChanged(self,path):
        self.enableCreate()
        
    @pyqtSlot(str)
    def on_lineEdit_3_textChanged(self,path):
        self.enableCreate()
        
    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.function     = str(self.lineEdit.text())
        self.directory    = str(self.lineEdit_2.text())
        self.functionPlot = str(self.lineEdit_3.text())
        self.accept()
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.reject()
        
    def enableCreate(self):
        if os.path.exists(str(self.lineEdit.text()))\
           and\
           os.path.exists(str(self.lineEdit_2.text()))\
           and\
           os.path.exists(str(self.lineEdit_3.text())):
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

if __name__=='__main__':
    app = QApplication(sys.argv)

    form = PathSelection()
    
    form.show()
    
    #print(form.exec_())
    app.exec_() 