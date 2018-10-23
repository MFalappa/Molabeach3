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

raw = np.loadtxt('C:\Users\MFalappa\Downloads\\150424_12_05_Grattachecca.txt')

startDate = np.zeros(3)
startDate[0] = int(raw[0]) # year
startDate[1] = int(raw[1]) # month
startDate[2] = int(raw[2]) # day

endDate = np.zeros(3)
endDate[0] = int(raw[3]) # year
endDate[1] = int(raw[4]) # month
endDate[2] = int(raw[5]) # day

startRaw = raw.shape[0]-4

findRaw = False

while findRaw == False:
    
    if (raw[startRaw+1] == startDate[0]) and (raw[startRaw+2] == startDate[1]) and (raw[startRaw+3] == startDate[2]) and (raw[startRaw-2] == startDate[0]) and (raw[startRaw-1] == startDate[1]) and (raw[startRaw] == startDate[2]):
        
        startRaw = startRaw -3
        findRaw = True
    else:
        startRaw = startRaw - 1  


startH = int(raw[startRaw+11])
startM = int(raw[startRaw+12])
startS = int(raw[startRaw+13])

endH = int(raw[startRaw+14])
endM = int(raw[startRaw+15])
endS = int(raw[startRaw+16])

offSet = 21
firstCode = 27
nEvent = int(raw[startRaw+offSet])
start = 19
nameEvent = ['StartTrial','StopTrial','LedONSx','LedONdx','LedOFFSx','LedOFFdx','LightON','LightOFF','LeftLever','RightLever','NosePokeIN','NosePokeOUT','GivePelletON','StartOfInterTrial','EndOfInterTrial','TimeOutReached','ProbeTrialSound','ProbeTrialStim','StartExperiment','StopExperiment','NULL','NULL','LeftTrial','RightTrial','LeftTrial NonRewarded','RightTrial NonRewarded','ON Whater','OFF Whater']

code = np.zeros((nEvent),dtype = int)
time = np.zeros((nEvent),dtype = float)
event = np.empty((nEvent),dtype = "S35")


if raw[startRaw+firstCode] == start:
    for kk in range(nEvent):
        code[kk] = int(raw[startRaw+firstCode+kk])
        time[kk] = raw[startRaw+firstCode+nEvent+kk]
        event[kk] = nameEvent[int(code[kk]-1)]
else:
    code = -1
    time = -1
    print('Code and Time non detected')
    
if code[0] != start and time[0] != 0:
    print('Parsing of file is wrong')
else:
    print('Parsing of file is correct')
        

    
