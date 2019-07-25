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

from Plotting_GUI import (Plt_RawPowerDensity_Loop_GUI,Plt_MedianPowerDensity_GUI,
                          std_ErrorBar_Plt_TimeCourse_GUI,std_ErrorBar_Plt_TimeCourse_GUI)

import matplotlib.pylab as plt
import numpy as np


def plotPowerDensity(*myinputs):
    print('myinput',list(myinputs[0].keys()),list(myinputs[0]['Fig:Power Density'].keys()))
    figs  = Plt_RawPowerDensity_Loop_GUI(\
        *myinputs[0][list(myinputs[0].keys())[0]]['Single Subject'])
    figsall = Plt_MedianPowerDensity_GUI(\
        *myinputs[0][list(myinputs[0].keys())[0]]['Group'])
    fig1 = figsall[0]
    figDict = {'Fig Power Density':{}}
    figDict['Fig Power Density']['Grouped'] = fig1
    for key in list(figs.keys()):
        figDict['Fig Power Density']['%s'%key] = figs[key]
        figs[key].show()
    figDict['Fig Power Density']['Wake x Group'] = figsall[1]
    figDict['Fig Power Density']['REM x Group'] = figsall[2]
    figDict['Fig Power Density']['NREM x Group'] = figsall[3]
    fig1.show()
    return figDict


def plotSleepTimeCourse(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    for key in KeyVect:
        if 'Num' in key:
            Key1 = key
        else:
            Key2 = key
    print(KeyVect)
    fig  = std_ErrorBar_Plt_TimeCourse_GUI(\
        *myinputs[0][list(myinputs[0].keys())[0]][Key1])
    fig1 = std_ErrorBar_Plt_TimeCourse_GUI(\
        *myinputs[0][list(myinputs[0].keys())[0]][Key2])
    figDict = {'Fig Sleep Time Course':{}}
    figDict['Fig Sleep Time Course']['Num Episodes'] = fig
    figDict['Fig Sleep Time Course']['Episode Duration'] = fig1
    fig.show()
    fig1.show()
    return figDict 