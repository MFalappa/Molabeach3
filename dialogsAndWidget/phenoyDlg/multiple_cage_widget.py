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

from cage_widget import * 
from PyQt4.QtCore import *
from PyQt4.QtGui import * 
import sys
import numpy as np

class multi_cageWidget(QWidget):
    def __init__(self,cage_widget_dict,parent=None):
        super(multi_cageWidget,self).__init__(parent)
        gird_layout = QGridLayout()
        i = 0
        for key in np.sort(cage_widget_dict.keys()):
            gird_layout.addWidget(cage_widget_dict[key],i//2+1,i%2+1)
            i+=1
        self.setLayout(gird_layout)
        
class testdlg_1(QDialog):
    def __init__(self, parent=None):
        super(testdlg_1,self).__init__(parent)
        cage_d = {}
        for k in range(5):
            cage_d[k] = cage_widget(cage_id=k)
            print 'ciao'
        m_cage = multi_cageWidget(cage_d)
        layout = QHBoxLayout()
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = m_cage
#        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 380, 247))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        
def main():
    app = QApplication(sys.argv)
    form = testdlg_1()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()