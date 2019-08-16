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
import datetime as dt
from copy import copy
from auxiliary_functions import (powerDensity_function,
                                 vector_hours,bin_epi,epidur_if_binAdj,
                                 extract_epi,consecutive_bins,
                                 filter_emg,
                                 ellip_bandpass_filter,
                                 normalize_emg,
                                 compute_perc,
                                 extract_start,
                                 AITComputation_GUI,
                                 TimeUnit_to_Hours_GUI,
                                 Time_Details_GUI,
                                 F_OnSet_GUI,
                                 F_OffSet_GUI,
                                 F_Probes_x_TimeInterval_GUI,
                                 F_PeakProbes_GUI)

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
    DataGroup  = myInput[5]
#    lock       = myInput[4]
    
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]['Sleep']:
            lenName = max(lenName,len(name))
    
    
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]['EMG']:
            count_sub += 1


    percentile = np.array(myInput[1][0]['LineEdit'][0].split(','),dtype = int)
    
    stages = ['W','R','NR']
    first = True
    rc = 0
    for key in list(DataGroup.keys()):
        emg_data = DataGroup[key]['EMG']
        sleep_data = DataGroup[key]['Sleep']
        for kk in range(len(emg_data)):
            
            emg =  Datas[emg_data[kk]].Dataset['emg']
            std = 5
            ampl = np.nanstd(emg)*std
            
            emg_filterd = filter_emg(emg,ampl)
            emg_filterd_2 = ellip_bandpass_filter(emg_filterd, 0.1, 240, 500, order=3, rp=0.1, rs=40)
        
            sleep = Datas[sleep_data[kk]].Dataset

            raEMG,av,norm_h, norm_l = normalize_emg(emg_filterd_2)
            percent = compute_perc(raEMG,sleep,stages,percentile)
            
            
            if first:
                types_hours = np.array(percentile,dtype=np.str_)
                types = np.hstack((['Group','Subject emg','Subject scored','Norm high','Norm low'],types_hours))
                
                df_emg_norm_wake = np.zeros((count_sub,),dtype={'names':types,
                                      'formats':('U%d'%lenGroupName,'U%d'%lenName,'U%d'%lenName)+(float,)*types_hours.shape[0]+(float,)+(float,)})
                df_emg_norm_rem = np.zeros((count_sub,),dtype={'names':types,
                                      'formats':('U%d'%lenGroupName,'U%d'%lenName,'U%d'%lenName)+(float,)*types_hours.shape[0]+(float,)+(float,)})
                df_emg_norm_nrem = np.zeros((count_sub,),dtype={'names':types,
                                      'formats':('U%d'%lenGroupName,'U%d'%lenName,'U%d'%lenName)+(float,)*types_hours.shape[0]+(float,)+(float,)})
    
                first = False
            
            cc = 0
            for col in types_hours:
                df_emg_norm_wake[col][rc] = percent[0,cc]
                df_emg_norm_rem[col][rc] = percent[1,cc]
                df_emg_norm_nrem[col][rc] = percent[2,cc]
                cc += 1
            
            df_emg_norm_wake['Subject emg'][rc] = emg_data[kk]
            df_emg_norm_wake['Subject scored'][rc] = sleep_data[kk]
            df_emg_norm_wake['Group'][rc] = key
            df_emg_norm_wake['Norm high'][rc] = norm_h
            df_emg_norm_wake['Norm low'][rc] = norm_l
            
            df_emg_norm_rem['Subject emg'][rc] = emg_data[kk]
            df_emg_norm_rem['Subject scored'][rc] = sleep_data[kk]
            df_emg_norm_rem['Group'][rc] = key
            df_emg_norm_rem['Norm high'][rc] = norm_h
            df_emg_norm_rem['Norm low'][rc] = norm_l
            
            df_emg_norm_nrem['Subject emg'][rc] = emg_data[kk]
            df_emg_norm_nrem['Subject scored'][rc] = sleep_data[kk]
            df_emg_norm_nrem['Group'][rc] = key
            df_emg_norm_nrem['Norm high'][rc] = norm_h
            df_emg_norm_nrem['Norm low'][rc] = norm_l
           
            rc += 1
            
    DataDict['EMG norm'] = {}
    DataDict['EMG norm']['WAKE'] = pd.DataFrame(df_emg_norm_wake)
    DataDict['EMG norm']['REM'] = pd.DataFrame(df_emg_norm_rem)
    DataDict['EMG norm']['NREM'] = pd.DataFrame(df_emg_norm_nrem)
    

    title = 'emg normalized'   
    x_label = 'Percentiles'
    y_label = 'Amplitude [A.U.]'
    dictPlot['Fig:emg normalized'] = {}
    dictPlot['Fig:emg normalized']['Single Subject'] = (pd.DataFrame(df_emg_norm_wake),
                                                        pd.DataFrame(df_emg_norm_rem),
                                                        pd.DataFrame(df_emg_norm_nrem),
                                                        title,
                                                        x_label,
                                                        y_label,
                                                        percentile,
                                                        None)
                                                      
    info['Types']  = ['Emg','normalization in #']
    info['Factor'] = [0,1,2]
    
    datainfo = {'WAKE': info,'REM': info,
                'NREM': info}
            
            
    return DataDict, dictPlot, datainfo 

def Attentional_analysis(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
#    lock       = myInput[4]
    
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))

    types = Input[0]['Combo'][0][0]
    bins = Input[0]['Combo'][1]
    dark = Input[0]['Combo'][2]
    dur_dark = Input[0]['Combo'][3]
    
    if types == 1: #reaction time
        VAR = 'Reaction Time'           
    elif types == 2: #anticipation
        VAR = 'Time anticipated'        
    elif types == 3: #food
        VAR = 'Eaten food'  
    elif types == 4: #error
        VAR = 'Error Type' 
      
    nTrials = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            time = Datas[name].Dataset['Time']
            action = Datas[name].Dataset['Action']
            
            start = np.where(action==TimeStamps['ACT_START_TEST'])[0]
            nTrials += start.shape[0]-1

    types_res = ['Group','Subject','Trial type','Hour',VAR]
    res = np.zeros((nTrials,),dtype={'names':types_res,
                           'formats':('U%d'%lenGroupName,'U%d'%lenName,'U%d'%lenName)+(int,)+(float,)})
            
    tn = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            time = Datas[name].Dataset['Time']
            action = Datas[name].Dataset['Action']
            
            start = np.where(action==TimeStamps['ACT_START_TEST'])[0]
            
            date = extract_start(time,action,TimeStamps)
       
            
            for tt in range(start.shape[0]-1):
                tmp_time = time[start[tt]:start[tt+1]]
                tmp_action = action[start[tt]:start[tt+1]]
                
                
                hour = date + dt.timedelta(seconds = tmp_time[0])
                    
                if np.where(tmp_action == 60)[0]:
                    trial = 'No Cue'
                elif np.where(tmp_action == 61)[0]:
                    trial = 'Cong'
                elif np.where(tmp_action == 62)[0]:
                    trial = 'Incon'
                else:
                    trial = 'Training'
                    
                
                light_r = np.where(tmp_action == TimeStamps['Right Light On'])[0]
                light_l = np.where(tmp_action == TimeStamps['Left Light On'])[0]

                if light_r.shape[0]:
                    pellet = tmp_time[tmp_action == TimeStamps['Give Pellet Right']]
                    if pellet.shape[0]:
                        food = 0.025
                        nose = np.where(tmp_action == TimeStamps['Right NP In'])[0]
                        t_n = tmp_time[nose]
                        reaction = t_n[t_n >= tmp_time[light_r]][0] - tmp_time[light_r]
                        before = np.sum(t_n < tmp_time[light_r])
                        correct = 1
                    else:
                        food = 0
                        tR = np.where(tmp_action == TimeStamps['ACT_TIMEOUT_REACHED'])[0]
                        if tR:
                            reaction = np.nan
                            before = np.nan
                            correct = 2
                        else:
                            opposite = np.where(tmp_action == TimeStamps['Left NP In'])[0]   
                            wrong = tmp_time[opposite] >= tmp_time[light_r]
                            if np.sum(wrong):
                                correct = 3
                            else:
                                center = np.where(tmp_action == TimeStamps['Center NP In'])[0]
                                wrong = tmp_time[center] >= tmp_time[light_r]
                                if np.sum(wrong):
                                    correct = 4
                        
                elif light_l.shape[0]:
                    pellet = tmp_time[tmp_action == TimeStamps['Give Pellet Left']]
                    if pellet.shape[0]:
                        food = 0.025
                        nose = np.where(tmp_action == TimeStamps['Left NP In'])[0]
                        t_n = tmp_time[nose]
                        reaction = t_n[t_n >= tmp_time[light_l]][0] - tmp_time[light_l]
                        before = np.sum(t_n < tmp_time[light_l])
                        correct = 1
                    else:
                        food = 0
                        tR = np.where(tmp_action == TimeStamps['ACT_TIMEOUT_REACHED'])[0]
                        if tR:
                            reaction = np.nan
                            before = np.nan
                            correct = 2
                        else:
                            opposite = np.where(tmp_action == TimeStamps['Right NP In'])[0]   
                            wrong = tmp_time[opposite] >= tmp_time[light_l]
                            if np.sum(wrong):
                                correct = 3
                            else:
                                center = np.where(tmp_action == TimeStamps['Center NP In'])[0]
                                wrong = tmp_time[center] >= tmp_time[light_l]
                                if np.sum(wrong):
                                    correct = 4

                res['Group'][tn] = key
                res['Subject'][tn] = name
                res['Trial type'][tn] = trial
                res['Hour'][tn] = hour.hour
                
                if types == 1: #reaction time
                    res['Reaction Time'][tn] = reaction 
                    y_label = 'Time [seconds]'
                elif types == 2: #anticipation
                    res['Time anticipated'][tn] = before 
                    y_label  = 'Occurences [#]'
                elif types == 3: #food
                    res['Eaten food'][tn] = food 
                    y_label = 'Eaten food [mg]'
                elif types == 4: #error
                    res['Error Type'][tn] = correct 
                    y_label = 'Rate [%]'
                
                tn +=1
          
    
    DataDict['Attentional'] = {}
    DataDict['Attentional'][VAR] = pd.DataFrame(res)
    

    title = 'Attentional analysis'   
    x_label = 'Time'

    dictPlot['Fig:Attentional analysis'] = {}
    dictPlot['Fig:Attentional analysis']['Single Subject'] = (pd.DataFrame(res),
                                                              title,
                                                              x_label,
                                                              y_label,
                                                              bins,
                                                              VAR,
                                                              dark,
                                                              dur_dark)
                                                      
    info['Types']  = ['Attentional','selected']
    info['Factor'] = [0]
    
    datainfo = {VAR: info }
    
    return DataDict, dictPlot, datainfo
def Group_Error_Rate(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
#    lock       = myInput[4]
    
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    
    Dark_start = Input[0]['Combo'][0]
    Dark_length = Input[0]['Combo'][1]
    StatIndex = Input[0]['Combo'][2]
    TimeInterval = Input[0]['Combo'][3]
#    Dataset_Dict = {}
#    TimeStamps_Dict = {}
    
    types = Input[0]['Combo'][4]
    if types == 0:
        types = 'Single subject'
    elif types == 1:
        types = 'Group'


    nTrials = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            time = Datas[name].Dataset['Time']
            action = Datas[name].Dataset['Action']
            
            start = np.where(action==TimeStamps['ACT_START_TEST'])[0]
            nTrials += start.shape[0]-1

    types_res = ['Group','Subject','Time','Correct']
    res = np.zeros((nTrials,),dtype={'names':types_res,
                           'formats':('U%d'%lenGroupName,'U%d'%lenName,'U30')+(int,)})

    nt = 0
    for group in list(DataGroup.keys()):
        for dataName in DataGroup[group]:
            time = Datas[dataName].Dataset['Time']
            action = Datas[dataName].Dataset['Action']
            
            start = np.where(action==TimeStamps['ACT_START_TEST'])[0]
            
            date = extract_start(time,action,TimeStamps)
            
            for tt in range(start.shape[0]-1):
                tmp_time = time[start[tt]:start[tt+1]]
                tmp_action = action[start[tt]:start[tt+1]]
                
                hour = date + dt.timedelta(seconds = tmp_time[0])
                
                idx_left = tmp_action == TimeStamps['Give Pellet Left']
                idx_right = tmp_action == TimeStamps['Give Pellet Right']
                
                tot = np.sum(idx_left) + np.sum(idx_right)
                
                res['Group'][nt] = group
                res['Subject'][nt] = dataName
                res['Time'][nt] = hour.strftime("%Y/%m/%d, %H:%M:%S")
                
                if tot > 0:
                    res['Correct'][nt] = 1
                else:
                    res['Correct'][nt] = 0
                    
                nt +=1
    
    x_label = 'Time'
    y_label = 'Error Rate [%]'

    DataDict = {'Group Error Rate' : {}}
    DataDict['Group Error Rate']['Error Rate'] = pd.DataFrame(res)
    dictPlot = {}
    dictPlot['Fig: Group Error Rate'] = {}
    dictPlot['Fig: Group Error Rate']['Single Subject'] = (pd.DataFrame(res),
                                                            types,
                                                            x_label,
                                                            y_label,
                                                            Dark_start,
                                                            Dark_length,
                                                            StatIndex,
                                                            TimeInterval)    
    info = {}
    info['Error Rate'] = {'Error Rate' : {}}
    info['Error Rate']['Types'] =\
        ['Group', 'Error Rate']
    info['Error Rate']['Factor'] = [0,1]
    
    return DataDict, dictPlot, info

def AIT(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
#    lock       = myInput[4]
    
    
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
            
            
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1
    
    """
        Ait computation from std input dlg
    """
    
    TimeInterval  = Input[0]['Combo'][0]
    Dark_start    = Input[0]['Combo'][1]
    Dark_length   = Input[0]['Combo'][2]
#    inputForPlots = {}
#    dataDict      = {}
   
    
    first = True
    rc = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            data = Datas[name]
            OrdMedian,OrdMean,OrdStd,perc25,perc75,\
            Hour_Dark,Hour_Light,HourStart_AIT = AITComputation_GUI(data.Dataset, 
                                                                    Dark_start,
                                                                    TimeStamps, 
                                                                    Dark_length,
                                                                    TimeInterval=TimeInterval)
            
            
            Hours=np.hstack((Hour_Dark,Hour_Light))
            dark_bin = (((Dark_start-12) * 3600.)%(3600.*24))/TimeInterval
            Hlabel = TimeUnit_to_Hours_GUI(Hours+dark_bin,TimeInterval)
            LenDark = Hour_Dark.shape[0]
            
            if first:
                
                types_lab = np.array(Hlabel,dtype=np.str_)
                types = np.hstack((['Group','Subject'],types_lab))
                
                df_mean = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_lab.shape[0]})
    
                df_median = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_lab.shape[0]})
                
                df_Standard_Error = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_lab.shape[0]})
                
                df_Perc_25 = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_lab.shape[0]})
                
                df_Perc_75 = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_lab.shape[0]})
                
                first = False
                
            
            cc = 0
            for col in types_lab:
                df_mean[col][rc] = OrdMean[cc]
                df_median[col][rc] = OrdMedian[cc]
                df_Standard_Error[col][rc] = OrdStd[cc]
                df_Perc_25[col][rc] = perc25[cc]
                df_Perc_75[col][rc] = perc75[cc]
                cc += 1
                
            
            df_mean['Subject'][rc] = name
            df_mean['Group'][rc] = key
            df_median['Subject'][rc] = name
            df_median['Group'][rc] = key
            df_Standard_Error['Subject'][rc] = name
            df_Standard_Error['Group'][rc] = key
            df_Perc_25['Subject'][rc] = name
            df_Perc_25['Group'][rc] = key
            df_Perc_75['Subject'][rc] = name
            df_Perc_75['Group'][rc] = key
            rc += 1
            
    
    
    DataDict['AIT MEAN'] = pd.DataFrame(df_mean)
    DataDict['AIT MEDIAN'] = pd.DataFrame(df_median)
    DataDict['AIT STD ERROR'] = pd.DataFrame(df_Standard_Error)
    DataDict['AIT 25 PERC'] = pd.DataFrame(df_Perc_25)
    DataDict['AIT 75 PERC'] = pd.DataFrame(df_Perc_75)

                
                
   

    inputForPlots = {}
    inputForPlots['Fig_AIT'] = (DataDict,
                                Hlabel,
                                'b', 'r', 
                                LenDark, 0.3,
                                'Actual Inter Trial',
                                'AIT Duration (min)')

    
    info = {}
    info['AIT'] = {}
    info['AIT']['Types']  = ['AIT', 'Single Subject']
    info['AIT']['Factor'] = [0,5]
    
    DD = {}
    DD['AIT'] = {}
    DD['AIT']['MEAN'] = DataDict['AIT MEAN']
    DD['AIT']['MEDIAN'] = DataDict['AIT MEDIAN']
    DD['AIT']['STDERR'] = DataDict['AIT STD ERROR']
    DD['AIT']['25PERC'] = DataDict['AIT 25 PERC']
    DD['AIT']['75PERC'] = DataDict['AIT 75 PERC']
    
    return DD, inputForPlots, info
    
    return DataDict, dictPlot, info
def peak_procedure(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]

    if Input[0]['Combo'][0] == 'Probe Left':
        HopperSide = 'l'
    elif Input[0]['Combo'][0] == 'Probe Right':
        HopperSide = 'r'   
    if Input[0]['Combo'][1] == 'Left':
        LocName  = 'left hopper'
        loc_for_Pk = 'l'
    else:
        LocName  = 'right hopper'
        loc_for_Pk = 'r'

    t_first = Input[0]['TimeSpinBox'][0][0]*3600 +\
              Input[0]['TimeSpinBox'][0][1]*60
    t_last  = Input[0]['TimeSpinBox'][1][0]*3600 +\
              Input[0]['TimeSpinBox'][1][1]*60
    tend    = Input[0]['DoubleSpinBox'][1]
    centiSec = np.arange(0,tend,0.01)
    
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
            
            
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1
            
    first = True
    rc = 0
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            data = Datas[name].Dataset
            
            Start_exp,Start_Time,End_Time = Time_Details_GUI(data,TimeStamps)
            
            if Input[0]['Combo'][0] == 'All':
                TrialOnset = np.where(data['Action']==TimeStamps['ACT_START_TEST'])[0]
                TrialOffset = np.where(data['Action']==TimeStamps['End Intertrial Interval'])[0]
                TrialOnset = F_OnSet_GUI(TrialOffset,TrialOnset)
                TrialOffset = F_OffSet_GUI(TrialOnset,TrialOffset)
                if len(TrialOnset)>len(TrialOffset):
                    TrialOnset=TrialOnset[:-1]
                index = np.where((data['Time'][TrialOnset] + Start_exp)%24 <= t_last)[0] 
                index_2 = np.where((data['Time'][TrialOnset][index] + Start_exp)%24 >= t_first)[0]
                TrialOnset = TrialOnset[index][index_2]
                TrialOffset = TrialOffset[index][index_2]
                Pks = TrialOnset,TrialOffset
            
            else:
                Pks = F_Probes_x_TimeInterval_GUI(data, TimeStamps, Start_exp,
                                             End_Time, HopperSide, tend = tend,
                                          Floor=True,  t_first = t_first, 
                                          t_last = t_last)
  
            
            Pk = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,loc_for_Pk)
            
            if first:
                types_lab = np.array(centiSec,dtype=np.str_)
                types = np.hstack((['Group','Subject'],types_lab))
                
                res = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':('U%d'%lenGroupName,'U%d'%lenName,)+(float,)*types_lab.shape[0]})
    
                first = False
                
            cc = 0
            for col in types_lab:
                res[col][rc] = Pk[1][cc]
                cc += 1
                
            
            res['Subject'][rc] = name
            res['Group'][rc] = key
            rc += 1
    
        

    DataDict = {}
    DataDict['Single Subject Peak'] = {}
    DataDict['Single Subject Peak']['Peak_%s'%LocName] = pd.DataFrame(res)
    
    dictPlot = {}
    dictPlot['Fig: Peak Procedure'] = {}
    dictPlot['Fig: Peak Procedure']['all Subject'] = (pd.DataFrame(res),
                                                      LocName,
                                                      centiSec,
                                                      'Time [s]',
                                                      'Normalized Response Rate' )  
    
    info = {}
    info['Peak %s'%LocName] = {}
    info['Peak %s'%LocName]['Types']  = ['Peak Procedure', 'Single Subject']
    info['Peak %s'%LocName]['Factor'] = [0,2]
    
    return DataDict, dictPlot, info
def raster_plot(*myInput):
    DataDict, dictPlot, info = {},{},{}
    
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]    
    
    if Input[0]['Combo'][0] == 'Probe Left':
        HopperSide = 'l'
    elif Input[0]['Combo'][0] == 'Probe Right':
        HopperSide = 'r'
    
    if Input[0]['Combo'][1] == 'Left':
        loc_for_Pk = 'l'
        LocName  = 'Left'
    elif Input[0]['Combo'][1] == 'Right':
        LocName  = 'Right'
        loc_for_Pk = 'r'
    else:
        LocName = 'Both'
        
    t_first = Input[0]['TimeSpinBox'][0][0]*3600 +\
              Input[0]['TimeSpinBox'][0][1]*60
    t_last  = Input[0]['TimeSpinBox'][1][0]*3600 +\
              Input[0]['TimeSpinBox'][1][1]*60
    tend    = Input[0]['DoubleSpinBox'][0]
    if Input[0]['Combo'][1] == 'Both':
        printBoth = True
        loc_for_Pk = 'l'
        loc_for_Pk1 = 'r'
    else:
        printBoth = False
    
    
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
            
            
    count_sub = 0        
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            count_sub += 1

    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            data = Datas[name].Dataset
            
            Start_exp,Start_Time,End_Time = Time_Details_GUI(data,TimeStamps)
    
            if Input[0]['Combo'][0] == 'All':
                TrialOnset = np.where(data['Action']==TimeStamps['Center Light On'])[0]
                TrialOffset = np.where(data['Action']==TimeStamps['End Intertrial Interval'])[0]
                TrialOnset = F_OnSet_GUI(TrialOffset,TrialOnset)
                TrialOffset = F_OffSet_GUI(TrialOnset,TrialOffset)
                if len(TrialOnset)>len(TrialOffset):
                    TrialOnset=TrialOnset[:-1]
                index = np.where((data['Time'][TrialOnset] + Start_exp)%24 <= t_last)[0] 
                index_2 = np.where((data['Time'][TrialOnset][index] + Start_exp)%24 >= t_first)[0]
                TrialOnset = TrialOnset[index][index_2]
                TrialOffset = TrialOffset[index][index_2]
                Pks = TrialOnset,TrialOffset
                Pk = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,loc_for_Pk)
           
                if printBoth:
                    Pk1 = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,loc_for_Pk1)
                
            
              
            else:
                Pks_0,Pks_1,indTrOn,trNum = F_Probes_x_TimeInterval_GUI(data, 
                                              TimeStamps, Start_exp,
                                              End_Time, HopperSide, tend = tend,
                                              Floor=True,  t_first = t_first, 
                                              t_last = t_last,
                                              return_IndProbe=True)
                
                Pks = (Pks_0,Pks_1)
                Pk = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,
                                      loc_for_Pk,trial_num=trNum,trial_ind=indTrOn)
                if printBoth:
                    Pk1 = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,
                                           loc_for_Pk1,trial_num=trNum,
                                           trial_ind=indTrOn)
            
            if Input[0]['Combo'][1] == 'Both':
                DataDict[name] = {}
                DataDict[name][loc_for_Pk] = pd.DataFrame(Pk[0])
                DataDict[name][loc_for_Pk1] = pd.DataFrame(Pk1[0])
                
                dictPlot[name] = {}
                dictPlot[name][loc_for_Pk] = Pk[0]
                dictPlot[name][loc_for_Pk1] = Pk1[0]
                
            else:
                DataDict[name] = {}
                DataDict[name][loc_for_Pk] = pd.DataFrame(Pk[0])
                
                dictPlot[name] = {}
                dictPlot[name][loc_for_Pk] = Pk[0]


    info['Raster'] = {}
    info['Raster']['Types']  = ['Raster', LocName]
    info['Raster']['Factor'] = [0,5]
                
    return DataDict, dictPlot, info





def LDA(*myInput):
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