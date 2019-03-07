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
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtCore import pyqtSignal,QObject
from ui_behav_GUI import Ui_MainWindow
import os, sys

classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
phenopy_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'mainScripts')

sys.path.append(classes_dir)
sys.path.append(phenopy_dir)
        
class behav_gui_class(QMainWindow, Ui_MainWindow, QObject):
    sleepSig = pyqtSignal(str,name='behavSignal')
    def __init__(self,data,parent=None):
        super(behav_gui_class, self).__init__(parent)
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.closeTab)
        self.pushButton_run.clicked.connect(self.perforAct)

        
    def perforAct(self):
        print('sono qui')        
        pass
    
    def closeTab(self):
        self.close()
        self.closeBehav.emit('behav_gui_class')
        super(behav_gui_class, self).close()
      
def main():
    import sys
    app = QApplication(sys.argv)
    dlg = behav_gui_class()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()