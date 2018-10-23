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

import ui_Wizard_2
from PyQt4.QtCore import (pyqtSignature,SIGNAL)
from PyQt4.QtGui import (QApplication, QDialog)
import sys

class Wizard_2(QDialog, ui_Wizard_2.Ui_Dialog):
    def __init__(self,parent=None):
        super(Wizard_2, self).__init__(parent)
        self.setupUi(self)
        self.analysisType = 'Single'
        self.radioButton.setChecked(True)
        self.connect(self.pushButtonCancel,SIGNAL('clicked()'),self.reject)
        self.connect(self.pushButtonContinue,SIGNAL('clicked()'),self.accept)
    @pyqtSignature('void')
    def on_radioButton_clicked(self):
        self.analysisType = 'Single'
    @pyqtSignature('void')
    def on_radioButton_2_clicked(self):
        self.analysisType = 'Group'
        
if __name__=='__main__':
    app = QApplication(sys.argv)

    form = Wizard_2()
    
    form.show()
    
    #print(form.exec_())
    app.exec_() 