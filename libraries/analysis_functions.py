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
                                 vector_hours,bin_epi,epidur_if_binAdj,
                                 extract_epi,consecutive_bins,
                                 filter_emg,
                                 ellip_bandpass_filter,
                                 normalize_emg,
                                 compute_perc)
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
    
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1
    
    first = True
    rc = 0
    for name in list(AllData.keys()):
        Time = AllData[name].Timestamp
        
        if epochType == 'S':
            for kk in ['R','NR']:
                AllData[name].Stage[AllData[name].Stage == kk] = 'S'
                AllData[name].Stage[AllData[name].Stage == kk +'*'] = 'S'
            
        
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
        epi = bin_epi(AllData[name][index_light], epidur, Time[i0],Time[i1],epoch=epochType)
        epi_dur_light = epidur_if_binAdj(epi, epidur,binvec = range(0,12,Bin), epochDur=EpochDur)*EpochDur
        
        i0 = index_dark[0]
        i1 = index_dark[-1]
        epi = bin_epi(AllData[name][index_dark], epidur, Time[i0],Time[i1],epoch=epochType)
        epi_dur_dark = epidur_if_binAdj(epi, epidur,binvec = range(0,12,Bin), epochDur=EpochDur)*EpochDur
        
        
        time_course = (np.hstack((epi_dur_light,epi_dur_dark))*100)/(3600*Bin)
        
        if first:
            types_hours = np.array(range(0,24,Bin),dtype=np.str_)
            types = np.hstack((['Group','Subject'],types_hours))
            
            df_time_course = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_hours.shape[0]})
            
          
            first = False
        
        cc = 0
        for col in types_hours:
            df_time_course[col][rc] = time_course[cc]
            cc += 1
        
        df_time_course['Subject'][rc] = name
        df_time_course['Group'][rc] = key
       
        rc += 1
        
    DataDict['Sleep Time Course'] = {}
    DataDict['Sleep Time Course'][epochType] = pd.DataFrame(df_time_course)
    
    title = 'Time spent in: %s'%epochType
    x_label = 'Time [Zt]'
    y_label = '% of total time'
    dictPlot['Fig:Sleep Time Course'] = {}
    dictPlot['Fig:Sleep Time Course']['Single Subject'] = (pd.DataFrame(df_time_course),
                                                            title,x_label,
                                                            y_label,
                                                            tick_Num,
                                                            dark_start,
                                                            stat_index,
                                                            total_or_mean)
                                                      
    info['Types']  = ['Single Subject EEG','Total time in %']
    info['Factor'] = [0]
    
    datainfo = {epochType: info }
   
    
    return DataDict,dictPlot, datainfo
            
    
    
    
    return DataDict,dictPlot, datainfo
def delta_rebound(*myInput):
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

    bins = Input[0]['Combo'][0]
    col_freq = Input[0]['Combo'][1]
    epoch = Input[0]['Combo'][2]
    
    AllData  = {}
    for group in list(DataGroup.keys()):
        for key in DataGroup[group]:
            try:
                lock.lockForRead()
                AllData[key] = copy(Datas.takeDataset(key))
            finally:
                lock.unlock()
    
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1
    

    first = True
    rc = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            if Input[0]['PhaseSel'][0][name][0][5]:
                condition = 'Baseline'
                col_input = 0
            elif Input[0]['PhaseSel'][0][name][1][5]:
                condition = 'Sleep Deprivation'
                col_input = 1
            elif Input[0]['PhaseSel'][0][name][2][5]:
                condition = 'Rebound'
                col_input = 2
                
            start = Input[0]['PhaseSel'][0][name][col_input][1]
            stop = Input[0]['PhaseSel'][0][name][col_input][2]
            
            norm_start = Input[0]['PhaseSel'][0][name][col_input][3]
            norm_stop = Input[0]['PhaseSel'][0][name][col_input][4]
            
            idx = np.where(AllData[name].Timestamp >= start)[0]
            AllData[name] = AllData[name][idx]
                
            idx = np.where(AllData[name].Timestamp <= stop)[0]
            AllData[name] = AllData[name][idx]
                
            if Input[0]['PhaseSel'][0][name][col_input][6]:
                idx_norm = None 
            else:
                idx_norm = (AllData[name].Timestamp >= norm_start) * (AllData[name].Timestamp <= norm_stop)
                
                
            array_episodes = extract_epi(AllData[name], epoch = epoch, 
                                     merge_if=1,
                                     min_epi_len=2)
            
            index = []
            for start,end in array_episodes:
                index = np.hstack((index,range(start,end)))
                
            index = np.array(index,dtype=int)
            mask = np.ones(AllData[name].Stage.shape[0], dtype=bool)
            mask[index] = False
            
            non_index = np.arange(AllData[name].Stage.shape[0])[mask]
            
            Power = copy(AllData[name].PowerSp)
            Power[non_index,:] = np.nan
            Power[np.where(AllData[name].Stage!=epoch)[0],:] = np.nan
            
            
            binvect = consecutive_bins(AllData[name].Timestamp,bins=bins)
            all_bins = np.unique(binvect)
            
            if idx_norm is None:
                norm_factor = 1
            else:
                norm_factor = np.nanmean(Power[idx_norm,col_freq])
                
            idx = 0
            res = np.zeros(all_bins.shape[0])
            for k in all_bins:
                idx_sel = np.where(binvect==k)[0]
                if idx_sel.shape[0] < 2:
                    continue
                res[idx] = np.nanmean(Power[idx_sel,col_freq])/norm_factor
                idx += 1
            
            if first:
                types_hours = np.array(range(0,24,int(bins/3600)),dtype=np.str_)
                types = np.hstack((['Group','Subject','Norm factor'],types_hours))
                
                df_power = np.zeros((count_sub,),dtype={'names':types,
                                      'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_hours.shape[0]+(float,)})
                
              
                first = False
            
            cc = 0
            for col in types_hours:
                df_power[col][rc] = res[cc]
                cc += 1
            
            df_power['Subject'][rc] = name
            df_power['Group'][rc] = key
            df_power['Norm factor'][rc] = norm_factor
           
            rc += 1
        

    DataDict['Delta-Theta'] = {}
    DataDict['Delta-Theta'][epoch] = pd.DataFrame(df_power)
    
    
    if col_freq == 0:
        title = ' Delta Power during ' + condition
    elif col_freq == 1:
        title = 'Theta Power during ' + condition
        
    
    x_label = 'Time'
    y_label = 'Power'
    dictPlot['Fig:EEG Power'] = {}
    dictPlot['Fig:EEG Power']['Single Subject'] = (pd.DataFrame(df_power),
                                                            title,x_label,
                                                            y_label,
                                                            None,
                                                            None,
                                                            None,
                                                            None)
                                                      
    info['Types']  = ['Single Subject EEG','Total time in %']
    info['Factor'] = [0]
    
    datainfo = {epoch: info }
   
    
    return DataDict,dictPlot, datainfo  
def Sleep_cycles(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    DataGroup  = myInput[2]
    lock       = myInput[4]
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    
    AllData  = {}
    for group in list(DataGroup.keys()):
        for key in DataGroup[group]:
            try:
                lock.lockForRead()
                AllData[key] = copy(Datas.takeDataset(key))
            finally:
                lock.unlock()
    
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1


    maxTime = myInput[1][0]['DoubleSpinBox'][0]
    steps = myInput[1][0]['Combo'][0]

    bins = range(0,int(maxTime)+int(steps),int(steps))
    first = True
    rc = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            array_episodes = extract_epi(AllData[name], epoch = 'R', 
                                     merge_if=2,
                                     min_epi_len=2)
           
            
            cycle_dur_x_sbj = 0
            for ep in range(array_episodes.shape[0]-1):
                start = array_episodes['Start'][ep]
                stop = array_episodes['Start'][ep+1]
                res = (stop-start)*4
                cycle_dur_x_sbj = np.hstack((cycle_dur_x_sbj,res))
            
            
            res_min = cycle_dur_x_sbj/60.
            n_res = np.histogram(res_min, bins=bins,range=(0, int(maxTime)))
            
            if first:
                types_hours = np.array(bins[:-1],dtype=np.str_)
                types = np.hstack((['Group','Subject'],types_hours))
                
                df_cycles = np.zeros((count_sub,),dtype={'names':types,
                                      'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_hours.shape[0]})
        
                first = False
            
            cc = 0
            for col in types_hours:
                df_cycles[col][rc] = n_res[0][cc]
                cc += 1
            
            df_cycles['Subject'][rc] = name
            df_cycles['Group'][rc] = key
           
            rc += 1
            
    DataDict['Cycles durations'] = {}
    DataDict['Cycles durations']['Cycles'] = pd.DataFrame(df_cycles)
    

    title = 'Cycles durations'   
    x_label = 'Duration [minutes]'
    y_label = 'Occurences [#]'
    dictPlot['Fig:Cycles durations raw'] = {}
    dictPlot['Fig:Cycles durations raw']['Single Subject'] = (pd.DataFrame(df_cycles),
                                                            title,x_label,
                                                            y_label,
                                                            n_res[1],
                                                            None,
                                                            None,
                                                            None)
                                                      
    info['Types']  = ['Cycles','Occurences in #']
    info['Factor'] = [0]
    
    datainfo = {'Cycles': info }
    
    return DataDict, dictPlot, datainfo
def emg_normalized(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    DataGroup  = myInput[2]
    lock       = myInput[4]
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    
    AllData  = {}
    for group in list(DataGroup.keys()):
        for key in DataGroup[group]:
            try:
                lock.lockForRead()
                AllData[key] = copy(Datas.takeDataset(key))
            finally:
                lock.unlock()
    
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1


    percentile = myInput[1][0]['Combo'][0]
    
    stages = ['W','R','NR']
    first = True
    rc = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            
            emg = AllData[name].emg
            std = 5
            ampl = np.nanstd(emg)*std
            
            emg_filterd = filter_emg(emg,ampl)
            emg_filterd_2 = ellip_bandpass_filter(emg_filterd, 0.1, 240, 500, order=3, rp=0.1, rs=40)
        
            scored = AllData[name].Stage

            raEMG,av,norm_h, norm_l = normalize_emg(emg_filterd_2)
            percent = compute_perc(raEMG,scored,stages,percentile)
            
            
            if first:
                types_hours = np.array(percentile,dtype=np.str_)
                types = np.hstack((['Group','Subject','Norm high','Norm low'],types_hours))
                
                df_emg_norm = np.zeros((count_sub,),dtype={'names':types,
                                      'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_hours.shape[0]+(float,)+(float,)})
        
                first = False
            
            cc = 0
            for col in types_hours:
                df_emg_norm[col][rc] = percent[cc]
                cc += 1
            
            df_emg_norm['Subject'][rc] = name
            df_emg_norm['Group'][rc] = key
            df_emg_norm['Norm high'][rc] = norm_h
            df_emg_norm['Norm low'][rc] = norm_l
           
            rc += 1
            
    DataDict['EMG norm'] = {}
    DataDict['EMG norm']['EMGnorm'] = pd.DataFrame(df_emg_norm)
    

    title = 'emg normalized'   
    x_label = 'Percentiles'
    y_label = 'Amplitude [A.U.]'
    dictPlot['Fig:emg normalized'] = {}
    dictPlot['Fig:emg normalized']['Single Subject'] = (pd.DataFrame(df_emg_norm),
                                                            title,x_label,
                                                            y_label,
                                                            percentile,
                                                            None,
                                                            None,
                                                            None)
                                                      
    info['Types']  = ['Emg','nomralization in #']
    info['Factor'] = [0]
    
    datainfo = {'Emg': info }
            
            
    return DataDict, dictPlot, datainfo 

    
    
    
    
    
    
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
