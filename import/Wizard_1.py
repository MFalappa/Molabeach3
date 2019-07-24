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

import ui_Wizard_1
import sys,os
from PyQt5.QtCore import (pyqtSlot)
from PyQt5.QtWidgets import (QApplication,QDialog, QFileDialog)

class Wizard_1(QDialog, ui_Wizard_1.Ui_newAnalysis):
    def __init__(self,parent=None):
        super(Wizard_1, self).__init__(parent)
        self.setupUi(self)
        
        self.radioButton.setChecked(True)
        self.pushButton.setEnabled(False)
        self.lineEdit_analysis.textChanged[str].connect(self.checkContinue)
        self.lineEdit_plotting.textChanged[str].connect(self.checkContinue)
        self.radioButton.setChecked(True)
        self.analysisType = 'Behaviour'
       
#   if continue is clicked return true else return false
    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.accept()
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.reject()
    @pyqtSlot()
    def on_pushButton_analysis_clicked(self):
        path,_ = QFileDialog.getOpenFileName (parent = self, caption = 'Select Analysis Script', directory = '.', filter="Python script (*.py)")
        self.lineEdit_analysis.setText(path)
    
    @pyqtSlot()
    def on_pushButton_plotting_clicked(self):
        path,_ = QFileDialog.getOpenFileName (parent = self, caption = 'Select Plotting Script', directory = '.', filter="Python script (*.py)")
        self.lineEdit_plotting.setText(path)
    
#   if radiobutton are clicked set analysis type to the following
    @pyqtSlot()
    def on_radioButton_clicked(self):
        self.analysisType = 'Behaviour'
    @pyqtSlot()
    def on_radioButton_1_clicked(self):
        self.analysisType = 'Sleep'
    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        self.analysisType = 'Spike'
    @pyqtSlot()
    def on_radioButton_3_clicked(self):
        self.analysisType = 'Integrative'
    
    
#   continue checking    
    def checkContinue(self):
        path_plt = self.lineEdit_plotting.text()
        path_an = self.lineEdit_analysis.text()
        if os.path.exists(path_an) and \
           os.path.exists(path_plt) and \
           path_an.endswith('.py') and \
           path_plt.endswith('.py'):
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
def main():
    app = QApplication(sys.argv)

    form = Wizard_1()
    form.show()
    
    #print(form.exec_())
    app.exec_() 
    print(form.analysisType)            
if __name__=='__main__':
    main()
    