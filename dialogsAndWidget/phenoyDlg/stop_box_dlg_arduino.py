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
sys.path.append(os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries'))
sys.path.append(os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses'))
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_stop_box_dlg import *

class stop_box_dlg_arduino(Ui_Dialog,QDialog):
    stop_arduino_sig = pyqtSignal(list, name='stop_arduino_sig')
    def __init__(self, recordinBox, parent=None):
        super(stop_box_dlg_arduino, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.recordinBox = recordinBox
        self.stop_arduino_sig.connect(self.test)
        
        self.groupBox_select.setTitle("     Running box     ")
#        self.pushButton_stop.setStyleSheet("QPushButton { background-color: black }")
#        self.pushButton_cancel.setStyleSheet("QPushButton{ background-color: white }")
        spaceritem = QSpacerItem(0,0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addSpacerItem(spaceritem)

        # CREATE A CHECKER BOX LIST
        self.dictRec = {}
        self.box_group = QButtonGroup(parent=self)
        self.box_group.setExclusive(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        for box in self.recordinBox:
            self.dictRec[box] = QCheckBox("Box %d"%(box+1),parent=self.scrollAreaWidgetContents)
            self.box_group.addButton(self.dictRec[box])
            self.dictRec[box].setFont(font)
            self.verticalLayout_4.addWidget(self.dictRec[box])
            self.dictRec[box].setChecked(True)
        
        self.connect(self.pushButton_stop,SIGNAL('clicked()'),self.emit_signal_stop)
        self.connect(self.pushButton_cancel,SIGNAL('clicked()'),self.close)
        self.connect(self.checkBox_select_all,SIGNAL('clicked(bool)'),self.all_click)
        
        

    def all_click(self,tof):
        if tof:
            for box in self.recordinBox:
                self.dictRec[box].setChecked(True)
        else:
            for box in self.recordinBox:
                self.dictRec[box].setChecked(False)
                
    def box_checked(self,button):
        self.checkBox_select_all.setChecked(False)
    
        
    def get_checked(self):
        checked_list = []
        for box in self.dictRec.keys():
            if self.dictRec[box].isChecked():
                checked_list += [box]
        return checked_list
        
    def emit_signal_stop(self):
        recordinBox = self.get_checked()
        self.stop_arduino_sig.emit(recordinBox)
        self.close()
    
    def test(self,recordinBox):
        print recordinBox
     
def main():
    import sys
    app = QApplication(sys.argv)
    form = stop_box_dlg_arduino(range(16))
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()