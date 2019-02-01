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

import sys,os
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses')
sys.path.append(lib_dir)
sys.path.append(classes_dir)
import pycanusb
import canportreader
from msgview import *
from messageLib import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QDialog,QApplication,QLabel,QVBoxLayout,QProgressBar
from read_output_prg import *
#from Parser import parsing_Funct
#from time import sleep
class readProgram(QDialog):
    def __init__(self,row_dict,transl_dict,parent=None,Id=127):
        super(readProgram, self).__init__(parent)
        
        self.row_dict = row_dict
        self.transl_dict = transl_dict
        
        self.canusb = parent.parent.serialPort
        self.canReader = parent.parent.Reader
        self.parent = parent
        self.canReader.received.disconnect()
        self.canReader.received.connect(self.recieveMsg)
        
        # Progress bar  
        self.Label = QLabel('Reading program from box %d'%Id)
        self.cnt = 0
        layout= QVBoxLayout()
        layout.addWidget(self.Label)
        self.progress = QProgressBar()
        self.progress.setGeometry(200, 80, 850, 20)
        self.progress.setMinimumWidth(500)
        self.progress.setMinimum(0)
        layout.addWidget(self.progress)        
        
        self.setLayout(layout)

        self.ListOfMsg = []
        self.ListOfMsg_str = []
        self.Index=0
        self.Id = Id
        self.ProgLen = 0
        self.reply = None
#        QTimer.singleShot(500, self.startReading)
    
    def exec_(self):
        #▒ insert progress bar
        QTimer.singleShot(50,self.startReading)
        super(readProgram, self).exec_()
        
        
    
    def initialization(self,msg):
        self.canusb.write(msg)
        print('Initialized')
        
    def recieveMsg(self,msg):
        print('Recieved msg: %s'%msg.dataAsHexStr())
        if msg.data[3] == self.reply and self.reply==37:
            self.ProgLen = 16**2 * msg.data[5] + msg.data[4]
            self.progress.setMaximum(self.ProgLen - 1)
            self.readProg()
        elif msg.data[3] == self.reply:
            self.readProg()
            self.ListOfMsg += [msg]
            self.ListOfMsg_str += [msg.dataAsHexStr()]
            self.cnt += 1
            self.progress.setValue(self.cnt)
                       
    def startReading(self):
        msg = read_Size_Log_and_Prog(self.Id)
        self.reply = 37
        self.canusb.write(msg)
        
    def readProg(self):
        if self.Index==self.ProgLen:
            int_list = hexString_to_int(self.ListOfMsg_str)
            program_transl = create_program(int_list)
            self.canReader.received.disconnect()
            self.canReader.received.connect(self.parent.parent.recieveMsg)
            self.row_dict[self.Id] = self.ListOfMsg_str
            self.transl_dict[self.Id] = program_transl
            self.accept()
            self.reply = None
            self.close()
        else:    
            msg = read_External_EEPROM(self.Id,self.Index)
            self.reply = msg.data[3]
            self.canusb.write(msg)
            self.Index +=1
            
if __name__=='__main__':  
    import numpy as np     
#    CommandList = []
#    CommandList += [switch_Lights_Msg(128,1,2,5)]
#    CommandList += [ReleaseFood_Msg(128,'Right')]
#    CommandList += [switch_Lights_Msg(128,0,0,0)]
#    CommandList = parsing_Funct('C:\Users\ebalzani\Desktop\labview\Program_Example_2.prg',128)
    app = QApplication(sys.argv)
    dlg =readProgram({},{},Id=1)
    dlg.show()
    app.exec_()
    newList=[]
    fh = open('C:\\Users\ebalzani\IIT\Dottorato\Matte\Color Preference\Data\\27-6 to 28-6\\change_color_prog_uploaded.txt','w')
    for msg in dlg.ListOfMsg:
        print(msg.dataAsHexStr(),msg.data[4])
        fh.write(msg.dataAsHexStr()+'\n')
    fh.close()
    dlg.close()

    #print(form.exec_())

