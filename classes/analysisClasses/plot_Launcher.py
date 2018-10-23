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
from Plotting_GUI import *
from custom_Plots import *
def select_Function_GUI(funcName, *otherInputs):
    plt.show(block=False)
    if funcName == 'Actogram':
        fig = plotActogram(*otherInputs)
        return fig
    elif funcName == 'AIT':
        fig = plotAIT(*otherInputs)
        return fig
    elif funcName == 'Error_Rate':
        fig = plotErrorRate(*otherInputs)
        return fig
    elif funcName == 'Raster_Plot':
        fig = plotRasterPlot(*otherInputs)
        return fig
    elif funcName == 'Peak_Procedure':
        fig = plotPeakProcedure(*otherInputs)
        return fig

    elif funcName == 'spikeStatistics':
        fig = plotSpikeStatistics(*otherInputs)
        return fig
