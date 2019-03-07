#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:58:53 2019

@author: Matte
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication,QButtonGroup,
                             QSpacerItem,QSizePolicy,QCheckBox,QTableWidgetItem)
from PyQt5.QtCore import (pyqtSignal,Qt,QObject)

from ui_microsystemGui import Ui_MainWindow
import os, sys

classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
phenopy_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'mainScripts')

sys.path.append(classes_dir)
sys.path.append(phenopy_dir)
import datetime

from xbee_thread import (parsing_XBee_log)
from canUsb_thread import (CANMsg,parsing_can_log)

import binascii

from messageLib import (Read_Time_Msg,Read_Date_Msg,Set_Date_Msg,Set_Time_Msg,
                        ReleaseFood_Msg,switch_Lights_Msg,switch_Noise_Msg,
                        get_exp_id,get_phase,get_box_id,get_subject,
                        get_mean_distribution,get_threshold_sensor,
                        get_trial_max_number,get_trial_timeout,
                        set_Trial_Timeout_ms,set_Max_Trial_Num,set_Mean_Distribution_ITI,
                        set_exp_id,set_phase,set_box_id,set_subject,set_threshold_sensor,
                        set_noise_freq,get_noise_freq,Get_Bactery_Level_Msg,
                        get_ic2_Status,get_trial_number,get_firmware_version,
                        Start_Stop_Trial_Msg,read_Size_Log_and_Prog,
                        Read_RealTime_Msg,XbeeMsg_from_Bytearray)

        
class msg_sender_gui(QMainWindow, Ui_MainWindow, QObject):
    sendGUImessage = pyqtSignal(list, name='sendGUImessage')
    def __init__(self, box_list=[],MODE = 0, parent=None):
        super(msg_sender_gui, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        if MODE:
            self.update_table = self.update_table_xbee
        else:
            self.update_table = self.update_table_can
        self.parent = parent
        if parent:
            parent.forwardToGUI.connect(self.update_table)
            parent.microsystemGuiActive = True
        else:
            self.sendGUImessage.connect(self.prova_lista_msg)
        self.setupUi(self)
        self.mode = MODE
        
#        self.groupBox.setStyleSheet("QGroupBox { background-color: rgb(255, 255,\
#            255); border:2px solid rgb(83, 84, 84); }")
        self.scrollArea_Box.setStyleSheet("QScrollArea { border:2px solid rgb(83, 84, 84); }")
        self.spinBox_param1.setFixedWidth(72)
        self.spinBox_param2.setFixedWidth(72)
        
        # GROUP BUTTON SIDE AND SET MUTUALLY EXCLUSIVE
        self.checkBox_all.setChecked(True)
        self.buttonGroup_side = QButtonGroup()
        self.buttonGroup_side.addButton(self.checkBox_left)
        self.buttonGroup_side.addButton(self.checkBox_center)
        self.buttonGroup_side.addButton(self.checkBox_right)
        self.buttonGroup_side.addButton(self.checkBox_all)
        self.buttonGroup_side.setExclusive(True)
        
        # DICTIONARY FOR RANGE PARAMETERS
        self.rangeDict = {'trial_timeout':(0,1000000), # sec da trasformare in ms
                          'mood':(0,1),
                          'freq':(62985,65525),
                          'exp_id':(0,65535),
                          'phase':(0,65535),
                          'box_id':(0,65535),
                          'subject':(0,65535),
                          'mean_distr':(0,65),
                          'poke_th':(0,65535),
                          'max_trial_num':(0,1000000), 
                          'trial_timeout':(0,1000000)} # sec da trasformare in  ms
        
        # GROUP BUTTON COLOR AND SET MUTUALLY EXCLUSIVE
        self.checkBox_white.setChecked(True)
        self.buttonGroup_color = QButtonGroup()
        self.buttonGroup_color.addButton(self.checkBox_blu)
        self.buttonGroup_color.addButton(self.checkBox_green)
        self.buttonGroup_color.addButton(self.checkBox_cyano)
        self.buttonGroup_color.addButton(self.checkBox_red)
        self.buttonGroup_color.addButton(self.checkBox_violet)
        self.buttonGroup_color.addButton(self.checkBox_yellow)
        self.buttonGroup_color.addButton(self.checkBox_white)
        self.buttonGroup_color.setExclusive(True)
        
        # GROUP BUTTON GET/SET AND SET MUTUALLY EXCLUSIVE
        self.checkBox_get.setChecked(True)
        self.buttonGroup_gs = QButtonGroup()
        self.buttonGroup_gs.addButton(self.checkBox_get)
        self.buttonGroup_gs.addButton(self.checkBox_set)
        self.buttonGroup_gs.setExclusive(True)
        self.radioButton_box_id.setChecked(True)

        # INIZIALIZATION OTHER PARAM
        self.spinBox_param2.setEnabled(False)
        
        # CONNECT BUTTON GROUP TO CHECK STATUS OF INPUTS
        self.buttonGroup_side.buttonClicked.connect(self.recheck_if_checked)
        self.buttonGroup_color.buttonClicked.connect(self.recheck_if_checked)
        self.buttonGroup_gs.buttonClicked.connect(self.recheck_if_checked)
        
                     
        # CONNECT ALL BUTTON TO SEND MESSEGE
        self.pushButton_send_actuate.clicked.connect(self.sendAction)
        self.pushButton_send_datetime.clicked.connect(self.sendTime)
        self.pushButton_send_other_gs.clicked.connect(self.sendGetSet)
        self.pushButton_send_other_g.clicked.connect(self.sendOnlyget)
        self.pushButton_send_custom.clicked.connect(self.sendCustom) #
        
                     
        # CONNECT LIGH OFF TO ALL FEEDER
        self.radioButton_light_off.clicked.connect(self.disable_feeder)
        self.radioButton_sound_off.clicked.connect(self.disable_feeder)
        self.radioButton_light_on.clicked.connect(self.eneable_feeder)
        self.radioButton_sound_on.clicked.connect(self.eneable_feeder)
        self.radioButton_release_pellet.clicked.connect(self.disable_hopper)
        
        self.radioButton_noise_frequency.toggled.connect(self.setDisableParm)
                     
        # Connect Close button
        self.pushButton_done.clicked.connect(self.close)

                     
        # Disable unallowed wifi commands
        if MODE:
            self.radioButton_poke_th_left.setEnabled(False)
            self.radioButton_poke_th_center.setEnabled(False)
            self.radioButton_poke_th_right.setEnabled(False)
            self.tab_custom.setDisabled(True)
                     
        # CONNECT BUTTON TO SET RANGE
        f = lambda: self.set_range2('mood','freq')
        self.radioButton_noise_frequency.clicked.connect(f)        
        f = lambda: self.set_range1('exp_id')
        self.radioButton_exp_id.clicked.connect(f)        
        f = lambda: self.set_range1('phase')
        self.radioButton_phase.clicked.connect(f)        
        f = lambda: self.set_range1('box_id')
        self.radioButton_box_id.clicked.connect(f)        
        f = lambda: self.set_range1('subject')
        self.radioButton_subject.clicked.connect(f)        
        f = lambda: self.set_range1('mean_distr')
        self.radioButton_mean_distr.clicked.connect(f)   
        f = lambda: self.set_range1('poke_th')
        self.radioButton_poke_th_left.clicked.connect(f)   
        f = lambda: self.set_range1('poke_th')
        self.radioButton_poke_th_center.clicked.connect(f)   
        f = lambda: self.set_range1('poke_th')
        self.radioButton_poke_th_right.clicked.connect(f)   
        f = lambda: self.set_range1('max_trial_num')
        self.radioButton_max_trial_num.clicked.connect(f)   
        f = lambda: self.set_range1('trial_timeout')
        self.radioButton_trial_timeout.clicked.connect(f)   
        
        # CONNECT CLEAR TABLE
        self.pushButton__reset.clicked.connect(self.clear_table)   
        
        # SET RABUTTON STANDARD CHECKED STATUS CHECKED
        self.radioButton_fw.setChecked(True)
        self.radioButton_release_pellet.setChecked(True)
        self.radioButton_read_time.setChecked(True)
        
        self.pushButton_send_datetime
        self.pushButton_send_actuate
        self.pushButton_send_other_gs
        self.pushButton_send_other_g
        self.pushButton_send_custom
        
        # SOURCE ADDRESS DICTIONARY
        self.sa_dictionary = {}
        
        
        for box in box_list:
            self.sa_dictionary[box[0]]=box[1]
        self.create_scroll_box()
        
    def set_range1(self,key):
        self.spinBox_param1.setRange(*self.rangeDict[key])
        
    def set_range2(self,key1,key2):
         self.spinBox_param1.setRange(*self.rangeDict[key1])
         self.spinBox_param2.setRange(*self.rangeDict[key2])
         self.spinBox_param2.setValue(self.rangeDict[key2][1])
        
        
    def setDisableParm (self,on):
        
        if on:
            self.spinBox_param2.setEnabled(True)
        else:
            self.spinBox_param2.setEnabled(False)
            
        
    def sendGetSet(self):
        self.createandsend("get_set")
        
    def sendOnlyget(self):
        self.createandsend("only_get")
        
    def sendCustom(self):
        self.createandsend("custom")
    
    def sendAction(self):
        self.createandsend("action")
    
    def sendTime(self):
        self.createandsend('time')
        
    def disable_feeder(self):
        self.checkBox_center.setDisabled(True)
        self.checkBox_left.setDisabled(True)
        self.checkBox_right.setDisabled(True)
        self.checkBox_all.setChecked(True)
        
    def disable_hopper(self):
        self.checkBox_center.setDisabled(True)
        self.checkBox_left.setDisabled(False)
        self.checkBox_right.setDisabled(False)
        self.checkBox_all.setDisabled(False)
    
    def eneable_feeder(self):
        self.checkBox_center.setDisabled(False)
        self.checkBox_left.setDisabled(False)
        self.checkBox_right.setDisabled(False)
            
    
    def createandsend(self,groupsend):
        self.check_box_id()
        message_list = []
        for box in self.list_checked:
            if groupsend=="time":
                dt = datetime.datetime.now()
                if self.radioButton_read_time.isChecked():
                    message_list += [Read_Time_Msg(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_read_date.isChecked():
                    message_list += [Read_Date_Msg(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_set_dateTime.isChecked():
                    message_list += [Set_Date_Msg(box,dt.day,dt.month,dt.year-2000,dt.weekday()+1,source_address=self.sa_dictionary[box], MODE=self.mode),Set_Time_Msg(box,dt.microsecond//10000,dt.second,dt.minute,dt.hour,source_address=self.sa_dictionary[box], MODE=self.mode)]    
            elif groupsend=="action":
                if self.radioButton_release_pellet.isChecked():
                    hopper = self.check_hopper()
                    for ii in hopper:
                        message_list += [ReleaseFood_Msg(box,ii,source_address=self.sa_dictionary[box], MODE=self.mode)]
                else:
                    l,c,r = self.check_location()
                    if self.radioButton_light_on.isChecked():
                        clc = self.check_light()
                        message_list += [switch_Lights_Msg(box,l*clc,c*clc,r*clc,source_address=self.sa_dictionary[box], MODE=self.mode)]
                    elif self.radioButton_light_off.isChecked():
                        message_list += [switch_Lights_Msg(box,0,0,0,source_address=self.sa_dictionary[box], MODE=self.mode)]
                    elif self.radioButton_sound_on.isChecked():
                        message_list += [switch_Noise_Msg(box,l,c,r,source_address=self.sa_dictionary[box], MODE=self.mode)]
                    elif self.radioButton_sound_off.isChecked():
                        message_list += [switch_Noise_Msg(box,0,0,0,source_address=self.sa_dictionary[box], MODE=self.mode)]
            elif groupsend == "get_set":
                par1 = self.spinBox_param1.value()
                par2 = self.spinBox_param2.value()
                if self.radioButton_exp_id.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_exp_id(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_phase.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_phase(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_box_id.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_box_id(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_subject.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_subject(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_mean_distr.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_mean_distribution(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_poke_th_left.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_threshold_sensor(box,'l',source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_poke_th_center.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_threshold_sensor(box,'c',source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_poke_th_right.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_threshold_sensor(box,'r',source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_max_trial_num.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_trial_max_number(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_trial_timeout.isChecked() and self.checkBox_get.isChecked():
                    message_list += [get_trial_timeout(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                    #metodi set
                elif self.radioButton_trial_timeout.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_Trial_Timeout_ms(box,par1*1000,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_max_trial_num.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_Max_Trial_Num(box,par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                    #metodi set di matteo
                elif self.radioButton_mean_distr.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_Mean_Distribution_ITI(box,par1*1000,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_exp_id.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_exp_id(box,par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_phase.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_phase(box,par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_box_id.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_box_id(box,par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_subject.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_subject(box,par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_poke_th_left.isChecked() and self.checkBox_set.isChecked():
                    message_list += [set_threshold_sensor(box,'l',par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_poke_th_center.isChecked() and self.checkBox_set.isChecked():
                     message_list += [set_threshold_sensor(box,'c',par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_poke_th_right.isChecked() and self.checkBox_set.isChecked():
                     message_list += [set_threshold_sensor(box,'r',par1,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_noise_frequency.isChecked() and self.checkBox_set.isChecked():
                     message_list += [set_noise_freq(box,par1,par2,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_noise_frequency.isChecked() and self.checkBox_get.isChecked():
                     message_list += [get_noise_freq(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
            
            elif groupsend == "only_get":
                if self.radioButton_bactery_level.isChecked():
                    message_list +=[Get_Bactery_Level_Msg(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_ic2_status.isChecked():
                    message_list += [get_ic2_Status(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_trial_num.isChecked():
                    message_list += [get_trial_number(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_fw.isChecked():
                    message_list += [get_firmware_version(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_startAlone.isChecked():
                    message_list += [Start_Stop_Trial_Msg(box,True,Stand_Alone=True,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_stopAlone.isChecked():
                    message_list += [Start_Stop_Trial_Msg(box,False,Stand_Alone=True,source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_prog_size.isChecked():
                    message_list += [read_Size_Log_and_Prog(box, source_address=self.sa_dictionary[box], MODE=self.mode)]
                elif self.radioButton_readTrialTime.isChecked():
                    message_list += [Read_RealTime_Msg(box,source_address=self.sa_dictionary[box], MODE=self.mode)]
            
            
            elif groupsend == "custom":
                Msg = CANMsg()
                Msg.id = box + 1536
                Msg.len = self.spinBox.value()
                Msg.data[0] = self.spinBox_msg1.value()
                Msg.data[1] = self.spinBox_msg2.value()
                Msg.data[2] = self.spinBox_msg3.value()
                Msg.data[3] = self.spinBox_msg4.value()
                Msg.data[4] = self.spinBox_msg5.value()
                Msg.data[5] = self.spinBox_msg6.value()
                Msg.data[6] = self.spinBox_msg7.value()
                Msg.data[7] = self.spinBox_msg8.value()
                message_list += [Msg]
                
        self.sendGUImessage.emit(message_list)
        if not self.mode:
            for message in message_list:
                if message.data[0] is 35:
                    st = 'rW'
                elif message.data[0] is 64:
                    st = 'rR'
                else:
                    st = 'rR'
                self.update_table(message,st)
        else:
            for message in message_list:
                PAYLOAD = binascii.hexlify(message)[28:-2]
#                print 'gui payload',PAYLOAD
                if PAYLOAD[8:10] in ['05','06','0f','12','14','16','18','1a','1c','20','24']:
                    st = 'rR'
                else:
                    st = 'rW'
                self.update_table(message,st)
    
    
    def clear_table(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        
    def recheck_if_checked(self,button):
        if button.isChecked():
            button.setChecked(True)
    
    def create_scroll_box(self):
        self.check_box_dictionary = {} 
        self.checkBox_select_all = QCheckBox("Select All")
        self.verticalLayout_18.addWidget(self.checkBox_select_all)
        for box in list(self.sa_dictionary.keys()):
            box_widget = QCheckBox("Box %d"%box)
            self.check_box_dictionary[box] = box_widget
            self.verticalLayout_18.addWidget(box_widget)
        spaceritem = QSpacerItem(0,0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_18.addSpacerItem(spaceritem)
        self.checkBox_select_all.clicked.connect(self.select_all_clicked)
    
    def select_all_clicked(self,tof):
        if tof:
            for Id in list(self.sa_dictionary.keys()):
                self.check_box_dictionary[Id].setChecked(True)
        else:
            for Id in list(self.sa_dictionary.keys()):
                self.check_box_dictionary[Id].setChecked(False)
        
    def check_box_id(self):
        self.list_checked = []
        for box in list(self.sa_dictionary.keys()):
            if self.check_box_dictionary[box].isChecked():
                self.list_checked += [box]
                
    def check_hopper(self):
        if self.checkBox_left.isChecked():
            hopper = [0]
        elif self.checkBox_right.isChecked():
            hopper = [1]
        elif self.checkBox_all.isChecked():
            hopper = [0,1]
        return hopper
        
    def check_location(self):
        if self.checkBox_left.isChecked():
            l,c,r = 1,0,0
        elif self.checkBox_center.isChecked():
            l,c,r = 0,1,0
        elif self.checkBox_right.isChecked():
            l,c,r = 0,0,1
        elif self.checkBox_all.isChecked():
            l,c,r = 1,1,1
        return l,c,r
        
    def check_light(self):
        if self.checkBox_blu.isChecked():
            color = 1
        elif self.checkBox_green.isChecked():
            color = 2
        elif self.checkBox_cyano.isChecked():
            color = 3
        elif self.checkBox_red.isChecked():
            color = 4
        elif self.checkBox_violet.isChecked():
            color = 5
        elif self.checkBox_yellow.isChecked():
            color = 6
        elif self.checkBox_white.isChecked():
            color = 7
        return color
    
    def update_table_can(self,message,read_write):
        """
            In input riceve un messaggio dal parent (server_wifi_and_CAN...)
            fa il parsing del messaggio e completa la tabella di lettura
            proporrei di filtrare i keep alive che vengono emessi ogni 10s
        """
        if message.data[0] in [35,64,96,67,128]:
            self.tableWidget.insertRow(self.tableWidget.rowCount())  
            msg_type,box,txt = parsing_can_log(message) 
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,0,QTableWidgetItem('%d'%box))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,1,QTableWidgetItem(read_write))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,2,QTableWidgetItem(message.dataAsHexStr()))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,3,QTableWidgetItem(txt))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.scrollToBottom()
    
    def update_table_xbee(self,message,read_write):
        if type(message) is bytearray:
            message = XbeeMsg_from_Bytearray(message)
        if  message.has_key('rf_data'):
            try:
                msg_type,box,txt = parsing_XBee_log(message)
            except ValueError as e:
                print(e)
                return
            self.tableWidget.insertRow(self.tableWidget.rowCount())       
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,0,QTableWidgetItem('%d'%box))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,1,QTableWidgetItem(read_write))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,2,QTableWidgetItem(binascii.hexlify(message['rf_data'])))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,3,QTableWidgetItem(txt))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.scrollToBottom()
    
    def prova_lista_msg(self,message_list):
        for msg in message_list:
            print('Messaggio inviato o rievuto con successo', msg.dataAsHexStr())
            
    def closeEvent(self,events):
        self.parent.launchMessageGUIAction.setEnabled(True)
        self.parent.read_Program_ation.setEnabled(True)
        self.parent.upload_Program_ation.setEnabled(True)
        self.parent.microsystemGuiActive = False
        super(msg_sender_gui, self).close()
            
    
        
def main():
    import sys
    app = QApplication(sys.argv)
    form = msg_sender_gui(box_list=[(10, "GasGas"),(1, "dada"),(2, "saa"),(3, "www")])
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()