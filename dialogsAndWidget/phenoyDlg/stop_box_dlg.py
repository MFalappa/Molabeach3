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
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_load_program_dlg import Ui_Dialog
from messageLib import *
from check_prog import *
from Parser import parsing_Funct
from ui_stop_box_dlg import *


        
class stop_box_dlg(Ui_Dialog,QDialog):
    stop_signal = pyqtSignal(list,list, name='stop_signal')
    def __init__(self, IDList, parent=None,source_address=None, MODE=0 ):
        super(stop_box_dlg, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.IDList = IDList
        self.mode = MODE
        self.sa_dictionary = source_address
        self.stop_signal.connect(self.test)
        
        # CREATE A CHECKER BOX LIST
        self.dictChecker = {}
        self.box_group = QButtonGroup(parent=self)
        self.box_group.setExclusive(False)
        font = QtGui.QFont()
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
        
        self.connect(self.pushButton_stop,SIGNAL('clicked()'),self.emit_signal_stop)
        self.connect(self.pushButton_cancel,SIGNAL('clicked()'),self.close)
        self.connect(self.checkBox_select_all,SIGNAL('clicked(bool)'),self.select_all_clicked)

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
        for Id in self.dictChecker.keys():
            if self.dictChecker[Id].isChecked():
                checked_list += [Id]
        return checked_list
        
    def emit_signal_stop(self):
        msg_list = []
        idList = self.get_checked()
        for box in idList:
            msg_list += [switch_Lights_Msg(box,0,0,0,source_address=self.sa_dictionary[box], MODE=self.mode)]
            msg_list += [Start_Stop_Trial_Msg(box,False,Stand_Alone=True,source_address=self.sa_dictionary[box], MODE=self.mode)]
        self.stop_signal.emit(msg_list,idList)
    
    def test(self,l,d):
        print l
        print d
def main():
    import sys
    app = QApplication(sys.argv)
    form = stop_box_dlg(range(20))
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()