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
                          plot_Standard_Input_Error_Rate_GUI,std_ErrorBar_Plt_TimeCourse_GUI,
                          plot_Rsquared_Grid_GUI,plot_R_Squared_vs_Lag_GUI,plotLDARes_Dict,
                          Gr_BoxPlot_LD_GUI,CDF_Gr_Plot_GUI,CDF_average_plot_GUI,
                          F_ExpGain_Plt_GUI,std_Bar_Plot_GUI)

import matplotlib.pylab as plt
import numpy as np


def plotPowerDensity(*myinputs):
    print('myinput',list(myinputs[0].keys()),list(myinputs[0]['Fig:Power Density'].keys()))
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
def plt_Error_Rate_Gr(*myinputs):
    print(list(myinputs[0].keys()))
    fig,fig1  = plot_Standard_Input_Error_Rate_GUI(\
        *myinputs[0][list(myinputs[0].keys())[0]]['Error Rate'])
    figDict = {'Fig Group Error Rate':{}}
    figDict['Fig Group Error Rate']['Group Error Rate'] = fig
    figDict['Fig Group Error Rate']['Group Error Rate Bar'] = fig1
    fig.show()
    fig1.show()
    return figDict
def plotSleepTimeCourse(*myinputs):
    KeyVect = myinputs[0][list(myinputs[0].keys())[0]]
    for key in KeyVect:
        if 'Num' in key:
            Key1 = key
        else:
            Key2 = key
    print(KeyVect)
    fig  = std_ErrorBar_Plt_TimeCourse_GUI(\
        *myinputs[0][list(myinputs[0].keys())[0]][Key1])
    fig1 = std_ErrorBar_Plt_TimeCourse_GUI(\
        *myinputs[0][list(myinputs[0].keys())[0]][Key2])
    figDict = {'Fig Sleep Time Course':{}}
    figDict['Fig Sleep Time Course']['Num Episodes'] = fig
    figDict['Fig Sleep Time Course']['Episode Duration'] = fig1
    fig.show()
    fig1.show()
    return figDict 
def plotMRA(*myinputs):
    print('Entered plotMRA')
    print(myinputs[0][list(myinputs[0].keys())[0]])
    fig = plot_Rsquared_Grid_GUI(*myinputs[0][list(myinputs[0].keys())[0]]['MRA'])[0]
    fig2 = plot_R_Squared_vs_Lag_GUI(*myinputs[0][list(myinputs[0].keys())[0]]\
        ['R_squared_vs_lag_sleep'])
    for key in list(fig.keys()):
        fig[key].show()
    for key in list(fig2.keys()):
        fig2[key].show()
    figDict = {'Fig MRA':fig}
    figDict['Fig MRA'].update(fig2)
    return figDict
def plotLDA(*myInput):
    figs  = plotLDARes_Dict(*myInput[0]['Fig:LDA Results']['Scatter'])
    figs2 = plotLDARes_Dict(*myInput[0]['Fig:Group LDA Results']['Scatter'])
    figDict = {'Fig LDA':{}}
    for key in list(figs.keys()):
        figDict['Fig LDA'][key] = figs[key]
    for key in list(figs2.keys()):
        figDict['Fig LDA'][key] = figs2[key]
    return figDict
def plotSwitchLatency(*myInput):
    figs  = Gr_BoxPlot_LD_GUI(*myInput[0]['Fig:Group Switch Latency']['Record switch time'])
    fig1 = CDF_Gr_Plot_GUI(*myInput[0]['Fig:Group Switch Latency']['Gaussian Fit'])
    fig4 = CDF_average_plot_GUI(*myInput[0]['Fig:Group Switch Latency']['Gaussian Fit'])
    figDict = {'Fig Switch Latency':{}}
    figDict['Fig Switch Latency']['Gaussian Fit'] = fig1
    fig2 = F_ExpGain_Plt_GUI(*myInput[0]['Fig:Group Switch Latency']['Optimal Surface'])
    fig3 = std_Bar_Plot_GUI(*myInput[0]['Fig:Group Switch Latency']['Expected Gain'])
    for key in list(figs.keys()):
        figDict['Fig Switch Latency']['Record switch time_%s'%key] = figs[key]
        figs[key].show()
    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()
    figDict['Fig Switch Latency']['Expected Gain'] = fig3
    figDict['Fig Switch Latency']['Optimal Surface'] = fig2
    figDict['Fig Switch Latency']['Gaussian Fit avg'] = fig4
    return figDict
def delta_reb_plt(*myInput):
    key = list(myInput[0]['Fig:Rebound'].keys())[0]
    band = key.split(' ')[0]
    norm_rebound = myInput[0]['Fig:Rebound']['%s Time Course'%band]
    v_tot_sec = np.vectorize(lambda t:t.total_seconds())
    figDict = {'Fig Rebound':{}}
    for subject in np.unique(norm_rebound['Subject']):
        sub_data = norm_rebound[norm_rebound['Subject'] == subject]
        time_h = v_tot_sec(sub_data['Time0'] - sub_data['Time0'][0]) / 3600.
        fig = plt.figure()
        plt.title(key + '\n%s'%subject,fontsize=20)
        plt.plot(time_h,sub_data['Power'],lw=1.2)
        plt.ylabel('Norm Power',fontsize=15)
        plt.xlabel('Time(hrs)',fontsize=15)
        plt.xlim(time_h[0]-1,time_h[-1]+1)
        figDict['Fig Rebound'][key+' %s'%subject] = fig
    fig = plt.figure()
    plt.title('Group '+key,fontsize=20)
    pl = []
    genl = []
    for gen in np.unique(norm_rebound['Group']):
        gr_data = norm_rebound[norm_rebound['Group'] == gen]
        subjects = np.unique(gr_data['Subject'])
        mx_size = 0 
        for sub in subjects:
            tmp = np.sum(gr_data['Subject']==sub)
            if tmp > mx_size:
                mx_size = tmp
                delta_t = gr_data[gr_data['Subject']==sub]['Time0']-gr_data[gr_data['Subject']==sub]['Time0'][0]
                time_h = v_tot_sec(delta_t)/3600.
        mat_data = np.zeros((subjects.shape[0],mx_size))
        isub = 0
        for sub in subjects:
            vals = gr_data[gr_data['Subject']==sub]
            mat_data[isub,:vals.shape[0]] = vals['Power']
            isub += 1
        mean = np.nanmean(mat_data,axis=0)
        sem = np.nanstd(mat_data,axis=0) / (np.sum(1 - np.isnan(mat_data),axis=0) ** 0.5)
        pl += [plt.errorbar(time_h,mean,sem,elinewidth=1.2,lw=1.2)]
        genl += [gen]
    plt.ylabel('Norm Power',fontsize=15)
    plt.xlabel('Time(hrs)',fontsize=15)
    plt.xlim(time_h[0]-1,np.max([plt.xlim()[1],time_h[-1]+1]))
    plt.legend(pl,genl,fontsize=15,loc=2,frameon=False)
    figDict['Fig Rebound']['Group '+key] = fig  
    return figDict   
