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

from custom_Analysis_Gr import *
def function_Launcher_Gr(name,*myInput):
    if name == 'Power_Density':
        outputData, inputForPlots, info = Power_Density(*myInput)
        return outputData, inputForPlots, info
    if name == 'Group_Error_Rate':
        outputData, inputForPlots, info = Group_Error_Rate(*myInput)
        return outputData, inputForPlots, info
    if name == 'Sleep_Time_Course':
        outputData, inputForPlots, info = Sleep_Time_Course(*myInput)
        return outputData, inputForPlots, info
    if name == 'Linear_Discriminant_Analysis':
        outputData, inputForPlots, info = Linear_Discriminant_Analysis(*myInput)
        return outputData, inputForPlots, info
    if name == 'Multiple_Regression_Analysis':
        outputData, inputForPlots, info = Multiple_Regression_Analysis(*myInput)
        return outputData, inputForPlots, info
    if name == 'LDA':
        outputData, inputForPlots, info = LDA(*myInput)
        return outputData, inputForPlots, info
    if name == 'Switch_Latency':
        outputData, inputForPlots, info = Switch_Latency(*myInput)
        return outputData, inputForPlots, info
    if name == 'delta_rebound':
        outputData, inputForPlots, info = delta_rebound(*myInput)
        return outputData, inputForPlots, info
