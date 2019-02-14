#!/usr/bin/env python3
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
from PyQt5.QtCore import pyqtSignal,QThread,QTimer
from Modify_Dataset_GUI import OrderedDict
from xbee import XBee
import binascii


class recievingXBeeThread(QThread):
    recieved = pyqtSignal(dict, name='xBeeMsgReceived')
    def __init__(self, serialPort, parent=None):
        super(recievingXBeeThread,self).__init__()
        self.serialPort = serialPort
        
    def startReading(self):
        if not self.isRunning():
            self.start()
            
    def stopReading(self):
        if self.isRunning() == True:
            self._xBee.halt()
            self.exit()
            self.wait()      
    def emitSignal(self, msg):
        self.recieved.emit(msg) 
        
    def run(self):
        self.setPriority(QThread.HighestPriority)
        QTimer.singleShot(20,self.connectXBee)
        self.exec_()
        
    def connectXBee(self):
        self._xBee = XBee(self.serialPort, callback = self.emitSignal)
        print('Connected')
        
    def terminate(self):
        if self.isRunning() == True:
            self._xBee.halt()
            self.exit()
            self.wait() 
            print('all disconnected')
        super(recievingXBeeThread,self).terminate()
        print('thread reciever terminated ')

class ZigBee_thread(QThread):
    addNewDevice = pyqtSignal(dict, name='newDeviceFound')
    def __init__(self, serialPort, parent = None):
        super(ZigBee_thread,self).__init__(parent)
        self.serialPort = serialPort
        self.readThread = recievingXBeeThread(serialPort)
        self.address_dict = OrderedDict()
        

    def run(self):
        self.readThread.recieved.connect(self.add_new_address)
        self.setPriority(QThread.HighestPriority)
        self.readThread.start()
        self.exec_()
        
    def terminate(self):
        self.readThread.terminate()
        try:
            self.readThread.recieved.disconnect()
        except TypeError:
            pass
        super(ZigBee_thread,self).terminate()
    
    def add_new_address(self,msg):
        try:
            PAYLOAD = binascii.hexlify(msg['rf_data'])
            ID = int(PAYLOAD[4:8], 16)
            if not ID in list(self.address_dict.keys()):
                self.address_dict[ID] = msg['source_addr']
                thisdict = {ID: msg['source_addr']}
                self.addNewDevice.emit(thisdict)
        except KeyError:
            pass

    
def parsing_XBee_log(message):
    try:
        PAYLOAD = binascii.hexlify(message['rf_data'])
        print('PAYLOAD', PAYLOAD)
        Id = int(PAYLOAD[4:8], 16)
#        print 'Id', Id
#        print PAYLOAD[8:10],PAYLOAD[8:10] == '06'
        if PAYLOAD[8:12] == '034c':
            action = int(PAYLOAD[20:24], 16)
            if action > 15:
                time = int(PAYLOAD[12:20], 16)
            else:
                time = int(PAYLOAD[18:20], 16)
            return 'Log', Id, '%d\t%d\n'%(time,action)
        elif PAYLOAD[8:10] == '06':
            day = int(PAYLOAD[12:14], 16)
            month = int(PAYLOAD[14:16], 16)
            year = int(PAYLOAD[16:18], 16)
            hour = int(PAYLOAD[18:20], 16)
            minute = int(PAYLOAD[20:22], 16)
            second = int(PAYLOAD[22:24], 16)
           
            return 'Datetime', Id, '%d-%d-%d\t%d:%d:%d'%(day,month,year,
                                                         hour,minute,second)
        else:
            raise AttributeError
    except:
        raise ValueError
        
    return 127,'parsing to be implemented\n'    