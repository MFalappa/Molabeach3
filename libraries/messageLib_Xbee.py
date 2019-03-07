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

from numpy import base_repr
import binascii

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
            self.xbeeForm['rf_data'] = binascii.unhexlify(index_0) + binascii.unhexlify(index_1)
            
            for i in msg[2:]:
                if i is 0:
                   self.xbeeForm['rf_data'] += '\x00'
                else:
                    try:
                        self.xbeeForm['rf_data'] += binascii.unhexlify(base_repr(i,16))
                    except TypeError:
                        self.xbeeForm['rf_data'] += binascii.unhexlify(base_repr(i,16,1))
                
            self.xbeeForm['rf_data'] += (14-len(self.xbeeForm['rf_data']))*'\xff'
            self.xbeeForm['rf_data'] = bytearray(self.xbeeForm['rf_data'])
            self.xbeeForm['options'] = bytearray(b'\x00')
        
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
    
def switch_Lights_Msg(Id, Left, Center, Right, source_address=None):
    """
        Returns a switch light message
        
        Input:
        ------
            Id = int, the id of the device in Hex
            Left = int, 0,1,2,3,4,5,6,7
    """
    if not (Left in [0,1,2,3,4,5,6,7] and 
            Right in [0,1,2,3,4,5,6,7] and
            Center in [0,1,2,3,4,5,6,7]):
        raise ValueError
        
    Msg = XBeeMsg([Id, 1, 7, Left, Center, Right], source_address)
    return Msg

def switch_Noise_Msg(Id, Left, Center, Right, source_address=None):
    """
        Returns a switch light message
        
        Input:
        ------
            Id = int, the id of the device in Hex
            Left = int, 0,1,2,3,4,5,6,7
    """
    if not (Left in [0,1] and 
            Right in [0,1] and
            Center in [0,1]):
        raise ValueError
        
    Msg = XBeeMsg([Id, 1, 8, Left, Center, Right], source_address)
    return Msg

def ReleaseFood_Msg(Id, Right_or_Left, source_address=None):
    """
        Returns a switch light message
    """
    if Right_or_Left:
        Msg = XBeeMsg([Id, 1, 9, 1], source_address)
    else:
        Msg = XBeeMsg([Id, 1, 9, 0], source_address)
    return Msg

def Enable_Active_Poke_Control_Msg(Id,Active_or_Inactive, source_address=None):
    """
        Returns a switch light message
    """
    if Active_or_Inactive:
        Msg = XBeeMsg([Id, 1, 35, 1], source_address)
    else:
        Msg = XBeeMsg([Id, 1, 35,0], source_address)
    return Msg
    
def Start_Stop_Trial_Msg(Id,Start_or_Stop,Stand_Alone=False,
                         source_address=None):
    """
        Returns a switch light message
    """
    if Start_or_Stop:
        Msg = XBeeMsg([Id, 1, 2, int(Stand_Alone)], source_address)
    else:
        Msg = XBeeMsg([Id, 1, 29], source_address)
    return Msg

def Read_RealTime_Msg(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 18], source_address)
    return Msg

#def Get_Bactery_Level_Msg(Id, source_address):
#    Msg = XBeeMsg([Id, 1, 29, 0], source_address)
#    return Msg
    
def Read_Date_Msg(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 6], source_address)
    return Msg  
    
def Read_Time_Msg(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 7], source_address)
    return Msg 

def Msg_Recieved_String(self, msg):
#        print('Recieved dat: ',base_repr(msg.data[0],16),base_repr(msg.data[1],16),
#   set_Max_Trial_Num           base_repr(msg.data[2],16),base_repr(msg.data[3],16),base_repr(msg.data[4],16),
#              base_repr(msg.data[5],16),base_repr(msg.data[6],16),base_repr(msg.data[7],16))
        return
def Switch_to_Operational_State_Msg():
    return None 
    
def set_Mean_Distribution_ITI(Id,mean, source_address=None):
    Msg = XBeeMsg([Id, 1, 27,mean//(16**2),mean%(16**2)], source_address)
    return Msg

def set_Max_Trial_Num(Id,Max, source_address=None):
    Msg = XBeeMsg([Id, 1, 21,Max//(16**6),(Max%(16**6))//16**4,
                   (Max%(16**4))//(16**2),Max%(16**2)], source_address)
    return Msg
    
def set_Trial_Timeout_ms(Id, ms, source_address=None):
    Msg = XBeeMsg([Id, 1, 23,ms//(16**6),(ms%(16**6))//16**4,
                   (ms%(16**4))//(16**2),ms%(16**2)], source_address)
    return Msg
    
def set_Probability_Array(Id,probArray, source_address=None):
    if len(probArray)>20:
        raise ValueError('You can choose at max 20 different probability')
    MsgList = []
    arrayInd = 0
    try:
        while True:
            array = probArray[:3]
            if len(array) == 0:
                raise ValueError
            elif len(array) == 1:
                array = list(array) + [255,255]
            elif len(array) == 2:
                array = list(array) + [255]
            Msg = XBeeMsg([Id, 1, 25,arrayInd,array[0],array[1],array[2]],\
                source_address)
            arrayInd += 3
            MsgList += [Msg]
            probArray = probArray[3:]
    except ValueError:
        pass
    return MsgList
    
def read_Size_Log_and_Prog(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 36], source_address)
    return Msg

def read_External_EEPROM(Id,Index, source_address=None):
    Msg = XBeeMsg([Id, 1, 20,Index//(16**2),Index%(16**2)], source_address)
    return Msg


if __name__ == "__main__":
    Id = 127
    source_address = bytearray(b'\x00\x13\xa2\x00\x40\xbe\x57\xab')
    Left,Right,Center = 1,1,1
    Active_or_Inactive=0
    text = ''
    msg = switch_Lights_Msg(Id, Left, Center, Right,source_address)
    string = binascii.hexlify(msg.byteArrayToSend())
    text += 'Switch lights on (three lights switched to blue)\t'
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=switch_Noise_Msg(Id, 1, 0, Right,source_address)
    text += 'Switch noise on (left and right only)\t'
    string = binascii.hexlify(msg.byteArrayToSend())
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=read_External_EEPROM(Id,100,source_address)
    string = binascii.hexlify(msg.byteArrayToSend())
    text += 'Read external eeprom\t'
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    
    text = text.rstrip('\t')
    text += '\n'
    msg=read_Size_Log_and_Prog(Id,source_address)
    text += 'Read size log and prog\t'
    string = binascii.hexlify(msg.byteArrayToSend())
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msgList=set_Probability_Array(Id,[100,90,80,70,60,50,40,30,20,10,0],source_address)
    for msg in msgList:
        text += 'Set prob. array from 100% to 0%\t'
        string = binascii.hexlify(msg.byteArrayToSend())
        for k in range(0,len(string),2):
            text += string[k:k+2] + '\t'
        text = text.rstrip('\t')
        text += '\n'
    msg=set_Trial_Timeout_ms(Id, 1100, source_address)
    text += 'Timeout 1100 ms\t'
    string = binascii.hexlify(msg.byteArrayToSend())
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=set_Max_Trial_Num(Id, 9999,source_address)
    string = binascii.hexlify(msg.byteArrayToSend())
    text += 'trial max number 9999\t'
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=set_Mean_Distribution_ITI(Id,47,source_address)
    msg=Read_Date_Msg(Id, source_address)
    text += 'Read Date\t'
    string = binascii.hexlify(msg.byteArrayToSend())
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=Read_RealTime_Msg(Id, source_address)
    text += 'read real time\t'
    string = binascii.hexlify(msg.byteArrayToSend())
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=Start_Stop_Trial_Msg(Id,1,Stand_Alone=False,source_address=source_address)
    string = binascii.hexlify(msg.byteArrayToSend())
    text += 'Start trial (NON stand-alone)\t'
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=Enable_Active_Poke_Control_Msg(Id,Active_or_Inactive,source_address)
    string = binascii.hexlify(msg.byteArrayToSend())
    text += 'Deactivate Active Poke controle\t'
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    msg=ReleaseFood_Msg(Id,1,source_address)
    text += 'Release food right\t'
    string = binascii.hexlify(msg.byteArrayToSend())
    for k in range(0,len(string),2):
        text += string[k:k+2] + '\t'
    text = text.rstrip('\t')
    text += '\n'
    fh = open('C:\\Users\ebalzani\IIT\Microsystems\\wifi_msg_example.txt','w')
    fh.write(text)
    fh.close()
#    import canportreader
#    import pycanusb
#    from time import clock,sleep
#    t0=clock()  
#    Op=Switch_to_Operational_State_Msg()
#    Msg = switch_Lights_Msg(680,1,2,3)
#    Msg_2 = ReleaseFood_Msg(680,1)
#    Msg_3 = ReleaseFood_Msg(680,2)
#    Msg_4 = Enable_Active_Poke_Control_Msg(680,1)
#    Msg_5 = Start_Stop_Trial_Msg(680,0)
#    Msg_6 = Read_RealTime_Msg(680)
#    Msg_7 = Get_Bactery_Level_Msg(680)
#    Msg_8 = Read_Date_Msg(680)
#    Msg_9 = Read_Time_Msg(680)
#    t1=clock()
#    print t1-t0
#    canusb = pycanusb.CanUSB(bitrate='500')
#    sleep(1)
#    canReader = canportreader.CanPortReader(canusb, Msg_Recieved_String,sampleRate=10)
#    sleep(1)
#    canusb.write(Op)
#    sleep(5)
#    canusb.write(Msg)
#    sleep(0.1)
#    canusb.write(Msg_2)
#    sleep(2)
#    canusb.write(switch_Lights_Msg(680,4,5,6))
#    sleep(2)
#    canusb.write(switch_Lights_Msg(680,0,0,0))
#    sleep(0.001)
#    canusb.write(switch_Noise_Msg(680,0,1,1))
#    sleep(1)
#    canusb.write(switch_Noise_Msg(680,0,0,0))
