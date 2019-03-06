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
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui_spike_gui import Ui_MainWindow
import os, sys

classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
phenopy_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'mainScripts')

sys.path.append(classes_dir)
sys.path.append(phenopy_dir)
        
class spk_gui(QMainWindow, Ui_MainWindow, QObject):
    spkSig = pyqtSignal(str,name='spkSignal')
    def __init__(self, parent=None):
        super(spk_gui, self).__init__(parent)
        self.setupUi(self)
        self.connect(self.pushButton_done,SIGNAL('clicked()'),self.close)
        self.connect(self.pushButton_save,SIGNAL('clicked()'),self.saveAct)
        
    def saveAct(self):
        print('sono qui')        
        pass
      
def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = spk_gui()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()