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

import os,sys
lib_fld = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
sys.path.append(lib_fld)
import pandas as pd
#import datetime
import numpy as np
from copy import copy
from auxiliary_functions import (powerDensity_function,
                                 vector_hours,bin_epi,epidur_if_binAdj)



def Power_Density(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    lock       = myInput[4]

    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))


    freqLim_Hz = Input[0]['DoubleSpinBox'][0]
    MeanOrMedian = Input[0]['Combo'][0]
    color_list = [Input[0]['Combo'][1],
                  Input[0]['Combo'][2],
                  Input[0]['Combo'][3]]
    legend_list = ['Wake', 'Rem', 'NRem']
    title_size = Input[0]['SpinBox'][0]
    linewidth  = Input[0]['SpinBox'][1]
    legend_size = Input[0]['SpinBox'][2]
    axis_label_size = Input[0]['SpinBox'][3]
    suptitle_size = Input[0]['SpinBox'][4]
 
    DataDict = {}
    AllData  = {}
    for key in list(Datas.keys()):
        try:
            lock.lockForRead()
            AllData[key] = copy(Datas.takeDataset(key))
        finally:
            lock.unlock()
    
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1
   
    (Power_Wake, Power_Rem, Power_NRem, Fr,IndexArray_dict,IndexGroup) = \
                              powerDensity_function(AllData,DataGroup, freqLim_Hz)
                              
            

    first = True
    rc = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            if first:
                typesFr = np.array(np.round(Fr,decimals=2),dtype=np.str_)
                types = np.hstack((['Group','Subject'],typesFr))
                df_wake = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*Fr.shape[0]})
                df_nrem = np.zeros((count_sub,), dtype={'names': types,
                                                        'formats': ('U%d'%lenGroupName, 'U%d'%lenName,) + (float,) * Fr.shape[0]})
                df_rem = np.zeros((count_sub,), dtype={'names': types,
                                                        'formats': ('U%d'%lenGroupName, 'U%d'%lenName,) + (float,) * Fr.shape[0]})
                first = False
            cc = 0
            for col in typesFr:
                df_wake[col][rc] = Power_Wake[IndexGroup[key][name],cc]
                df_nrem[col][rc] = Power_NRem[IndexGroup[key][name], cc]
                df_rem[col][rc] = Power_Rem[IndexGroup[key][name], cc]
                cc += 1
            df_wake['Subject'][rc] = name
            df_wake['Group'][rc] = key

            df_nrem['Subject'][rc] = name
            df_nrem['Group'][rc] = key

            df_rem['Subject'][rc] = name
            df_rem['Group'][rc] = key
            rc += 1


                
    DataDict['Power Density Wake'] = pd.DataFrame(df_wake)

    DataDict['Power Density NRem'] = pd.DataFrame(df_nrem)

    DataDict['Power Density Rem'] = pd.DataFrame(df_rem)

    dictPlot['Fig:Power Density'] = {}
    dictPlot['Fig:Power Density']['Single Subject'] = (Fr,Power_Wake,\
                                                       Power_Rem,Power_NRem,\
                                                       IndexGroup,\
                                                       color_list,linewidth,\
                                                       legend_list ,\
                                                       title_size,\
                                                       axis_label_size,\
                                                       legend_size)
                               
    dictPlot['Fig:Power Density']['Group'] = (Fr, Power_Wake, Power_Rem,
                                              Power_NRem, IndexArray_dict, 
                                              color_list, linewidth,
                                              legend_list, 'Power Density',
                                              suptitle_size, axis_label_size,
                                              legend_size, title_size,
                                              MeanOrMedian)

    info['Types']  = ['Group EEG','Power Density']
    info['Factor'] = [0,1,2]
    datainfo = {'Power Density Wake': info,'Power Density Rem': info,
                'Power Density NRem': info}
    DD = {}
    DD['Power Density'] = {}
    DD['Power Density']['Power Density Wake'] = DataDict['Power Density Wake']
    DD['Power Density']['Power Density Rem'] = DataDict['Power Density Rem']
    DD['Power Density']['Power Density NRem'] = DataDict['Power Density NRem']

    return DD, dictPlot, datainfo


def Sleep_Time_Course(*myInput):
    DataDict, dictPlot, datainfo = {},{},{}
    
    Datas = myInput[0]
    Input = myInput[1]
    lock = myInput[4]
    
    DataGroup  = myInput[2]
    Bin = Input[0]['SpinBox'][0]
    EpochDur = Input[0]['SpinBox'][1]
    tick_Num = Input[0]['SpinBox'][2]
    dark_start = Input[0]['SpinBox'][3]
    Type = Input[0]['Combo'][0]
    stat_index = Input[0]['Combo'][1]
    total_or_mean = Input[0]['Combo'][2]
    
    
    epidur = 3600 * Bin
    
    if (2 in Type) and (3 in Type):
        epochType = 'S'
    elif 1 in Type:
        epochType = 'W'
    elif 2 in Type:
        epochType = 'R'
    else:
        epochType = 'NR'
    
    AllData  = {}
    for group in list(DataGroup.keys()):
        for key in DataGroup[group]:
            try:
                lock.lockForRead()
                AllData[key] = copy(Datas.takeDataset(key))
            finally:
                lock.unlock()


    for name in list(AllData.keys()):
        Time = AllData[name].Timestamp
        
        h0 = Time[0].hour
        if Time[0].minute > 58:
            h0 += 1
            
        if h0 > 12:
            light_hours = np.arange(h0+12,h0+24)%24
            dark_hours = np.arange(h0,h0+12)%24
        else:
            dark_hours = np.arange(h0+12,h0+24)%24
            light_hours = np.arange(h0,h0+12)%24
            
        hours = vector_hours(Time)
        
        
        index_light = np.zeros(0,dtype=int)
        for h in light_hours:
            index_light = np.hstack((index_light, np.where(hours == h)[0]))
        
        index_dark = np.zeros(0,dtype=int)
        for h in dark_hours:
            index_dark = np.hstack((index_dark, np.where(hours == h)[0]))
            
        i0 = index_light[0]
        i1 = index_light[-1]

        epi_l = bin_epi(AllData[name][index_light], epidur, Time[i0],Time[i1],epoch=epochType)
        mepidur_l = epidur_if_binAdj(epi_l, epidur,epochDur=EpochDur)

        
    
                
                
    
    
#    if (2 in Type) and (3 in Type):
#        word = 'Sleep'
#    elif 1 in Type:
#        word = 'Wake'
#    elif 2 in Type:
#        word = 'Rem'
#    else:
#        word = 'NRem'
#    
#    
#    
#    
#    DataDict = {'Sleep Time Course' : {}}
#    DataDict['Sleep Time Course']['Group %s Num Episodes'%word] =\
#        std_Matrix_Group
#    if total_or_mean == 'Mean':
#        DataDict['Sleep Time Course']['Group %s Episode Duration'%word] =\
#            std_Matrix_Group_Dur
#    else:
#        DataDict['Sleep Time Course']['Group Total %s'%word] =\
#            std_Matrix_Group_Dur
#    DataDict['Sleep Time Course']['%s Num Episodes'%word] = std_Matrix_Nep
#    if total_or_mean == 'Mean':
#        DataDict['Sleep Time Course']['%s Episode Duration'%word] =\
#            std_Matrix_Dur
#    else:
#        DataDict['Sleep Time Course']['Total %s'%word] =\
#            std_Matrix_Dur
#    DataDict['Sleep Time Course']['Daily %s Num Episodes'%word] = std_Daily_Nep
#    if total_or_mean == 'Mean':            
#        DataDict['Sleep Time Course']['Daily %s Episode Duration'%word] =\
#            std_Daily_Dur
#    else:
#        DataDict['Sleep Time Course']['Daily Total %s'%word] = std_Daily_Dur
#    
#    info = {}
#    info['Types']  = ['Single Subject EEG','Num Episodes']
#    info['Factor'] = [0,1]
#    datainfo = {'%s Num Episodes'%word: info}
#    
#    info = {}
#    info['Types']  = ['Single Subject EEG','Episode Duration']
#    info['Factor'] = [0,1]
#    if total_or_mean == 'Mean':
#        datainfo['%s Episode Duration'%word] = info
#    else:
#        datainfo['Total %s'%word] = info
#    info = {}
#    info['Types']  = ['Single Subject EEG','Daily Num Episodes']
#    info['Factor'] = [0,1]
#    datainfo['Daily %s Num Episodes'%word] = info
#    
#    info = {}
#    info['Types']  = ['Single Subject EEG','Daily Episode Duration']
#    info['Factor'] = [0,1]
#    if total_or_mean == 'Mean':
#        datainfo['Daily %s Episode Duration'%word] = info
#    else:
#        datainfo['Daily Total %s'%word] = info
#    
#    
#    info = {}
#    info['Types']  = ['Group EEG','Episode Duration']
#    info['Factor'] = [0,1]
#    if total_or_mean == 'Mean':
#        datainfo['Group %s Episode Duration'%word] = info
#    else:
#        datainfo['Group Total %s'%word] = info
#    
#    info = {}
#    info['Types']  = ['Group EEG','Num Episodes']
#    info['Factor'] = [0,1]
#    datainfo['Group %s Num Episodes'%word] = info
#      
#    title = 'Number of sleep episodes: %s'%word
#    x_label = ''
#    y_label = 'Episodes num'
#    dictPlot = {'Fig:Sleep Time Course' : {}}
#    dictPlot['Fig:Sleep Time Course']['%s Num Episodes'%word] =\
#        (std_Matrix_Group, title, x_label, y_label, True, stat_index, 1.5, 20,
#         12, 15, tick_Num)
#    if total_or_mean == 'Mean':
#        title = '%s episode duration'%word
#        y_label = 'Episodes duration (min)'
#        saveName = '%s Episode Duration'%word
#    else:
#        title = 'Total %s'%word
#        y_label = '%s total (min)'%word
#        saveName = 'Total %s'%word
#    x_label = ''
#    
#    dictPlot['Fig:Sleep Time Course'][saveName] = (std_Matrix_Group_Dur, title, x_label, y_label, True, stat_index,1.5, 20, 12, 15, tick_Num)
#    
    
    return DataDict,dictPlot, datainfo
            
    
    
    
    return DataDict,dictPlot, datainfo



#def Group_Error_Rate(*myInput):
#    DataDict, dictPlot, info = {},{},{}
#    
#    Datas      = myInput[0]
#    Input      = myInput[1]
#    DataGroup  = myInput[2]
#    TimeStamps = myInput[3]
#    lock       = myInput[4]
#    
#    Dark_start = Input[0]['Combo'][0]
#    Dark_length = Input[0]['Combo'][1]
#    StatIndex = Input[0]['Combo'][2]
#    TimeInterval = Input[0]['Combo'][3]
#    Dataset_Dict = {}
#    TimeStamps_Dict = {}
#
#    for group in list(DataGroup.keys()):
#        for dataName in DataGroup[group]:
#            try:
#                lock.lockForRead()
#                Dataset_Dict[dataName] = copy(Datas.takeDataset(dataName))
#                if Datas.getTimeStamps(dataName):
#                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
#                else:
#                    TimeStamps_Dict[dataName] = TimeStamps
#            finally:
#                lock.unlock()
#    VectorError = std_Subjective_Error_Rate_GUI(Dataset_Dict, TimeStamps_Dict,
#                                                DarkStart = Dark_start,
#                                                DarkDuration = Dark_length,
#                                                TimeInterval = TimeInterval) 
#
#    Error_Group_Matrix = stdMatrix_Group_Stat_Index_GUI(VectorError, DataGroup)
#    x_label = 'Time (h)'
#    y_label = 'Error Rate'
#
#    DataDict = {'Group Error Rate' : {}}
#    DataDict['Group Error Rate']['Error Rate'] = Error_Group_Matrix
#    dictPlot = {}
#    dictPlot['Fig: Group Error Rate'] = {}
#    dictPlot['Fig: Group Error Rate']['Error Rate'] = (
#        Error_Group_Matrix, Dark_length, TimeInterval, 'Error Rate group',
#        x_label, y_label, 20, 15, 12, 15, True, StatIndex, 1.5, 2, 4, 0.4)
#    info = {}
#    info['Error Rate'] = {'Error Rate' : {}}
#    info['Error Rate']['Types'] =\
#        ['Group', 'Error Rate']
#    info['Error Rate']['Factor'] = [0,1]
#    return DataDict, dictPlot, info
#
#def error_rate():
#    return 4
#
def Linear_Discriminant_Analysis():
    return 4
#def Multiple_Regression_Analysis():
#    return 4
def LDA():
    return 4
#def Switch_Latency():
#    return 4
#def delta_rebound():
#    return 4
#def Actograms():
#    return 4
#def AIT():
#    return 4
#
#def raster_plot():
#    return 4
#def peak_procedure():
#    return 4
#def Attentional_analysis():
#    return 4
#def sleep_fragmentation():
#    return 4
#def Sleep_cycles():
#    return 4
#def emg_normalized():
#    return 4


    

def Switch_Latency_TEST(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    Tend = Input[0]['DoubleSpinBox'][0]
    ts = Input[0]['DoubleSpinBox'][1]
    tl = Input[0]['DoubleSpinBox'][2]
    Short = ts
    Long = tl
    ProbeShort = Input[0]['DoubleSpinBox'][3]
    Cond_SProbe = Input[0]['DoubleSpinBox'][4]
    Cond_LProbe = Input[0]['DoubleSpinBox'][5] 
    Mean_minmax = Input[0]['Range'][0]
    Cv_minmax = Input[0]['Range'][1]
    Dark_start = Input[0]['Combo'][0]
    Dark_length   = Input[0]['Combo'][1]
    type_tr   = Input[0]['Combo'][2]
    Long_Side = Input[0]['Combo'][3]
    group_list = DataGroup.keys()
    group_list.sort()
    long_side_dict = {}
    k = 0
    for gr in group_list:
        long_side_dict[gr] = Long_Side
        k += 1
    Mouse_Name = np.hstack(DataGroup.values())
    lenName = 0
    lenGroupName = 0
    for key in DataGroup.keys():
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    Mouse_Grouped = DataGroup
    AllData = OrderedDict()
    TimeStamps_Dict = {}
    DataDict = {}
    DataDict['Group Switch Latency'] = {}
    long_side_sub = {}
    print('CREATING TIMESTAMPS DICT')
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            try:
                lock.lockForRead()
                AllData[dataName] = copy(Datas.takeDataset(dataName))
                if Datas.getTimeStamps(dataName):
                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
                else:
                    TimeStamps_Dict[dataName] = TimeStamps
            finally:
                lock.unlock()
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            long_side_sub[dataName] = long_side_dict[gr]
    print('\n\nGR SWITCH LAT\n\n')          
    table,left,right,Record_Switch,HSSwitch = F_New_Gr_Switch_Latency_GUI(AllData,TimeStamps_Dict,Mouse_Name,ts=ts,tl=tl,scale=1,Tend=Tend,Long_Side=long_side_sub,type_tr=type_tr)
    for name in Record_Switch.keys():
        if Record_Switch[name].shape[0] < 10:
            message = '%s less then 10 trials...'%name
            Record_Switch.pop(name)
            HSSwitch.pop(name)
            right.pop(name)
            left.pop(name)
            table.pop(name)
            AllData.pop(name)
            for gr in Mouse_Grouped.keys():
                if name in Mouse_Grouped[gr]:
                    Mouse_Grouped[gr].remove(name)
    prev_groups = Mouse_Grouped.keys()
    for gr in prev_groups:
        if not len(Mouse_Grouped[gr]):
            s = Mouse_Grouped.pop(gr)
    func = lambda h : h.hour
    v_func = np.vectorize(func)
    tmp = {}
    for name in Record_Switch.keys():
        tmp[name] = v_func(HSSwitch[name])
    HSSwitch = tmp
    Hour_Dark,Hour_Light=Hour_Light_and_Dark_GUI(Dark_start,Dark_length)
    Best_Model,Pdf,Cdf,EmCdf=F_Gr_Fit_GMM_GUI(Record_Switch,Mouse_Grouped,n_gauss=1)
    Median,Mean,Std=Subj_Median_Mean_Std_GUI(Record_Switch,HSSwitch)
    Hour_label = TimeUnit_to_Hours_GUI(np.hstack((Hour_Dark,Hour_Light)),3600)
    DataLen    = len(Hour_label) * len(Record_Switch.keys())
    print('\n\nGMM FIT\n\n')  
    std_Switch, GMM_Fit = std_Switch_Latency_GUI(Record_Switch, HSSwitch,
                                                 Mouse_Grouped, Dark_start=Dark_start, 
                                                 Dark_length=Dark_length)
    EXP, MAX = F_ExpGain_GUI(Short, Long, ProbeShort, Cond_SProbe, Cond_LProbe,
                             MeanRange=Mean_minmax,CVRange=Cv_minmax)
    std_Exp_Gain = Exp_Gain_Matrix_GUI(GMM_Fit, Short, Long, Mouse_Grouped, 
                                       ProbeShort, Cond_SProbe,
                                       Cond_LProbe)
    std_Exp_Gain['Value'] = std_Exp_Gain ['Value']/np.max(EXP)
    DataDict['Group Switch Latency']['Group Switch Latency'] = np.zeros(DataLen, dtype = {
        'names':('Group','Subject','Time','Mean','Median','SEM'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,'|S5',float,
                   float,float)})
    DataDict['Group Switch Latency']['Group Switch Latency']['Time'] = list(Hour_label) * len(Record_Switch.keys())
    ind = 0
    for key in Mouse_Grouped.keys():
        for name in Mouse_Grouped[key]:
            DataDict['Group Switch Latency']['Group Switch Latency']['Group'][ind:len(Hour_label)+ind]\
                = [key] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Subject'][ind:len(Hour_label)+ind]\
                = [name] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Mean'][ind:len(Hour_label)+ind]\
                = Mean[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['Median'][ind:len(Hour_label)+ind]\
                = Median[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['SEM'][ind:len(Hour_label)+ind]\
                = Std[name]
            ind += len(Hour_label)
    DataDict['Group Switch Latency']['Expected Gain'] = std_Exp_Gain
    Gr_Mean,Gr_Std=Gr_Mean_Std_GUI(Median,Mouse_Grouped)
    Group_Name = Mouse_Grouped.keys()
    dictPlot = {}
    dictPlot['Fig:Group Switch Latency'] = {}
    dictPlot['Fig:Group Switch Latency']['Boxplot'] = Gr_Mean,Hour_Light,Hour_Dark,\
                                            Group_Name
    dictPlot['Fig:Group Switch Latency']['Gaussian Fit'] = Cdf, EmCdf, Group_Name,\
                                            Mouse_Grouped, ts, tl
    dictPlot['Fig:Group Switch Latency']['Optimal Surface'] =\
        (EXP, MAX, Mean_minmax, Cv_minmax,
         std_Exp_Gain, 40, 12)
    dictPlot['Fig:Group Switch Latency']['Expected Gain'] =\
        (std_Exp_Gain, 'Expected Gain', 20, 1, 3, 1, 0.95,
        'Normalized Exp. Gain', 12, 15)
    info = {}
    info['Group Switch Latency'] = {}
    info['Group Switch Latency']['Types']  = ['Group', 'Switch Latency']
    info['Group Switch Latency']['Factor'] = [0,1,2]
    info['Expected Gain'] = {}
    info['Expected Gain']['Types']  = ['Single Subject', 'Expected Gain']
    info['Expected Gain']['Factor'] = [0,1]
    return DataDict,dictPlot,info

def Switch_Latency_TEST(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    Tend = Input[0]['DoubleSpinBox'][0]
    ts = Input[0]['DoubleSpinBox'][1]
    tl = Input[0]['DoubleSpinBox'][2]
    Short = ts
    Long = tl
    ProbeShort = Input[0]['DoubleSpinBox'][3]
    Cond_SProbe = Input[0]['DoubleSpinBox'][4]
    Cond_LProbe = Input[0]['DoubleSpinBox'][5] 
    Mean_minmax = Input[0]['Range'][0]
    Cv_minmax = Input[0]['Range'][1]
    Dark_start = Input[0]['Combo'][0]
    Dark_length   = Input[0]['Combo'][1]
    type_tr   = Input[0]['Combo'][2]
    Long_Side = Input[0]['Combo'][3]
    group_list = DataGroup.keys()
    group_list.sort()
    long_side_dict = {}
    k = 0
    for gr in group_list:
        long_side_dict[gr] = Long_Side
        k += 1
    Mouse_Name = np.hstack(DataGroup.values())
    lenName = 0
    lenGroupName = 0
    for key in DataGroup.keys():
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    Mouse_Grouped = DataGroup
    AllData = OrderedDict()
    TimeStamps_Dict = {}
    DataDict = {}
    DataDict['Group Switch Latency'] = {}
    long_side_sub = {}
    print('CREATING TIMESTAMPS DICT')
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            try:
                lock.lockForRead()
                AllData[dataName] = copy(Datas.takeDataset(dataName))
                if Datas.getTimeStamps(dataName):
                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
                else:
                    TimeStamps_Dict[dataName] = TimeStamps
            finally:
                lock.unlock()
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            long_side_sub[dataName] = long_side_dict[gr]
    print('\n\nGR SWITCH LAT\n\n')          
    table,left,right,Record_Switch,HSSwitch = F_New_Gr_Switch_Latency_GUI(AllData,TimeStamps_Dict,Mouse_Name,ts=ts,tl=tl,scale=1,Tend=Tend,Long_Side=long_side_sub,type_tr=type_tr)
    for name in Record_Switch.keys():
        if Record_Switch[name].shape[0] < 10:
            message = '%s less then 10 trials...'%name
            Record_Switch.pop(name)
            HSSwitch.pop(name)
            right.pop(name)
            left.pop(name)
            table.pop(name)
            AllData.pop(name)
            for gr in Mouse_Grouped.keys():
                if name in Mouse_Grouped[gr]:
                    Mouse_Grouped[gr].remove(name)
    prev_groups = Mouse_Grouped.keys()
    for gr in prev_groups:
        if not len(Mouse_Grouped[gr]):
            s = Mouse_Grouped.pop(gr)
    func = lambda h : h.hour
    v_func = np.vectorize(func)
    tmp = {}
    for name in Record_Switch.keys():
        tmp[name] = v_func(HSSwitch[name])
    HSSwitch = tmp
    Hour_Dark,Hour_Light=Hour_Light_and_Dark_GUI(Dark_start,Dark_length)
    Best_Model,Pdf,Cdf,EmCdf=F_Gr_Fit_GMM_GUI(Record_Switch,Mouse_Grouped,n_gauss=1)
    Median,Mean,Std=Subj_Median_Mean_Std_GUI(Record_Switch,HSSwitch)
    Hour_label = TimeUnit_to_Hours_GUI(np.hstack((Hour_Dark,Hour_Light)),3600)
    DataLen    = len(Hour_label) * len(Record_Switch.keys())
    print('\n\nGMM FIT\n\n')  
    std_Switch, GMM_Fit = std_Switch_Latency_GUI(Record_Switch, HSSwitch,
                                                 Mouse_Grouped, Dark_start=Dark_start, 
                                                 Dark_length=Dark_length)
    EXP, MAX = F_ExpGain_GUI(Short, Long, ProbeShort, Cond_SProbe, Cond_LProbe,
                             MeanRange=Mean_minmax,CVRange=Cv_minmax)
    std_Exp_Gain = Exp_Gain_Matrix_GUI(GMM_Fit, Short, Long, Mouse_Grouped, 
                                       ProbeShort, Cond_SProbe,
                                       Cond_LProbe)
    std_Exp_Gain['Value'] = std_Exp_Gain ['Value']/np.max(EXP)
    DataDict['Group Switch Latency']['Group Switch Latency'] = np.zeros(DataLen, dtype = {
        'names':('Group','Subject','Time','Mean','Median','SEM'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,'|S5',float,
                   float,float)})
    DataDict['Group Switch Latency']['Group Switch Latency']['Time'] = list(Hour_label) * len(Record_Switch.keys())
    ind = 0
    for key in Mouse_Grouped.keys():
        for name in Mouse_Grouped[key]:
            DataDict['Group Switch Latency']['Group Switch Latency']['Group'][ind:len(Hour_label)+ind]\
                = [key] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Subject'][ind:len(Hour_label)+ind]\
                = [name] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Mean'][ind:len(Hour_label)+ind]\
                = Mean[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['Median'][ind:len(Hour_label)+ind]\
                = Median[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['SEM'][ind:len(Hour_label)+ind]\
                = Std[name]
            ind += len(Hour_label)
    DataDict['Group Switch Latency']['Expected Gain'] = std_Exp_Gain
    Gr_Mean,Gr_Std=Gr_Mean_Std_GUI(Median,Mouse_Grouped)
    Group_Name = Mouse_Grouped.keys()
    dictPlot = {}
    dictPlot['Fig:Group Switch Latency'] = {}
    dictPlot['Fig:Group Switch Latency']['Boxplot'] = Gr_Mean,Hour_Light,Hour_Dark,\
                                            Group_Name
    dictPlot['Fig:Group Switch Latency']['Gaussian Fit'] = Cdf, EmCdf, Group_Name,\
                                            Mouse_Grouped, ts, tl
    dictPlot['Fig:Group Switch Latency']['Optimal Surface'] =\
        (EXP, MAX, Mean_minmax, Cv_minmax,
         std_Exp_Gain, 40, 12)
    dictPlot['Fig:Group Switch Latency']['Expected Gain'] =\
        (std_Exp_Gain, 'Expected Gain', 20, 1, 3, 1, 0.95,
        'Normalized Exp. Gain', 12, 15)
    info = {}
    info['Group Switch Latency'] = {}
    info['Group Switch Latency']['Types']  = ['Group', 'Switch Latency']
    info['Group Switch Latency']['Factor'] = [0,1,2]
    info['Expected Gain'] = {}
    info['Expected Gain']['Types']  = ['Single Subject', 'Expected Gain']
    info['Expected Gain']['Factor'] = [0,1]
    return DataDict,dictPlot,info

def Switch_Latency_TEST(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    Tend = Input[0]['DoubleSpinBox'][0]
    group_list = DataGroup.keys()
    group_list.sort()
    long_side_dict = {}
    k = 0
    for gr in group_list:
        long_side_dict[gr] = Long_Side
        k += 1
    Mouse_Name = np.hstack(DataGroup.values())
    lenName = 0
    lenGroupName = 0
    for key in DataGroup.keys():
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    Mouse_Grouped = DataGroup
    AllData = OrderedDict()
    TimeStamps_Dict = {}
    DataDict = {}
    DataDict['Group Switch Latency'] = {}
    long_side_sub = {}
    print('CREATING TIMESTAMPS DICT')
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            try:
                lock.lockForRead()
                AllData[dataName] = copy(Datas.takeDataset(dataName))
                if Datas.getTimeStamps(dataName):
                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
                else:
                    TimeStamps_Dict[dataName] = TimeStamps
            finally:
                lock.unlock()
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            long_side_sub[dataName] = long_side_dict[gr]
    print('\n\nGR SWITCH LAT\n\n')          
    table,left,right,Record_Switch,HSSwitch = F_New_Gr_Switch_Latency_GUI(AllData,TimeStamps_Dict,Mouse_Name,ts=ts,tl=tl,scale=1,Tend=Tend,Long_Side=long_side_sub,type_tr=type_tr)
    for name in Record_Switch.keys():
        if Record_Switch[name].shape[0] < 10:
            message = '%s less then 10 trials...'%name
            Record_Switch.pop(name)
            HSSwitch.pop(name)
            right.pop(name)
            left.pop(name)
            table.pop(name)
            AllData.pop(name)
            for gr in Mouse_Grouped.keys():
                if name in Mouse_Grouped[gr]:
                    Mouse_Grouped[gr].remove(name)
    prev_groups = Mouse_Grouped.keys()
    for gr in prev_groups:
        if not len(Mouse_Grouped[gr]):
            s = Mouse_Grouped.pop(gr)
    func = lambda h : h.hour
    v_func = np.vectorize(func)
    tmp = {}
    for name in Record_Switch.keys():
        tmp[name] = v_func(HSSwitch[name])
    HSSwitch = tmp
    Hour_Dark,Hour_Light=Hour_Light_and_Dark_GUI(Dark_start,Dark_length)
    Best_Model,Pdf,Cdf,EmCdf=F_Gr_Fit_GMM_GUI(Record_Switch,Mouse_Grouped,n_gauss=1)
    Median,Mean,Std=Subj_Median_Mean_Std_GUI(Record_Switch,HSSwitch)
    Hour_label = TimeUnit_to_Hours_GUI(np.hstack((Hour_Dark,Hour_Light)),3600)
    DataLen    = len(Hour_label) * len(Record_Switch.keys())
    print('\n\nGMM FIT\n\n')  
    std_Switch, GMM_Fit = std_Switch_Latency_GUI(Record_Switch, HSSwitch,
                                                 Mouse_Grouped, Dark_start=Dark_start, 
                                                 Dark_length=Dark_length)
    EXP, MAX = F_ExpGain_GUI(Short, Long, ProbeShort, Cond_SProbe, Cond_LProbe,
                             MeanRange=Mean_minmax,CVRange=Cv_minmax)
    std_Exp_Gain = Exp_Gain_Matrix_GUI(GMM_Fit, Short, Long, Mouse_Grouped, 
                                       ProbeShort, Cond_SProbe,
                                       Cond_LProbe)
    std_Exp_Gain['Value'] = std_Exp_Gain ['Value']/np.max(EXP)
    DataDict['Group Switch Latency']['Group Switch Latency'] = np.zeros(DataLen, dtype = {
        'names':('Group','Subject','Time','Mean','Median','SEM'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,'|S5',float,
                   float,float)})
    DataDict['Group Switch Latency']['Group Switch Latency']['Time'] = list(Hour_label) * len(Record_Switch.keys())
    ind = 0
    for key in Mouse_Grouped.keys():
        for name in Mouse_Grouped[key]:
            DataDict['Group Switch Latency']['Group Switch Latency']['Group'][ind:len(Hour_label)+ind]\
                = [key] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Subject'][ind:len(Hour_label)+ind]\
                = [name] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Mean'][ind:len(Hour_label)+ind]\
                = Mean[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['Median'][ind:len(Hour_label)+ind]\
                = Median[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['SEM'][ind:len(Hour_label)+ind]\
                = Std[name]
            ind += len(Hour_label)
    DataDict['Group Switch Latency']['Expected Gain'] = std_Exp_Gain
    Gr_Mean,Gr_Std=Gr_Mean_Std_GUI(Median,Mouse_Grouped)
    Group_Name = Mouse_Grouped.keys()
    dictPlot = {}
    dictPlot['Fig:Group Switch Latency'] = {}
    dictPlot['Fig:Group Switch Latency']['Boxplot'] = Gr_Mean,Hour_Light,Hour_Dark,\
                                            Group_Name
    dictPlot['Fig:Group Switch Latency']['Gaussian Fit'] = Cdf, EmCdf, Group_Name,\
                                            Mouse_Grouped, ts, tl
    dictPlot['Fig:Group Switch Latency']['Optimal Surface'] =\
        (EXP, MAX, Mean_minmax, Cv_minmax,
         std_Exp_Gain, 40, 12)
    dictPlot['Fig:Group Switch Latency']['Expected Gain'] =\
        (std_Exp_Gain, 'Expected Gain', 20, 1, 3, 1, 0.95,
        'Normalized Exp. Gain', 12, 15)
    info = {}
    info['Group Switch Latency'] = {}
    info['Group Switch Latency']['Types']  = ['Group', 'Switch Latency']
    info['Group Switch Latency']['Factor'] = [0,1,2]
    info['Expected Gain'] = {}
    info['Expected Gain']['Types']  = ['Single Subject', 'Expected Gain']
    info['Expected Gain']['Factor'] = [0,1]
    return DataDict,dictPlot,info

def Switch_Latency_TEST(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    Tend = Input[0]['DoubleSpinBox'][0]
    group_list = DataGroup.keys()
    group_list.sort()
    long_side_dict = {}
    k = 0
    for gr in group_list:
        long_side_dict[gr] = Long_Side
        k += 1
    Mouse_Name = np.hstack(DataGroup.values())
    lenName = 0
    lenGroupName = 0
    for key in DataGroup.keys():
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    Mouse_Grouped = DataGroup
    AllData = OrderedDict()
    TimeStamps_Dict = {}
    DataDict = {}
    DataDict['Group Switch Latency'] = {}
    long_side_sub = {}
    print('CREATING TIMESTAMPS DICT')
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            try:
                lock.lockForRead()
                AllData[dataName] = copy(Datas.takeDataset(dataName))
                if Datas.getTimeStamps(dataName):
                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
                else:
                    TimeStamps_Dict[dataName] = TimeStamps
            finally:
                lock.unlock()
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            long_side_sub[dataName] = long_side_dict[gr]
    print('\n\nGR SWITCH LAT\n\n')          
    table,left,right,Record_Switch,HSSwitch = F_New_Gr_Switch_Latency_GUI(AllData,TimeStamps_Dict,Mouse_Name,ts=ts,tl=tl,scale=1,Tend=Tend,Long_Side=long_side_sub,type_tr=type_tr)
    for name in Record_Switch.keys():
        if Record_Switch[name].shape[0] < 10:
            message = '%s less then 10 trials...'%name
            Record_Switch.pop(name)
            HSSwitch.pop(name)
            right.pop(name)
            left.pop(name)
            table.pop(name)
            AllData.pop(name)
            for gr in Mouse_Grouped.keys():
                if name in Mouse_Grouped[gr]:
                    Mouse_Grouped[gr].remove(name)
    prev_groups = Mouse_Grouped.keys()
    for gr in prev_groups:
        if not len(Mouse_Grouped[gr]):
            s = Mouse_Grouped.pop(gr)
    func = lambda h : h.hour
    v_func = np.vectorize(func)
    tmp = {}
    for name in Record_Switch.keys():
        tmp[name] = v_func(HSSwitch[name])
    HSSwitch = tmp
    Hour_Dark,Hour_Light=Hour_Light_and_Dark_GUI(Dark_start,Dark_length)
    Best_Model,Pdf,Cdf,EmCdf=F_Gr_Fit_GMM_GUI(Record_Switch,Mouse_Grouped,n_gauss=1)
    Median,Mean,Std=Subj_Median_Mean_Std_GUI(Record_Switch,HSSwitch)
    Hour_label = TimeUnit_to_Hours_GUI(np.hstack((Hour_Dark,Hour_Light)),3600)
    DataLen    = len(Hour_label) * len(Record_Switch.keys())
    print('\n\nGMM FIT\n\n')  
    std_Switch, GMM_Fit = std_Switch_Latency_GUI(Record_Switch, HSSwitch,
                                                 Mouse_Grouped, Dark_start=Dark_start, 
                                                 Dark_length=Dark_length)
    EXP, MAX = F_ExpGain_GUI(Short, Long, ProbeShort, Cond_SProbe, Cond_LProbe,
                             MeanRange=Mean_minmax,CVRange=Cv_minmax)
    std_Exp_Gain = Exp_Gain_Matrix_GUI(GMM_Fit, Short, Long, Mouse_Grouped, 
                                       ProbeShort, Cond_SProbe,
                                       Cond_LProbe)
    std_Exp_Gain['Value'] = std_Exp_Gain ['Value']/np.max(EXP)
    DataDict['Group Switch Latency']['Group Switch Latency'] = np.zeros(DataLen, dtype = {
        'names':('Group','Subject','Time','Mean','Median','SEM'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,'|S5',float,
                   float,float)})
    DataDict['Group Switch Latency']['Group Switch Latency']['Time'] = list(Hour_label) * len(Record_Switch.keys())
    ind = 0
    for key in Mouse_Grouped.keys():
        for name in Mouse_Grouped[key]:
            DataDict['Group Switch Latency']['Group Switch Latency']['Group'][ind:len(Hour_label)+ind]\
                = [key] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Subject'][ind:len(Hour_label)+ind]\
                = [name] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Mean'][ind:len(Hour_label)+ind]\
                = Mean[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['Median'][ind:len(Hour_label)+ind]\
                = Median[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['SEM'][ind:len(Hour_label)+ind]\
                = Std[name]
            ind += len(Hour_label)
    DataDict['Group Switch Latency']['Expected Gain'] = std_Exp_Gain
    Gr_Mean,Gr_Std=Gr_Mean_Std_GUI(Median,Mouse_Grouped)
    Group_Name = Mouse_Grouped.keys()
    dictPlot = {}
    dictPlot['Fig:Group Switch Latency'] = {}
    dictPlot['Fig:Group Switch Latency']['Boxplot'] = Gr_Mean,Hour_Light,Hour_Dark,\
                                            Group_Name
    dictPlot['Fig:Group Switch Latency']['Gaussian Fit'] = Cdf, EmCdf, Group_Name,\
                                            Mouse_Grouped, ts, tl
    dictPlot['Fig:Group Switch Latency']['Optimal Surface'] =\
        (EXP, MAX, Mean_minmax, Cv_minmax,
         std_Exp_Gain, 40, 12)
    dictPlot['Fig:Group Switch Latency']['Expected Gain'] =\
        (std_Exp_Gain, 'Expected Gain', 20, 1, 3, 1, 0.95,
        'Normalized Exp. Gain', 12, 15)
    info = {}
    info['Group Switch Latency'] = {}
    info['Group Switch Latency']['Types']  = ['Group', 'Switch Latency']
    info['Group Switch Latency']['Factor'] = [0,1,2]
    info['Expected Gain'] = {}
    info['Expected Gain']['Types']  = ['Single Subject', 'Expected Gain']
    info['Expected Gain']['Factor'] = [0,1]
    return DataDict,dictPlot,info

def Switch_Latency_TEST(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    Tend = Input[0]['DoubleSpinBox'][0]
    group_list = DataGroup.keys()
    group_list.sort()
    long_side_dict = {}
    k = 0
    for gr in group_list:
        long_side_dict[gr] = Long_Side
        k += 1
    Mouse_Name = np.hstack(DataGroup.values())
    lenName = 0
    lenGroupName = 0
    for key in DataGroup.keys():
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    Mouse_Grouped = DataGroup
    AllData = OrderedDict()
    TimeStamps_Dict = {}
    DataDict = {}
    DataDict['Group Switch Latency'] = {}
    long_side_sub = {}
    print('CREATING TIMESTAMPS DICT')
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            try:
                lock.lockForRead()
                AllData[dataName] = copy(Datas.takeDataset(dataName))
                if Datas.getTimeStamps(dataName):
                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
                else:
                    TimeStamps_Dict[dataName] = TimeStamps
            finally:
                lock.unlock()
    for gr in Mouse_Grouped.keys():
        for dataName in Mouse_Grouped[gr]:
            long_side_sub[dataName] = long_side_dict[gr]
    print('\n\nGR SWITCH LAT\n\n')          
    table,left,right,Record_Switch,HSSwitch = F_New_Gr_Switch_Latency_GUI(AllData,TimeStamps_Dict,Mouse_Name,ts=ts,tl=tl,scale=1,Tend=Tend,Long_Side=long_side_sub,type_tr=type_tr)
    for name in Record_Switch.keys():
        if Record_Switch[name].shape[0] < 10:
            message = '%s less then 10 trials...'%name
            Record_Switch.pop(name)
            HSSwitch.pop(name)
            right.pop(name)
            left.pop(name)
            table.pop(name)
            AllData.pop(name)
            for gr in Mouse_Grouped.keys():
                if name in Mouse_Grouped[gr]:
                    Mouse_Grouped[gr].remove(name)
    prev_groups = Mouse_Grouped.keys()
    for gr in prev_groups:
        if not len(Mouse_Grouped[gr]):
            s = Mouse_Grouped.pop(gr)
    func = lambda h : h.hour
    v_func = np.vectorize(func)
    tmp = {}
    for name in Record_Switch.keys():
        tmp[name] = v_func(HSSwitch[name])
    HSSwitch = tmp
    Hour_Dark,Hour_Light=Hour_Light_and_Dark_GUI(Dark_start,Dark_length)
    Best_Model,Pdf,Cdf,EmCdf=F_Gr_Fit_GMM_GUI(Record_Switch,Mouse_Grouped,n_gauss=1)
    Median,Mean,Std=Subj_Median_Mean_Std_GUI(Record_Switch,HSSwitch)
    Hour_label = TimeUnit_to_Hours_GUI(np.hstack((Hour_Dark,Hour_Light)),3600)
    DataLen    = len(Hour_label) * len(Record_Switch.keys())
    print('\n\nGMM FIT\n\n')  
    std_Switch, GMM_Fit = std_Switch_Latency_GUI(Record_Switch, HSSwitch,
                                                 Mouse_Grouped, Dark_start=Dark_start, 
                                                 Dark_length=Dark_length)
    EXP, MAX = F_ExpGain_GUI(Short, Long, ProbeShort, Cond_SProbe, Cond_LProbe,
                             MeanRange=Mean_minmax,CVRange=Cv_minmax)
    std_Exp_Gain = Exp_Gain_Matrix_GUI(GMM_Fit, Short, Long, Mouse_Grouped, 
                                       ProbeShort, Cond_SProbe,
                                       Cond_LProbe)
    std_Exp_Gain['Value'] = std_Exp_Gain ['Value']/np.max(EXP)
    DataDict['Group Switch Latency']['Group Switch Latency'] = np.zeros(DataLen, dtype = {
        'names':('Group','Subject','Time','Mean','Median','SEM'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,'|S5',float,
                   float,float)})
    DataDict['Group Switch Latency']['Group Switch Latency']['Time'] = list(Hour_label) * len(Record_Switch.keys())
    ind = 0
    for key in Mouse_Grouped.keys():
        for name in Mouse_Grouped[key]:
            DataDict['Group Switch Latency']['Group Switch Latency']['Group'][ind:len(Hour_label)+ind]\
                = [key] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Subject'][ind:len(Hour_label)+ind]\
                = [name] * len(Hour_label)
            DataDict['Group Switch Latency']['Group Switch Latency']['Mean'][ind:len(Hour_label)+ind]\
                = Mean[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['Median'][ind:len(Hour_label)+ind]\
                = Median[name]
            DataDict['Group Switch Latency']['Group Switch Latency']['SEM'][ind:len(Hour_label)+ind]\
                = Std[name]
            ind += len(Hour_label)
    DataDict['Group Switch Latency']['Expected Gain'] = std_Exp_Gain
    Gr_Mean,Gr_Std=Gr_Mean_Std_GUI(Median,Mouse_Grouped)
    Group_Name = Mouse_Grouped.keys()
    dictPlot = {}
    dictPlot['Fig:Group Switch Latency'] = {}
    dictPlot['Fig:Group Switch Latency']['Boxplot'] = Gr_Mean,Hour_Light,Hour_Dark,\
                                            Group_Name
    dictPlot['Fig:Group Switch Latency']['Gaussian Fit'] = Cdf, EmCdf, Group_Name,\
                                            Mouse_Grouped, ts, tl
    dictPlot['Fig:Group Switch Latency']['Optimal Surface'] =\
        (EXP, MAX, Mean_minmax, Cv_minmax,
         std_Exp_Gain, 40, 12)
    dictPlot['Fig:Group Switch Latency']['Expected Gain'] =\
        (std_Exp_Gain, 'Expected Gain', 20, 1, 3, 1, 0.95,
        'Normalized Exp. Gain', 12, 15)
    info = {}
    info['Group Switch Latency'] = {}
    info['Group Switch Latency']['Types']  = ['Group', 'Switch Latency']
    info['Group Switch Latency']['Factor'] = [0,1,2]
    info['Expected Gain'] = {}
    info['Expected Gain']['Types']  = ['Single Subject', 'Expected Gain']
    info['Expected Gain']['Factor'] = [0,1]
    return DataDict,dictPlot,info
