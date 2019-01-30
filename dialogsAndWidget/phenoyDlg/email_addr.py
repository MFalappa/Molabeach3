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

import os
import sys
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'classes','phenopyClasses')
sys.path.append(classes_dir)

from PyQt5.QtWidgets import (QLineEdit,QDialog,QApplication)
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import (Qt,pyqtSlot)
from passlib.hash import pbkdf2_sha256
from validate_email import validate_email

import ui_email_addr
from smtplib import SMTP


class email_addr_add(QDialog,ui_email_addr.Ui_Form):
    def __init__(self,parent=None):
        """
          self.lineEdit = account
          self.lineEdit_2 = psw
          self.lineEdit_3 = server
          self.spinBox = Port
        """
        super(email_addr_add,self).__init__(parent)        
        self.setupUi(self)
        self.pushButtonOk.setEnabled(False)
        self.pushButton_email.setEnabled(False)
        self.spinBox.setRange(1,999)
        self.spinBox.setValue(587)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
   
    @pyqtSlot("QString")
    def on_lineEdit_textEdited(self):
        self.checkfields()
    @pyqtSlot("QString")
    def on_lineEdit_2_textEdited(self):
        self.checkfields()
    @pyqtSlot("QString")
    def on_lineEdit_3_textEdited(self):
        self.checkfields()
    @pyqtSlot("QString")
    def on_lineEdit_4_textEdited(self):
        self.checkfields()
    @pyqtSlot("QString")
    def on_pushButtonOk_clicked(self):
        self.accept()
    @pyqtSlot("QString")
    def on_pushButton_email_clicked(self):
        try:
            smtpObj = SMTP(host=self.lineEdit_3.text(),port=self.spinBox.value())   
            print(smtpObj.ehlo())
            print(smtpObj.starttls())
            print(smtpObj.login(self.lineEdit.text(),self.lineEdit_2.text()))
            message = """From: From Person %s
To: To Person %s
Subject: Test email

This is a test e-mail message."""%(self.lineEdit.text(),self.lineEdit_4.text())
            smtpObj.sendmail(self.lineEdit.text(), [self.lineEdit_4.text()],
                             message)
            palette = QPalette()
            palette.setColor(QPalette.Foreground,Qt.green)
            self.label.setPalette(palette)
            self.label.setText("Email succesfully sent")
            smtpObj.close()
        except Exception:
            palette = QPalette()
            palette.setColor(QPalette.Foreground,Qt.red)
            self.label.setPalette(palette)
            self.label.setText("Unable to send email")
            try:
                smtpObj.close()
            except:
                pass
    def checkfields(self):
        account = self.lineEdit.text()
        email_flag = validate_email(account)
        psw_flag = len(self.lineEdit_2.text()) > 0
        server = self.lineEdit_3.text()
        server_flag = len(server)
        if email_flag * psw_flag * server_flag:
            self.pushButtonOk.setEnabled(True)
            if validate_email(self.lineEdit_4.text()):
                self.pushButton_email.setEnabled(True)
            else:
                self.pushButton_email.setEnabled(False)
        else:
            self.pushButtonOk.setEnabled(False)
            self.pushButton_email.setEnabled(False)
    def accept(self):
        self.pdict = {'email': self.lineEdit.text(),
                      'password': pbkdf2_sha256.encrypt(self.lineEdit_2.text(),
                                                        rounds=200000,
                                                        salt_size=16),
                      'server': self.lineEdit_3.text(),
                      'port': self.spinBox.value(),
                      'receivers': [self.lineEdit.text()]}
        QDialog.accept(self)
    
    @pyqtSlot("QString")
    def on_pushButton_clicked(self):
        self.reject()
if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = email_addr_add()
    ans = form.exec_()
    print(ans)
    app.exec_()
    
#main()