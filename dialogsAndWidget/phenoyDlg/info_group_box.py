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
from PyQt5.QtWidgets import (QWidget,QGroupBox,QSpacerItem,QVBoxLayout,
                             QHBoxLayout,QSizePolicy,QLabel,QApplication)
from PyQt5.QtGui import (QPixmap,QImage,QFont)
from PyQt5.QtCore import QSize
import sys
import os
figDir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'images')



class info_group_box(QWidget):
    def __init__(self, title, Id_cage=None, parent=None):
        super(info_group_box, self).__init__(parent)
        self.groupBox_info = QGroupBox(title)
        self.groupBox_info.setFixedSize(400, 130)
        figRec = os.path.abspath(os.path.join(figDir,'recIcon.png'))
        figPause = os.path.abspath(os.path.join(figDir,'pauseIcon.png'))

        self.iconRec = QPixmap.fromImage(QImage(figRec))
        self.iconPause = QPixmap.fromImage(QImage(figPause))
        self.iconRec = self.iconRec.scaled(QSize(60,60))
        self.iconPause = self.iconPause.scaled(QSize(60,60))
        
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.groupBox_info = QGroupBox('Experiment Info')
        self.groupBox_info.setFont(font)
        self.groupBox_info.setStyleSheet("QGroupBox { background-color: rgb(255, 255,\
            255); border:1px solid rgb(83, 84, 84); }")
        
        self.verticalLayout = QVBoxLayout()
        hLayout = QHBoxLayout(self.groupBox_info)
        layout = QHBoxLayout()

        
        self.label_1 = QLabel('')
        self.verticalLayout.addWidget(self.label_1)
        if Id_cage:
            self.label_2 = QLabel('Cage ID:')
            self.verticalLayout.addWidget(self.label_2)
        else:
            self.label_2 = QLabel('')
            self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QLabel('Status:', self.groupBox_info)
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QLabel('Bactery level:')
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QLabel('Directory to save:')
        self.verticalLayout.addWidget(self.label_5)
        
        l2 = QVBoxLayout()
        labelv4 = QLabel('')
        l2.addWidget(labelv4)
        labelv1 = QLabel('<b>%s</b>'%Id_cage)  
        l2.addWidget(labelv1)
        self.labelStatus = QLabel('Pause') 
        l2.addWidget(self.labelStatus)
        self.labelDir = QLabel('') 
        l2.addWidget(self.labelDir)
        self.bacterylevel = QLabel('') 
        l2.addWidget(self.bacterylevel)
        
        l3 = QVBoxLayout()
        l4 = QVBoxLayout()
        l3.addSpacerItem(spacerItem)
        self.labelRec = QLabel('')
        self.labelRec.setPixmap(self.iconPause)
        l4.addWidget(self.labelRec)
        
        hLayout.addLayout(self.verticalLayout)
        hLayout.addLayout(l2)
        hLayout.addLayout(l3)
        hLayout.addLayout(l4)
        layout.addWidget(self.groupBox_info)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    dialog = info_group_box('Program Info',127)
    dialog.show()
    app.exec_()
if __name__ == '__main__':
    main()