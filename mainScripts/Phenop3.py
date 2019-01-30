#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:03:32 2019

@author: Matte
"""
read_program_dlg
load_program_dlg
start_box_dlg
stop_box_dlg
autentication_dlg
import sys
import os
import binascii
import serial
import numpy as np
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(file_dir,'classes','phenopyClasses'))
sys.path.append(os.path.join(file_dir,'classes','analysisClasses'))
sys.path.append(os.path.join(file_dir,'dialogsAndWidget','phenoyDlg'))
sys.path.append(os.path.join(file_dir,'dialogsAndWidget','analysisDlg'))
sys.path.append(os.path.join(file_dir,'libraries'))
sys.path.append(os.path.join(file_dir,'export'))
import_dir = os.path.join(file_dir,'import')
image_dir = os.path.join(file_dir,'images')

from serial.tools import list_ports
from subprocess32 import Popen
from start_reading_thread import (recievingXBeeThread,ZigBee_thread,
                                  parsing_XBee_log,parsing_can_log)
from sys import executable

from send_email_thread import send_email_thread
from set_receiver_dlg import set_receiver_dlg
from email_addr import email_addr_add

from cage_widget import cage_widget
from multiple_cage_widget import multi_cageWidget

from Modify_Dataset_GUI import OrderedDict,action_Reply_Struct


from PyQt5.QtWidgets import (QMainWindow, QApplication,QPushButton,QLabel,
                             QDialog,QHBoxLayout,QVBoxLayout,QTextBrowser,
                             QSpacerItem,QSizePolicy,QDockWidget,QListWidget,
                             QAction,QMessageBox,QScrollArea)
from PyQt5.QtCore import (pyqtSignal,pyqtSlot,QTimer,QSettings,Qt)
from PyQt5.QtGui import QIcon



class find_device_or_analysis(QDialog):
    def __init__(self, sampleRate=10, canusb=None, xbee = None, arduino = None, parent=None):
        super(find_device_or_analysis,self).__init__(parent)
        
        self.parent = parent
        self.canusb = canusb
        self.xbee = xbee
        self.arduino = arduino
        self.MODE = None
        
        layout = QHBoxLayout()
        
        CloseButton = QPushButton('Continue', parent = self)
        StartButton_CAN = QPushButton('Start Search CAN', parent = self)
        StartButton_Xbee = QPushButton('Start Search XBEE', parent = self)
        self.stopFind_Button = QPushButton('Stop Search', parent=self)
        clearButton = QPushButton('Clear', parent=self)
        self.sampleRate = sampleRate
        label = QLabel('<b>Detected Devices:</b>')
        self.textBrowser = QTextBrowser()
        vlayout = QVBoxLayout()
        
        vlayout2 =  QVBoxLayout()
        button_analysis = QPushButton('Analysis')
        button_lightCtrl = QPushButton('Light controller')
        vlayout2.addWidget(button_analysis)
        vlayout2.addWidget(button_lightCtrl)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vlayout2.addSpacerItem(spacerItem)
        vlayout.addWidget(label)        
    
        hlayout =  QHBoxLayout()
        hlayout.addWidget(self.textBrowser)
        hlayout.addLayout(vlayout2)
        vlayout.addLayout(hlayout)
        
        layout.addWidget(StartButton_CAN)
        layout.addWidget(StartButton_Xbee)
        layout.addWidget(self.stopFind_Button)
        layout.addWidget(clearButton)
        layout.addWidget(CloseButton)
        vlayout.addLayout(layout)
        self.setLayout(vlayout)
        self.device_num = 0
        
        if not self.canusb:
            StartButton_CAN.setEnabled(False) 
        
        if not self.xbee:
            StartButton_Xbee.setEnabled(False)
            
        if not self.arduino:
            button_lightCtrl.setEnabled(False) 

        
        
        self.serialPort = None
        self.thread = ZigBee_thread(None,parent=self)
        self.thread.addNewDevice.connect(self.add_text)
 
        CloseButton.clicked.connect(self.closeMainWindow)
        StartButton_CAN.clicked.connect(self.startThread_can)
        StartButton_Xbee.clicked.connect(self.startThread_xbee)
        clearButton.clicked.connect(self.clearList)
        button_analysis.clicked.connect(self.startAnalysis)
        button_lightCtrl.clicked.connect(self.parent.startLightController)
        self.stopFind_Button.clicked.connect(self.stopThread)
        
        
#==============================================================================
#       To connect: first Phenopy search if canusb or xbee are available
#       then you can choose which mode activate
#==============================================================================
    @pyqtSlot()
    def startThread_can(self):
        self.MODE = 0 
        self.serialPort = serial.Serial(self.canusb, baudrate=500000,timeout=1)

    @pyqtSlot()             
    def startThread_xbee(self):
        self.MODE = 1
        self.serialPort = serial.Serial(self.xbee, baudrate=19200,timeout=1)
        self.thread = ZigBee_thread(self.serialPort,parent=self)
        self.thread.addNewDevice.connect(self.add_text)
        self.address_dict = OrderedDict()
        
        if not self.thread.isRunning():
            self.clearList()
            self.thread.start()
            self.source_address = self.address_dict

    @pyqtSlot()
    def startAnalysis(self):
        self.parent.launch_online_analysis()
     
    @pyqtSlot()
    def closeMainWindow(self):
        if self.MODE == 0:
            print('to be implemented')
        elif self.MODE == 1:
            if self.thread.readThread.isRunning() or self.thread.isRunning():
                self.thread.terminate()
            self.serialPort.close()
            self.accept()
        
        return self.MODE, self.serialPort, self.address_dict
        
    def add_text(self, msg): 
        if self.MODE == 0:
            if msg.id - 1792 > 127 or msg.id - 1792 < 0: # only keep alive are 1792 + cage ID 
                                                         # to characterize it use the fact that
                                                         # 1792 <= 1792 + cage ID <= 1792 + 127
                return
            ID = msg.id - 1792
            string = msg.dataAsHexStr()
            if ID in list(self.address_dict.keys()):
                return
            self.device_num += 1
            self.textBrowser.append('<font color="red">%d\t</font><b>ID:</b> %s\t<b>Data:</b> %s\n'%\
                        (self.device_num,ID,string))
            Dict = {ID:ID}
            self.address_dict.update(Dict)
        
        elif self.MODE == 1:
            ID = list(msg.keys())[0]
            self.device_num += 1
            string_Address = binascii.hexlify(msg[ID])
            self.textBrowser.append('<font color="red">%d.\t</font><b>ID:</b> %s\t<b>Address:</b> %s\n'%\
                        (self.device_num,ID,string_Address))
            self.address_dict.update(msg)
        

    
    @pyqtSlot()
    def stopThread(self):
        if self.MODE == 0:
            print('to be implemented')
        elif self.MODE == 1:
            self.thread.terminate()

    @pyqtSlot()
    def clearList(self):
        self.device_num = 0
        self.address_dict.clear()
        self.textBrowser.clear()
        if self.MODE == 0:
            print('to be implemented')
        elif self.MODE == 1:
            if self.thread.isRunning():
                self.thread.terminate()
            self.thread.address_dict.clear()
     
    @pyqtSlot()
    def closeEvent(self,b):
        if self.MODE == 0:
            self.canReader.stopReading()
            self.canusb._CanUSB__canusb_Close(self.canusb._CanUSB__handle)
            del self.canusb
            if self.canReader.isRunning():
                self.canReader.terminate()
        
        elif self.MODE == 1:
            if self.thread.isRunning():
                self.thread.terminate()
        else:
            self.close()

class Msg_Server(QMainWindow):
    
    forwardToGUICAN = pyqtSignal(str,str, name='sendGUImessage')
    forwardToGUIXbee = pyqtSignal(dict,str, name='sendGUImessage')    
    
    def __init__(self, programDict, port_can, port_xbee, port_arduino,parent=None):
        super(Msg_Server,self).__init__(parent)
        self.programDict = programDict
        
        self.can = port_can
        self.xbee = port_xbee
        self.arduino = port_arduino
        
        self.finalizing = False
        self.microsystemGuiActive = False
        self.arduinoGui = None
        self.__password = ''
        self.send_email_thread = send_email_thread(parent = self)
        self.saveFolderPath = os.path.curdir
        self.logString = {}         # LISTA DI LOG COI CODICI AZIONE
        self.infoString = {}        # LISTA DI LOG CON LE INFO
        self.timerSaveDict = {}     # DIZIONARIO DI TIMERS SHIFTATI PER IL SALVATAGGIO
        self.fileNames = {}         # NOMI DEI FILE DA SALVARE
        self.block_num = {}         # NUMERO ABORT TRIAL X CAGE
        self.Phenopy = None
        
        #   Creo oggetti per stack di messaggi da inviare
        self.stack_list = []                         # contiene id, msg, e identificatore risposta
        self.stack_counter = 0                       # numero tentativi di invio
        self.timer_stack = QTimer()                  # timer per inviare nuovamente il messaggio



#        self.write_if_stack   # controlla se ci sono mex in stack e li manda
#        self.connect(self.timer_stack, SIGNAL('timeout()'),

#        if check_status_every is None:
#            self.check_status_every = 4*3600*1000
#        else:
#            self.check_status_every = check_status_every
            
        
        
        
        dialog = find_device_or_analysis(canusb=self.can, xbee = self.xbee, arduino = self.arduino, parent=self)
        dialog.show()
        
        if not dialog.exec_():
            return None  
        
        self.MODE = dialog.MODE
        self.serialPort = dialog.serialPort
        self.source_address = dialog.address_dict
        
        if self.MODE == 0:
            print('ci devo lavorare')
            self.parsing_log = parsing_can_log
            self.Reader.startReading()
            self.forwardToGUI = self.forwardToGUICAN
            
        elif self.MODE == 1:
            self.Reader = recievingXBeeThread(self.serialPort)
            self.Reader.recieved.connect(self.recieveMsg)
            self.Reader.start()
            self.parsing_log = parsing_XBee_log
            self.forwardToGUI = self.forwardToGUIXbee
            
        self.IDList = list(self.source_address.keys())
        
        settings = QSettings()
        logDockWidgetRight = QDockWidget("Info", parent=self)
        logDockWidgetRight.setObjectName("LogDockWidgetRight")
        logDockWidgetRight.setAllowedAreas(Qt.RightDockWidgetArea)
        logDockWidgetRight.setMaximumWidth(300)
        self.listWidgetRight = QListWidget()
        logDockWidgetRight.setWidget(self.listWidgetRight)
        self.addDockWidget(Qt.RightDockWidgetArea,logDockWidgetRight)
        self.dict_cage_widget = {}
        self.addCage_widget()
        
        try:
            self.restoreGeometry(settings.value("MainWindow/Geometry"))
            self.restoreState(settings.value("MainWindow/State"))
        except:
            pass
        
        try:
            childkeys = settings.childKeys()
            new_keys = []
            for key in childkeys:
                new_keys += [str(key)]
            if  'SaveDirectory' in new_keys:
                self.saveFolderPath = str(str(settings.value('SaveDirectory')))
        except:
            print('Save new path')
            
        # CREATE A MENU
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileSetSavePathAction = self.createAction("Set &Path", self.setSavePath, 
                                                       'Ctrl+P', None,"Set path to log folder")
        self.fileSetSavePathAction.setEnabled(True)
        self.fileStartStandAloneAction = self.createAction("&Start Recording",
                                                           self.start_box,
                                                           'Alt+R', None,
                                                           "Start Recording")
        self.MenuEdit = self.menuBar().addMenu("&Edit")
        
        try:
            self.pdict = np.load(os.path.join(os.curdir,'pdict.npy')).all()
            self.receivers = self.pdict['receivers']
        except:
            self.pdict = {}
            self.setSender()
            self.receivers = self.pdict['receivers']
        
        if len(list(self.pdict.keys())) == 0:
            self.fileStartStandAloneAction.setEnabled(False)
        
        self.fileStopAction = self.createAction("S&top", self.stop_box,None, None, "Stop program")
        self.fileSetSenderAction = self.createAction("Set Sender", self.setSender,None, None, "Set email sender")
        self.fileSetReceiverAction = self.createAction("Set Receivers", self.setReceivers,None, None,"Set email receivers")
        self.launchMessageGUIAction = self.createAction("&Message GUI", self.start_message_gui, None, None, "Lunch message dialog")
        self.launchArduinoGUIAction = self.createAction("&Light Controller", self.startLightController, None, None, "Lunch light controller")

        self.fileMenu.addActions([self.fileSetSavePathAction,#self.fileStartAction,
                                  self.fileStartStandAloneAction,self.fileStopAction])
        self.MenuEdit.addActions([self.launchMessageGUIAction,self.fileSetSenderAction,self.fileSetReceiverAction,self.launchArduinoGUIAction])
        self.menuProgram = self.menuBar().addMenu('P&rogram')
        self.read_Program_ation = self.createAction("Read Program",self.read_program, None,None, "Read program")
        self.upload_Program_ation = self.createAction("Upload Program",self.upload_program, None,None,"Upload program")
        self.menuProgram.addActions([self.read_Program_ation,self.upload_Program_ation])                     
        self.menuAnalysis = self.menuBar().addMenu('&Online Analysis')
        self.launch_anal_action = self.createAction("Start Analysis",self.launch_online_analysis, None,None, "Start analyzing data")
        self.menuAnalysis.addActions([self.launch_anal_action])
        self.menuHelp = self.menuBar().addMenu('&Help')
#        self.menuHelp.createActions("matteo.falappa@libero.it",None,None,None,"edoardo.balzani87@gmail.com",None,None,None,"IIT, January 2019",None,None,None)

        
        if len(list(self.pdict.keys()))==0:
            self.upload_Program_ation.setEnable(False)
        
#        if not self.MODE:
#            self.sendMessage(Switch_to_Operational_State_Msg(MODE=self.MODE))  ## Importazione di una delle due librerie in corso d'opera
        
    
    
    def launch_online_analysis(self):
        if (not self.Phenopy) or not (self.Phenopy.poll() is None):
            self.Phenopy = Popen([executable,os.path.join(file_dir,'mainAnalysis.py')])
        
    def read_program(self):
        self.read_Program_ation.setEnabled(False)
        self.upload_Program_ation.setEnabled(False)
        self.launchMessageGUIAction.setEnabled(False)
        dialog = read_program_dlg(self.IDList,parent=self)
        dialog.show()

    def upload_program(self):
        self.read_Program_ation.setEnabled(False)
        self.upload_Program_ation.setEnabled(False)
        self.launchMessageGUIAction.setEnabled(False)
        dialog = load_program_dlg(self.IDList,parent=self)
        dialog.show()
   
    def addCage_widget(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        for Id in self.IDList:
            self.dict_cage_widget[Id] = cage_widget(MODE=self.MODE, cage_id=Id)
        m_cage = multi_cageWidget(self.dict_cage_widget,parent=self)
        self.scrollArea.setWidget(m_cage)
        self.setCentralWidget(self.scrollArea)
        
    def get_not_recording_box(self):
        newList = []
        for box  in self.IDList:
            if not self.dict_cage_widget[box].isRec:
                newList += [box]
        return newList
 
    def get_recording_box(self):
        newList = []
        for box  in self.IDList:
            if self.dict_cage_widget[box].isRec:
                newList += [box]
        return newList
    
    def start_box(self):
        newList = self.get_not_recording_box()
        dlg = start_box_dlg(newList, parent=self,source_address=self.source_address, MODE=self.MODE)
        dlg.show()
        dlg.start_signal.connect(self.Start_StandAlone)

    def Start_StandAlone(self,msg_list,IDList):
        ## AGGIUNGI UN REFRESH CAGE WIDGET
        dialog = autentication_dlg(self.pdict)
        if not dialog.exec_():
            return
        self.__password = dialog.edit_psw.text()
     
        self.finalizing = False
        for Id in IDList: 
            self.timerSaveDict[Id] = QTimer()
        for ind in range(len(IDList)):
            self.logString[IDList[ind]] = ''
            self.infoString[IDList[ind]] = ''
            self.dict_cage_widget[Id].clear()
#            self.connect(self.timerSaveDict[IDList[ind]],SIGNAL('timeout()'),
#                         lambda Id = IDList[ind] : self.saveLog(Id))
            self.timerSaveDict[IDList[ind]].start(120000+ind*8000)
            self.fileNames[IDList[ind]] = str(IDList[ind])+'.tmpcsv'

            tmp = os.path.join(self.dict_cage_widget[IDList[ind]].path2save,self.fileNames[IDList[ind]])
            f = open(tmp,'a')
            f.close()
        self.add_stack(msg_list)
        
    def stop_box(self):
        newList = self.get_recording_box()
        dlg = stop_box_dlg(newList, parent=self,source_address=self.source_address, MODE=self.MODE)
        dlg.show()
        dlg.stop_signal.connect(self.StopServer)
        
    
    def StopServer(self,msg_list,IDList):
        if self.MODE == 0:
            print('ci devo lavorare')
        elif self.MODE == 1:
            for Id in IDList:
                self.saveLog(Id)
            self.finalizing = True
            self.add_stack(msg_list)
            self.fileStartStandAloneAction.setEnabled(True)
    
    def recieveMsg(self,message):
        try:
            Type, Id, log = self.parsing_log(message)
            print('Received ', Type, log,message)
        except (TypeError, ValueError) as e:
            print(e)
            return
        if not Type in ['Info','Log','Timer','Changed_address']:
            return
            
        self.check_answ(message) 
      
        boxList = self.get_recording_box()
        if Id in boxList:
            self.dict_cage_widget[Id].analyze_msg(message)
            if Type == 'Info':
                self.infoString[Id] += log
                num_item = self.listWidgetRight.count()
                if num_item == 100:
                    self.listWidgetRight.takeItem(0) ## check if first item is 0 or 1
                self.listWidgetRight.addItem('ID: %d\t'%Id + log)
                print('added info...')
            self.recieveStandAlone(message,Type, Id, log)
            
        else:
            if not self.microsystemGuiActive:
                self.dict_cage_widget[Id].analyze_msg(message)
            else:
                if self.MODE == 0:
                    if message.data[0] is 96:
                        st = 'W'
                    elif message.data[0] is 67:
                        st = 'R'
                    elif message.data[0] is 128:
                        st = 'E'
                    else:
                        st = 'R'
                else:
                    st = 'R'
                self.forwardToGUI.emit(message,st)

    def recieveStandAlone(self,message,Type, Id, log):
        if Type == 'Log':
            action = int(log.rstrip('\n').split('\t')[1])
            if action == 48: # abort pellet release
                self.block_num[Id] += 1
                if self.send_email_thread.isRunning():
                    self.send_email_thread.wait()
                self.send_email_thread.initialize(Id, self.block_num[Id],
                                                  self.pdict,self.__password) ##### AGGIUNGI EMAIL TYPE
                self.send_email_thread.start()
            if action == 50:
                pass

            self.logString[Id] += log
            if self.finalizing:
                self.saveLog(Id)
            
#==============================================================================
# ARRIVATO QUI A MODIFICARE IL CAZZO DI PROGRAMMA DI MODO CHE VADA SIA WIFI CHE
# VIA CAVO, VA SISTEMATO PERFORM ACTION
#==============================================================================
            
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
##        if slot is not None:
##            action.triggered.connect(self.)
##            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action   

    def setSender(self):
        if len(list(self.pdict.keys())):
            answ = QMessageBox.question(self,'Change sender settings?', 'Current sender\nemail: %s\nserver: %s\nport: %s\nDo you want to change sender?'%(self.pdict['email'],self.pdict['server'],
                                        self.pdict['port']),QMessageBox.No|QMessageBox.Yes)
            if answ != 16384:
                return
        dialog = email_addr_add(parent=self)
        if dialog.exec_():
            self.pdict = dialog.pdict
        if len(list(self.pdict.keys())):
            self.fileStartStandAloneAction.setEnabled(True)
            self.receivers = [self.pdict['receivers']]
        else:
            self.fileStartStandAloneAction.setEnabled(False)
            
    def setReceivers(self):
        dialog = set_receiver_dlg(self.pdict['receivers'],self.pdict,self)
        dialog.show()
   
    def sendMessage(self,msg): 
        print('manda un messaggio')
#        try:
#            print('Write message:',binascii.hexlify(msg))
#        except: 
#            print('Write message:',msg)
#        
#        self.serialPort.write(msg)
#        return 

        
     
    def saveLog(self,Id):
        print('salva il log')
#        self.timerSaveDict[Id].stop()
#        tmp = os.path.join(self.dict_cage_widget[Id].path2save,self.fileNames[Id])
#        fh = open(tmp,'a')        
#        fh.write(self.logString[Id])
#        fh.close()
#        self.logString[Id] = ''
#        self.infoString[Id] = ''
#        if not self.finalizing:
#            self.timerSaveDict[Id].start(1800000)
#        
    def setSavePath(self):
        if os.path.exists(self.saveFolderPath):
            pt = self.saveFolderPath
        else:
            pt = '.'
        dlg = change_dir_prog(self.IDList,parent=self,dir2save=pt)
        dlg.show()
        dlg.update_dir_signal.connect(self.update_dirs)
#        
    def update_dirs(self,lisId,Dir):
       for Id in lisId:
            self.dict_cage_widget[Id].setPath2save(Dir)
                    
    def add_stack(self, list_of_msg):
        print('aggiorna la dir')
#        DT = 50
#        if not self.stack_list:
#            self.stack_counter = 0
#        for msg in list_of_msg:
#            answ = getAnsw(msg, self.MODE)
#            self.stack_list += [[msg, answ]]
#        if not self.timer_stack.isActive():
#            self.timer_stack.start(DT)
#    
    def write_if_stack(self):
        print('aggiorna la dir')

#        MAXCOUNTER = 10
#        DT = 1500
#        if self.stack_counter <= MAXCOUNTER:
#            if self.stack_list:
#                self.sendMessage(self.stack_list[0][0])
#                self.timer_stack.stop()
#                self.timer_stack.start(DT)
#                self.stack_counter += 1
#            else:
#                self.stack_counter = 0
#                self.timer_stack.stop()
#        else:
#            if self.stack_list:
#                msg = self.stack_list.pop(0)[0]
#                self.write_if_stack()
#                self.stack_counter = 0
#                string = 'Cannot send a message\n' + stringFromMsg(msg)
#                dialog = QMessageBox(QMessageBox.Warning,'Cannot send a message',string,
#                                QMessageBox.Ok,parent=self)
#                dialog.show()
#    
    def check_answ(self, msg):
        print('guarda la risposta')

#        self.timer_stack.stop()
#        if not self.stack_list:
#            return
#        cka = checkAnsw(self.stack_list[0], self.MODE)
##        if self.MODE and msg.has_key('rf_data'):
##            print('rf_data check answ: ', msg['rf_data'],self.stack_list[0][1],cka.check(msg))
##        elif self.MODE:
##            print('check answ: ', msg, self.stack_list[0][1],cka.check(msg))
##        else:
##            print('check answ: ', msg.dataAsHexStr(),self.stack_list[0][1],cka.check(msg))
#        if cka.check(msg):
#            self.stack_list.pop(0)
#            self.stack_counter = 0
#            self.write_if_stack()
#    
    def start_message_gui(self):
        print('fai qualcosa la dir')

#        bl = self.get_not_recording_box()
#        box_list = []
#        for ID in bl:
#            box_list += [(ID,self.source_address[ID])]
#        self.microsystemGUI = msg_sender_gui(box_list=box_list, MODE=self.MODE, parent=self)
#        self.microsystemGUI.sendGUImessage.connect(self.sendGUIMessage)
#        self.microsystemGUI.show()
#        self.launchMessageGUIAction.setEnabled(False)
#        self.read_Program_ation.setEnabled(False)
#        self.upload_Program_ation.setEnabled(False)
#    
    def sendGUIMessage(self,msg_list):
        print('fai qualcosa la dir')
#        self.add_stack(msg_list)
        
    def closeEvent(self, event):
#        if self.Phenopy:
#            self.Phenopy.kill()
#        settings = QSettings()
#        settings.setValue("MainWindow/Geometry", 
#                          self.saveGeometry())
#        settings.setValue("MainWindow/State", 
#                          self.saveState())
#       
#        settings.setValue('SaveDirectory',self.saveFolderPath)
#        if len(list(self.pdict.keys())):
#            np.save(os.path.join(os.curdir,'pdict.npy'),self.pdict)
#        if self.MODE:
#            self.Reader.terminate()
#            if self.serialPort:
#                self.serialPort.close()
        print('close event')
        super(Msg_Server,self).close()
        
    def startLightController(self):
        print('arduino')
#        if not self.arduinoGui:
#            found = False
#            for val in list_ports.comports():
#                port = val[0]
#                descr = val[1]
#                if 'ARDUINO' in descr.upper():
#                    found = True
#                    break
#            if not found:
#                print( 'Did not found an arduino conected')
##                QMessageBox.warning(self, 'Serial connection error', 'Could not find Arduino connected', buttons = QMessageBox.Ok, defaultButton = QMessageBox.NoButton)
#                port = None
#                return
#            self.arduinoGui = timerGui(15,port,baud=9600,parent=self)
#        self.arduinoGui.show()
        

#            return ValueError('Unable to connect to adapter')

def main():

    port_can = None
    port_xbee = None
    port_arduino = None
    
    for val in list_ports.comports():
        port = val[0]
        descr = val[1]
        
        if 'CANUSB' in descr:
            port_can = port
            
        if 'XBee' in descr:
            port_xbee = port
            
        if 'ARDUINO' in descr.upper():
            port_arduino = port
             
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    d={}

    form = Msg_Server(d,port_can,port_xbee,port_arduino)
    form.show()
    app.exec_()
    return form

    
    
    

    
if __name__== '__main__':
    main()