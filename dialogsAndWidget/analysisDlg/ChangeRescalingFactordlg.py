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
from PyQt5.QtWidgets import (QApplication, QDialog)
from PyQt5.QtCore import (pyqtSlot,QPluginLoader,Qt)

import ui_Change_Rascale_Factor
MAC = 'qt_mac_set_native_menubar' in dir()
QPlugin = QPluginLoader("qico5.dll")

class ChangeRescalingFactordlg(QDialog,ui_Change_Rascale_Factor.Ui_TimeScaledlg):
    def __init__(self,scale,parent=None):
        super(ChangeRescalingFactordlg,self).__init__(parent)        
        self.setupUi(self)
        self.scaleLabel.setText(str(scale))
        self.pushButtonApply.setEnabled(False)
        if not MAC:
            self.pushButtonCancel.setFocusPolicy(Qt.NoFocus)
        
    @pyqtSlot()
    def on_pushButtonCancel_clicked(self):
        self.close()
    @pyqtSlot()
    def on_pushButtonApply_clicked(self):
        self.accept()
        
    @pyqtSlot(str)
    def on_lineEdit_textEdited(self):
        try:
            float(str(self.lineEdit.text()))
            self.pushButtonApply.setEnabled(True)
        except ValueError:
            self.lineEdit.clear()
            self.pushButtonApply.setEnabled(False)
        
            
        
if __name__== '__main__':
    import sys
    app = QApplication(sys.argv)
    form = ChangeRescalingFactordlg(1000)
    form.exec_()
#    form.show()
    
    
