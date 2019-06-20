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

from PyQt5.QtCore import (pyqtSignal, QThread)
import os,sys
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
phenoDlg_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'dialogsAndWidget','analysisDlg')
sys.path.append(lib_dir)
sys.path.append(phenoDlg_dir)

from Modify_Dataset_GUI import OrderedDict
from copy import copy
from launcher_Gr import function_Launcher_Gr
import traceback

#from Analyzing_GUI import *
#from Plotting_GUI import *

class analysisGroup_thread(QThread):
    threadFinished = pyqtSignal()
    def __init__(self, Datas, lock, parent = None):
        super(analysisGroup_thread, self).__init__(parent)
        self.lock = lock
        self.Datas = Datas
        self.inputForPlots = OrderedDict()
        self.outputData = OrderedDict()
        self.info = OrderedDict()
        
    def initialize(self, Input, analysisName, GroupsDict,TimeStamps,pairedGroups,
                   Other = None):
#        print('start initialize Gr')
        self.Input = Input
        self.analysisName = analysisName
        self.TimeStamps = copy(TimeStamps)
        self.GroupsDict = GroupsDict
        self.pairedGroups = pairedGroups
        self.Other = Other
        flag = True
        for key in list(Input.keys()):
            if 'SavingDetails' in Input[key]:
                self.savingDetails = Input[key]['SavingDetails']
                flag = False
                break
        if flag:
            self.savingDetails = False
#        print('end initialize ',self.savingDetails)
    def run(self):
        self.outputData, self.inputForPlots, self.info =\
            self.analyze(self.analysisName)
        self.threadFinished.emit()
#        self.emit(pyqtSignal('threadFinished()'))
        
    def setInput(self, Input, DataList):
        self.Input = Input
#        self.GroupsDict = GroupsDict
    
    def analyze(self, analysisName):
#        print('Gr analyze called',':',analysisName)
        try:
            outputData, inputForPlot, info = \
                function_Launcher_Gr(analysisName,self.Datas,
                                     self.Input,self.GroupsDict,
                                     self.TimeStamps, self.lock,self.pairedGroups,
                                     self.Other)
        except Exception as inst:
            print((type(inst)))    # the exception instance
            print((inst.args))     # arguments stored in .args
            print(inst)
            x = inst.args     # unpack args
            print(('x =', x))
            outputData, inputForPlot, info = None, None, None
            traceback.print_exc()
        return outputData, inputForPlot, info

