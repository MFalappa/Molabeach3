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
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses')
sys.path.append(classes_dir)
sys.path.append(lib_dir)
from PyQt5.QtWidgets import (QDialog,QButtonGroup,QCheckBox,
                             QSpacerItem,QSizePolicy,QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,pyqtSignal
from ui_load_program_dlg import Ui_Dialog
from messageLib import switch_Lights_Msg,Start_Stop_Trial_Msg

from check_prog import *
from Parser import parsing_Funct
from ui_start_box_dlg import *


        
class start_box_dlg(Ui_Dialog,QDialog):
    start_signal = pyqtSignal(list,list, name='start_signal')
    def __init__(self, IDList, parent=None,source_address=None, MODE=0 ):
        super(start_box_dlg, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.IDList = IDList
        self.mode = MODE
        self.sa_dictionary = source_address
#        self.start_signal.connect(self.test)
        
        # CREATE A CHECKER BOX LIST
        self.dictChecker = {}
        self.box_group = QButtonGroup(parent=self)
        self.box_group.setExclusive(False)
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        for Id in self.IDList:
            self.dictChecker[Id] = QCheckBox("Box %d"%Id,parent=self.scrollAreaWidgetContents)
            self.box_group.addButton(self.dictChecker[Id])
            self.dictChecker[Id].setFont(font)
            self.verticalLayout_4.addWidget(self.dictChecker[Id])
            self.dictChecker[Id].setChecked(True)
        
        spaceritem = QSpacerItem(0,0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addSpacerItem(spaceritem)
        
        self.pushButton_start.clicked.connect(self.emit_signal_start)
        self.pushButton_cancel.clicked.connect(self.close)
        self.checkBox_select_all.clicked.connect(self.select_all_clicked)
#        self.connect(self.pushButton_start,SIGNAL('clicked()'),self.emit_signal_start)
#        self.connect(self.pushButton_cancel,SIGNAL('clicked()'),self.close)
#        self.connect(self.checkBox_select_all,SIGNAL('clicked(bool)'),self.select_all_clicked)

    def select_all_clicked(self,tof):
        if tof:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(True)
        else:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(False)
                
    def box_checked(self,button):
        self.checkBox_select_all.setChecked(False)
    
        
    def get_checked(self):
        checked_list = []
        for Id in list(self.dictChecker.keys()):
            if self.dictChecker[Id].isChecked():
                checked_list += [Id]
        return checked_list
        
    def emit_signal_start(self):
        msg_list = []
        idList = self.get_checked()
        for box in idList:
            msg_list += [switch_Lights_Msg(box,0,0,0,source_address=self.sa_dictionary[box], MODE=self.mode)]
            msg_list += [Start_Stop_Trial_Msg(box,True,Stand_Alone=True,source_address=self.sa_dictionary[box], MODE=self.mode)]
        self.start_signal.emit(msg_list,idList)
 
    
#    def test(self,l,d):
#        print(l)
#        print(d)
def main():
    import sys
    app = QApplication(sys.argv)
    form = start_box_dlg(list(range(20)))
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()