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
libraries_fld = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
sys.path.append(libraries_fld)


from PyQt5.QtWidgets import (QDialog,QLabel,QPushButton,QHBoxLayout,QWidget,
                             QVBoxLayout,QScrollArea,QInputDialog)


class intLabelPairing_dlg(QDialog):
    def __init__(self,labelDict1,labelDict2,parent=None):
        super(intLabelPairing_dlg, self).__init__(parent)
        
        self.dict1 = labelDict1
        self.dict2 = labelDict2
        self.pairedLabel = None

        scroll = QScrollArea(self)
        lay = QVBoxLayout(self)
        lay.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        
        pairing = {}
        for gr in self.dict1.keys():
            pairing[gr] = {}
            pairing[gr]['Type I'] = self.dict1[gr]
            pairing[gr]['Type II'] = self.dict2[gr]
            
            string = QLabel("Gruop <b>%s</b> is paired:" %gr)
            scrollLayout.addWidget(string)
            
            for ll in range(len(self.dict1[gr])):
                
                string = QLabel("%s - %s" %(self.dict1[gr][ll],
                                            self.dict2[gr][ll]))
                scrollLayout.addWidget(string)
            
            string = QLabel("")
            scrollLayout.addWidget(string)
            string = QLabel("===========")
            scrollLayout.addWidget(string)
            string = QLabel("")
            scrollLayout.addWidget(string)
            
        self.pushButton_return = QPushButton("Return")
        self.pushButton_accept = QPushButton("Accept")
        
        hLayout_button = QHBoxLayout()
        hLayout_button.addWidget(self.pushButton_return)
        hLayout_button.addWidget(self.pushButton_accept)
        
        scrollLayout.addLayout(hLayout_button)
        scroll.setWidget(scrollContent)
        
        self.pushButton_accept.clicked.connect(self.addNameToLabel)
        self.pushButton_return.clicked.connect(self.closeTab)
        
    def closeTab(self):
        self.close()
        super(intLabelPairing_dlg, self).close()
        
    
    def addNameToLabel(self):
        options = ("Behavior","Sleep","Spikes")
        type1, okPressed = QInputDialog.getItem(self, "Choose data type","Type I:", options, 0, False)
        if okPressed and type1:
            type2, okPressed = QInputDialog.getItem(self, "Choose data type","Type II:", options, 0, False)
            if okPressed and type2:
                pairing = {}
                for gr in self.dict1.keys():
                    pairing[gr] = {}
                    pairing[gr][type1] = self.dict1[gr]
                    pairing[gr][type2] = self.dict2[gr]
                    
        
        self.pairedLabel = pairing
        self.close()
        super(intLabelPairing_dlg, self).close()
        
        