#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 12:30:53 2019

@author: Matte
"""

def info_label(function_name):
    
    if function_name == 'Switch_Latency':
        label = 'Switch Latency'
        description = 'Compute the switch time from short to long location'
        type_func = 'Behaviour'
        
    elif function_name == 'Power_Density':
        label = 'Power desnity'
        description = 'Compute the power of whole spectrum during selected stage'
        type_func = 'Sleep'
        
    elif function_name == 'Group_Error_Rate':
        label = 'Error rate'
        description = 'Compute the error rate for selected group.\nThis is a gruop analysis'
        type_func = 'Behaviour'
        
    elif function_name == 'Sleep_Time_Course':
        label = 'Time course'
        description = 'Compute the averege of selected sleep-wake stage along 24 hours'
        type_func = 'Sleep'
        
    elif function_name == 'Linear_Discriminant_Analysis':
        label = 'Linear discriminant analysis'
        description = 'Parlare con Edo'
        type_func = 'Integrative'
        
    elif function_name == 'Multiple_Regression_Analysis':
        label = 'Multiple regression analysis'
        description = 'Parlare con Edo'
        type_func = 'Integrative'
        
    elif function_name == 'LDA':
        label = 'Linear discriminant analysis'
        description = 'Compute the switch time from short to long location'
        type_func = 'Integrative'
        
    elif function_name == 'delta_rebound':
        label = 'Delta - Theta'
        description = 'Compute the time course of the power of selected sleep-wake stage along 24 hours'
        type_func = 'Sleep'

        
        


    else:
        label = None
        description = None
        type_func = None
    

    return label, description, type_func