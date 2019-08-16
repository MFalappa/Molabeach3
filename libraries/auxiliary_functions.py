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
from scipy.optimize import curve_fit
import scipy.stats as sts
import numpy as np
import datetime as dt
import warnings


def F_FitSin_FixPeriod(Vector,amplitude0,phase0,translation0, function):
    """
    Function Target:
    ================
        This function computes a sin fit of the vector Vector.
        
    Input:
    ======
        - Vector : numpy array, shape 1 x n
            The 1D array we want to fit
        - amplitude0 : int
            Starting amplitude for the approx. algorithm
        - phase0 : int
            Starting phase for the approx. algorithm
        - translation0 : int
            Starting horizontal translation for the approx. algorithm
        - period0 : int
            Starting period for the approx. algorithm
        - MaxIter : integer
            Max iteration for the approx. algorithm
            
    Output:
    =======
        - F : numpy array, shape 1 x n
            Sinusoidal fit
        - popt : list
            All the fitted paramethers (amplitude, period, phase,translation)
        - corr : float
            Pearson correlaiton coefficient between sinfit and Vector
        - p_value : floar
            p-value relative to the pearson coefficient corr 
    """
    x = np.arange(0,len(Vector),1)
    p0 = [amplitude0, phase0, translation0] 

    popt, pcov = curve_fit(function, x, Vector, p0,absolute_sigma=True,maxfev=10**3)
    
    
    
    popt, pcov = curve_fit(function, x, Vector, popt,absolute_sigma=True,maxfev=10**3)
    
    F = function(x,popt[0],popt[1],popt[2])
    corr,p_value=sts.pearsonr(Vector,F)
    
    return F,popt,corr,p_value

def fit_sin_GUI(x,b1,b2,b3,b4):
    return b1*np.sin(2*np.pi*(1/b2)*x+b3)+b4

def Fit_Sin_BestPeriod(Array, p_min, p_max, start_hour, step_num = 100,
                       Light_start = 7, interval = 3600):
    Period_Array = np.zeros(step_num, dtype = {
                            'names':('Period','Phase','Amplitude',
                            'Translation','Pearson corr','p_value'),
                            'formats':(float, float, float,
                                       float, float, float)}
                             )
    day_length = (24 * 3600 / interval)
    a0  = (max(Array) - min(Array))/2
    ph0 = 2 * np.pi / 24 * ((start_hour - Light_start) % day_length)
    t0  = min(Array)
    Periods = np.linspace(p_min, p_max, step_num)
    Period_Array['Period'] = Periods
    ind = 0
    BestCorr = -1
    for period in Periods:
        p0 = period * (3600 / interval)
        function = lambda x, b1, b3, b4 : fit_sin_GUI(x, b1, p0, b3, b4)
        F, popt, corr, p_value = F_FitSin_FixPeriod(Array, a0, ph0, t0,
                                                    function)
        Period_Array['Amplitude'][ind]    = popt[0]
        Period_Array['Phase'][ind]        = popt[1]
        Period_Array['Translation'][ind]  = popt[2]
        Period_Array['Pearson corr'][ind] = corr
        Period_Array['p_value'][ind]      = p_value
        if corr > BestCorr:
            BestCorr = corr
            Best_Fit = F
        ind += 1
    Best_Fit_Param = Period_Array[np.argmax(Period_Array['Pearson corr'])]
    return Period_Array, Best_Fit_Param, Best_Fit

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

def F_Actogram_GUI(Y,Start_Time,End_Time,interval,TimeStamps,*period,**kwargs):
    """
    Function targets: This function calculate the numbers of NP per interval of time
                    (interval length is given as input).
                     

    Input ( 
             Y=Dataset, nx2 array: first column time stamps, second column event codes
             Start_time = start experiment (seconds from midnight of the first day of experiment)
             End_time = last NP time (seconds from midnight of the first day of experiment)
             interval = fraction of an hour in seconds
             period = tuple, the periodicity of the activity we consider in hour 
             (Optional, default is 24) 
            ) 
    Output (
             Action_x_Interval = vector, containing number of NP per time interval
             N_Day = number of days for the actogram
            )

    """
    
    if len(period)==0:
        period=24
    elif len(period)==1:
        period=period[0]
    else:
        #print 'Warning! Too many input argumet...'
        return()
    if 3600%interval!=0:
        #print('Warning! The interval you choose is not a fraction of an hour')
        return()
    if 'String' in kwargs:
        String=kwargs['String']
    else:
        String='FullData'
    
#   NP activity indexies
    Index_LeftNPin = np.where(Y['Action']==TimeStamps['Left NP In'])[:][0]
    Index_LeftNPout = np.where(Y['Action']==TimeStamps['Left NP Out'])[:][0]
    Index_RightNPin = np.where(Y['Action']==TimeStamps['Right NP In'])[:][0]
    Index_RightNPout = np.where(Y['Action']==TimeStamps['Right NP Out'])[:][0]
    Index_CenterNPin = np.where(Y['Action']==TimeStamps['Center NP In'])[:][0]
    Index_CenterNPout = np.where(Y['Action']==TimeStamps['Center NP Out'])[:][0]

#   Reorder NP activity indexies and save all NP times reordered.

    Index_NP_All=np.sort(np.hstack((Index_LeftNPin, Index_LeftNPout, Index_RightNPin,
                  Index_RightNPout, Index_CenterNPin, Index_CenterNPout)))
    NP_Times_All=Y['Time'][Index_NP_All]

#   Total time activity in sec from the first hour of experiment

    Start_Hour = (Start_Time //  3600) * 3600
    Total_Action_Time = End_Time-Start_Hour

#   Second from the between the beginning of the first hour of activity to the
#   Start_exp

    Delta_Sec = Start_Time - Start_Hour
    
#   Seconds from the beginning of the hour for every nose poke time

    NP_Times_All= NP_Times_All+Delta_Sec
    
#   Number of colums in the actogram

    N_Bins = int(np.ceil(Total_Action_Time/interval))

#   Vector containing the border times of our N_bins [t_0,t_0+interval,t_0+2*interval...]

    Intervals_endpoints = np.hstack((interval*np.arange(0,N_Bins),NP_Times_All[-1]))
   # #print Intervals_endpoints[40:60]
    
#   Action_x_Interval is a vector containing NP Totals per single time inteval

    Action_x_Interval=[]

#   We count how many actions happen in the same interval of time and we
#   record this values in the vector Action_x_Interval.
    

    for i in np.arange(N_Bins):

            Total=NP_Times_All[np.where(NP_Times_All>=Intervals_endpoints[i])]
            Total=Total[np.where(Total<Intervals_endpoints[i+1])]
            Action_x_Interval=np.hstack((Action_x_Interval,np.array([len(Total)])))        

#   We divide the experiment time interval into 2*period h periods and then
#   draw an actogram #printing in the 1st line 1st and 2nd day of experiment
#   on the 2nd line the 2nd and 3rd day and so on...
    
    ##print('Added optional argument String!')
    Activity_Duration = End_Time-Start_Time
    if String=='FullData':
        
        N_Day=End_Time//(3600*period)
    else:
        N_Day = int(np.floor((Activity_Duration)/(period*3600)))
    
    return(Action_x_Interval,N_Day)
    
def F_PeakProbes_GUI(Y,TimeStamps,ProbesOn,ProbesOff,tend,l_r, TMAX=np.inf,
                     trial_num=-1,trial_ind=None):
    """
    Function targets:   computing a raster plot matrix and a vector with the
                        peaks distribution

    Input:              - Y = the dataset, nx2 matrix with time stamps and action
                        codes
                        -ProbesOn = a vector containing the indexes of probe trials
                        start (center light on in a probe trial)
                        -ProbesOff = a vector containing the indexes of probe trials
                        end (End ITI in a probe trial)
                        -tend = scalar containing a time limit of a trial
                        -l_r = string containing 'r' or 'l' in case we're
                        analysing a right or a left trial

    Output:             -Raster = matrix n'xtend*100 containing raster plot
                        -Peaks = vector containig the peak distribution
    """
    
    if l_r=='l':
        
        On=TimeStamps['Left NP In']
        Off=TimeStamps['Left NP Out']
        
    elif l_r=='r':
        
        On=TimeStamps['Right NP In']
        Off=TimeStamps['Right NP Out']

    
#   We consider tend*100 time points for each probe trial and we set
#   Raster(i,j)= 1 if in the i trial at the time tj the mouse is in the hopper,
#   Raster(i,j)=0 otherwise.
    tend=int(tend)
    if not trial_ind is None:
        Raster=np.zeros((trial_num,tend*100), dtype = int)
    else:
        Raster=np.zeros((len(ProbesOn),tend*100), dtype = int)
    Times=np.arange(tend*100,dtype=float)/100
    for i in range(len(ProbesOn)):
#        print(ProbesOn[i],ProbesOff[i])
        temporarydata = Y[:][ProbesOn[i]:ProbesOff[i]]
        RespOn = np.where(temporarydata['Action']==On)[0]
        RespOff = np.where(temporarydata['Action']==Off)[0]
        TimeOn = temporarydata['Time'][list(RespOn)]-temporarydata['Time'][1]
        TimeOff = temporarydata['Time'][RespOff]-temporarydata['Time'][1]
        if len(TimeOff)<len(TimeOn):
#            TimeOn=TimeOn[:-1]
            TimeOff = np.hstack((TimeOff,[tend]))
        if len(TimeOff) > len(TimeOn):
            if TimeOff[0] < TimeOn[0]:
                TimeOff = TimeOff[1:]
            else:
                TimeOff = TimeOff[:-1]
        Ind = np.where(TimeOff<=TMAX)[0]           
        TimeOn = TimeOn[Ind]
        TimeOff=TimeOff[Ind]
        
        for ind in range(len(TimeOn)):
            time_0=TimeOn[ind]
            time_1=TimeOff[ind]
            Tmp=Times[np.where(Times<=time_1)[0]]
            Raster_ind=np.where(Tmp>=time_0)[0]
            if not trial_ind is None:
                Raster[trial_ind[i]][Raster_ind] = 1
            else:
                Raster[i][Raster_ind]=1
                
#   We sum the colum of the matrix raster.

    Peaks=np.sum(Raster,axis=0)
    return(Raster,Peaks)
    
def F_Probes_x_TimeInterval_GUI(Y,TimeStamps,Start_exp,End_Time,l_r,tend=np.inf,Floor=False,
                            t_first=0,t_last=3600*24,return_IndProbe=False):
    """
    Function Targets:   This function delete probes on and off indexes of trials that are not in the range
         				(t_first,t_last) for each day of analysis

                        
    Input:              -Y = Dataset, nx2 matrix
                        -ProbesOn = vector containing the indexes of every probe trial start of the 
                            Dataset Y
                        -ProbesOff = vector containing the indexes of every probe trial end of the
                            Dataset Y
                        -Start_exp = start time of the experiment (seconds form midnight before the 
                            analysis begins)
                        -EndTime = last NP time (seconds from midnight of the first
                            day of experiment)
                        -t_first_last[0]/[1] == t_first/t_last=time interval of the probes trial we want 
                            to analyze (seconds 0<=t_first<t_last<=3600*24)
                        
    Output:             -ProbesOn,ProbesOff = vector containing the ProbesOn/Off
                            indexes of trials in the chosen interval
                      
    """

       

    if t_first<0 or t_last>3600*24:
        return()

    TrialOnset = np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    TrialOffset = np.where(Y['Action']==TimeStamps['End Intertrial Interval'])[0]
    end_trial = np.where(Y['Action']==TimeStamps['Start Intertrial Interval'])[0]
#    if len(np.where(Y['Action']==36)[0])>0:
#        TrialOffset = np.where(Y['Action']==36)[0]
#    else:
#        TrialOffset = np.where(Y['Action']==33)[0]
    Probes=np.where(Y['Action']==TimeStamps['Probe Trial'])[0]
    
#   Happens if a in the last trial we stop collecting data before the
#   trial finishes, we just cut the last TrialOnset
    TrialOnset = F_OnSet_GUI(TrialOffset,TrialOnset)
    TrialOffset = F_OffSet_GUI(TrialOnset,TrialOffset)
    if len(TrialOnset)>len(TrialOffset):
        TrialOnset=TrialOnset[:-1]
    if len(end_trial) > len(TrialOffset):
        end_trial=end_trial[:-1]
    dt = Y['Time'][end_trial] - Y['Time'][TrialOnset]

    keep_index = np.where(dt<=tend)[0]
    TrialOffset = TrialOffset[keep_index]
    TrialOnset = TrialOnset[keep_index]

#   Here we keep only the onset and offset in our time interval
    
    Index = np.where((Y['Time'][TrialOnset] + Start_exp)%(3600*24)>=t_first)[0]
    TrialOnset = TrialOnset[Index]
    TrialOffset = TrialOffset[Index]
    Index = np.where((Y['Time'][TrialOffset] + Start_exp)%(3600*24)<=t_last)[0]
    TrialOnset = TrialOnset[Index]
    TrialOffset = TrialOffset[Index]

#   Here we keep only probes contained in the interval we choose

    #N_Day=np.floor((End_Time-Start_exp)/(3600*24))
##
##  I changed floor to ceil to take into account all the data without cutting the
##  last day.
##
    if Floor:
        N_Day=np.floor((End_Time-Start_exp)/(3600*24))
    else:
        N_Day=np.ceil((End_Time-Start_exp)/(3600*24))
    TimeProbe=Y['Time'][Probes]
    TimeOn=Y['Time'][TrialOnset]
    TimeOff=Y['Time'][TrialOffset]
    ProbesCut=[]

#   for each day we find the indexies of probes trial between first trial on and
#   last trial off in our choosen range

    for i in range(int(N_Day)):
        try:
           Index=np.where(TimeOff<=3600*24*(i+1))[0][-1]
           T1=TimeOff[Index]
           Index=np.where(TimeOn>=3600*24*(i))[0][0]
           T0=TimeOn[Index]    
           Temp_Ind=np.where(TimeProbe<=T1)[0]
           Temp_Time=TimeProbe[Temp_Ind]
           Temp_Ind=Temp_Ind[Temp_Time>=T0]
           ProbesCut=np.hstack((ProbesCut,Probes[Temp_Ind]))
          
        except IndexError:
           print(('No Probes in day %i'%i))
           
    Probes = np.array(ProbesCut, dtype = int)


#   Numbers of long and short probe

#   We save the index before the ptobe (35) of long and short trials which is
#   a 23 in case of short probe or 27 in case of long. (The mouse give the
#   correct answer after the end of the signal but doesn't get rewarded)
    
    if l_r=='l':
        for i in range(1,len(Probes[1:])):
            IndexLeft = np.where(Y['Action'][Probes[i-1]:Probes[i]]==23)[0]
            IndexRight = np.where(Y['Action'][Probes[i-1]:Probes[i]]==27)[0]
            
            if len(IndexLeft) and not len(IndexRight):
                DeltaIndex=Probes[i]-Probes[i-1]-IndexLeft[-1]
                break
            elif not len(IndexLeft):
                pass
            elif IndexLeft[-1] > IndexRight[-1]:
                DeltaIndex=Probes[i]-Probes[i-1]-IndexLeft[-1]
                break
        
        try:
            Probes = Probes[list(np.where(Y['Action'][list(Probes-DeltaIndex)] == 23)[0])]-1    
        except NameError:
            return(np.array([]),np.array([]))
            
        
    elif l_r=='r':
        for i in range(1,len(Probes[1:])):
            IndexLeft = np.where(Y['Action'][Probes[i-1]:Probes[i]]==23)[0]
            IndexRight = np.where(Y['Action'][Probes[i-1]:Probes[i]]==27)[0]
           
            if len(IndexRight) and not len(IndexLeft):
                DeltaIndex=Probes[i]-Probes[i-1]-IndexRight[-1]
                break
            elif not len(IndexRight):
                pass
            elif IndexLeft[-1] < IndexRight[-1]:
                DeltaIndex=Probes[i]-Probes[i-1]-IndexRight[-1]
                break
        
        try:
            Probes = Probes[list(np.where(Y['Action'][list(Probes-DeltaIndex)] == 27)[0])]-1    
        except NameError:
            return(np.array([]),np.array([]))
    
#   Record the indexies in which a probe sh/lg starts and stops

    IndProbesOn=[]
    IndProbesOff=[]
    for i in range(len(Probes)):
        if Probes[i] <= TrialOffset[-1] and Probes[i]>=TrialOnset[0]:
            IndProbesOn = np.hstack((IndProbesOn,
                                np.where(TrialOnset <= Probes[i])[0][-1]))
            IndProbesOff = np.hstack((IndProbesOff,
                                np.where(TrialOffset >= Probes[i])[0][0]))
            
    ProbesOn = TrialOnset[list(IndProbesOn)]
    ProbesOff = TrialOffset[list(IndProbesOff)]

#   Here we keep only trial that lasts less then tend sec
    Index=np.where(Y['Time'][list(Probes)]-Y['Time'][ProbesOn]<=tend)[0]
    ProbesOn=ProbesOn[Index]
    ProbesOff=ProbesOff[Index] 
    if return_IndProbe:
        return(ProbesOn,ProbesOff,IndProbesOn,len(TrialOnset))
    return(ProbesOn,ProbesOff)

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

def F_TimeInterval_From_Light_Start(Y,Start_exp,TimeInterval,Indexes,LightStartsec):
    
    # set first bin of ight phase as start of experiment
    sec = Y['Time'][Indexes] + Start_exp - LightStartsec
    
    IntervalStartTime = np.floor(sec/TimeInterval)
    return IntervalStartTime

def F_OffSet_GUI(TrialOnSet,OffSet):
    """
    Function Target:        This function calculate the TrialOffSet relative to the
                            TrialOnSet given.
                            
    Input:                  -TrialOnSet=vector, integer, indexes of some trial onset 
                            -OffSet=vector, indexes of all the trials off set
    
    Output:                 -TrialOffSet=vector,indexes of the Off Set relative 
                                of trial TrialOnset
    """
    TrialOnSet=np.array(TrialOnSet)
    OffSet=np.array(OffSet)
    TrialOffSet=np.array([],dtype=int)
    Tmp=-1
    for ind in TrialOnSet:
        All_Following_Off=np.where(OffSet>ind)[0]
        if len(All_Following_Off)>0:
            OffSet=OffSet[All_Following_Off]
            ##print OffSet
            if Tmp!=OffSet[0]:        
                TrialOffSet=np.hstack((TrialOffSet,OffSet[0]))
            Tmp=OffSet[0]
            OffSet=OffSet[1:]
    return(TrialOffSet)

def F_OnSet_GUI(TrialOffSet,OnSet):
    """
    Function Target:        This function calculate the OnSet relative to the
                            TrialOffSet given.
                            
    Input:                  -TrialOffSet=vector, integer, indexes of some trial offset 
                            -OnSet=vector, indexes of all the trials on set
    
    Output:                 -TrialOnSet=vector,indexes of the On Set relative of TrialOffSet
    """
    TrialOffSet=np.array(TrialOffSet)
    OnSet=np.array(OnSet)
    TrialOnSet=np.array([],dtype=int)
    Tmp=-1
    for ind in TrialOffSet[::-1]:
        All_Previous_On=np.where(OnSet<=ind)[0]
        if len(All_Previous_On)>0:
            OnSet=OnSet[All_Previous_On]
            if Tmp!=OnSet[-1]:
                TrialOnSet=np.hstack((TrialOnSet,OnSet[-1]))
            Tmp=OnSet[-1]
            OnSet=OnSet[:-1]
        try:
            OnSet[0]
            pass
        except IndexError:
            break
    return(TrialOnSet[::-1])

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

def MultipleHour_Light_and_Dark(Dark_start,Len_Dark,TimeInterval=7200):
    if Len_Dark % (3600*24/TimeInterval) != 0 and (24-Len_Dark) % (3600*24/TimeInterval) != 0:
        warnings.warn('One of the time point will contain both light and dark phase', UserWarning)
    
    daybins = (24*3600)//TimeInterval    
    dark_dur = (Len_Dark*3600)//TimeInterval    
    dark_hour = np.arange((Dark_start * 3600)//TimeInterval,(Dark_start * 3600)//TimeInterval+dark_dur)%daybins
    light_hour = np.arange((Dark_start * 3600)//TimeInterval+dark_dur,(Dark_start * 3600)//TimeInterval+dark_dur+(daybins-dark_dur))%daybins
    return dark_hour,light_hour

def F_AIT_GUI(Y,TimeStamps,TimeInterval=3600,Light_Start=8):
    """
    Fiunction Taeget:   This function calculates the index of AIT start and stop,
                        the hour of every AIT start and the duration of every AIT
                        
    Input:              -Y=nx2 dataset
    
    OutPut:             -AIT_OnSet/AIT_OffSet=vector, index of AIT on and off
                        -HourStart_AIT=vector, hour in which AIT starts (from
                        00:00 of the first day of exp)
                        -AIT_Dur=vector, duration of every AIT
    """
    Start_exp=Time_Details_GUI(Y,TimeStamps)[0]
    TrialOnSet=np.where(Y['Action']==TimeStamps['ACT_START_TEST'])[0]
    AIT_OnSet=np.where(Y['Action']==TimeStamps['End Intertrial Interval'])[0]
    AIT_OffSet=F_OffSet_GUI(AIT_OnSet,TrialOnSet)
    AIT_OnSet=F_OnSet_GUI(AIT_OffSet,AIT_OnSet)
#    HourStart_AIT=F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,AIT_OnSet,AIT_OffSet,'a',np.inf)[1]
    HourStart_AIT = F_TimeInterval_From_Light_Start(Y,Start_exp,TimeInterval,AIT_OnSet,Light_Start*3600)    
 
    
    #HourStart_AIT=F_Hour_Trial_GUI(Y,TimeStamps,Start_exp,AIT_OnSet,AIT_OffSet,'a',np.inf,24)[1]
    AIT_Dur=Y['Time'][AIT_OffSet]-Y['Time'][AIT_OnSet]
    return(AIT_OnSet,AIT_OffSet,HourStart_AIT,AIT_Dur)
    

def AITComputation_GUI(Y,DarkStart,TimeStamps,DarkDuration=12,TimeUnitToMinute=60,TimeInterval=3600):
    """
    Function Target:    This function is computing the mean and std error of
                        the actual inter trial (AIT) per daily hour. First elements
                        of the OrdMean etc. are from the Dark Phase, then there's
                        the light phase
    Input:
        -Y=nx2 Dataset
        -DarkStart=int, starting hour of the dark phase
        -DarkDuration=int, numer of hour of dark phase
    
    Output:
        -OrdMedian/Mean/Std=vector, first DarKDuration elements are Median/mean/
        std error of AIT
        -Hour_Dark/Light =vector, dark/light hour
    """
    Light_Start = (DarkStart + DarkDuration) % 24
    AIT_OnSet,AIT_OffSet,HourStart_AIT,AIT_Dur=F_AIT_GUI(Y,TimeStamps,TimeInterval=TimeInterval,Light_Start=Light_Start)
    Hour_Dark,Hour_Light = MultipleHour_Light_and_Dark(12,DarkDuration,TimeInterval)
    Mean = np.zeros(Hour_Dark.shape[0]+Hour_Light.shape[0])
    Median = np.zeros(Hour_Dark.shape[0]+Hour_Light.shape[0])
    STD = np.zeros(Hour_Dark.shape[0]+Hour_Light.shape[0])
    perc25 = np.zeros(Hour_Dark.shape[0]+Hour_Light.shape[0])
    perc75 = np.zeros(Hour_Dark.shape[0]+Hour_Light.shape[0])
    idx = 0
    for h in np.hstack((Hour_Dark,Hour_Light)):
        ih = (HourStart_AIT%(Hour_Dark.shape[0]+Hour_Light.shape[0])) == h
        Mean[idx] = np.nanmean(AIT_Dur[ih]/TimeUnitToMinute)
        Median[idx] = np.nanmedian(AIT_Dur[ih]/TimeUnitToMinute)
        STD[idx] = np.nanstd(AIT_Dur[ih]/TimeUnitToMinute)
        perc25[idx] = np.nanpercentile(AIT_Dur[ih]/TimeUnitToMinute,25)
        perc75[idx] = np.nanpercentile(AIT_Dur[ih]/TimeUnitToMinute,75)
        idx += 1
    return(Mean,Median,STD,perc25,perc75,Hour_Dark,Hour_Light,HourStart_AIT)

def extract_start(times,actions,codes):
    
    aa = 2000 + times[actions==codes['Start Year']] 
    mm = times[actions==codes['Start Month']]
    dd = times[actions==codes['Start Day']] 
    hh = times[actions==codes['Start Hour']] 
    mi = times[actions==codes['Start Minute']] 
    ss = times[actions==codes['Start Second']] 
        
    data_start = dt.datetime(aa,mm,dd,hh,mi,ss)
    
    return data_start

def filter_emg(emg_sig,cut_amp):
    emg_f = np.zeros(int(emg_sig.shape[0]))
    for kk in range(emg_sig.shape[0]):
        if emg_sig[kk] > cut_amp:
            
            tmp = np.nanmean(emg_f[kk-6:kk])
            
            if not np.isnan(tmp):
                emg_f[kk] = np.nanmean(emg_f[kk-6:kk])
            else:
                continue
            
        elif emg_sig[kk] < -cut_amp:
            
            tmp = np.nanmean(emg_f[kk-6:kk])
            
            if not np.isnan(tmp):
                emg_f[kk] = np.nanmean(emg_f[kk-6:kk])
            else:
                continue
            
        else:
            emg_f[kk] = emg_sig[kk]
        
    
    return emg_f

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
    fcut = np.array(tuple((low, high)))
    b, a = ellip(order, rp, rs, fcut, btype='bandpass')
    
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


    