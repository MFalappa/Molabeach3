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
import _winreg as winreg
import itertools
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Modify_Dataset_GUI import OrderedDict
from xbee import *
import binascii

def enumerate_serial_ports():
    """ Uses the Win32 registry to return a iterator of serial 
        (COM) ports existing on this computer.


    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise IterationError

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
#            print 'comval',val
            yield (str(val[1]), str(val[0]))
        except EnvironmentError:
            break

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
        print 'Connected'
    def terminate(self):
        if self.isRunning() == True:
            self._xBee.halt()
            self.exit()
            self.wait() 
            print 'all disconnected'
        super(recievingXBeeThread,self).terminate()
        print 'thread reciever terminated '

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
            if not ID in self.address_dict.keys():
                self.address_dict[ID] = msg['source_addr']
                thisdict = {ID: msg['source_addr']}
                self.addNewDevice.emit(thisdict)
        except KeyError:
            pass

def parsing_can_log(message):
#    print 'Parsing data 0:', message.data[0]
    print message.data[0], message.data[1]
    if message.data[0] is 76 and message.data[1] is 1:
        #print 'Log Msg id: ',message.id
        Id = message.id - 640
#        print 'PARSING LOG'
        return 'Log', Id, '%d\t%d\n'%(int(message.dataAsHexStr()[4:12],16),
                                              message.data[6])
    elif message.data[0] is 96 and message.data[1] is 2:
        if message.data[3] is 5:
            return 'Set Date',message.id-1408, None
        elif message.data[3] is 6:
            return 'Set Time',message.id-1408, None
            
    elif message.data[0] is 96:
#        print 'parsing', message
#        print message.id
#        print '\n\n\n'
        Id = message.id - 1408
#        print Id
        return Id, None
    elif message.data[0] == 67 and message.data[1] is 1 and\
        message.data[3] is 65:
        Id = message.id - 1408
        time = int(message.dataAsHexStr()[-2:]+message.dataAsHexStr()[-4:-2]+
                message.dataAsHexStr()[-6:-4]+message.dataAsHexStr()[-8:-6],16)
        return 'Timer',Id, '%d\t38\n'%time
    
    elif message.data[0] is 67 and message.data[1] is 2:
        print 'Entered in time settings',message.data[3]
        Id = message.id - 1408
        if message.data[3] == 5:
            return 'Date',Id,'%d-%d-%d'%(message.data[4],message.data[5],
                                   message.data[6])
        elif message.data[3] == 6:
            return 'Time',Id, '%d:%d:%d'%(message.data[7],message.data[6],
                                   message.data[5])
#    elif message.data[0] is 
    else:
#        print 'Not recognize data'
#        print message,'\n'
        raise ValueError
    
def parsing_XBee_log(message):
    try:
        PAYLOAD = binascii.hexlify(message['rf_data'])
        print 'PAYLOAD', PAYLOAD
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