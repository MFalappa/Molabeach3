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
        label = 'LDA'
        description = 'Compute the Linear discriminant analysis combining behaviour data and sleep data.\nIn order to run the analysis, create groups with the same name for each data type, the data will be matched according to the order'
        type_func = 'Integrative'
        
    elif function_name == 'delta_rebound':
        label = 'Delta - Theta'
        description = 'Compute the time course of the power of selected sleep-wake stage along 24 hours'
        type_func = 'Sleep'
    
    #da qui vanno controllati i nomi
    elif function_name == 'Actograms':
        label = 'Actograms'
        description = 'Display circadian activity data.\nThis analysis should be compute from TSE or Mycrosystem data or with data from running wheels'
        type_func = 'Behaviour'
        
    elif function_name == 'AIT':
        label = 'Acutal inter trial'
        description = 'Compute the mean and std error of the actual inter trial (AIT) per daily hour'
        type_func = 'Behaviour'
        
    elif function_name == 'peak_procedure':
        label = 'Peak analysis'
        description = 'Compute the  analysis for the peak behavioural test'
        type_func = 'Behaviour'
        
    elif function_name == 'raster_plot':
        label = 'Raster analysis'
        description = 'Compute the raster plot for the selected location by bose-poke activity'
        type_func = 'Behaviour'
        
    elif function_name == 'error_rate':
        label = 'Single error rate'
        description = 'Compute the error rate for selected group.\nThis is a single subject analysis'
        type_func = 'Behaviour'
        
    #da implementare
    elif function_name == 'Attentional_analysis':
        label = 'Attentional analysis'
        description = 'Compute the analysis for the attentional test.\nTo be added to Phenopy'
        type_func = 'Behaviour'
        
    elif function_name == 'sleep_fragmentation':
        label = 'Sleep fragmentation'
        description = 'Compute the number of sleep episodes of slected duration.\nTo be added to Phenopy'
        type_func = 'Sleep'
        
    elif function_name == 'emg_normalized':
        label = 'EMG normalized'
        description = 'Compute the analysis of the EMG signal.\nTo be added to Phenopy'
        type_func = 'Integrative'
        
    elif function_name == 'Sleep_cycles':
        label = 'Sleep cycles'
        description = 'Compute the analysis of the REM and-or REM sleep.\nTo be added to Phenopy'
        type_func = 'Sleep'
        
        
    

    else:
        label = None
        description = None
        type_func = None
    

    return label, description, type_func