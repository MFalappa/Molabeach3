#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 13:22:30 2019

@author: Matte
"""
import sys
import os
import serial
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(file_dir,'libraries'))
from PyQt5.QtWidgets import QApplication,QDialog,QHBoxLayout,QPushButton
from PyQt5.QtCore import pyqtSignal,QThread,QTimer
from Modify_Dataset_GUI import OrderedDict
#import binascii
from serial.tools import list_ports

# message flags
CANMSG_EXTENDED      = 128
CANMSG_RTR           = 64
# Carriage return command for CanUSB
CR = b'\r'   
# Open command for CanUSB
OPEN = b'O\r'  
# Close command for CanUSB
CLOSE = b'C\r' 
canbaud = b'S6'

from ctypes import (c_uint,c_ubyte,Structure)
class CANMsg(Structure):
    _fields_ = [("id", c_uint),
                ("timestamp", c_uint),
                ("flags", c_ubyte),
                ("len", c_ubyte),
                ("data", c_ubyte * 8)]
    
    def __repr__(self):
        if self.flags & CANMSG_EXTENDED:
            ext = '|Extended'
        else:
            ext = ''
        if self.flags & CANMSG_RTR:
            rtr = '|RTR'
        else:
            rtr = ''
        return "ID: %d%s%s, Length: %d, Data: %s, Timestamp: %d" % (self.id, ext, rtr, self.len, self.dataAsHexStr(), self.timestamp)
        
    def dataAsHexStr(self, length=8, prefix='0x'):
        s = prefix
        for i in range(length):
            if i < self.len:
                s = s + '%0.2x' % self.data[i]
            else:
                s = s + '00'
        return s
        
    def copy(self):
        m = CANMsg()
        m.id = self.id
        m.timestamp = self.timestamp
        m.flags = self.flags
        m.len = self.len
        for i in range(self.len):
            m.data[i] = self.data[i]
        return m

class recievingCanUsbThread(QThread):
    recieved = pyqtSignal(CANMsg, name='canMsgReceived')
    def __init__(self, serialPort, parent=None):
        super(recievingCanUsbThread,self).__init__()
        self.serialPort = serialPort
        
    def startReading(self):
        if not self.isRunning():
            self.start()
        
    def stopReading(self):
        if self.isRunning() == True:
            self.exit()
            self.wait() 
        
    def emitSignal(self, msg):
        self.recieved.emit(msg) 
        
    def run(self):
        self.setPriority(QThread.HighestPriority)
        QTimer.singleShot(20,self.connectCanUsb)
        self.exec_()
        
    def connectCanUsb(self):
        print('sono connesso con can')
        self.canUsb = serial.Serial(self.serialPort, baudrate=500000,timeout=1)
        
#
        
    def readSerial(self):
        print('to be implemented')
#        self.timer.stop()
#        byte = self.canUsb.read_until(b'\r')
#        
#        print(byte)
#        byte = b't70D17F\r'
#        print(byte)


    def terminate(self):
        if self.isRunning() == True:
            self.exit()
            self.wait() 
            print('all disconnected')
        super(recievingCanUsbThread,self).terminate()
        print('thread reciever terminated ')



class canUsb_thread(QThread):
    addNewDevice = pyqtSignal(CANMsg, name='newDeviceFound')
    def __init__(self, serialPort, parent = None):
        super(canUsb_thread,self).__init__(parent)
        self.serialPort = serialPort
        self.address_dict = OrderedDict()
        
    def run(self):
        self.canUsb = serial.Serial(self.serialPort, baudrate=500000,timeout=1)
        print('mi sono connesso')
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_new_address)
        self.timer.start(500)
        self.exec_()
        
    def terminate(self):
        if self.isRunning() == True:
            self.exit()
            self.wait() 
            print('all disconnected')
        super(canUsb_thread,self).terminate()
        
    def add_new_address(self):
        print('sto cercando il device')
        self.timer.stop()
        self.canUsb.write(canbaud+CR)
        byte = self.canUsb.read_until(b'\r') 
        byte = b't70D17F\r'
        print(byte)
        
        if byte is b'':
            self.timer.start(500)
            return
        else:
            if byte[0] == 116:
                msg = CANMsg()
                msg.id = int(byte[1:4],16)
                if not msg.id in list(self.address_dict.keys()):
                    msg.len = byte.bytesize
                    msg_tr = (c_ubyte * 8)(*[c_ubyte(c) for c in byte[:8]])
                    msg.data = msg_tr         
#                    msg.data[0] = 7  
                    self.addNewDevice.emit(msg)
                    self.timer.start(500)
                else:
                    self.timer.start(500)
            else:
                self.timer.start(500)
    
    
def parsing_can_log(message):
    if message.data[0] is 76 and message.data[1] is 1:
        Id = message.id - 640
        return 'Log', Id, '%d\t%d\n'%(int(message.dataAsHexStr()[4:12],16),
                                              message.data[6])
    elif message.data[0] is 96 and message.data[1] is 2:
        if message.data[3] is 5:
            return 'Set Date',message.id-1408, None
        elif message.data[3] is 6:
            return 'Set Time',message.id-1408, None
            
    elif message.data[0] is 96:
        Id = message.id - 1408
        return Id, None
    elif message.data[0] == 67 and message.data[1] is 1 and\
        message.data[3] is 65:
        Id = message.id - 1408
        time = int(message.dataAsHexStr()[-2:]+message.dataAsHexStr()[-4:-2]+
                message.dataAsHexStr()[-6:-4]+message.dataAsHexStr()[-8:-6],16)
        return 'Timer',Id, '%d\t38\n'%time
    
    elif message.data[0] is 67 and message.data[1] is 2:
        print('Entered in time settings',message.data[3])
        Id = message.id - 1408
        if message.data[3] == 5:
            return 'Date',Id,'%d-%d-%d'%(message.data[4],message.data[5],
                                   message.data[6])
        elif message.data[3] == 6:
            return 'Time',Id, '%d:%d:%d'%(message.data[7],message.data[6],
                                   message.data[5])
    else:
        print('Not recognize data')
        print(message,'\n')
#        raise ValueError
  

    
        
if __name__ == "__main__":
    # Carriage return command for CanUSB
    CR = b'\r'
    
    # Open command for CanUSB
    OPEN = b'O\r'
    
    # Close command for CanUSB
    CLOSE = b'C\r'
    
    canbaud = b'S6'
    
    for val in list_ports.comports():
        port = val[0]
        descr = val[1]
        
        if 'CANUSB' in descr:
            print(descr)
            port_can = port

    
   