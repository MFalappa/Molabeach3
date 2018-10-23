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
from ui_get_folder_and_format_dlg_export import Ui_Dialog_export
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

class get_export_info_dlg(QDialog,Ui_Dialog_export):
    def __init__(self, parent=None):
        super(get_export_info_dlg,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_ok.setEnabled(False)
        self.path_folder = os.path.dirname(__file__)
        self.ext = self.comboBox.currentText()
        self.delim = self.comboBox_2.currentText()
        self.connect(self.pushButton_browse,SIGNAL('clicked()'),self.browse)
        self.connect(self.pushButton_ok,SIGNAL('clicked()'), self.ok_click)
        self.connect(self.pushButton_Cancel,SIGNAL('clicked()'),self.reject)
        self.connect(self.lineEdit,SIGNAL('textChanged (const QString&)'),self.check_folder)
        self.connect(self.comboBox,SIGNAL('currentIndexChanged (const QString&)'),self.change_ext)
        
    def browse(self):
        folder = QFileDialog. getSaveFileName(self,'Select a file name...', self.path_folder,filter="Export (*%s)"%self.comboBox.currentText())
        if not folder.endswith(self.comboBox.currentText()):
            folder += self.comboBox.currentText()
        self.path_folder = folder
        self.lineEdit.setText(folder)
    
    def change_ext(self):
        ext = self.comboBox.currentText()
        file_name = self.lineEdit.text()
        delim_list = []
        print ext,file_name
        for row in xrange(self.comboBox.count()):
            delim_list += [self.comboBox.itemText(row)]
        if file_name and not file_name.endswith(ext):
            if file_name.split('.')[-1] in delim_list:
                file_name = '.'.join(file_name.split('.')[:-1]) + ext
            else:
                file_name += ext
            self.lineEdit.setText(file_name)
    
    def check_folder(self,file_name):
        if os.path.exists(os.path.dirname(file_name)):
            self.pushButton_ok.setEnabled(True)
        else:
            self.pushButton_ok.setEnabled(False)
    
    def ok_click(self):
        self.ext = self.comboBox.currentText()
        self.path_folder = self.lineEdit.text()
        if not self.path_folder.endswith(self.comboBox.currentText()):
            self.path_folder += self.comboBox.currentText()
        self.delim = self.comboBox_2.currentText()
        self.accept()

def main():
    import sys
    app = QApplication(sys.argv)
    form = get_export_info_dlg()
    print form.exec_()
#    res = app.exec_()
#    print res
if __name__ == '__main__':
    main()