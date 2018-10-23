# -*- coding: utf-8 -*-
"""
This file is part of pyQanmon.

pyQanmon is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyQanmon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyQanmon.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2010, Martin Gysel
"""

from PyQt4 import QtCore, QtGui, uic
import pycanusb

class CANTableMsgGeneric(QtGui.QWidget):
    def __init__(self, parent = None):
        super(CANTableMsgGeneric, self).__init__(parent)
        uic.loadUi("./tmessage.ui", self)
        
        self.idTable.cellClicked.connect(self._cellClicked)
        
        self.canId = 0
        
    def _cellClicked(self, x, y):
        pass
        
    def setSendRecv(self, recv):
        self.sendButton.clicked.connect(recv)
        
    def getMsg(self):
        pass


class CANTableMsg(CANTableMsgGeneric):
    def __init__(self, parent = None):
        super(CANTableMsg, self).__init__(parent)
        
        self.idTable.setSpan(0,0,1,29)
        self.idTable.setSpan(1,0,1,10)
        self.idTable.setSpan(1,10,1,19)
        self.extId.setCheckState(QtCore.Qt.PartiallyChecked)
        
        self.canId = 0
        
    def _cellClicked(self, x, y):
        print x, y
        if x == 2:
            if self.idTable.item(x,y).text() == '0':
                self.idTable.setItem(x,y, QtGui.QTableWidgetItem('1'))
            else:
                self.idTable.setItem(x,y, QtGui.QTableWidgetItem('0'))
            
            val = 0
            val_e = 0
            for i in range(29):
                val = val + int(self.idTable.item(2,28-i).text()) * 2**i
                if i == 18:
                    val_e = val
            val_s = (val - val_e)>>19
            self.idTable.setItem(0,0, QtGui.QTableWidgetItem(str(val)))
            self.idTable.setItem(1,10, QtGui.QTableWidgetItem(str(val_e)))
            self.idTable.setItem(1,0, QtGui.QTableWidgetItem(str(val_s)))
            self.canId = val
        
    def getMsg(self):
        msg = pycanusb.CANMsg()
        
        msg.id = self.canId
        msg.len = int(str(self.length.text()))
        
        dat = str(self.data.currentText())
        if (self.formatData.currentText() == 'Hex'):
            dat = dat[:msg.len*2]
            dat = dat.ljust(msg.len*2,'0')
            for i in range(msg.len):
                msg.data[i] = int(dat[:2],16)
                dat = dat[2:]
        elif (self.formatData.currentText() == 'Bin'):
            dat = dat[:msg.len*8]
            dat.ljust(msg.len*8,'0')
            for i in range(msg.len):
                msg.data[i] = int(dat[:8],2)
                dat = dat[8:]
        
        if self.extId.checkState() == QtCore.Qt.Checked:
            msg.flags |= pycanusb.CANMSG_EXTENDED
        elif self.extId.checkState() == QtCore.Qt.PartiallyChecked:
            if msg.id > 2047:
                msg.flags |= pycanusb.CANMSG_EXTENDED
        
        return msg

class CANMMsg(CANTableMsgGeneric):
    def __init__(self, parent = None):
        super(CANMMsg, self).__init__(parent)
        
        self.idTable.setSpan(0,0,1,29)
        self.idTable.setSpan(1,0,1,2)
        self.idTable.setSpan(1,2,1,8)
        #self.idTable.setSpan(1,10,1,2)
        self.idTable.setSpan(1,12,1,8)
        self.idTable.setSpan(1,20,1,8)
        
        self.idTable.setItem(1,10, QtGui.QTableWidgetItem('0'))
        self.idTable.setItem(1,11, QtGui.QTableWidgetItem('0'))
        self.idTable.setItem(1,28, QtGui.QTableWidgetItem('0'))
        
        self.msgPrioBox = QtGui.QSpinBox(self.idTable)
        self.msgPrioBox.setRange(0,3)
        self.idTable.setCellWidget(1, 0, self.msgPrioBox)
        
        self.addrBox = QtGui.QComboBox(self.idTable)
        self.addrBox.addItem('00000000')
        self.addrBox.addItem('11111111')
        self.idTable.setCellWidget(1, 2, self.addrBox)
        
        self.origBox = QtGui.QComboBox(self.idTable)
        self.origBox.addItem('00000000')
        self.origBox.addItem('11111111')
        self.idTable.setCellWidget(1, 12, self.origBox)
        
        self.cmdBox = QtGui.QComboBox(self.idTable)
        self.idTable.setCellWidget(1, 21, self.cmdBox)
        
        self.extId.setCheckState(QtCore.Qt.Checked)
        
    def _cellClicked(self, x, y):
        print x, y
        if x == 1 and y == 28:
            if self.idTable.item(x,y).text() == '0':
                self.idTable.setItem(x,y, QtGui.QTableWidgetItem('1'))
                self.idTable.setItem(x+1,y, QtGui.QTableWidgetItem('1'))
            else:
                self.idTable.setItem(x,y, QtGui.QTableWidgetItem('0'))
                self.idTable.setItem(x+1,y, QtGui.QTableWidgetItem('0'))
            