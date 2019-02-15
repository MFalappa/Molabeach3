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
from PyQt5.QtWidgets import (QLabel,QDialog,QVBoxLayout,QProgressBar,QMessageBox)
from PyQt5.QtCore import QTimer

class uploadProgram_gui(QDialog):
    def __init__(self,commandList, devId, isLast=False,parent=None):
        super(uploadProgram_gui, self).__init__(parent)
        self.Label = QLabel('Uploading on device number %d'%devId)
        self.cnt = 0
        self.isLast = isLast
        layout= QVBoxLayout()
        layout.addWidget(self.Label)
        self.canReader = parent.Reader
        self.parent = parent
        self.canReader.received.disconnect()
        self.canReader.received.connect(self.recieveMsg)
        self.commandList = commandList
        self.reply = None
        
        # Progress bar        
        self.progress = QProgressBar()
        self.progress.setGeometry(200, 80, 850, 20)
        self.progress.setMinimumWidth(500)
        self.progress.setMinimum(0)
        self.progress.setMaximum(len(commandList)-1)
        layout.addWidget(self.progress)

        self.setLayout(layout)
        

    def exec_(self):
        #▒ insert progress bar
        QTimer.singleShot(50,lambda msg = self.commandList[0] : self.uploadProg(msg))
        super(uploadProgram_gui, self).exec_()
        
    def recieveMsg(self,msg):
        print('Recieved msg: %s'%msg.dataAsHexStr())
        if msg.data[3] == self.reply:
            try:
                self.commandList.pop(0)
                self.uploadProg(self.commandList[0])
                self.cnt += 1
                self.progress.setValue(self.cnt)
            except IndexError:
                if self.isLast:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
    
                    msg.setText("The program has been uploaded")
                    msg.setWindowTitle("Uploading successful")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                print('Finished Uploading')
                self.Label.setText('Finished Uploading')
                self.accept()
                self.canReader.received.disconnect()
                self.canReader.received.connect(self.parent.recieveMsg)
                self.close()
                
                
    def uploadProg(self,msg):
        print('Uploading msg: %s'%msg.dataAsHexStr())
        self.reply = msg.data[3]
        self.parent.serialPort.write(msg)
    