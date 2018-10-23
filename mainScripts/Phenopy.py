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

#==============================================================================
#  Server With GUI
#  Il server deve rimanere in costante lettura della porta a cui è collegato il
#  canusb con un "samplerate" variabile
#  TODO
#  Timer Reply Option:
#  Quando setto un timer per l'iti devo ricevere e salvare il tempo in cui incomincia
#  e finisce il timer
#
#
#   TODO PER INSERIRLA IN GUI
#       1. rendere tutti i dialoghi in modalità show e non exec_ (33 dialoghi)
#       2. creare un thread per importazione dato
#       3. creare un thread per edit dato
#   rimettere check answer e commentare azione sendOneTest
#==============================================================================


import os,sys
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(file_dir,'libraries'))
sys.path.append(os.path.join(file_dir,'dialogsAndWidget','phenoyDlg'))
sys.path.append(os.path.join(file_dir,'dialogsAndWidget','phenoyDlg'))
import_dir = os.path.join(file_dir,'import')
image_dir = os.path.join(file_dir,'images')
#sys.path.append(os.path.join(file_dir,'dialogsAndWidget','analysisDlg'))
sys.path.append(os.path.join(file_dir,'classes','phenopyClasses'))
sys.path.append(os.path.join(file_dir,'export'))
from sys import executable
from subprocess32 import Popen
from serial.tools import list_ports
# Import Qt modules
from microsystemGUI import *
from load_program_dlg import *
from read_program_gui import *
import _winreg as winreg
import binascii
import itertools
from checkAnsw import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import  uic
import pycanusb
import canportreader
from msgview import *
import datetime as dt
from time import clock,sleep
from copy import copy
from numpy import base_repr, binary_repr
from messageLib import *
from credential_dlg import autentication_dlg
from set_receiver_dlg import set_receiver_dlg
from myPyXBee import *
#import cageThread_SDO_Control
import os
import serial
import numpy as np
from xbee import XBee
from Modify_Dataset_GUI import OrderedDict,action_Reply_Struct
from email_addr import email_addr_add
from smtplib import *
from cage_widget import *
from send_email_thread import send_email_thread
from multiple_cage_widget import multi_cageWidget
from change_dir_prog import *
from start_box_dlg import *
from stop_box_dlg import *
from arduinoGui import *

__version__='1.0.0'
MONITOR_COLUMN_CNT = 4
#REPLYDICTIONARY = np.load('ReplyDictionary.npy').all()

def programPippo(msg):
    return msg.dataAsHexStr()

class find_device_Xbee(QDialog):
    def __init__(self,serialPortTuple,parent=None):
        super(find_device_Xbee,self).__init__(parent)
        self.parent = parent
        layout = QHBoxLayout()
        if type(serialPortTuple) is tuple:
            serialPort = serial.Serial(serialPortTuple[0], baudrate=19200,
                                   timeout=1)
        else:
            serialPort = serialPortTuple
        CloseButton = QPushButton('Continue', parent = self)
        StartButton = QPushButton('Start Search', parent = self)
        self.stopFind_Button = QPushButton('Stop Search', parent=self)
        clearButton = QPushButton('Clear', parent=self)
#        te = QTextEdit()
        label = QLabel('<b>Detected Devices:</b>')
        self.textBrowser = QTextBrowser()
        vlayout = QVBoxLayout()
        
        vlayout2 =  QVBoxLayout()
        button_analysis = QPushButton('Analysis')
        button_lightCtrl = QPushButton('Light controller')
        vlayout2.addWidget(button_analysis)
        vlayout2.addWidget(button_lightCtrl)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        vlayout2.addSpacerItem(spacerItem)
#        vlayout.addWidget(te)
        vlayout.addWidget(label)
    
        hlayout =  QHBoxLayout()
        hlayout.addWidget(self.textBrowser)
        hlayout.addLayout(vlayout2)
        vlayout.addLayout(hlayout)

        layout.addWidget(StartButton)
        layout.addWidget(self.stopFind_Button)
        layout.addWidget(clearButton)
        layout.addWidget(CloseButton)
        vlayout.addLayout(layout)
        self.device_num = 0
        self.setLayout(vlayout)
        self.serialPort = serialPort
        self.thread = ZigBee_thread(serialPort,parent=self)
        self.connect(CloseButton,SIGNAL('clicked()'),self.closeMainWindow)
        self.connect(StartButton,SIGNAL('clicked()'),self.startThread)
        self.connect(self.stopFind_Button,SIGNAL('clicked()'),self.stopThread)
        self.connect(clearButton,SIGNAL('clicked()'),self.clearList)
        self.connect(button_analysis,SIGNAL('clicked()'),self.startAnalysis)
        self.connect(button_lightCtrl,SIGNAL('clicked()'),self.parent.startLightController)
        self.thread.addNewDevice.connect(self.add_text)
        self.address_dict = OrderedDict()
          
    def startAnalysis(self):
        self.parent.launch_online_analysis()
            
    def closeMainWindow(self):
        print self.thread.readThread.isRunning(), self.thread.isRunning()
        if self.thread.readThread.isRunning() or self.thread.isRunning():
            self.thread.terminate()
#        self.serialPort.close()
        self.accept()
        
    def add_text(self, Dict):
        ID = Dict.keys()[0]
        self.device_num += 1
        string_Address = binascii.hexlify(Dict[ID])
        self.textBrowser.append('<font color="red">%d.\t</font><b>ID:</b> %s\t<b>Address:</b> %s\n'%\
                    (self.device_num,ID,string_Address))
        self.address_dict.update(Dict)
                    
    def startThread(self):
        if not self.thread.isRunning():
            print 'Thread started'
            self.clearList()
            self.thread.start()
        
    def stopThread(self):
        self.thread.terminate()
    
    def clearList(self):
        self.address_dict.clear()
        self.textBrowser.clear()
        if self.thread.isRunning():
            self.thread.terminate()
        self.thread.address_dict.clear()
        self.device_num = 0
    
    def closeEvent(self,b):
        if self.thread.isRunning():
            self.thread.terminate()
        print 'Close Event'

class find_device_CAN(QDialog):
    def __init__(self, sampleRate=10, canusb=None,parent=None):
        super(find_device_CAN,self).__init__(parent)
        self.parent = parent
        layout = QHBoxLayout()
        if canusb is None:
            self.canusb = pycanusb.CanUSB(bitrate='500')
        else:
            self.canusb = canusb
        print 'READER OFF'
        self.canReader = canportreader.CanPortReader(self.canusb, self.add_text,
                                                     sampleRate=sampleRate)
        print 'READER ON'
        CloseButton = QPushButton('Continue', parent = self)
        StartButton = QPushButton('Start Search', parent = self)
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
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        vlayout2.addSpacerItem(spacerItem)
#        vlayout.addWidget(te)
        vlayout.addWidget(label)        
    
        hlayout =  QHBoxLayout()
        hlayout.addWidget(self.textBrowser)
        hlayout.addLayout(vlayout2)
        vlayout.addLayout(hlayout)
        
        layout.addWidget(StartButton)
        layout.addWidget(self.stopFind_Button)
        layout.addWidget(clearButton)
        layout.addWidget(CloseButton)
        vlayout.addLayout(layout)
        self.setLayout(vlayout)
        self.device_num = 0
        self.connect(CloseButton,SIGNAL('clicked()'),self.closeMainWindow)
        self.connect(StartButton,SIGNAL('clicked()'),self.startThread)
        self.connect(self.stopFind_Button,SIGNAL('clicked()'),self.stopThread)
        self.connect(clearButton,SIGNAL('clicked()'),self.clearList)
        self.connect(button_analysis,SIGNAL('clicked()'),self.startAnalysis)
        self.connect(button_lightCtrl,SIGNAL('clicked()'),self.parent.startLightController)
        self.address_dict = OrderedDict()
     
    def startAnalysis(self):
        self.parent.launch_online_analysis()
        
    def closeMainWindow(self):
        self.canReader.stopReading
        if self.canReader.isRunning():
            self.canReader.terminate()
            self.canReader._readTimer.timeout.disconnect()
        self.accept()
        
    def add_text(self, msg):
#        print msg
        if msg.id - 1792 > 127 or msg.id - 1792 < 0: # only keep alive are 1792 + cage ID 
                                                     # to characterize it use the fact that
                                                     # 1792 <= 1792 + cage ID <= 1792 + 127
            return
        ID = msg.id - 1792
        string = msg.dataAsHexStr()
        if ID in self.address_dict.keys():
            return
        self.device_num += 1
        self.textBrowser.append('<font color="red">%d\t</font><b>ID:</b> %s\t<b>Data:</b> %s\n'%\
                    (self.device_num,ID,string))
        Dict = {ID:ID}
        self.address_dict.update(Dict)

    def startThread(self):
        if not self.canReader.isRunning():
            self.clearList()
        try:
            self.canReader.startReading()
            if self.canReader.isRunning():
                pass
        except:
            pass

    def stopThread(self):
        self.canReader.stopReading()
#        if self.canReader.isRunning():
#            self.canReader.terminate()
            
    
    def clearList(self):
        self.device_num = 0
        self.address_dict.clear()
        self.textBrowser.clear()
        self.canReader.stopReading()
        if self.canReader.isRunning():
            self.canReader.terminate()
        
    def closeEvent(self,b):
        self.canReader.stopReading()
        self.canusb._CanUSB__canusb_Close(self.canusb._CanUSB__handle)
        del self.canusb
        if self.canReader.isRunning():
            self.canReader.terminate()
        print 'Close Event'

    
        
class not_find_can_or_xbee(QDialog):
    def __init__(self,parent=None):
        super(not_find_can_or_xbee,self).__init__(parent)
        self.parent = parent
        layout = QHBoxLayout()
        
        CloseButton = QPushButton('Close', parent = self)
        StartButton = QPushButton('Start Search', parent = self)
        StartButton.setEnabled(False)

        stopFind_Button = QPushButton('Stop Search', parent=self)
        stopFind_Button.setEnabled(False)
        clearButton = QPushButton('Clear', parent=self)
        clearButton.setEnabled(False)
        
        label = QLabel('<b>Detected Devices:</b>')
        textBrowser = QTextBrowser()
        textBrowser.append('CANUSB or Xbee were not found, check the COM port connection.\nYou could lunch analysis or light controller if Arduino is connected.')
        vlayout = QVBoxLayout()
        
        vlayout2 =  QVBoxLayout()
        button_analysis = QPushButton('Analysis')
        button_lightCtrl = QPushButton('Light controller')
        vlayout2.addWidget(button_analysis)
        vlayout2.addWidget(button_lightCtrl)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        vlayout2.addSpacerItem(spacerItem)
        vlayout.addWidget(label)
    
        hlayout =  QHBoxLayout()
        hlayout.addWidget(textBrowser)
        hlayout.addLayout(vlayout2)
        vlayout.addLayout(hlayout)

        layout.addWidget(StartButton)
        layout.addWidget(stopFind_Button)
        layout.addWidget(clearButton)
        layout.addWidget(CloseButton)
        vlayout.addLayout(layout)
        
        self.setLayout(vlayout)
        self.connect(CloseButton,SIGNAL('clicked()'),self.close)
        self.connect(button_analysis,SIGNAL('clicked()'),self.startAnalysis)
        self.connect(button_lightCtrl,SIGNAL('clicked()'),self.parent.startLightController)
    
    def startAnalysis(self):
        self.parent.launch_online_analysis()
        
#    def closeMainWindow(self):
#        self.canReader.stopReading
#        if self.canReader.isRunning():
#            self.canReader.terminate()
#            self.canReader._readTimer.timeout.disconnect()
#        self.accept()
        
#    def add_text(self, msg):
##        print msg
#        if msg.id - 1792 > 127 or msg.id - 1792 < 0: # only keep alive are 1792 + cage ID 
#                                                     # to characterize it use the fact that
#                                                     # 1792 <= 1792 + cage ID <= 1792 + 127
#            return
#        ID = msg.id - 1792
#        string = msg.dataAsHexStr()
#        if ID in self.address_dict.keys():
#            return
#        self.device_num += 1
#        self.textBrowser.append('<font color="red">%d\t</font><b>ID:</b> %s\t<b>Data:</b> %s\n'%\
#                    (self.device_num,ID,string))
#        Dict = {ID:ID}
#        self.address_dict.update(Dict)

#    def startThread(self):
#        if not self.canReader.isRunning():
#            self.clearList()
#        try:
#            self.canReader.startReading()
#            if self.canReader.isRunning():
#                pass
#        except:
#            pass

#    def stopThread(self):
#        self.canReader.stopReading()
#        if self.canReader.isRunning():
#            self.canReader.terminate()
            
    
#    def clearList(self):
#        self.device_num = 0
#        self.address_dict.clear()
#        self.textBrowser.clear()
#        self.canReader.stopReading()
#        if self.canReader.isRunning():
#            self.canReader.terminate()
        
#    def closeEvent(self,b):
#        self.canReader.stopReading()
#        self.canusb._CanUSB__canusb_Close(self.canusb._CanUSB__handle)
#        del self.canusb
#        if self.canReader.isRunning():
#            self.canReader.terminate()
#        print 'Close Event'

    


#==============================================================================
#  EXAMPLE OF QOBJECT  with connect to be used for
#==============================================================================

class Msg_Server(QMainWindow):
    forwardToGUICAN = pyqtSignal(CANMsg,str, name='sendGUImessage')
    forwardToGUIXbee = pyqtSignal(dict,str, name='sendGUImessage')
    def __init__(self, programDict,
                 sampleRate=100,parent=None,check_status_every=None):
        super(Msg_Server,self).__init__(parent)
        self.programDict = programDict
        self.finalizing = False
        self.microsystemGuiActive = False
        self.arduinoGui = None
        self.__password = ''
        self.send_email_thread = send_email_thread(parent = self)
        self.saveFolderPath = os.path.curdir
        self.logString = {} # LISTA DI LOG COI CODICI AZIONE
        self.infoString = {} # LISTA DI LOG CON LE INFO
        self.timerSaveDict = {} # DIZIONARIO DI TIMERS SHIFTATI PER IL SALVATAGGIO
        self.fileNames = {} # NOMI DEI FILE DA SALVARE
        self.block_num = {} # NUMERO ABORT TRIAL X CAGE
        self.Phenopy = None
        
        
        
        
#   Creo oggetti per stack di messaggi da inviare
        self.stack_list = [] # contiene id, msg, e identificatore risposta
        self.stack_counter = 0 # numero tentativi di invio
        self.timer_stack = QTimer() # timer per inviare nuovamente il messaggio
        self.connect(self.timer_stack, SIGNAL('timeout()'),
                     self.write_if_stack) # controlla se ci sono mex in stack e li manda
           
#==============================================================================
#       To connect follow a different procedure... first as input of init you
#        can say if you want a wifi or can connection then the reader class
#        connection will be a different thread
#==============================================================================
        
        if not self.connectAdapter():
            raise ValueError, 'Unable to connect to adapter'
            self.close()
            
        if self.mode == 'CAN':
            self.Reader = canportreader.CanPortReader(self.serialPort,
                                                         self.recieveMsg,
                                                         sampleRate=sampleRate)
            self.parsing_log = parsing_can_log
            self.Reader.startReading()
            self.forwardToGUI = self.forwardToGUICAN
            
        elif self.mode == 'XBee':
            
            self.Reader = recievingXBeeThread(self.serialPort)
            self.Reader.recieved.connect(self.recieveMsg)
            self.Reader.start()
            self.parsing_log = parsing_XBee_log
            self.forwardToGUI = self.forwardToGUIXbee
#        if check_status_every is None:
#            self.check_status_every = 4*3600*1000
#        else:
#            self.check_status_every = check_status_every
        self.IDList = self.source_address.keys()
        
        
        settings = QSettings()
        logDockWidgetRight = QDockWidget("Info", parent=self)
        logDockWidgetRight.setObjectName("LogDockWidgetRight")
        logDockWidgetRight.setAllowedAreas(
                                      Qt.RightDockWidgetArea)
        logDockWidgetRight.setMaximumWidth(300)
        self.listWidgetRight = QListWidget()
        logDockWidgetRight.setWidget(self.listWidgetRight)
        self.addDockWidget(Qt.RightDockWidgetArea,logDockWidgetRight)
        self.dict_cage_widget = {}
        self.addCage_widget()
        
        try:
            self.restoreGeometry(
                settings.value("MainWindow/Geometry"))
            self.restoreState(settings.value("MainWindow/State"))
        except:
            pass
        
        try:
            childkeys = settings.childKeys()
            new_keys = []
            for key in childkeys:
                new_keys += [unicode(key)]
            if  u'SaveDirectory' in new_keys:
                self.saveFolderPath = unicode(unicode(settings.value(u'SaveDirectory')))
        except:
            print 'Save new path'
            
        # CREATE A MENU
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileSetSavePathAction = self.createAction("Set &Path", self.setSavePath,
                'Ctrl+P', None,
                "Set path to log folder")
        self.fileSetSavePathAction.setEnabled(True)
        self.fileStartStandAloneAction = self.createAction("&Start Recording",
                                                           self.start_box,
                                                           'Alt+R', None,
                                                           "Start Recording")
#        self.filsendone = self.createAction("&SENDONE TEST",
#                                                           self.sendOneTest,
#                                                           None, None,
#                                                           "Sendone")                                                   
        self.MenuEdit = self.menuBar().addMenu("&Edit")
        
        try:
            self.pdict = np.load(os.path.join(os.curdir, 'pdict.npy')).all()
            self.receivers = self.pdict['receivers']
        except:
            self.pdict = {}
            self.setSender()
            self.receivers = self.pdict['receivers']
        
        if len(self.pdict.keys()) == 0:
            self.fileStartStandAloneAction.setEnabled(False)
        
        self.fileStopAction = self.createAction("S&top", self.stop_box,None, None,
                                           "Stop program")
        self.fileSetSenderAction = self.createAction("Set Sender", self.setSender,None, None,
                                           "Set email sender")
        self.fileSetReceiverAction = self.createAction("Set Receivers", self.setReceivers,None, None,
                                           "Set email receivers")
        self.launchMessageGUIAction = self.createAction("&Message GUI", self.start_message_gui,
                                               None, None, "Lunch message dialog")
        self.launchArduinoGUIAction = self.createAction("&Light Controller", self.startLightController,
                                               None, None, "Lunch light controller")
#        if len(self.pdict.rUIAction = self.createAction("&Message GUI", self.start_message_gui,
#                                               None, None, "Lunch message dialog")
        self.fileMenu.addActions([self.fileSetSavePathAction,#self.fileStartAction,
                                  self.fileStartStandAloneAction,self.fileStopAction])
        self.MenuEdit.addActions([self.launchMessageGUIAction,self.fileSetSenderAction,self.fileSetReceiverAction,
                                  self.launchArduinoGUIAction])
        
        self.menuProgram = self.menuBar().addMenu('P&rogram')
        
        self.read_Program_ation = self.createAction("Read Program",self.read_program, None,None,
                                                           "Read program")
        self.upload_Program_ation = self.createAction("Upload Program",self.upload_program, None,None,
                                                           "Upload program")
        self.menuProgram.addActions([self.read_Program_ation,self.upload_Program_ation])                     
        
        
        self.menuAnalysis = self.menuBar().addMenu('&Online Analysis')
        self.launch_anal_action = self.createAction("Start Analysis",self.launch_online_analysis, None,None,
                                                           "Start analyzing data")
        self.menuAnalysis.addActions([self.launch_anal_action])
        self.menuHelp = self.menuBar().addMenu('&Help')
        
#        self.menuHelp.createActions("matteo.falappa@iit.it",None,None,None,"edoardo.balzani@iit.it",None,None,None,"IIT, February 2017",None,None,None)

        
        
        if len(self.pdict.keys())==0:
            self.upload_Program_ation.setEnable(False)
        
        if not self.MODE:
            self.sendMessage(Switch_to_Operational_State_Msg(MODE=self.MODE))  ## Importazione di una delle due librerie in corso d'opera
        
        
#        self.online_analysis_dlg = MainWindow()
    
#    def sendOneTest(self):
#        try:
#            Id = self.IDList[0]
#            msg = Start_Stop_Trial_Msg(Id,False,True,
#                                           self.source_address[Id],
#                                           MODE=self.MODE)
#            answ = getAnsw(msg, self.MODE)
#            self.stack_list += [[msg, answ]]
#            self.sendMessage(msg)
            
#        except:
#            pass
        
        
    
    def launch_online_analysis(self):
        if (not self.Phenopy) or not (self.Phenopy.poll() is None):
            self.Phenopy = Popen([executable,os.path.join(phenopy_dir,'mainAnalysis.py')])

    def startLightController(self):
        if not self.arduinoGui:
            found = False
            for val in list_ports.comports():
                port = val[0]
                descr = val[1]
                if 'ARDUINO' in descr.upper():
                    found = True
                    break
            if not found:
                print( 'Did not found an arduino conected')
#                QMessageBox.warning(self, 'Serial connection error', 'Could not find Arduino connected', buttons = QMessageBox.Ok, defaultButton = QMessageBox.NoButton)
                port = None
                return
            self.arduinoGui = timerGui(15,port,baud=9600,parent=self)
        self.arduinoGui.show()
        
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
        for Id in IDList: # lanciare solo per gabbie selezionate
            self.timerSaveDict[Id] = QTimer()
        for ind in range(len(IDList)):
            self.logString[IDList[ind]] = ''
            self.infoString[IDList[ind]] = ''
            self.dict_cage_widget[Id].clear()
            self.connect(self.timerSaveDict[IDList[ind]],SIGNAL('timeout()'),
                         lambda Id = IDList[ind] : self.saveLog(Id))
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
        for key in self.block_num.keys():
            self.block_num[key] = 0

        for Id in IDList:
            self.saveLog(Id)
        self.finalizing = True
        self.add_stack(msg_list)
        self.fileStartStandAloneAction.setEnabled(True)
    
        
    def recieveMsg(self,message):
        try:
            Type, Id, log = self.parsing_log(message)
            print 'Received ', Type, log,message
        except (TypeError, ValueError) as e:
            print e
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
                print 'added info...'
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
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action   

        

    def setSender(self):
        if len(self.pdict.keys()):
            answ = QMessageBox.question(self,'Change sender settings?', 'Current sender\nemail: %s\nserver: %s\nport: %s\nDo you want to change sender?'%(self.pdict['email'],self.pdict['server'],
                                        self.pdict['port']),QMessageBox.No|QMessageBox.Yes)
            if answ != 16384:
                return
        dialog = email_addr_add(parent=self)
        if dialog.exec_():
            self.pdict = dialog.pdict
        if len(self.pdict.keys()):
            self.fileStartStandAloneAction.setEnabled(True)
            self.receivers = [self.pdict['receivers']]
        else:
            self.fileStartStandAloneAction.setEnabled(False)
            
    def setReceivers(self):
        dialog = set_receiver_dlg(self.pdict['receivers'],self.pdict,
                                  self)
        dialog.show()
        
    
    def sendMessage(self,msg):   
        try:
            print 'Write message:',binascii.hexlify(msg)
        except: 
            print 'Write message:',msg
        
        self.serialPort.write(msg)
        return 
        
    def connectAdapter(self):
        """
            Connecting to the adapter via pycanusb.py 
        """
        try:
            
            self.serialPort = pycanusb.CanUSB(bitrate='500')
            self.mode = 'CAN'
            self.MODE = 0
            dialog = find_device_CAN(canusb=self.serialPort,parent=self)
            dialog.show()
            if not dialog.exec_():
                print 'ci prov'
                return False
            self.source_address = dialog.address_dict
            
        except AttributeError:
            print 'Exception handling' # aggiungo dialogo selezione com port 
            
            p = enumerate_serial_ports()
            for port in p:
                if '\\Device\\VCP' in port[1]:
                    self.wifi = True
                    print 'Try to open serial port'
                    self.serialPort = serial.Serial(port[0], baudrate=19200,
                                                    timeout=1)
                    dialog = find_device_Xbee(self.serialPort,parent=self)
                    dialog.show()
                    if not dialog.exec_():
                        return False
                    self.source_address = dialog.address_dict
                    
            
            self.mode = 'XBee'
            self.MODE = 1
        try:
            for key in self.source_address.keys():
                self.block_num[key] = 0
        except AttributeError:
            self.source_address = {}
            self.serialPort = None
            dialog = not_find_can_or_xbee(parent=self)
            dialog.show()
            if not dialog.exec_():
                return False
#        print('Serial Port: ',self.serialPort)
        return True
        
    def saveLog(self,Id):
        self.timerSaveDict[Id].stop()
        tmp = os.path.join(self.dict_cage_widget[Id].path2save,self.fileNames[Id])
        fh = open(tmp,'a')        
        fh.write(self.logString[Id])
        fh.close()
        self.logString[Id] = ''
        self.infoString[Id] = ''
        if not self.finalizing:
            self.timerSaveDict[Id].start(1800000)
        
    def setSavePath(self):
        if os.path.exists(self.saveFolderPath):
            pt = self.saveFolderPath
        else:
            pt = '.'
        dlg = change_dir_prog(self.IDList,parent=self,dir2save=pt)
        dlg.show()
        dlg.update_dir_signal.connect(self.update_dirs)
        
    def update_dirs(self,lisId,Dir):
       for Id in lisId:
            self.dict_cage_widget[Id].setPath2save(Dir)
                      
    def add_stack(self, list_of_msg):
        DT = 50
        if not self.stack_list:
            self.stack_counter = 0
        for msg in list_of_msg:
            answ = getAnsw(msg, self.MODE)
            self.stack_list += [[msg, answ]]
        if not self.timer_stack.isActive():
            self.timer_stack.start(DT)
    
    def write_if_stack(self):
        MAXCOUNTER = 10
        DT = 1500
        if self.stack_counter <= MAXCOUNTER:
            if self.stack_list:
                self.sendMessage(self.stack_list[0][0])
                self.timer_stack.stop()
                self.timer_stack.start(DT)
                self.stack_counter += 1
            else:
                self.stack_counter = 0
                self.timer_stack.stop()
        else:
            if self.stack_list:
                msg = self.stack_list.pop(0)[0]
                self.write_if_stack()
                self.stack_counter = 0
                string = 'Cannot send a message\n' + stringFromMsg(msg)
                dialog = QMessageBox(QMessageBox.Warning,'Cannot send a message',string,
                                QMessageBox.Ok,parent=self)
                dialog.show()
    
    def check_answ(self, msg):
        self.timer_stack.stop()
        if not self.stack_list:
            return
        cka = checkAnsw(self.stack_list[0], self.MODE)
#        if self.MODE and msg.has_key('rf_data'):
#            print('rf_data check answ: ', msg['rf_data'],self.stack_list[0][1],cka.check(msg))
#        elif self.MODE:
#            print('check answ: ', msg, self.stack_list[0][1],cka.check(msg))
#        else:
#            print('check answ: ', msg.dataAsHexStr(),self.stack_list[0][1],cka.check(msg))
        if cka.check(msg):
            self.stack_list.pop(0)
            self.stack_counter = 0
            self.write_if_stack()
    
    def start_message_gui(self):
        bl = self.get_not_recording_box()
        box_list = []
        for ID in bl:
            box_list += [(ID,self.source_address[ID])]
        self.microsystemGUI = msg_sender_gui(box_list=box_list, MODE=self.MODE, parent=self)
        self.microsystemGUI.sendGUImessage.connect(self.sendGUIMessage)
        self.microsystemGUI.show()
        self.launchMessageGUIAction.setEnabled(False)
        self.read_Program_ation.setEnabled(False)
        self.upload_Program_ation.setEnabled(False)
    
    def sendGUIMessage(self,msg_list):
        self.add_stack(msg_list)
        
    def closeEvent(self, event):
        if self.Phenopy:
            self.Phenopy.kill()
        settings = QSettings()
        settings.setValue("MainWindow/Geometry", 
                          self.saveGeometry())
        settings.setValue("MainWindow/State", 
                          self.saveState())
       
        settings.setValue('SaveDirectory',self.saveFolderPath)
        if len(self.pdict.keys()):
            np.save(os.path.join(os.curdir,'pdict.npy'),self.pdict)
        if self.MODE:
            self.Reader.terminate()
            if self.serialPort:
                self.serialPort.close()
        super(Msg_Server,self).close()
                

def readLastLine(pathToFile):
    if not os.path.exists(pathToFile):
        raise ValueError
    elif not pathToFile.endswith('tmpcsv'):
        raise ValueError
    with open(pathToFile, "rb") as f:
        try:
            f.seek(-2, 2)            # Jump to the second last byte.
            
            flag=True
            while flag:
                while f.read(1) != "\n": # Until EOL is found...
                    f.seek(-2, 1)        # ...jump back the read byte plus one more.
                last = f.readline() 
                Length = len(last)
    
                if Length>2:    # if the length of the line is greater than 2
                                # we are done
                    flag=False
                else:           # if the line is of 1 or two char go back to previous
                                # line. (tipically if you have final "\n" char or final "\r\n")
                    f.seek(-(Length+2),1)
            f.close()
        except:
            last = ''
        return last


def main():
    num_port = 0
    k = 0
    p = enumerate_serial_ports()
    for port in p:
        num_port += 1
        print port
    p=enumerate_serial_ports()
    for port in p:
        if '\\Device\\VCP' in port[1] :
#            ser = serial.Serial(port[0], baudrate=19200, timeout=1)
            break
        else:
            k+=1
            
#    found = False
#    for val in list_ports.comports():
#        port = val[0]
#        descr = val[1]
#        if 'USB' in descr.upper():
#            found = True
#            break
#    if not found:
#        print( 'Did not find any connection')
#        port = None
            

    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    d={}
    basedir = os.path.dirname(os.path.realpath(__file__))


    form = Msg_Server(d)
    form.show()
    app.exec_()
    return form
if __name__=='__main__':
    form = main()

        
#==============================================================================
#         Inserisci la relazione messaggio-risposta
#==============================================================================
