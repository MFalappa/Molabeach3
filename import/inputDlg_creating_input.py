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

def inputDlg_creating_input(pathToAutonomice,dictInput,func_Name):
    if not pathToAutonomice.endswith('\\'):
        pathToAutonomice += '\\'
    try:
        fh = open(pathToAutonomice + 'inputDlgCreator.py','a')
        line =  '    if analysisName == \'%s\':\n'%func_Name
        for key in dictInput.keys():
            line += '        dictInput[\'%s\'] = %s\n'%(key,dictInput[key])
        line += '        return dictInput\n'
        fh.write(line)
    except:
        raise ValueError,'Unable to write new input'
        