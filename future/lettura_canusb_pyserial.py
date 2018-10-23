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
import serial
from myPyXBee import enumerate_serial_ports
from time import sleep
# baudmap
BAUDMAP = {'10k':b'S0', '20k':b'S1', '50k':b'S2', '100k':b'S3', '125k':b'S4', '250k':b'S5', '500k':b'S6', '800k':b'S7', '1M':b'S8'}

# Carriage return command for CanUSB
CR = b'\r'

# Open command for CanUSB
OPEN = b'O\r'

# Close command for CanUSB
CLOSE = b'C\r'

canbaud = b'S6'
for p in enumerate_serial_ports():
    if 'VCP' in p[1]:
        break
canPort = serial.Serial(p[0],baudrate=500000,timeout=1)
res = canPort.write(CLOSE) # res == 2 tutto ok
#
baudres=canPort.write(canbaud+CR)

res = canPort.write(OPEN)

canPort.write(bytearray('t60A20100\r')) # switch to operational
totprint = 1
i=0
while True:
    byte = canPort.read()
    byteARRAY = bytearray()
    while byte == '\r':
        byte = canPort.read()
    byteARRAY += byte
    while byte!=CR:
        byte = canPort.read()
        byteARRAY += byte
    print byteARRAY
    if i >=totprint:
        break
    i+=1

print '%d heart bit plotted'%totprint
canPort.write(bytearray('t60A82301120505010100\r'))
sleep(3)
canPort.write(bytearray('t60A82301120500000000\r'))
canPort.close()