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

from PyQt4.QtCore import QTimer, QSize
from PyQt4.QtGui import QPixmap, QLayout, QSizePolicy, QWidget, QDialog,\
    QApplication, QHBoxLayout, QImage, QFont
import ui_hopper_widget
import sys
import os
path_img = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'images')
from messageLib import *
from time import clock

class hopper_widget(QWidget, ui_hopper_widget.Ui_hopper_widget):
    def __init__(self, side, parent=None):
        super(hopper_widget, self).__init__(parent)
        self.setupUi(self)
#        specerItem = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.lightOff = QPixmap.fromImage(QImage(os.path.join(path_img,'LightOff_50.png')))
        self.lightOff = self.lightOff.scaled(QSize(30,30))
        self.lightOn = QPixmap.fromImage(QImage(os.path.join(path_img,'LightOn_50.png')))
        self.lightOn = self.lightOn.scaled(QSize(30,30))
        self.nose_In = QPixmap.fromImage(QImage(os.path.join(path_img,'raton_rescaled.jpg')))
        self.nose_In = self.nose_In.scaled(QSize(46,23))
        self.label_light.setPixmap(self.lightOff)
        self.label_NP.clear()
        self.label_noise.setText('Off')
        self.font = QFont('',8)
        self.label_4.setFont(self.font)
        self.label_4.setText('Nose Out')
        self.label_empty.setText('')
        self.label_empty.setFixedHeight(10)
#==============================================================================
#     SET ALL FONTS TO REDUCE FONTSIZE
#==============================================================================
        
        self.groupBox_hopper.setStyleSheet("QGroupBox { background-color: rgb(255, 255,\
            255); border:1px solid rgb(83, 84, 84); }")
        if side == 'Left':
            self.light_on_msg = 22
            self.light_off_msg = 23
            self.noise_on_msg = 42
            self.noise_off_msg = 43
            self.nose_in_msg = 28
            self.nose_out_msg = 29
        elif side == 'Center':
            self.light_on_msg = 24
            self.light_off_msg = 25
            self.noise_on_msg = 44
            self.noise_off_msg = 45
            self.nose_in_msg = 30
            self.nose_out_msg = 31
        elif side == 'Right':
            self.light_on_msg = 26
            self.light_off_msg = 27
            self.noise_on_msg = 46
            self.noise_off_msg = 47
            self.nose_in_msg = 32
            self.nose_out_msg = 33
        self.groupBox_hopper.setFixedSize(150, 130)

#        QTimer.singleShot(5100,lambda x = 'Off': self.set_icon_light(x))
#        print 'GB size',self.groupBox_hopper.size()
    def set_icon_light(self, On_Off):
        if On_Off is 'Off':
            self.label_light.setPixmap(self.lightOff)
        else:
            self.label_light.setPixmap(self.lightOn)
            
    def set_icon_nose(self, In_Out):
        if In_Out is 'In':
            self.label_NP.setPixmap(self.nose_In)
#            self.label_NP.setFixedHeight(50)
            self.label_4.setText('Nose In')
        else:
            self.label_NP.clear()
#            self.label_NP.setFixedHeight(50)
            self.label_4.setFont(self.font)
            self.label_4.setText('Nose Out')
            
    def set_noise(self, On_Off):
        if On_Off is 'Off':
            self.label_noise.setText('Off')
        else:
            self.label_light.setPixmap(self.lightOn)
    
    def analyze_CAN_msg(self, msg):
#        print msg.data[6] 
        if msg.data[6] is self.light_on_msg:
            self.set_icon_light('On')

        elif msg.data[6] is self.light_off_msg:
            self.set_icon_light('Off')

        elif msg.data[6] is self.nose_in_msg:
            self.set_icon_nose('In')

        elif msg.data[6] is self.nose_out_msg:
            self.set_icon_nose('Out')

        elif msg.data[6] is self.noise_on_msg:
            self.label_noise.setText('On')

        elif msg.data[6] is self.noise_off_msg:
            self.label_noise.setText('Off')

#        print clock() - t0
        
    def analyze_XBee_msg(self, msg):
        try:
            PAYLOAD = binascii.hexlify(msg['rf_data'])
            action = int(PAYLOAD[20:24], 16)
            if action is self.light_on_msg:
                self.set_icon_light('On')

            elif action is self.light_off_msg:
                self.set_icon_light('Off')

            elif action is self.nose_in_msg:
                self.set_icon_nose('In')

            elif action is self.nose_out_msg:
                self.set_icon_nose('Out')

            elif action is self.noise_on_msg:
                self.label_noise.setText('On')

            elif action is self.noise_off_msg:
                self.label_noise.setText('Off')

        except KeyError:
            return None
        
            
class testdlg(QDialog):
    def __init__(self, parent=None):
        super(testdlg,self).__init__(parent)
        layout = QHBoxLayout()
#        scroll_area = QScrollArea()
        self.hopper_widget = hopper_widget('Left')
#        self.hopper_widget.resize(QSize(292,178))
#        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
#                                                     QSizePolicy.Fixed))
#        scroll_area.setWidget(self.hopper_widget)
        layout.addWidget(self.hopper_widget)
#        self.resize(size)
        self.setLayout(layout)
        Msg = pycanusb.CANMsg()
        Msg.id = 127
        Msg.len = 8
        Msg.data[6] = 22
        
        Msg1 = pycanusb.CANMsg()
        Msg1.id = 127
        Msg1.len = 8
        Msg1.data[6] = 28
        
        Msg2 = pycanusb.CANMsg()
        Msg2.id = 127
        Msg2.len = 8
        Msg2.data[6] = 29
        
        Msg3 = pycanusb.CANMsg()
        Msg3.id = 127
        Msg3.len = 8
        Msg3.data[6] = 23
        
        QTimer.singleShot(4000, lambda x = Msg1: self.hopper_widget.analyze_CAN_msg(x))
        QTimer.singleShot(4000, lambda x = Msg: self.hopper_widget.analyze_CAN_msg(x))
        QTimer.singleShot(8000, lambda x = Msg2: self.hopper_widget.analyze_CAN_msg(x))
        QTimer.singleShot(10000, lambda x = Msg3: self.hopper_widget.analyze_CAN_msg(x))
#
def main():
    app = QApplication(sys.argv)
    form = hopper_widget('Left')
#    form = testdlg()
    form.show()
#    print form.size()
    app.exec_()
    print form.groupBox_hopper.size()
if __name__ == '__main__':
    main()
#    

#main()