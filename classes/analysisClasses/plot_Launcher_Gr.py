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

import sys,os
lib_fld = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
sys.path.append(lib_fld)

from custom_Plots_Gr import (F_Error_Rate_New_plt_GUI,plotPowerDensity,plt_Error_Rate_Gr,
                             plotSleepTimeCourse,plotLDA,plotMRA,
                             plotSwitchLatency,delta_reb_plt)

def select_Function_GUI_Gr(funcName, *otherInputs):
    
    if funcName == 'Error Rate':
        fig = F_Error_Rate_New_plt_GUI(*otherInputs)
        return fig
 
    elif funcName == 'Power_Density':
        fig = plotPowerDensity(*otherInputs)
        return fig
    elif funcName == 'Group_Error_Rate':
        fig = plt_Error_Rate_Gr(*otherInputs)
        return fig
    elif funcName == 'Sleep_Time_Course':
        fig = plotSleepTimeCourse(*otherInputs)
        return fig
    elif funcName == 'Linear_Discriminant_Analysis':
        fig = plotLDA(*otherInputs)
        return fig
    elif funcName == 'Multiple_Regression_Analysis':
        fig = plotMRA(*otherInputs)
        return fig
    elif funcName == 'LDA':
        fig = plotLDA(*otherInputs)
        return fig
    elif funcName == 'Switch_Latency':
        fig = plotSwitchLatency(*otherInputs)
        return fig
    elif funcName == 'delta_rebound':
        fig = delta_reb_plt(*otherInputs)
        return fig
