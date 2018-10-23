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

def functionCaller_Generator(pythonFilePath,newName,Dir):
    fh = file(pythonFilePath,'r')
    funcNameList = []
    if not newName.endswith('.py'):
        newName = newName.split('.')[0] + '.py'
    if not Dir.endswith('\\'):
        Dir += '\\'
    if not os.path.exists(Dir):
        raise ValueError, 'Directory %s not found'%Dir
    for line in fh.readlines():
        if line[0] == '#':
            continue
        word  = line.split(' ')
        try:
            index = word.index('def')
        except ValueError:
            continue
        for item in word[index+1:]:
            if item == '':
                continue
            funcNameList += [item.split('(')[0]]
            break
    fh.close()
    fh = open(Dir+newName,'w')
    program = 'from custom_Analysis import *\n\n'
    program += 'def function_Launcher(name,*myInput):\n'
    for name in funcNameList:
        program += '    if name == \'%s\':\n'%name
        program += '        outputData, inputForPlots, info = %s(*myInput)\n'%name
        program += '        return outputData, inputForPlots, info\n'
    fh.write(program)
    fh.close()
    return