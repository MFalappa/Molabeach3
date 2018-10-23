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
import numpy as np
#from email_addr import email_addr_add
import czipfile
from smtplib import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
import os
import getpass
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class autentication_dlg(QDialog):
    def __init__(self, email,parent=None):
        super(autentication_dlg,self).__init__(parent)
        self.pdict = {}
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        label = QLabel()
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        label.setText(email)
        v_layout.addWidget(label)
        label_psw = QLabel("Password: ")
        self.edit_psw = QLineEdit()
        self.edit_psw.setEchoMode(QLineEdit.Password)
        h_layout.addWidget(label_psw)
        h_layout.addWidget(self.edit_psw)
        v_layout.addLayout(h_layout)
        h_layout = QHBoxLayout()
        self.pushOk = QPushButton('Ok')
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
        h_layout.addWidget(self.pushOk)
        v_layout.addLayout(h_layout)
        
        self.connect(pushCancel,SIGNAL('clicked()'),self.reject)
        self.setLayout(v_layout)
        

class mysend_email(autentication_dlg):
    def __init__(self, email_sender,email_recievers, file_to_send, server, port,
                 mail_body='', mail_object='',parent=None):
        """
        Input:
        ======
            email_sender :
            --------------
                string, email address sender
            email_recievers : 
            --------------------
                list, list of email addresses of receivers
            file_to_send : 
            --------------
                string, attachment to be sent
            server :
            --------
                string, server name
            port :
            ------
                int, port number
            mail_body : 
            -----------
                string, mail body
            mail_object : 
            -----------
                string, mail subject
                
        """
        super(mysend_email, self).__init__(email_sender,parent)
        self.file = file_to_send
        self.sender = email_sender
        self.receivers = email_recievers
        self.mail_body = mail_body
        self.mail_object = mail_object
        self.port = port
        self.server = server
        self.connect(self.pushOk,SIGNAL('clicked()'),self.send_email)
        
    def set_body(self,mail_body):
        self.mail_body = mail_body
    
#    def set_psw(self):
#        dialog = autentication_dlg(self.sender)
#        if not dialog.exec_():
#            return
#        self.__password = dialog.edit_psw.text()
    
    def set_object(self,mail_object):
        self.mail_object = mail_object
        
    def send_email(self):
        self.__psw = self.edit_psw.text()
        try:
            smtpObj = SMTP(host=self.server,
                           port=self.port)
#            print self.__psw
            print smtpObj.ehlo()
            print smtpObj.starttls()
            print smtpObj.login(self.sender, self.__psw)
            message = MIMEMultipart()
            message['Subject'] = self.mail_object
            message['From'] = self.sender
            message['To'] = ','.join(self.receivers)
            message.attach(MIMEText(self.mail_body))
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(self.file, "rb").read())
            Encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment; filename="%s"'%os.path.basename(self.file))
#
            message.attach(part)
            smtpObj.sendmail(self.sender,
                             self.receivers,
                             message.as_string())
            self.accept()
        except Exception, e:
            print e
            print 'Unable to send email'
            self.reject()
            pass

def zip_my_file(file_list,zip_name = 'myfile.zip'):
    zf = czipfile.ZipFile(zip_name,'w')
    for f in file_list:
        zf.write(f,os.path.basename(f))
    zf.close()
    
    
def main():
    app = QApplication(sys.argv)
    sender = 'edoardo.balzani87@gmail.com'
    receiver=['edoardo.balzani@iit.it']
    port = 587
    server = 'smtp.googlemail.com'
    mail_object='prova'
    mail_body='Se non riesco non c\'e\' problema!'
    file_attach = 'C:\Users\ebalzani\IIT\Dottorato\SCI paper\Figs\Figures-1.png'
    send_email = mysend_email(sender,receiver,file_attach,server,port,mail_body,mail_object)
    send_email.show()
    app.exec_()
    zip_file = 'C:\Users\ebalzani\IIT\myPython\\tmp\images\\prova1.zip'
    file_list = ['C:\Users\ebalzani\IIT\myPython\\tmp\images\\autonomiceLogo.png','C:\Users\ebalzani\IIT\myPython\\tmp\images\\back.png']
    zip_my_file(file_list,zip_file)
if __name__ == '__main__':
    main()
    