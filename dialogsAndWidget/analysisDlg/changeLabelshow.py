#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 12:30:53 2019

@author: Matte
"""

def info_label(function_name):
    
    if function_name == 'Switch_Latency':
        label = 'Switch analysis'
        description = 'Compute the analysis for the switch timing task'
        type_func = 'Behaviour'
        
    elif function_name == 'Power_Density':
        label = 'Power density'
        description = 'Compute the power of whole spectrum during selected stage'
        type_func = 'Sleep'
        
    elif function_name == 'Group_Error_Rate':
        label = 'Group error rate'
        description = 'Compute the error rate for selected group.\nThis is a gruop analysis'
        type_func = 'Behaviour'
        
    elif function_name == 'Sleep_Time_Course':
        label = 'Time course'
        description = 'Compute the averege of selected sleep-wake stage along 24 hours'
        type_func = 'Sleep'
        
    elif function_name == 'LDA':
        label = 'Linear discriminant analysis'
        description = 'Compute the switch time from short to long location'
        type_func = 'Integrative'
        
    elif function_name == 'delta_rebound':
        label = 'Delta - Theta'
        description = 'Compute the time course of the power of selected sleep-wake stage along 24 hours'
        type_func = 'Sleep'
    
    elif function_name == 'F_Actogram_GUI':
        label = 'Actogram'
        description = 'Display circadian activity data.\n This analysis should be compute from TSE or Mycrosystem data or with data from running wheels'
        type_func = 'Behaviour'
        
    elif function_name == 'AITComputation_GUI':
        label = 'Acutal inter trial'
        description = 'Compute the mean and std error of the actual inter trial (AIT) per daily hour'
        type_func = 'Behaviour'
        
    elif function_name == 'F_PeakProbes_GUI':
        label = 'Peak analysis'
        description = 'Compute the  analysis for the peak behavioural test'
        type_func = 'Behaviour'
        
    elif function_name == 'Raster_plot':
        label = 'Raster analysis'
        description = 'Compute the raster plot for the selected location by bose-poke activity'
        type_func = 'Behaviour'
        
    elif function_name == 'Error_Rate':
        label = 'Single error rate'
        description = 'Compute the error rate for selected group.\nThis is a single subject analysis'
        type_func = 'Behaviour'
        
    elif function_name == 'Attentional_analysis':
        label = 'Attentional_analysis'
        description = 'Compute the analysis for the attentional test.\nTo be added to Phenopy'
        type_func = 'Behaviour'
        
    elif function_name == 'sleep_fragmentation':
        label = 'Sleep fragmentation'
        description = 'Compute the number of sleep episodes of slected duration.\nTo be added to Phenopy'
        type_func = 'Sleep'
        
    elif function_name == 'emg_normalized':
        label = 'EMG normalized'
        description = 'Compute the analysis of the EMG signal.\nTo be added to Phenopy'
        type_func = 'Sleep'
        
    elif function_name == 'Sleep_cycles':
        label = 'Sleep cycles'
        description = 'Compute the analysis of the REM and-or REM sleep.\nTo be added to Phenopy'
        type_func = 'Sleep'
        
        
    

    else:
        label = None
        description = None
        type_func = None
    

    return label, description, type_func