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

from PyQt5.QtCore import QThread
from smtplib import SMTP
from copy import copy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class send_email_thread(QThread):
    def __init__(self, parent = None):
        super(send_email_thread, self).__init__(parent)
        self.Id = None
        self.num_blocks = None
    def initialize(self,Id, num_blocks, pdict, psw):
        self.num_blocks = num_blocks
        self.Id = Id
        self.pdict = copy(pdict)
        self.__password = psw
    def run(self):
        
        if (self.num_blocks % 50) != 1:
            return
        try:
            smtpObj = SMTP(host=self.pdict['server'],
                           port=self.pdict['port'])
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(self.pdict['email'], self.__password)
            message = MIMEMultipart()
            message['Subject'] = 'Aborted Pellet Release'
            message['From'] = self.pdict['email']
            message['To'] = ','.join(self.pdict['receivers'])
            body = MIMEText("%d release aborted from device %d"%(self.num_blocks,
                                                                 self.Id))
            message.attach(body)
            smtpObj.sendmail(self.pdict['email'],
                             self.pdict['receivers'],
                             message.as_string())
        except Exception as e:
            print(e)
            print('Unable to send email')
            pass