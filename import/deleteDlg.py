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

import os,sys
file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
lib_dir = os.path.join(file_path,'libraries')
sys.path.append(lib_dir)
#from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QHBoxLayout,
                         QPushButton,QVBoxLayout, QSizePolicy,QSpacerItem)
                             
from PyQt5.QtGui import (QFont)

from MyDnDDialog import MyDnDListWidget

class deleteDlg(QDialog):
    def __init__(self, funcList, parent=None):
        super(deleteDlg,self).__init__(parent)
        self.keepFunc = MyDnDListWidget()
        self.keepFunc.addItems(funcList)
        self.deletefunc = MyDnDListWidget()
        self.continueButton = QPushButton('Continue')
        cancelButton = QPushButton('Cancel')
        font = QFont()
        font.setBold(True)
        font.setPixelSize(15)
        Label = QLabel('All Functions')
        Label_2 = QLabel('Function to Delete')
        Label.setFont(font)
        Label_2.setFont(font)
        Vlayout = QVBoxLayout()
        Vlayout.addWidget(Label)
        Vlayout.addWidget(self.keepFunc)
        Vlayout2 = QVBoxLayout()
        Vlayout2.addWidget(Label_2)
        Vlayout2.addWidget(self.deletefunc)
        HLayout = QHBoxLayout()
        HLayout.addLayout(Vlayout)
        HLayout.addLayout(Vlayout2)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, 
                                 QSizePolicy.Minimum)
        HLayout_2 = QHBoxLayout()
        HLayout_2.addSpacerItem(spacerItem)
        HLayout_2.addWidget(cancelButton)
        HLayout_2.addWidget(self.continueButton)
        layout = QVBoxLayout()
        layout.addLayout(HLayout)
        layout.addLayout(HLayout_2)
        self.setLayout(layout)
        
        self.continueButton.setEnabled(False)
        
        self.continueButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)
   
#        self.connect(self.deletefunc,pyqtSignal('dropped()'),self.enableOk)
#        self.connect(self.deletefunc,pyqtSignal('dragged()'),self.enableOk) 
#        self.connect(self.keepFunc,pyqtSignal('dropped()'),self.enableOk)
#        self.connect(self.keepFunc,pyqtSignal('dragged()'),self.enableOk)
        
    def enableOk(self):
        if self.deletefunc.count() > 0:
            self.continueButton.setEnabled(True)
        else:
            self.continueButton.setEnabled(False)
    def get_List(self):
        item = self.deletefunc.takeItem(0)
        listDel = []
        while item:
            listDel += [str(item.text())]
            item = self.deletefunc.takeItem(0)
        return listDel
            
        
    
if __name__=='__main__':
    app = QApplication(sys.argv)

    form = deleteDlg(['yo bru','ciao'])
    
    form.show()
    
    #print(form.exec_())
    app.exec_() 
    print( form.get_List())