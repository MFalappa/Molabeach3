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
from Analyzing_GUI import *
from Plotting_GUI import *
from Modify_Dataset_GUI import *
from copy import copy,deepcopy
import sys
from PyQt5.QtWidgets import QApplication
import pandas as pd
## TODO: creare dizionario timestamps[dataname] per tipo di dato e cambiare le funzioni
## che richiamano timestamps in analyzing_gui
def Power_Density(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    lock       = myInput[4]
    print('Input ok')
    DataDict, dictPlot, info = {},{},{}
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    print('lenNames ok')
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
    print('set input ol')
    DataDict = {}
    AllData  = {}
    for key in list(Datas.keys()):
        try:
            lock.lockForRead()
            AllData[key] = copy(Datas.takeDataset(key))
        finally:
            lock.unlock()
    print('Data copied')
    (Power_Wake, Power_Rem, Power_NRem, Fr,
        IndexArray_dict,IndexGroup)= F_PowerDensity_GUI(AllData,
                       DataGroup, freqLim_Hz)
    print('PD analysis done')
    NRow = np.prod(Power_Wake.shape)
    DataDict['Power Density Wake'] = np.zeros(NRow, dtype = {
        'names':('Group','Subject','Frequency (Hz)','Value'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,float,float)})
    index = 0
    shape = Power_Wake.shape[1]
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]: 
            DataDict['Power Density Wake']['Group'][index:index + shape] =\
                key
            DataDict['Power Density Wake']['Subject'][index:index + shape] =\
                name
            DataDict['Power Density Wake']['Frequency (Hz)']\
                [index:index + shape] = Fr
            DataDict['Power Density Wake']['Value'][index:index + shape] =\
                Power_Wake[IndexGroup[key][name],:]
            index += shape
    print('PD data Wake extracted')
    index = 0      
#    DataDict['Power Density Rem'] = DataDict['Power Density Wake']
    DataDict['Power Density Rem'] = np.zeros(NRow, dtype = {
        'names':('Group','Subject','Frequency (Hz)','Value'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,float,float)})
    shape = Power_Rem.shape[1]
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            DataDict['Power Density Rem']['Value'][index:index + shape] =\
                Power_Rem[IndexGroup[key][name],:]
            DataDict['Power Density Rem']['Group'][index:index + shape] =\
                key
            DataDict['Power Density Rem']['Subject'][index:index + shape] =\
                name
            DataDict['Power Density Rem']['Frequency (Hz)']\
                [index:index + shape] = Fr
            index += shape
    index=0
    print('PD data Rem extracted')
#    DataDict['Power Density NRem'] = DataDict['Power Density Wake']
    DataDict['Power Density NRem'] = np.zeros(NRow, dtype = {
        'names':('Group','Subject','Frequency (Hz)','Value'),
        'formats':('|S%d'%lenGroupName,'|S%d'%lenName,float,float)})
    shape = Power_NRem.shape[1]
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            DataDict['Power Density NRem']['Value'][index:index + shape] =\
                Power_NRem[IndexGroup[key][name],:]
            DataDict['Power Density NRem']['Group'][index:index + shape] =\
                key
            DataDict['Power Density NRem']['Subject'][index:index + shape] =\
                name
            DataDict['Power Density NRem']['Frequency (Hz)']\
                [index:index + shape] = Fr
            index += shape
    print('PD data Nrem extracted')
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
    print('dictPlot build')
    info['Types']  = ['Group EEG','Power Density']
    info['Factor'] = [0,1,2]
    datainfo = {'Power Density Wake': info,'Power Density Rem': info,
                'Power Density NRem': info}
    DD = {}
    DD['Power Density'] = {}
    DD['Power Density']['Power Density Wake'] = DataDict['Power Density Wake']
    DD['Power Density']['Power Density Rem'] = DataDict['Power Density Rem']
    DD['Power Density']['Power Density NRem'] = DataDict['Power Density NRem']
#    print('Completed analysis')
#    raw_input('press any key')
    return DD, dictPlot, datainfo
def Group_Error_Rate(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    
    Dark_start = Input[0]['Combo'][0]
    Dark_length = Input[0]['Combo'][1]
    StatIndex = Input[0]['Combo'][2]
    TimeInterval = Input[0]['Combo'][3]
    Dataset_Dict = {}
    TimeStamps_Dict = {}
#    print(DataGroup)
    for group in list(DataGroup.keys()):
        for dataName in DataGroup[group]:
            try:
                lock.lockForRead()
                Dataset_Dict[dataName] = copy(Datas.takeDataset(dataName))
                if Datas.getTimeStamps(dataName):
                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
                else:
                    TimeStamps_Dict[dataName] = TimeStamps
            finally:
                lock.unlock()
    VectorError = std_Subjective_Error_Rate_GUI(Dataset_Dict, TimeStamps_Dict,
                                                DarkStart = Dark_start,
                                                DarkDuration = Dark_length,
                                                TimeInterval = TimeInterval) 
#==============================================================================
#   Group statistical index matrix creation
#==============================================================================
    Error_Group_Matrix = stdMatrix_Group_Stat_Index_GUI(VectorError, DataGroup)
    x_label = 'Time (h)'
    y_label = 'Error Rate'
#==============================================================================
#   Plot error bars per group
#==============================================================================
#    fig = plot_Standard_Input_Error_Bar(Error_Group_Matrix, Dark_length,
#                                        TimeInterval, 'Error Rate group',
#                                        x_label, y_label, title_size = 20, 
#                                        label_size = 15, tick_size = 12,
#                                        legend_size = 15,
#                                        hold_on = True, stat_ind = StatIndex,
#                                        linewidth = 1.5, elinewidth = 2,
#                                        tick_every = 2)
    DataDict = {'Group Error Rate' : {}}
    DataDict['Group Error Rate']['Error Rate'] = Error_Group_Matrix
    dictPlot = {}
    dictPlot['Fig: Group Error Rate'] = {}
    dictPlot['Fig: Group Error Rate']['Error Rate'] = (
        Error_Group_Matrix, Dark_length, TimeInterval, 'Error Rate group',
        x_label, y_label, 20, 15, 12, 15, True, StatIndex, 1.5, 2, 4, 0.4)
    info = {}
    info['Error Rate'] = {'Error Rate' : {}}
    info['Error Rate']['Types'] =\
        ['Group', 'Error Rate']
    info['Error Rate']['Factor'] = [0,1]
    return DataDict, dictPlot, info
def Sleep_Time_Course(*myInput):
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
    
    AllData  = {}
    for group in list(DataGroup.keys()):
        for key in DataGroup[group]:
            try:
                lock.lockForRead()
                AllData[key] = copy(Datas.takeDataset(key))
            finally:
                lock.unlock()
    secTimeDiff = []
    tinit = []
    ind = False
    for name in list(AllData.keys()):
        timeDiff = AllData[name].Timestamp[-1] - AllData[name].Timestamp[0]
        secTimeDiff += [timeDiff]
        if ind:
            daydiff = AllData[name].Timestamp[0] - tinit[0]
            AllData[name].Timestamp = AllData[name].Timestamp\
                - datetime.timedelta(days=daydiff.days)
        else:
            ind = True
        tinit += [AllData[name].Timestamp[0]]
    maxTime = np.array(tinit) + np.array(secTimeDiff)
    startT = np.min(tinit)
    startT.replace(second=0)
    finalT = np.max(maxTime)
    NEP_Dict = {}
    TimeDict = {}
    Time_MyDict = {}
    Epi_Dur = {}
    print('Start/End time')
    print(startT, finalT)
    for name in list(AllData.keys()):
        Time = AllData[name].Timestamp
        Epoch = F_Epoch(AllData[name].Stage)
#==============================================================================
#         Insert nans
#==============================================================================
        Time, Epochs = add_NANs(Time, Epoch)
        non_nan_ind = np.where(np.logical_not(np.isnan(Epochs[0])))[0]
        NAN_IND_PSP = np.where(np.isnan(AllData[name].PowerSp[:,0]))[0]
        Epoch = np.array(Epochs[0],dtype=float)
        Epoch[non_nan_ind][NAN_IND_PSP] = np.nan
        print(('LEN Epoch nans',len(NAN_IND_PSP)))
        # End new code
        NEP,TT1 = EpocheTot_xTimebin_GUI(Epoch, Time, Bin, startT, finalT,
                                         Type=Type)
        NEP_Dict[name] = NEP
        TimeDict[name] = TT1
        print(name,' ',TT1[0],' ',TT1[-1])
        Mean,Dur,TT = EpisodsDurationXhour_GUI(Epoch,Time,Bin,startT,finalT,
                                               EpochDur=EpochDur,Type=Type,
                                               total_or_mean=total_or_mean)
        Epi_Dur[name] = Mean
        Time_MyDict[name] = TT
    std_Matrix_Nep = std_Binned_TimeCourse_GUI(NEP_Dict, TimeDict)
    std_Matrix_Dur = std_Binned_TimeCourse_GUI(Epi_Dur, Time_MyDict,
                                               rescaleBy=60)
    std_Daily_Nep =\
        std_DailyAverage_SubjectiveTimeCourse_GUI(std_Matrix_Nep, dark_start)
    std_Daily_Dur =\
        std_DailyAverage_SubjectiveTimeCourse_GUI(std_Matrix_Dur, dark_start)
    std_Matrix_Group = std_TimeCourse_Group_GUI(std_Matrix_Nep, DataGroup)
    std_Matrix_Group_Dur = std_TimeCourse_Group_GUI(std_Matrix_Dur,
                                                    DataGroup)
    std_Matrix_Group_Dur['Mean'] = std_Matrix_Group_Dur['Mean'] / 60.
    std_Matrix_Group_Dur['Median'] = std_Matrix_Group_Dur['Median'] / 60.
    std_Matrix_Group_Dur['SEM'] = std_Matrix_Group_Dur['SEM'] / 60.
    std_Matrix_Group_Dur['25 perc'] = std_Matrix_Group_Dur['25 perc'] / 60.
    std_Matrix_Group_Dur['75 perc'] = std_Matrix_Group_Dur['75 perc'] / 60.
    
    if (2 in Type) and (3 in Type):
        word = 'Sleep'
    elif 1 in Type:
        word = 'Wake'
    elif 2 in Type:
        word = 'Rem'
    else:
        word = 'NRem'
    DataDict = {'Sleep Time Course' : {}}
    DataDict['Sleep Time Course']['Group %s Num Episodes'%word] =\
        std_Matrix_Group
    if total_or_mean == 'Mean':
        DataDict['Sleep Time Course']['Group %s Episode Duration'%word] =\
            std_Matrix_Group_Dur
    else:
        DataDict['Sleep Time Course']['Group Total %s'%word] =\
            std_Matrix_Group_Dur
    DataDict['Sleep Time Course']['%s Num Episodes'%word] = std_Matrix_Nep
    if total_or_mean == 'Mean':
        DataDict['Sleep Time Course']['%s Episode Duration'%word] =\
            std_Matrix_Dur
    else:
        DataDict['Sleep Time Course']['Total %s'%word] =\
            std_Matrix_Dur
    DataDict['Sleep Time Course']['Daily %s Num Episodes'%word] = std_Daily_Nep
    if total_or_mean == 'Mean':            
        DataDict['Sleep Time Course']['Daily %s Episode Duration'%word] =\
            std_Daily_Dur
    else:
        DataDict['Sleep Time Course']['Daily Total %s'%word] = std_Daily_Dur
    
    info = {}
    info['Types']  = ['Single Subject EEG','Num Episodes']
    info['Factor'] = [0,1]
    datainfo = {'%s Num Episodes'%word: info}
    
    info = {}
    info['Types']  = ['Single Subject EEG','Episode Duration']
    info['Factor'] = [0,1]
    if total_or_mean == 'Mean':
        datainfo['%s Episode Duration'%word] = info
    else:
        datainfo['Total %s'%word] = info
    info = {}
    info['Types']  = ['Single Subject EEG','Daily Num Episodes']
    info['Factor'] = [0,1]
    datainfo['Daily %s Num Episodes'%word] = info
    
    info = {}
    info['Types']  = ['Single Subject EEG','Daily Episode Duration']
    info['Factor'] = [0,1]
    if total_or_mean == 'Mean':
        datainfo['Daily %s Episode Duration'%word] = info
    else:
        datainfo['Daily Total %s'%word] = info
    
    
    info = {}
    info['Types']  = ['Group EEG','Episode Duration']
    info['Factor'] = [0,1]
    if total_or_mean == 'Mean':
        datainfo['Group %s Episode Duration'%word] = info
    else:
        datainfo['Group Total %s'%word] = info
    
    info = {}
    info['Types']  = ['Group EEG','Num Episodes']
    info['Factor'] = [0,1]
    datainfo['Group %s Num Episodes'%word] = info
      
    title = 'Number of sleep episodes: %s'%word
    x_label = ''
    y_label = 'Episodes num'
    dictPlot = {'Fig:Sleep Time Course' : {}}
    dictPlot['Fig:Sleep Time Course']['%s Num Episodes'%word] =\
        (std_Matrix_Group, title, x_label, y_label, True, stat_index, 1.5, 20,
         12, 15, tick_Num)
    if total_or_mean == 'Mean':
        title = '%s episode duration'%word
        y_label = 'Episodes duration (min)'
        saveName = '%s Episode Duration'%word
    else:
        title = 'Total %s'%word
        y_label = '%s total (min)'%word
        saveName = 'Total %s'%word
    x_label = ''
    
    dictPlot['Fig:Sleep Time Course'][saveName] = (
        std_Matrix_Group_Dur, title, x_label, y_label, True, stat_index,
        1.5, 20, 12, 15, tick_Num)
    return DataDict,dictPlot, datainfo
def Linear_Discriminant_Analysis(*myinput):
    Datas      = myinput[0]
    Input      = myinput[1]
    DataGroup  = myinput[2]
    lock       = myinput[4]
    
    Behaviour_Dark_Start = Input[0]['Combo'][0]
    Sleep_Dark_Start = Input[0]['Combo'][1]
    Dark_Length = Input[0]['SpinBox'][0]
    marker_size = Input[0]['SpinBox'][1]
    Behaviour_GroupDict = DataGroup['Behaviour']['Group Dict']
    Sleep_GroupDict = DataGroup['Sleep']['Group Dict']
    DataDict, dictPlot, info = {}, {}, {}
    AllData_Behaviour, AllData_Sleep  = {}, {}
    lenBe, lenSl = 0,0
    for key1 in DataGroup['Behaviour']['Data Name']:
        try:
            lock.lockForRead()
            AllData_Behaviour[key1] = copy(Datas.takeDataset(key1))
            lenBe = max(lenBe,len(key1))
        finally:
            lock.unlock()
    for key in DataGroup['Sleep']['Data Name']:
        try:
            lock.lockForRead()
            AllData_Sleep[key] = copy(Datas.takeDataset(key))
            lenSl = max(lenSl,len(key))
        finally:
            lock.unlock()
    funcVect = np.vectorize(TimeBin_From_TimeString)
    print(('string: ', AllData_Sleep[key]['Time'][1]))
    TimeBin = Time_To_Seconds(AllData_Sleep[key]['Time'][1]) -\
        Time_To_Seconds(AllData_Sleep[key]['Time'][0])
    TimeBin_be = Time_To_Seconds(AllData_Behaviour[key1]['Time'][1]) -\
        Time_To_Seconds(AllData_Behaviour[key1]['Time'][0])    
    print(('TimeBin: ', TimeBin))
    if TimeBin != TimeBin_be:
        raise ValueError('Different time binning between sleep and behavioural data')
    lenGr = 0
    for key in list(Behaviour_GroupDict.keys()):
        lenGr = max(lenGr, len(key))
    info['Linear Discriminant Analysis'] = {}
    size = len(list(Behaviour_GroupDict.keys())) * len(list(AllData_Behaviour.keys())) *\
        len(list(AllData_Sleep.keys()))
    fit_Matrix = np.zeros(size, dtype=\
        {'names':('Sleep Data', 'Behaviour Data', 'Group',
                  'Weighted Error', 'Slope', 'Intercept'),
         'formats':('S%d'%lenSl, 'S%d'%lenBe, 'S%d'%lenGr,
                    float, float, float)})
    
    DataDict['Linear Discriminant Analysis'] = {}
    dictPlot['Linear Discriminant Analysis'] = {}
    indSub = 0
    for keySl in list(AllData_Sleep.keys()):
        for keyBe in list(AllData_Behaviour.keys()):
            Sleep_Matrix = AllData_Sleep[keySl]
            Behaviour_Matrix = AllData_Behaviour[keyBe]
            Group_Mean_Sleep,Group_Mean_Error,ldaFit,ldaScore,weights,\
            timeVect_Sleep,timeVect_Error,Classification=\
            F_LDA_GUI(Sleep_Matrix, Behaviour_Matrix, Sleep_GroupDict,
                      Behaviour_GroupDict, Sleep_Dark_Start=Sleep_Dark_Start,
                      Error_Dark_Start=Behaviour_Dark_Start,
                      DarkLen=Dark_Length, TimeBin=TimeBin)
            dataArray, ldaFitArray = LDA_ArrayCreation_GUI(Group_Mean_Error,
                                                           Group_Mean_Sleep,
                                                           ldaFit,
                                                           ldaScore,
                                                           weights,
                                                           timeVect_Sleep,
                                                           keyBe,
                                                           keySl,
                                                           Classification,
                                                           Bin=TimeBin)
            
            fit_Matrix['Sleep Data'][indSub:indSub+2] = keySl
            fit_Matrix['Behaviour Data'][indSub:indSub+2] = keyBe
            fit_Matrix['Group'][indSub:indSub+2] = ldaFitArray['Group']
            fit_Matrix['Weighted Error'][indSub:indSub+2] =\
                ldaFitArray['Weighted Error']
            fit_Matrix['Slope'][indSub:indSub+2] = ldaFitArray['Slope']
            fit_Matrix['Intercept'][indSub:indSub+2] = ldaFitArray['Intercept']
            indSub += 2
            DataDict['Linear Discriminant Analysis']['LDA_%s_vs_%s'%\
                (keyBe,keySl)] = dataArray
            info['LDA_%s_vs_%s'%(keyBe,keySl)] = {}
            info['LDA_%s_vs_%s'%(keyBe,keySl)]['Types'] = ['LDA Data',
                 'Single Subject']
            info['LDA_%s_vs_%s'%(keyBe,keySl)]['Factor'] = [0,1,2,3,4]
            for group in list(Group_Mean_Sleep.keys()):
                X = np.zeros((len(Group_Mean_Sleep[group]),2))
                X[:,0] = Group_Mean_Sleep[group]
                X[:,1] = Group_Mean_Error[group]
                LenDark = Dark_Length * 3600.0 / TimeBin
                LenLight = (24 - Dark_Length) * 3600.0 / TimeBin
                y=np.hstack((np.zeros(LenDark),np.ones(LenLight)))
                X = np.nan_to_num(X)
                y_pred = ldaFit[group].predict(X)
                tmpData = dataArray[np.where(dataArray['Group']==group)[0]]
                labelHourDark = funcVect(tmpData['Time']\
                        [np.where(tmpData['Phase'] == 'Dark')[0]],3600)
                labelHourLight = funcVect(tmpData['Time']\
                        [np.where(tmpData['Phase'] == 'Light')[0]],3600)
                x_label = keySl.split('.')[0]
                y_label = keyBe.split('.')[0]
                dictPlot['Linear Discriminant Analysis']\
                    ['LDA_%s_vs_%s_%s'%(keyBe.split('.')[0],
                                        keySl.split('.')[0],group)] =\
                    (ldaFit[group], X, y, y_pred,
                    'Linear Discriminant Analysis\n%s'%group,labelHourDark,
                    labelHourLight, x_label, 15, y_label, 15, 20, False,
                    marker_size)
    DataDict['Linear Discriminant Analysis']['LDA_Fit_Patameters'] = fit_Matrix
    info['LDA_Fit_Patameters'] = {}
    info['LDA_Fit_Patameters']['Types'] = ['LDA Parameters','Group']
    info['LDA_Fit_Patameters']['Factor'] = [0]
    return DataDict, dictPlot ,info
def Multiple_Regression_Analysis(*myinput):
    Datas      = myinput[0]
    Input      = myinput[1]
    DataGroup  = myinput[2]
    lock       = myinput[4]
    
    print('ok datas')
#    print Datas, Input, DataGroup,lock
    p_entrance = Input[0]['DoubleSpinBox'][0]
    p_exit = Input[0]['DoubleSpinBox'][1]
    label_size = Input[0]['SpinBox'][0]
    title_size = Input[0]['SpinBox'][1]
    rotation = Input[0]['SpinBox'][2]
    Behaviour_GroupDict = DataGroup['Predictor Behavior']['Group Dict']
    Sleep_GroupDict = DataGroup['Predictors Sleep']['Group Dict']
    Observation_GroupDict = DataGroup['Observation']['Group Dict']
    AllData_Behaviour, AllData_Sleep, AllData_Obs  = {}, {}, {}
    AllGroup = {}
    lenBe, lenSl = 0,0
    print('ok initializing')
    for key in DataGroup['Predictor Behavior']['Data Name']:
        try:
            lock.lockForRead()
            AllData_Behaviour[key] = copy(Datas.takeDataset(key))
            AllGroup[key] = Behaviour_GroupDict
            lenBe = max(lenBe,len(key))
        finally:
            lock.unlock()
    print('ok AllData_BEhaviour')
    for key in DataGroup['Predictors Sleep']['Data Name']:
        try:
            lock.lockForRead()
            AllData_Sleep[key] = deepcopy(Datas.takeDataset(key))
            AllGroup[key] = Sleep_GroupDict
            lenSl = max(lenSl,len(key))
        finally:
            lock.unlock()
    print('ok AllData_Sleep')
    for key in DataGroup['Observation']['Data Name']:
        try:
            lock.lockForRead()
            AllData_Obs[key] = deepcopy(Datas.takeDataset(key))
            AllGroup[key] = Observation_GroupDict
            lenSl = max(lenSl,len(key))
        finally:
            lock.unlock()
    print('ok AllData_Obs')
    lenGr = 0
    for key in list(Behaviour_GroupDict.keys()):
        lenGr = max(lenGr, len(key))
#==============================================================================
#   Ho salvato tutti i dizionari con i nomi dei dataset come chiavi e i 
#   gruppi come valori                      
#==============================================================================
    bestLagSleep, R_squared_Sleep, lagVect_sleep = find_BestLag(AllGroup,
                                                                AllData_Sleep,
                                                                AllData_Obs)
    print('ok bestLag sleep',bestLagSleep)
    bestLagCircadian, R_squared_Circadian, lagVect_circa =\
        find_BestLag(AllGroup,  AllData_Behaviour, AllData_Obs)
    print('ok bestLag circadian',bestLagCircadian)
#==============================================================================
#   Perform a step wise multiple regression
#==============================================================================
    regressionModels = multipleRegressionProcedure(AllData_Behaviour,
                                                   AllData_Sleep,
                                                   AllData_Obs,
                                                   AllGroup,
                                                   bestLagCircadian,
                                                   bestLagSleep,
                                                   p_entrance=p_entrance,
                                                   p_exit=p_exit)
    print('ok regression model')
#    print regressionModels
    dictPlot = {'Fig MRA':{}}
    dictPlot['Fig MRA']['MRA'] = (regressionModels, 'Predictor comparison',
                                   'Observation', 'Predictor sleep', label_size,
                                   title_size, rotation, None, None)
    dictPlot['Fig MRA']['R_squared_vs_lag_circadian'] =  lagVect_circa,\
        R_squared_Circadian
    dictPlot['Fig MRA']['R_squared_vs_lag_sleep'] =  lagVect_sleep,\
        R_squared_Sleep    
    dataDict = {'MRA':{}}
    dataDict['MRA']['MRA_matrix'] = build_Rsquared_Matrix(regressionModels)
    info = {}
    info['MRA_matrix'] = {}
    info['MRA_matrix']['Types'] = ['MRA info','Group']
    info['MRA_matrix']['Factor'] = [0,1,2,3]
    return dataDict, dictPlot, info
def LDA(*myInput):
    print('ENTER SWITCH LAT')
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    pairedGroups = myInput[5]
    dark_start = Input[0]['Combo'][0]
    dark_len   = Input[0]['Combo'][1]
    beh_par = Input[0]['Combo'][2]
    sleep_par   = Input[0]['Combo'][3]
    hd,hl=Hour_Light_and_Dark_GUI(dark_start,dark_len,TimeInterval=3600)
    num_col = 0
    for group in list(pairedGroups.keys()):
        num_col += len(pairedGroups[group]['Behavior'])
    dtype = {'names':('Group','Subject',beh_par,sleep_par),
             'formats':('S50','S100',float,float)}
    struct_mat = np.zeros(num_col, dtype=dtype)
    dtype = {'names':('Group','Subject','Score'),
             'formats':('S50','S100',float)}
    score_mat = np.zeros(num_col, dtype=dtype)
    dtype = {'names':('Group','Subject','Hour','Prob_Dark','Prob_Light'),
             'formats':('S50','S100','S5',float,float)}
    prob_mat = np.zeros(num_col*24, dtype=dtype)
    hour_str = []
    for h in range(24):
        hour_str += ['%d:00'%h]
    X_norm_d,struct_mat_d,y_d,lda_res_d, gauss_light_d, gauss_dark_d,line_light_d,line_dark_d, Index_for_color_d, v_ort_d = {},{},{},{},{},{},{},{},{},{}
    title_d = {}
    y_gr_d = {}
    lda_res_gr_d = {}
    gauss_light_gr_d = {}
    gauss_dark_gr_d = {}
    line_light_gr_d = {}
    line_dark_gr_d ={}
    Index_for_color_gr_d = {} 
    struct_mat_gr_d = {} 
    v_ort_gr_d = {}
    title_gr_d = {} 
    ind_row = 0
    score_per_group = {}
    for group in list(pairedGroups.keys()):
        score_per_group[group] = np.zeros((24,2))
        beh_tmp = np.zeros((24,len(pairedGroups[group]['Sleep'])))
        sleep_tmp = np.zeros((24,len(pairedGroups[group]['Sleep'])))
        i_sub = 0
        for sub_beh  in pairedGroups[group]['Behavior']:
            sub_sleep = pairedGroups[group]['Sleep'][i_sub]
            print(sub_beh,sub_sleep)
            try:
                lock.lockForRead()
                data_beh = deepcopy(Datas.takeDataset(sub_beh))
                data_sleep = deepcopy(Datas.takeDataset(sub_sleep))
                time_stamps = Datas.getTimeStamps(sub_beh)
            finally:
                lock.unlock()
            res,X_norm,Struct_mat,explained_variance,v_ort,v,y_pred,lda_res,\
            Index_for_color,y = performLDA_Analysis(data_beh, data_sleep,
                                                    time_stamps, beh_par, 
                                                    sleep_par, dark_start,dark_len)
            dailyScore_beh,dailyScore_sleep = computeDailyScore(data_beh, data_sleep, time_stamps, beh_par, sleep_par)
            sleep_tmp[:,i_sub] = dailyScore_sleep
            beh_tmp[:,i_sub] = dailyScore_beh
            i_sub += 1
            line_light,line_dark,rot_v_light,rot_v_dark = res
            struct_mat['Group'][ind_row] = group
            struct_mat['Subject'][ind_row] = sub_beh
            struct_mat[beh_par][ind_row] = Struct_mat[1,Index_for_color]
            struct_mat[sleep_par][ind_row] = Struct_mat[0,Index_for_color]
            score_mat['Group'][ind_row] = group
            score_mat['Subject'][ind_row] = sub_beh
            score_mat['Score'][ind_row] = lda_res.score(X_norm,y)
            prob_mat['Group'][ind_row*24:(ind_row+1)*24] = group
            prob_mat['Subject'][ind_row*24:(ind_row+1)*24] = sub_beh
            prob_mat['Hour'][ind_row*24:(ind_row+1)*24] = hour_str
            p = lda_res.predict_proba(X_norm)
            prob_mat['Prob_Dark'][ind_row*24:(ind_row+1)*24] = p[:,0]
            prob_mat['Prob_Light'][ind_row*24:(ind_row+1)*24] = p[:,1]
            X_norm_d[sub_beh] = X_norm
            y_d[sub_beh] = y
            lda_res_d[sub_beh] = lda_res
            gauss_light_d[sub_beh] = rot_v_light
            gauss_dark_d[sub_beh] = rot_v_dark
            line_light_d[sub_beh] = line_light
            line_dark_d[sub_beh] = line_dark
            Index_for_color_d[sub_beh] = Index_for_color
            struct_mat_d[sub_beh] = Struct_mat
            v_ort_d[sub_beh] = v_ort
            title_d[sub_beh] = sub_beh
            ind_row += 1
        score_per_group[group][:,0] = np.nanmean(beh_tmp,axis=1)
        score_per_group[group][:,1] = np.nanmean(sleep_tmp,axis=1)
        y_pred_gr,prob_pred_gr,score_list_gr,v_gr,X_norm_gr,lda_res_gr = compute_LDA(score_per_group[group],y)
        std_weights_gr,Struct_mat_gr,explained_variance_gr,v_ort_gr,Index_for_color_gr = compute_structure_matrix(y,score_per_group[group],X_norm_gr,v_gr)
        res_gr = gaussian_fit(X_norm_gr,v_gr,hd,hl)
        score_per_group[group][:,0] = X_norm_gr[:,0]
        score_per_group[group][:,1] = X_norm_gr[:,1]
        y_gr_d[group] = y
        lda_res_gr_d[group] = lda_res_gr
        gauss_light_gr_d[group] = res_gr[2]
        gauss_dark_gr_d[group] = res_gr[3]
        line_light_gr_d[group] = res_gr[0]
        line_dark_gr_d[group] = res_gr[1]
        Index_for_color_gr_d[group] = Index_for_color_gr
        struct_mat_gr_d[group] = Struct_mat_gr
        v_ort_gr_d[group] = v_ort_gr
        title_gr_d[group] = group
    dictPlot = {}
    dictPlot['Fig:LDA Results'] = {}
    dictPlot['Fig:LDA Results']['Scatter'] = X_norm_d, y_d, lda_res_d, gauss_light_d, gauss_dark_d,line_light_d,line_dark_d, Index_for_color_d, struct_mat_d, v_ort_d ,hl, hd,title_d,beh_par,sleep_par
    dictPlot['Fig:Group LDA Results'] = {}
    dictPlot['Fig:Group LDA Results']['Scatter'] = score_per_group,y_gr_d,lda_res_gr_d,gauss_light_gr_d,gauss_dark_gr_d,line_light_gr_d,line_dark_gr_d,Index_for_color_gr_d,struct_mat_gr_d,v_ort_gr_d,hl, hd,title_gr_d,beh_par,sleep_par
    DataDict = {}
    DataDict['LDA Results'] = {}
    DataDict['LDA Results']['Structure_Matrix'] = struct_mat
    DataDict['LDA Results']['LDA_Score'] = score_mat
    DataDict['LDA Results']['Classification_Probability'] = prob_mat
    info = {}
    info['Structure_Matrix'] = {}
    info['Structure_Matrix']['Types']  = ['Structure_Matrix']
    info['Structure_Matrix']['Factor'] = [0,1]
    info['LDA_Score'] = {}
    info['LDA_Score']['Types']  = ['LDA_score']
    info['LDA_Score']['Factor'] = [0,1]
    info['Classification_Probability'] = {}
    info['Classification_Probability']['Types']  = ['Classification_Probability']
    info['Classification_Probability']['Factor'] = [0,1,2]
    return DataDict,dictPlot,info
def Switch_Latency(*myInput):
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
    group_list = list(DataGroup.keys())
    group_list.sort()
    long_side_dict = {}
    k = 0
    for gr in group_list:
        long_side_dict[gr] = Long_Side
        k += 1
    Mouse_Name = np.hstack(list(DataGroup.values()))
    lenName = 0
    lenGroupName = 0
    for key in list(DataGroup.keys()):
        lenGroupName = max(lenGroupName,len(key))
        for name in DataGroup[key]:
            lenName = max(lenName,len(name))
    Mouse_Grouped = DataGroup
    AllData = OrderedDict()
    TimeStamps_Dict = {}
    DataDict = {}
    DataDict['Group Switch Latency'] = {}
    long_side_sub = {}
    isMEDDict = {}
    print('CREATING TIMESTAMPS DICT')
    for gr in list(Mouse_Grouped.keys()):
        for dataName in Mouse_Grouped[gr]:
            try:
                lock.lockForRead()
                AllData[dataName] = deepcopy(Datas.takeDataset(dataName))
                isMEDDict[dataName] = 'MED_SW' in Datas.dataType(dataName)
                if Datas.getTimeStamps(dataName):
                    TimeStamps_Dict[dataName] = Datas.getTimeStamps(dataName)
                else:
                    TimeStamps_Dict[dataName] = TimeStamps
            finally:
                lock.unlock()
    for gr in list(Mouse_Grouped.keys()):
        for dataName in Mouse_Grouped[gr]:
            long_side_sub[dataName] = long_side_dict[gr]
    print('\n\nGR SWITCH LAT\n\n')          
    table,left,right,Record_Switch,HSSwitch = F_New_Gr_Switch_Latency_GUI(AllData,TimeStamps_Dict,Mouse_Name,ts=ts,tl=tl,scale=1,Tend=Tend,Long_Side=long_side_sub,type_tr=type_tr,isMEDDict=isMEDDict)
    for name in list(Record_Switch.keys()):
        if Record_Switch[name].shape[0] < 10:
            Record_Switch.pop(name)
            HSSwitch.pop(name)
            right.pop(name)
            left.pop(name)
            table.pop(name)
            AllData.pop(name)
            for gr in list(Mouse_Grouped.keys()):
                if name in Mouse_Grouped[gr]:
                    Mouse_Grouped[gr].remove(name)
#    prev_groups = Mouse_Grouped.keys()
#    for gr in prev_groups:
#        if not len(Mouse_Grouped[gr]):
#            s = Mouse_Grouped.pop(gr)
    func = lambda h : h.hour
    v_func = np.vectorize(func)
    tmp = {}
    for name in list(Record_Switch.keys()):
        tmp[name] = v_func(HSSwitch[name])
    HSSwitch = tmp
    Hour_Dark,Hour_Light=Hour_Light_and_Dark_GUI(Dark_start,Dark_length)
    Best_Model,Pdf,Cdf,EmCdf=F_Gr_Fit_GMM_GUI(Record_Switch,Mouse_Grouped,n_gauss=1)
    Median,Mean,Std=Subj_Median_Mean_Std_GUI(Record_Switch,HSSwitch)
    Hour_label = TimeUnit_to_Hours_GUI(np.hstack((Hour_Dark,Hour_Light)),3600)
    DataLen    = len(Hour_label) * len(list(Record_Switch.keys()))
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
    
    tmp_msgr = Cdf.__len__()
    DataDict['Group Switch Latency']['CDF'] = np.zeros(tmp_msgr*(10**4), dtype = {'names':('Group','Subject','X','Y'),'formats':('|S%d'%lenGroupName,'|S%d'%lenName,float,float)})
                   
    DataDict['Group Switch Latency']['Group Switch Latency']['Time'] = list(Hour_label) * len(list(Record_Switch.keys()))
    ind = 0
    idx_cdf = 0
    for key in list(Mouse_Grouped.keys()):
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
                
            DataDict['Group Switch Latency']['CDF']['Group'][idx_cdf:idx_cdf + 10**4] = [key]
            DataDict['Group Switch Latency']['CDF']['Subject'][idx_cdf:idx_cdf + 10**4] = [name]
            DataDict['Group Switch Latency']['CDF']['X'][idx_cdf:idx_cdf + 10**4] = Cdf[name]['x']
            DataDict['Group Switch Latency']['CDF']['Y'][idx_cdf:idx_cdf + 10**4] = Cdf[name]['y']
            
            idx_cdf += 10**4
            ind += len(Hour_label)
    
    DataDict['Group Switch Latency']['Expected Gain'] = std_Exp_Gain
        
    Gr_Mean,Gr_Std=Gr_Mean_Std_GUI(Median,Mouse_Grouped)
    Group_Name = list(Mouse_Grouped.keys())
    dictPlot = {}
    dictPlot['Fig:Group Switch Latency'] = {}
    dictPlot['Fig:Group Switch Latency']['Record switch time'] = Gr_Mean,Hour_Light,Hour_Dark,\
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
    info['CDF'] = {}
    info['CDF']['Types']  = ['Group', 'Switch Latency']
    info['CDF']['Factor'] = [0,1]

    return DataDict,dictPlot,info
def delta_rebound(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    TimeBin_Sec = Input[0]['Combo'][0]
    normCol = Input[0]['Combo'][1]
    stage = Input[0]['Combo'][2]
    
    phase_dict = Input[0]['PhaseSel'][0] # dict containing matrix for phase sel
    subjects = list(phase_dict.keys())
    duration_sec = np.zeros(len(subjects))
    idx = 0
    for name in subjects:
        phase_dict[name] = phase_dict[name][phase_dict[name]['isChecked']== True]
        duration = phase_dict[name][-1]['dayEnd'] - phase_dict[name][0]['dayStart']
        duration_sec[idx] = duration.total_seconds()
        idx += 1
    raw_rebound = np.zeros(0,dtype={'names':('Subject','Group','Phase','Time0','Time1','Power'),
                           'formats':('S100','S100','S2',datetime.datetime,datetime.datetime,float)})
    norm_rebound = np.zeros(0,dtype={'names':('Subject','Group','Phase','Time0','Time1','Power'),
                           'formats':('S100','S100','S2',datetime.datetime,datetime.datetime,float)})
    norm_fact = np.zeros(len(subjects),dtype={'names':('Subject','Group','Norm Factor'),
                         'formats':('S100','S100',datetime.datetime,datetime.datetime,float)})
    delta_to_Sec = lambda t : t.total_seconds()
    vec_delta_to_sec = np.vectorize(delta_to_Sec)
    k_sub = 0
    for gen in list(DataGroup.keys()):
        for name in DataGroup[gen]: 
            try:
                lock.lockForRead()
                sleep_data = deepcopy(Datas.takeDataset(name))
                if 'EEG Full Power Spectrum' in Datas.dataType(name):
                    sleep_data = sleep_data.Return_FreqBandData()
            finally:
                lock.unlock()
            phase_mat = phase_dict[name]
            times = sleep_data.Timestamp[:]
            power = sleep_data.PowerSp[:,:]
            idx_star = (sleep_data.Stage == 'W*') | (sleep_data.Stage == 'NR*') | (sleep_data.Stage == 'R*' )
            power[idx_star,:] = np.nan
            if stage != 'All':
                idx_stage = sleep_data.Stage != stage
                power[idx_stage,:] = np.nan
            idx_nm = (times >= phase_mat[0]['normStart']) * (times <= phase_mat[0]['normEnd'])
            nm_power = power[idx_nm,:]
            norm_fact['Norm Factor'][k_sub] = np.nanmean(nm_power[:,normCol])
            norm_fact['Subject'][k_sub] = name
            norm_fact['Group'][k_sub] = gen
            for phase in phase_mat['phase']:
                d0 = phase_mat['dayStart'][np.where(phase_mat['phase']==phase)[0][0]]
                d1 = phase_mat['dayEnd'][np.where(phase_mat['phase']==phase)[0][0]]
                idx_ph  = (times >= d0) * (times <= d1)
                ph_times = times[idx_ph]
                ph_power = power[idx_ph,normCol]
                secs = vec_delta_to_sec(ph_times - ph_times[0].replace(second=0,minute=0))
                tsec = 0
                pwr = []
                tms0 = []
                tms1 = []
                while tsec*TimeBin_Sec < secs[-1]:
                   idx_bin = (secs >= tsec*TimeBin_Sec) * (secs < (tsec+1)*TimeBin_Sec)
                   pwr += [np.nanmean(ph_power[idx_bin])]
                   tms0 += [ph_times[np.where(idx_bin)[0][0]]]
                   tms1 += [ph_times[np.where(idx_bin)[0][-1]]]
                   tsec += 1
                tmp_raw = np.zeros(len(pwr),dtype={'names':('Subject','Group','Phase','Time0','Time1','Power'),
                           'formats':('S100','S100','S2',datetime.datetime,datetime.datetime,float)})
                tmp_raw['Subject'] = name
                tmp_raw['Group'] = gen
                tmp_raw['Phase'] = phase
                tmp_raw['Time0'] = tms0
                tmp_raw['Time1'] = tms1
                tmp_raw['Power'] = pwr
                raw_rebound = np.hstack((raw_rebound,tmp_raw))
                tmp_raw['Power'] = tmp_raw['Power'] / norm_fact['Norm Factor'][k_sub]
                norm_rebound = np.hstack((norm_rebound,tmp_raw))
            k_sub += 1
    if normCol == 0:
        band = 'Delta'
    elif normCol == 1:
        band = 'Theta'
    DataDict = {}
    DataDict['Power Rebound'] = {}
    DataDict['Power Rebound']['Raw %s Rebound'%band] = raw_rebound
    DataDict['Power Rebound']['Norm %s Rebound'%band] = norm_rebound
    DataDict['Power Rebound']['Norm Factor'] = norm_fact
    dictPlot = {}
    dictPlot['Fig:Rebound'] = {}
    dictPlot['Fig:Rebound']['%s Time Course'%band] = norm_rebound
    info = {}
    info['Raw %s Rebound'%band] = {}
    info['Raw %s Rebound'%band]['Types']  = ['Raw %s Rebound'%band]
    info['Norm %s Rebound'%band] = {}
    info['Norm %s Rebound'%band]['Types']  = ['Norm %s Rebound'%band]
    info['Norm Factor'] = {}
    info['Norm Factor']['Types']  = ['%s Norm Factor'%band]
    return DataDict,dictPlot,info
