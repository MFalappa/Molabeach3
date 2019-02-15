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
import sys
from PyQt5.QtWidgets import (QWidget,QGridLayout,QGroupBox,
                             QHBoxLayout,QApplication,QLayout)
from PyQt5.QtGui import QFont
from hopper_Widget import hopper_widget
from pellet_widget import pellet_widget
from info_group_box import info_group_box
import datetime
import binascii

class cage_widget(QWidget):
    def __init__(self, MODE=0, cage_id=None, parent=None, path2save = '.'):
        super(cage_widget, self).__init__(parent)
        layout = QGridLayout()
        self.path2save = path2save
        self.isRec = False
        self.group_box = QGroupBox('Mouse %d'%cage_id)
        self.group_box.setStyleSheet("QGroupBox { border:2px solid rgb(83, 84, 84); }")
        self.left_hopper = hopper_widget('Left',parent=self.group_box)
        self.left_hopper.groupBox_hopper.setTitle('Left Hopper')
        self.center_hopper = hopper_widget('Center',parent=self.group_box)
        self.center_hopper.groupBox_hopper.setTitle('Center Hopper')
        self.right_hopper = hopper_widget('Right',parent=self.group_box)
        self.right_hopper.groupBox_hopper.setTitle('Right Hopper')
        self.left_pellet = pellet_widget(side='Left',parent=self.group_box)
        self.right_pellet = pellet_widget(side='Right',parent=self.group_box)
        self.center_pellet = pellet_widget(side='Center',parent=self.group_box)
        self.prog_info = info_group_box('Info',Id_cage=cage_id,parent=self.group_box)

        layout.addWidget(self.left_pellet,1,0)
        layout.addWidget(self.center_pellet,1,1)
        layout.addWidget(self.right_pellet,1,2)
        layout.addWidget(self.left_hopper,2,0)
        layout.addWidget(self.center_hopper,2,1)
        layout.addWidget(self.right_hopper,2,2)
        layout.addWidget(self.prog_info,0,0,1,3)

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.group_box.setFont(font)
        hlayout = QHBoxLayout()
        self.group_box.setLayout(layout)
        hlayout.addWidget(self.group_box)
        hlayout.setSizeConstraint(QLayout.SetFixedSize)
        layout.setSizeConstraint(QLayout.SetFixedSize)        
        
        self.MODE = MODE
        self.setLayout(hlayout)
     
        
    def change_flag_CAN(self,msg):
        if not self.isRec and msg.data[0] is 96 and msg.data[1] is 1 and msg.data[3] is 64:
            self.isRec = True
            self.prog_info.labelStatus.setText('Recording')
            self.prog_info.labelRec.setPixmap(self.prog_info.iconRec)
        elif self.isRec and msg.data[0] is 96 and msg.data[1] is 1 and msg.data[3] is 66:
            self.isRec = False
            self.prog_info.labelStatus.setText('Pause')
            self.prog_info.labelRec.setPixmap(self.prog_info.iconPause)
            
    def change_flag_Xbee(self,msg):
        if 'rf_data' in msg:
            PAYLOAD = binascii.hexlify(msg['rf_data'])
            action = int(PAYLOAD[20:24], 16)
            if not self.isRec and action == 2:
                self.isRec = True
                self.prog_info.labelStatus.setText('Recording')
                self.prog_info.labelRec.setPixmap(self.prog_info.iconRec)
            elif self.isRec and action == 29:
                self.isRec = False
                self.prog_info.labelStatus.setText('Pause')
                self.prog_info.labelRec.setPixmap(self.prog_info.iconPause)
        else:
            return
            
    def start_exp(self):
        now = datetime.datetime.now()
        date, hour= now.isoformat().split('T')[0],now.isoformat().split('T')[1][:5]
        self.prog_info.label_2.setText('Start exp: %s'%date)
        self.prog_info.label_3.setText('At: %s'%hour)
        
    def analyze_msg(self, msg):
        if self.MODE:
            self.analyze_msg_Xbee(msg)
        else:
            self.analyze_msg_CAN(msg)
            
    def analyze_msg_CAN(self, msg):
        self.center_pellet.update_labels(msg)
        self.left_pellet.update_labels(msg)
        self.right_pellet.update_labels(msg)
        self.left_hopper.analyze_CAN_msg(msg)
        self.right_hopper.analyze_CAN_msg(msg)
        self.center_hopper.analyze_CAN_msg(msg)
        self.change_flag_CAN(msg)
        
    def analyze_msg_Xbee(self,msg):
        self.center_pellet.update_labels_Xbee(msg)
        self.left_pellet.update_labels_Xbee(msg)
        self.right_pellet.update_labels_Xbee(msg)
        self.left_hopper.analyze_XBee_msg(msg)
        self.right_hopper.analyze_XBee_msg(msg)
        self.center_hopper.analyze_XBee_msg(msg)
        self.change_flag_Xbee(msg)
        
    def clear(self):
        self.center_pellet.clear()
        self.left_pellet.clear()
        self.right_pellet.clear()

        
    def setPath2save(self,Dir):
       self.path2save = Dir
       self.prog_info.labelDir.setText(self.path2save)
       
    def setBacteryLevel(self,level):
        self.bacterylevel = level
        self.prog_info.bacterylevel_label.setText(self.bacterylevel)

def main():
    app = QApplication(sys.argv)
    app.exec_()

if __name__== '__main__':
    main()