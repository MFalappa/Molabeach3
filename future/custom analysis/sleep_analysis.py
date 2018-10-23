# -*- coding: utf-8 -*-
""""
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

Copyright (C) 2017 FONDAZIONE ISTITUTO ITALIANO DI TECNOLOGIA
                   E. Balzani, M. Falappa - All rights reserved

@author: edoardo.balzani87@gmail.com; mfalappa@outlook.it

                                Publication:
         An approach to monitoring home-cage behavior in mice that 
                          facilitates data sharing
                          
        DOI: 10.1038/nprot.2018.031      

*******************************************************************************
THIS SCRIP ISN'T DESCRIBED IN THE PAPER. IT WAS WRITTEN FOR OUR CUSTOM ANALYSIS
WE WILL INTRODUCE IN THE NEXT RELEASE OF PHENOPY AFTER A HARD DEBUG AND 
GENERALIZATION

*******************************************************************************
SOME OF FUNCTIONS IN THIS SCRIPT ARE ALREADY IN PHENOPY, THE OTHER WILL BE 
INCLUDED IN THE NEXT RELEASE

THESE FUNCTIONS ARE ALREADY DEBUGGED
*******************************************************************************
"""

import sys
sys.path.append('/Users/Matte/Python_script/Phenopy/libraries')

import datetime as dt
from Modify_Dataset_GUI import *
from copy import copy
import matplotlib.pylab as plt

def return_vector_hours(ts):
    return ts.hour

v_return_vector_hours = np.vectorize(return_vector_hours)

def norm_fact_calc(data_eeg, norm_hrs, array_epi,skip_bef_aft = 1, col=0, epoch ='NR',consecutive=False):
    if consecutive:
        hours = consecutive_bins(data_eeg.Timestamp,bins = 3600)
    else:
        hours = v_return_vector_hours(data_eeg.Timestamp)
    index = []
    for h in norm_hrs:
        index = np.hstack((index,np.where(hours==h)[0]))
    index = np.sort(np.array(index,dtype=int))
    mask = np.ones(data_eeg.Stage.shape[0],dtype=bool)
    mask[index] = 0
    power_vect = copy(data_eeg.PowerSp[:,col])
    power_vect[np.where(mask)] = np.nan
    power_vect[np.where(data_eeg.Stage != epoch)[0]] = np.nan
    for start,end in array_epi:
        if start >= end-2*skip_bef_aft:
            continue
        power_vect[start:start+skip_bef_aft] = np.nan
        power_vect[end-skip_bef_aft:end] = np.nan
        index = np.array(np.where(data_eeg.Stage[start+skip_bef_aft:end-skip_bef_aft]!=epoch)[0],dtype=int)
        power_vect[start+skip_bef_aft:end-skip_bef_aft][index] = np.nan
    print np.nanmean(power_vect)
    return np.nanmedian(power_vect),power_vect
    
def consecutive_bins(ts,bins,startfromzero=True):
    binvect = np.zeros(len(ts))
    if not startfromzero:
        day0 = ts[0] - dt.timedelta(0,ts[0].hour*3600 + ts[0].minute * 60 +ts[0].second)
    #    print day0
        k=0
        for time in ts:
            s0 = (time - day0).days *3600*24 + (time - day0).seconds
            binvect[k] = s0//bins
            k+=1
    else:
        dts = ts- dt.datetime(ts[0].year,ts[0].month,ts[0].day,ts[0].hour,0,0)
        k = 0
        for DT in dts:
            binvect[k] = ((dts[k].days * 3600 * 24) + dts[k].seconds)//bins
            k+=1
    return binvect

def compute_time_in_LD(phase,light_hours,dark_hours):
    t0 = phase[0]
    DT = dt.timedelta(0,4)
    duration_in_light = 0.
    duration_in_dark = 0.
    while t0 < phase[1]:
        if t0.hour in dark_hours:
            duration_in_dark += 4
        else:
            duration_in_light += 4
        t0 += DT
    return duration_in_light / 3600., duration_in_dark / 3600.
    
def diurnal_ratio_of_wakefulness(data_sleep, phase_vector,light_hours, 
                             dark_hours, epoch_dur=4, sub_name='Sub1'):
    results = np.zeros(len(phase_vector), dtype={'names':('Subject','Phase_Label','Phase_Days','Diurnal_Ratio_of_Wakefulness','WAKE_Percent_Light','WAKE_Percent_Dark'),
                       'formats':('S100','S100','S100',float,float,float)})
    results['Subject'] = sub_name
    ind_ph = 0
    for phase in phase_vector:
        data_ph = data_sleep[np.where(data_sleep.Timestamp < phase[1])[0]]
        data_ph = data_ph[np.where(data_ph.Timestamp >= phase[0])[0]]
        
        # consider artefacts
        iw = np.where(data_ph.Stage=='W*')[0]
        inr = np.where(data_ph.Stage=='NR*')[0]
        ir = np.where(data_ph.Stage=='R*')[0]
        
        data_ph.Stage[iw] = 'W'
        data_ph.Stage[inr] = 'NR'
        data_ph.Stage[ir] = 'R'
        
        hours = v_return_vector_hours(data_ph.Timestamp)
        index_light = np.zeros(0,dtype=int)
        for h in light_hours:
            index_light = np.hstack((index_light, np.where(hours == h)[0]))
        
        index_dark = np.zeros(0,dtype=int)
        for h in dark_hours:
            index_dark = np.hstack((index_dark, np.where(hours == h)[0]))
            
      
        if 'WT_344_PT' in sub_name:
            if index_light.shape[0] == 0:
                print 'sto eseguendo l eccezione'
                index_light = np.array([1,2])
                print 'shape not is %d' %index_light.shape[0]
                tot_wake_light = 1
                
        
        tot_wake_light = float((np.where(data_ph.Stage[index_light] == 'W')[0]).shape[0])
        tot_wake_dark = float((np.where(data_ph.Stage[index_dark] == 'W')[0]).shape[0])
        
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Phase_Label'][ind_ph] = phase[2]
        results['Diurnal_Ratio_of_Wakefulness'][ind_ph] = (tot_wake_light / index_light.shape[0]) / (tot_wake_dark / index_dark.shape[0])
        results['WAKE_Percent_Light'][ind_ph] = 100*(tot_wake_light / index_light.shape[0])
        results['WAKE_Percent_Dark'][ind_ph] = 100*(tot_wake_dark / index_dark.shape[0])

        ind_ph += 1
    
    return results
    
def diurnal_ratio_of_rem(data_sleep, phase_vector, light_hours, 
                             dark_hours, epoch_dur=4, sub_name='Sub1'):
    results = np.zeros(len(phase_vector), dtype={'names':('Subject','Phase_Label','Phase_Days','Diurnal_Ratio_of_REM','REM_Percent_Light','REM_Percent_Dark'),
                       'formats':('S100','S100','S100',float,float,float)})
    results['Subject'] = sub_name
    ind_ph = 0
    for phase in phase_vector:
        data_ph = data_sleep[np.where(data_sleep.Timestamp < phase[1])[0]]
        data_ph = data_ph[np.where(data_ph.Timestamp >= phase[0])[0]]
        
        # consider artefacts
        iw = np.where(data_ph.Stage=='W*')[0]
        inr = np.where(data_ph.Stage=='NR*')[0]
        ir = np.where(data_ph.Stage=='R*')[0]
        
        data_ph.Stage[iw] = 'W'
        data_ph.Stage[inr] = 'NR'
        data_ph.Stage[ir] = 'R'
        
        hours = v_return_vector_hours(data_ph.Timestamp)
        index_light = np.zeros(0,dtype=int)
        for h in light_hours:
            index_light = np.hstack((index_light, np.where(hours == h)[0]))
        
        index_dark = np.zeros(0,dtype=int)
        for h in dark_hours:
            index_dark = np.hstack((index_dark, np.where(hours == h)[0]))
        
        tot_rem_light = float((np.where(data_ph.Stage[index_light] == 'R')[0]).shape[0])
        tot_rem_dark = float((np.where(data_ph.Stage[index_dark] == 'R')[0]).shape[0])
        
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Phase_Label'][ind_ph] = phase[2]
        if index_light.shape[0]is 0 or index_dark.shape[0] is 0:
            results['Diurnal_Ratio_of_REM'][ind_ph] = np.nan
        elif tot_rem_dark == 0:
            results['Diurnal_Ratio_of_REM'][ind_ph] = np.inf
        else:
            results['Diurnal_Ratio_of_REM'][ind_ph] = (tot_rem_light / index_light.shape[0]) / (tot_rem_dark / index_dark.shape[0])
        
        if 'WT_344_PT' in sub_name:
            if index_light.shape[0] == 0:
                print 'sto eseguendo l eccezione'
                index_light = np.array([1,2])
                print 'shape noy is %d' %index_light.shape[0]
                
        results['REM_Percent_Light'][ind_ph] = 100*(tot_rem_light / index_light.shape[0])
        results['REM_Percent_Dark'][ind_ph] = 100*(tot_rem_dark / index_dark.shape[0])
        ind_ph += 1
    return results

def diurnal_ratio_of_nrem(data_sleep, phase_vector, light_hours, 
                             dark_hours, epoch_dur=4, sub_name='Sub1'):
    results = np.zeros(len(phase_vector), dtype={'names':('Subject','Phase_Label','Phase_Days','Diurnal_Ratio_of_NREM','NREM_Percent_Light','NREM_Percent_Dark'),
                       'formats':('S100','S100','S100',float,float,float)})
    results['Subject'] = sub_name
    ind_ph = 0
    for phase in phase_vector:
        data_ph = data_sleep[np.where(data_sleep.Timestamp < phase[1])[0]]
        data_ph = data_ph[np.where(data_ph.Timestamp >= phase[0])[0]]
        
        # consider artefacts
        iw = np.where(data_ph.Stage=='W*')[0]
        inr = np.where(data_ph.Stage=='NR*')[0]
        ir = np.where(data_ph.Stage=='R*')[0]
        
        data_ph.Stage[iw] = 'W'
        data_ph.Stage[inr] = 'NR'
        data_ph.Stage[ir] = 'R'
        
        hours = v_return_vector_hours(data_ph.Timestamp)
        index_light = np.zeros(0,dtype=int)
        for h in light_hours:
            index_light = np.hstack((index_light, np.where(hours == h)[0]))
        
        index_dark = np.zeros(0,dtype=int)
        for h in dark_hours:
            index_dark = np.hstack((index_dark, np.where(hours == h)[0]))
        
        tot_nrem_light = float((np.where(data_ph.Stage[index_light] == 'NR')[0]).shape[0])
        tot_nrem_dark = float((np.where(data_ph.Stage[index_dark] == 'NR')[0]).shape[0])
        
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Phase_Label'][ind_ph] = phase[2]
        if index_light.shape[0]is 0 or index_dark.shape[0] is 0:
            results['Diurnal_Ratio_of_NREM'][ind_ph] = np.nan
        elif tot_nrem_dark == 0:
            results['Diurnal_Ratio_of_NREM'][ind_ph] = np.inf
        else:
            results['Diurnal_Ratio_of_NREM'][ind_ph] = (tot_nrem_light / index_light.shape[0]) / (tot_nrem_dark / index_dark.shape[0])
        
        if 'WT_344_PT' in sub_name:
            if index_light.shape[0] == 0:
                print 'sto eseguendo l eccezione'
                index_light = np.array([1,2])
                print 'shape noy is %d' %index_light.shape[0]
                
        
        results['NREM_Percent_Light'][ind_ph] = 100*(tot_nrem_light / index_light.shape[0])
        results['NREM_Percent_Dark'][ind_ph] = 100*(tot_nrem_dark / index_dark.shape[0])
        ind_ph += 1
    return results
    
    
def diurnal_ratio_of_total_sleep(data_sleep, phase_vector, light_hours, 
                             dark_hours, epoch_dur=4, sub_name='Sub1'):
    results = np.zeros(len(phase_vector), dtype={'names':('Subject','Phase_Label','Phase_Days','Diurnal_Ratio_of_sleep','light_Percent_sleep','dark_Percent_sleep'),
                       'formats':('S100','S100','S100',float,float,float)})
    results['Subject'] = sub_name
    ind_ph = 0
    for phase in phase_vector:
        data_ph = data_sleep[np.where(data_sleep.Timestamp < phase[1])[0]]
        data_ph = data_ph[np.where(data_ph.Timestamp >= phase[0])[0]]
        
        # consider artefacts
        iw = np.where(data_ph.Stage=='W*')[0]
        inr = np.where(data_ph.Stage=='NR*')[0]
        ir = np.where(data_ph.Stage=='R*')[0]
        
        
        
        data_ph.Stage[iw] = 'W'
        data_ph.Stage[inr] = 'S'
        data_ph.Stage[ir] = 'S'
        
        inr = np.where(data_ph.Stage=='NR')[0]
        ir = np.where(data_ph.Stage=='R')[0]
        
        data_ph.Stage[inr] = 'S'
        data_ph.Stage[ir] = 'S'
        
        hours = v_return_vector_hours(data_ph.Timestamp)
        index_light = np.zeros(0,dtype=int)
        for h in light_hours:
            index_light = np.hstack((index_light, np.where(hours == h)[0]))
        
        index_dark = np.zeros(0,dtype=int)
        for h in dark_hours:
            index_dark = np.hstack((index_dark, np.where(hours == h)[0]))
        
        tot_nrem_light = float((np.where(data_ph.Stage[index_light] == 'S')[0]).shape[0])
        tot_nrem_dark = float((np.where(data_ph.Stage[index_dark] == 'S')[0]).shape[0])
        
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Phase_Label'][ind_ph] = phase[2]
        if index_light.shape[0]is 0 or index_dark.shape[0] is 0:
            results['Diurnal_Ratio_of_sleep'][ind_ph] = np.nan
        elif tot_nrem_dark == 0:
            results['Diurnal_Ratio_of_sleep'][ind_ph] = np.inf
        else:
            results['Diurnal_Ratio_of_sleep'][ind_ph] = (tot_nrem_light / index_light.shape[0]) / (tot_nrem_dark / index_dark.shape[0])
        
        if 'WT_344_PT' in sub_name:
            if index_light.shape[0] == 0:
                print 'sto eseguendo l eccezione'
                index_light = np.array([1,2])
                print 'shape noy is %d' %index_light.shape[0]
                
        
        results['light_Percent_sleep'][ind_ph] = 100*(tot_nrem_light / index_light.shape[0])
        results['dark_Percent_sleep'][ind_ph] = 100*(tot_nrem_dark / index_dark.shape[0])
        ind_ph += 1
    return results
    

def sleep_efficiency_x_phase(data_sleep, phase_vector, light_hours, 
                             dark_hours, epoch_dur=4, sub_name='Sub1'):
    """
        Percentuale di tempo di sonno x fase:
            - (tot_sleep_epochs_dark) / (tot_epochs_dark)
            - (tot_sleep_epochs_light) / (tot_epochs_light)
    """
    results = np.zeros(len(phase_vector), dtype={'names':('Subject','Phase_Label','Phase_Days',
                       'Diurnal_Sleep_Efficiency_Light','Diurnal_Sleep_Efficiency_Dark'),
                       'formats':('S100','S100','S100',float,float)})
    results['Subject'] = sub_name
    ind_ph = 0
    for phase in phase_vector:
        data_ph = data_sleep[np.where(data_sleep.Timestamp < phase[1])[0]]
        data_ph = data_ph[np.where(data_ph.Timestamp >= phase[0])[0]]
        
        # consider artefacts
        iw = np.where(data_ph.Stage=='W*')[0]
        inr = np.where(data_ph.Stage=='NR*')[0]
        ir = np.where(data_ph.Stage=='R*')[0]
        
        data_ph.Stage[iw] = 'W'
        data_ph.Stage[inr] = 'NR'
        data_ph.Stage[ir] = 'R'
        
        hours = v_return_vector_hours(data_ph.Timestamp)
        index_light = np.zeros(0,dtype=int)
        for h in light_hours:
            index_light = np.hstack((index_light, np.where(hours == h)[0]))
        
        index_dark = np.zeros(0,dtype=int)
        for h in dark_hours:
            index_dark = np.hstack((index_dark, np.where(hours == h)[0]))
        
        tot_rem_light = float((np.where(data_ph.Stage[index_light] == 'R')[0]).shape[0])
        tot_rem_dark = float((np.where(data_ph.Stage[index_dark] == 'R')[0]).shape[0])
        tot_nrem_light = float((np.where(data_ph.Stage[index_light] == 'NR')[0]).shape[0])
        tot_nrem_dark = float((np.where(data_ph.Stage[index_dark] == 'NR')[0]).shape[0])
        
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Phase_Label'][ind_ph] = phase[2]
        
        if 'WT_344_PT' in sub_name:
            if index_light.shape[0] == 0:
                print 'sto eseguendo l eccezione'
                index_light = np.array([1,2])
                print 'shape noy is %d' %index_light.shape[0]
                
        
        results['Diurnal_Sleep_Efficiency_Light'][ind_ph] = 100*(tot_rem_light+tot_nrem_light) / index_light.shape[0]
        results['Diurnal_Sleep_Efficiency_Dark'][ind_ph] = 100*(tot_rem_dark+tot_nrem_dark) / index_dark.shape[0]
        ind_ph += 1
    return results

def arousal_index_x_phsae(data_sleep, phase_vector, light_hours, 
                             dark_hours, epoch_dur=4, sub_name='Sub1',
                             consecutive_sleep=2):
    results = np.zeros(len(phase_vector), dtype={'names':('Subject','Phase_Label','Phase_Days',
                       'Arousal_Index_Light','Arousal_Index_Dark','Light_Duration_hours','Dark_Duration_hours','Arousal_Index_Light_x_Hour','Arousal_Index_Dark_x_Hour'),
                       'formats':('S100','S100','S100',float,float,float,float,float,float)})
    results['Subject'] = sub_name
    ind_ph = 0
    for phase in phase_vector:
        data_ph = data_sleep[np.where(data_sleep.Timestamp < phase[1])[0]]
        data_ph = data_ph[np.where(data_ph.Timestamp >= phase[0])[0]]
        
        # consider artefacts
        iw = np.where(data_ph.Stage=='W*')[0]
        inr = np.where(data_ph.Stage=='NR*')[0]
        ir = np.where(data_ph.Stage=='R*')[0]
        
        data_ph.Stage[iw] = 'W'
        data_ph.Stage[inr] = 'S'
        data_ph.Stage[ir] = 'S'
        
        # collapse rem and nrem
        inr = np.where(data_ph.Stage=='NR')[0]
        ir = np.where(data_ph.Stage=='R')[0]
        data_ph.Stage[inr] = 'S'
        data_ph.Stage[ir] = 'S'
        
#        hours = v_return_vector_hours(data_ph.Timestamp)
        hours_plus4 = v_return_vector_hours(data_ph.Timestamp+dt.timedelta(0,4))
        
        index_sleep = np.where(data_ph.Stage == 'S')[0]
        arousal_number = np.zeros(index_sleep.shape[0])
        ind = 0
        len_epi = 1
        while ind < index_sleep.shape[0] - 1:
            if index_sleep[ind] + 1 == index_sleep[ind+1]:
                len_epi += 1
            elif len_epi >= consecutive_sleep:
                arousal_number[ind] = 1
                len_epi = 1
            ind += 1
        hour_sleep = hours_plus4[index_sleep]
        arousal_light = np.zeros(0,dtype=int)
        for h in light_hours:
            arousal_light = np.hstack((arousal_light,np.sum(arousal_number[np.where(hour_sleep==h)[0]] )))
        
        arousal_dark = np.zeros(0,dtype=int)
        for h in dark_hours:
            arousal_dark = np.hstack((arousal_dark,np.sum(arousal_number[np.where(hour_sleep==h)[0]] )))
        
        dur_light, dur_dark = compute_time_in_LD(phase,light_hours,dark_hours)
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Phase_Label'][ind_ph] = phase[2]
        results['Arousal_Index_Light'][ind_ph] = np.sum(arousal_light)
        results['Arousal_Index_Dark'][ind_ph] = np.sum(arousal_dark)
        results['Dark_Duration_hours'][ind_ph] = dur_dark
        results['Light_Duration_hours'][ind_ph] = dur_light
        results['Arousal_Index_Light_x_Hour'][ind_ph] = results['Arousal_Index_Light'][ind_ph] / dur_light
        results['Arousal_Index_Dark_x_Hour'][ind_ph] = results['Arousal_Index_Dark'][ind_ph] / dur_dark

        ind_ph += 1
        
    return results

def rem_latency(data_sleep, phase_vector, light_hours, 
                             dark_hours, epoch_dur=4, sub_name='Sub1',cons_w_for_split=2):
    results = np.zeros(len(phase_vector), dtype={'names':('Subject','Phase_Label','Phase_Days',
                       'REM_Latency_Light','REM_Latency_Dark','Num_Of_REM_Episodes_Light','Num_Of_REM_Episodes_Dark'),
                       'formats':('S100','S100','S100',float,float,float,float)})
    results['Subject'] = sub_name
    episode_dict_phase = {}
    ind_ph = 0
    for phase in phase_vector:
        iph = np.where(data_sleep.Timestamp < phase[1])[0]
        iph = iph[np.where(data_sleep.Timestamp[iph] >= phase[0])[0]]
        data_ph = data_sleep[iph]
        
        # consider artefacts
        iw = np.where(data_ph.Stage=='W*')[0]
        inr = np.where(data_ph.Stage=='NR*')[0]
        ir = np.where(data_ph.Stage=='R*')[0]
        
        data_ph.Stage[iw] = 'W'
        data_ph.Stage[inr] = 'NR'
        data_ph.Stage[ir] = 'R'
        
        index_sleep = np.sort(np.hstack((np.where(data_ph.Stage == 'NR')[0],np.where(data_ph.Stage == 'R')[0])))
        ind = 0
        
        dict_sleep_epi = {}
        epi_ind = 0
        dict_sleep_epi[epi_ind] = []
        dict_epi_index = {}
        dict_epi_index[epi_ind] = []
        dict_epi_index_original = {}
        dict_epi_index_original[epi_ind] = []
        while ind < index_sleep.shape[0] - 1:
            if index_sleep[ind] + 1 == index_sleep[ind+1]:
                dict_sleep_epi[epi_ind] +=  [data_ph.Stage[index_sleep[ind]]]
                dict_epi_index[epi_ind] += [index_sleep[ind]]
                dict_epi_index_original[epi_ind] += [iph[index_sleep[ind]]]
            else:
                dict_sleep_epi[epi_ind] += [data_ph.Stage[index_sleep[ind]]]
                dict_epi_index[epi_ind] += [index_sleep[ind]]
                dict_epi_index_original[epi_ind] += [iph[index_sleep[ind]]]
                epi_ind += 1
                dict_sleep_epi[epi_ind] = []
                dict_epi_index[epi_ind] = []
                dict_epi_index_original[epi_ind] = []
                
            ind += 1
        dict_epi_index_original.pop(epi_ind)
        dict_epi_index.pop(epi_ind)
        dict_sleep_epi.pop(epi_ind)
        keys = np.sort(dict_epi_index.keys())
        for k in keys[:-1]:
            if dict_epi_index[k+1][0] - dict_epi_index[k][-1] < cons_w_for_split:
                dict_epi_index[k+1] = dict_epi_index[k] + dict_epi_index[k+1]
                dict_sleep_epi[k+1] = dict_sleep_epi[k] + dict_sleep_epi[k+1]
                dict_epi_index_original[k+1] = dict_epi_index_original[k] + dict_epi_index_original[k+1]
                dict_epi_index.pop(k)
                dict_sleep_epi.pop(k)
                dict_epi_index_original.pop(k)
                
        episode_dict_phase[phase[2]] = {'index':dict_epi_index_original,'stage':dict_sleep_epi}
        duration_light = np.zeros(0)
        duration_dark = np.zeros(0)
        keys = np.sort(dict_epi_index.keys())
        for k in keys:
            find_rem = np.where(np.array(dict_sleep_epi[k]) == 'R')[0]
            if find_rem.shape[0]:
                rem_0 = find_rem[0]
                dur = (dict_epi_index[k][rem_0] - dict_epi_index[k][0]) * epoch_dur
                hepi = data_ph.Timestamp[dict_epi_index[k][0]].hour
                if hepi in light_hours:
                    duration_light = np.hstack((duration_light,dur))
                else:
                    duration_dark = np.hstack((duration_dark,dur))
        
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Phase_Label'][ind_ph] = phase[2]
        results['REM_Latency_Light'][ind_ph] = np.nanmean(duration_light)
        results['REM_Latency_Dark'][ind_ph] = np.nanmean(duration_dark)
        results['Num_Of_REM_Episodes_Light'][ind_ph] = duration_light.shape[0]
        results['Num_Of_REM_Episodes_Dark'][ind_ph] = duration_dark.shape[0]
        ind_ph += 1
    return results, episode_dict_phase

def extract_epi(data_eeg,epoch='NR',merge_if=3,min_epi_len=3):
    epoch_vect = data_eeg.Stage
    index = np.zeros(len(epoch_vect))
    index[np.where(epoch_vect==epoch)[0]] = 1
    dict_episodes = {}
    k = 0
    old_end = 0
    while True:
        try:
            start,end = None,None
            start = old_end + np.where(index[old_end:] == 1)[0][0]
            end = start + np.where(index[start:] == 0)[0][0]
            old_end = end
        except IndexError:
            if not start is None:
                end = len(index) - 1
                dict_episodes[k] = [start,end]
            break
        dict_episodes[k] = [start,end]
        k += 1
     
    list_keys = np.sort(dict_episodes.keys()[:-1])
    for key in list_keys:
        if dict_episodes[key+1][0] - dict_episodes[key][1] <= merge_if:
            start,end = dict_episodes.pop(key)
            dict_episodes[key+1] = [start,dict_episodes[key+1][1]]
           
            
    list_keys = np.sort(dict_episodes.keys())
    for key in list_keys:
        num_nrem = len(np.where(epoch_vect[dict_episodes[key][0]:dict_episodes[key][1]]==epoch)[0])
        if num_nrem < min_epi_len:
            dict_episodes.pop(key) 
    
    array_episodes = np.zeros(len(dict_episodes.keys()),dtype={'names':('Start','End'),'formats':(int,int)}) 
    list_keys = np.sort(dict_episodes.keys()) 
    for k in xrange(array_episodes.shape[0]):
        array_episodes['Start'][k],array_episodes['End'][k] = dict_episodes[list_keys[k]]
    return array_episodes

def merge_epi(episodes,merge_if=1):
    # duration of episodes
    delta = episodes['End'] - episodes['Start']
    # condition for merging episodes
    boolean = delta <= merge_if
    if not np.sum(boolean):
        return episodes
    indexes = np.where(boolean)[0]
    # assiging new types to transitions
    for i in indexes:
        if i == 0:
            episodes['Stage'][i] = episodes['Stage'][i+1]
        if i == episodes.shape[0] - 1:
            episodes['Stage'][i] = episodes['Stage'][i-1]
        else:
            if delta[i-1] > delta[i+1]:
                episodes['Stage'][i] = episodes['Stage'][i-1]
            else:
                episodes['Stage'][i] = episodes['Stage'][i+1]
    type_prev = episodes['Stage'][0]
    for i in xrange(1,episodes.shape[0]):
        if episodes['Stage'][i] == type_prev:
            episodes['Start'][i] = episodes['Start'][i-1]
            episodes['Start'][i-1] = -1
        type_prev = episodes['Stage'][i]
    episodes = episodes[episodes['Start'] != -1]  
    return episodes

def power_per_phase(data_sleep, phase_vector, deltaCol=0,
                    epoch_dur=4, sub_name='Sub1',group='Group1',epoch='NR',merge_if=3,min_epi_len=3):
    results = np.zeros(len(phase_vector), dtype={'names':('Group','Subject','Phase_Label','Phase_Days','Power'),
                       'formats':('S100','S100','S100','S100',float)})
    results['Subject'] = sub_name
    results['Group'] = group
    ind_ph = 0
    for phase in phase_vector:
        data_ph = data_sleep[np.where(data_sleep.Timestamp < phase[1])[0]]
        data_ph = data_ph[np.where(data_ph.Timestamp >= phase[0])[0]]
        epi_ph = extract_epi(data_ph,epoch=epoch,merge_if=merge_if,min_epi_len=min_epi_len)
        delta_index = []
        for start,end in epi_ph:
            delta_index = np.hstack((delta_index,range(start,end)))
        delta_index = np.array(delta_index,dtype=int)
        mask = np.ones(data_ph.Stage.shape[0], dtype=bool)
        mask[delta_index] = False
        non_delta = np.arange(data_ph.Stage.shape[0])[mask]
        data_ph.PowerSp[non_delta,:] = np.nan
        data_ph.PowerSp[np.where(data_ph.Stage!=epoch)[0],:] = np.nan
        results['Phase_Label'][ind_ph] = phase[2]
        results['Phase_Days'][ind_ph] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        results['Power'][ind_ph] = np.nanmean(data_ph.PowerSp[:,deltaCol])
        ind_ph += 1
    return results
        
        
def delta_power(data_eeg,array_episodes,epoch='NR',bins=3600,normFact=1,deltaCol=0,sub_name='Sub1'):
    delta_index = []
    for start,end in array_episodes:
        delta_index = np.hstack((delta_index,range(start,end)))
    delta_index = np.array(delta_index,dtype=int)
    mask = np.ones(data_eeg.Stage.shape[0], dtype=bool)
    mask[delta_index] = False
    non_delta = np.arange(data_eeg.Stage.shape[0])[mask]
    Power = copy(data_eeg.PowerSp)
    Power[non_delta,:] = np.nan
    Power[np.where(data_eeg.Stage!=epoch)[0],:] = np.nan
    binvect = consecutive_bins(data_eeg.Timestamp,bins=bins)
    all_bins = np.unique(binvect)
    matrix = np.zeros(all_bins.shape[0],dtype={'names':('Subject','Bin','Start','End','NumEpochs','Mean','Median','SD'),
    'formats':('S100',int,'S40','S40',int,float,float,float)})
    k = 0
    if normFact != 1:
        normFact = normFact / 100.
    for b in all_bins:
        index = np.where(binvect == b)[0]

        index_bin = list(set(index).intersection(delta_index))
#        print len(index_bin),Power[index_bin,deltaCol]
        PowerBin = Power[index_bin,deltaCol]/normFact
        matrix['Subject'][k] = sub_name
        matrix['Bin'][k] = b
        matrix['Start'][k] = data_eeg.Timestamp[index[0]].isoformat()
        matrix['End'][k] = data_eeg.Timestamp[index[-1]].isoformat()
        matrix['NumEpochs'][k] = len(index_bin)
        if len(index_bin):
            matrix['Mean'][k] = np.nanmean(PowerBin)
            matrix['Median'][k] = np.nanmedian(PowerBin)
            matrix['SD'][k] = np.nanstd(PowerBin)
        else:
            matrix['Mean'][k] = np.nan
            matrix['Median'][k] = np.nan
            matrix['SD'][k] = np.nan
        k += 1
    return matrix
    
    
def dRem(data_eeg, light_hours,
         sub_name='Sub1',group='Group1', min_rems=1, merge_if=0,min_wake_per_epi=3):
    data_eeg.Stage[np.where(data_eeg.Stage=='W*')[0]] = 'W'
    data_eeg.Stage[np.where(data_eeg.Stage=='R*')[0]] = 'R'
    array_episodes = extract_epi(data_eeg,epoch='W',merge_if=merge_if,min_epi_len=min_wake_per_epi)
    intrusion_index = []
    all_w_to_R = []
    for start,end in array_episodes:
        if end >= len(data_eeg.Stage)-1:
            continue
        if data_eeg.Stage[end] == 'R':
            intrusion_index += [end]
    REMS = np.where(data_eeg.Stage=='R')[0]
    for i in REMS:
        if i > 0 and data_eeg.Stage[i-1]=='W':
            all_w_to_R += [i]
            
    matrix = np.zeros(1,dtype={'names':('Subject','Group','Total Light','Total Dark'),
                                       'formats':('S100','S100',int,int)})
    if len(intrusion_index):
        hours = v_return_vector_hours(data_eeg.Timestamp[intrusion_index]+dt.timedelta(0,4))
        
        for h in hours:
            if h in light_hours:
                matrix['Total Light'][0] = matrix['Total Light'][0] + 1
            else:
                matrix['Total Dark'][0] = matrix['Total Dark'][0] + 1
                
    matrix['Subject'][0] = sub_name
    matrix['Group'][0] = group
    return intrusion_index,all_w_to_R,matrix

def Stage_2_Stage_dist(data_eeg, phase_vect,stage,sub_name='Sub1',group='Group1', min_epi_len=2, merge_if=1,
                       epoch_dur = 4):
    data_eeg.Stage[np.where(data_eeg.Stage==stage+'*')[0]] = stage
    array_episodes = extract_epi(data_eeg,epoch=stage,merge_if=merge_if,min_epi_len=min_epi_len)
    matrix = np.zeros(len(phase_vect),dtype={'names':('Subject','Group','Stage','Phase_Days','Phase','Mean(min)','Median(min)','STD(min)','Num.'),
                                       'formats':('S100','S100','S3','S100','S100',float,float,float,int)})
    matrix['Subject'] = sub_name
    matrix['Group'] = group
    matrix['Stage'] = stage
    phase_ind = 0
    for phase in phase_vect:
        episodes = True
        ind_cut = np.where(data_eeg.Timestamp[array_episodes['Start']] < phase[1])[0]
        if not ind_cut.shape[0]:
            episodes = False
        if episodes:  
            array_phase = array_episodes[ind_cut]
            ind_cut = np.where(data_eeg.Timestamp[array_phase['Start']] >= phase[0])[0]
            if not ind_cut.shape[0]:
                episodes = False
        if episodes: 
            array_phase = array_phase[ind_cut]
            dtime_vec = (array_phase['Start'][1:] - array_phase['End'][:-1]) * epoch_dur / 60.
            
            matrix[phase_ind]['Mean(min)'] = np.nanmean(dtime_vec)
            matrix[phase_ind]['Median(min)'] = np.nanmedian(dtime_vec)
            matrix[phase_ind]['STD(min)'] = np.nanstd(dtime_vec)
            matrix[phase_ind]['Num.'] = len(dtime_vec)
        else:
            matrix[phase_ind]['Mean(min)'] = np.nan
            matrix[phase_ind]['Median(min)'] = np.nan
            matrix[phase_ind]['STD(min)'] = np.nan
            matrix[phase_ind]['Num.'] = 0
        matrix[phase_ind]['Phase_Days'] = phase[0].isoformat() + ' -> ' + phase[1].isoformat()
        matrix[phase_ind]['Phase'] = phase[2]
        phase_ind += 1
    return matrix

if __name__=='__main__':
    plt.close('all')
    datas = np.load('/Users/Matte/Scuola/Dottorato/Projects/Pace/Paper mch/sleep/RTM/male22.phz')
    light_hours = np.arange(16+12,16+24)%24
    dark_hours = np.arange(16,16+12)%24
    print datas.keys()[0]
    data_eeg = datas[datas.keys()[0]].all().Dataset
    phase_vector = [(data_eeg.Timestamp[0],data_eeg.Timestamp[-900*12]+dt.timedelta(0,4),'first'),
                    (data_eeg.Timestamp[-900*12]+dt.timedelta(0,4),data_eeg.Timestamp[-1]+dt.timedelta(0,4),'last')]
    matrix = Stage_2_Stage_dist(data_eeg,phase_vector,'R',merge_if=3,min_epi_len=3)
