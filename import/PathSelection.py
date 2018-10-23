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
from PyQt4.QtCore import (pyqtSignature)
from PyQt4.QtGui import (QApplication, QDialog,QFileDialog)

class PathSelection(QDialog, ui_PathSelection.Ui_Dialog):
    def __init__(self,parent=None):
        super(PathSelection, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.setEnabled(False)

    @pyqtSignature('void')
    def on_pushButtonFolder_clicked(self):
        path = QFileDialog.getExistingDirectory(self, 
                                           u"Select Autonomice Folder",
                                           ".")
        self.lineEdit_2.setText(path)
        
    @pyqtSignature('void')
    def on_pushButtonFunction_clicked(self):
        path = QFileDialog.getOpenFileName(self, 
                                           u"Select a Python File",
                                           ".", u"Python files (*.py *.pyw)")
        self.lineEdit.setText(path)
    
    @pyqtSignature('void')
    def on_pushButtonFunction_2_clicked(self):
        path = QFileDialog.getOpenFileName(self, 
                                           u"Select a Python File",
                                           ".", u"Python files (*.py *.pyw)")
        self.lineEdit_3.setText(path)
        
    @pyqtSignature('const QString&')
    def on_lineEdit_textChanged(self,path):
        self.enableCreate()
        
    @pyqtSignature('const QString&')
    def on_lineEdit_2_textChanged(self,path):
        self.enableCreate()
        
    @pyqtSignature('const QString&')
    def on_lineEdit_3_textChanged(self,path):
        self.enableCreate()
        
    @pyqtSignature('void')
    def on_pushButton_clicked(self):
        self.function     = unicode(self.lineEdit.text())
        self.directory    = unicode(self.lineEdit_2.text())
        self.functionPlot = unicode(self.lineEdit_3.text())
        self.accept()
    
    @pyqtSignature('void')
    def on_pushButton_2_clicked(self):
        self.reject()
        
    def enableCreate(self):
        if os.path.exists(unicode(self.lineEdit.text()))\
           and\
           os.path.exists(unicode(self.lineEdit_2.text()))\
           and\
           os.path.exists(unicode(self.lineEdit_3.text())):
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

if __name__=='__main__':
    app = QApplication(sys.argv)

    form = PathSelection()
    
    form.show()
    
    #print(form.exec_())
    app.exec_() 