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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_new_time_sleep_course_group(df):
    
    groups = np.unique(df['Group'])
    subject = len(df)
    fr = df.T
    
    x_group = np.zeros((subject,len(fr[0][2:])),dtype=float)
    x_label = np.zeros((subject),dtype=int)
    
    gg = 1
    sb = 0
    for kk in groups:
        for sbj in range(subject):
            if fr[sbj]['Group'] == kk:
                x_group[sb,:] = np.array(fr[sbj][2:])
                x_label[sb] = gg
                sb +=1
                
        gg +=1
     
    fig = plt.figure()
    for kk in range(len(groups)):
        print(kk)
        print(groups[kk])
        sbj_tr = x_label == kk+1
        print(sbj_tr)
        m = np.nanmean(x_group[sbj_tr,:],axis = 0)
        s = np.nanstd(x_group[sbj_tr,:],axis = 0)/np.sqrt(np.sum(sbj_tr))
        
        plt.errorbar(range(m.shape[0]),y = m, yerr = s,  elinewidth=2.5,
                                                         linewidth=2,
                                                         marker='o',
                                                         markersize=8,
                                                         label = groups[kk])
    
    return fig

def plot_new_time_sleep_course_single(df):
    
    groups = np.unique(df['Group'])
    subject = len(df)
    fr = df.T
    
    fig = plt.figure()
    
    gg = 1

    for kk in groups:
        plt.subplot(len(groups),1,gg)
        plt.title(kk)
        
        for sbj in range(subject):
            if fr[sbj]['Group'] == kk:
                plt.plot(fr[sbj][2:],label=fr[sbj][1])
                
        gg +=1
    
    return fig


def Plt_RawPowerDensity_GUI(Freq, y_axis_list, color_list = ['r'],
                           linewidth = 2, legend_list = ['Wake'],
                           title = 'Power Density', title_size = 20, 
                           axis_label_size = 15,
                           legend_size = 15,ylim=None):
    """
        Function Target: 
        ================
            Plot the power density from input dataset
        Input:
        ======
            - Freq : numpy array
                x_axis vector
            - y_axis_list : list of numpy arrays
                each element of the list is a y_axis for delta power
        Output:
        =======
            - fig : matplotlib.figure.Figure
                The power density figure
    """
    fig = plt.figure(figsize=(4.5*3.13,3.5*3.13))
    #plt.hold(1)        
    for k in range(len(y_axis_list)):
        plt.plot(Freq, y_axis_list[k], color = color_list[k],
                 linewidth = linewidth, label = legend_list[k])
    plt.title(title, fontsize = title_size)
    plt.xlabel('Frequency (Hz)', fontsize = axis_label_size)
    plt.ylabel('Power Density', fontsize = axis_label_size)
    plt.legend(fontsize = legend_size)
    plt.xlim(0,max(Freq))
    if type(ylim) is tuple:
        plt.ylim(ylim)
    #plt.hold(0)
    return fig

def Plt_RawPowerDensity_Loop_GUI(Freq,Power_Wake,Power_Rem,Power_NRem,IndexGroup,
                             color_list = ['r','y','g'],linewidth = 2, 
                             legend_list = ['Wake','Rem','NRem'],
                             title_size = 20, axis_label_size = 15,
                             legend_size = 15):
    figDict = {}
    maxList = []
    for group in list(IndexGroup.keys()):
        for subject in list(IndexGroup[group].keys()):
            row = IndexGroup[group][subject]
            maxList += [np.max([np.max(Power_Wake[row]),np.max(Power_Rem[row]),
                                np.max(Power_NRem[row])])]
    ylim = (0,np.max(maxList)*1.05)
    for group in list(IndexGroup.keys()):
        for subject in list(IndexGroup[group].keys()):
            noext = subject.split('.')[0]
            title = 'Power Density\n%s (%s)'%(noext,group)
            row = IndexGroup[group][subject]
            y_axis_list = [Power_Wake[row],Power_Rem[row],Power_NRem[row]]
            figDict[subject] =\
                Plt_RawPowerDensity_GUI(Freq, y_axis_list,
                                        color_list = color_list,
                                        linewidth = linewidth,
                                        legend_list = legend_list,
                                        title = title,
                                        title_size = title_size, 
                                        axis_label_size = axis_label_size,
                                        legend_size = legend_size,ylim=ylim)
    return figDict

def Plt_MedianPowerDensity_GUI(Freq, PowerW_matrix, PowerR_matrix,
                               PowerNR_matrix, IndexArray_dict, 
                               color_list = ['k', 'r', 'b'],
                               linewidth = 2, legend_list = ['Wake', 'Rem',
                               'NRem'], suptitle = 'Power Density',
                               suptitle_size = 25, axis_label_size = 10,
                               legend_size = 15,title_size=15,
                               MeanOrMedian = 'Mean'):
    fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
    nrow = len(list(IndexArray_dict.keys()))
    ind = 1
    MAX_list = []
    for key in list(IndexArray_dict.keys()):
        Index   = IndexArray_dict[key]
        if MeanOrMedian == 'Median':
            PowerW  = np.nanmedian(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmedian(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmedian(PowerNR_matrix[Index],axis=0)

        else:
            PowerW  = np.nanmean(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmean(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmean(PowerNR_matrix[Index],axis=0)
            
        MAX_list += [np.max([np.max(PowerW),np.max(PowerNR),np.max(PowerR)])]
    ylim = (0,1.05*np.max(MAX_list))
    genotype_mean = {}
    gen_yer = {}
    for key in list(IndexArray_dict.keys()):
        plt.subplot(nrow,1,ind)
        Index   = IndexArray_dict[key]
        if MeanOrMedian == 'Median':
            PowerW  = np.nanmedian(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmedian(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmedian(PowerNR_matrix[Index],axis=0)
            
            PowerWs = np.percentile(PowerW_matrix[Index], 75, axis=0)
            PowerRs = np.percentile(PowerR_matrix[Index], 75, axis=0)
            PowerNRs = np.percentile(PowerNR_matrix[Index], 75, axis=0)
            
            error_high = np.array([PowerWs,PowerRs,PowerNRs])
            
            PowerWs = np.percentile(PowerW_matrix[Index], 25, axis=0)
            PowerRs = np.percentile(PowerR_matrix[Index], 25, axis=0)
            PowerNRs = np.percentile(PowerNR_matrix[Index], 25, axis=0)
            
            error_low = np.array([PowerWs,PowerRs,PowerNRs])
            gen_yer[key] = {'high':error_high,'low':error_low}
            genotype_mean[key] = [PowerW,PowerR,PowerNR]
            
        else:
            PowerW  = np.nanmean(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmean(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmean(PowerNR_matrix[Index],axis=0)
            
            PowerWs = sts.sem(PowerW_matrix[Index],axis=0)
            PowerRs = sts.sem(PowerR_matrix[Index],axis=0)
            PowerNRs = sts.sem(PowerNR_matrix[Index],axis=0)
            genotype_mean[key] = [PowerW,PowerR,PowerNR]
#        yVal = np.array([PowerW,PowerR,PowerNR])
            yErr = np.array([PowerWs,PowerRs,PowerNRs])
            gen_yer[key] = yErr
        plt.title('Genotype: %s'%key, fontsize = title_size)
        plt.xlabel('Frequency (Hz)', fontsize = axis_label_size)
        plt.ylabel('Power Density', fontsize = axis_label_size)
        PP = [PowerW,PowerR,PowerNR]
        legend_list = []
        for k in range(3):
#            plt.plot(Freq, PP[k], color = color_list[k],
#                 linewidth = linewidth, label = legend_list[k])
            if MeanOrMedian == 'Median':
                legend_list += [plt.errorbar(Freq, PP[k],yerr=np.vstack([error_low[k,:], error_high[k,:]]),color = color_list[k])]
            else:
                legend_list += [plt.errorbar(Freq, PP[k],yerr=yErr[k,:],color = color_list[k])]
        plt.legend(legend_list,['Wake','REM','NREM'],fontsize = legend_size)
        ind += 1
        plt.ylim(ylim)  
        plt.xlim(0,max(Freq))
    plt.suptitle(suptitle, fontsize = suptitle_size)

    list_title = ['Power Wake','Power REM','Power NREM']
    tuple_fig = ()
    color_list = ['k', 'r', 'b','g','y',(125./255,)*3,'m','c']
    for k in range(3):
        tuple_fig += (plt.figure(figsize=(5.5*3.13,3.5*3.13)),)
        legend_list = []
        legend_lab = []
        plt.title(list_title[k],fontsize=20)
        i = 0
        for key in list(IndexArray_dict.keys()):
            if type(gen_yer[key]) is dict:
                legend_list += [plt.errorbar(Freq, genotype_mean[key][k],yerr=np.vstack([gen_yer[key]['low'][k,:], gen_yer[key]['high'][k,:]]),color=color_list[i%len(color_list)])]
            else:
                legend_list += [plt.errorbar(Freq, genotype_mean[key][k],yerr=gen_yer[key][k],color=color_list[i%len(color_list)])]
            legend_lab += [key]
            i += 1
        plt.xlabel('Frequency (Hz)', fontsize = axis_label_size)
        plt.ylabel('Power Density', fontsize = axis_label_size)
        plt.legend(legend_list,legend_lab,fontsize = legend_size)
    return (fig,) + tuple_fig
