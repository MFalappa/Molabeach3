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

import sys,os
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses')
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
sys.path.append(classes_dir)
sys.path.append(lib_dir)
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_read_prog_gui import Ui_Dialog
from messageLib import *
from check_prog import *
from Parser import parsing_Funct
from uploadProg_gui import *
from readProg_gui import *
import datetime as dt

class read_program_dlg(Ui_Dialog,QDialog):
    def __init__(self, IDList, parent=None):
        super(read_program_dlg, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.IDList = IDList
        
        # salvataggio row e translated
        self.row_dict = {}
        self.transl_dict = {}
        
        # Create check box list
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
            self.verticalLayout_5.addWidget(self.dictChecker[Id])
            self.dictChecker[Id].setChecked(True)
        
        spaceritem = QSpacerItem(0,0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addSpacerItem(spaceritem)
        
        # set enabled state
        self.checkBox_select_all.setChecked(True)
        self.pushButton_save.setEnabled(False)
        
        # Connect check box
        self.connect(self.box_group,SIGNAL('buttonClicked (QAbstractButton*)'),self.box_checked)
        self.connect(self.checkBox_select_all,SIGNAL('clicked(bool)'),self.select_all_clicked)
        self.connect(self.pushButton_readprog,SIGNAL('clicked()'),self.readprog)
        self.connect(self.pushButton_close,SIGNAL('clicked()'),self.close)
        self.connect(self.pushButton_save,SIGNAL('clicked()'),self.save)
        
    def readprog(self):
        self.textBrowser__transl.setText('')
        self.textBrowser_row.setText('')
        self.pushButton_save.setEnabled(False)
        for Id in self.IDList:
            if self.dictChecker[Id].isChecked():
                readProg = readProgram(self.row_dict,self.transl_dict,parent=self,Id=Id)
                readProg.exec_()
                self.textBrowser__transl.append('Box %d:\n'%Id+self.transl_dict[Id])
                self.textBrowser_row.append('Box %d:\n'%Id+'\n'.join(self.row_dict[Id]))
        
        self.pushButton_save.setEnabled(True)
        
    def save(self):
        path = unicode(QFileDialog.getExistingDirectory(self,"Select save folder",os.path.curdir))        
        for Id in self.IDList:
            if self.dictChecker[Id].isChecked():
                now = dt.datetime.now()
                string = '\n'.join(self.row_dict[Id])
                fhname = '%d_%d_%d_%d_%d_box_%d_row.txt'%(now.year,now.month,now.day,now.hour,now.minute,Id)
                fh = open(os.path.join(path, fhname),'w')
                fh.write(string)
                fh.close()
                string = self.transl_dict[Id]
                fhname = '%d_%d_%d_%d_%d_box_%d_translated.txt'%(now.year,now.month,now.day,now.hour,now.minute,Id)
                fh = open(os.path.join(path, fhname),'w')
                fh.write(string)
                fh.close()
        
    def select_all_clicked(self,tof):
        if tof:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(True)
        else:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(False)
                
    def box_checked(self,button):
        self.checkBox_select_all.setChecked(False)
    
    def closeEvent(self,event):
        self.parent.read_Program_ation.setEnabled(True)
        self.parent.upload_Program_ation.setEnabled(True)
        self.parent.launchMessageGUIAction.setEnabled(True)
        super(read_program_dlg, self).close()

def main():
    import sys
    app = QApplication(sys.argv)
    form = read_program_dlg(range(20))
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()    