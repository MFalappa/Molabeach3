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
from Plotting_GUI import *

def plotActogram(*myInput):
    figDict = {'Fig Actogram':{},'Fig SinFit':{}}
    data_dict = myInput[0]
    print 'plotActo inputs',myInput[0].keys()
    for dataName in data_dict.keys():
        Actogram = data_dict[dataName]['Fig_Actogram'][0]
        N_Day = data_dict[dataName]['Fig_Actogram'][1] 
        interval = data_dict[dataName]['Fig_Actogram'][2]
        boolean = data_dict[dataName]['Fig_Actogram'][3]
        normStr = data_dict[dataName]['Fig_Actogram'][4]
        hrs = data_dict[dataName]['Fig_Actogram'][5]
        kwargs = data_dict[dataName]['Fig_Actogram'][6]
        fig = Print_Actogram_GUI(Actogram,N_Day,interval,boolean,*(normStr,hrs),**kwargs)
        figName = 'Actogram_' + dataName.split('.')[0]
        figDict['Fig Actogram'][figName] = fig
        
        Period_Array = data_dict[dataName]['Fig Sinfit'][0]
        Best_Fit_Param = data_dict[dataName]['Fig Sinfit'][1]
        subject = data_dict[dataName]['Fig Sinfit'][2]
        fig = plt_Best_Period(Period_Array,Best_Fit_Param,subject)
        figName = 'SinFit_' + dataName.split('.')[0]
        figDict['Fig Actogram'][figName] = fig                
    return figDict
    
def plotErrorRate(*myInput):
    figDict = {'Fig Error Rate':{}}
    data_dict = myInput[0]
    for dataName in data_dict.keys():
        cr = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][0]
        HLabel = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][1]
        c1 = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][2]
        c2 = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][3]
        LD = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][4]
        alpha = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][5]
        title = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][6]
        boolean = data_dict[dataName]['Fig_Error_Rate_Daily_Average'][7]
        fig = F_Error_Rate_New_plt_GUI(cr,HLabel,c1,c2,LD,alpha,title,boolean)
        figName = 'Error_Rate_' + dataName.split('.')[0]
        figDict['Fig Error Rate'][figName] = fig
    return figDict

def plotAIT(*myInput):
    figDict = {'Fig AIT':{}}
    data_dict = myInput[0]
    for dataName in data_dict.keys():
        OrdMean = data_dict[dataName]['Fig_AIT'][0]
        OrdStd = data_dict[dataName]['Fig_AIT'][1]
        Hlabel = data_dict[dataName]['Fig_AIT'][2]
        c1 = data_dict[dataName]['Fig_AIT'][3]
        c2 = data_dict[dataName]['Fig_AIT'][4]
        LenDark = data_dict[dataName]['Fig_AIT'][5]
        alpha = data_dict[dataName]['Fig_AIT'][6]
        title = data_dict[dataName]['Fig_AIT'][7]
        ylab = data_dict[dataName]['Fig_AIT'][8]
        none = data_dict[dataName]['Fig_AIT'][9]
        median = data_dict[dataName]['Fig_AIT'][10]
        perc25 = data_dict[dataName]['Fig_AIT'][11]
        perc75 = data_dict[dataName]['Fig_AIT'][12]
        fig = F_Error_Bar_New_plt_GUI(OrdMean,OrdStd,Hlabel,c1,c2,LenDark,alpha,title + ' - Mean $\pm$ SEM',ylab,none)
        figName = 'Mean_AIT_' + dataName.split('.')[0]
        figDict['Fig AIT'][figName] = fig
        fig = F_Error_Bar_New_plt_GUI(median,[perc25,perc75],Hlabel,c1,c2,LenDark,alpha,title + ' - Median',ylab,none)
        figName = 'Median_AIT_' + dataName.split('.')[0]
        figDict['Fig AIT'][figName] = fig
    return figDict
    
def plotRasterPlot(*myInput):
    figDict = {'Fig Raster Plot':{}}
    data_dict = myInput[0]
    for dataName in data_dict.keys():
        fig = F_Raster_Plt_GUI(*data_dict[dataName][data_dict[dataName].keys()[0]])
        figName = data_dict[dataName].keys()[0] + '_' + dataName.split('.')[0]
        figDict['Fig Raster Plot'][figName] = fig
    return figDict
    
def plotPeakProcedure(*myInput):
    figDict = {'Fig Peak Procedure':{}}
    data_dict = myInput[0]
    for dataName in data_dict.keys():
        fig = F_PeakProbes_plt_GUI(*data_dict[dataName][data_dict[dataName].keys()[0]])
        figName = data_dict[dataName].keys()[0] + '_' + dataName.split('.')[0]
        figDict['Fig Peak Procedure'][figName] = fig
    return figDict
def plotSpikeStatistics(*myInput):
    figDict = {'Firing Rate':{},'log2(ISI)':{}}
    dictFR = myInput[0]['Fig:Spike Statistics']['Firing Rate']
    dictIsi = myInput[0]['Fig:Spike Statistics']['ISI']
    for name in dictFR.keys():
        for k in range(len(dictFR[name]['nameFR'])):
            fig = plt.figure()
            firingRate = dictFR[name]['firingRate'][k,:]
            timeSec =  dictFR[name]['time(Sec)']
            plt.bar(timeSec,firingRate,width=timeSec[1]-timeSec[0])
            plt.title(dictFR[name]['nameFR'][k],fontsize=15)
            plt.ylabel('Spike/sec',fontsize=12)
            plt.xlabel('Time(sec)',fontsize=12)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            svName = 'Firing_Rate_'+dictFR[name]['nameFR'][k].replace('\n','').replace(' ','_').replace('.nex','_')
            figDict['Firing Rate'][svName] = fig
            fig = plt.figure()
            log2ISI= dictIsi[name]['histISI'][k,:]
            edgeISI =  dictIsi[name]['edgeISI'][k,:]
            plt.bar(edgeISI[:-1],log2ISI,width=np.diff(edgeISI))
            plt.title(dictIsi[name]['nameISI'][k],fontsize=15)
            plt.ylabel('Counts',fontsize=12)
            plt.xlabel('log2(ISI)',fontsize=12)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            svName = 'ISI_'+dictIsi[name]['nameISI'][k].replace('\n','').replace('.nex','_')
            figDict['log2(ISI)'][svName] = fig
    return figDict
