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
from canUsb_thread import CANMsg
from xbee_thread import XBeeMsg
import binascii
import datetime
    

def XbeeMsg_from_Bytearray(byte_msg):

    source_address = byte_msg[5:13]
    rf_data = binascii.hexlify(byte_msg[14:28])

    msg_list = [int(rf_data[:4],16), int(rf_data[4:8],16)]
    for i in range(8,20,2):
        if int(rf_data[i:i+2],16) is 255:
            break
        msg_list += [int(rf_data[i:i+2],16)]

    return XBeeMsg(msg_list,source_address)
    
#Matteo message======================================
def set_subject(Id,sbj_num,source_address=None,MODE=0):
    if MODE:
        return set_subject_Xbee(Id,sbj_num,source_address)
    Data = [35,2,18,32,sbj_num,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    

def set_exp_id(Id,exp_num,source_address=None,MODE=0):
    if MODE:
        return set_exp_id_xbee(Id,exp_num,source_address)
    Data = [35,2,18,33,exp_num,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def set_phase(Id,phase,source_address=None,MODE=0):
    if MODE:
        return set_phase_xbee(Id,phase,source_address)
    Data = [35,2,18,34,phase,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_box_id(Id,new_id,source_address=None,MODE=0):
    if MODE:
        return set_box_id_xbee(Id,new_id,source_address)
    Data = [35,2,18,35,new_id,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_threshold_sensor(Id,l_c_r,thres,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No threshold sensor message implemented for xbee')
    if l_c_r == 'l':
        code = 16
    elif l_c_r == 'c':
        code = 17
    elif l_c_r == 'r':
        code = 18
    Data = [35,2,18,code,thres%(16**2),thres//16**2,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_noise_freq(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No nosie frequency message implemented for xbee')
    
    Data = [64,2,18,20,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def set_noise_freq(Id,mod,freq,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No nosie frequency message implemented for xbee')
    if mod < 0 or mod > 1:
        raise ValueError('mod must be 0 or 1')
#    if freq < 1 or freq > 255:
#        raise ValueError, 'freq must be between 1 and 255'
    Data = [35,2,18,20,mod,freq%(16**2),freq//16**2,0]
    Msg = CANMsg()
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
        
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
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
        
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
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
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
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
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
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
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
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
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
    Data = [64,1,18,65,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg
    
def Get_Bactery_Level_Msg(Id,source_address=None, MODE=0):
    if MODE:
        return get_bactery_level_Xbee(Id,source_address)
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
    Data = [64,2,18,21,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg
    
def Read_Date_Msg(Id,source_address=None, MODE=0):
    if MODE:
        return Read_Date_Msg_Xbee(Id,source_address)
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
    Data = [64,2,18,5,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def Set_Date_Msg(Id,day,month,year,week_day,source_address=None, MODE=0):
    if MODE:
        raise ValueError('Data can be set only via CAN bus')
    if year > 99 or week_day > 7:
        raise ValueError('Year must be between 0 and 99 and week day must be a positive integer between 1 and 7')
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
    Data = [35,2,18,5,day,month,year,week_day]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg


def Read_Time_Msg(Id,source_address=None, MODE=0):
    if MODE:
        return Read_Time_Msg_Xbee(Id,source_address)
    Msg = CANMsg()
    
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
    Data = [64,2,18,6,0,0,0,0]
    for ind in Index:
        Msg.data[ind] = Data[ind]
    return Msg

def Set_Time_Msg(Id,millisec,second,minute,hour,source_address=None, MODE=0):
    if MODE:
        raise ValueError('Time can be set only via CAN bus')
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Index = list(range(8))
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
    Msg = CANMsg()
    Msg.id = 0
    Msg.len = 2
    Data = [1,0]
    for ind in [0,1]:
        Msg.data[ind] = Data[ind]
    return Msg 
    
def set_Mean_Distribution_ITI(Id,mean,source_address=None, MODE=0):
    if MODE:
        return set_Mean_Distribution_ITI_Xbee(Id,mean,source_address)
    Msg = CANMsg()
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
    Msg = CANMsg()
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
    Msg = CANMsg()
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
        raise ValueError('You can choose at max 20 different probability')
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
            Msg = CANMsg()
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
        raise ValueError('No ic2 status message implemented for xbee')
    Data = [64,1,18,48,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_threshold_sensor(Id,l_c_r,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No threshold sensor message implemented for xbee')
    if l_c_r == 'l':
        code = 16
    elif l_c_r == 'c':
        code = 17
    elif l_c_r == 'r':
        code = 18
    Data = [64,2,18,code,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_subject(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No subject message implemented for xbee')
    Data = [64,2,18,32,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_exp_id(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No subject message implemented for xbee')
    Data = [64,2,18,33,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_phase(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No subject message implemented for xbee')
    Data = [64,2,18,34,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_box_id(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError('No subject message implemented for xbee')
    Data = [64,2,18,35,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    

def get_trial_number(Id,source_address=None,MODE=0):
    if MODE:
        return get_trial_number_Xbee(Id,source_address)
    Data = [64,2,18,36,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def get_trial_max_number(Id,source_address=None,MODE=0):
    if MODE:
        return get_trial_max_number_Xbee(Id,source_address)
    Data = [64,2,18,80,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg


def get_trial_timeout(Id,source_address=None,MODE=0):
    if MODE:
        return get_trial_timeout_Xbee(Id,source_address=source_address)
    Data = [64,2,18,81,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_firmware_version(Id,source_address=None,MODE=0):
    if MODE:
        raise ValueError('Not Yet implemented for Xbee')
    Data = [64,10,16,0,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_mean_distribution(Id,source_address=None,MODE=0):
    if MODE:
        return get_mean_distribution_Xbee(Id,source_address=source_address)
    Data = [64,2,18,83,0,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def get_Probability_Array(Id,index,source_address=None,MODE=0):
    if index > 17:
        raise ValueError('Index between 0 and 17')
    if MODE:
        return get_probability_array_Xbee(Id,index,source_address)
    Data = [64,2,18,82,index,0,0,0]
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Start_Trial(Id,row):
    Msg = CANMsg()
    Msg.id = Id + 1536
    Msg.len = 8
    Data = [35,2,18,96,row,0,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg 
    
def program_Reset_Trigger(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,8,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_event_Trigger(Id,row,L_M_R):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,33,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,34,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,35,0,0]
    else:
        raise ValueError('L_M_R must contain a string with \'L\'/\'M\'/\'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_event_Poke(Id,row,L_M_R):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,30,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,31,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,32,0,0]
    else:
        raise ValueError('L_M_R must contain a string with \'L\'/\'M\'/\'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_Start_Trial_Timer(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,7,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_if_Random_MC(Id,row,Index):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,50,Index,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Light_On(Id,row,L_M_R,color):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if color not in list(range(1,8)):
        raise ValueError('color must be an integer between 1 and 7!')
    if L_M_R == 'L':
        Data = [35,2,18,96,row,10,color,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,12,color,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,14,color,0]
    else:
        raise ValueError('L_M_R must contain a string with \'L\'/\'M\'/\'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_manage_RGB(Id,row,color_L=0,color_M=0,color_R=0):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,9,color_L+16*color_M,color_R]
    if color_L not in list(range(0,8)):
        raise ValueError('color must be an integer between 0 and 7!')
    if color_M not in list(range(0,8)):
        raise ValueError('color must be an integer between 0 and 7!')
    if color_R not in list(range(0,8)):
        raise ValueError('color must be an integer between 0 and 7!')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_Fix_Delay(Id,row,ms):
    """
        ms = int, millisec of delay
    """
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,40,ms%(16**2),ms//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Light_Off(Id,row,L_M_R):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,11,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,13,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,15,0,0]
    else:
        raise ValueError('L_M_R must contain a string with \'L\'/\'M\'/\'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Loop_Local_Trial(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,3,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_Trigger(Id,row,L_M_R):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,57,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,58,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,59,0,0]
    else:
        raise ValueError('L_M_R must be \'L\',\'M\' or \'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Release_Pellet(Id,row,L_R):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_R == 'L':
        Data = [35,2,18,96,row,80,0,0]
    elif L_R == 'R':
        Data = [35,2,18,96,row,81,0,0]
    else:
        raise ValueError('L_R must be \'L\' or \'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_End_Local_Trial(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,5,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_End_Block_If(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,2,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_End_Loop_Local_Trial(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,4,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_Else_Block_If(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,6,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg


def program_Fixed_Delay_ITI(Id,row,ms):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if not (type(ms) is int and ms>10):
        raise ValueError('ms must be an iteger quantity >10')
    Data = [35,2,18,96,row,41,ms%(16**2),ms//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Random_Delay_ITI(Id,row,sec):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if not (type(sec) is int and sec >= 0):
        raise ValueError('sec must be an iteger quantity >=0')
    Data = [35,2,18,96,row,42,sec%(16**2),sec//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_End_Trial(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,1,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg 

def program_Counter_Init(Id,row,counterInd,Ind0):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,70,counterInd,Ind0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
def program_Counter_Inc(Id,row,counterInd):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,71,counterInd,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def program_If_Light(Id,row,L_M_R):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,63,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,64,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,65,0,0]
    else:
        raise ValueError('L_R must be \'L\', \'M\' or \'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
def program_If_Presence(Id,row,L_M_R):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if L_M_R == 'L':
        Data = [35,2,18,96,row,60,0,0]
    elif L_M_R == 'M':
        Data = [35,2,18,96,row,61,0,0]
    elif L_M_R == 'R':
        Data = [35,2,18,96,row,62,0,0]
    else:
        raise ValueError('L_R must be \'L\', \'M\' or \'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_Counter(Id,row,G_L_E,counter0,counter1):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if G_L_E == 'G':
        Data = [35,2,18,96,row,66,counter0,counter1]
    elif G_L_E == 'L':
        Data = [35,2,18,96,row,67,counter0,counter1]
    elif G_L_E == 'E':
        Data = [35,2,18,96,row,68,counter0,counter1]
    else:
        raise ValueError('L_R must be \'L\', \'M\' or \'R\'')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_Random_Mc_Step(Id,row,index):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,52,index,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_init_Random_Mc_index(Id,row):
    
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,54,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_is_Random_Mc_index(Id,row,index):
    
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,55,index,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Dummy_Test(Id,row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,82,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
    
def read_Size_Log_and_Prog(Id, source_address=None, MODE=0):
    if MODE:
        return read_Size_Log_and_Prog_Xbee(Id, source_address)
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [64,2,18,37,0,0,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg
def read_External_EEPROM(Id,Index,source_address=None, MODE=0):
    if MODE:
        return read_External_EEPROM_Xbee(Id, Index, source_address)
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [64,2,18,4,0,0,Index%(16**2),Index//(16**2)]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def log_ITI_end_Msg(Id, row):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,43,0,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Noise_On(Id, row, left, center, right):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if left:
        Data = [35,2,18,96,row,16,0,0]
    elif center:
        Data = [35,2,18,96,row,18,0,0]
    elif right:
        Data = [35,2,18,96,row,20,0,0]
    else:
        raise ValueError('At least one side must be indicated')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_action(Id,row,mark):
    
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    Data = [35,2,18,96,row,79,mark,0]
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_Noise_Off(Id, row, left, center, right):
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if left:
        Data = [35,2,18,96,row,17,0,0]
    elif center:
        Data = [35,2,18,96,row,19,0,0]
    elif right:
        Data = [35,2,18,96,row,21,0,0]
    else:
        raise ValueError('At least one side must be indicated')
    for ind in range(8):
        Msg.data[ind] = Data[ind]
    return Msg

def program_If_TimoutReached(Id,row):
    Msg = CANMsg()
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
    Msg = CANMsg()
    Msg.id = Id +1536
    Msg.len = 8
    if pin < 1 or pin >= 15:
        raise ValueError('Pin must be an INT between 1 and 15')
    print('duration',duration) 
    if duration < 1 or duration > 250:
        raise ValueError('Duration must be in the range of [1,250]')
    elif duration != 1 and duration % 10 != 0:
        raise ValueError('Duration must be a multiple of 10')
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



def stringFromMsg(msg):
    """
        Retrurns a string with the message content. To be used in warning message
        in server_wifi_and_can_ask_status.py
    """
    if type(msg) is CANMsg:
        string = 'Id: %d\n'%msg.id + msg.dataAsHexStr()
    elif type(msg) is bytearray:
        msg = XbeeMsg_from_Bytearray(msg)
        string = 'Id: %d\n'%msg.toIntList()[0] + binascii.hexlify(msg['rf_data'])
    else:
        string = 'Id: %d\n'%msg.toIntList()[0] + binascii.hexlify(msg['rf_data'])       
    return string
