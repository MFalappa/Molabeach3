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
 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_load_program_dlg import Ui_Dialog
from messageLib import *
import os,sys
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses')
library_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')

sys.path.append(classes_dir)
sys.path.append(library_dir)

from check_prog import *
from Parser import parsing_Funct
from uploadProg_gui import *


        
class load_program_dlg(Ui_Dialog,QDialog):
    def __init__(self, IDList, parent=None):
        super(load_program_dlg, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.IDList = IDList
        
        self.pushButton_load.setEnabled(False)
        
        # CREATE A CHECKER BOX LIST
        self.dictChecker = {}
        self.box_group = QButtonGroup(parent=self)
        self.box_group.setExclusive(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        for Id in self.IDList:
            self.dictChecker[Id] = QCheckBox("Box %d"%Id)
            self.box_group.addButton(self.dictChecker[Id])
            self.dictChecker[Id].setFont(font)
            self.verticalLayout_4.addWidget(self.dictChecker[Id])
            self.dictChecker[Id].setChecked(True)
        
        spaceritem = QSpacerItem(0,0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addSpacerItem(spaceritem)
        
        self.connect(self.lineEdit_search,SIGNAL('textChanged(const QString&)'),self.setLoadEnabled)
        self.connect(self.pushButton_search,SIGNAL('clicked()'),self.search_prg)
        self.connect(self.pushButton_load,SIGNAL('clicked()'),self.load_prg)
        self.connect(self.box_group,SIGNAL('buttonClicked (QAbstractButton*)'),self.box_checked)
        self.connect(self.checkBox_select_all,SIGNAL('clicked(bool)'),self.select_all_clicked)
        self.connect(self.pushButton_close,SIGNAL('clicked()'),self.close)
        
    def select_all_clicked(self,tof):
        if tof:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(True)
        else:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(False)
                
    def box_checked(self,button):
        self.checkBox_select_all.setChecked(False)
    
        
    def search_prg(self):
        pathToText = unicode(QFileDialog.getOpenFileName(self,"Program to upload",os.path.curdir,"Programs available (*.txt *.prg)"))
        self.lineEdit_search.setText(pathToText)
            
    
    def setLoadEnabled(self):
        path = self.lineEdit_search.text()
        if os.path.exists(path) and (path.endswith('.prg') or path.endswith('.txt')):
            tof, sentence = check_prog(path)
            if tof:
                self.textBrowser.setText('Ok! '+sentence)
                self.pushButton_load.setEnabled(True)
                self.pushButton_load.setFocus()
            else:
                self.pushButton_load.setEnabled(False)
                self.textBrowser.setText(sentence)
        else:
            self.pushButton_load.setEnabled(False)
            self.textBrowser.setText('Invalid file name...')
        
    def get_checked(self):
        checked_list = []
        for Id in self.dictChecker.keys():
            if self.dictChecker[Id].isChecked():
                checked_list += [Id]
        return checked_list
    
    def load_prg(self):
        path = self.lineEdit_search.text()
        checked_list = self.get_checked()
        for Id in checked_list:
            msg_list = parsing_Funct(path,Id)
            try:
                isLast = Id == checked_list[-1]
                dialog = uploadProgram_gui(msg_list,Id,isLast=isLast,parent=self.parent)
                dialog.exec_()
            except Exception,e:
                print e
                print Id, 'First message', msg_list[0]
    
    def closeEvent(self,event):
        self.parent.read_Program_ation.setEnabled(True)
        self.parent.upload_Program_ation.setEnabled(True)
        self.parent.launchMessageGUIAction.setEnabled(True)
        super(load_program_dlg, self).close()
                
def main():
    import sys
    app = QApplication(sys.argv)
    form = load_program_dlg(range(20))
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()