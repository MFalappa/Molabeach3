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


import ui_pellet_widget
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from messageLib import *

class pellet_widget(QWidget, ui_pellet_widget.Ui_pellet_widget):
    def __init__(self, side='Left', pellet_num=0, MODE=0, parent=None):
        super(pellet_widget, self).__init__(parent)
        
        self.setupUi(self)
        self.abort_num = 0
        
#        self.layout.addWidget(self.label_not_released)
        self.groupBox_pellet.setFixedSize(150, 130)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                       QSizePolicy.MinimumExpanding))
        self.MODE = MODE
        self.groupBox_pellet.setStyleSheet("QGroupBox { background-color: rgb(255, 255,\
            255); border:1px solid rgb(83, 84, 84); }")
        if side == 'Left':
            self.pellet_rel_msg = 34
            self.lateral = True
            self.groupBox_pellet.setTitle('Food Left')
        elif side == 'Right':
            self.pellet_rel_msg = 35
            self.lateral = True
            self.groupBox_pellet.setTitle('Food Right')
        else:
            self.lateral = False
            self.pellet_rel_msg = 51 # uso 24 (center light on) al posto di 15 (ACT_TRIAL)
            self.groupBox_pellet.setTitle('Trial Info')
            label_not_released = QLabel('Abort Release:')
#            label_not_released.setFixedHeight(50)
#            label_not_released.setFixedWidth(100)
            self.abort_label = QLabel('0')
            self.label_2.setText('Trials num:')
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            font.setPointSize(8)
            label_not_released.setFont(font)
            hlayout = QHBoxLayout()
            hlayout.addWidget(label_not_released)
            hlayout.addWidget(self.abort_label)
            self.verticalLayout_3.addLayout(hlayout)
        self.pellet_num = pellet_num
        self.label_pelletnum.setText('%d'%self.pellet_num)
        print self.groupBox_pellet.size()
#        self.label_pelletnum.setFixedHeight(50)
#        self.label_pelletnum.setFixedWidth(100)

    def update_labels(self, msg):
        if msg.data[6] == self.pellet_rel_msg:
            self.pellet_num += 1
            self.label_pelletnum.setText('%d'%self.pellet_num)

        elif msg.data[6] == 48 and not self.lateral:
            self.abort_num += 1
            self.abort_label.setText('<font color=\'red\'>%d</font>'%self.abort_num)
        
        else:
            return None
            
    def update_labels_Xbee(self, msg):
        try:
            PAYLOAD = binascii.hexlify(msg['rf_data'])
            action = int(PAYLOAD[20:24], 16)
            if action == self.pellet_rel_msg:
                self.pellet_num += 1
                self.label_pelletnum.setText('%d'%self.pellet_num)
            elif action == 48:
                self.abort_num += 1
                self.abort_label.setText('<font color=\'red\'>%d</font>'%self.abort_num)
        except KeyError:
            return
    
    def clear(self):
        self.abort_num = 0
        self.pellet_num = 0
        self.label_pelletnum.setText('%d'%self.pellet_num)
        if not self.lateral:
            self.abort_label.setText('<font color=\'red\'>%d</font>'%self.abort_num)
        
def main():
    app = QApplication(sys.argv)
#    form = hopper_widget()
    form = pellet_widget(side='Center')
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()
#main()