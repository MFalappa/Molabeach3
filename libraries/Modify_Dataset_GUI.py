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

import numpy as np
import matplotlib.pyplot as plt
import bisect
import os
from copy import copy,deepcopy
import datetime
import scipy.stats as sts
from PyQt5.QtCore import QObject, pyqtSignal
import warnings
def intConv(x):
    return int(x)

def dateConvertion(dateString):
    try:
        date = datetime.datetime.strptime(dateString,'%m/%d/%Y %H:%M:%S')
        return date
    except:
        pass
    vectIntConv = np.vectorize(intConv)
    if '/' in dateString:
        CHAR = '/'
        sign = -1
    else:
        CHAR = '-'
        sign = 1
    marker_option = ['T',' ']
    for c in marker_option:
        i = dateString.find(c)
        if  i >= 0:
            split_i = i
    Date = vectIntConv(dateString[:split_i].split(CHAR))[::sign]
    
    if Date[0] < 100:
        Date[0] = 2000 + Date[0]
    Time = vectIntConv(dateString[split_i+1:].split(':'))
    DateTime = np.hstack((Date, Time))
    return datetime.datetime(*DateTime)

def vectDateConvertion(List):
    func = np.vectorize(dateConvertion)
    return func(List)
    
def Time_Details_GUI(Y,TimeStamps,*scale,**kwargs):
    """
    Funcion targets: This funcion calculates the initial
                     and the ending time of NP activity (starting from midnight
                     of the day the analisis begun).
                     
    Input ( 
             Y=Dataset, nx2 array: first column time stamps, second column event codes
             scale=scalar, scale in case time stamps are not in sec. (default scale=1)
             Start=sec, to specify a different start experiment, useful if you
             cut the dataset at a certain hour.
            )
            
    Output (
            Start_exp = start time of the experiment (seconds form midnight before the analisis begins)
            Start_time = first NP time (seconds from midnight of the first day of experiment)
            End_time = last NP time (seconds from midnight of the first day of experiment)       
            )
    """

    if len(scale)!=1:
        scale=1
    else:
        scale=scale[0]
    
    if  'Start_exp' in kwargs:
        Start_exp=kwargs['Start_exp']
    else:
        Start_exp=F_Start_exp_GUI(Y,TimeStamps)
    
#   first and last NP activity  (second from midnight)
    
    if len(np.where(Y['Action']==TimeStamps['Left NP In'])[0])!=0:
        
        m1=Y['Time'][np.where(Y['Action']==TimeStamps['Left NP In'])[0][0]]
        M1=Y['Time'][np.where(Y['Action']==TimeStamps['Left NP In'])[0][-1]]
        
    else:
        m1,M1=-1,-1
        
    if len(np.where(Y['Action']==TimeStamps['Left NP Out'])[0])!=0:
        m2=Y['Time'][np.where(Y['Action']==TimeStamps['Left NP Out'])[0][0]]
        M2=Y['Time'][np.where(Y['Action']==TimeStamps['Left NP Out'])[0][-1]]
    else:
        m2,M2=-1,-1
        
    if len(np.where(Y['Action']==TimeStamps['Center NP In'])[0])!=0:
        m3=Y['Time'][np.where(Y['Action']==TimeStamps['Center NP In'])[0][0]]
        M3=Y['Time'][np.where(Y['Action']==TimeStamps['Center NP In'])[0][-1]]
    else:
        m3,M3=-1,-1
        
    if len(np.where(Y['Action']==TimeStamps['Center NP Out'])[0])!=0:
        m4=Y['Time'][np.where(Y['Action']==TimeStamps['Center NP Out'])[0][0]]
        M4=Y['Time'][np.where(Y['Action']==TimeStamps['Center NP Out'])[0][-1]]
    else:
        m4,M4=-1,-1
        
    if len(np.where(Y['Action']==TimeStamps['Right NP In'])[0])!=0:
        m5=Y['Time'][np.where(Y['Action']==TimeStamps['Right NP In'])[0][0]]
        M5=Y['Time'][np.where(Y['Action']==TimeStamps['Right NP In'])[0][-1]]
    else:
        m5,M5=-1,-1
        
    if len(np.where(Y['Action']==TimeStamps['Right NP Out'])[0])!=0:
        m6=Y['Time'][np.where(Y['Action']==TimeStamps['Right NP Out'])[0][0]]
        M6=Y['Time'][np.where(Y['Action']==TimeStamps['Right NP Out'])[0][-1]]
    else:
        m6,M6=-1,-1
    
    m = np.array([m1,m2,m3,m4,m5,m6])
    Ind = np.where(m!=-1)[0]
    Start_Time=Start_exp+min(m[Ind])/scale
    End_Time=Start_exp+max(M1,M2,M3,M4,M5,M6)/scale



    return(Start_exp,Start_Time,End_Time)
    
def Rescale_Time_GUI(Y,TimeStamps,scale=1000,header=12,footer=3):
    """
    Function Targets:       This function rescale the time stamps. 
                            (our time stamps usually are in millisec).
                            
    Input:                  -scale = the rescaling factor
    
    Output:                 -Y = nx2 matrix (dictionary) containing the rescaled
                            dataset
    """
#   Changing time unit from millisec to sec.
    if len(np.where(Y['Action']==TimeStamps['End Month'])[0])>0:
        Y['Time'][header:-footer]=Y['Time'][header:-footer]/scale
    else:
        Y['Time'][header:]=Y['Time'][header:]/scale
    return(Y)
    
def F_Rescale_A_Dataset(Dataset,TimeColumLabel,scale,header=12,footer=3):
    """
    Function Target:
    ----------------
        Rescale a generic dataset given the time column label, header and footer.
        Let footer=-1 if no footer is present
    Input:
    ------
        Dataset
            nxm dataset (numpy structured array)
        TimeColumLabel 
            string, label of the time column
        Scale
            float, the scaling factor
        header/footer
            int, length of header/footer
    Output:
    -------
        Dataset
            mxn dateset with times rescaled by 1/scale
        
    """
    if footer==-1:
        Dataset[TimeColumLabel][header:]=Dataset[TimeColumLabel][header:]/scale
    else:
        Dataset[TimeColumLabel][header:-1*footer]=Dataset[TimeColumLabel][header:-1*footer]/scale
    return Dataset
    
def Positive_Times_GUI(Y):
    """
    Function Targets:       This function keeps only positive time stamps.
                            
    Input:                  -Y = nx2 matrix (dictionary) containing original
                            dataset
    
    Output:                 -Y = nx2 matrix (dictionary) containing positive time stamps
    
    """
    Index=np.where(Y['Time']>=0)[0]
    
    New_Y=np.array(np.zeros(len(Index),dtype={'names':('Time','Action'),'formats':('f8','f8')}))
    New_Y['Time']=Y['Time'][Index]
    New_Y['Action']=Y['Action'][Index]

                
    return(New_Y)

def F_Import_GUI(Mouse_Name,Exp_Name,Path_Exp,footerLen=4):
    Datas={}
    
    for i in np.arange(len(Mouse_Name)):
        This_Path=Path_Exp+Exp_Name[i]
        delim = DetectDelimiter_GUI(This_Path)
        try:
            Datas[Mouse_Name[i]]= np.loadtxt(This_Path,delimiter=delim,
                dtype={'names':('Time','Action'),'formats':('f8','f8')})
        except ValueError:
            Datas[Mouse_Name[i]]= np.genfromtxt(This_Path,delimiter=delim,
                                  names=True,skip_footer=footerLen)
        
    return(Datas)
    
def F_Start_exp_GUI(Y,TimeStamps):
    """
    Function Targets:               This function calculates the start exp time
    
    Input:                          -Y=nx2 matrix, dataset
                                    -scale=scalar, scale in case time stamps are not in sec.
    
    Output:                         -Start_exp=start time of the experiment (seconds form midnight before the analisis begins)
    """
#   Here we save huor-min-sec of the beginning of our experiment
    
    second_start_exp = Y['Time'][np.where(Y['Action']==TimeStamps['Start Second'])[0]];
    minute_start_exp = Y['Time'][np.where(Y['Action']==TimeStamps['Start Minute'])[0]];
    hour_start_exp = Y['Time'][np.where(Y['Action']==TimeStamps['Start Hour'])[0]];
#   We assume as initial time t_0 midnight of the day the experiment starts.
#   Here we save how many sec from t_0 passed until we start the experiment. 

    Start_exp = second_start_exp+minute_start_exp*60+hour_start_exp*3600
    
    return(Start_exp)

def Cut_Dataset_GUI(Data,Start,End,TimeStamps,scale=1,DayOrSec='Day',header=12,footer=3):
    """
    Function Target:        This function cut the dataset keeping only datas from
                            Start to End .
                            
    Input:                  -Data=nx2 matrix, dataset
                            -Start=scalar, day/second from the exp start
                            from which we'll be keeping the data
                            -End=scalar, last day/second for wich we keeps the data
                            -scale=scalar, to cut dataset with different time scale
                            -DayOrSec=string, specifies if Start and end are seconds
                            or days
                            
    Output:                 -Y=nx2 matrix, dataset with only Day_end - Day_start
                            days of data recorded, from Day_start to Day_end.
                            The starting hour, minute and second are also updated
                            according to the starting hour choosen
                            
    """
    if DayOrSec=='Day':
        Sec_start=3600*24*scale*Start
        Sec_end=3600*24*scale*End
        StartDayToSum = Start
        
    elif DayOrSec=='Sec':
        Sec_start=Start
        Sec_end=End
        StartDayToSum = Sec_start//(3600*24)
        
        
    
    OldStartMonth=int(Data['Time'][np.where(Data['Action']==TimeStamps['Start Month'])[0][0]])
    OldStartDay=int(Data['Time'][np.where(Data['Action']==TimeStamps['Start Day'])[0][0]])
    OldStartYear = int(Data['Time'][np.where(Data['Action']==TimeStamps['Start Year'])[0][0]])
        
    NewStartDate=summing_day_GUI(OldStartMonth,OldStartDay,OldStartYear,StartDayToSum)
    
    
    Start_exp=F_Start_exp_GUI(Data,TimeStamps)
    

    Temp=Data.copy()
#    
#    Temp=Temp[:][Index]
#    
#    Index=np.where(Temp['Action']<=37)[0]
    Temp=Temp[:][header:-footer]
    
    Temp['Time']=Temp['Time']+Start_exp
    Index=np.where(Temp['Time']>=Sec_start)[0]
    
    try:
        OnSet=np.where(Temp['Action'][Index]==TimeStamps['Center Light On'])[0][0]        
        #OffSet=np.where(Temp['Action'][Index]==TimeStamps['Start Intertrial Interval'])[0][0]
        OffSet=np.where(Temp['Action'][Index]==TimeStamps['End Intertrial Interval'])[0][0]
        if OffSet<OnSet:
            Index=Index[OnSet:]
            
    except IndexError:
        pass
    
    Temp=Temp[:][Index]
    
    Index=np.where(Temp['Time']<=Sec_end)[0]
    
    try:
        OnSet=np.where(Temp['Action'][Index]==TimeStamps['Center Light On'])[0][-1]
        #OffSet=np.where(Temp['Action'][Index]==TimeStamps['Start Intertrial Interval'])[0][-1]
        OffSet=np.where(Temp['Action'][Index]==TimeStamps['End Intertrial Interval'])[0][-1]
        if OffSet<OnSet:
            Index=Index[:OffSet+1]
            
    except IndexError:
        pass
    
    
    Temp=Temp[:][Index]
    
    
    
#   Seconds from midnight of the new start experiment that will be the second we
#   we choose since when we cut the dataset   
    
    New_Start_exp = Sec_start -3600*24*(Sec_start//(3600*24))
    
    New_Hour = (New_Start_exp//3600)%24
    New_Minute = (New_Start_exp//60)%60
    New_Second = (New_Start_exp)%60
    
    Temp['Time']=Temp['Time']-Sec_start
    
    

    Y=np.hstack((Data[:][:header],Temp))
    
    Y['Time'][np.where(Y['Action']==TimeStamps['Start Month'])[0][0]]=NewStartDate[0]
    Y['Time'][np.where(Y['Action']==TimeStamps['Start Day'])[0][0]]=NewStartDate[1]
    Y['Time'][np.where(Y['Action']==TimeStamps['Start Year'])[0][0]]=NewStartDate[2]
    Y['Time'][np.where(Y['Action']==TimeStamps['Start Hour'])[0]]=New_Hour
    Y['Time'][np.where(Y['Action']==TimeStamps['Start Minute'])[0]]=New_Minute
    Y['Time'][np.where(Y['Action']==TimeStamps['Start Second'])[0]]=New_Second
    
    End_Time=Time_Details_GUI(Y,TimeStamps)[2]
    Y=Terminate_Dataset_GUI(Y,End_Time,TimeStamps)
    
    return(Y)
    
def Select_Interval_GUI(Data,Start_second,End_second,TimeStamps,InOrOut='In',scale=1,header=12,footer=3):
    """
    Function Target:        This function cut the dataset keeping only 
                            time stamps relative to a specifyed second interval.
                            It will not record uncomplete trials
    Input:                  -Data=n x 2 dataset RESCALED IN SECONDS
                            -Start_second=scalar, first second of the day we keep
                            -End_second=scalar, ending second of the day we keep
                            -InOrOut=string, to specify if you want to take value inside or
                            outside the interval

    Output:                 -Data=n' x 2 cutted dataset
    """
    Start_exp,Start_Time,End_Time=Time_Details_GUI(Data,TimeStamps)
    if Data['Action'][-footer]==TimeStamps['End Month']:
        Temp=np.array(Data[header:-footer]) 
    else:
        Temp=np.array(Data[header:]) 
        
    N_Day = (End_Time )//(3600*24)#- Start_exp)//(3600*24)
    
    Index = []
    Temp['Time']=Temp['Time']+Start_exp
    for day in range(N_Day+1):
        
        if InOrOut=='In':
            TmpIndex=np.where(Temp['Time']>=Start_second*scale+day*3600*24)[0]
            try:
                OnSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['Center Light On'])[0][0]
                OffSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['End Intertrial Interval'])[0][0]
                if OffSet<OnSet:
                    TmpIndex=TmpIndex[OnSet:]
            
            except IndexError:
                OnSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['Center Light On'])[0]
                OffSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['End Intertrial Interval'])[0]
                if len(OnSet)==0 and len(OffSet)==0:
                    pass
                elif len(OnSet)==0:
                    TmpIndex=TmpIndex[OffSet[0]+1:]
                elif len(OffSet)==0:
                    TmpIndex=TmpIndex[:OnSet[0]]
                print('Exception Raised (IndexError)')
                pass
            
            TmpIndex=TmpIndex[np.where(Temp['Time'][TmpIndex]<=End_second*scale+(day)*3600*24)[0]]
            try:
                OnSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['Center Light On'])[0][-1]
                OffSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['End Intertrial Interval'])[0][-1]
                if OffSet<OnSet:
                    TmpIndex=TmpIndex[:OffSet+1]
            
            except IndexError:
                OnSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['Center Light On'])[0]
                OffSet=np.where(Temp['Action'][TmpIndex]==TimeStamps['End Intertrial Interval'])[0]
                if len(OnSet)==0 and len(OffSet)==0:
                    pass
                elif len(OnSet)==0:
                    TmpIndex=TmpIndex[OffSet[0]+1:]
                elif len(OffSet)==0:
                    TmpIndex=TmpIndex[:OnSet[0]]
                print('Exception Raised (IndexError)')
                pass
                
            
            
        elif InOrOut=='Out':
            TmpIndex0 = np.where(Temp['Time']>=day*3600*24)[0]
            try:
                OnSet=np.where(Temp['Action'][TmpIndex0]==TimeStamps['Center Light On'])[0][0]
                OffSet=np.where(Temp['Action'][TmpIndex0]==TimeStamps['End Intertrial Interval'])[0][0]
                if OffSet<OnSet:
                    TmpIndex0=TmpIndex0[OnSet:]
            
            except IndexError:
                print('Exception Raised (IndexError)')
                pass
            
            TmpIndex0 = TmpIndex0[np.where(Temp['Time'][TmpIndex0]<Start_second*scale+day*3600*24)[0]]
            try:
                OnSet=np.where(Temp['Action'][TmpIndex0]==TimeStamps['Center Light On'])[0][-1]
                OffSet=np.where(Temp['Action'][TmpIndex0]==TimeStamps['End Intertrial Interval'])[0][-1]
                if OffSet<OnSet:
                    TmpIndex0=TmpIndex0[:OffSet+1]
            
            except IndexError:
                OnSet=np.where(Temp['Action'][TmpIndex0]==TimeStamps['Center Light On'])[0]
                OffSet=np.where(Temp['Action'][TmpIndex0]==TimeStamps['End Intertrial Interval'])[0]
                if len(OnSet)==0 and len(OffSet)==0:
                    pass
                elif len(OnSet)==0:
                    TmpIndex0=TmpIndex0[OffSet[0]+1:]
                elif len(OffSet)==0:
                    TmpIndex0=TmpIndex0[:OnSet[0]]
                print('Exception Raised (IndexError)')
                pass
                
            TmpIndex1 = np.where(Temp['Time']<(day+1)*3600*24)[0]
            try:
                OnSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['Center Light On'])[0][-1]
                OffSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['End Intertrial Interval'])[0][-1]
                if OffSet<OnSet:
                    TmpIndex1=TmpIndex1[:OffSet+1]
            
            except IndexError:
                OnSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['Center Light On'])[0]
                OffSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['End Intertrial Interval'])[0]
                if len(OnSet)==0 and len(OffSet)==0:
                    pass
                elif len(OnSet)==0:
                    TmpIndex1=TmpIndex1[OffSet[0]+1:]
                elif len(OffSet)==0:
                    TmpIndex1=TmpIndex1[:OnSet[0]]
                print('Exception Raised (IndexError)')
                pass
            
            TmpIndex1 = TmpIndex1[np.where(Temp['Time'][TmpIndex1]>End_second*scale+day*3600*24)[0]]
            try:
                OnSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['Center Light On'])[0][0]
                OffSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['End Intertrial Interval'])[0][0]
                if OffSet<OnSet:
                    TmpIndex1=TmpIndex1[OnSet:]
            
            except IndexError:
                
                OnSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['Center Light On'])[0]
                OffSet=np.where(Temp['Action'][TmpIndex1]==TimeStamps['End Intertrial Interval'])[0]
                if len(OnSet)==0 and len(OffSet)==0:
                    pass
                elif len(OnSet)==0:
                    TmpIndex1=TmpIndex1[OffSet[0]+1:]
                elif len(OffSet)==0:
                    TmpIndex1=TmpIndex1[:OnSet[0]]
                print('Exception Raised (IndexError)')
                pass
            
            TmpIndex = np.hstack((TmpIndex0,TmpIndex1))
            
        Index = np.hstack((Index,TmpIndex))
    Index=np.array(Index,dtype=int)                                                    
                 
    if Data['Action'][-footer]==6:
        Data=np.hstack((Data[:][:header],Data[header:-footer][Index],Data[:][-footer:]))
    else:
        
        Data=np.hstack((Data[:][:header],Data[header:][Index]))
        End_Time=Time_Details_GUI(Data,TimeStamps)[2]
        Data=Terminate_Dataset_GUI(Data,End_Time,TimeStamps)
    
    return(Data) 
    

    
def Select_Interval_Gr_GUI(Datas,Start_second,End_second,TimeStamps,scale=1000):
    for name in list(Datas.keys()):
        Datas[name]=Select_Interval_GUI(Datas,Start_second,End_second,TimeStamps,scale=scale)
    return(Datas)
    
def F_Gr_Rescale_Time_GUI(Datas,TimeStamps,scale):
    Y={}
    for name in list(Datas.keys()):
        Y[name]=Rescale_Time_GUI(Datas[name],TimeStamps,scale)
    return(Y)
    
def F_savefig_GUI(fig,path,filename,Format):
    figname=path+filename+Format
    plt.savefig(figname)
    return()
    
def F_Grouping_Dataset_GUI(Datas,Group_Name,Group_Numerosity,Mouse_Name):
    """
    Function Target:    This function returned Dataset of mice in specified 
                        groups as a dictionary.
                        
    Input:              -Datas=dictionary, keys=mouse names, Datas[name]= dataset 
                        of all mice not grouped
                        -Group_Name=list, contains the name of the groups
                        -Group_Numerosity=list/np array of integer, contains each
                        group numerosity. The sum of this array should be equal to
                        the number of mice, the len of this array must be equal
                        to the number of groups
                        -Mouse_Name=list, mouse names
                        
    Output:             -NewDatas=dictionary,keys=group name.
                            -NewDatas[name]=dictionary, keys=mouse name
                                -NewDatas[gr name][mouse name]=datasets  divided per group
                                
    EXAMPLE: If Group_Numerosity=[4,5] there must be 2 groups and the first
    four mice in Mouse_Name are assigned to the first  group and the next five
    to the second. If len(Mouse_Name)>9 the last mice won't be considered.
                        
    """
    New_Datas={}

    Number_of_Groups=len(Group_Numerosity)
    for i in range(Number_of_Groups):
        New_Datas[Group_Name[i]]={}

        if i==0:
            Ind=0
        else:
            Ind=sum(Group_Numerosity[:i])
        for j in np.arange(Group_Numerosity[i]):
            New_Datas[Group_Name[i]][Mouse_Name[Ind+j]]=Datas[Mouse_Name[Ind+j]]
           
    return(New_Datas)

def F_Grouping_Names_GUI(Group_Name,Group_Numerosity,Mouse_Name):
    """
    Function Target:    This function returned Dataset of mice in specified 
                        groups as a dictionary.
                        
    Input:              -Datas=dictionary, keys=mouse names, Datas[name]= something not grouped
                        -Group_Name=list, contains the name of the groups
                        -Group_Numerosity=list/np array of integer, contains each
                        group numerosity. The sum of this array should be equal to
                        the number of mice, the len of this array must be equal
                        to the number of groups
                        -Mouse_Name=list, mouse names
                        
    Output:             -Mouse_Grouped=dictionary,keys=group name.
                            -Mouse_Grouped[name]=dictionary, keys=mouse name
                                -Mouse_Grouped[name][mouse name]=list of names divided per group
                                
    EXAMPLE: If Group_Numerosity=[4,5] there must be 2 groups and the first
    four mice in Mouse_Name are assigned to the first  group and the next five
    to the second. If len(Mouse_Name)>9 the last mice won't be considered.
                        
    """
    Grouped_Mice={}
    Number_of_Groups=len(Group_Numerosity)
    for i in range(Number_of_Groups):
        Grouped_Mice[Group_Name[i]]=[]

        if i==0:
            Ind=0
        else:
            Ind=sum(Group_Numerosity[:i])
        for j in np.arange(Group_Numerosity[i]):
            Grouped_Mice[Group_Name[i]]=Grouped_Mice[Group_Name[i]]+[Mouse_Name[Ind+j]]
           
    return(Grouped_Mice)
    
def addDays(dateTime, daynum=0):
    return dateTime + datetime.timedelta(days=daynum)
    
vectAddDays = np.vectorize(addDays)

def Hour_Light_and_Dark_GUI(Dark_start,Len_Dark,TimeInterval=3600):
    """
    Function Target:    This Function calculate hour light and dark if you 
                        specify dark start hour and the number of dark hour.
                        
    Input:              -Dark_Start=scalar, hour of thr day in which dark phase
                        starts
                        -Len_Dark=scalar,length of dark phase in hours
                        -TimeInterval=interval of time, in second. must divide 3600
                        
    Output:             -Vector contained ordered TimeInterval light and dark,if TimeInterval=3600
                        Vector elements are hours 
    """
    if 3600.0%TimeInterval!=0:
        raise ValueError('TimeInterval must divide 3600')
    NumInterval=(3600*24)//TimeInterval
    Len_Light_Interval=NumInterval-Len_Dark*(3600//TimeInterval)
    Len_Dark_Interval=Len_Dark*(3600//TimeInterval)
    Dark_start_Interval=Dark_start*(3600//TimeInterval)
    Hour_Dark=np.arange(Dark_start_Interval,Dark_start_Interval+Len_Dark_Interval)%(24*(3600//TimeInterval))
    Hour_Light=np.arange(Dark_start_Interval+Len_Dark_Interval,Dark_start_Interval+Len_Dark_Interval+Len_Light_Interval)%(24*(3600//TimeInterval))
    return(Hour_Dark,Hour_Light)

def MultipleHour_Light_and_Dark(Dark_start,Len_Dark,TimeInterval=7200):
    if Len_Dark % (3600*24/TimeInterval) != 0 and (24-Len_Dark) % (3600*24/TimeInterval) != 0:
        warnings.warn('One of the time point will contain both light and dark phase', UserWarning)
    
    daybins = (24*3600)//TimeInterval    
    dark_dur = (Len_Dark*3600)//TimeInterval    
    dark_hour = np.arange((Dark_start * 3600)//TimeInterval,(Dark_start * 3600)//TimeInterval+dark_dur)%daybins
    light_hour = np.arange((Dark_start * 3600)//TimeInterval+dark_dur,(Dark_start * 3600)//TimeInterval+dark_dur+(daybins-dark_dur))%daybins
    return dark_hour,light_hour

def TimeUnit_to_Hours_GUI(TimeBinVector,Interval):
    """
    Function Target:
    ----------------
        This function transforms time bins to actual daily time
    """
    Seconds = np.round((TimeBinVector * Interval)%(3600*24))
    Hours = Seconds // 3600
    Minutes = (Seconds%3600)//60
    
    
    HourLabels = []
    for k in range(len(TimeBinVector)):
        string='%d:'%Hours[k]
        if Minutes[k]<10:
            string+='0%d'%Minutes[k]
        else:
            string+='%d'%Minutes[k]
        HourLabels += [string]
    return HourLabels
    
def Hours_to_TimeUnit_GUI(HourLabels,Interval=None):
    """
    Function Target:
    ----------------
        This function converts hours to Time Unit vector
    """
    Seconds = []
    if Interval is None:
        Interval = TimeInterval_From_HourLabel_GUI(HourLabels)
        
    for hour in HourLabels:
        stringList = hour.split(':')
        Hour = int(stringList[0])
        Minute = int(stringList[1])
        Seconds +=[Hour*3600+Minute*60]
    TimeBinVector = np.array(Seconds,dtype=int)/Interval
    return TimeBinVector
    
def TimeInterval_From_HourLabel_GUI(HourLabels):
    try: 
        Hour_0 = int(HourLabels[0].split(':')[0])
        Minute_0 = int(HourLabels[0].split(':')[1])
        k=1
        while Hour_0 == 23:
           Hour_0 = int(HourLabels[k].split(':')[0])
           Minute_0 = int(HourLabels[k].split(':')[1]) 
           k+=1
        Hour_1 = int(HourLabels[k].split(':')[0])
        Minute_1 = int(HourLabels[k].split(':')[1])
        Interval = (Hour_1-Hour_0)*3600+(Minute_1-Minute_0)*60
    except (IndexError, ValueError):
        k=0
        Hour_0 = int(HourLabels[0].split('-')[0])
        Hour_1 = int(HourLabels[0].split('-')[-1])
        k=1
        while Hour_0>=Hour_1:
            Hour_0 = int(HourLabels[k].split('-')[0])
            Hour_1 = int(HourLabels[k].split('-')[-1])
            k+=1
        Interval = (Hour_1-Hour_0)*3600
    
    return Interval

    
def Leap_GUI(year):
    """
    Target of the Function: if the year is bisestile returns 1, otherwise 0, and
                            it also returns the day of the calendar depending
                            on the case
                            
    Input:                  Year
    Output:                 i = 1,0 if Year is leap,not leap respectively
                            Calendar = vector containing the each month's day
                            
    
    
    """

    if (year % 4) == 0 & ( year % 100 != 0 or year % 400 ==0 ):

        Calendar = [31,29,31,30,31,30,31,31,30,31,30,31]
        i=1

       
    else:
        
        Calendar = [31,28,31,30,31,30,31,31,30,31,30,31]
        i=0
        
    return(i,Calendar)





def summing_day_GUI(month,day,year,days_from_today):
    """
    Input:  month, day, year= a date
        days_from_today = number of days we want to add to this date       
 
        
    Output: new_day = new date resulting from adding days_from_today days from the
                date in input
    """


    Calendar= Leap_GUI(year)[1]       
    Tot_day=sum(Calendar[0:int(month)-1])+day+days_from_today


    while Tot_day > 365+Leap_GUI(year)[0]:

        Tot_day=Tot_day-365-Leap_GUI(year)[0]
        year = year+1               

    Calendar=Leap_GUI(year)[1]
    month = np.where(np.cumsum(Calendar)>=Tot_day)[0][0]+1
    day = Tot_day-sum(Calendar[0:int(month)-1])
        
    new_date=month,day,year
    return(new_date)
    
def Terminate_Dataset_GUI(Y,End_Time,TimeStamps,scaled=True):
    """
    Function Target:    This function calculates the last day of the dataset
                        and complete truncate dataset (like dataset of ongoing
                        experiment or dataset with negative times)
                    
    Input:              -Y=nx2 dataset
                        -End_Time=scalar,
                            second from midnight of first day of exp
    Output:             -Y=nx2 dataset merged with the last day of experiment 
    """

    if len(np.where(Y['Action']==TimeStamps['End Month'])[0])==0:  
        N_Day=End_Time//(3600*24)
        Start_month=Y['Time'][np.where(Y['Action']==TimeStamps['Start Month'])[0][0]]
        Start_Day=Y['Time'][np.where(Y['Action']==TimeStamps['Start Day'])[0][0]]
        Start_Year=Y['Time'][np.where(Y['Action']==TimeStamps['Start Year'])[0][0]]
        End_Month,End_Day,End_Year=summing_day_GUI(Start_month,Start_Day,Start_Year,N_Day)
        Tmp=np.zeros(3,dtype={'names':('Time','Action'),'formats':('f8','f8')})
        Tmp['Action']=[TimeStamps['End Month'],TimeStamps['End Day'],TimeStamps['End Year']]
        Tmp['Time']=[End_Month,End_Day,End_Year]
        Y=np.hstack((Y,Tmp))
    elif scaled:
        N_Day=End_Time//(3600*24)
        Start_month=Y['Time'][np.where(Y['Action']==TimeStamps['Start Month'])[0][0]]
        Start_Day=Y['Time'][np.where(Y['Action']==TimeStamps['Start Day'])[0][0]]
        Start_Year=Y['Time'][np.where(Y['Action']==TimeStamps['Start Year'])[0][0]]
        End_Month,End_Day,End_Year=summing_day_GUI(Start_month,Start_Day,Start_Year,N_Day)

        Y['Time'][np.where(Y['Action']==TimeStamps['End Month'])[0][0]] = End_Month
        Y['Time'][np.where(Y['Action']==TimeStamps['End Day'])[0][0]] = End_Day
        Y['Time'][np.where(Y['Action']==TimeStamps['End Year'])[0][0]] = End_Year
        
    return Y
    
def Merge_2_Dataset_GUI(Y0,Y1,TimeStamps,scale=1,header=12,footer=3):
    """
    Function Target:    This Function merges two dataset in a way that the second dataset
                        starts after the first, keeping the correct start daily hour
                        of both datasets
                    
    Input:              -Y0=first dataset
                        -Y1=second dataset
                        
    Output:             -New_Y=merged dataset
    """
    
#    TimeStamps = np.load('/Users/Matte/Python_script/Phenopy/actionDictionaries/AM-Microsystems.npy').all()
#    TimeStamps['Center Light On']=51
    
    Start_exp_0,Start_Time_0,End_Time_0=Time_Details_GUI(Y0,TimeStamps,scale)
    Start_exp_1,Start_Time_1,End_Time_1=Time_Details_GUI(Y1,TimeStamps,scale)
# Here I cut eventual incomplete final trial
    try:
        Ind0=np.where(Y0['Action']==TimeStamps['Center Light On'])[0][-1]
        Ind1=np.where(Y0['Action']==TimeStamps['End Intertrial Interval'])[0][-1]
        if Ind0>Ind1:
            Y0=Y0[:Ind1+1]
    except:
        pass
    try:
        Ind0=np.where(Y1['Action']==TimeStamps['Center Light On'])[0][0]
        Ind1=np.where(Y1['Action']==TimeStamps['End Intertrial Interval'])[0][0]
        if Ind0>Ind1:
            Y1=Y1[Ind1+1:]
    except:
        pass

#   In case the dataset was ongoing    
    if Y0['Action'][-footer]==TimeStamps['End Month']:
        LastTimeStamp=Y0['Time'][-footer-1]
    else:
        LastTimeStamp=Y0['Time'][-1]
    N_Day=int(np.floor((LastTimeStamp+Start_exp_0)/(3600*24)))
    
#   Second from midnght from last day of exp 0 to last timestamps of exp 0 
    Last_Day_Time=LastTimeStamp+Start_exp_0-3600*24*N_Day
#   Time from the end of exp 0 to the start of exp 1    
#    Time_Difference=Start_exp_1-Last_Day_Time
    Time_Delta=Start_Time_1-Last_Day_Time
    Time_Difference=Start_exp_1-Last_Day_Time
    
    if Time_Delta<0:
        Time_Difference=Time_Difference+3600*24
    Y=Y1[header:].copy()
    

    h = ((Start_exp_1+Y['Time'][header:-footer]) // 60) % (24*60)
    if Y['Action'][-footer]==TimeStamps['End Month']:
        Y['Time'][:-footer]=Y['Time'][:-footer]+LastTimeStamp+Time_Difference
    else:
        Y['Time']=Y['Time']+LastTimeStamp+Time_Difference
    hh = ((Start_exp_0+Y['Time'][header:-footer]) // 60) % (24*60)
    if not np.prod(hh==h):
        raise ValueError('Data Assigned To Different Daily time')
    if Y0['Action'][-footer]==TimeStamps['End Month']:
        New_Y=np.hstack((Y0[:-footer],Y))
    else:
        New_Y=np.hstack((Y0,Y))
    return(New_Y)
    
def Merge_N_Dataset_GUI(Datas,Keys,TimeStamps,scale=1):
    """
    Function Target:    This Function merges two dataset in a way that the second dataset
                        starts after the first, keeping the correct start daily hour
                        of both datasets
                    
    Input:              -Datas=Dictionary of nx2 datasets
                        -Keys=list of ordered keys
                        
    Output:             -New_Datas=merged dataset
    """
    if len(Keys)==1:
        return(list(Datas.values())[0])
    New_Datas=Merge_2_Dataset_GUI(Datas[Keys[0]],Datas[Keys[1]],TimeStamps,scale=scale)
    for key_num in range(2,len(Keys)):

        New_Datas=Merge_2_Dataset_GUI(New_Datas,Datas[Keys[key_num]],TimeStamps,scale=scale)
    return(New_Datas)
    
def StartDate_GUI(Data,TimeStamps):
    """
    Function Target:  This function returns the date in which exp starts
    
    Input:            -Data=nx2 dataset
    
    Output:           -Month,Day,Year=tuple, starting exp date
    """
    Month=int(Data['Time'][np.where(Data['Action']==TimeStamps['Start Month'])[0][0]])
    Day=int(Data['Time'][np.where(Data['Action']==TimeStamps['Start Day'])[0][0]])
    Year=int(Data['Time'][np.where(Data['Action']==TimeStamps['Start Year'])[0][0]])
    return Month,Day,Year
    
def EndDate_GUI(Data,TimeStamps):
    """
    Function Target:  This function returns the date in which exp ends
    Input:            -Data=nx2 dataset
    Output:           -Month,Day,Year=tuple, ending exp date
    """
    Month=int(Data['Time'][np.where(Data['Action']==TimeStamps['End Month'])[0][0]])
    Day=int(Data['Time'][np.where(Data['Action']==TimeStamps['End Day'])[0][0]])
    Year=int(Data['Time'][np.where(Data['Action']==TimeStamps['End Year'])[0][0]])
    return Month,Day,Year
    
def StartHour_GUI(Data,TimeStamps):
    StartHour=Data['Time'][np.where(Data['Action']==TimeStamps['Start Hour'])[0][0]]
    StartMinute=Data['Time'][np.where(Data['Action']==TimeStamps['Start Minute'])[0][0]]
    return StartHour,StartMinute

def CreateGroupMatrix_GUI(SubjectName,StatName_Vector,Values,Groups = None):
    """
        Function Target:
        ----------------
            This function creates a matrix given a vector of subject names,
            the vector of the corrisponding extracted statistic and the matrix
            Values containing the corrisponding extracted statistics
        Input:
        ------
            - SubjectName
                array/list of subject names, if repeated means that you have 
                extracted several statistics, (mean or median or stderror)
            - StatName_Vector
                Array/list of stat names
            - Values
                Matrix containing the values of extracted stat. 
                Matrix(i,j) = StatName_Vector(i) extracted from SubjectName(i)
                of group Groups(i) at the time point j
            - Groups
                array/list of group names, optional, if None Groups will be a
                vector of ones
        Output:
        -------
            - Matrix
                numpy structured array with column labels
    """
    totRows=len(Values)
    if Groups is None:
        Groups = [[1]]*totRows
        lenGroupName = 1
    else:
        lenGroupName = 0
        for grName in Groups:
            lenGroupName = max(len(str(grName)),lenGroupName)
        Groups = np.array(Groups).reshape((totRows,1))
    lenSubjectName = 0
    for SubjName in SubjectName:
        lenSubjectName = max(lenSubjectName,len(str(SubjName)))
    Values = np.array(Values)
    totTimePoint = len(Values[0,:])
    SubjectName = np.array(SubjectName).reshape((totRows,1))
    
    
    StatName_Vector = np.array(StatName_Vector).reshape((totRows,1))
    
    Matrix = np.hstack((Groups,SubjectName,StatName_Vector,Values))
    dTypes='|S%d,|S%d,|S6,'%(lenGroupName,lenSubjectName)
    stringLabel = 'Group,Subject,Stat,'
    for k in range((totTimePoint)):
        stringLabel+='Time_%d,'%k
        dTypes += 'float,'
    dTypes = str(dTypes[:-1])
    stringLabel=str(stringLabel[:-1])
    Matrix = np.core.records.fromarrays(list(Matrix.T),names=stringLabel,formats=dTypes)
    return Matrix

def EndHour_GUI(Data,TimeStamps):
    End_Time=Time_Details_GUI(Data,TimeStamps)[-1]
    EndHour=(End_Time//3600)%24
    EndMinute=(End_Time//60)%60
    return EndHour,EndMinute
    
def DetectDelimiter_GUI(csvFile,delimiters=[';','\t',',']):
    """
    Function Target:
        This function look for different delimiters in a .csv or .txt file.
    Input:
        - csvFile= Path to the file
        - delimiters = list of possible delimiters
    OutPut:
        - delimiter = string, containing the delimiter if it was one in the 
        delimiters list, otherwise it contains None
    """
    with open(csvFile, 'U') as myCsvfile:
        header=myCsvfile.readline()
        line1=myCsvfile.readline()
        while header:
            count = []
            for d in delimiters:
                count += [header.count(d) + line1.count(d)]
            if max(count)>1:
                return delimiters[np.argmax(count)]
            header = myCsvfile.readline()
        return None

def create_OutputData_GUI(DataDict):
    """
        This function take as input a data dict of numpy struct
        array and creates a numpy struct array containing all
        datasets.\n
        
        Input:
        ------
            -Datadict = dictionary of numpy struct arrays
    """
    lengths    = []
    maxNameLen = 0
    Keys       = list(DataDict.keys())
    for key in Keys:
        lengths    += [len(DataDict[key])]
        maxNameLen = max(len(key), maxNameLen)
    tupleNames   = ('Subject',) + DataDict[key].dtype.names
    tupleFormats = ('|S%d'%maxNameLen,)
    for descr in DataDict[key].dtype.descr:
        tupleFormats += (np.dtype(descr[1]),)
    outputData = np.zeros(sum(lengths),\
                          dtype = {'names':tupleNames,
                                   'formats':tupleFormats})
    ind_0 = 0
    for k in range(len(lengths)):
        outputData['Subject'][ind_0: ind_0 + lengths[k]] = Keys[k]
        for name in tupleNames[1:]:
            outputData[name][ind_0: ind_0 + lengths[k]]  =\
                DataDict[Keys[k]][name]
        ind_0 += lengths[k]
    return outputData

class Dataset_GUI(object):
    def __init__(self,Dataset,Label,Path=None,Types=None,Scaled=(True,10000),FactorColumns=None,
                 TimeStamps=None):
        self.Dataset = Dataset
        self.Label = Label
        self.Path = Path
        self.Types = Types
        self.Scaled = Scaled 
        self.FactorColumns = FactorColumns
        self.TimeStamps = TimeStamps

class DatasetContainer_GUI(QObject):
    updateSignal = pyqtSignal(name='dataContainerUpdated')
    def __init__(self,TimeStamps=None,parent=None):
        super(DatasetContainer_GUI,self).__init__(parent)
        self.__Datas = OrderedDict()
        self.__TimeStamps = TimeStamps
        self.updateSignal.emit()
        
    def __iter__(self):
        for Label in list(self.keys()):
            yield self.__Datas[Label].Label,self.__Datas[Label].Dataset
    
    def getTimeStamps(self,label):
        return self.__Datas[label].TimeStamps
        
    def add(self,data):
        """
        Method Target:
            This method add a new object of the type Dataset_GUI to the 
            DataContainer_GUI interface.
        Input:
            - data = object of the class Dataset_GUI
        """
        self.__Datas.pop(data.Label)
        self.__Datas[data.Label] = data
        self.updateSignal.emit()
        
    def join(self,other):

        for key in list(other.keys()):
            # copy old keys
            old_key = copy(key)
            # create new key
            while key in list(self.keys()):
                key += '_1'
            # cerate new data_GUI object with new key
            new_data = Dataset_GUI(other[old_key].Dataset,
                                   key,
                                   other[old_key].Path,
                                   other[old_key].Types,
                                   other[old_key].Scaled,
                                   other[old_key].FactorColumns,
                                   other[old_key].TimeStamps)
            # remove old dataset_GUI
            self.add(new_data)

    def remove(self,Label):
        self.__Datas.pop(Label)
        self.updateSignal.emit()
        
    def pop(self,Label):
        Data = self.__Datas.pop(Label)
        if Data:
            return Data.Label,Data.Dataset
        self.updateSignal.emit()
        
    def clear(self):
        self.__Datas.clear()
        self.updateSignal.emit()
        
    def path(self,Label):
        return self.__Datas[Label].Path
        
    def changePath(self,Label,NewPath):
        self.__Datas[Label].Path = NewPath
        
    def dataType(self,Label):
        return self.__Datas[Label].Types
        
    def scaled(self,Label):
        return self.__Datas[Label].Scaled
    
    def factorCulumnIndexes(self,Label):
        return self.__Datas[Label].FactorColumns
        
    def changeScale(self,Label,newScale):
        data=Dataset_GUI(self.takeDataset(Label),Label,self.path(Label),
                         self.dataType(Label),(True,newScale))
        self.pop(Label)        
        self.add(data)  
        
    def keys(self):
        return list(self.__Datas.keys())
        
    def renameColumns(self,Label,columTuple):
        Data=self.takeDataset(Label)
        dt = deepcopy(Data.dtype)
        names = list(dt.names)
        for k in range(len(columTuple)):
            if columTuple[k] is not None:
                names[k] = columTuple[k]
        dt.names = tuple(names)
        newData = np.rec.array(Data,dtype=dt)
        Data = np.array(newData)
        
        data=Dataset_GUI(Data,Label,self.path(Label),
                         self.dataType(Label),self.scaled(Label))
        self.pop(Label) 
        self.add(data)

    def __getitem__(self, Label):
        return self.__Datas[Label]

    def has_key(self,Label):
        if Label in list(self.keys()):
            return True
        else:
            return False
        
    def save(self,Label,fname):
        Dataset = copy(self.__Datas[Label].Dataset)
        Types = self.__Datas[Label].Types
        Scaled = self.__Datas[Label].Scaled
        boolType = 1
        for Type in Types:
            if 'EEG' in Type:
                boolType = 0
                break
        if boolType:
            try:
                if Dataset.dtype.names==('Time','Action'):
                    if self.__Datas[Label].Scaled[0]:
                        Dataset=self.ReturnToOriginalScale(\
                            Label,self.__Datas[Label].Scaled[1])
            except:
                return False
        if not save_A_Data_GUI(Dataset,Types,Scaled,
                    fname,self.factorCulumnIndexes(Label)):
            return False
        
        data = Dataset_GUI(self.__Datas[Label].Dataset,os.path.basename(fname)
            ,fname,Types,self.scaled(Label))
        self.__Datas.pop(Label)
        self.add(data)
#            self.__Datas[Label].Label = os.path.basename(fname)
#            self.__Datas[Label].Path = fname
        return True
        
    
    def ReturnToOriginalScale(self,Label,scale):
        Dataset = Rescale_Time_GUI(self.__Datas[Label],self.getTimeStamps(Label),1.0/float(scale))
        #Dataset = Rescale_Time(Dataset,1.0/float(scale))
        return Dataset
        
    def takeDataset(self,Label):
        return self.__Datas[Label].Dataset
        
    def changeKey(self,OldLabel,NewLabel):
        
        data=Dataset_GUI(self.takeDataset(OldLabel),NewLabel,self.path(OldLabel),self.dataType(OldLabel),self.scaled(OldLabel))
        self.pop(OldLabel)        
        self.add(data)  
    
def save_A_Data_GUI(Dataset,Types,Scaled,
                    fname,FactorColumnInd=None):
    try:
        Data = Dataset.reconstructDataMatrix()
       
        fmt = ['%i','%s','%s'] + ['%f']*Dataset.PowerSp.shape[1]
       
        header = ''
        for i in range(len(Data.dtype.names))  :
            header = header + Data.dtype.names[i] + '\t'
        header = header[:-1]
        np.savetxt(fname, Data, header=header, comments='',
                   delimiter='\t', fmt=fmt)
        return True
    except AttributeError:
        pass
    try:
        header,DType = '',''
        fmt=[]
        for i in range(len(Dataset.dtype.names))  :
            header = header + Dataset.dtype.names[i]+';'
            if Dataset.dtype[i] == int or Dataset.dtype[i] == bool:
                fmt = fmt + ['%i']
                DType =DType + 'int;'
            elif Dataset.dtype[i] == float:
                fmt = fmt + ['%f']
                DType = DType + 'float;'
            elif Dataset.dtype[i] == datetime.datetime:
                fmt += ['%s']
                DType = DType + 'S%d'%20
            else:
                stringlen=0
                for index in range(len(Dataset[Dataset.dtype.names[i]])):
                    tmp=len(Dataset[Dataset.dtype.names[i]][index])
                    if tmp>stringlen:
                        stringlen=tmp
                
                fmt = fmt + ['%s']
                DType = DType + 'S%d;'%stringlen
        footer = 'Types;'
        if Types is not None:
            for Type in Types:
                footer = footer + Type + ';'
        footer = footer[:-1]+'\nScaled;%d;%f'%Scaled
        footer = footer+'\ndtype;'+DType[:-1]
        if FactorColumnInd is not None:
            footer += '\nfactorColumns;'
            for ind in FactorColumnInd: 
                footer = footer+'%d;'%ind
            footer=footer[:-1]
        else:
            footer += '\nfactorColumns;'
       
        header=header[:-1]
        np.savetxt(fname,Dataset,header=header,footer=footer,comments='',
                   delimiter=';',fmt=fmt)
        return True
    except:
        return False

def dateTimeArange(timeFirst, timeLast, sec=4):
    lenVect = int(np.ceil(((timeLast - timeFirst).seconds +\
        (timeLast - timeFirst).days * 3600 * 24))/4)
    timeVect = np.zeros(lenVect + 1,dtype=datetime.datetime)
    for k in range(lenVect + 1):
        timeVect[k] = timeFirst + k * datetime.timedelta(seconds=sec)
    return timeVect

def getEEGHeaderLen(path, delimiter =','):
    fh = open(path,'U')
    line = fh.readline()
    header = 0
    while line:
        try:
            float(line.split(delimiter)[0])
            return header
        except:
            header += 1
            line = fh.readline()
    return None
      
class EEG_Data_Struct(object):
    def __init__(self, PowerSp = None, Stage = None, Time = None,
                 freqTuple = None, freqLim_Hz = 20.5, PathToFile = None,
                 delimiter = '\t', StageCol = 1, timeCol = 2,
                 lastFreq = None, header = 18, freqBand = False, complete=True):  
        self.freqBand = freqBand
        self.freqTuple = []
        if PathToFile:
            fh = open(PathToFile, 'U')
            for tmp in range(header-1):
                fh.readline()
            line = (fh.readline()[:-1]).split(delimiter)
            fh.close()
            
            removeCol = []
            numCol = 0
            first = True
            if complete:
                FreqList = []                
                for word in line:
                    if not 'Hz' in word:# word.endswith('Hz'):
                        if word == '':
                            removeCol += [numCol]
                        numCol += 1
                        
                        continue
                    else:
                        if first:
                            first = False
                            firstPw = numCol
                        freq = float(word[:-2])
                        FreqList += [freq]
                        
                        if freq <= freqLim_Hz:
                            numCol += 1
                        else:
                            freq = float(line[numCol-1][:-2])
                            break
                if lastFreq:
                    FreqList += [lastFreq]
                else:
                    lastFreq = 2 * FreqList[-1] - FreqList[-2]
                    FreqList += [lastFreq]
                for k in range(len(FreqList)-1):
                    self.freqTuple += [(FreqList[k],FreqList[k+1])]
                
            else:
                for word in line:
                    if word in ['Delta','delta']:
                       self.freqTuple += [(0.25,5.)]
                    elif word in ['Theta','theta']:
                        self.freqTuple += [(5.,9.)]
                    elif word in ['Alpha','alpha']:
                        self.freqTuple += [(9.,12.)]
                    elif word in ['Beta','beta']:
                        self.freqTuple += [(12.,20.)]
                    elif word in ['Gamma','gamma']:
                        self.freqTuple += [(20.,40.)]
                    else:
                        removeCol += [numCol]
                    if len(self.freqTuple) is 1:
                        firstPw = numCol
                    numCol += 1
                    
            self.freqTuple = np.array(self.freqTuple)
            useCol = list(range(firstPw, numCol))
            self.PowerSp   = np.genfromtxt(PathToFile, skip_header = header,
                                           usecols = useCol, dtype = float,
                                           delimiter=delimiter)
            self.Stage     = np.genfromtxt(PathToFile, skip_header = header,
                                           usecols = [StageCol], dtype = '|S3',
                                           delimiter=delimiter)

            self.Timestamp = np.genfromtxt(PathToFile, skip_header = header,
                                           usecols = [timeCol], dtype = '|S20',
                                           delimiter=delimiter)

            self.Timestamp = vectDateConvertion(self.Timestamp)

            self.Timestamp = addSecondToEEGTimeStamp(self.Timestamp)

        else:
            self.PowerSp      = PowerSp
            self.Stage        = Stage
            if Time.dtype.char == 'S':
                Time = vectDateConvertion(Time)
            self.Timestamp    = Time
            self.Timestamp = addSecondToEEGTimeStamp(self.Timestamp)
            self.freqTuple    = np.array(freqTuple)
            
        if self.PowerSp.shape[1] > self.freqTuple.shape[0]:
            self.PowerSp = self.PowerSp[:,:self.freqTuple.shape[0]]
        elif self.PowerSp.shape[1] < self.freqTuple.shape[0]:
            self.freqTuple = self.freqTuple[:self.PowerSp.shape[1],:]

    def takeCols(self,freqMin, freqMax):
        useCol = []
        col = 0
        for rangeFreq in self.freqTuple:
            if freqMin <= rangeFreq[0] and rangeFreq[0] <= freqMax:
                useCol += [col]
            col += 1

        return self.PowerSp[:,useCol],self.freqTuple[useCol]
    
    def __getitem__(self,index):
        return EEG_Data_Struct(self.PowerSp[index,:],self.Stage[index],
                               self.Timestamp[index],self.freqTuple)
        
        
    def Return_FreqBandData(self,Bands = [(0.25, 5), (5, 9),
                                       (9, 12), (12,20)]):
        Data = np.zeros((self.PowerSp.shape[0],len(Bands)))
        col = 0
        freqTuple = []
        for band in Bands:
            BandData,BandFreq = self.takeCols(*band)
            Data[:,col] = np.sum(BandData, axis = 1)
            freqTuple += [(BandFreq[0,0],BandFreq[-1,-1])]
            col += 1
        Data = EEG_Data_Struct(PowerSp = Data, Stage = self.Stage,
                               Time = self.Timestamp, 
                               freqTuple = freqTuple, freqBand = True)       
        return Data

    def reconstructDataMatrix(self):
        isovect = np.vectorize(returnIsoFmt)
        shape = self.PowerSp.shape
        fmt = (int, '|S3', '|S19') + (float,)*shape[0]
        names = ('EpochNo', 'Stage', 'Time')
        for tup in self.freqTuple:
            names += ('%.6fHz'%tup[0],)

        DM = np.zeros(shape[0], dtype={'names':names,
                      'formats':fmt})
        DM['Time'] = isovect(self.Timestamp)
        DM['Stage'] = self.Stage
        DM['EpochNo'] = list(range(shape[0]))
        ind = 0
        for row in self.PowerSp.T:
            DM[names[ind+3]] = row
            ind += 1
        return DM

def returnIsoFmt(dt):
    return dt.isoformat()

def addSecondToEEGTimeStamp(timeVect, epoch_dur=False):
    if timeVect[0].second !=0 or timeVect[1].second != 0 or\
        timeVect[2].second != 0:

        return timeVect
    timeStamp = copy(timeVect)
    firstMinute = timeStamp[0].minute
    ind = 0
    for timeVal in timeStamp:
        secondMinute = timeVal.minute
        if secondMinute != firstMinute:
            break
        ind += 1
    countLen = 0
    for timeVal in timeStamp[ind:]:
        thirdMin = timeVal.minute
        if thirdMin != secondMinute:
            break
        countLen += 1
    EpochDur = 60 // countLen
    startEpoch = countLen - ind
    h = startEpoch


    for k in range(len(timeStamp)):
        timeStamp[k] = timeStamp[k].replace(second=0)
        timeStamp[k] = timeStamp[k] + datetime.timedelta(seconds=h*EpochDur)
        h = (h + 1) % countLen
    return timeStamp
    
def translate_EEG_in_Time(dataStruct,time_delta_sec):
    if type(time_delta_sec) is int:
        time_delta_sec = datetime.timedelta(0,time_delta_sec)
    dataStruct.Timestamp = dataStruct.Timestamp + time_delta_sec
    return dataStruct

def Parse_A_Datestr(dateStr):
    """
        Function Target:
        ================
            parse a date string of the format:
                "Year-Month-Day Hour:Minute:Second"
    """
    if 'T' in dateStr:
        return datetime.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%S')
    return datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
        
    
def Parse_TimeVect(TimeVect):
    func = np.vectorize(Parse_A_Datestr)
    return func(TimeVect)

def Return_Hour_Minute(datetimeVect):
    timeVect = np.zeros(len(datetimeVect),dtype='S5')
    for k in range(len(datetimeVect)):
        timeVect[k] = '%d:%d'%(datetimeVect[k].hour,datetimeVect[k].minute)
    return timeVect

def TimeBin_From_TimeString(timeStr, Binning = 3600):

    try:
        Bin = (timeStr.hour * 3600 + timeStr.minute * 60) // Binning
    except AttributeError:
        Bin = (int(timeStr.split(':')[0]) * 3600 +\
               int(timeStr.split(':')[1]) * 60) // Binning
    return Bin
#==============================================================================
# New   Ordered Dictionary
#==============================================================================


"""Provides the OrderedDict example class.

WARNING: This class is wrongly named, it should be called SortedDict.
A correctly named version is included in this directory, and a more
sophisticated version is available from
http://pypi.python.org/pypi/sorteddict
"""



class OrderedDict(object):
    """A dictionary that is ordered by key
    
    Initializing with a dictionary is expensive because all the
    dictionary's keys must be sorted. This is also true of the update()
    method.
    """

    def __init__(self, dictionary=None):
        """Initializes with a shallow copy of the given dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        >>> OrderedDict()
        OrderedDict({})
        >>> e = OrderedDict(d)
        >>> e.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        self.__keys = []
        self.__dict = {}
        if dictionary is not None:
            if isinstance(dictionary, OrderedDict):
                self.__dict = dictionary.__dict.copy()
                self.__keys = dictionary.__keys[:]
            else:
                self.__dict = dict(dictionary).copy()
                self.__keys = sorted(self.__dict.keys())


    def update(self, dictionary=None, **kwargs):
        """Updates this dictionary with another dictionary and/or with
        keyword key=value pairs


        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5))
        >>> d.update(dict(a=4, z=-4))
        >>> d.items()
        [('a', 4), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('z', -4)]
        >>> del d["a"]
        >>> del d["i"]
        >>> d.update({'g': 9}, a=1, z=3)
        >>> d.items()
        [('a', 1), ('g', 9), ('n', 3), ('s', 1), ('t', 5), ('z', 3)]
        >>> e = OrderedDict(dict(p=4, q=5))
        >>> del d["a"]
        >>> del d["n"]
        >>> e.update(d)
        >>> e.items()
        [('g', 9), ('p', 4), ('q', 5), ('s', 1), ('t', 5), ('z', 3)]
        """
        if dictionary is None:
            pass
        elif isinstance(dictionary, OrderedDict):
            self.__dict.update(dictionary.__dict)
        elif (isinstance(dictionary, dict) or 
              not hasattr(dictionary, "items")):
            self.__dict.update(dictionary)
        else:
            for key, value in list(dictionary.items()):
                self.__dict[key] = value
        if kwargs:
            self.__dict.update(kwargs)
        self.__keys = sorted(self.__dict.keys())


    @classmethod
    def fromkeys(cls, iterable, value=None):
        """A class method that returns an OrderedDict whose keys are
        from the iterable and each of whose values is value

        >>> d = OrderedDict()
        >>> e = d.fromkeys("KYLIE", 21)
        >>> e.items()
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        >>> e = OrderedDict.fromkeys("KYLIE", 21)
        >>> e.items()
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        """
        dictionary = cls()
        for key in iterable:
            dictionary[key] = value
        return dictionary


    def getAt(self, index):
        """Returns the index-th item's value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.getAt(0)
        2
        >>> d.getAt(5)
        6
        >>> d.getAt(2)
        3
        >>> d.getAt(19)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        return self.__dict[self.__keys[index]]


    def setAt(self, index, value):
        """Sets the index-th item's value to the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.getAt(5)
        6
        >>> d.setAt(5, 99)
        >>> d.getAt(5)
        99
        >>> d.setAt(19, 42)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        self.__dict[self.__keys[index]] = value


    def copy(self):
        """Returns a shallow copy of this OrderedDict

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> e = d.copy()
        >>> e.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        dictionary = OrderedDict()
        dictionary.__keys = self.__keys[:]
        dictionary.__dict = self.__dict.copy()
        return dictionary


    def clear(self):
        """Removes every item from this OrderedDict
        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> d.clear()
        >>> len(d)
        0
        >>> d["m"] = 3
        >>> d["a"] = 5
        >>> d["z"] = 7
        >>> d["e"] = 9
        >>> d.keys()
        ['a', 'e', 'm', 'z']
        """
        self.__keys = []
        self.__dict = {}


    def get(self, key, value=None):
        """Returns the value associated with key or value if key isn't
        in the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.get("X", 21)
        21
        >>> d.get("i")
        4
        """
        return self.__dict.get(key, value)


    def setdefault(self, key, value):
        """If key is in the dictionary, returns its value;
        otherwise adds the key with the given value which is also
        returned

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.setdefault("n", 99)
        3
        >>> d.values()
        [2, 4, 3, 1, 5, 6]
        >>> d.setdefault("r", -20)
        -20
        >>> d.items()[2:]
        [('n', 3), ('r', -20), ('s', 1), ('t', 5), ('y', 6)]
        >>> d.setdefault("@", -11)
        -11
        >>> d.setdefault("z", 99)
        99
        >>> d.setdefault("m", 50)
        50
        >>> d.keys()
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self.__dict:
            bisect.insort_left(self.__keys, key)
        return self.__dict.setdefault(key, value)


    def pop(self, key, value=None):
        """If key is in the dictionary, returns its value and removes it
        from the dictionary; otherwise returns the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.pop("n")
        3
        >>> "n" in d
        False
        >>> d.pop("q", 41)
        41
        >>> d.keys()
        ['a', 'i', 's', 't', 'y']
        >>> d.pop("a")
        2
        >>> d.pop("t")
        5
        >>> d.keys()
        ['i', 's', 'y']
        """
        if key not in self.__dict:
            return value
        i = bisect.bisect_left(self.__keys, key)
        del self.__keys[i]
        return self.__dict.pop(key, value)


    def popitem(self):
        """Returns and removes an arbitrary item from the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> len(d)
        3
        """
        item = self.__dict.popitem()
        i = bisect.bisect_left(self.__keys, item[0])
        del self.__keys[i]
        return item


    def keys(self):
        """Returns the dictionary's keys in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.keys()
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return self.__keys[:]


    def values(self):
        """Returns the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.values()
        [2, 4, 3, 1, 5, 6]
        """
        return [self.__dict[key] for key in self.__keys]


    def items(self):
        """Returns the dictionary's items in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        return [(key, self.__dict[key]) for key in self.__keys]


    def __iter__(self):
        """Returns an iterator over the dictionary's keys

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d)
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return iter(self.__keys)


    def iterkeys(self):
        """Returns an iterator over the dictionary's keys

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d)
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return iter(self.__keys)


    def itervalues(self):
        """Returns an iterator over the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.itervalues())
        [2, 4, 3, 1, 5, 6]
        """
        for key in self.__keys:
            yield self.__dict[key]


    def iteritems(self):
        """Returns an iterator over the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.iteritems())
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        for key in self.__keys:
            yield key, self.__dict[key]


    def has_key(self, key):
        """Returns True if key is in the dictionary; otherwise returns
        False. Use in instead.

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.has_key("a")
        True
        >>> d.has_key("x")
        False
        """
        return key in self.__dict


    def __contains__(self, key):
        """Returns True if key is in the dictionary; otherwise returns
        False

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> "a" in d
        True
        >>> "x" in d
        False
        """
        return key in self.__dict


    def __len__(self):
        """Returns the number of items in the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> del d["n"]
        >>> del d["y"]
        >>> len(d)
        4
        >>> d.clear()
        >>> len(d)
        0
        """
        return len(self.__dict)


    def __delitem__(self, key):
        """Deletes the item with the given key from the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.keys()
        ['a', 'i', 'n', 's', 't', 'y']
        >>> del d["s"]
        >>> d.keys()
        ['a', 'i', 'n', 't', 'y']
        >>> del d["y"]
        >>> d.keys()
        ['a', 'i', 'n', 't']
        >>> del d["a"]
        >>> d.keys()
        ['i', 'n', 't']
        >>> d = OrderedDict(dict(a=1, b=2, z=3))
        >>> d.keys()
        ['a', 'b', 'z']
        >>> del d["c"]
        Traceback (most recent call last):
        ...
        KeyError: 'c'
        >>> d.keys()
        ['a', 'b', 'z']
        """
        del self.__dict[key]
        i = bisect.bisect_left(self.__keys, key)
        del self.__keys[i]


    def __getitem__(self, key):
        """Returns the value of the item with the given key

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d["i"]
        4
        >>> d["y"]
        6
        >>> d["z"]
        Traceback (most recent call last):
        ...
        KeyError: 'z'
        """
        return self.__dict[key]


    def __setitem__(self, key, value):
        """If key is in the dictionary, sets its value to value;
        otherwise adds the key to the dictionary with the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d["t"] = -17
        >>> d["z"] = 43
        >>> d["@"] = -11
        >>> d["m"] = 22
        >>> d["r"] = 5
        >>> d.keys()
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self.__dict:
            bisect.insort_left(self.__keys, key)
        self.__dict[key] = value


    def __repr__(self):
        """Returns an eval()-able string representation of the
        dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5))
        >>> repr(d)
        "OrderedDict({'a': 2, 'i': 4, 'n': 3, 's': 1, 't': 5})"
        >>> d = OrderedDict({2: 'a', 3: 'm', 1: 'x'})
        >>> repr(d)
        "OrderedDict({1: 'x', 2: 'a', 3: 'm'})"

        Alternative implementation using a list comprehension:

        return "OrderedDict({{{0}}})".format(", ".join(
                for key in self.__keys]))
        """
        pieces = []
        for key in self.__keys:
            pieces.append("{0!r}: {1!r}".format(key, self.__dict[key]))
        return "OrderedDict({{{0}}})".format(", ".join(pieces))

def add_NANs(time_vect, *epoch_vect_tuple):
    """
        Function Target:
        ================
            This function adds missing time stamps, in case of datas with time
            jumps and adds NaNs as the corresponding power values or epochs
    """
    dt = np.diff(time_vect)
    k = 0
    for t in dt:
        dt[k] = t.seconds + t.days * 3600 * 24
        k += 1
    epoch_dur = sts.mode(dt)[0]
    jump_ind = np.where(dt != epoch_dur[0])[0]
    new_time = copy(time_vect)
    new_epoch = {}
    k=0
    for epoch in epoch_vect_tuple:
         new_epoch[k] = epoch
         k += 1
    for ind in jump_ind[::-1]:
        if dt[ind] % epoch_dur[0] != 0:
            raise ValueError
#       In case there is more then one day one day of difference 
        dt[ind] = dt[ind] % (3600 * 24)
        if dt[ind] == 0: # in case there's exactly one day of difference

            dt[ind] = dt[ind] + 3600 * 24
        num_add_epochs = int(dt[ind] // epoch_dur[0])
        add_times = []
        for k in range(1,num_add_epochs):
            add_times = np.hstack((add_times, time_vect[ind] +\
            datetime.timedelta(0, k * epoch_dur[0])))


        new_time = np.hstack((new_time[:ind+1], add_times, new_time[ind+1:]))
        for key in list(new_epoch.keys()):
            new_epoch[key] = np.hstack((new_epoch[key][:ind+1], np.zeros(num_add_epochs) *
            np.nan, new_epoch[key][ind+1:]))
    return new_time, new_epoch#,add_times

class action_Reply_Struct(object):
    def __init__(self,folder='.'):#,actionList = [], replyList = []):
        self.actionList = []#actionList
        self.replyList = []#replyList
        path = os.path.join(folder,'ReplyDictionary_SDO.npy')
        self.REPLYDICTIONARY = np.load(path).all()
    def append_action(self,action_msg):
        self.actionList.append(action_msg)
        if type(action_msg) is tuple:
            return
        self.replyList.append(self.expectedReply(action_msg))
    def append_actions(self,action_msg_list):
        for action_msg in action_msg_list:
            self.actionList.append(action_msg)
            if type(action_msg) is tuple:
                continue
            self.replyList.append(self.expectedReply(action_msg))
    def expectedReply(self,action_msg):
        return self.REPLYDICTIONARY[action_msg.dataAsHexStr()[4:10]]
    def popAction(self):
        try:
            action = self.actionList.pop(0)
        except IndexError:
            action = None
        return action
        
    def popReply(self):
        try:
            reply = self.replyList.pop(0)
        except IndexError:
            reply = None
        return reply
    def isEmpty(self):
        try:
            self.actionList[0]
        except IndexError:
            try:
                self.replyList[0]
            except IndexError:
                return True
        return False
    def clear(self):
        self.actionList = []
        self.replyList = []
    def __repr__(self):
        return ('Action-Reply Structure\nTot Actions: %d\nTot Replies: %d'
                            %(len(self.actionList),len(self.replyList)))
        

class AnalysisList(list):
    def __init__(self, sleep_list=[], behavior_list=[], integrative_list=[]):
        tmp = sleep_list + behavior_list + integrative_list
        super(AnalysisList, self).__init__(tmp)
        self.__all_list = tmp
        self.__behavior_list = behavior_list
        self.__sleep_list = sleep_list
        self.__integrative_list = integrative_list
        
    
    def append(self, value, label):
        super(AnalysisList,self).append(value)
        if label == 'sleep':
            self.__sleep_list.append(value)
        elif label == 'behavior':
            self.__behavior_list.append(value)
        elif label == 'integrative':
            self.__integrative_list.append(value)
        else:
            raise ValueError('Must choose label between \"sleep\", \"behavior\" and \"integrative\"')
    def __repr__(self):
        
        string = 'Behavior list: ' + self.__behavior_list.__repr__()
        string += '\nSleep list: ' + self.__sleep_list.__repr__()
        string += '\nIntegrative list: ' + self.__integrative_list.__repr__()
        return string
        
    def get_behavior(self):
        return self.__behavior_list
        
    def get_sleep(self):
        return self.__sleep_list
        
    def get_integrative(self):
        return self.__integrative_list