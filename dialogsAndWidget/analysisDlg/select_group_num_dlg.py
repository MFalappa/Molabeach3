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

from ui_select_group_num_dlg import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

MAC = "qt_mac_set_native_menubar" in dir()
class select_group_num(QDialog,Ui_Dialog):
    def __init__(self, parent=None):
        super(select_group_num,self).__init__(parent)
        self.setupUi(self)
        self.spinBox.setValue(2)
        if not MAC:
            self.pushButton_ok.setFocus(True)
    
    @pyqtSignature('void')
    def on_pushButton_ok_clicked(self):
        self.accept()
    
    @pyqtSignature('void')
    def on_pushButton_cancel_clicked(self):
        self.reject()

def main():
    import sys
    app = QApplication(sys.argv)
    form = select_group_num()
    form.show()
    app.exec_()
if __name__=='__main__':
    main()