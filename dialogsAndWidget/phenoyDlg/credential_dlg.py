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
from passlib.hash import pbkdf2_sha256
import numpy as np

class autentication_dlg(QDialog):
    def __init__(self, pdict,parent=None):
        super(autentication_dlg,self).__init__(parent)
        self.pdict = pdict
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        label = QLabel()
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        label.setText(pdict['email'])
        v_layout.addWidget(label)
        label_psw = QLabel("Password: ")
        self.edit_psw = QLineEdit()
        self.edit_psw.setEchoMode(QLineEdit.Password)
        h_layout.addWidget(label_psw)
        h_layout.addWidget(self.edit_psw)
        v_layout.addLayout(h_layout)
        h_layout = QHBoxLayout()
        pushOk = QPushButton('Ok')
        pushCancel = QPushButton('Cancel')
        spaceritem = QSpacerItem(0,0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label = QLabel("")
        h_layout.addSpacerItem(spaceritem)
        h_layout.addWidget(self.label)
        v_layout.addLayout(h_layout)
        
        h_layout = QHBoxLayout()
        spaceritem = QSpacerItem(20,40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addSpacerItem(spaceritem)
        h_layout.addWidget(pushCancel)
        h_layout.addWidget(pushOk)
        v_layout.addLayout(h_layout)
        self.connect(pushOk,SIGNAL('clicked()'),self.checkpsw)
        self.connect(pushCancel,SIGNAL('clicked()'),self.reject)
        self.setLayout(v_layout)
        
    def checkpsw(self):
        if pbkdf2_sha256.verify(self.edit_psw.text(),self.pdict['password']):
            self.accept()
        else:
            self.edit_psw.setText("")
            palette = QPalette()
            palette.setColor(QPalette.Foreground,Qt.red)
            self.label.setPalette(palette)
            self.label.setText('Wrong password!')
            
def main():
    pdict = np.load(os.path.join(classes_dir,'pdict.npy')).all()
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    form = autentication_dlg(pdict)
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()