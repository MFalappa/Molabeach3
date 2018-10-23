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

import serial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep
import datetime
import sys
sys.path.append('/Users/Matte/Python_script/Phenopy/libraries/messageLib')
from house_light import *
from stop_box_dlg_arduino import *

class readSerial(QThread):
    msgReceived = pyqtSignal(bytes, name='messageReceived')
    def __init__(self,port,baud,freqRead=100,parent=None):
        super(readSerial,self).__init__(parent)
        self.serial = serial.Serial(port,baud,timeout=0.5)
        self.readTimer = QTimer()
        self.freqRead = freqRead
        self.readTimer.timeout.connect(self.readSerial)
        
    
    def run(self):
        self.exec_()
    
    def startReading(self):
        if self.isRunning() == False:
            self.start()
            self.readTimer.start(self.freqRead)
    
    def readSerial(self):
        inwait = self.serial.inWaiting()
        if inwait:
            char = self.serial.read()
        
            # search initial char
            if char != '=':
                if char != 'T':
                    return
            msg = ''
            
            while char != '\n':
                char = self.serial.read()
                msg += char
            msg = msg[:-2]
            self.msgReceived.emit(msg)
    
    def stopAll(self):
        if self.isRunning():
            self.readTimer.stop()
            self.exit()
            self.wait()
            self.terminate()
            self.serial.close()
            

class timerGui(QMainWindow):
    def __init__(self, numBox, port, colSpan=4, baud=9600,parent=None):
        super(timerGui,self).__init__(parent)
        if not port is None:
            self.reader = readSerial(port, baud, parent=self)
            self.reader.msgReceived.connect(self.parseMessage)
        else:
            self.reader = None
        self.resize(1180,835)
        self.setMaximumSize(1180,835)
        self.loopMinutes = {}
        self.loopIdx = {}
        self.startCycle = {}
        self.switchTime = {}
        self.lock = QReadWriteLock()
        self.savePath = os.path.curdir
        self.fhSave = None
        # Timer for switch light status
        self.checkTimeTimer = QTimer()
        
        # setup light status initial
        self.lightStatus = '0'*numBox
        self.numBox = numBox
        self.boxDict = {}
        gridLayout = QGridLayout()
        row = 1
        for k in range(numBox):
            self.boxDict[k] = house_light(k, numBox, parent=self)
            self.boxDict[k].updateDictSignal.connect(self.applyTimerSchedule)
            self.boxDict[k].groupBox_hopper.doubleClickSignal.connect(self.setUpLightCycle)
            col = (k+1) % colSpan
#            print col
            if col == 0:
                col = 4
                
            gridLayout.addWidget(self.boxDict[k], row, col)
            if col == 4:
                row += 1
                
        window = QWidget()
        window.setLayout(gridLayout)
        scrollArea = QScrollArea()
        scrollArea.setWidget(window)
        layout = QVBoxLayout()
        layout.addWidget(scrollArea)
        buttonStart = QPushButton('Start Timer')
        self.buttonStop = QPushButton('Stop Timer')
        self.buttonStop.setEnabled(False)
        self.buttonSavePath = QPushButton('Set Log Path')
        
        labelDir = QLabel('Save Path: ')
        font = QFont()
        font.setBold(True)
        labelDir.setFont(font)
        self.pathLabel = QLabel('Saving directory not set')
        spaceritem = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        hlayout = QHBoxLayout()
        hlayout.addSpacerItem(spaceritem)
        hlayout.addWidget(labelDir)
        hlayout.addWidget(self.pathLabel)
        hlayout.addWidget(self.buttonSavePath)
        hlayout.addWidget(self.buttonStop)
        hlayout.addWidget(buttonStart)
        layout.addLayout(hlayout)
        self.checkTimerThread = checkSwitchTime(self.numBox, self.boxDict, self.lock,parent=self)
        self.checkTimerThread.setUpDict(self.switchTime, self.loopIdx, self.loopMinutes)
        self.checkTimerThread.sendMsg.connect(self.write)
        
        self.connect(buttonStart,SIGNAL('clicked()'),self.startArduino)
        self.connect(self.buttonStop,SIGNAL('clicked()'),self.stopThread)
        self.connect(self.buttonSavePath,SIGNAL('clicked()'),self.setPath)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def setPath(self):
         folder = QFileDialog.getExistingDirectory(self,'Select Directory',self.savePath)
         self.savePath = folder
         self.pathLabel.setText(folder)
         
    def setUpLightCycle(self, num):
        list_recordings = []
        for box in range(self.numBox):
            if not self.boxDict[box].isRecording:
                list_recordings += [box]
        self.boxDict[num].setupLightCycle(list_recordings)
        
    def applyTimerSchedule(self,loopMinutes,lightStatus,switchTime):
        # upotential bug, must live ficed the timer
        try:
            self.lock.lockForRead()
            self.loopMinutes.update(loopMinutes)
            newLightStatus = ''
            for k in range(self.numBox):
                if k in lightStatus.keys():
                    newLightStatus += '%d'%lightStatus[k]
                else:
                    newLightStatus += self.lightStatus[k]
        finally:
            self.lock.unlock()
        try:
            self.lock.lockForWrite()
            self.lightStatus = newLightStatus
            self.startCycle.update(switchTime)
        
            # set change icon set/unset
            for k in loopMinutes.keys():
                self.boxDict[k].set_cycle(True, switchTime[k])
        finally:
            self.lock.unlock()
        
        
    def startArduino(self):
        self.buttonSavePath.setEnabled(False)
        
        # check for the box to be started
        boxToStart = []
        for k in range(self.numBox):
            if (not self.boxDict[k].isRecording) and self.boxDict[k].cycleSet:
                boxToStart += [k]
                
        if not len(boxToStart):
            return
        
        try:
            self.lock.lockForWrite()
            for k in range(len(boxToStart)):
                self.loopIdx[boxToStart[k]] = 0
        finally:
            self.lock.unlock()
            
        now = datetime.datetime.now() 
        
        
        # set up switch times for first iteration
                    
        removeBox = 0
        for k in range(len(boxToStart)):
            idx = boxToStart[k]
            if self.startCycle[idx] < now:
                QMessageBox.warning(self, 'Error in start timer', 'Could not start timer for box %d since the starting time precedes current time'%idx, buttons = QMessageBox.Ok, defaultButton = QMessageBox.NoButton)
                print 'Current time is posterior to start loop for box %d'%k
                removeBox += 1
                continue
            try:
                self.lock.lockForWrite()
                self.switchTime[idx] = self.startCycle[idx] #+ datetime.timedelta(0,int(60*self.loopMinutes[idx][self.loopIdx[idx]]))
                # set the flag status of the particular box
                self.boxDict[idx].set_recording(True)
                # disconnect groupbox
                self.boxDict[idx].groupBox_hopper.doubleClickSignal.disconnect()
            finally:
                self.lock.unlock()
        
        if len(boxToStart) == removeBox:
            return
#        # time to check switch status
#        if not self.checkTimeTimer.isActive():
#            self.checkTimeTimer.timeout.connect(self.checkSwitchLight)
#            self.checkTimeTimer.start(100)
        # start reading
        self.buttonStop.setEnabled(True)
        
        if self.reader:
            self.reader.startReading()
        
        if not self.fhSave:
            self.fhSave = open(os.path.join(self.savePath,'timerLog.txt'),'a')
            self.fhSave.write('Box\tSWitch_Type\tTime\n')
        if self.fhSave.closed:
            self.fhSave = open(os.path.join(self.savePath,'timerLog.txt'),'a')
        
        
        
        # switch leds
        firstMsg = QTimer()
        firstMsg.singleShot(1*10**3,self.writeFirst)
        
    def writeFirst(self):
        self.write(bytearray(self.lightStatus,'utf-8'))
        if not self.checkTimerThread.isRunning():
            self.checkTimerThread.startChecking()
        
    def stopThread(self):
        try:
            self.lock.lockForRead()
            boxToStop = []
            for k in range(self.numBox):
                if (self.boxDict[k].isRecording):
                    boxToStop += [k]
        finally:
            self.lock.unlock()
        dlg = stop_box_dlg_arduino(boxToStop,parent=self)
        dlg.show()
        dlg.stop_arduino_sig.connect(self.stopArduino)
        
    
    def stopArduino(self,boxToStop):
        try:
            self.lock.lockForWrite()
            msg = ''
            for box in boxToStop:
               self.boxDict[box].set_recording(False)
               self.boxDict[box].set_icon_light('Off')
               # removing cycle settings
               self.switchTime.pop(box)
               self.startCycle.pop(box)
               self.loopMinutes.pop(box)
               # reconnect groupbox
               self.boxDict[box].groupBox_hopper.doubleClickSignal.connect(self.setUpLightCycle)
            # create the message for switching off the lights
            for k in range(self.numBox):
                if k in boxToStop:
                    msg += '0'
                else:
                    msg += self.lightStatus[k]
            # check if any box is still light-cycling
            countRec = 0
            for box in self.boxDict.keys():
                countRec += self.boxDict[box].isRecording
            # stop tread
            if self.reader:
                self.write(bytearray(msg,'utf-8'))
            else:
                print msg
                
            self.lightStatus = msg
            # if no box are cycling, stop check timer, disable stop button
            if not countRec:
                self.checkTimerThread.terminate()
                self.checkTimerThread.wait()
                if self.checkTimerThread.checkTimer.isActive():
                    self.checkTimerThread.checkTimer.stop()
                self.buttonStop.setEnabled(False)
                self.buttonSavePath.setEnabled(True)
                if self.fhSave and (not self.fhSave.closed):
                    self.fhSave.close()
        
        finally:
            self.lock.unlock()

        
    def parseMessage(self, msg):
        print msg
        print("Message Parsed:", msg)
        now = datetime.datetime.now()
        if len(msg) != self.numBox:
            return
        box = 0
        for char in msg:
            if char == '1':
                self.boxDict[box].set_icon_light('On')
                if not self.fhSave.closed:
                    self.fhSave.write('%d\t'%(box + 1)+'On\t'+now.isoformat() + '\n')
            elif char == '0':
                self.boxDict[box].set_icon_light('Off')
                if not self.fhSave.closed:
                    self.fhSave.write('%d\t'%(box + 1)+'Off\t'+now.isoformat() + '\n')
            box += 1
               
    
        
    def write(self,msg):
        if self.reader:
            self.reader.serial.write(msg)
        print( 'Writing',msg)
    
    def closeEvent(self,event):
        if not self.reader:
            return
        self.write('0'*self.numBox)
        self.reader.stopAll()
        if self.fhSave and (not self.fhSave.closed):
            self.fhSave.close()
#        self.reader.start()

class checkSwitchTime(QThread):
    sendMsg = pyqtSignal(bytearray, name="sendMsgArduino")
    def __init__(self, numbox, boxDict, lock, parent=None):
        super(checkSwitchTime,self).__init__(parent)
        self.numBox = numbox
        self.parent = parent
        self.boxDict = boxDict
        self.lock = lock
        self.isReady = False
        self.checkTimer = QTimer()
        self.checkTimer.timeout.connect(self.checkSwitchLight)
    
    def setUpDict(self,switchTime,loopIdx,loopMinutes):
        self.switchTime = switchTime
        self.loopIdx = loopIdx
        self.loopMinutes = loopMinutes
        self.isReady = True
    
    def run(self):
        self.exec_()
        
    def checkSwitchLight(self):
        try:
            self.lock.lockForWrite()
            statusList = list(self.parent.lightStatus)
        
            now = datetime.datetime.now()
            anyswitch = False
            for k in range(self.numBox):
                
                if not k in self.switchTime.keys():
                    statusList[k] = '0'
                    continue
                if now >= self.switchTime[k]:
                    print('Switch led %d at %s'%(k,now.isoformat()))
                    anyswitch = True
                    
                    self.loopIdx[k] = (self.loopIdx[k] + 1) % len(self.loopMinutes[k])
                    if statusList[k] == '1':
                        statusList[k] = '0'
                    else:
                        statusList[k] = '1'
                    self.switchTime[k] = self.switchTime[k] + datetime.timedelta(0,int(60*self.loopMinutes[k][self.loopIdx[k]]))
                    self.boxDict[k].setDateTimeEdit(self.switchTime[k])
    #        print(self.switchTime)
            if anyswitch:
                self.parent.lightStatus = ''.join(statusList)
                self.sendMsg.emit(bytearray(self.parent.lightStatus,'utf-8'))
        finally:
            self.lock.unlock()
        
            
    def startChecking(self):
        if self.isRunning() == False:
            self.start()
            self.checkTimer.start(100)
           
        
def main():
    from serial.tools import list_ports
    import sys
    found = False
    for val in list_ports.comports():
        port = val[0]
        descr = val[1]
        if 'ARDUINO' in descr.upper():
            found = True
            break
    if not found:
        print( 'Did not found an arduino conected')
        port = None
    app = QApplication(sys.argv)
    TG = timerGui(15,port,baud=9600)
    TG.show()
    app.exec_()
        
if __name__== '__main__':
    main()
