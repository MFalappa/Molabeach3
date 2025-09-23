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
from plots_functions import *
def select_Function_GUI_all(funcName, *otherInputs):
 
    if funcName == 'Power_Density':
        fig = plotPowerDensity(*otherInputs)
        return fig
   
    elif funcName == 'Sleep_Time_Course':
        fig = plotSleepTimeCourse(*otherInputs)
        return fig
 
    elif funcName == 'delta_rebound':
        fig = plotDeltaTimeCourse(*otherInputs)
        return fig
    
    elif funcName == 'Sleep_cycles':
        fig = plotSleep_cycles(*otherInputs)
        return fig
    
    elif funcName == 'emg_normalized':
        fig = plotEMG(*otherInputs)
        return fig
    
    elif funcName == 'Attentional_analysis':
        fig = plotAttentional(*otherInputs)
        return fig
    
    elif funcName == 'Group_Error_Rate':
        fig = plotErrorRate(*otherInputs)
        return fig
        
    elif funcName == 'AIT':
        fig = plotAIT(*otherInputs)
        return fig   
     
    elif funcName == 'peak_procedure':
        fig = plotPeak(*otherInputs)
        return fig
    
    elif funcName == 'raster_plot':
        fig = plotRaster(*otherInputs)
        return fig
    
    elif funcName == 'Actograms':
        fig = plotActograms(*otherInputs)
        return fig
    
    elif funcName == 'Switch_Latency':
        fig = plotSwitch_Latency(*otherInputs)
        return fig
    
    elif funcName == 'LDA':
        fig = plotLDA(*otherInputs)
        return fig