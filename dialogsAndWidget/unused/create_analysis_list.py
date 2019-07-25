#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:35:01 2019

@author: Matte
"""


import numpy as np

dict_functions = {}


dict_functions['Switch_Latency'] = {
        'label' : 'Switch analysis',
        'description' : 'Compute the analysis for the switch timing task',
        'type_func' : 'Behaviour'}

dict_functions['Power_Density'] = {
        'label' : 'Power density',
        'description' : 'Compute the power of whole spectrum during selected stage',
        'type_func' : 'Sleep'}

dict_functions['Group_Error_Rate'] = {
        'label' : 'Group error rate',
        'description' : 'Compute the error rate for selected group.\nThis is a gruop analysis',
        'type_func' : 'Behaviour'}

dict_functions['Sleep_Time_Course'] = {
        'label' : 'Time course',
        'description' : 'Compute the averege of selected sleep-wake stage along 24 hours',
        'type_func' : 'Sleep'}

dict_functions['LDA'] = {
        'label' : 'LDA',
        'description' : 'Compute the Linear discriminant analysis combining behaviour data and sleep data.\nIn order to run the analysis, create groups with the same name for each data type\n\nData will be matched according to the order',
        'type_func' : 'Integrative'}

dict_functions['delta_rebound'] = {
        'label' : 'Delta - Theta',
        'description' : 'Compute the time course of the power of selected sleep-wake stage along 24 hours',
        'type_func' : 'Sleep'}

dict_functions['Actograms'] = {
        'label' : 'Actograms',
        'description' : 'Display circadian activity data.\nThis analysis should be compute from TSE or Mycrosystem data or with data from running wheels',
        'type_func' : 'Behaviour'}

dict_functions['AIT'] = {
        'label' : 'Acutal inter trial',
        'description' : 'Compute the mean and standard error of the actual inter trial (AIT) per daily hour',
        'type_func' : 'Behaviour'}

dict_functions['peak_procedure'] = {
        'label' : 'Peak analysis',
        'description' : 'Compute the  analysis for the peak behavioural test',
        'type_func' : 'Behaviour'}        

dict_functions['raster_plot'] = {
        'label' : 'Raster analysis',
        'description' : 'Compute the raster plot for the selected location by nose-poke activity',
        'type_func' : 'Behaviour'}           
        
dict_functions['error_rate'] = {
        'label' : 'Single error rate',
        'description' : 'Compute the error rate for selected group.\nThis is a single subject analysis',
        'type_func' : 'Behaviour'} 
        
dict_functions['Attentional_analysis'] = {
        'label' : 'Attentional analysis',
        'description' : 'Compute the analysis for the attentional test.\nTo be added to Phenopy',
        'type_func' : 'Behaviour'} 
        
dict_functions['sleep_fragmentation'] = {
        'label' : 'Sleep fragmentation',
        'description' : 'Compute the number of sleep episodes of selected duration.\nTo be added to Phenopy',
        'type_func' : 'Sleep'}  

dict_functions['Sleep_cycles'] = {
        'label' : 'Sleep cycle',
        'description' : 'Compute the duration of REM - non-REM alternations.\nTo be added to Phenopy',
        'type_func' : 'Sleep'} 

dict_functions['emg_normalized'] = {
        'label' : 'EMG analysis',
        'description' : 'Compute the distributions of Normalized EMG Values (DNE) along each sleep stage.\nTo be added to Phenopy',
        'type_func' : 'Sleep'} 


np.save('/Users/Matte/Python_script/Phenopy3/mainScripts/Analysis.npy',dict_functions)

 








        
  