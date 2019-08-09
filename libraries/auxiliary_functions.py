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
#from copy import copy

from copy import deepcopy
from scipy.signal import filtfilt,ellip
import numpy as np
import datetime as dt

def compute_perc(sig,sc,states,perc_list):
    res_perc = np.zeros((states.__len__(),perc_list.__len__()),dtype = float)
    idx = 0
    for st in states:
        s_e__epocs = extract_epi(sc,epoch = st,merge_if=2,min_epi_len=2)
        s_e__epocs['Start'] = 2*(s_e__epocs['Start']*4)
        s_e__epocs['End'] = 2*(s_e__epocs['End']*4)
        
        sig_stage = np.array([])
        for tr in range(s_e__epocs.shape[0]):
            start = s_e__epocs['Start'][tr]
            stop = s_e__epocs['End'][tr]
            sig_stage = np.hstack((sig_stage,sig[start:stop]))
       
        pc = 0
        for pp in perc_list:
            try:
                val = np.percentile(sig_stage,pp)
            except:
                val = np.nan
                
            res_perc[idx,pc] = val
            pc += 1
        idx += 1
           
    return res_perc

def normalize_emg(signal):
    
    # process EMG signal: rectify
    emg_rectified = abs(signal)
    # 250 is not a magic number: fs = 500 Hz, wanted bin = 0.5 s
    ra = np.zeros(int(emg_rectified.shape[0]/250))
    idx = 0
    for kk in range(0, emg_rectified.shape[0],250):
        ra[idx] = np.nanmean(emg_rectified[kk:kk+250])
        idx += 1
    
    hp = np.percentile(ra,99.5)
    lp = np.percentile(ra,0.5)

    ra[ra > hp] = hp  
    ra[ra < lp] = lp
  
    emg_norm = ((ra - np.min(ra))/(np.max(ra)-np.min(ra)))*100
    avgEMG = np.nanmean(emg_norm)
        
    return emg_norm,avgEMG,hp,lp

def ellip_bandpass(lowcut, highcut, fs, order=5, rp=0.1, rs=40):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = ellip(order, rp, rs, [low, high], btype='bandpass')
    return b, a

def ellip_bandpass_filter(data, lowcut, highcut, fs, order=5, rp=0.1, rs=40):
    b, a = ellip_bandpass(lowcut, highcut, fs, order=order, rp=rp, rs=rs)
    y = filtfilt(b, a, data)
    return y

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


def vector_hours(timestamps):
    
    res = np.zeros(timestamps.shape[0],dtype = int)
    for tt in range(timestamps.shape[0]):
        res[tt] = timestamps[tt].hour
    
    return res

def bin_epi(data_eeg, tbinSec, time0, time1,epoch='NR',epochDur = 4):
    
    binVect = np.array([time0])
    tdelta = dt.timedelta(0,tbinSec)
    tt = time0
    while tt < time1 - tdelta:
        binVect = np.hstack((binVect, [tt + tdelta]))
        tt = tt + tdelta
    
    epi = np.array(extract_epi(data_eeg,epoch=epoch,merge_if=0,min_epi_len=1),{'names':('Start','End'),'formats':(float,float)})
    
    for tt in binVect:
        idx_epi = 0
        for episode in epi:
            
            if tt <= time0 + dt.timedelta(0,epochDur * episode['Start']):
                idx_epi += 1
                continue
            elif tt < time0 + dt.timedelta(0,epochDur * episode['End']):
                tmpE = deepcopy(episode['End'])
                epi['End'][idx_epi] = ((tt - time0).seconds + 3600*24*(tt - time0).days) / float(epochDur)
                tmpepi = np.zeros(1,dtype={'names':('Start','End'),'formats':(float,float)})
                tmpepi['Start'] = epi['End'][idx_epi]
                tmpepi['End'] = tmpE
                epi = np.hstack((epi, tmpepi))
                sort_idx = np.argsort(epi,order='Start')
                epi = epi[sort_idx]
                idx_epi += 1
                break
            elif idx_epi + 1 < epi.shape[0] and tt <  time0 + dt.timedelta(0,epochDur * epi['Start'][idx_epi+1]):
#                idx_epi = cyle_epi_idx + idx_epi + 1
                idx_epi += 1
                break
            idx_epi += 1
    return epi

def epidur_if_binAdj(epi, bins, binvec = range(24), epochDur=4):
    binepi = (epi['Start'] * epochDur) // bins
    idx = 0
    
    binvec = np.array(binvec)
    res = np.zeros(binvec.shape[0])
    for k in binvec:
        res[idx] = np.nansum(epi['End'][binepi==k] - epi['Start'][binepi==k])
        idx += 1
    return res

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
     
#    list_keys = dict_episodes.keys()
    list_keys = list(dict_episodes)
    for key in list_keys:
        try:
            if dict_episodes[key+1][0] - dict_episodes[key][1] <= merge_if:
                start,end = dict_episodes.pop(key)
                dict_episodes[key+1] = [start,dict_episodes[key+1][1]]
        except:
            break
           
    list_keys = list(dict_episodes)
    for key in list_keys:
        num_nrem = len(np.where(epoch_vect[dict_episodes[key][0]:dict_episodes[key][1]]==epoch)[0])
        if num_nrem < min_epi_len:
            dict_episodes.pop(key) 
    
    array_episodes = np.zeros(len(dict_episodes.keys()),dtype={'names':('Start','End'),'formats':(int,int)}) 
    
    list_keys = list(dict_episodes)
    for k in range(array_episodes.shape[0]):
        array_episodes['Start'][k],array_episodes['End'][k] = dict_episodes[list_keys[k]]
    return array_episodes


def powerDensity_function(dataDict, Group_Dict, freqLim_Hz,
                   delimiter = '\t'):
    """
        Input:
        ======
           
            - dataDict : dictionary
                keys are data names, values are EEG_Dataset object 
            - Group_Dict : dictionary
                Keys are group names, values are data names of
                the corrisponding group
            - freqLim_Hz : float
                higer frequency that will be imported
            - delimiter : char  
                delimiter of the EEG dataset column (default '\t')
        
        Output:
        =======
            - Power_Wake : numpy array
                power density of Wake Stages
           
            - Power_Rem : numpy array
                power density of Rem Stages
            
            - Power_NRem : numpy array
                power density of NRem Stages
            - FreqVect : numpy array
                frequencies (x_axis when ploting Power Density)
            - normFactor : float
                Normalization factor
    """
    GroupNum   = {}
    IndexGroup = {}
    IndexArray_dict = {}
    totSub  = 0
    for key in list(Group_Dict.keys()):
        GroupNum[key] = len(Group_Dict[key])
        IndexGroup[key] = {}
        IndexArray_dict[key] = np.array([], dtype=int)
        kk = 0
        for subject in Group_Dict[key]:
            IndexGroup[key][subject] = totSub + kk
            IndexArray_dict[key] = np.hstack((IndexArray_dict[key],
                                            [totSub + kk]))
            kk += 1
        totSub += GroupNum[key]
        
    flag = True

    for group in list(Group_Dict.keys()):
        for subject in Group_Dict[group]:
            DataStruct = dataDict[subject]
            ind = IndexGroup[group][subject]
            freqTuple = DataStruct.freqTuple
            colNum = -1
            for f in freqTuple[:,1]:
                if f <= freqLim_Hz:
                    colNum += 1
                else:
                    break
            freqLim_Hz = freqTuple[colNum][1]
            if flag:
                Power_Wake = np.zeros((totSub, colNum+1), dtype = float)
                Power_Rem  = np.zeros((totSub, colNum+1), dtype = float)
                Power_NRem = np.zeros((totSub, colNum+1), dtype = float)
                FreqVect   = np.linspace(0, freqLim_Hz, colNum+1)
                flag = False
            Data  = DataStruct.PowerSp[1:-1,:colNum+1]
            Stage = DataStruct.Stage
            Bool   = (Stage[1:-1] == Stage[:-2]) *\
                     (Stage[1:-1] == Stage[2: ])
            Index  = np.arange(len(Bool),dtype=int)
            Wake   = np.where(Stage[1:-1] == 'W')[0]
            Rem    = np.where(Stage[1:-1] == 'R')[0]
            NRem   = np.where(Stage[1:-1] == 'NR')[0]
            pw  = Index[Wake][np.where(Bool[Wake] ==True)[0]]
            pr  = Index[Rem][np.where(Bool[Rem]   ==True)[0]]
            pnr = Index[NRem][np.where(Bool[NRem] ==True)[0]]
            normFactor = normalizFactor_powerDensity(Data,pw, pr, pnr)
            Power_Wake[ind,:] = np.nanmean(Data[pw],axis=0)  / normFactor
            Power_Rem[ind,:]  = np.nanmean(Data[pr],axis=0)  / normFactor
            Power_NRem[ind,:] = np.nanmean(Data[pnr],axis=0) / normFactor
    
    return (Power_Wake, Power_Rem, Power_NRem, FreqVect,IndexArray_dict, IndexGroup)

def normalizFactor_powerDensity(PowerSp, pw, pr, pnr):
    """
        Function Target:
        ================
            Computing normalizing factor of power density
        Input:
        ======
            - PowerSp : numpy array (float)
                Matrix  (epochs x frequency band) containing a power
                spectrum
            - pw, pr, pnr : numpy array (int)
                Indexes of wake, rem, nrem epochs that are not on the
                border between one stage and the other
        Output:
        =======
            - Normalization Factor : float
            
    """
    Tot_p = np.zeros(len(pw) + len(pr) + len(pnr))
    Tot_p[0:len(pw)] = np.nanmean(PowerSp[pw,:], axis=1)
    Tot_p[len(pw):len(pw) + len(pnr)] = np.nanmean(PowerSp[pnr,:], axis=1)
    Tot_p[len(pw) + len(pnr):] = np.nanmean(PowerSp[pr,:], axis=1)
    return np.nanmean(Tot_p)


    