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
from PyQt5.QtCore import pyqtSignal,QThread,QTimer
from Modify_Dataset_GUI import OrderedDict
#from time import sleep
import binascii
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

setupBytes = canbaud + CR

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
    
    def to_byte(self):
        x = b't'
        x = (x + bytes(hex(self.id)[2:],'utf-8') + 
             bytes(hex(self.len)[2:],'utf-8')+
             binascii.hexlify(self.data))
        x = x + b'\r'
                          
        return x
        
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
        self.canUsb = serial.Serial(self.serialPort, baudrate=500000,timeout=0)
        self.canUsb.write(OPEN)
        self.canUsb.write(CLOSE)
        self.canUsb.write(canbaud+CR)
        self.canUsb.write(OPEN)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.readSerial)
        self.timer.start(1)
        self.exec_()
        
    def readSerial(self):
        self.timer.stop()
        byte = self.canUsb.read() 
        if byte is not b'':
            if byte[0] == 116:
                while byte[-1] != 13:
                    byte += self.canUsb.read()
                
#                print('byte is: ', byte)
                msg = CANMsg()
                msg.id = int(byte[1:4],16)
                msg.len = int(byte[4:5],16)
                byteNew = byte[-3:-1] + b'0'*(16-2*msg.len)
                list_msg = []
                for kk in range(0,len(byteNew),2):
                    list_msg += [int(byteNew[kk:kk+2],16)]
                X = (c_ubyte * 8)(*[c_ubyte(c) for c in list_msg])
                msg.data = X
                self.recieved.emit(msg)

        self.timer = QTimer()    
        self.timer.timeout.connect(self.readSerial)
        self.timer.start(1)
        
    def writeSerial(self,byte_msg):
        self.canUsb.write(byte_msg)

    def terminate(self):
        if self.isRunning() == True:
            self.exit()
            self.wait() 
        super(recievingCanUsbThread,self).terminate()



class canUsb_thread(QThread):
    addNewDevice = pyqtSignal(CANMsg, name='newDeviceFound')
    def __init__(self, serialPort, parent = None):
        super(canUsb_thread,self).__init__(parent)
        self.serialPort = serialPort
        self.address_dict = OrderedDict()
        
    def run(self):
        self.canUsb = serial.Serial(self.serialPort, baudrate=500000,timeout=0)
        self.canUsb.write(CLOSE)
        self.canUsb.write(canbaud+CR)
        self.canUsb.write(OPEN)
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_new_address)
        self.timer.start(1)
        self.exec_()
        
    def terminate(self):
        self.timer.stop()
        if self.isRunning() == True:
            self.exit()
            print('all disconnected')
        super(canUsb_thread,self).terminate()
        
    def add_new_address(self):
        self.timer.stop()
        byte = self.canUsb.read()
#        print(byte)
        if byte is not b'':
            if byte[0] == 116:
                while byte[-1] != 13:
                    byte += self.canUsb.read()
                
                msg = CANMsg()
                msg.id = int(byte[1:4],16)
                if not msg.id in list(self.address_dict.keys()):
                    msg.len = int(byte[4:5],16)
                    byteNew = byte[-3:-1] + b'0'*(16-2*msg.len)
                    list_msg = []
                    for kk in range(0,len(byteNew),2):
                        list_msg += [int(byteNew[kk:kk+2],16)]
                    X = (c_ubyte * 8)(*[c_ubyte(c) for c in list_msg])
#                    print(X)
                    msg.data = X
                    self.addNewDevice.emit(msg)

        self.timer = QTimer()    
        self.timer.timeout.connect(self.add_new_address)
        self.timer.start(1)

ID: 650, Length: 8, Data: 0x004c76166e002229, Timestamp: 3124962997
Received  Log 7738990	38
 
def parsing_can_log(message):
    print('===============================')

    if message.data[0] is 76 and message.data[1] is 1:
        Id = message.id - 640
        return 'Log', Id, '%d\t%d\n'%(int(message.dataAsHexStr()[4:12],16),
                                              message.data[6])
    elif message.data[0] is 35 and message.data[1] is 2:
        if message.data[3] is 5:
            return 'Set Date',message.id-1536, None
        elif message.data[3] is 6:
            return 'Set Time',message.id-1536, None
            
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
    elif message.data[0] is 127:
        return
    
    else:
#        print('Not recognize data: ', message.data[0])
        return 'Log',message.id-1408, None

#        print(message,'\n')
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
            
    ser = serial.Serial(port_can, baudrate=500000,timeout=1)
    
    res = ser.write(CLOSE) # res == 2 tutto ok
    print(res)
    print(ser.inWaiting())

    baudres=ser.write(canbaud+CR)
    res = ser.write(OPEN)
#    ser.write(bytearray(b't60D20100\r')) # switch to operational
    print(ser.inWaiting())
    print(ser.read_until(CR))
              
#    if self.first:
#        self.canUsb.write(b'60D10100')
#        sleep(5)
#        self.canUsb.write(b't60D82301120505010100\r')
#        self.first = False


    
   