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
import os,sys
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses')
sys.path.append(classes_dir)
from ui_load_program_dlg import Ui_Dialog
from messageLib import *

from check_prog import *
from Parser import parsing_Funct
from ui_change_path_dlg import *


class change_dir_prog(Ui_Dialog,QDialog):
    update_dir_signal = pyqtSignal(list, str, name='setSavePath')
    def __init__(self, IDList, parent=None, dir2save='.'):
        super(change_dir_prog, self).__init__(parent)
        self.parent = parent
        self.dir2save = dir2save
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.IDList = IDList
        
        self.pushButton_apply.setEnabled(False)
        
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
        
        self.connect(self.lineEdit_search,SIGNAL('textChanged(const QString&)'),self.setDirEnable)
        self.connect(self.pushButton_search,SIGNAL('clicked()'),self.search_dir)
        self.connect(self.pushButton_apply,SIGNAL('clicked()'),self.emit_signal_dir)
        self.connect(self.box_group,SIGNAL('buttonClicked (QAbstractButton*)'),self.box_checked)
        self.connect(self.checkBox_select_all,SIGNAL('clicked(bool)'),self.select_all_clicked)
        self.connect(self.pushButton_done,SIGNAL('clicked()'),self.close)
        
    def select_all_clicked(self,tof):
        if tof:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(True)
        else:
            for Id in self.IDList:
                self.dictChecker[Id].setChecked(False)
                
    def box_checked(self,button):
        self.checkBox_select_all.setChecked(False)
    
        
    def search_dir(self):
        Dir = QFileDialog.getExistingDirectory(self, "Open Directory",
                                                 self.dir2save,
                                                 QFileDialog.ShowDirsOnly
                                                 | QFileDialog.DontResolveSymlinks)
        self.lineEdit_search.setText(Dir)
        self.setDirEnable()
    
    def setDirEnable(self):
        path = self.lineEdit_search.text()
        if os.path.exists(path) and os.path.isdir(path):
                self.pushButton_apply.setEnabled(True)
                self.pushButton_apply.setFocus()
        else:
            self.pushButton_apply.setEnabled(False)

        
    def get_checked(self):
        checked_list = []
        for Id in self.dictChecker.keys():
            if self.dictChecker[Id].isChecked():
                checked_list += [Id]
        return checked_list
        
    def emit_signal_dir(self):
        self.update_dir_signal.emit(self.get_checked(),self.lineEdit_search.text())
    
    def test(self,l,d):
        print l
        print d
def main():
    import sys
    app = QApplication(sys.argv)
    form = change_dir_prog(range(20))
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()