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

import os,sys
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
sys.path.append(lib_dir)
from canUsb_thread import CANMsg
from messageLib import XbeeMsg_from_Bytearray,XBeeMsg
import binascii


"""
 mex xbee XBeeMsg
 msg_list = [Id, msg, answ]
 risposta a read: 
     msg.data[0] == 67
     msg.data[1]/[2]/[3] == answ.data[1]/[2]/[3]
 risposta a write:
     msg.data[0] == 96
     msg.data[1]/[2]/[3] == answ.data[1]/[2]/[3]
"""
class checkAnsw(object):
    def __init__(self, msg_list, MODE=0):
        super(checkAnsw, self).__init__()
        self.msg_list = msg_list
        self.MODE = MODE
    
    def __repr__(self):
        print('Object of class checkAnsw\nMessage: ')
        print(self.msg_list)
        print('Mode: ',self.MODE)
        
    def check(self, msg):
        if self.MODE:
            return checkXbee(self.msg_list, msg)
        else:
            return checkCAN(self.msg_list, msg)

def checkXbee(msg_list, msg):
    answ = msg_list[1]
    try:
        source_address = msg['source_addr']
        source_address_answ = answ['source_addr']
        PAYLOAD = binascii.hexlify(msg['rf_data'])
        PAYLOAD_answ = binascii.hexlify(answ['rf_data'])
        Id = int(PAYLOAD[4:8], 16)
        Id_answ = int(PAYLOAD_answ[4:8], 16)
        func = int(PAYLOAD[8:10],16)
        func_answ = int(PAYLOAD_answ[8:10],16)
#        print PAYLOAD
#        print PAYLOAD_answ
        if source_address == source_address_answ and\
            Id == Id_answ and func == func_answ:
            return True
    except: 
        return False
    return False

def checkCAN(msg_list, msg):
    answ = msg_list[1]
    if msg.id  != answ.id:
        return False
    if msg.data[0] is answ.data[0] and\
        msg.data[1] is answ.data[1] and\
        msg.data[2] is answ.data[2]:
        return True
    return False
    
def getAnsw(msg, MODE):
    if MODE:
        return xbeeGetAnsw(msg)
    else:
        return  canGetAnsw(msg)

def canGetAnsw(msg):
    answ = CANMsg()
    answ.id = msg.id - 128
    answ.len = 8
    if msg.data[0] is 35: #WRITE
        data_list  = [96, msg.data[1], msg.data[2], msg.data[3], 0, 0, 0, 0]
    elif msg.data[0] is 64: #READ
        data_list  = [67, msg.data[1], msg.data[2], msg.data[3], 0, 0, 0, 0]
    else:
        raise ValueError("Must be a Get/Set type of message, msg.data[0] = 35 or 64!")
    for i in range(8):
        answ.data[i] = data_list[i]
    return answ

def xbeeGetAnsw(msg):
    if type(msg) is bytearray:
        xbeemsg = XbeeMsg_from_Bytearray(msg)
    else:
        xbeemsg = msg
    try:
        PAYLOAD = binascii.hexlify(xbeemsg['rf_data'])
        Id = int(PAYLOAD[:4], 16)
        master_Id = int(PAYLOAD[4:8], 16)
        func = int(PAYLOAD[8:10],16)
        if func in [2,7,8,9,11,12,13,14,21,23,25,27,29,31]: # LISTA MESSAGGI SET CHE VOGLIONO IN RISPOSTA ACK func = 1
            func = 1
        return XBeeMsg([master_Id, Id, func], xbeemsg['source_addr'])
    except:
        raise ValueError('Message of incorrect format...')
        
    
#class parsing_xbee_log_test(QDialog):
#    def __init__(self,Id=3,parent=None):
#        super(parsing_xbee_log_test,self).__init__(parent)
#        self.check_msg =  None
#        source_address = binascii.unhexlify('0013a20040da7664')
#        p = enumerate_serial_ports()
#        for port in p:
#            if '\\Device\\VCP' in port[1]:
#                self.wifi = True
#                print 'Try to open serial port'
#                self.serialPort = serial.Serial(port[0], baudrate=19200,
#                                                timeout=1)
#        
#        sleep(1)
#        self.Reader = recievingXBeeThread(self.serialPort)
#        self.Reader.recieved.connect(self.parsing_xbee_log_test)
#        self.Reader.start()
#        
#        sleep(1)
##        Msg = Switch_to_Operational_State_Msg()
##        Msg_1 = get_ic2_Status(Id)
#        Msg_2 = Read_Date_Msg(Id,source_address=source_address, MODE=1)
#        Msg_3 = Read_Time_Msg(Id,source_address=source_address, MODE=1)
##        Msg_4 = get_threshold_sensor(Id,'l')
##        Msg_5 = get_threshold_sensor(Id,'c')
##        Msg_6 = get_threshold_sensor(Id,'r')
#        Msg_7 = Get_Bactery_Level_Msg(Id,source_address=source_address, MODE=1)
##        Msg_8 = get_subject(Id,source_address=source_address,MODE=1)
##        Msg_9 = get_exp_id(Id,source_address=source_address,MODE=1)
##        Msg_10 = get_phase(Id,source_address=source_address,MODE=1)
##        Msg_11 = get_box_id(Id,source_address=source_address,MODE=1)
#        Msg_12 = get_trial_number(Id,source_address=source_address,MODE=1)
#        Msg_13 = read_Size_Log_and_Prog(Id, source_address=source_address, MODE=1)
#        Msg_14 = get_trial_max_number(Id,source_address=source_address,MODE=1)
#        Msg_15 = get_trial_timeout(Id,source_address=source_address,MODE=1)
##        Msg_16 = get_Probability_Array(Id,2,source_address=source_address,MODE=1)
#        Msg_17 = get_mean_distribution(Id,source_address=source_address,MODE=1)
#        
##        QTimer.singleShot(50,lambda msg = Msg : self.write(Msg))
##        QTimer.singleShot(150,lambda msg = Msg_1 : self.write(Msg_1))
#        QTimer.singleShot(2000,lambda msg = Msg_2 : self.write(Msg_2))
#        QTimer.singleShot(4000,lambda msg = Msg_3 : self.write(Msg_3))
##        QTimer.singleShot(300,lambda msg = Msg_4 : self.write(Msg_4))
##        QTimer.singleShot(350,lambda msg = Msg_5 : self.write(Msg_5))
##        QTimer.singleShot(400,lambda msg = Msg_6 : self.write(Msg_6))
#        QTimer.singleShot(6000,lambda msg = Msg_7 : self.write(Msg_7))
##        QTimer.singleShot(500,lambda msg = Msg_8 : self.write(Msg_8))
##        QTimer.singleShot(550,lambda msg = Msg_9 : self.write(Msg_9))
##        QTimer.singleShot(600,lambda msg = Msg_10 : self.write(Msg_10))
##        QTimer.singleShot(650,lambda msg = Msg_11 : self.write(Msg_11))
#        QTimer.singleShot(8000,lambda msg = Msg_12 : self.write(Msg_12))
#        QTimer.singleShot(10000,lambda msg = Msg_13: self.write(Msg_13))
#        QTimer.singleShot(12000,lambda msg = Msg_14 : self.write(Msg_14))
#        QTimer.singleShot(14000,lambda msg = Msg_15 : self.write(Msg_15))
##        QTimer.singleShot(900,lambda msg = Msg_16 : self.write(Msg_16))
#        QTimer.singleShot(16000,lambda msg = Msg_17 : self.write(Msg_17))
#        QTimer.singleShot(18000,self.disconnect)
#        
#        
#    def write(self,Msg):
#        mm = XbeeMsg_from_Bytearray(Msg)
#        print 'Writing',binascii.hexlify(mm['rf_data'])
#        self.serialPort.write(Msg)
#        
#        try:
#            self.check_msg = getAnsw(XbeeMsg_from_Bytearray(Msg), 1)
#        except IndexError:
#            
#            pass
#        
#    def parsing_xbee_log_test(self, message):
#        
#        try:
#            print 'Reading',binascii.hexlify(message['rf_data'])
#            PAYLOAD = binascii.hexlify(message['rf_data'])
#            Id = int(PAYLOAD[4:8], 16)
#            
#            cka = checkAnsw([Id,None,self.check_msg],MODE=1)
##            print 'ac',cka
#            res = cka.check(message)
#            print 'answ',res,'\n'
#        except Exception, e:
#            pass
#        return
#    
#    def disconnect(self):
#        print 'disconnect'
#        self.Reader.stopReading()
#        del self.serialPort
#        self.accept()
#        self.close()
#        
#        print 'end'
#
#def main():
#    test  = 'XBEE'
#    Id = 3
#    if test == 'XBEE':
#        #    import canportreader
#    
#        
##        t0=clock()  
##        
##        t1=clock()
#        
#        app = QApplication(sys.argv)
#        dlg = parsing_xbee_log_test(Id=3)
#        app.exec_()
#
#if __name__=='__main__':
#    main()