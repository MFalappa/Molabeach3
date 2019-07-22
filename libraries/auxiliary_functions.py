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
#from scipy import stats

import numpy as np
#import datetime

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


    