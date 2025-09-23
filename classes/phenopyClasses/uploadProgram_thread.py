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
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
class_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'classes','analysisClasses')
phenoDlg_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'dialogsAndWidget','phenoyDlg')
sys.path.append(class_dir)
sys.path.append(lib_dir)
sys.path.append(phenoDlg_dir)
import pycanusb
import canportreader
from msgview import *
from messageLib import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QDialog,QApplication,QLabel,QHBoxLayout
from Parser import parsing_Funct
from check_prog import check_prog

class uploadProgram(QThread):
    def __init__(self,commandList,canusb,lock,parent=None):
        super(uploadProgram, self).__init__(parent)
        self.canusb = canusb
        self.canReader = canportreader.CanPortReader(self.canusb, self.recieveMsg,sampleRate=10)
        self.canReader.startReading()
        self.commandList = commandList
        self.reply = None
        self.lock = lock
        
    
    def initialization(self,msg):
        self.canusb.write(msg)
        print('Initialized')
        self.Label.setText('Initialized')
    
    
    def recieveMsg(self,msg):
        print('Recieved msg: %s'%msg.dataAsHexStr())
        self.Label.setText('Recieved msg: %s'%msg.dataAsHexStr())
        if msg.data[3] == self.reply:
            try:
                self.commandList.pop(0)
                self.uploadProg(self.commandList[0])
            except IndexError:
                print('Finished Uploading')
                self.Label.setText('Finished Uploading')
                self.accept()
                
    def uploadProg(self,msg):
        print('Uploading msg: %s'%msg.dataAsHexStr())
        self.Label.setText('Uploading msg: %s'%msg.dataAsHexStr())
        self.reply = msg.data[3]
        self.canusb.write(msg)
    

if __name__=='__main__':       
#    CommandList = []
#    CommandList += [switch_Lights_Msg(128+1536,1,2,5)]
#    CommandList += [ReleaseFood_Msg(128+1536,'Right')]
#    CommandList += [switch_Lights_Msg(128+1536,0,0,0)]
    file_name = 'C:\\Users\ebalzani\IIT\myPython\\canusb_project\Programmi\\Program_Peak_Left.prg'
    tof, sentence = check_prog(file_name)
    print(sentence)
    if tof:
        CommandList = parsing_Funct(file_name,3)
        app = QApplication(sys.argv)
        dlg = uploadProgram(CommandList)
##    dlg.show()
#    dlg.exec_()
#    #print(form.exec_())
#    app.exec_()