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
from numpy import base_repr, binary_repr
import binascii
import datetime

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
    
    def has_key(self,key):
        return key in self.xbeeForm.keys()
        
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
        print self.xbeeForm
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
    

def XbeeMsg_from_Bytearray(byte_msg):
#    start = binascii.hexlify(byte_msg[0:1])
#    length = binascii.hexlify(byte_msg[1:3])
#    API_ID_Mes = binascii.hexlify(byte_msg[3:4])
#    Count_Mes = binascii.hexlify(byte_msg[4:5])
    source_address = byte_msg[5:13]
#    options = binascii.hexlify(byte_msg[13:14])
    rf_data = binascii.hexlify(byte_msg[14:28])
#    cksum = binascii.hexlify(byte_msg[28:29])
#    print rf_data,cksum
    msg_list = [int(rf_data[:4],16), int(rf_data[4:8],16)]
    for i in xrange(8,20,2):
        if int(rf_data[i:i+2],16) is 255:
            break
        msg_list += [int(rf_data[i:i+2],16)]
#    print msg_list
    return XBeeMsg(msg_list,source_address)
    
#Matteo message======================================
def set_subject(Id,sbj_num,source_address=None,MODE=0):
    if MODE:
        return set_subject_Xbee(Id,sbj_num,source_address)
    Data = [35,2,18,32,sbj_num,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    

def set_exp_id(Id,exp_num,source_address=None,MODE=0):
    if MODE:
        return set_exp_id_xbee(Id,exp_num,source_address)
    Data = [35,2,18,33,exp_num,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def set_phase(Id,phase,source_address=None,MODE=0):
    if MODE:
        return set_phase_xbee(Id,phase,source_address)
    Data = [35,2,18,34,phase,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_box_id(Id,new_id,source_address=None,MODE=0):
    if MODE:
        return set_box_id_xbee(Id,new_id,source_address)
    Data = [35,2,18,35,new_id,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_threshold_sensor(Id,l_c_r,thres,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No threshold sensor message implemented for xbee'
    if l_c_r == 'l':
        code = 16
    elif l_c_r == 'c':
        code = 17
    elif l_c_r == 'r':
        code = 18
    Data = [35,2,18,code,thres%(16**2),thres//16**2,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_noise_freq(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No nosie frequency message implemented for xbee'
    
    Data = [64,2,18,20,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_noise_freq(Id,mod,freq,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No nosie frequency message implemented for xbee'
    if mod < 0 or mod > 1:
        raise ValueError, 'mod must be 0 or 1'
#    if freq < 1 or freq > 255:
#        raise ValueError, 'freq must be between 1 and 255'
    Data = [35,2,18,20,mod,freq%(16**2),freq//16**2,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
#Matteo message======================================   
    
def switch_Lights_Msg(Id,Left,Center,Right,source_address=None, MODE=0):
    """
        Returns a switch light message
        
        Input:
        ------
            Id = int, the id of the device in Hex
            Left = int, 0,1,2,3,4,5,6,7
    """
    if MODE:
        return switch_Lights_Msg_Xbee(Id,Left,Center,Right,source_address)
    if not (Left in [0,1,2,3,4,5,6,7] and 
            Right in [0,1,2,3,4,5,6,7] and
            Center in [0,1,2,3,4,5,6,7]):
        raise ValueError
        
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data  = [35,1,18,5,Left,Center,Right,0] # Decimal based of  [0x23,0x1,0x12,0x5,0xLeft,0xCenter,0xRight,0x0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def switch_Noise_Msg(Id,Left,Center,Right,source_address=None, MODE=0):
    """
        Returns a switch light message
        
        Input:
        ------
            Id = int, the id of the device in Hex
            Left = int, 0,1,2,3,4,5,6,7
    """
    if MODE:
        return switch_Noise_Msg_Xbee(Id,Left,Center,Right,source_address)
    if not (Left in [0,1] and 
            Right in [0,1] and
            Center in [0,1]):
        raise ValueError
        
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data = [35,1,18,2,Left,Center,Right,0] # Decimal based of  [0x23,0x1,0x12,0x5,0xLeft,0xCenter,0xRight,0x0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def ReleaseFood_Msg(Id,Right_or_Left,source_address=None, MODE=0):
    """
        Returns a release food
    """
    if MODE:
        return ReleaseFood_Msg_Xbee(Id,Right_or_Left,source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    if not Right_or_Left:
        Data = [35,1,18,0,0,0,0,0] 
    else:
        Data = [35,1,18,1,0,0,0,0] 
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def Enable_Active_Poke_Control_Msg(Id,Active_or_Inactive,source_address=None,
                                   MODE=0):
    """
        Returns a switch light message
    """
    if MODE:
        return Enable_Active_Poke_Control_Msg_Xbee(Id,Active_or_Inactive,
                                                   source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    if Active_or_Inactive:
        Active_or_Inactive = 1
    else:
        Active_or_Inactive = 0
    Data = [35,1,18,36,Active_or_Inactive,0,0,0] 
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg
    
def Start_Stop_Trial_Msg(Id,Start_or_Stop,Stand_Alone=False,
                         source_address=None, MODE=0):
    """
        Returns a switch light message
    """
    if MODE:
        return Start_Stop_Trial_Msg_Xbee(Id,Start_or_Stop,Stand_Alone=Stand_Alone,
                         source_address=source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    if Start_or_Stop:
        Data = [35,1,18,64,int(Stand_Alone),0,0,0]
    else:
        Data = [35,1,18,66,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg
    
def Read_RealTime_Msg(Id,source_address=None, MODE=0):
    if MODE:
        return Read_RealTime_Msg_Xbee(Id, source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data = [64,1,18,65,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg
    
def Get_Bactery_Level_Msg(Id,source_address=None, MODE=0):
    if MODE:
        return get_bactery_level_Xbee(Id,source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data = [64,2,18,21,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg
    
def Read_Date_Msg(Id,source_address=None, MODE=0):
    if MODE:
        return Read_Date_Msg_Xbee(Id,source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data = [64,2,18,5,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def Set_Date_Msg(Id,day,month,year,week_day,source_address=None, MODE=0):
    if MODE:
        raise ValueError, 'Data can be set only via CAN bus'
    if year > 99 or week_day > 7:
        raise ValueError, 'Year must be between 0 and 99 and week day must be a positive integer between 1 and 7'
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data = [35,2,18,5,day,month,year,week_day]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg


def Read_Time_Msg(Id,source_address=None, MODE=0):
    if MODE:
        return Read_Time_Msg_Xbee(Id,source_address)
    Msg = pycanusb.CANMsg()
    
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data = [64,2,18,6,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def Set_Time_Msg(Id,millisec,second,minute,hour,source_address=None, MODE=0):
    if MODE:
        raise ValueError, 'Time can be set only via CAN bus'
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = range(8)
    Data = [35,2,18,6,millisec,second,minute,hour]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def set_current_datetime(Id,source_address=None):
    date = datetime.datetime.now()
    Msg = Set_Date_Msg(Id,date.day,date.month,date.year-2000,date.weekday()+1,
                       source_address=source_address)
    Msg2 = Set_Time_Msg(Id,date.microsecond//10000,date.second,date.minute,
                        date.hour,source_address=source_address)
    return [Msg,Msg2]
    
def Msg_Recieved_String(self, msg,source_address=None):
#        print('Recieved dat: ',base_repr(msg.data[0],16),base_repr(msg.data[1],16),
#   set_Max_Trial_Num           base_repr(msg.data[2],16),base_repr(msg.data[3],16),base_repr(msg.data[4],16),
#              base_repr(msg.data[5],16),base_repr(msg.data[6],16),base_repr(msg.data[7],16))
        return
def Switch_to_Operational_State_Msg(MODE=0):
    if MODE:
        return Switch_to_Operational_State_Msg_Xbee()
    Msg = pycanusb.CANMsg()
    Msg.id = 0
    Msg.len = 2
    Data = [1,0]
    for ind in [0,1]:
        Msg.data[ind] = Data[ind]
    return Msg 
    
def set_Mean_Distribution_ITI(Id,mean,source_address=None, MODE=0):
    if MODE:
        return set_Mean_Distribution_ITI_Xbee(Id,mean,source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,83,mean%16**2,(mean%16**4)//16**2,
            (mean%16**6)//16**4,mean//16**6]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def set_Max_Trial_Num(Id,Max,source_address=None, MODE=0):
    if MODE:
        return set_Max_Trial_Num_Xbee(Id,Max,source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,80,Max%16**2,(Max%16**4)//16**2,
            (Max%16**6)//16**4,Max//16**6]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_Trial_Timeout_ms(Id,ms,source_address=None, MODE=0):
    if MODE:
        return set_Trial_Timeout_ms_Xbee(Id,ms,source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,81,int(ms)%(16**2),int(ms)//(16**2),0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_Probability_Array(Id,probArray,source_address=None,MODE=0):
    if MODE:
        return set_Probability_Array_Xbee(Id,probArray,source_address)
    if len(probArray)>20:
        raise ValueError,'You can choose at max 20 different probability'
    MsgList = []
    arrayInd = 0
    try:
        while True:
            array = probArray[:3]
            if len(array) == 0:
                raise ValueError
            elif len(array) == 1:
                array = list(array) + [0,0]
            elif len(array) == 2:
                array = list(array) + [0]
            Msg = pycanusb.CANMsg()
            Msg.id = Id +1536
            Msg.len = 8
            Data = [35,2,18,82,arrayInd,array[0],array[1],array[2]]
            for ind in range(8):
                Msg.data[ind] = Data[ind]
            arrayInd += 3
            MsgList += [Msg]
            probArray = probArray[3:]
    except ValueError:
        pass
    return MsgList

def get_ic2_Status(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No ic2 status message implemented for xbee'
    Data = [64,1,18,48,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_threshold_sensor(Id,l_c_r,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No threshold sensor message implemented for xbee'
    if l_c_r == 'l':
        code = 16
    elif l_c_r == 'c':
        code = 17
    elif l_c_r == 'r':
        code = 18
    Data = [64,2,18,code,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_subject(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No subject message implemented for xbee'
    Data = [64,2,18,32,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_exp_id(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No subject message implemented for xbee'
    Data = [64,2,18,33,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_phase(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No subject message implemented for xbee'
    Data = [64,2,18,34,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_box_id(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'No subject message implemented for xbee'
    Data = [64,2,18,35,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    

def get_trial_number(Id,source_address=None,MODE=0):
    if MODE:
        return get_trial_number_Xbee(Id,source_address)
    Data = [64,2,18,36,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def get_trial_max_number(Id,source_address=None,MODE=0):
    if MODE:
        return get_trial_max_number_Xbee(Id,source_address)
    Data = [64,2,18,80,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg


def get_trial_timeout(Id,source_address=None,MODE=0):
    if MODE:
        return get_trial_timeout_Xbee(Id,source_address=source_address)
    Data = [64,2,18,81,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_firmware_version(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError, 'Not Yet implemented for Xbee'
    Data = [64,10,16,0,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_mean_distribution(Id,source_address=None,MODE=0):
    if MODE:
        return get_mean_distribution_Xbee(Id,source_address=source_address)
    Data = [64,2,18,83,0,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_Probability_Array(Id,index,source_address=None,MODE=0):
    if index > 17:
        raise ValueError, 'Index between 0 and 17'
    if MODE:
        return get_probability_array_Xbee(Id,index,source_address)
    Data = [64,2,18,82,index,0,0,0]
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Start_Trial(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    Data = [35,2,18,96,row,0,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg 
    
def program_Reset_Trigger(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,8,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_event_Trigger(Id,row,L_M_R):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,33,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,34,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,35,0,0]
    else:
        raise ValueError,'L_M_R must contain a string with \'L\'/\'M\'/\'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_event_Poke(Id,row,L_M_R):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,30,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,31,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,32,0,0]
    else:
        raise ValueError,'L_M_R must contain a string with \'L\'/\'M\'/\'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_Start_Trial_Timer(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,7,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_if_Random_MC(Id,row,Index):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,50,Index,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Light_On(Id,row,L_M_R,color):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if color not in range(1,8):
        raise ValueError,'color must be an integer between 1 and 7!'
    if L_M_R == 'L':
        Data = [35,2,18,96,row,10,color,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,12,color,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,14,color,0]
    else:
        raise ValueError,'L_M_R must contain a string with \'L\'/\'M\'/\'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_manage_RGB(Id,row,color_L=0,color_M=0,color_R=0):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,9,color_L+16*color_M,color_R]
    if color_L not in range(0,8):
        raise ValueError,'color must be an integer between 0 and 7!'
    if color_M not in range(0,8):
        raise ValueError,'color must be an integer between 0 and 7!'
    if color_R not in range(0,8):
        raise ValueError,'color must be an integer between 0 and 7!'
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_Fix_Delay(Id,row,ms):
    """
        ms = int, millisec of delay
    """
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,40,ms%(16**2),ms//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Light_Off(Id,row,L_M_R):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,11,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,13,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,15,0,0]
    else:
        raise ValueError,'L_M_R must contain a string with \'L\'/\'M\'/\'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Loop_Local_Trial(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,3,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_Trigger(Id,row,L_M_R):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,57,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,58,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,59,0,0]
    else:
        raise ValueError,'L_M_R must be \'L\',\'M\' or \'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Release_Pellet(Id,row,L_R):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_R == 'L':
        Data = [35,2,18,96,row,80,0,0]
    elif L_R == 'R':
        Data = [35,2,18,96,row,81,0,0]
    else:
        raise ValueError,'L_R must be \'L\' or \'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_End_Local_Trial(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,5,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_End_Block_If(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,2,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_End_Loop_Local_Trial(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,4,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_Else_Block_If(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,6,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg


def program_Fixed_Delay_ITI(Id,row,ms):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if not (type(ms) is int and ms>10):
        raise ValueError,'ms must be an iteger quantity >10'
    Data = [35,2,18,96,row,41,ms%(16**2),ms//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Random_Delay_ITI(Id,row,sec):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if not (type(sec) is int and sec >= 0):
        raise ValueError,'sec must be an iteger quantity >=0'
    Data = [35,2,18,96,row,42,sec%(16**2),sec//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_End_Trial(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,1,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg 

def program_Counter_Init(Id,row,counterInd,Ind0):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,70,counterInd,Ind0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
def program_Counter_Inc(Id,row,counterInd):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,71,counterInd,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_If_Light(Id,row,L_M_R):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,63,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,64,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,65,0,0]
    else:
        raise ValueError,'L_R must be \'L\', \'M\' or \'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
def program_If_Presence(Id,row,L_M_R):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,60,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,61,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,62,0,0]
    else:
        raise ValueError,'L_R must be \'L\', \'M\' or \'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_Counter(Id,row,G_L_E,counter0,counter1):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if G_L_E == 'G':
        Data = [35,2,18,96,row,66,counter0,counter1]
    elif G_L_E == 'L':
        Data = [35,2,18,96,row,67,counter0,counter1]
    elif G_L_E == 'E':
        Data = [35,2,18,96,row,68,counter0,counter1]
    else:
        raise ValueError,'L_R must be \'L\', \'M\' or \'R\''
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_Random_Mc_Step(Id,row,index):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,52,index,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Dummy_Test(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,82,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def read_Size_Log_and_Prog(Id, source_address=None, MODE=0):
    if MODE:
        return read_Size_Log_and_Prog_Xbee(Id, source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [64,2,18,37,0,0,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
def read_External_EEPROM(Id,Index,source_address=None, MODE=0):
    if MODE:
        return read_External_EEPROM_Xbee(Id, Index, source_address)
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [64,2,18,4,0,0,Index%(16**2),Index//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def log_ITI_end_Msg(Id, row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,43,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Noise_On(Id, row, left, center, right):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if left:
        Data = [35,2,18,96,row,16,0,0]
    elif center:
        Data = [35,2,18,96,row,18,0,0]
    elif right:
        Data = [35,2,18,96,row,20,0,0]
    else:
        raise ValueError,'At least one side must be indicated'
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Noise_Off(Id, row, left, center, right):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if left:
        Data = [35,2,18,96,row,17,0,0]
    elif center:
        Data = [35,2,18,96,row,19,0,0]
    elif right:
        Data = [35,2,18,96,row,21,0,0]
    else:
        raise ValueError,'At least one side must be indicated'
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_TimoutReached(Id,row):
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,69,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
  
def program_TTL(Id,row,pin,duration):
    """
        Description:
        ============
            - pin : numero in binario rappresenta quali pin sono attivi 
                    esempio : input 3 = 1100 -> attivo il primo e secondo pin
            - duration : range (10,250), step di 10, durata in ms del segnale 
                        alto a 5V
    """
    Msg = pycanusb.CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if pin < 1 or pin >= 15:
        raise ValueError, 'Pin must be an INT between 1 and 15'
    print 'duration',duration 
    if duration < 1 or duration > 250:
        raise ValueError, 'Duration must be in the range of [1,250]'
    elif duration != 1 and duration % 10 != 0:
        raise ValueError, 'Duration must be a multiple of 10'
    Data = [35,2,18,96,row,83,pin,duration]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg


#==============================================================================
#   XBee messages
#==============================================================================
def switch_Lights_Msg_Xbee(Id, Left, Center, Right, source_address=None):
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
    return Msg.byteArrayToSend()

def switch_Noise_Msg_Xbee(Id, Left, Center, Right, source_address=None):
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
    return Msg.byteArrayToSend()

def ReleaseFood_Msg_Xbee(Id, Right_or_Left, source_address=None):
    """
        Returns a switch light message
    """
    if Right_or_Left:
        Msg = XBeeMsg([Id, 1, 9, 1], source_address)
    else:
        Msg = XBeeMsg([Id, 1, 9, 0], source_address)
    return Msg.byteArrayToSend()

def Enable_Active_Poke_Control_Msg_Xbee(Id,Active_or_Inactive, source_address=None):
    """
        Returns a switch light message
    """
    if Active_or_Inactive:
        Msg = XBeeMsg([Id, 1, 35, 1], source_address)
    else:
        Msg = XBeeMsg([Id, 1, 35,0], source_address)
    return Msg.byteArrayToSend()
    
def Start_Stop_Trial_Msg_Xbee(Id,Start_or_Stop,Stand_Alone=False,
                         source_address=None):
    """
        Returns a switch light message
    """
    if Start_or_Stop:
        Msg = XBeeMsg([Id, 1, 2, int(Stand_Alone)], source_address)
    else:
        Msg = XBeeMsg([Id, 1, 29], source_address)
    return Msg.byteArrayToSend()

def Read_RealTime_Msg_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 18], source_address)
    return Msg.byteArrayToSend()

#def Get_Bactery_Level_Msg(Id, source_address):
#    Msg = XBeeMsg([Id, 1, 29, 0], source_address)
#    return Msg
    
def Read_Date_Msg_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 6], source_address)
    return Msg.byteArrayToSend()
    
def Read_Time_Msg_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 6], source_address)
    return Msg.byteArrayToSend()

def Msg_Recieved_String_Xbee(self, msg):
#        print('Recieved dat: ',base_repr(msg.data[0],16),base_repr(msg.data[1],16),
#   set_Max_Trial_Num           base_repr(msg.data[2],16),base_repr(msg.data[3],16),base_repr(msg.data[4],16),
#              base_repr(msg.data[5],16),base_repr(msg.data[6],16),base_repr(msg.data[7],16))
        return
def Switch_to_Operational_State_Msg_Xbee():
    return None 
    
def set_Mean_Distribution_ITI_Xbee(Id,mean, source_address=None):
    Msg = XBeeMsg([Id, 1, 27,mean//(16**2),mean%(16**2)], source_address)
    return Msg.byteArrayToSend()

def set_Max_Trial_Num_Xbee(Id,Max, source_address=None):
    Msg = XBeeMsg([Id, 1, 21,Max//(16**6),(Max%(16**6))//16**4,
                   (Max%(16**4))//(16**2),Max%(16**2)], source_address)
    return Msg.byteArrayToSend()
    
def set_Trial_Timeout_ms_Xbee(Id, ms, source_address=None):
    Msg = XBeeMsg([Id, 1, 23,ms//(16**6),(ms%(16**6))//16**4,
                   (ms%(16**4))//(16**2),ms%(16**2)], source_address)
    return Msg.byteArrayToSend()
    
def set_Probability_Array_Xbee(Id,probArray, source_address=None):
    if len(probArray)>20:
        raise ValueError,'You can choose at max 20 different probability'
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
            MsgList += [Msg.byteArrayToSend()]
            probArray = probArray[3:]
    except ValueError:
        pass
    return MsgList
    
def read_Size_Log_and_Prog_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 36], source_address)
    return Msg.byteArrayToSend()

def read_External_EEPROM_Xbee(Id,Index, source_address=None):
    Msg = XBeeMsg([Id, 1, 20,Index//(16**2),Index%(16**2)], source_address)
    return Msg.byteArrayToSend()

def get_bactery_level_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 5], source_address)
    return Msg.byteArrayToSend()
    
def get_trial_number_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 15], source_address)
    return Msg.byteArrayToSend()

def get_trial_max_number_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 22], source_address)
    return Msg.byteArrayToSend()

def get_trial_timeout_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 24], source_address)
    return Msg.byteArrayToSend()

def get_mean_distribution_Xbee(Id, source_address=None):
    Msg = XBeeMsg([Id, 1, 28], source_address)
    return Msg.byteArrayToSend()
    
def get_probability_array_Xbee(Id,Index,source_address=None):   
    Msg = XBeeMsg([Id, 1, 26, Index], source_address)
    return Msg.byteArrayToSend()
    
def set_subject_Xbee(Id,sbj,source_address=None):
    Msg = XBeeMsg([Id, 1, 11, sbj], source_address)
    return Msg.byteArrayToSend()
    
def set_exp_id_xbee(Id,exp_id,source_address=None):
    Msg = XBeeMsg([Id, 1, 12, exp_id], source_address)
    return Msg.byteArrayToSend()
    
def set_phase_xbee(Id,phase,source_address=None):
    Msg = XBeeMsg([Id, 1, 13, phase], source_address)
    return Msg.byteArrayToSend()
    
def set_box_id_xbee(Id,box_id,source_address=None):
    Msg = XBeeMsg([Id, 1, 14, box_id], source_address)
    return Msg.byteArrayToSend()
    
def parsing_can_log(message,pc_id='0001'):
#    print 'arrivato',message.data[:]
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
        
    else:
        return 'unknown',message.id,'Matteo ti sei dimenticato qualcosa <3'

def parsing_XBee_log(message,pc_id='0001'):
    try:
        PAYLOAD = binascii.hexlify(message['rf_data'])
        
        if PAYLOAD[:4] == pc_id:
#            print 'ANSWER'
            is_answ = True
        else:
            print 'QUESTION'
            is_answ = False
#        print 'PARSING PAYLOAD',PAYLOAD
        Id = int(PAYLOAD[4:8], 16)
        if PAYLOAD[8:12] == '034c': # logfiles
            action = int(PAYLOAD[20:24], 16)
            if action > 15:
                time = int(PAYLOAD[12:20], 16)
            else:
                time = int(PAYLOAD[18:20], 16)
            return 'Log', Id, '%d\t%d'%(time,action)
        elif PAYLOAD[8:10] == '01':
            return 'Info', Id, 'Device Actuated'
        elif PAYLOAD[8:10] == '05':
            if is_answ:
                return 'Info', Id, 'Bactery Level %d'%int(PAYLOAD[10:14],16)
            else:
                return 'Info', Id, 'Request get Bactery Level'
        elif PAYLOAD[8:10] == '06':
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
        elif PAYLOAD[8:10] == '07':
            if is_answ:
                return 'Info', Id, 'RGB message'
            else:
                return 'Info', Id, 'Request RGB message'
        elif PAYLOAD[8:10] == '08':
            return 'Info', Id, 'Sound message'
        elif PAYLOAD[8:10] == '09':
            if is_answ:
                return 'Info', Id, 'Release pellet'
            else:
                return 'Info', Id, 'Request release pellet'
            
        elif PAYLOAD[8:10] == '0b':
            if is_answ:
                return 'Info', Id, 'Subject number set'
            else:
                return 'Info', Id, 'Request set subject number'
        elif PAYLOAD[8:10] == '0c':
            if is_answ:
                return 'Info', Id, 'Experiment id set'
            else:
                return 'Info',Id, 'Request exp id set'
        elif PAYLOAD[8:10] == '0d':
            if is_answ:
                return 'Info', Id, 'Phase set'
            else:
                return 'Info',Id, 'Request phase set'
        elif PAYLOAD[8:10] == '0e':
            if is_answ:
                return 'Info', Id, 'Box id set'
            else:
                return 'Info', Id, 'Request box id set'
        elif PAYLOAD[8:10] == '0f':
            if is_answ:
                trial_num = int(PAYLOAD[10:14],16)
                return 'Info', Id, 'Trial number %d'%trial_num
            else:
                return 'Info', Id, 'Request get trial number'
        elif PAYLOAD[8:10] == '12':
            if is_answ:
                print 'trial time payload',PAYLOAD
                return 'Info', Id, 'Trial time %d'%int(PAYLOAD[12:20], 16)
            else:
                return 'Info', Id, 'Request get real Time'
        elif PAYLOAD[8:10] == '14':
            if is_answ:
                return 'Info', Id, 'Ext EEPROM address %d'%(int(PAYLOAD[10:14],16))
            else:
                return 'Info', Id, 'Request get ext EEPROM'
        elif PAYLOAD[8:10] == '15':
            if is_answ:
                return 'Info', Id, 'Trial max number set'
            else:
                return 'Info', Id, 'Request set trial max number'
        elif PAYLOAD[8:10] == '16':
            if is_answ:
                trial_max = int(PAYLOAD[10:18],16)
                return 'Info', Id, 'Trial Max Number %d'%trial_max
            else:
                return 'Info', Id, 'Request get max trial number'
        elif PAYLOAD[8:10] == '17':#check if true
            if is_answ:
                return 'Info', Id, 'Set trial timeout'%trial_max
            else:
                return 'Info', Id, 'Request set trial timeout'
        elif PAYLOAD[8:10] == '18':#check if true
            if is_answ:
                trial_max = int(PAYLOAD[10:18],16)
                return 'Info', Id, 'Trial Timeout %d\n'%trial_max
            else:
                return 'Info', Id, 'Request get trial timeout'
        elif PAYLOAD[8:10] == '1b':
            if is_answ:
                return 'Info', Id, 'Mean Distribution set'
            else:
                return 'Info', Id, 'Request set mean distribution'
        elif PAYLOAD[8:10] == '1c':
            if is_answ:
                return 'Info', Id, 'Mean Distribution %d'%int(PAYLOAD[10:14],16)
            else:
                return 'Info', Id, 'Request get mean distribution'
        elif PAYLOAD[8:10] == '20':#check if true
            if is_answ:
                return 'Info', Id, 'Probablity Array Index %d Value %d, %d, %d\n'%int(PAYLOAD[10:18],16)
            else:
                return 'Info', Id, 'Request get probability array'
        elif PAYLOAD[8:10] == '24':
            if is_answ:
                return 'Info', Id, 'Program Size %d\n'%int(PAYLOAD[14:18],16)
            else:
                return 'Info', Id, 'Request get program size'
        else:
            raise AttributeError
    except:
        raise ValueError
        
    return 127,'parsing to be implemented\n'

def stringFromMsg(msg):
    """
        Retrurns a string with the message content. To be used in warning message
        in server_wifi_and_can_ask_status.py
    """
    if type(msg) is pycanusb.CANMsg:
        string = 'Id: %d\n'%msg.id + msg.dataAsHexStr()
    elif type(msg) is bytearray:
        msg = XbeeMsg_from_Bytearray(msg)
        string = 'Id: %d\n'%msg.toIntList()[0] + binascii.hexlify(msg['rf_data'])
    else:
        string = 'Id: %d\n'%msg.toIntList()[0] + binascii.hexlify(msg['rf_data'])       
    return string
#        raise ValueError
#if __name__ == "__main__":
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
# source_addr = '10202310'