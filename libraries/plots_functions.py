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
                          plot_new_time_sleep_course_single,
                          plot_new_time_sleep_course_group,
                          plot_sleep_cycles,
                          plot_emg_norm,
                          plot_attentional,
                          plot_errors,
                          plot_ait,
                          plot_peak_procedure,
                          plot_raster)

def plotPowerDensity(*myinputs):
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
    fig_single = plot_new_time_sleep_course_single(KeyVect['Single Subject'])
    fig_group = plot_new_time_sleep_course_group(KeyVect['Single Subject'])
    figDict = {'Fig Sleep Time Course':{}}
    figDict['Fig Sleep Time Course']['Time course single'] = fig_single
    figDict['Fig Sleep Time Course']['Time course group'] = fig_group
    fig_single.show()
    fig_group.show()
    return figDict 
def plotDeltaTimeCourse(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    fig_single = plot_new_time_sleep_course_single(KeyVect['Single Subject'])
    fig_group = plot_new_time_sleep_course_group(KeyVect['Single Subject'])
    figDict = {'Fig Power Time Course':{}}
    figDict['Fig Power Time Course']['Power time course single'] = fig_single
    figDict['Fig Power Time Course']['Power time course group'] = fig_group
    fig_single.show()
    fig_group.show()
    return figDict 
def plotSleep_cycles(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    fig = plot_sleep_cycles(KeyVect['Single Subject'])
    figDict = {'Fig sleep cycles':{}}
    figDict['Fig sleep cycles']['Sleep cycles duration'] = fig
    fig.show()
    return figDict 
def plotEMG(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    fig1,fig2,fig3 = plot_emg_norm(KeyVect['Single Subject'])
    figDict = {'Fig EMG normalized':{}}
    figDict['Fig EMG normalized']['Wake'] = fig1
    figDict['Fig EMG normalized']['REM'] = fig2
    figDict['Fig EMG normalized']['nonREM'] = fig3
    fig1.show()
    fig2.show()
    fig3.show()
    return figDict
def plotAttentional(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    fig = plot_attentional(KeyVect['Single Subject'])
    figDict = {'Fig Attentional test':{}}
    figDict['Fig Attentional test'][KeyVect['Single Subject'][5]] = fig
    fig.show()
    return figDict
def plotErrorRate(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    fig = plot_errors(KeyVect['Single Subject'])
    figDict = {'Fig Error rate':{}}
    figDict['Fig Error rate'][KeyVect['Single Subject'][1]] = fig
    fig.show()
    return figDict
def plotAIT(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    fig = plot_ait(KeyVect)
    figDict = {'Fig AIT':{}}
    figDict['Fig AIT']['Single subject'] = fig
    fig.show()
    return figDict
def plotPeak(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    fig1,fig2 = plot_peak_procedure(KeyVect)
    figDict = {'Fig Peak':{}}
    figDict['Fig Peak']['Single subject'] = fig1
    figDict['Fig Peak']['Group'] = fig2
    fig1.show()
    fig2.show()
    return figDict
def plotRaster(*myinputs):
    figDict = {'Fig Raster':{}}
    for key in myinputs[0].keys():
        figDict['Fig Raster'][key] = plot_raster(myinputs[0][key])
        
        
    for key in figDict['Fig Raster'].keys():
        tmp = figDict['Fig Raster'][key]
        tmp.show()
    
    return figDict

