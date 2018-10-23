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
import pycanusb
import canportreader
from msgview import *
from messageLib import *
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QDialog,QApplication,QLabel,QHBoxLayout
import sys
from Parser import parsing_Funct
from check_prog import check_prog

class uploadProgram(QDialog):
    def __init__(self,commandList,parent=None):
        super(uploadProgram, self).__init__(parent)
        self.Label = QLabel('Connecting to adapter')
        layout= QHBoxLayout()
        layout.addChildWidget(self.Label)
        self.connectAdapter()
        self.canReader = canportreader.CanPortReader(self.canusb, self.recieveMsg,sampleRate=10)
        self.canReader.startReading()
        self.commandList = commandList
        self.reply = None
        QTimer.singleShot(500,lambda msg = commandList[0] : self.uploadProg(msg))
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
        self.Label.setText('Recieved msg: %s'%msg.dataAsHexStr())
        if msg.data[3] == self.reply:
            try:
                self.commandList.pop(0)
                self.uploadProg(self.commandList[0])
            except IndexError:
                print 'Finished Uploading'
                self.Label.setText('Finished Uploading')
                self.accept()
                
    def uploadProg(self,msg):
        print 'Uploading msg: %s'%msg.dataAsHexStr()
        self.Label.setText('Uploading msg: %s'%msg.dataAsHexStr())
        self.reply = msg.data[3]
        self.canusb.write(msg)
        
if __name__=='__main__':       
#    CommandList = []
#    CommandList += [switch_Lights_Msg(128+1536,1,2,5)]
#    CommandList += [ReleaseFood_Msg(128+1536,'Right')]
#    CommandList += [switch_Lights_Msg(128+1536,0,0,0)]
#    CommandList = parsing_Funct('C:\canusb_project\Programmi\\Program_Peak_Left.prg',13)
#    app = QApplication(sys.argv)
#    dlg = uploadProgram(CommandList)

    file_name = 'C:\Users\MFalappa\Desktop\Microsystem\sw\\Program_switch_probes.txt'
    tof, sentence = check_prog(file_name)
    print sentence
    if tof:
        CommandList = parsing_Funct(file_name,15)
        app = QApplication(sys.argv)
        dlg = uploadProgram(CommandList)
#    dlg.show()
    dlg.exec_()
    #print(form.exec_())
    app.exec_()