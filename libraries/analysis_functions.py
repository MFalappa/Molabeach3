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

#import datetime
import numpy as np
from copy import copy
from auxiliary_functions import (powerDensity_function)



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
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            if first:
                typesFr = np.array(np.round(Fr,decimals=2),dtype=np.str_)
                types = np.hstack((['Group','Subject'],typesFr))
                df_res = np.zeros((count_sub,),dtype={'names':types,
                                  'formats':(np.str_,np.str_,)+(float,)*Fr.shape[0]})
            Power_Wake[IndexGroup[key][name],:]
#                wake = np.vstack((Fr,Power_Wake[IndexGroup[key][name],:]))
#                sbj = np.vstack(('Subject',name))
#                grs = np.vstack(('Groups',key))
#                first = False
#            else:
#                wake = np.vstack((wake,Power_Wake[IndexGroup[key][name],:]))
#                sbj = np.vstack((sbj,name))
#                grs = np.vstack((grs,key))
                
    DataDict['Power Density Wake'] = np.hstack((grs,sbj,wake))
    
    first = True
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            if first:
                nrem = np.vstack((Fr,Power_NRem[IndexGroup[key][name],:]))
                sbj = np.vstack(('Subject',name))
                grs = np.vstack(('Groups',key))
                first = False
            else:
                nrem = np.vstack((nrem,Power_NRem[IndexGroup[key][name],:]))
                sbj = np.vstack((sbj,name))
                grs = np.vstack((grs,key))
                
    DataDict['Power Density NRem'] = np.hstack((grs,sbj,nrem))
    
    first = True
    for key in list(DataGroup.keys()):
        for name in DataGroup[key]:
            if first:
                rem = np.vstack((Fr,Power_Rem[IndexGroup[key][name],:]))
                sbj = np.vstack(('Subject',name))
                grs = np.vstack(('Groups',key))
                first = False
            else:
                rem = np.vstack((rem,Power_Rem[IndexGroup[key][name],:]))
                sbj = np.vstack((sbj,name))
                grs = np.vstack((grs,key))
                
    DataDict['Power Density Rem'] = np.hstack((grs,sbj,rem))

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

#
#def Sleep_Time_Course(*myInput):
#    DataDict, dictPlot, datainfo = {},{},{}
#    return DataDict,dictPlot, datainfo
#
#
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
#def Linear_Discriminant_Analysis():
#    return 4
#def Multiple_Regression_Analysis():
#    return 4
#def LDA():
#    return 4
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


    
