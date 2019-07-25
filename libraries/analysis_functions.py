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



def Group_Error_Rate(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]

    return DataDict, dictPlot, info

def error_rate():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info


def LDA():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def Switch_Latency():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def delta_rebound():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def Actograms():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def AIT():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def raster_plot():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def peak_procedure():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def Attentional_analysis():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def sleep_fragmentation():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def Sleep_cycles():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info

def emg_normalized():
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    return DataDict, dictPlot, info


    

