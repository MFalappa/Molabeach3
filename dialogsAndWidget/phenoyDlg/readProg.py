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
sys.path.append(lib_dir)
import pycanusb
import canportreader
from msgview import *
from messageLib import *
from PyQt4.QtCore import QTimer,Qt
from PyQt4.QtGui import QDialog,QApplication,QLabel,QHBoxLayout

#from Parser import parsing_Funct
#from time import sleep
class readProgram(QDialog):
    def __init__(self,parent=None,Id=127):
        super(readProgram, self).__init__(parent)
        self.Label = QLabel('Connecting to adapter')
        layout= QHBoxLayout()
        layout.addChildWidget(self.Label)
        self.connectAdapter()
        self.canReader = canportreader.CanPortReader(self.canusb, self.recieveMsg,sampleRate=10)
        self.canReader.startReading()
        self.ListOfMsg=[]
        self.Index=0
        self.Id = Id
        self.ProgLen = 0
        self.reply = None
        QTimer.singleShot(500, self.startReading)
        self.setLayout(layout)

    def connectAdapter(self):
        """
            Connecting to the adapter via pycanusb.py 
        """
        self.canusb = pycanusb.CanUSB(bitrate='500')
        print('CanUSB: ',self.canusb)
        Msg = Switch_to_Operational_State_Msg()
        QTimer.singleShot(50,lambda msg = Msg : self.initialization(Msg))
        
    
    def initialization(self,msg):
        self.canusb.write(msg)
        print 'Initialized'
        self.Label.setText('Initialized')
        
    def recieveMsg(self,msg):
        print 'Recieved msg: %s'%msg.dataAsHexStr()
#        print msg.data[3],msg.data[4],msg.data[5]
        self.Label.setText('Recieved msg: %s'%msg.dataAsHexStr())
        if msg.data[3] == self.reply and self.reply==37:
            self.ProgLen = 16**2 * msg.data[5] + msg.data[4]
            print self.ProgLen
            return
            self.readProg()
        elif msg.data[3] == self.reply:
            self.readProg()
            self.ListOfMsg += [msg]
                       
    def startReading(self):
        msg = read_Size_Log_and_Prog(self.Id)
        self.reply = 37
        self.canusb.write(msg)
        
    def readProg(self):
        print self.ProgLen,self.Index
        if self.Index==self.ProgLen:
            self.accept()
            self.reply = None
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
    dlg =readProgram(Id=1)
    dlg.show()
    app.exec_()
    newList=[]
    fh = open('C:\Users\ebalzani\IIT\Dottorato\Matte\Color Preference\Data\\27-6 to 28-6\\change_color_prog_uploaded.txt','w')
    for msg in dlg.ListOfMsg:
        print msg.dataAsHexStr(),msg.data[4]
        fh.write(msg.dataAsHexStr()+'\n')
    fh.close()
    dlg.close()

    #print(form.exec_())

