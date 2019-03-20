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
import sys
import os
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(file_dir,'libraries'))
from xbee import XBee
from PyQt5.QtCore import pyqtSignal,QThread,QTimer
from Modify_Dataset_GUI import OrderedDict
import binascii
from numpy import base_repr



class XBeeMsg(object):
    def __init__(self, msg, source_address,parent = None):
        if type(msg) is dict:
          self.xbeeForm = msg
        else:
            self.xbeeForm = {}
            self.xbeeForm['source_addr'] = source_address
            
            index_0 = base_repr(msg[0],16)
            index_1 = base_repr(msg[1],16)
            if len(index_0)>4 or len(index_1)>4:
                raise ValueError
            index_0 = '0'*(4-len(index_0)) + index_0
            index_1 = '0'*(4-len(index_1)) + index_1
            self.xbeeForm['rf_data'] = (binascii.unhexlify(index_0).decode('utf8') + 
                                        binascii.unhexlify(index_1).decode('utf8'))
            for i in msg[2:]:
                if i is 0:
                   self.xbeeForm['rf_data'] += '\x00'
                else:
                    try:
                        self.xbeeForm['rf_data'] += binascii.unhexlify(base_repr(i,16,1)).decode('utf8')
                    except:
                        self.xbeeForm['rf_data'] += binascii.unhexlify(base_repr(i,16)).decode('utf8')
             
            
            self.xbeeForm['rf_data'] = bytearray(self.xbeeForm['rf_data'], 'utf8')
            string_end = (14-len(self.xbeeForm['rf_data']))* binascii.unhexlify(base_repr(255,16))
            self.xbeeForm['rf_data'] += string_end
            self.xbeeForm['options'] = bytearray(b'\x00')
    
    def has_key(self,key):
        return key in list(self.xbeeForm.keys())
        
    def __getitem__(self,key):
        return self.xbeeForm[key]
    def __setitem__(self,key,value):
        self.xbeeForm[key] = value
    def __repr__(self):
        return 'XBeeMsg: ' + self.xbeeForm.__repr__()
    
    def toIntList(self):
        stringData = binascii.hexlify(self.xbeeForm['rf_data'])
        listData = [int(stringData[:4],16),int(stringData[4:8],16)]
        for num in stringData[8::2]:
            listData += [int(num,16)]
        listData += (12-len(listData))*[255]
        return listData
        
    def byteArrayToSend(self):
        start = bytearray(b'\x7E')
        length = bytearray(b'\x00\x19')
        API_ID_Mes = bytearray(b'\x00')
        Count_Mes = bytearray(b'\x01')
        useful = bytearray()
#        print(self.xbeeForm)
        useful = (API_ID_Mes + Count_Mes + self.xbeeForm['source_addr'] 
                    + self.xbeeForm['options'] + self.xbeeForm['rf_data'])
        chks = self.calcCheckSum(useful)
        useful.append(int(chks,16))
        return start + length + useful
    
    def calcCheckSum(self,resp): #resp array di int #return str hex (Es. '0x7e')
    	hex_sum = 0
    	for i in resp:
    		hex_sum = hex_sum + i
    	hex_sum = hex(hex_sum & int('0xFF',16))
    	hex_sum = hex(int('0xFF',16) - int(hex_sum,16))
    	return hex_sum
    
    def isCheckSum(self,resp): # return true/false
    	useful = resp[3:-1]
    	cksum = resp[-1]
    	hex_sum = self.calcCheckSum(useful)
    	return (hex(cksum) == hex_sum)

class recievingXBeeThread(QThread):
    received = pyqtSignal(dict, name='xBeeMsgReceived')
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
        self.received.emit(msg) 
        
    def run(self):
        self.setPriority(QThread.HighestPriority)
        QTimer.singleShot(20,self.connectXBee)
        self.exec_()
        
    def connectXBee(self):
        self._xBee = XBee(self.serialPort, callback = self.emitSignal)
#        print('Connected')
        
    def terminate(self):
        if self.isRunning() == True:
            self._xBee.halt()
            self.exit()
            self.wait() 
            print('all disconnected')
        super(recievingXBeeThread,self).terminate()
#        print('thread reciever terminated ')
        

class ZigBee_thread(QThread):
    addNewDevice = pyqtSignal(dict, name='newDeviceFound')
    def __init__(self, serialPort, parent = None):
        super(ZigBee_thread,self).__init__(parent)
        self.serialPort = serialPort
        self.readThread = recievingXBeeThread(serialPort)
        self.address_dict = OrderedDict()
        

    def run(self):
        self.readThread.received.connect(self.add_new_address)
        self.setPriority(QThread.HighestPriority)
        self.readThread.start()
        self.exec_()
        
    def terminate(self):
        self.readThread.terminate()
        try:
            self.readThread.received.disconnect()
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

    
def parsing_XBee_log(message,pc_id=b'0001'):
    try:
        PAYLOAD = binascii.hexlify(message['rf_data'])
        
        if PAYLOAD[:4] == pc_id:
            is_answ = True
        else:
            is_answ = False

        Id = int(PAYLOAD[4:8], 16)
        
        if PAYLOAD[8:12] == b'034c': # logfiles
            action = int(PAYLOAD[20:24], 16)
            if action > 15:
                time = int(PAYLOAD[12:20], 16)
            else:
                time = int(PAYLOAD[18:20], 16)
            return 'Log', Id, '%d\t%d'%(time,action)
        
        if PAYLOAD[8:12] == b'0201': # stand alone mode
            return 'Stand Alone Mode', Id, 'Action'
        
        elif PAYLOAD[8:10] == b'01':
            return 'Info', Id, 'Device Actuated'
        
        elif PAYLOAD[8:10] == b'05':
            if is_answ:
                return 'Info', Id, 'Bactery Level %d'%int(PAYLOAD[10:14],16)
            else:
                return 'Info', Id, 'Request get Bactery Level'
        
        elif PAYLOAD[8:10] == b'06':
            if is_answ:
                day = int(PAYLOAD[12:14], 16)
                month = int(PAYLOAD[14:16], 16)
                year = int(PAYLOAD[16:18], 16)
                hour = int(PAYLOAD[18:20], 16)
                minute = int(PAYLOAD[20:22], 16)
                second = int(PAYLOAD[22:24], 16)
               
                return 'Info', Id, 'Date %d-%d-%d Time %d:%d:%d'%(day,month,year,
                                                         hour,minute,second)
            else:
                return 'Info', Id, 'Request get Date and Time'
        
        elif PAYLOAD[8:10] == b'07':
            if is_answ:
                return 'Info', Id, 'RGB message'
            else:
                return 'Info', Id, 'Request RGB message'
        
        elif PAYLOAD[8:10] == b'08':
            return 'Info', Id, 'Sound message'
        
        elif PAYLOAD[8:10] == b'09':
            if is_answ:
                return 'Info', Id, 'Release pellet'
            else:
                return 'Info', Id, 'Request release pellet'
            
        elif PAYLOAD[8:10] == b'0b':
            if is_answ:
                return 'Info', Id, 'Subject number set'
            else:
                return 'Info', Id, 'Request set subject number'
        
        elif PAYLOAD[8:10] == b'0c':
            if is_answ:
                return 'Info', Id, 'Experiment id set'
            else:
                return 'Info',Id, 'Request exp id set'
        
        elif PAYLOAD[8:10] == b'0d':
            if is_answ:
                return 'Info', Id, 'Phase set'
            else:
                return 'Info',Id, 'Request phase set'
        
        elif PAYLOAD[8:10] == b'0e':
            if is_answ:
                return 'Info', Id, 'Box id set'
            else:
                return 'Info', Id, 'Request box id set'
        
        elif PAYLOAD[8:10] == b'0f':
            if is_answ:
                trial_num = int(PAYLOAD[10:14],16)
                return 'Info', Id, 'Trial number %d'%trial_num
            else:
                return 'Info', Id, 'Request get trial number'
        
        elif PAYLOAD[8:10] == b'12':
            if is_answ:
                print('trial time payload',PAYLOAD)
                return 'Info', Id, 'Trial time %d'%int(PAYLOAD[12:20], 16)
            else:
                return 'Info', Id, 'Request get real Time'
        
        elif PAYLOAD[8:10] == b'14':
            if is_answ:
                return 'Info', Id, 'Ext EEPROM address %d'%(int(PAYLOAD[10:14],16))
            else:
                return 'Info', Id, 'Request get ext EEPROM'
        
        elif PAYLOAD[8:10] == b'15':
            if is_answ:
                return 'Info', Id, 'Trial max number set'
            else:
                return 'Info', Id, 'Request set trial max number'
        
        elif PAYLOAD[8:10] == b'16':
            if is_answ:
                trial_max = int(PAYLOAD[10:18],16)
                return 'Info', Id, 'Trial Max Number %d'%trial_max
            else:
                return 'Info', Id, 'Request get max trial number'
        
        elif PAYLOAD[8:10] == b'17':#check if true
            if is_answ:
                return 'Info', Id, 'Set trial timeout'%trial_max
            else:
                return 'Info', Id, 'Request set trial timeout'
        
        elif PAYLOAD[8:10] == b'18':#check if true
            if is_answ:
                trial_max = int(PAYLOAD[10:18],16)
                return 'Info', Id, 'Trial Timeout %d\n'%trial_max
            else:
                return 'Info', Id, 'Request get trial timeout'
        
        elif PAYLOAD[8:10] == b'1b':
            if is_answ:
                return 'Info', Id, 'Mean Distribution set'
            else:
                return 'Info', Id, 'Request set mean distribution'
        
        elif PAYLOAD[8:10] == b'1c':
            if is_answ:
                return 'Info', Id, 'Mean Distribution %d'%int(PAYLOAD[10:14],16)
            else:
                return 'Info', Id, 'Request get mean distribution'
        
        elif PAYLOAD[8:10] == b'20':#check if true
            if is_answ:
                return 'Info', Id, 'Probablity Array Index %d Value %d, %d, %d\n'%int(PAYLOAD[10:18],16)
            else:
                return 'Info', Id, 'Request get probability array'
        
        elif PAYLOAD[8:10] == b'24':
            if is_answ:
                return 'Info', Id, 'Program Size %d\n'%int(PAYLOAD[14:18],16)
            else:
                return 'Info', Id, 'Request get program size'
        
        elif PAYLOAD[8:10] == b'04':
            if is_answ:
                return 'Keep Alive', Id, None
            else:
                return 'Keep Alive', Id, None
        
        elif PAYLOAD[8:10] == b'1d':
            return 'Stop Stand Alone', Id, 'Stop Stand Alone'
            
            
        else:
            print('**************')
            print(PAYLOAD[8:10])
            raise AttributeError
    except:
        return 'Status', None, None