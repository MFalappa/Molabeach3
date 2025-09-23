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
from numpy import binary_repr
from serial.tools import list_ports
from ctypes import (c_uint,c_ubyte,Structure)

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
        to_send = bytes(hex(self.id)[2:],'utf-8')
        
        if to_send== b'0':
            to_send = b'000'
            
        x = (x + to_send + bytes(hex(self.len)[2:],'utf-8')+
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
    received = pyqtSignal(CANMsg, name='canMsgReceived')
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
        self.received.emit(msg) 
        
    def run(self):
        self.canUsb = serial.Serial(self.serialPort, baudrate=500000,timeout=0)
        self.canUsb.write(OPEN)
        self.canUsb.write(CLOSE)
        self.canUsb.write(canbaud+CR)
        self.canUsb.write(OPEN)
        
        self.setPriority(QThread.HighestPriority)
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
                if msg.len == 8:
                    byteNew = byte[5:-1]
                else:
                    byteNew = byte[-3:-1] + b'0'*(16-2*msg.len)
                
                list_msg = []
                for kk in range(0,len(byteNew),2):
                    list_msg += [int(byteNew[kk:kk+2],16)]
                X = (c_ubyte * 8)(*[c_ubyte(c) for c in list_msg])
#                print('====',list_msg)
                msg.data = X
                self.received.emit(msg)

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



def parsing_can_log(message,pc_id='0001'):
    if message.data[0] is 76: # LOG MESSAGES
        Id = message.id - 640
        return 'Log', Id, '%d\t%d\n'%(int(message.dataAsHexStr()[4:12],16),message.data[6])#'%d\t%d\t%d\t%s\n'%(int(message.dataAsHexStr()[4:12],16),
                                              #message.data[6],message.data[7],message.dataAsHexStr())
    elif  message.data[0] is 0:
        Id = message.id - 1792
        return 'Log', Id, '%d\t%d\t%d\t%s\n'%(message.data[0],
                                              message.data[0],
                                              message.data[0],
                                              message.dataAsHexStr())
    
    elif message.data[0] is 67: # READ INFORMATION MESSAGES
        Id = message.id - 1408
        if message.data[1] is 1: 
            if message.data[3] is 48: # IC2 STATUS
                ic2_status = binary_repr(message.data[4])
                return 'Info', Id, 'IC2 Status %s\n'%ic2_status   
            elif message.data[3] is 65:
                time = int(message.dataAsHexStr()[-2:]+message.dataAsHexStr()[-4:-2]+message.dataAsHexStr()[-6:-4]+message.dataAsHexStr()[-8:-6],16)
                return 'Timer',Id, '%d\t38\n'%time
            
        
        if message.data[1] is 10: # FIRMWARE
            if message.data[3] is 00:
                firmware = binascii.unhexlify(message.dataAsHexStr()[-8:]).decode()
                return 'Info', Id, 'Firmware version %s\n'%firmware
           
        if message.data[1] is 2:
            if message.data[3] is 5: # DATE MESSAGE 
                return 'Info', Id, 'Date %d-%d-%d\n'%(message.data[4],
                                                      message.data[5],
                                                      message.data[6])
            elif message.data[3] is 6: # Time
                return 'Info', Id, 'Time %d:%d:%d\n'%(message.data[7],
                                                      message.data[6],
                                                      message.data[5])
                                                      
                                                      
            elif message.data[3] is 1:
                return 'Changed_address', Id, message.data[4]
            elif message.data[3] is 16: # threshold sensor left
                return 'Info', Id, 'Poke Threshold Left %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 17: # threshold sensor mid
                return 'Info', Id, 'Poke Threshold Mid %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 18: # threshold sensor right
                return 'Info', Id, 'Poke Threshold Right %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 21: # bactery level
                return 'Info', Id, 'Bactery Level %d%%\n'%((message.data[5]*16**2+message.data[4]))
            elif message.data[3] is 37: # Size program
                return 'Info', Id, 'Program Size %d\n'%(message.data[5]*16**2+message.data[4])

            elif message.data[3] is 32: # subject
                return 'Info', Id, 'Subject %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 33: # exp id
                return 'Info', Id, 'Exp Id %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 34: # phase
                return 'Info', Id, 'Phase %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 35: # phase id
                return 'Info', Id, 'Box Id %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 36: # Trial Num
                return 'Info', Id, 'Trial Number %d\n'%(message.data[5]*16**2+message.data[4])
            elif message.data[3] is 80: # max trial
                return 'Info', Id, 'Trial Max Number %d\n'%(message.data[6]*16**4+message.data[5]*16**2+message.data[4])
            elif message.data[3] is 81: # timeout trial
                return 'Info', Id, 'Trial Timeout %d\n'%(message.data[6]*16**4+message.data[5]*16**2+message.data[4])
            elif message.data[3] is 82: # sPRb array
                return 'Info', Id, 'Probablity Array Index %d Value %d, %d, %d\n'%(message.data[4],message.data[5],message.data[6],message.data[7])
            elif message.data[3] is 83: # mean distribution
                return 'Info', Id, 'Mean distributoin %d\n'%(message.data[5]*16**2+message.data[4])
    
    elif message.data[0] is 128:
          Id = message.id - 1408
          return 'Info',Id, 'Message send is wrong!'
          
          
    elif message.data[0] is 96: # and message.data[1] is 2:
        Id = message.id - 1408
        
        if message.data[1] is 1:
            if message.data[3] is 0: #relise pellet
                return 'Info', Id, 'Release pellet left'
            elif message.data[3] is 1: #pellet right
                return 'Info', Id, 'Release pellet right'
            elif message.data[3] is 2:
                return 'Info', Id, 'Sound message'
            elif message.data[3] is 5:
                return 'Info', Id, 'RGB message'
            elif message.data[3] is 48:
                return 'Info', Id, 'Request I2C status'
            elif message.data[3] is 65:
                return 'Info',Id, 'Request real trial time'
            elif message.data[3] is 64: # stand alone
                return 'Info', Id, 'Started stand alone'
            elif message.data[3] is 66: # FIRMWARE
                return 'Info', Id, 'Stopped stand alone'

        elif message.data[1] is 2:
            if message.data[3] is 1:
                return 'Info', Id,'Change address done'
            elif message.data[3] is 5:
                return 'Info',Id, 'Date set'
            elif message.data[3] is 6:
                return 'Info',Id, 'Time set'
            elif message.data[3] is 16:
                return 'Info', Id,'Threshold left set'
            elif message.data[3] is 17:
                return 'Info', Id,'Threshold center set'
            elif message.data[3] is 18:
                return 'Info', Id,'Threshold right set'
            elif message.data[3] is 20:
                return 'Info', Id,'Sound mode set'
            elif message.data[3] is 32:
                return 'Info', Id,'Subject number set'
            elif message.data[3] is 33:
                return 'Info', Id,'Experiment id set'
            elif message.data[3] is 34:
                return 'Info', Id,'Phase number set'
            elif message.data[3] is 35:
                return 'Info', Id,'Box id set'
            elif message.data[3] is 36:
                return 'Info', Id,'RTrial number set'
            elif message.data[3] is 80:
                return 'Info', Id,'Trial max number set'
            elif message.data[3] is 81:
                return 'Info', Id,'Trial timeout (ms) set'    
            elif message.data[3] is 83:
                return 'Info', Id,'Mean distribution set'
                        
        elif message.data[1] is 10: # FIRMWARE
            if message.data[3] is 00:
                return 'Info', Id, 'Request Firmware version'
                
    elif message.data[0] is 35: # Write INFORMATION MESSAGES
        Id = message.id - 1536
        
        if message.data[1] is 2:
            if message.data[3] is 5: # DATE MESSAGE 
                return 'Info', Id, 'Request set date'
            elif message.data[3] is 6: # Time
                return 'Info', Id, 'Request set time'
            elif message.data[3] is 1:
                return 'Info',Id, 'Request changed address'
            elif message.data[3] is 16: # threshold sensor left
                return 'Info', Id, 'Request set Poke Threshold Left'
            elif message.data[3] is 17: # threshold sensor mid
                return 'Info', Id, 'Request set Poke Threshold Mid'
            elif message.data[3] is 18: # threshold sensor right
                return 'Info', Id, 'Request set Poke Threshold Right'
            elif message.data[3] is 21: # bactery level
                return 'Info', Id, 'Request set Bactery Level'
            elif message.data[3] is 37: # Size program
                return 'Info', Id, 'Request set Program Size'
            elif message.data[3] is 32: # subject
                return 'Info', Id, 'Request set Subject id'
            elif message.data[3] is 33: # exp id
                return 'Info', Id, 'Request set Exp Id'
            elif message.data[3] is 34: # phase
                return 'Info', Id, 'Request set Phase'
            elif message.data[3] is 35: # phase id
                return 'Info', Id, 'Request set Box Id'
            elif message.data[3] is 36: # Trial Num
                return 'Info', Id, 'Request set Trial Number'
            elif message.data[3] is 80: # max trial
                return 'Info', Id, 'Request set Trial Max Number'
            elif message.data[3] is 81: # timeout trial
                return 'Info', Id, 'Request Trial Timeout'
            elif message.data[3] is 82: # sPRb array
                return 'Info', Id, 'Request set Probablity Array Index'
            elif message.data[3] is 83: # mean distribution
                return 'Info', Id, 'Request set Mean distributoin'
                
        elif message.data[1] is 1:
            if message.data[3] is 0:
                return 'Info', Id, 'Request release pellet left'
            elif message.data[3] is 1:
                return 'Info', Id, 'Request release pellet right'
            elif message.data[3] is 2:
                return 'Info', Id, 'Request a/dectivate sound'
            elif message.data[3] is 5:
                return 'Info', Id, 'Request rgb manage'
            elif message.data[3] is 64:
                return 'Info', Id, 'Request start stand alone'
            elif message.data[3] is 66:
                return 'Info', Id, 'Request stop stand alone'
                
    elif message.data[0] is 64:
        Id = message.id - 1536
        if message.data[1] is 1: 
            if message.data[3] is 48: # IC2 STATUS
                return 'Info', Id, 'Request get IC2 Status' 
            elif message.data[3] is 65:
                return 'Info',Id, 'Request get real Time'
            
        
        if message.data[1] is 10: # FIRMWARE
            if message.data[3] is 00:
                return 'Info', Id, 'Request get Firmware version'
        
        
        if message.data[1] is 2:
            if message.data[3] is 5: # DATE MESSAGE 
                return 'Info', Id, 'Request get Date' 
            elif message.data[3] is 6: # Time
                return 'Info', Id, 'Request get Time' 
                                                      
                                                      
            elif message.data[3] is 1:
                return 'Request get Changed address'
            elif message.data[3] is 16: # threshold sensor left
                return 'Info', Id, 'Request get Poke Threshold Left'
            elif message.data[3] is 17: # threshold sensor mid
                return 'Info', Id, 'Request get Poke Threshold Mid'
            elif message.data[3] is 18: # threshold sensor right
                return 'Info', Id, 'Request get Poke Threshold Right'
            elif message.data[3] is 21: # bactery level
                return 'Info', Id, 'Request get Bactery Level'
            elif message.data[3] is 37: # Size program
                return 'Info', Id, 'Request get Program Size'

            elif message.data[3] is 32: # subject
                return 'Info', Id, 'Request get Subject'
            elif message.data[3] is 33: # exp id
                return 'Info', Id, 'Request get Exp Id'
            elif message.data[3] is 34: # phase
                return 'Info', Id, 'Request get Phase'
            elif message.data[3] is 35: # phase id
                return 'Info', Id, 'Request get Box Id'
            elif message.data[3] is 36: # Trial Num
                return 'Info', Id, 'Request get Trial Number'
            elif message.data[3] is 80: # max trial
                return 'Info', Id, 'Request get Trial Max Number'
            elif message.data[3] is 81: # timeout trial
                return 'Info', Id, 'Request get Trial Timeout'
            elif message.data[3] is 82: # sPRb array
                return 'Info', Id, 'Request get Probablity Array Index'
            elif message.data[3] is 83: # mean distribution
                return 'Info', Id, 'Request get Mean distributoin'
            
    elif message.data[0] is 5:
        Id = message.id - 1792
        return 'Keep alive', Id, 'Operational mode'
    
    elif message.data[0] is 127:
        Id = message.id - 1792
        return 'Keep alive', Id, 'Pre-operational mode'
        
    else:
        return 'Unknown message',message.id,'bk'
  

    
        
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


    
   