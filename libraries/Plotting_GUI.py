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
import datetime as dt
import scipy.stats as sts

def plot_raster(Input):
    
    for kk in Input.keys():
        Raster = Input[kk]
        XMIN,XMAX,YMIN,YMAX = np.inf, 0, np.inf, 0
        strn = kk

        end=Raster-np.hstack((Raster[:,1:],np.zeros((np.size(Raster,axis=0),1))))
        Ind=np.where(end==-1)
        Ind=(Ind[0],Ind[1]+1)
        v0=np.zeros((np.size(Raster,axis=0),np.size(Raster,axis=1)))
        v0[Ind]=1
        
        Ind=np.where(end==1)
        v1=np.zeros((np.size(Raster,axis=0),np.size(Raster,axis=1)))
        v1[Ind]=1
        
        I0=np.where(v0==1)
        I1=np.where(v1==1)
        
        if strn=='l':
            print('left')
            color1='r'
            color2='or'
            label = 'NP right'
        else:
            print('right')
            color1='b'
            color2='ob'
            label = 'NP left'
        
        scale = 10
        fig = plt.figure()
        plt.plot(I1[1]/float(scale),I1[0]+1,'ow')
        plt.plot(I0[1]/float(scale),I0[0]+1,color2)
        plt.hlines(I0[0]+1,I0[1]/float(scale),I1[1]/float(scale),color1,label=label)
        xmin,xmax = plt.xlim()
        ymin,ymax = plt.ylim()
        XMIN = min(XMIN,xmin)
        XMAX = max(XMAX,xmax)
        YMIN = min(YMIN,ymin)
        YMAX = max(YMAX,ymax)
    
    plt.xlim(XMIN,XMAX)
    plt.ylim(YMIN,YMAX)

    plt.title('Raster plot')
    plt.legend()
    plt.ylabel('Trial number')
    plt.xlabel('Time(sec)')
    
    return fig

def plot_peak_procedure(Input):
    
    df = Input['all Subject'][0]
    loc = Input['all Subject'][1]
    xlab = Input['all Subject'][2]
    x_axis = Input['all Subject'][3]
    y_axis = Input['all Subject'][4]
    
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
    
    fig1 = plt.figure()
    plt.title(loc)
    for kk in range(len(groups)):
        sbj_tr = x_label == kk+1
        m = np.nanmean(x_group[sbj_tr,:],axis = 0)
        s = np.nanstd(x_group[sbj_tr,:],axis = 0)/np.sqrt(np.sum(sbj_tr))
        plt.errorbar(xlab,y = m, yerr = s,  elinewidth=2.5,
                                                         linewidth=2,
                                                         marker='o',
                                                         markersize=8,
                                                         label = groups[kk])
    
#    ind = np.arange(m.shape[0])
#    plt.xticks(ind, xlab)
    plt.legend()
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    fig2 = plt.figure()
    plt.title(loc)
    gg = 1
    for kk in groups:
        plt.subplot(len(groups),1,gg)
        for sbj in range(subject):
            if fr[sbj]['Group'] == kk:
                plt.plot(xlab,np.array(fr[sbj][2:]))
                
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    return fig1,fig2

def plot_ait(Input):
    
    df_m = Input[0]['AIT MEAN']
    df_s = Input[0]['AIT STD ERROR']
    labs = Input[1]
    title = Input[6]
    y_label = Input[7]
    x_label = 'Time [h]'
    
    hlab = np.array([])
    for kk in labs:
        hlab = np.hstack((hlab,kk[:2]))      
        
    labels = tuple(np.array(hlab))
    groups = np.unique(df_m['Group'])
   
    gg = 1
    fig = plt.figure(title)
    for gr in groups:
        plt.subplot(len(groups),1,gg)
        idx = df_m['Group'] == gr
        df_M = df_m[idx]
        df_S = df_s[idx]
        plt.title(gr)
        for sb in np.unique(df_M['Subject']):
            
            df_m_sub = df_M[df_M['Subject']==sb]
            df_s_sub = df_S[df_S['Subject']==sb]
            m = np.array([])
            s = np.array([])
            for kk in df_m_sub.keys()[2:]:
                m = np.hstack((m,df_m_sub[kk]))
                s = np.hstack((s,df_s_sub[kk]))
                
            plt.errorbar(range(m.shape[0]),y = m, yerr = s,elinewidth=2.5,
                                                           linewidth=2,
                                                           marker='o',
                                                           markersize=8,
                                                           label = sb)
            
        gg += 1
        ind = np.arange(m.shape[0])
        plt.xticks(ind, labels)
        plt.legend()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    
    return fig

def plot_errors(Input):
    
    df = Input[0]
    types = Input[1]
    x_label = Input[2]
    y_label = Input[3]
    dark_start = Input[4]
    dark_dur = Input[5]
    StatIndex = Input[6]
    Bins = Input[7]
    h_bins = Bins/3600
    
    if StatIndex == 'Mean':
        func = getattr(np,'nanmean')
    else:
        func = getattr(np,'nanmedian')
        
    
    groups = np.unique(df['Group'])
    subject = np.unique(df['Subject'])
    
    dark = np.arange(dark_start,dark_start+dark_dur,h_bins)%24
    res = np.zeros((len(subject),2*dark.shape[0]),dtype = float)
    
    sj = 0
    sbj_tr = np.array([])
    for sb in subject:
        time = np.array([])
        sub_df = df[df['Subject']==sb]
        for idx in sub_df.index:
            tmp = dt.datetime.strptime(sub_df['Time'][idx][12:], "%H:%M:%S")
            time = np.hstack((time,tmp))
       
        t0 = dt.datetime(1900, 1, 1, dark_start, 00)
        for zt in range(res.shape[1]):
            idx =  (time >= t0) & (time < t0+dt.timedelta(seconds = Bins))
            res[sj,zt] = 1-(func(sub_df['Correct'][idx]))
            t0 += dt.timedelta(seconds = Bins)
            if t0.day > 1:
                t0 -= dt.timedelta(hours = 24)
        sj += 1
        sbj_tr = np.hstack((sbj_tr,np.unique(sub_df['Group'])))
    
    
    if types == 'Single subject':
        fig = plt.figure()
        ss = 0
        for sb in subject:
            plt.plot(res[ss,:],label = sb)
            ss += 1
        plt.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.tight_layout()
        
    else:
        fig = plt.figure()
        gg = 1
        for gg in groups:
            idx = sbj_tr == gg
                
            m = np.nanmean(res[idx,:],axis = 0)
            s = np.nanstd(res[idx,:],axis = 0)/np.sqrt(np.sum(idx))  
            plt.errorbar(range(m.shape[0]),y = m, yerr = s,elinewidth=2.5,
                                                           linewidth=2,
                                                           marker='o',
                                                           markersize=8,
                                                           label = gg)
            
        plt.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.tight_layout()
  
    return fig
    
def plot_attentional(Input):
    
    df = Input[0]
    xlabel = Input[2]
    ylabel = Input[3]
    bins = Input[4]
    types = Input[5]
    dark_start = Input[6]
    dark_dur = Input[7]


    groups = np.unique(df['Group'])
    
    dark = np.array(range(dark_start,dark_start+dark_dur,bins))%24
    light = np.array(range(dark_start+dark_dur,dark_start+(dark_dur*2),bins))%24
    
    trials = df['Trial type']
    
    sbn = 1
    fig = plt.figure(types)
    for kk in np.unique(trials):
        sub_df = df[df['Trial type']==kk]
        plt.subplot(len(np.unique(trials)),1,sbn)
        first = True
        sbj_tr = np.array([])
        for sb in np.unique(sub_df['Subject']):
            tmp = np.zeros(int((dark_dur*2)/bins),dtype = float)
            hd = 0
            sbj_df = sub_df[sub_df['Subject']==sb]
            
            for hh in dark:
                idx = (sbj_df['Hour']>=hh)&(sbj_df['Hour']<(hh+bins))
                if 'Reaction' in types:
                    tmp[hd] = np.nanmean(sbj_df[types][idx])
                elif 'Error Type' in types:
                   perf = sbj_df[types][idx]
                   idx = perf == 1
                   tmp[hd] = 1-(np.nansum(idx)/float(perf.shape[0]))
                elif 'Anticipation' in types:
                    tmp[hd] = np.nansum(sbj_df[types][idx])
                elif 'Food' in types:
                    tmp[hd] = np.nansum(sbj_df[types][idx])
                    
                hd += 1
                
            for hh in light:
                idx = (sbj_df['Hour']>=hh)&(sbj_df['Hour']<(hh+bins))
                if 'Reaction' in types:
                    tmp[hd] = np.nanmean(sbj_df[types][idx])
                elif 'Error Type' in types:
                   perf = sbj_df[types][idx]
                   idx = perf == 1
                   tmp[hd] = 1-(np.nansum(idx)/float(perf.shape[0]))
                elif 'Anticipation' in types:
                    tmp[hd] = np.nansum(sbj_df[types][idx])
                elif 'Food' in types:
                    tmp[hd] = np.nansum(sbj_df[types][idx])
                    
                hd += 1
            
            if first:
                first = False 
                vect = tmp
            else:
                vect = np.vstack((vect,tmp))
        
        
            sbj_tr = np.hstack((sbj_tr,np.unique(sbj_df['Group'])))
        
        for gg in groups:
            idx = sbj_tr == gg
            
            m = np.nanmean(vect[idx,:],axis = 0)
            s = np.nanstd(vect[idx,:],axis = 0)/np.sqrt(np.sum(idx))  
            plt.errorbar(range(m.shape[0]),y = m, yerr = s,elinewidth=2.5,
                                                       linewidth=2,
                                                       marker='o',
                                                       markersize=8,
                                                       label = gg)
            plt.title(kk)
        
        sbn += 1
    
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    
    return fig
def plot_emg_norm(Input):
    wake = Input[0]
    rem = Input[1]
    nrem = Input[2]
#    title = Input[3]
    x_axis = Input[4]
    y_axis = Input[5]
    x_lab = Input[6]
    
    groups = np.unique(wake['Group'])
    subject = len(wake)

    x_group_wake = np.zeros((subject,len(wake.T[0][5:])),dtype=float)
    x_label_wake = np.zeros((subject),dtype=int)
    x_group_rem = np.zeros((subject,len(rem.T[0][5:])),dtype=float)
    x_label_rem = np.zeros((subject),dtype=int)
    x_group_nrem = np.zeros((subject,len(nrem.T[0][5:])),dtype=float)
    x_label_nrem = np.zeros((subject),dtype=int)
    gg = 1
    sb = 0
    for kk in groups:
        for sbj in range(subject):
            if wake.T[sbj]['Group'] == kk:
                x_group_wake[sb,:] = np.array(wake.T[sbj][5:])
                x_label_wake[sb] = gg
                x_group_rem[sb,:] = np.array(rem.T[sbj][5:])
                x_label_rem[sb] = gg
                x_group_nrem[sb,:] = np.array(nrem.T[sbj][5:])
                x_label_nrem[sb] = gg
                sb +=1  
        gg +=1
        
    fig1 = plt.figure()
    plt.title('Wake')
    for kk in range(len(groups)):
        sbj_tr = x_label_wake == kk+1
        m = np.nanmean(x_group_wake[sbj_tr,:],axis = 0)
        s = np.nanstd(x_group_wake[sbj_tr,:],axis = 0)/np.sqrt(np.sum(sbj_tr))
        plt.errorbar(range(m.shape[0]),y = m, yerr = s,elinewidth=2.5,
                                                       linewidth=2,
                                                       marker='o',
                                                       markersize=8,
                                                       label = groups[kk])
    labels = tuple(np.array(x_lab,dtype=np.str_))
    ind = np.arange(m.shape[0])
    plt.xticks(ind, labels)
    plt.legend()
    plt.yscale('log')
    plt.ylim(0.01, 100)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    fig2 = plt.figure()
    plt.title('rem')
    for kk in range(len(groups)):
        sbj_tr = x_label_rem == kk+1
        m = np.nanmean(x_group_rem[sbj_tr,:],axis = 0)
        s = np.nanstd(x_group_rem[sbj_tr,:],axis = 0)/np.sqrt(np.sum(sbj_tr))
        plt.errorbar(range(m.shape[0]),y = m, yerr = s,elinewidth=2.5,
                                                       linewidth=2,
                                                       marker='o',
                                                       markersize=8,
                                                       label = groups[kk])
    labels = tuple(np.array(x_lab,dtype=np.str_))
    ind = np.arange(m.shape[0])
    plt.xticks(ind, labels)
    plt.legend()
    plt.yscale('log')
    plt.ylim(0.01, 100)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    fig3 = plt.figure()
    plt.title('non rem')
    for kk in range(len(groups)):
        sbj_tr = x_label_nrem == kk+1
        m = np.nanmean(x_group_nrem[sbj_tr,:],axis = 0)
        s = np.nanstd(x_group_nrem[sbj_tr,:],axis = 0)/np.sqrt(np.sum(sbj_tr))
        plt.errorbar(range(m.shape[0]),y = m, yerr = s,elinewidth=2.5,
                                                       linewidth=2,
                                                       marker='o',
                                                       markersize=8,
                                                       label = groups[kk])
    labels = tuple(np.array(x_lab,dtype=np.str_))
    ind = np.arange(m.shape[0])
    plt.xticks(ind, labels)
    plt.legend()
    plt.yscale('log')
    plt.ylim(0.01, 100)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    return fig1,fig2,fig3

def plot_sleep_cycles(Input):
    df = Input[0]
    title = Input[1]
    x_axis = Input[2]
    y_axis = Input[3]
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
    plt.title(title)
    for kk in range(len(groups)):
        sbj_tr = x_label == kk+1
        m = np.nanmean(x_group[sbj_tr,:],axis = 0)
        s = np.nanstd(x_group[sbj_tr,:],axis = 0)/np.sqrt(np.sum(sbj_tr))
        plt.errorbar(range(m.shape[0]),y = m, yerr = s,elinewidth=2.5,
                                                       linewidth=2,
                                                       marker='o',
                                                       markersize=8,
                                                       label = groups[kk]) 
    labels = tuple(np.array(Input[4][:-1],dtype=np.str_))
    ind = np.arange(m.shape[0])
    plt.xticks(ind, labels)
    plt.legend()
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    return fig

def plot_new_time_sleep_course_group(Input):
    df = Input[0]
    title = Input[1]
    x_axis = Input[2]
    y_axis = Input[3]
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
    plt.title(title)
    for kk in range(len(groups)):
        sbj_tr = x_label == kk+1
        m = np.nanmean(x_group[sbj_tr,:],axis = 0)
        s = np.nanstd(x_group[sbj_tr,:],axis = 0)/np.sqrt(np.sum(sbj_tr))
        plt.errorbar(range(m.shape[0]),y = m, yerr = s,  elinewidth=2.5,
                                                         linewidth=2,
                                                         marker='o',
                                                         markersize=8,
                                                         label = groups[kk])
    plt.legend()
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    return fig

def plot_new_time_sleep_course_single(Input):
    df = Input[0]
    x_axis = Input[2]
    y_axis = Input[3]
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
        plt.legend()
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
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
