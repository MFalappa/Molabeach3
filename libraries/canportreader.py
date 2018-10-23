# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:13:21 2010

@author: Gysel
"""

from PyQt4 import QtCore
from pycanusb import CANMsg
from time import clock

class CanPortReader(QtCore.QThread):
    received = QtCore.pyqtSignal(CANMsg, name='canReceived')
    """ Description: A Thread which handles incoming and outgoing traffic. """
    def __init__(self, canPort = None, receiver = None, sampleRate = 100):
        super(CanPortReader, self).__init__()
        
        self._canPort = canPort
        self._recv = receiver
        print 'receiver in canport reader:', self._recv
        print(sampleRate)
        self._readTimer = QtCore.QTimer()
        self._sampleRate = sampleRate #in Millisekunden         
        self._readTimer.timeout.connect(self.__canPortReader)        
        
        self._statTimer = QtCore.QTimer()
        self._statRate = sampleRate #in Millisekunden         
        self._statTimer.timeout.connect(self.__printStat)        
        
        self.stat = None
        
        if self._recv != None:
            self.received.connect(self._recv)

    def setCanPort(self, canPort):
        self._canPort = canPort
    def getCanPort(self):
        return self._canPort
        
    def setReciever(self, receiver):
        self._recv = receiver
    def getReceiver(self):
        return self._recv
                
    def startReading(self):
        if self.isRunning() == False:
            print 'starting'
            #if not self._canPort.isOpen():
            #    self._canPort.open()
            
            self.start()
            print 'start ok'
            ####### LEVARE LA RIGA SOTTO
#            self.myt=clock()
            self._readTimer.start(self._sampleRate)
#            print 'start timer'
            self._statTimer.start(self._statRate)
#            print 'start timer 2'
    def stopReading(self):
        print 'stop reading called'
        if self.isRunning() == True:            
            #self._serialPort.close()
            self._readTimer.stop()
            
            self.exit()
            self.wait()
            self.terminate()

    
    def __canPortReader(self):
        """and self._serialPort.isOpen():"""
        
#        if self._canPort != None:
        try:
#            print 'Not none', self._canPort
            #msg = pycanusb.CANMsg()
#            print('Qui non funziona')
#            t0=clock()
#            print('From Start Timer: ',t0-self.myt)
#            print 'reader entered'
            msg = self._canPort.read()
#            print 'read ok'
#            print 'msg',msg
#            print(t1-t0)
            if msg != None and msg != False:
                self.received.emit(msg)
        except:
            pass
        
    def __printStat(self):
#        print 'stat in'
        stat = self._canPort.getStatistics()
        
#        print 'Stat:',stat
        if stat != self.stat:
            self.stat = stat
#            print stat
#        print 'status on'
        stat = self._canPort.status(True)
#        print 'status off'
#        if stat != '':
#            print "Status: %s" % stat

    def run(self):
        returnCode = self.exec_()
        """
        Thread wird immer mit Fehler beendet. Fehlerhafter Returnwert.
        if returnCode != 0:
            DebugMessage().printOut("ComportIO().run(): Fehler beim beenden von Thread.", 1)
        """
        return returnCode
