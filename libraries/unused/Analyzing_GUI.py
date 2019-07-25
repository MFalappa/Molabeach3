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
import datetime
import warnings

import numpy as np
import scipy.stats as sts
import sklearn.mixture as mxt


from scipy.optimize import curve_fit
from statsmodels.api import add_constant, OLS
from bisect import bisect_left,insort_left
from PyQt5 import QtGui

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda
from matplotlib.mlab import PCA as PCA_mpl

from Modify_Dataset_GUI import (Rescale_Time_GUI,MultipleHour_Light_and_Dark,
                                Time_Details_GUI,F_Start_exp_GUI,OrderedDict,
                                Hour_Light_and_Dark_GUI,TimeUnit_to_Hours_GUI,
                                dateTimeArange,Parse_TimeVect,TimeBin_From_TimeString)


def F_New_Gr_Switch_Latency_GUI(Datas,TimeStamps,Mouse_Name,H_By_H=False,ts=3,tl=6, type_tr='Long',scale=1,Tend=15,Long_Side='r',isMEDDict={}):
    """
aggoingere qui la descrizione della funzione
    """

    switch_dict = {}
    table_dict = {}
    left_dict = {}
    right_dict = {}
    hrs_switch_dict = {}
    for name in Mouse_Name:
        if type(Long_Side) is dict:
            l_side = Long_Side[name]
        else:
            l_side = Long_Side
            
        #=============to be tested
        if l_side is 'm': 
            cond_to_check = True
            while cond_to_check:
                reply = QtGui.QInputDialog.getText(None,'Choose long location, Left or Right',name)
                if reply[1]:
                    if 'L' in reply[0].upper():
                        l_side = 'l'
                        cond_to_check = False
                    elif 'R' in reply[0].upper():
                        l_side = 'r'
                        cond_to_check = False                    
        #=============to be tested
            
        Datas[name] = Rescale_Time_GUI(Datas[name], TimeStamps[name], scale)
    
        table,left_in,left_out,right_in,right_out,start,stop = switch_analysis_gui(Datas[name], TimeStamps[name], ts, tl,long_side=l_side,isMED=isMEDDict[name])
        
        left,right,switch,hrs_switch = compute_latency(table,left_in,left_out,right_in,right_out,start,stop,ts,tl,type_tr,long_side=l_side)
        switch_dict[name] = switch
        table_dict[name] = table
        left_dict[name] = left
        right_dict[name] = right
        hrs_switch_dict[name] = hrs_switch
    return(table_dict,left_dict,right_dict,switch_dict,hrs_switch_dict)

def condition_check(table_row,type_tr):
    if type_tr == 'Long_Probe':
        return table_row['type'] == 'Long' and table_row['isProbe']
    elif type_tr == 'Long_reward':
        return table_row['type'] == 'Long' and table_row['isCorrect'] and not table_row['isProbe']
    elif type_tr == 'Long':
        return table_row['type'] == 'Long' and table_row['isCorrect']
        
def compute_latency(table,left_in,left_out,right_in,right_out,start,stop,ts,tl,type_tr,long_side='r'):
    left = np.array([])
    right = np.array([])
    switch = np.array([])
    hrs_switch = np.array([])
    
    if long_side == 'r':
        np_in = left_in
        np_out = left_out 
        oth_in = right_in
    else:
        np_in = right_in
        np_out = right_out
        oth_in = left_in
        
    for k in range(table.shape[0]):
        if condition_check(table[k],type_tr):
                if len(oth_in[k][:,1])*len(np_in[k][:,1]) > 0:
                    left = np.concatenate((left,left_in[k][:,1]))
                    right = np.concatenate((right,right_in[k][:,1]))

                
                    idx = np.where( np_in[k][:,1] <= tl)[0]
                    if idx.shape[0] and np_out[k].shape[0] > idx[-1]:
                        print(k)

                ## MODIFICA DA IN AD OUT
                #switch = np.concatenate((switch,[left_in[k][idx[-1],1]]))
                        switch = np.concatenate((switch,[np_out[k][idx[-1],1]]))
                        hrs_switch = np.concatenate((hrs_switch, [table[k]['absTime']]))
    return left,right,switch,hrs_switch

def getRewardTrialMED(Y,TimeStamps,start,stop):
    reward_start = []
    for k in range(start.shape[0]):
        if TimeStamps['Give Pellet Center'] in Y['Action'][start[k]:stop[k]]:
            reward_start += [start[k]]
    return np.array(reward_start)
            
def getRewardedTrial(Y,TimeStamps):
    reward_left = np.where(Y['Action']==TimeStamps['Give Pellet Left'])[0]
    reward_right = np.where(Y['Action']==TimeStamps['Give Pellet Right'])[0]
    start_trial = np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    rewards = np.hstack((reward_left,reward_right))
    rewards.sort()
    rewarded_start = -1*np.ones(start_trial.shape[0],dtype=int)
    ind = 0
    for rwd in rewards:
        i_st = bisect_left(start_trial, rwd) - 1
        if i_st != rewarded_start[ind-1]:
            rewarded_start[ind] = i_st
            ind += 1
    mask = np.zeros(rewarded_start.shape[0],dtype=bool)
    mask[rewarded_start != -1] = 1
    rewarded_start = rewarded_start[mask]
    return start_trial[rewarded_start]


def createAbsoluteTime(Y,indexVect,Timestamps):
    day = Y['Time'][np.where(Y['Action']==Timestamps['Start Day'])[0][0]]
    month = Y['Time'][np.where(Y['Action']==Timestamps['Start Month'])[0][0]]
    year = Y['Time'][np.where(Y['Action']==Timestamps['Start Year'])[0][0]]
    
    hour = Y['Time'][np.where(Y['Action']==Timestamps['Start Hour'])[0][0]]
    minute = Y['Time'][np.where(Y['Action']==Timestamps['Start Minute'])[0][0]]
    second = Y['Time'][np.where(Y['Action']==Timestamps['Start Second'])[0][0]]
    
    secs = Y['Time'][indexVect]
    delta_sec = np.zeros(secs.shape[0],dtype=datetime.timedelta)
    for k in range(secs.shape[0]):
        delta_sec[k] = datetime.timedelta(0,secs[k])
    abstime = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    func = lambda dt : abstime + dt
    vec_func = np.vectorize(func)
    return vec_func(delta_sec)
    
def switch_analysis_gui(Y,TimeStamps,ts,tl,long_side='r',isMED = False):    
    if isMED:
        left_in,left_out,right_in,right_out,start,stop = create_np_activity(Y,TimeStamps,startTrial='Start Trial')
        rewarded_start = getRewardTrialMED(Y, TimeStamps,start,stop)
        trial_type = switch_type_trial(Y,TimeStamps,start,ts,tl,light_off='Right Light Off')
    else:
        left_in,left_out,right_in,right_out,start,stop = create_np_activity(Y,TimeStamps)
        rewarded_start = getRewardedTrial(Y, TimeStamps)
        trial_type = switch_type_trial(Y,TimeStamps,start,ts,tl)
    performance = switch_performance(trial_type,left_in,right_in,ts,tl,long_side)
    probe = switch_probe_check(start, performance, rewarded_start)
    times = createAbsoluteTime(Y,start,TimeStamps)
    table = np.zeros(trial_type.shape[0], dtype = {'names':('absTime','start','stop','type','isCorrect','isProbe'),
                     'formats':(datetime.datetime,int,int,'S5',bool,bool)})
    table['absTime'] = times[:trial_type.shape[0]]
    table['start'] = start[:trial_type.shape[0]]
    table['stop'] = stop[:trial_type.shape[0]]
    ind_short = np.where(trial_type == 0)[0]
    table['type'] = 'Long'
    table['type'][ind_short] =  'Short'
    table['isCorrect'] = performance[:trial_type.shape[0]]
    table['isProbe'] = probe[:trial_type.shape[0]]
    
    return table,left_in,left_out,right_in,right_out,start,stop
    

def switch_probe_check(start, performance, rewarded_start):
    correct = np.where(performance)[0]
    probe = np.zeros(performance.shape[0],dtype=bool)
  
    for k in correct:
        if not (start[k] in rewarded_start):
            probe[k] = True
      
    return probe
    
def switch_performance(trial_type,left_in,right_in,ts,tl,long_side='r'):
    
    if long_side == 'r':
        short_np = left_in
        long_np = right_in  
    else:
        short_np = right_in
        long_np = left_in
        
    
    performance = np.zeros(trial_type.shape[0],dtype = bool)
    
    for k in range(trial_type.shape[0]):
        if trial_type[k]==0: 
            try:
                tmp_short = np.where( short_np[k][:,1] >= ts)[0][0]
            except IndexError:
                continue
            
            try:
                tmp_long = np.where( long_np[k][:,1] >= ts)[0][0]
                if tmp_long > tmp_short:
                    performance[k] = True
            except IndexError:
                performance[k] = True
                continue
            
        else:
            try:
                tmp_long = np.where(long_np[k][:,1] >= tl)[0][0]
            except IndexError:
                continue
        
            try:
                tmp_short = np.where(short_np[k][:,1] >= tl)[0][0]
                if tmp_long < tmp_short: 
                    performance[k] = True
                    
            except IndexError:
                performance[k] = True
                continue
                
    return(performance)
    
    
def switch_type_trial(Y,TimeStamps,light_on,ts,tl,light_off='Center Light Off'):
    
    light_off = np.where(Y['Action']==TimeStamps[light_off])[0]
    
    while light_off[0] < light_on[0]:
        light_off = light_off[1:]
        
    while light_off[-1] < light_on[-1]:
        light_on = light_on[:-1]
    
    # here I'm picking the shorter index vector and pairing each of its index K
    # with the index of the longer index vector that immediatly follows/precedes
    # K. (follows if the longer is light_off, precedes otherwise)
    if light_on.shape[0] < light_off.shape[0]:
        func = np.vectorize( lambda x : bisect_left(light_off, x) )
        light_off = light_off[func(light_on)]
    elif light_on.shape[0] > light_off.shape[0]:
        func = np.vectorize( lambda x : bisect_left(light_on, x) - 1)
        light_on = light_on[func(light_off)]

# check the light signaling at the beginning and and of the data

    
        
    light_on = Y['Time'][light_on]
    light_off =  Y['Time'][light_off]
    

    
    duration = light_off - light_on
    tmp = np.zeros((2,duration.shape[0]))
    
    tmp[0,:] = np.abs(duration-ts)
    tmp[1,:] = np.abs(duration-tl)
    # 0, short 1, long
    trial_type = np.argmin(tmp,axis = 0)
    
    return(trial_type)
    
    
def create_np_activity(Y,TimeStamps,startTrial='Center Light On'):
    
    Left_NP_in=np.where(Y['Action']==TimeStamps['Left NP In'])[0]
    Right_NP_in=np.where(Y['Action']==TimeStamps['Right NP In'])[0]
    try:
        Left_NP_out=np.where(Y['Action']==TimeStamps['Left NP Out'])[0]
        Right_NP_out=np.where(Y['Action']==TimeStamps['Right NP Out'])[0]
    except KeyError:
        Left_NP_out = Left_NP_in
        Right_NP_out = Right_NP_in
    
    
    start_trial = np.where(Y['Action']==TimeStamps[startTrial])[0]
    end_trial = np.where(Y['Action']==TimeStamps['Start Intertrial Interval'])[0] #cambiato da start a end
    
    left_in = {}
    left_out = {}
    right_in = {}
    right_out = {}
    
    stop = np.ones(start_trial.shape[0],dtype = int) * -1
    start = np.ones(start_trial.shape[0],dtype = int) * -1
    tr_num  = 0
    
    while start_trial.shape[0] and end_trial.shape[0]:
        s0 = start_trial[0]
        e0 = end_trial[0]
        ind = 0
        while e0 < s0 and ind < end_trial.shape[0]:
            e0 =  end_trial[ind]
            ind += 1
        if e0 < s0:
            stop = stop[:tr_num]
            start = start[:tr_num]
            break
        
        stop[tr_num] = e0
        start[tr_num] = s0
        
        start_trial = start_trial[1:]
        end_trial = end_trial[ind+1:]
        idx = np.where((Left_NP_in > s0)  * (Left_NP_in < e0))[0]
        tmp = np.zeros((idx.shape[0],2))
        tmp[:,0] = Left_NP_in[idx]
        tmp[:,1] = Y['Time'][Left_NP_in[idx]] - Y['Time'][s0]
        left_in[tr_num] = tmp
        
        idx = np.where((Left_NP_out > s0)  * (Left_NP_out < e0))[0]
        tmp = np.zeros((idx.shape[0],2))
        tmp[:,0] = Left_NP_out[idx]
        tmp[:,1] = Y['Time'][Left_NP_out[idx]] - Y['Time'][s0]
        left_out[tr_num] = tmp
        
        idx = np.where((Right_NP_in > s0)  * (Right_NP_in < e0))[0]
        tmp = np.zeros((idx.shape[0],2))
        tmp[:,0] = Right_NP_in[idx]
        tmp[:,1] = Y['Time'][Right_NP_in[idx]] - Y['Time'][s0]
        right_in[tr_num] = tmp
        
        idx = np.where((Right_NP_out > s0)  * (Right_NP_out < e0))[0]
        tmp = np.zeros((idx.shape[0],2))
        tmp[:,0] = Right_NP_out[idx]
        tmp[:,1] = Y['Time'][Right_NP_out[idx]] - Y['Time'][s0]
        right_out[tr_num] = tmp
        
        
        tr_num += 1
    boolean = stop != -1
    stop = stop[boolean]
    start = start[boolean]
    
    return(left_in,left_out,right_in,right_out,start,stop)
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
    
def Normalize_Action_x_Interval_GUI(Action_x_Interval,period,Hour_Fraction,N_Day,string):
    """
    Function Targets:           This function normalized the action per interval of time,
                                day by day or normalize respect the total days
    
    Input:                      -Action_x_Interval=vector, activity per interval of time
                                -period=scalar, the period you're considering
                                -Hour_Fraction=scalar, integer,interval of time you consider
                                -N_Day=scalr, number of days of the experiment
                                -sring=string, specify how to normalize.
    Output:                     -Norm_Action_x_Interval=vector,normalized Action_x_Interval
    """
    if string=='All':
        length=int(Hour_Fraction*period*N_Day)
        Norm_Action_x_Interval=Action_x_Interval[:length]/max(Action_x_Interval[:length])
    elif string=='DayByDay':
        #   We keep only the NP that occured in the N_Day days of trials
        Norm_Action_x_Interval=np.zeros(N_Day*period*Hour_Fraction)
        #   We normalize actions of each day...
        for i in np.arange(N_Day):
            Norm_Action_x_Interval[i*Hour_Fraction*period:(i+1)*Hour_Fraction*period]=Action_x_Interval[i*Hour_Fraction*period:(i+1)*Hour_Fraction*period]/max(Action_x_Interval[i*Hour_Fraction*period:(i+1)*Hour_Fraction*period])
    elif string == 'FullData':
        Norm_Action_x_Interval=Action_x_Interval/max(Action_x_Interval)
    return(Norm_Action_x_Interval)
    
def F_Correct_Rate_GUI(Y,Start_exp,period,TimeStamps,*tend):
    
    """
    Function Target:    This function calculate the rate of correct responses
                        hour by hour.
                        
    Input:              -Y = Dataset, nx2 matrix.
                        -Start_exp = start time of the experiment (seconds
                        form midnight before the analisis begins)
                        -tend[0] = scalar, max time of a trial.(optional,
                        default=30).

                        
    Output:             -Correct_Rate = vector, element i of this vector contains
                        the correct rate of hour i.
                        -Act_x_Hour = dictionary containing number of trials per
                        type of trial for each hour of the day.
    """
    
    if len(tend)<1:
        tend=30
    else:
        tend=tend[0]

    TrialOnSet=np.where(Y['Action']==TimeStamps['ACT_START_TEST'])[0]
#    TrialOnSet=np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    TrialOffSet=np.where(Y['Action']==TimeStamps['End Intertrial Interval'])[0]
    StartITI=np.where(Y['Action']==TimeStamps['Start Intertrial Interval'])[0]
    
#    if len(TrialOnSet)>len(TrialOffSet):
#        TrialOnSet=TrialOnSet[:-1]
    
    if TrialOnSet[0]>TrialOffSet[0]:
        TrialOffSet=TrialOffSet[1:]
        
    elif TrialOnSet[-1]>TrialOffSet[-1]: 
        TrialOnSet=TrialOnSet[:-1]
    if StartITI[-1]>TrialOffSet[-1]:
        StartITI=StartITI[:-1]
    if StartITI[0]<TrialOnSet[0]:
        StartITI=StartITI[1:]
#    if len(StartITI)>len(TrialOffSet):
#        StartITI=StartITI[:-1]
  
#    KeepIndex=np.where(Y['Time'][StartITI]-Y['Time'][TrialOnSet]<=tend)[0]
#    TrialOnSet=TrialOnSet[KeepIndex]
#    TrialOffSet=TrialOffSet[KeepIndex]
    Act_x_Hour={}
    for lettera in 'arlp':
        TrialHour=F_Hour_Trial_GUI(Y,TimeStamps,Start_exp,
                              TrialOnSet,TrialOffSet,lettera,tend,period)[1]
        if len(TrialHour)>0:
            Act_x_Hour[lettera]=np.array(F_Activity_x_Hour_GUI(TrialHour),dtype=float)
        else:
            Act_x_Hour[lettera]=np.zeros(24,dtype=float)
    Correct_Rate=(
        Act_x_Hour['r']+Act_x_Hour['l']+Act_x_Hour['p'])/Act_x_Hour['a']

    
    return(Act_x_Hour,Correct_Rate)
    
def F_Correct_Rate_New_GUI(Y,TimeStamps,Start_exp,period,tend=np.inf,TimeInterval=3600):
    """
    Function Target: 
    ----------------
        This function calculate the rate of correct responses
        hour by hour.
                        
    Input:          
    ------
        -Y = Dataset, nx2 matrix.
        -Start_exp = start time of the experiment (seconds
        form midnight before the analisis begins)
        -tend[0] = scalar, max time of a trial.(optional,
        default=30).
        -TimeInterval = tot of seconds of the choosen time interval
            it must be a fraction of an hour. (Example, If you choose to
            extract a value every 15min put TimeInterval=900)
        -HBin = int \in [1,2,3,4,6,12], if HBin is set >1 the 
        function extract the correct rate every hour and averages
        these values by groups of HBin hours starting from Hour_Dark[0]
        to Hour_Light[-1]

                        
    Output:             
    -------
        -Correct_Rate = vector, element i of this vector contains
        the correct rate of hour/TimeInterval i.
        -Act_x_Hour = dictionary containing number of trials per
        type of trial for each hour of the day.
    
    """
    
    

    try:
        TrialOnSet=np.where(Y['Action']==51)[0]
    except:
        TrialOnSet=np.where(Y['Action']==TimeStamps['Center Light On'])[0]
        
    #TrialOffSet=np.where(Y['Action']==36)[0]
    TrialOffSet=np.where(Y['Action']==TimeStamps['End Intertrial Interval'])[0]
    
    if len(TrialOnSet)>len(TrialOffSet):
        TrialOnSet=TrialOnSet[:-1]
    Act_x_Hour={}
    for lettera in 'arlp':
        
        TrialHour=F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,TrialOnSet,
                                       TrialOffSet,lettera,tend)[1]
        
        Act_x_Hour[lettera]=np.array(F_Activity_x_TimeInterval_GUI(TrialHour,TimeInterval=TimeInterval),dtype=float)

    Correct_Rate=(
        Act_x_Hour['r']+Act_x_Hour['l']+Act_x_Hour['p'])/Act_x_Hour['a']

    
    return(Act_x_Hour,Correct_Rate)

def F_Correct_Rate_AllHour_GUI(Y,TimeStamps,Start_exp,*tend):
    
    """
    Function Target:    This function calculate the rate of correct responses
                        hour by hour.
                        
    Input:              -Y = Dataset, nx2 matrix.
                        -Start_exp = start time of the experiment (seconds
                        form midnight before the analisis begins)
                        -tend[0] = scalar, max time of a trial.(optional,
                        default=30).

                        
    Output:             -Correct_Rate = vector, element i of this vector contains
                        the correct rate of hour i.
                        -Act_x_Hour = dictionary containing number of trials per
                        type of trial for each hour of the day.
    """
    
    if len(tend)<1:
        tend=30
    else:
        tend=tend[0]
    period=24
    TrialOnSet=np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    TrialOffSet=np.where(Y['Action']==36)[0]
#    TrialOffSet=np.where(Y['Action']==TimeStamps['End Intertrial Interval'])[0]
    
    if len(TrialOnSet)>len(TrialOffSet):
        TrialOnSet=TrialOnSet[:-1]
    Act_x_Hour={}
    
    #Test={}    
    
    for lettera in 'arlp':
        TrialHour=F_Hour_Trial_GUI(Y,TimeStamps,Start_exp,
                              TrialOnSet,TrialOffSet,lettera,tend,period)[1]
        #Test[lettera]=TrialHour
        AllHours=np.array(F_Activity_x_Hour_All_GUI(TrialHour),dtype=float)
        if lettera is 'a':
            TotHour=len(AllHours)
            #hour0=TrialHour[0]
        Act_x_Hour[lettera]=np.zeros(TotHour,dtype=float)
        Act_x_Hour[lettera][:len(AllHours)]=AllHours

    Correct_Rate=(
        Act_x_Hour['r']+Act_x_Hour['l']+Act_x_Hour['p'])/Act_x_Hour['a']

    
    return(Act_x_Hour,Correct_Rate)
    
def F_Hour_Trial_GUI(Y,TimeStamps,Start_exp,TrialOnset,TrialOffset,l_r_p_a,tend,period):
    """
    Function Target: 	  This Function calculate the Trial start (long-short-probe-all)
                        indexes and the Hour of each trial start.

    Input: 			  -Y = Dataset, nx2 matrix.
                        -Start_exp = start time of the experiment (seconds
                        form midnight before the analysis begins).
                        -TrialOnset = vector containing the indexes of Central
                        Light On (Trail Start)
                        -TrialOffset = Vector containing the indexes of end ITI
                        (Trial End).
                        -l_r_p_a = string that indicates which kind of trials to
                        consider. 
                        -tend = scalar, max time of a trial.
                        -period=scalar, the period you're considering

    Output:		      -TrialOn = vector, indexes of every start of
                        trial.
                        -HourStartTime = hour of the day in which every
                        Trial begins. 
    """
    
    period=float(period)

    
    if l_r_p_a=='l':
        Off=TimeStamps['Give Pellet Left']
    elif l_r_p_a=='r':
        Off=TimeStamps['Give Pellet Right']
    elif l_r_p_a=='p':
        Off=TimeStamps['Probe Trial']
    
    if l_r_p_a=='a':
        InTr=Y['Time'][TrialOnset]
        
        HourStartTime=np.floor(((InTr+Start_exp)/3600)*period/24)
        
        TrialOn=TrialOnset
    else:
        TrialOff=np.where(Y['Action']==Off)[0]
        if len(TrialOff)!=0:

            IndOn=[]
            for i in range(len(TrialOff)):
                IndOn = list(np.hstack((IndOn,
                                    np.where(TrialOnset <= TrialOff[i])[0][-1])))
            IndOn = np.array(IndOn,dtype=int)                    
            TrialOn = TrialOnset[IndOn]
            
            TrialOn=TrialOn[:np.where(TrialOn<TrialOffset[-1])[0][-1]+1]
            IndInTr=np.where(Y['Time'][TrialOff]-Y['Time'][
                TrialOn[0:len(TrialOff)]]<tend)[0]
            InTr=Y['Time'][TrialOn[IndInTr]]
            HourStartTime=np.floor(((InTr+Start_exp)/3600)*period/24)
        else:
            TrialOn=[]
            HourStartTime=[]
    return(TrialOn,HourStartTime)

def F_TimeInterval_From_Light_Start(Y,Start_exp,TimeInterval,Indexes,LightStartsec):
    
    # set first bin of ight phase as start of experiment
    sec = Y['Time'][Indexes] + Start_exp - LightStartsec
    
    IntervalStartTime = np.floor(sec/TimeInterval)
    return IntervalStartTime

def F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,TrialOnset,TrialOffset,l_r_p_a,tend):
    """
    Function Target: 	  This Function calculate the Trial start (long-short-probe-all)
                        indexes and the Hour of each trial start.

    Input: 			  -Y = Dataset, nx2 matrix.
                        -Start_exp = start time of the experiment (seconds
                        form midnight before the analysis begins).
                        -TrialOnset = vector containing the indexes of Central
                        Light On (Trail Start)
                        -TrialOffset = Vector containing the indexes of end ITI
                        (Trial End).
                        -l_r_p_a = string that indicates which kind of trials to
                        consider. 
                        - TimeInterval=integer, time interval in second. Must
                        divide 3600.
                        -tend = scalar, max time of a trial.
                        -period=scalar, the period you're considering

    Output:		      -TrialOn = vector, indexes of every start of
                        trial.
                        -HourStartTime = TimeInterval of the day in which every
                        Trial begins. 
    """
    
    period=24

    
    if l_r_p_a=='l':
        Off=TimeStamps['Give Pellet Left']
    elif l_r_p_a=='r':
        Off=TimeStamps['Give Pellet Right']
    elif l_r_p_a=='p':
        Off=TimeStamps['Probe Trial']
    if 3600.0%TimeInterval!=0:
        warnings.warn('TimeInterval do not divide 3600!',UserWarning)
#        raise ValueError, 'TimeInterval must divide 3600'
    
    if l_r_p_a=='a':
        InTr=Y['Time'][TrialOnset]
        
        IntervalStartTime=np.floor(((InTr+Start_exp)/(TimeInterval))*period/24)
        
        TrialOn=TrialOnset
    else:
        TrialOff=np.where(Y['Action']==Off)[0]
        if len(TrialOff)!=0:

            IndOn=[]
            for i in range(len(TrialOff)):
                IndOn = np.array(np.hstack((IndOn,
                                 np.where(TrialOnset <= TrialOff[i])[0][-1])),dtype=int)
            
            TrialOn = TrialOnset[IndOn]
            TrialOn=TrialOn[:np.where(TrialOn<TrialOff[-1])[0][-1]+1]
            IndInTr=np.where(Y['Time'][TrialOff]-Y['Time'][
                TrialOn[0:len(TrialOff)]]<tend)[0]
            InTr=Y['Time'][TrialOn[IndInTr]]
            IntervalStartTime=np.floor(((InTr+Start_exp)/TimeInterval)*period/24)
        else:
             TrialOn=[]
             IntervalStartTime=[]
    return(TrialOn,IntervalStartTime)
    
def F_Activity_x_Hour_GUI(TrialHour,**kwargs):
    """
    Function Target:    This function calculate how many trials are in a certain
                        hour.
                        
    Input:              -TrialHour = vector that contains the hour of each trial.
    
    Output:             -Act_x_Hour = vector,number of activity for each hour of the day.
    """
    Act_x_hour=[]
    if 'period' in kwargs:
        period=kwargs['period']
    else:
        period=24
    TrialHour_period=TrialHour%period
    if 'Hours' in kwargs:
        for h in kwargs['Hours']:
            Act_x_hour=Act_x_hour+[len(np.where(TrialHour_period==h)[0])]
    else:        
        for h in range(period):
            Act_x_hour=Act_x_hour+[len(np.where(TrialHour_period==h)[0])]  
    return(Act_x_hour)
    
def F_Activity_x_Hour_All_GUI(TrialHour):
    """
    Function Target:    This function calculate how many trials are in a certain
                        hour.
                        
    Input:              -TrialHour = vector that contains the hour of each trial.
    
    Output:             -Act_x_Hour = vector,number of activity for each hour from hour 0 of exp.
    """
    Act_x_hour=[]
    TrialHour_24=TrialHour
    if len(TrialHour) is 0:
        return []
    for i in np.arange(max(TrialHour)+1):
        Act_x_hour=Act_x_hour+[len(np.where(TrialHour_24==i)[0])]  
    return(Act_x_hour)
    
def F_Activity_x_TimeInterval_GUI(TrialInterval,TimeInterval,**kwargs):
    """
    Function Target:    This function calculate how many trials are in a certain
                        TimeInterval (fraction of hour in seconds).
                        
    Input:              -TrialTimeInterval = vector that contains the interval of time of each trial.
    
    Output:             -Act_x_Hour = vector,number of activity for each time interval of the day.
    """
    NumberOfIntervals = int(24*3600//TimeInterval)
    if len(TrialInterval):
        Act_x_hour=[]
        if 'period' in kwargs:
            NumberOfIntervals=kwargs['period']
        else:
            NumberOfIntervals=np.ceil((24*3600)/TimeInterval)
        TrialInterval_period=TrialInterval%NumberOfIntervals
        if 'Intervals' in kwargs:
            for h in kwargs['Intervals']:
                Act_x_hour=Act_x_hour+[len(np.where(TrialInterval_period==h)[0])]
        else:        
            for h in np.arange(NumberOfIntervals):
                Act_x_hour=Act_x_hour+[len(np.where(TrialInterval_period==h)[0])]  
    else:
        Act_x_hour=np.zeros(NumberOfIntervals)
    return(Act_x_hour)
    
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

def HourDark_And_Light_BinnedMean_GUI(Values,TimeUnit,Hour_Dark,Hour_Light,
                                      Bin,TimeUnit_Dur_Sec=3600):
    """
    Function Target:
    ----------------
        This function can return the mean, median and std error of values in 
        Values for every timeunit of light and dark. It can average over more
        than one hour and over fraction of an hour.
        To obtain the mean over more then one hour put:
           - TimeUnit_Dur_Sec = 3600 
           - Bin = k(>1)
        To obtain the mean over a fraction of hour(for exemple every 15min
        in this example) put:
           - TimeUnit_Dur_Sec = 900 
           - Bin = 1
        To obtain the standard hour by hour mean put:
           - TimeUnit_Dur_Sec = 3600 
           - Bin = 1
               
    """
    TotBins=len(Hour_Dark[::Bin])+len(Hour_Light[::Bin])
    MeanVector = np.zeros(TotBins,dtype=float)
    MedianVetor = np.zeros(TotBins,dtype=float)
    StdErrorVector = np.zeros(TotBins,dtype=float)
    indBin=0
    if np.mod(3600,TimeUnit_Dur_Sec) != 0:
        raise ValueError
    dailyDur_In_TimeUnit = int(3600//TimeUnit_Dur_Sec) * 24
    TimeUnit=np.array(TimeUnit%dailyDur_In_TimeUnit)
    Label=[]
    
    for hind in range(0,len(Hour_Dark),Bin):
        hourBin = Hour_Dark[hind:hind+Bin]
        Indexes = []
        if hourBin[0]!=hourBin[-1]:
            Label += ['%d-%d'%(hourBin[0],hourBin[-1])]
        else:
            Label += [str(hourBin[0])]

        for hh in hourBin:

            Indexes = np.hstack([Indexes,np.where(TimeUnit==hh)[0]])
        Indexes=np.array(Indexes,dtype=int)
        MeanVector[indBin] = np.nanmean(Values[Indexes])
        MedianVetor[indBin] = np.nanmedian(Values[Indexes])
        StdErrorVector[indBin] = np.nanstd(Values[Indexes])/np.sqrt(len(Indexes))
        indBin+=1
    
    for hind in range(0,len(Hour_Light),Bin):
        hourBin = Hour_Light[hind:hind+Bin]
        Indexes = []
        if hourBin[0]!=hourBin[-1]:
            Label += ['%d-%d'%(hourBin[0],hourBin[-1])]
        else:
            Label += [str(hourBin[0])]

        for hh in hourBin:
            
            Indexes = np.hstack([Indexes,np.where(TimeUnit==hh)[0]])
        Indexes=np.array(Indexes,dtype=int)
        MeanVector[indBin] = np.nanmean(Values[Indexes])
        MedianVetor[indBin] = np.nanmedian(Values[Indexes])
        StdErrorVector[indBin] = np.nanstd(Values[Indexes])/np.sqrt(len(Indexes))
        indBin+=1
    return MeanVector,MedianVetor,StdErrorVector,Label

def HourDark_And_Light_BinnedTotal_GUI(TimeUnit,Hour_Dark,Hour_Light,
                                       Bin,TimeUnit_Dur_Sec=3600):
    """
    Function Target:
    ----------------
        This function can return the total activity per each timeunit of
        light and dark. It can average over more than one hour and over 
        fraction of an hour.
        To obtain the mean over more then one hour put:
           - TimeUnit_Dur_Sec = 3600 
           - Bin = k(>1)
        To obtain the mean over a fraction of hour(for exemple every 15min
        in this example) put:
           - TimeUnit_Dur_Sec = 900 
           - Bin = 1
        To obtain the standard hour by hour mean put:
           - TimeUnit_Dur_Sec = 3600 
           - Bin = 1
               
    """
    TotBins=len(Hour_Dark[::Bin])+len(Hour_Light[::Bin])
    MeanVector = np.zeros(TotBins,dtype=float)
    MedianVetor = np.zeros(TotBins,dtype=float)
    StdErrorVector = np.zeros(TotBins,dtype=float)
    indBin=0
    if np.mod(3600,TimeUnit_Dur_Sec) != 0:
        raise ValueError
    dailyDur_In_TimeUnit = int(3600//TimeUnit_Dur_Sec) * 24
    
    Label=[]
    
    for hind in range(0,len(Hour_Dark),Bin):
        hourBin = Hour_Dark[hind:hind+Bin]
        Counts = [[]]*Bin
        binInd=0
        lenInd=0
        if hourBin[0]!=hourBin[-1]:
            Label += ['%d-%d'%(hourBin[0],hourBin[-1])]
        else:
            Label += [str(hourBin[0])]

        for hh in hourBin:
            # Per ogni "ora" (intervallo di tempo) nel vettore hourBin conto quante azioni avvengono a quell'
            # e le salvo nella matrice Counts = [c_ij] dove c_ij=num di azioni
            # avvenute all'ora j  del giorno i
            # Dopo di che sommo lungo le righe e ottengo un vettore Values= [v_i]
            # dove v_i = tot azioni avvenute nelle oreValues in hourBin e poi
            # estraggo media, mediana e std error
            if hh<TimeUnit[0] or hh>TimeUnit[-1]:
                # Se al primo fiorno di regirtazione di dati inizio alle 14
                # e hh<14 allora metto un NaN al primo valore di Counts
                # e porto avanti di un giorno hh
                hh+=dailyDur_In_TimeUnit
                Counts[binInd] = np.hstack([Counts[binInd],np.nan])
            hhDay = hh
            
            while hhDay <= TimeUnit[-1]:
                
                Counts[binInd] = np.hstack([Counts[binInd],len(np.where(TimeUnit==hhDay)[0])])
                hhDay += dailyDur_In_TimeUnit

            lenInd=max(lenInd,len(Counts[binInd]))
            binInd+=1
        
        Values=np.zeros((Bin,lenInd),dtype=float)

        for k in range(Bin):
            Values[k,:len(Counts[k])]=Counts[k]
        Values = np.sum(Values,axis=0)

        MeanVector[indBin] = np.nanmean(Values)

        MedianVetor[indBin] = np.nanmedian(Values)
        StdErrorVector[indBin] = np.nanstd(Values)/np.sqrt(len(Values))
        indBin+=1
    
    for hind in range(0,len(Hour_Light),Bin):
        hourBin = Hour_Light[hind:hind+Bin]
        Counts = [[]]*Bin
        binInd=0
        lenInd=0
        if hourBin[0]!=hourBin[-1]:
            Label += ['%d-%d'%(hourBin[0],hourBin[-1])]
        else:
            Label += [str(hourBin[0])]

        for hh in hourBin:
            if hh<TimeUnit[0] or hh>TimeUnit[-1]:
                hh+=dailyDur_In_TimeUnit
               
                Counts[binInd] = np.hstack([Counts[binInd],np.nan])
            hhDay = hh
            while hhDay <= TimeUnit[-1]:
                Counts[binInd] = np.hstack([Counts[binInd],len(np.where(TimeUnit==hhDay)[0])])
                hhDay += dailyDur_In_TimeUnit


            lenInd=max(lenInd,len(Counts[binInd]))
            binInd+=1

        Values=np.zeros((Bin,lenInd),dtype=float)
        for k in range(Bin):
            Values[k,:len(Counts[k])]=Counts[k]
        Values = np.sum(Values,axis=0)

        MeanVector[indBin] = np.nanmean(Values)

        MedianVetor[indBin] = np.nanmedian(Values)
        StdErrorVector[indBin] = np.nanstd(Values)/np.sqrt(len(Values))
        indBin+=1
        
    return MeanVector,MedianVetor,StdErrorVector,Label

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
    TrialOnSet=np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    AIT_OnSet=np.where(Y['Action']==TimeStamps['End Intertrial Interval'])[0]
    AIT_OffSet=F_OffSet_GUI(AIT_OnSet,TrialOnSet)
    AIT_OnSet=F_OnSet_GUI(AIT_OffSet,AIT_OnSet)
#    HourStart_AIT=F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,AIT_OnSet,AIT_OffSet,'a',np.inf)[1]
    HourStart_AIT = F_TimeInterval_From_Light_Start(Y,Start_exp,TimeInterval,AIT_OnSet,Light_Start*3600)    
 
    
    #HourStart_AIT=F_Hour_Trial_GUI(Y,TimeStamps,Start_exp,AIT_OnSet,AIT_OffSet,'a',np.inf,24)[1]
    AIT_Dur=Y['Time'][AIT_OffSet]-Y['Time'][AIT_OnSet]
    return(AIT_OnSet,AIT_OffSet,HourStart_AIT,AIT_Dur)
    
def F_AIT_x_Phase_GUI(Y,phase_vect,TimeStamps):
    """
        nuova funzione per ait per phase
    """
    Start_exp=Time_Details_GUI(Y,TimeStamps)[0]
    TrialOnSet=np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    AIT_OnSet=np.where(Y['Action']==TimeStamps['End Intertrial Interval'])[0]
    AIT_OffSet=F_OffSet_GUI(AIT_OnSet,TrialOnSet)
    AIT_OnSet=F_OnSet_GUI(AIT_OffSet,AIT_OnSet)
    AIT_Dur=Y['Time'][AIT_OffSet]-Y['Time'][AIT_OnSet]
    hrs = np.floor((Start_exp+Y['Time'][AIT_OnSet]) / 3600.) % 24
    mean_ph = np.zeros(len(phase_vect))
    median_ph = np.zeros(len(phase_vect))
    std_ph = np.zeros(len(phase_vect))
    ind = 0
    for phase in phase_vect:
        data_h = []
        for h in phase:
            data_h = np.hstack((data_h,AIT_Dur[np.where(hrs == h)[0]]))
        mean_ph[ind] = np.nanmean(data_h)
        median_ph[ind] = np.nanmedian(data_h)
        std_ph[ind] = np.nanstd(data_h)
        ind += 1

    return mean_ph,median_ph,std_ph
    
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
    
def Subj_Median_Mean_Std_GUI(Vectors,HDay,Bias=True,HBin=3600):
    """
    Function Targets:   This function computes the median/mean/std dev of quantities
                        in Vectors for each relative hour of the day
    
    Input:              -Vectors=dictionary, Vectors[key]=vector, timestamps of a
                        certain action
                        -HDay=dictionary, HDay[key][i] = hour from 00:00 of first day of exp
                        in which the action happened
                        
    Output:             -Median/Mean/Std=vector, len =24 ,median/mean/std error of values
                        in Vecors. Median[key][i]=median of all Vector[key] action happened
                        at hour i.
    """
    Median={}
    Mean={}
    Std={}
    if 3600%HBin!=0:
        raise ValueError('3600 must be an integer multiple of HBin')
    Fraction = 3600//HBin
    for key in list(Vectors.keys()):
        Median[key] = np.zeros(24*Fraction)
        Mean[key] = np.zeros(24*Fraction)
        Std[key] = np.zeros(24*Fraction)
        for h in range(24*Fraction):
            Index = np.where((HDay[key]%(24*Fraction))==h)[0]
            Median[key][h] = np.nanmedian(Vectors[key][Index])
            Mean[key][h] = np.nanmean(Vectors[key][Index])
            Std[key][h] = np.nanstd(Vectors[key][Index])/np.sqrt(len(Vectors[key][Index]))
    return(Median,Mean,Std)
    
def daily_Median_Mean_Std_GUI(Vector,HDay,HBin=3600):
    """
    Function Targets:   This function computes the median/mean/std dev of quantities
                        in Vectors for each relative hour of the day
    
    Input:              -Vectors=dictionary, Vectors[key]=vector, timestamps of a
                        certain action
                        -HDay=dictionary, HDay[key][i] = hour from 00:00 of first day of exp
                        in which the action happened
                        
    Output:             -Median/Mean/Std=vector, len =24 ,median/mean/std error of values
                        in Vecors. Median[key][i]=median of all Vector[key] action happened
                        at hour i.
    """
    if 3600%HBin!=0:
        raise ValueError('3600 must be an integer multiple of HBin')
    Fraction = 3600//HBin
    
    Median = np.zeros(24*Fraction)
    Mean = np.zeros(24*Fraction)
    Std = np.zeros(24*Fraction)
    for h in range(24*Fraction):
        Index = np.where((HDay%(24*Fraction))==h)[0]
        Median[h] = np.nanmedian(Vector[Index])
        Mean[h] = np.nanmean(Vector[Index])
        Std[h] = np.nanstd(Vector[Index])/np.sqrt(len(Vector[Index]))
    return(Median,Mean,Std)
    
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
        print(ProbesOn[i],ProbesOff[i])
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

def F_Gr_Switch_Latency_GUI(Datas, TimeStamps, Mouse_Name, H_By_H=False, t0=3,
                            t1=6, Phase='all', scale=1000, Tend=15,
                            Long_Side='r'):
    """
    Function Target:    
    ================
        This function calculate the switching time for all trial of all
        mice and save it in a dictionary.
        
    Be careful, TimeStamps changed to dictionary
    """
    Record_Switch = {}
    HSSwitch = {}
    Latency_x_Hour = {}
    for name in Mouse_Name:
        if type(Long_Side) is dict:
            l_side = Long_Side[name]
        else:
            l_side = Long_Side
        Datas[name] = Rescale_Time_GUI(Datas[name], TimeStamps[name], scale)
        x = Time_Details_GUI(Datas[name], TimeStamps[name])
        print(name)
        Record_SwitchTrial, Active_Trials =\
            F_Record_Switch_Trials_GUI(Datas[name], TimeStamps[name], x[0], x[2],
                                       Long_Side=l_side, Tend=Tend)
        Record_Switch[name], HSSwitch[name] =\
            F_Switch_Analysis_GUI(Record_SwitchTrial, Active_Trials)
        Latency_x_Hour[name] = F_Hour_By_Hour_Binning_GUI(Record_Switch[name],
            HSSwitch[name])
    return(Record_Switch,HSSwitch,Latency_x_Hour)
    
def F_Record_Switch_Trials_GUI(Y,TimeStamps,Start_exp,End_Time,Long_Side='r',Tend=15):
    """
    Function Targets:   This function returns a matrix n x 3 containing times
                        of np in and out and number of trial of every switch 
                        trial
                        
    Input:              -Y= n x 2 dataset
                        -Long_Side=string, 'l'/'r' to indicate if long location
                        is on the left/right hopper
                        -Tend=scalar, max duration of a trial in seconds
                        -Start_exp=scalar, the start of exp, in seconds
                        -End_Time=scalar, time of exp end in seconds
                        
    Output:             -Record_SwitchTrial=dictionary, keys: Short/Long
                            -Record_SwitchTrial['Short']=n x 3 matrix containing 
                        times of np in and out in the short location and number 
                        of the considered trial.
                            -Record_SwitchTrial['Long']=n x 3 matrix containing 
                        times of np in and out in the Long location and number 
                        of the considered trial.
                        -Active_Trials=vector,trials with at least one "np in" 
                        in each location
                        
                        
    """
    Record_SwitchTrial={}
    Record_SwitchTrial['Short']=[]
    Record_SwitchTrial['Long']=[]
    RightRespOn_Trial,RightRespOff_Trial=F_Time_Response_GUI(Y,TimeStamps,Start_exp,End_Time,Location=Long_Side,TrialOnOff=True,tend=Tend)
    Left_NP_in=np.where(Y['Action']==TimeStamps['Left NP In'])[0]
    Left_NP_out=np.where(Y['Action']==TimeStamps['Left NP Out'])[0]
    Right_NP_in=np.where(Y['Action']==TimeStamps['Right NP In'])[0]
    Right_NP_out=np.where(Y['Action']==TimeStamps['Right NP Out'])[0]
    Left_NP_in_Trial=F_InterTrial_Activity_GUI(RightRespOn_Trial,RightRespOff_Trial,Left_NP_in)
    Left_NP_out_Trial=F_InterTrial_Activity_GUI(RightRespOn_Trial,RightRespOff_Trial,Left_NP_out)
    Right_NP_in_Trial=F_InterTrial_Activity_GUI(RightRespOn_Trial,RightRespOff_Trial,Right_NP_in)
    Right_NP_out_Trial=F_InterTrial_Activity_GUI(RightRespOn_Trial,RightRespOff_Trial,Right_NP_out)
    length=len(Right_NP_in_Trial)
    Record_SwitchTrial['Long']=np.array([], dtype={'names':('In','Out','Trial','Hour'),'formats':('f8','f8','int','int')})
    Record_SwitchTrial['Short']=np.array([], dtype={'names':('In','Out','Trial','Hour'),'formats':('f8','f8','int','int')})
    Active_Trials=[]
    Trial_Off = np.where(Y['Action']==TimeStamps['Start Intertrial Interval'])[0]
    if Trial_Off.shape[0] < length:
        Trial_Off = np.hstack((Trial_Off,Y.shape[0]-4))
    for trial in (trial for trial in range(length)):
        
        if (Right_NP_in_Trial[trial] and  Left_NP_in_Trial[trial]):
            Hour_Trial=int(np.floor((Start_exp+Y['Time'][RightRespOn_Trial[trial]])/3600))
            Left_In=Y['Time'][Left_NP_in_Trial[trial]]-Y['Time'][RightRespOn_Trial[trial]]
            Left_Out=Y['Time'][Left_NP_out_Trial[trial]]-Y['Time'][RightRespOn_Trial[trial]]
            Right_In=Y['Time'][Right_NP_in_Trial[trial]]-Y['Time'][RightRespOn_Trial[trial]]
            Right_Out=Y['Time'][Right_NP_out_Trial[trial]]-Y['Time'][RightRespOn_Trial[trial]]
            ## Added recently in case while testing the hopper there is a np out
            ## before an np in in the trial
            Right_Out = Right_Out[np.where(Right_Out >= Right_In[0])[0]]
            if len(Right_Out) == 0:
                Right_Out = np.hstack((Right_Out,Trial_Off[trial]))
            if Right_In[-1] > Right_Out[-1]: 
                Right_In = Right_In[:-1] # LEVO ULTIMO NP IN
            Left_Out = Left_Out[np.where(Left_Out >= Left_In[0])[0]]
            Right_Out = Right_Out[np.where(Right_Out >= Right_In[0])[0]]
            if Left_In[-1] > Left_Out[-1]: 
                Left_In = Left_In[:-1] # LEVO ULTIMO NP IN
#            print 'Right',Right_In,Right_Out
            if Long_Side == 'r':
                Long_In = Right_In
                Long_Out = Right_Out
                Short_In = Left_In
                Short_Out = Left_Out
            elif Long_Side == 'l':
                Long_In = Left_In
                Long_Out = Left_Out
                Short_In = Right_In
                Short_Out = Right_Out
            ###
#            if any(Long_Out) or len(Long_Out) is 0:
#                Long_Out=np.hstack((Long_Out,Long_In[-1]))

            try:  
                Tmp_Short=np.zeros(len(Short_In), dtype={'names':('In','Out','Trial','Hour'),'formats':('f8','f8','int','int')})
                Tmp_Short['In']=Short_In
                Tmp_Short['Out']=Short_Out
                Tmp_Short['Trial']=np.ones(len(Short_In))*trial
                Tmp_Short['Hour']=Hour_Trial*np.ones(len(Short_In))
                Record_SwitchTrial['Short']=np.hstack((Record_SwitchTrial['Short'],Tmp_Short))
                Tmp_Long=np.zeros(len(Long_In), dtype={'names':('In','Out','Trial','Hour'),'formats':('f8','f8','int','int')})
                Tmp_Long['In']=Long_In
                
                Tmp_Long['Out']=Long_Out
                Tmp_Long['Trial']=np.ones(len(Long_In))*trial
                Tmp_Long['Hour']=Hour_Trial*np.ones(len(Long_In))
                Record_SwitchTrial['Long']=np.hstack((Record_SwitchTrial['Long'],Tmp_Long))
                Active_Trials=Active_Trials+[trial]
            except ValueError:
                print('Error in trial %d'%trial)
            
    return(Record_SwitchTrial,Active_Trials)
    
def F_Time_Response_GUI(Y,TimeStamps,Start_exp,End_Time,tend=np.inf,TrialOnOff=False,**kwargs):
    """
    Function Target:        This function calculates the time in sec from start trial
                            pellet released (Reward_Time), the time from the
                            end of midlight signal to the end of trial (Time_response)
                            and the hour of each trial start. It can also return
                            only the values of Onset and Offset of trial you're
                            considering if specifyed.
                
    Input:                  -Y=nx2 dataset
                            -Start_exp=scalar, start time of the experiment 
                            (seconds form midnight before the analysis begins)
                            -End_Time=last NP time (seconds from midnight of 
                            the first day of experiment)
                            -tend=scalar,max duration of a considered trial 
                            (in seconds, default is infinity)
                            -kwargs=dictionary,key='Location'
                                -kwargs['Location']=string, to indicate if the
                                trial we want to consider are right or left hopper.
                            -TrialOnOff=boolean,default False, if true the 
                            the function returns only the indexes of onset/offsets
        
    Output:                 -Reward_Time=vector, times in sec from trial start
                            to pellet release
                            -Time_Response=vector, times in sec from midlight 
                            off to end trial
                            -StartTrial_Hour=vector, hours of the day of every
                            trial start
    """
    if 'Location' in kwargs and kwargs['Location']=='l':
        off=TimeStamps['Give Pellet Left']
    elif 'Location' in kwargs and kwargs['Location']=='r':
        off=TimeStamps['Give Pellet Right']
    elif 'Location' in kwargs and kwargs['Location']=='a':
        off=TimeStamps['Start Intertrial Interval']
    else:
        return()
        
    TrialOnSet=F_Trial_On_Set_GUI(Y,TimeStamps,Protocol='Switch')
#   Find trial offsets of the specifyed trials
    LocationTrialOff=np.where(Y['Action']==off)[0]
#   Find the relative on sets
    LocationTrialOn=F_OnSet_GUI(LocationTrialOff,TrialOnSet)
#   If there are problems of trial cutted.
    LocationTrialOff=F_OffSet_GUI(LocationTrialOn,LocationTrialOff)
#   Keep only trial of duration <=tend
    Reward_Time=Y['Time'][LocationTrialOff]-Y['Time'][LocationTrialOn]
    KeepIndexes=np.where(Reward_Time<=tend)[0]
    LocationTrialOn=LocationTrialOn[KeepIndexes]
    LocationTrialOff=LocationTrialOff[KeepIndexes]
#   If you want only the on and off sets 
    if TrialOnOff==True:
        return(LocationTrialOn,LocationTrialOff)
    Reward_Time=Reward_Time[KeepIndexes]
    
#   Calculate the hour of each trialonset    
    StartTrial_Hour=np.floor((Start_exp*np.ones(len(LocationTrialOn))+Y['Time'][LocationTrialOn])/3600)
#   Calculate the time of response (time between the the mid light off and the 
#   end of the trial).
    MidLightOff=np.where(Y['Action']==20)[0]
    TrialMidLightOff=F_InterTrial_Activity_GUI(LocationTrialOn,LocationTrialOff,MidLightOff,Vector=True)
    Time_Response=Y['Time'][LocationTrialOff]-Y['Time'][TrialMidLightOff]
    
    return(Reward_Time,Time_Response,StartTrial_Hour) 

def F_Trial_On_Set_GUI(Y,TimeStamps,**Protocols):
    """
    Function Target:            This function returns the index of trial On set.
    """
    if (Protocols['Protocol']=='RA' or Protocols['Protocol']=='P' 
            or Protocols['Protocol']=='Exp A' or Protocols['Protocol']=='Switch'):
        TrialOnSet=np.where(Y['Action']==TimeStamps['Center Light On'])[0]
        TrialOnSet=np.array(TrialOnSet,dtype=int)
    return(TrialOnSet)
    
def F_InterTrial_Activity_GUI(TrialOnSet,TrialOffSet,Activity,Vector=False):
    """
    Function Target:        This function calculate the Activity happened 
                            between TrialOnSet[i] and TrialOffSet[i] and save
                            it in ActivitySet[i].
                            
    Input:                  -TrialOnSet=vector, integer, indexes of some trial onset 
                            -TrialOffSet=vector, integer, indexes of some trial offset 
                            
                            IMPORTANT: TrialOffSet[i] must be the offset relative to TrialOnSet[i]
                            
                            -Activity=vector, indexes of some activities
                            -Vector=boolean, if true, it means that 
                                you want a single list and not a list of lists as an
                                output (Default is False)
                                
                            IMPORTANT: Put Vector=True only if there's only 
                            one of the Activity in each trial!!
    
    Output:                 -ActivitySet=list
                            if Vector==True:
                                -ActivitySet[i]=scalar, the only Activity happened between
                                TrialOnSet[i] and TrialOffSet[i]
                            else:
                                -ActivitySet[i]=list of all activity happened between
                                TrialOnSet[i] and TrialOffSet[i]
    """
    ActivitySet=[]
    for ind in range(len(TrialOnSet)):
        ActivitySet=ActivitySet+[[]]
        All_Following_Activity=np.where(Activity>=TrialOnSet[ind])[0]
        if len(All_Following_Activity)>0:
            All_InterTrial_Activity=np.where(Activity[All_Following_Activity]<=TrialOffSet[ind])[0]
            if len(All_InterTrial_Activity)>0:
                Activity=Activity[All_Following_Activity]
                ActivitySet[ind]=list(Activity[All_InterTrial_Activity])
    if Vector==True:
        ActivitySet=[item for sublist in ActivitySet for item in sublist]            
    return(ActivitySet)

def F_Switch_Analysis_GUI(Record_SwitchTrial,Active_Trials,t0=3,t1=6):
    """
    Function targets:   This function calculates the switch times and the hour of
                        the corrisponding trial for every mice.
                        
    Input:              -Record_SwitchTrial=dictionary, 
                            -Record_SwitchTrial['Long']/['Short']=nx3 matrix containing
                            times of np in and out in the long/short location and number 
                            of the considered trial.
                            -Active_Trials=vector,trials with at least one "np in" 
                            in each location
                        -t0/t1=scalar, start/end time of activation of short and long
                        locaiton
                        
    Output:             -Record_Switch=vector, switch latencies in sec from the trial start
                        -HSSwitch=vector, hour in which the switching trial begins.
                        HSSwitch[i]=hour corrisponding to the Record_Switch[i]
                        
    """
    Record_Switch=np.array([])
    HSSwitch=np.array([])
    for trial in Active_Trials:
        Index_Long=np.where(Record_SwitchTrial['Long']['Trial']==trial)[0]
        Index_Short=np.where(Record_SwitchTrial['Short']['Trial']==trial)[0]
        All_Long_Trial=Record_SwitchTrial['Long'][Index_Long]
        All_Short_Trial=Record_SwitchTrial['Short'][Index_Short]
        CheckSW=np.where(All_Short_Trial['Out']<All_Long_Trial['In'][0])[0]
        if any(CheckSW+1):
            CheckSW_RFT=np.where(All_Long_Trial['Out']>All_Short_Trial['Out'][max(CheckSW)])[0]
            TS=All_Long_Trial['In'][CheckSW_RFT[0]]-All_Short_Trial['Out'][CheckSW[-1]]
            if TS<t0+t1:
                Record_Switch=np.hstack((Record_Switch,All_Short_Trial['Out'][CheckSW[-1]]))
                HSSwitch=np.hstack((HSSwitch,All_Short_Trial['Hour'][0]))
    return(Record_Switch,HSSwitch)
    
def F_Hour_By_Hour_Binning_GUI(Record_Switch,HSSwitch):
    """
    Function Target:    This function divides all the switch latencies by the hour
                        of the day in which the trial happens.
                        
    Input:              -Record_Switch=vector, switch latencies in sec from the trial start
                        -HSSwitch=vector, hour in which the switching trial begins
                        
    Output:             -Latency_x_Hour=array of arrays, contains all switch latencies
                        grouped per hour of the day in which they happened.
                            ex. Latency_x_Hour[0]=array, contains all latencies of trials
                            happened at 00:00
                                Latency_x_Hour[7]=array, contains all latencies of trials
                            happened at 07:00...
                                
    """
    Latency_x_Hour=[[]]*24
    HSSwitch24=HSSwitch%24
    i=0
    for h in range(24):
        Ind=np.where(HSSwitch24==h)[0]
        i=i+ len(Ind)
        Latency_x_Hour[h]=Record_Switch[Ind]
    return(Latency_x_Hour)
    
def F_Gr_Fit_GMM_GUI(Record_Switch,Mouse_Grouped,n_gauss=10,FindBest=False):
    """
    Function Target: This function fits the swich latencies of every mice with
                     a mixed gaussian and returns the mixture distr., pdf, cdf, 
                     and empiric cdf.
    
    Input:           -Record_Switch=vector, switch latencies in sec from the trial start
                     -Mouse_Grouped=dictionary, key= group names
                         -Mouse_Grouped[group]=list of mouse names in the group
                     -n_gauss=number of gaussian in the fit you want to use
                     -FindBest=boolean:
                         -True if you look for the best fit
                         between n_gauss summed gaussian 
                         -False if you fix the number of gaussian in the fit
    
    Output:         -Best_Model=dictionary, keys= mouse name
                        Best_Model[name]=object of the class GMM. Gaussian mixture model
                        it fits the Record_Switch[name] vector
                    -Pdf=dictionary, keys = mouse name
                        -Pdf[name]=theorical pdf function for the mixture model
                    -Cdf=dictionary, keys = mouse name
                        -Cdf[name]=theorical cdf function for the mixture model
                    -EmCdf=dictionary, keys = mouse name
                        -EmCdf[name]=vector,empiric cumulative function values
    """
    Best_Model,Pdf,Cdf,EmCdf={},{},{},{}
    for group in list(Mouse_Grouped.keys()):
        for name in Mouse_Grouped[group]:
            Best_Model[name],Pdf[name],Cdf[name],EmCdf[name]=F_Fit_GMM_GUI(Record_Switch[name],n_gauss=n_gauss,FindBest=FindBest) 
    return(Best_Model,Pdf,Cdf,EmCdf)
    
def F_Fit_GMM_GUI(Sample,n_gauss=1,FindBest=False,Ind0=0,SampleSize=10**4):
    """
    Function Target:    This function find the best Gaussian Mixture fit of fixed
                        or variable order (n° of gaussian in the model). It returns
                        the fitted dsitr (object of the class GMM), pdf, cdf and
                        empiric cdf.
    
    Input:              -Sample=vector,the sample we want to approximate
                        -n_gauss=number of gaussian we want to use in the model.
                            if FindBest==False,(default) we fit with a n_gauss GMM
                            if FindBest==True, we fit with the best GMM with 
                            number of gaussians <= n_gauss.
                            (we choose the one that minimize AIC coeff.)
                        - FindBest=boolean, default False, to choose if we want
                        to fix the number of gaussians to n_gauss or if we want
                        to find the best model
                        -Ind0=positive integer, first index of the sample we consider
                        -SampleSize=positive integer, default is 1000, number of samples
                        we want from the fitted distr to find the theoretical cdf.
    """
    Sample=Sample[Ind0:]
    Sample = Sample.reshape((Sample.shape[0],1))
    print(Sample.shape)
    if FindBest:    
        N = np.arange(1, n_gauss)
    else:
        N=[n_gauss]
    models = [None for i in range(len(N))]
    
    for i in range(len(N)):
#        models[i] = mxt.GMM(N[i]).fit(Sample)
        models[i] = mxt.GaussianMixture(N[i]).fit(Sample)
    
    # compute the AIC and the BIC
    AIC = [m.aic(Sample) for m in models]
    #BIC = [m.bic(X) for m in models]
    # find the best models (the one that minimize AIC)
    Best_Model=models[np.argmin(AIC)]
    
    x=np.linspace(min(Sample)-0.1*np.abs(min(Sample)),max(Sample)+0.1*np.abs(max(Sample)),1000)
    x = x.reshape((x.shape[0],1))    
    # compute log probabilities
    logprob = np.zeros(x.shape[0])
    for k in range(x.shape[0]):
        logprob [k] = Best_Model.score(x[k].reshape((1,1)))
    # compute theoretical pdf 
    Pdf={}
    Pdf['x']=x.flatten()
    Pdf['y']=np.exp(logprob)
    # compute theoretical cdf
    Cdf={}
    Model_Sample=Best_Model.sample(SampleSize)[0].reshape(-1,)
    Model_Sample_Ord=np.sort(Model_Sample)

    NormCum = np.arange(len(Model_Sample_Ord),dtype=float)/len(Model_Sample_Ord)
    Cdf['x']=Model_Sample_Ord
    Cdf['y']=NormCum
    # compute empiric Cdf
    EmCdf={}
    Sample_Ord=np.sort(Sample.flatten())

    NormCum = np.arange(len(Sample_Ord),dtype=float)/len(Sample_Ord)
    EmCdf['x']=Sample_Ord
    EmCdf['y']=NormCum 
    return(Best_Model,Pdf,Cdf,EmCdf)
    
def Gr_Mean_Std_GUI(Vector,Groups):
    """
    Function Target: 
    ----------------
       This function calculates the mean and std dev of values in Vector.
                            
    Input:                  -Vector = dictionary, keys = mouse name
                                Vector[name] = array of length 24
                            -Groups = dictionary, keys = group names
                                Groups[group] = list, names of mice in each group
                        
    Output:                 -Mean= dictionary, keys = group names
                                -Mean[groupname]=means relative to the group "groupname"
                            -Std=dictionary, keys = group names
                                -Std[groupname]=biased empirical std error 
                                (divided by N) relative to the group "groupname"
    """
    Matrix={}
    Mean={}
    Std={}
    for name in list(Groups.keys()):
        if not len(Groups[name]):
            continue
        Matrix[name]=np.zeros(len(Vector[list(Vector.keys())[0]]))
        for subject in Groups[name]:
            Matrix[name]=np.vstack((Matrix[name],Vector[subject]))
        Matrix[name]=Matrix[name][1:,:]
        Mean[name]=np.nanmean(Matrix[name],axis=0)
        Std[name]=np.nanstd(Matrix[name],axis=0)
    return(Mean,Std)    

def F_OutSideTrial_Activity_GUI(TrialOnSet,TrialOffSet,Activity):
    """
    Function Target:
        This function keeps the Acitivity elements which are outside the interval
        [ TrialOnSet[i], TrialOffSet[i] ] for all i=0,...,len(TrialOnSet)
        
    Input:
        - TrialOnSet=vector, usually containing indexes of trial onset
        - TrialOffSet=vector, usually containing indexes of trial offset
    
    Output:
        - OutSideActivity=vector, subset of Activity taking only elements 
        specified in the function target
        - OTA=list of vectors, \n
            OTA[0]=all Activity lower then TrialOnSet[0]\n
            OTA[i]=all Activity n t.c. TrialOffSet[i]<n<TrialOnSet[i+1], for all i=1,...,len(OTA)-2\n
            OTA[-1]=all Activity element greater then TrialOffSet[-1]\n
    
    IMPORTANT: len(TrialOnSet)=len(TrialOffSet) & \n
                TrialOnSet[i]<TrialOffSet[i]<TrialOnSet[i+1]
    """
    InitialOutSideActivity = Activity[np.where(Activity<TrialOnSet[0])[0]]
    OutsideTrialActivity = [[]]*(len(TrialOnSet)+1)
    OutsideTrialActivity[0] = np.hstack((OutsideTrialActivity[0],InitialOutSideActivity))
    
    BetweenOutSideActivity=[]
    for index in range(len(TrialOnSet[1:])):
        TmpActivity = Activity[np.where(Activity<TrialOnSet[index])[0]]
        TmpActivity = TmpActivity[np.where(TmpActivity>TrialOffSet[index-1])[0]]
        BetweenOutSideActivity = np.hstack((BetweenOutSideActivity,TmpActivity))
        OutsideTrialActivity[index] = np.hstack((OutsideTrialActivity[index],TmpActivity))
    
    FinalOutSideActivity = Activity[np.where(Activity>TrialOffSet[-1])[0]]
    
    AllOutSideActivity = np.hstack((InitialOutSideActivity,
                                    BetweenOutSideActivity,
                                    FinalOutSideActivity))
    OutsideTrialActivity[-1]=np.hstack((OutsideTrialActivity[-1],FinalOutSideActivity))
    
    return AllOutSideActivity,OutsideTrialActivity
    
def Extracting_Data_GUI(Y,TimeStamps,Actions,TrialOn,TrialOff,TimeInterval=3600,InOutAll='All',TimeToConsider=np.inf):
    """
    Function Target:
        This Function extract info about the activity in Actions, considering\n 
        all/inside trial/outside trial activity. The info you can get is the\n 
        index of the activity in Y, the time in sec of the activity, the hour\n
        of the activity since 00:00 of 1st day of exp, the code of action\n
        and the hour in which the action is done
    
    Input:
        - Y = nx2 dataset
        - TimeStamps = dictionary, label = time stamp action, value = time stamp code
        - Actions = list of TimeStamps labels
        - TrialOn/Off = trial on/off label (must be one label in TimeStamps)
        - InOutTrial = string, 'Out','In','All', to specify if we consider actions\n
        outside trial/inside trial or all actions
        - TimeToConsider = scalar, sec of trial that we want to consider, starting\n
        from the beginning of the trial
        
    Output:
        - OrderedActions = matrix\n
            OrderedActions['Action'][i] = code of action i\n
            OrderedActions['Time'][i] = seconds from start exp in which action i\n
            took place
            OrderedActions['Hour'][i] = hour from midnight of 1st day of experiment\n
            in which action i took place
            OrderedActions['Trial'][i] = (Only for InOutAll equal to In or OuT)\n
            scalar, contains the number of the trial in which action i took place
    """
    AllCodes = [TimeStamps[Actions[i]] for i in range(len(Actions))]
    Start_exp = F_Start_exp_GUI(Y,TimeStamps)
    if InOutAll=='All':
        OrderedActions=np.array([], dtype={'names':('Action','Time','Hour','Index','Bins_Unit'),'formats':(int,float,'S5',int,int)})
        
        for code in AllCodes:
            ActionCodeIndex=np.where(Y['Action']==code)[0]
            ActionCodeTime = Y['Time'][ActionCodeIndex]
            ActionCodeInterval = F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,ActionCodeIndex,0,'a',np.inf)[1]
            CodeOrderedAction = np.zeros(len(ActionCodeIndex),dtype={'names':('Action','Time','Hour','Index','Bins_Unit'),'formats':(int,float,'S5',int,int)})
            CodeOrderedAction['Action'] = code
            CodeOrderedAction['Time'] = ActionCodeTime
            CodeOrderedAction['Index'] = ActionCodeIndex
            CodeOrderedAction['Bins_Unit'] = ActionCodeInterval
            Hour=((ActionCodeInterval*TimeInterval)//3600)%24
            Minute=((ActionCodeInterval*TimeInterval)//60)%60
            for ind in range(len(Hour)):
                hour=Hour[ind]
                minute=Minute[ind]
                if minute<10:
                    string='%d:0%d'%(hour,minute)
                else:
                    string='%d:%d'%(hour,minute)
                CodeOrderedAction['Hour'][ind]=string

            OrderedActions = np.hstack((OrderedActions,CodeOrderedAction))
        OrderedActions = np.sort(OrderedActions,order='Index')
        
        
    elif InOutAll=='In' or InOutAll=='Out':
        TrialOnSet = np.where(Y['Action']==TimeStamps[TrialOn])[0]
        TrialOffSet = np.where(Y['Action']==TimeStamps[TrialOff])[0]
        TrialOffSet = F_OffSet_GUI(TrialOnSet,TrialOffSet)
        TrialOnSet = F_OnSet_GUI(TrialOffSet,TrialOnSet)
        
        KeepIndex = np.where(Y['Time'][TrialOffSet]-Y['Time'][TrialOnSet]<=TimeToConsider)[0]
        TrialOnSet=TrialOnSet[KeepIndex]
        TrialOffSet=TrialOffSet[KeepIndex]
        
        Activity=[]

        #raw_input("Press enter to continue")
        for code in AllCodes:
            Activity = np.hstack((Activity,np.where(Y['Action']==code)[0]))
        Activity = np.sort(Activity)
        if InOutAll=='In':
            TrialActivity = F_InterTrial_Activity_GUI(TrialOnSet,TrialOffSet,Activity)
            OrderedActions = np.array([],dtype={'names':('Action','Second','Time','Index','Bins_Unit','Trial'),
                                            'formats':(int,float,'S5',int,int,int)})
            trialnum=0
            for trialIndex in TrialActivity:
                
                TrialAction = np.array(np.zeros(len(trialIndex)),dtype={'names':('Action','Second','Time','Index','Bins_Unit','Trial'),
                                            'formats':(int,float,'S5',int,int,int)})
                trialIndex=np.array(trialIndex,dtype=int)
                TrialAction['Second']=Y['Time'][trialIndex]
                TrialAction['Index']=trialIndex
                TrialAction['Action']=Y['Action'][trialIndex]
                TrialAction['Trial']=trialnum
                TrialAction['Bins_Unit']=F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,trialIndex,0,'a',np.inf)[1]
                Hour=((TrialAction['Bins_Unit']*TimeInterval)//3600)%24
                Minute=((TrialAction['Bins_Unit']*TimeInterval)//60)%60
                for ind in range(len(trialIndex)):
                    hour=Hour[ind]
                    minute=Minute[ind]
                    if minute<10:
                        string='%d:0%d'%(hour,minute)
                    else:
                        string='%d:%d'%(hour,minute)
                    TrialAction['Time'][ind]=string
                trialnum+=1
                OrderedActions = np.hstack((OrderedActions,TrialAction))
        else:
            TrialActivity = F_OutSideTrial_Activity_GUI(TrialOnSet,TrialOffSet,Activity)[1]
            OrderedActions = np.array([],dtype={'names':('Action','Second','Time','Following Trial','Bins_Unit','Index'),
                                            'formats':(int,float,'S5',int,int,int)})
            trialnum=0
            for trialIndex in TrialActivity:
                
                TrialAction = np.array(np.zeros(len(trialIndex)),dtype={'names':('Action','Second','Time','Following Trial','Bins_Unit','Index'),
                                                                        'formats':(int,float,'S5',int,int,int)})
                trialIndex=np.array(trialIndex,dtype=int)
                TrialAction['Second']=Y['Time'][trialIndex]
                TrialAction['Index']=trialIndex
                TrialAction['Action']=Y['Action'][trialIndex]
                TrialAction['Following Trial']=trialnum
                TrialAction['Bins_Unit']=F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,trialIndex,0,'a',np.inf)[1]
                Hour=((TrialAction['Bins_Unit']*TimeInterval)//3600)%24
                Minute=((TrialAction['Bins_Unit']*TimeInterval)//60)%60
                for ind in range(len(trialIndex)):
                    hour=Hour[ind]
                    minute=Minute[ind]
                    if minute<10:
                        string='%d:0%d'%(hour,minute)
                    else:
                        string='%d:%d'%(hour,minute)
                    TrialAction['Time'][ind]=string
                trialnum+=1
                OrderedActions = np.hstack((OrderedActions,TrialAction))
        
    
    return OrderedActions
    
def Average_TotalActivity_Matrix_GUI(Dataset,Bin_Column_Label,HBin,Groups=None,Extract=['Mean']):
    """
    Function Target:
    ----------------
        This function extract daily statistics for the activity in Dataset which
        is of the form of extracted timestamps.
    Input:
    ------
        - Dataset = dictionary of Extracted Time Stamps datasets or in general of structured
            array with a column of time unit corrisponding to a certain action
        - Bin_Column_Label = stirng, the label of the time bin column
        - HBin = int, number of seconds of each time bin. (900=15min binning...)
        - Groups = list of group names
        - Extract = list of stings, stat to extract. It can be: 'Mean','Median','Std Error'
    Output:
    -------
        - Matrix = structured array containing the daily stat of each subj
        - listNames = the list of the column of Matrix that contians the stats 
            (the other columns are for the groups,subjsets and type of stat)
        
    """
    Subjects = list(Dataset.keys())
    tmpDict = {}
    for key in Subjects:
        tmpDict[key] = Dataset[key][Bin_Column_Label]
    

    TotActivity = OrderedDict()
    ActivityBin = OrderedDict()    
    TotExtractedParameters = len(Extract)    
    
    for key in list(Dataset.keys()):
        Activity_x_Bin = np.array(F_Activity_x_Hour_All_GUI(Dataset[key][Bin_Column_Label]))
        Hour_0=int(Dataset[key][Bin_Column_Label][0])
        Activity_x_Bin=Activity_x_Bin[Hour_0:]
        TotActivity[key] = Activity_x_Bin
        ActivityBin[key] = np.arange(Hour_0,Dataset[key][Bin_Column_Label][-1]+1)
        
    Median,Mean,Std=Subj_Median_Mean_Std_GUI(TotActivity,ActivityBin,Bias=False,HBin=HBin)
    
    ListOfParam=[]
    for name in Extract:
        if name == 'Mean':
            ListOfParam+=[Mean]
        elif name == 'Median':
            ListOfParam+=[Median]
        elif name == 'Std Error':
            ListOfParam+=[Std]
    
    if Groups:
        lenName=0
        for group in list(Groups.keys()):
            lenName = max(lenName,len(str(group)))
        listNames=['Group','Subject','Stat']
        tupleTypes=['|S%d'%lenName,int,'|S9']
    else:
        listNames=['Subject','Stat']
        tupleTypes=[int,'|S9']
    for k in range((3600*24)//HBin):
        listNames+=['Time_%d'%k]
        tupleTypes+=[float]
        
    tupleNames=tuple(listNames)
    tupleTypes=tuple(tupleTypes)
    Matrix = np.zeros(len(Subjects)*TotExtractedParameters,dtype={'names':tupleNames,'formats':tupleTypes})
    ind=0
    
    if Groups:
        for group in list(Groups.keys()):
            for subject in Groups[group]:
                for k in range(TotExtractedParameters):
                    Matrix[ind+k] = tuple(np.hstack((group,subject,Extract[k],ListOfParam[k][subject])))
                    
                ind += TotExtractedParameters  
    return Matrix,listNames

def Average_TotalActivity_Matrix_Analyze_GUI(Matrix,GroupColLabel,StatColLabel,MeanOrMedian='Mean',
                                         TimeBinning_sec=3600,Dark_Start=20,
                                         Dark_Len=12,listNames=None,factorIndexes=[0,1,2]):
    """
    Function Target:
    ----------------
        This function averages subjective values extracted using the function
        Average_TotalActivity_Matrix_GUI over the different groups
    Input:
    ------
        - Matrix = structured array containing the extracted statistics
        - GroupColLabel = label of the column containing group names
        - StatColLabel = label of the column containing the stat type
        - MeanOrMedian = string to decide if you want to average the mean value
            or the median
        - Time_Binning_sec = int, number of sec of each time bin
        - Dark_Start = int, hour in which darkphase starts
        - Dark_Len = int, number of hour in dark phase
        - listNames = name of the time Bin cols
        - factorIndexes = list of int, index of factor cols
    Output:
    -------
        - MeanMatrix = matrix containing group averages
        - StdErrorMatrix = matrix contianing group std errors
        - Reorder_Vector = vector for reordering time bins to have first the dark
            phase and then the light phase means
    """
    if listNames is None:
       listNames =  list(Matrix.dtype.names)
    for ind in factorIndexes[::-1]:
        listNames.pop(ind)
    ListGroup=[]
    for group in Matrix[GroupColLabel]:
        if group not in ListGroup:
           ListGroup+=[group]
    IndexStat = np.where(Matrix[StatColLabel]==MeanOrMedian)[0]
    Matrix = Matrix[IndexStat]
    size=len(IndexStat),len(listNames)
    ArrayMatrix = np.zeros(size,dtype=float)
    
    
    for k in range(size[0]):
        ArrayMatrix[k,:] = list(Matrix[listNames][k])

        k+=1
    Dark_Bin,Light_Bin=Hour_Light_and_Dark_GUI(Dark_Start,Dark_Len,TimeBinning_sec)
    Reorder_Vector = np.hstack([Dark_Bin,Light_Bin])
    MeanMatrix = np.zeros(size[1],dtype={'names':tuple(ListGroup),'formats':(float,)*len(ListGroup)})
    StdErrorMatrix = np.zeros(size[1],dtype={'names':tuple(ListGroup),'formats':(float,)*len(ListGroup)})
    for group in ListGroup:
        grIndex=np.where(Matrix[GroupColLabel]==group)[0]
        MeanMatrix[group] = np.mean(ArrayMatrix[grIndex],axis=0)
        StdErrorMatrix[group] = np.std(ArrayMatrix[grIndex],axis=0)/np.sqrt(len(grIndex))
    return MeanMatrix,StdErrorMatrix,Reorder_Vector
    
def F_FitSin_GUI(Vector,amplitude0,phase0,translation0,period0=24,MaxIter=1000):
    """
    Function Target:
        This function computes a sin fit of the vector Vector.
        
    Input: 
        - Vector = the 1D array we want to fit\n
        - amplitude0 = scalar,starting amplitude for the approx. algorithm\n
        - phase0 = scalar,starting phase for the approx. algorithm\n
        - translation0 = scalar,starting horizontal translation for the approx. algorithm\n
        - period0 = scalar, starting period for the approx. algorithm\n
        - MaxIter = integer,max iteration for the approx. algorithm
    
    Output:
        - F = vector with the sinusoidal fit\n
        - popt = list, all the fitted paramethers (amplitude, period, phase,translation)\n
        - corr = scalar,pearson correlaiton coefficient between sinfit and Vector
        - p_value = scalar, p-value relative to the pearson coefficient corr 
    """
    x = np.arange(0,len(Vector),1)
    p0 = [amplitude0, period0, phase0, translation0] #ampiezza, periodo, fase, traslazione y

    popt, pcov = curve_fit(fit_sin, x, Vector, p0,np.std(Vector))
    
    for i in np.arange(0,MaxIter):
        popt, pcov = curve_fit(fit_sin, x, Vector, popt,np.std(Vector))
    
    F = fit_sin(x,popt[0],popt[1],popt[2],popt[3])
    corr,p_value=sts.pearsonr(Vector,F)

    
    return F,popt,corr,p_value

def Extracting_Latencies_GUI(Y,TimeStamps,Action_A,Action_B,TrialOn,TrialOff,InOutAll='All',TimeInterval=3600,TimeToConsider=np.inf):
    Action_A_Code = TimeStamps[Action_A]
    Action_B_Code = TimeStamps[Action_B]
    Start_exp = F_Start_exp_GUI(Y,TimeStamps)
    ActionCodeIndex_A=np.where(Y['Action']==TimeStamps[Action_A])[0]
    ActionCodeIndex_B=np.where(Y['Action']==TimeStamps[Action_B])[0]
    
    if ActionCodeIndex_A[0]>ActionCodeIndex_B[0]:
            ActionCodeIndex_B=ActionCodeIndex_B[1:]
    if ActionCodeIndex_A[-1]>ActionCodeIndex_B[-1]:
            ActionCodeIndex_A = ActionCodeIndex_A[:-1]
    
#    if len(ActionCodeIndex_A)==len(ActionCodeIndex_B)+1:
#        if ActionCodeIndex_A[0]>ActionCodeIndex_B[0]:
#            ActionCodeIndex_B=ActionCodeIndex_B[1:]
#        elif ActionCodeIndex_A[-1]>ActionCodeIndex_B[-1]:
#            ActionCodeIndex_A = ActionCodeIndex_A[:-1]
#        else:
#            raise ValueError,'Action A and B must be coupled.'
            
            
    if np.abs(len(ActionCodeIndex_A)-len(ActionCodeIndex_B))>0:
        raise ValueError('Action A and B must be coupled.')
    
    
    if InOutAll=='All':
        

        ActionCodeTime_A = Y['Time'][ActionCodeIndex_A]
        ActionCodeTime_B = Y['Time'][ActionCodeIndex_B]
        ActionCodeHour_A = F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,ActionCodeIndex_A,0,'a',np.inf)[1]
                        
        Latency = ActionCodeTime_B-ActionCodeTime_A  
        
        OrderedActions = np.zeros(len(ActionCodeIndex_A),
                                  dtype={'names':('Action A','Action B','Latency','Hour','Time A',
                                  'Time B','Index A','Index B','Bins_Unit'),
                                  'formats':(int,int,float,'S5',float,float,int,int,int)})
        OrderedActions['Action A'] =  Action_A_Code
        OrderedActions['Action B'] =  Action_B_Code
        OrderedActions['Time A'] = ActionCodeTime_A
        OrderedActions['Time B'] = ActionCodeTime_B
        OrderedActions['Index A'] = ActionCodeIndex_A
        OrderedActions['Index B'] = ActionCodeIndex_B
        OrderedActions['Bins_Unit'] = ActionCodeHour_A
        OrderedActions['Latency'] = Latency
        Hour=((ActionCodeHour_A*TimeInterval)//3600)%24
        Minute=((ActionCodeHour_A*TimeInterval)//60)%60
        for ind in range(len(Hour)):
            hour=Hour[ind]
            minute=Minute[ind]
            if minute<10:
                string='%d:0%d'%(hour,minute)
            else:
                string='%d:%d'%(hour,minute)
            OrderedActions['Hour'][ind]=string
        
    elif InOutAll=='In' or InOutAll=='Out':
        
        TrialOnSet = np.where(Y['Action']==TimeStamps[TrialOn])[0]
        TrialOffSet = np.where(Y['Action']==TimeStamps[TrialOff])[0]
        TrialOffSet = F_OffSet_GUI(TrialOnSet,TrialOffSet)
        TrialOnSet = F_OnSet_GUI(TrialOffSet,TrialOnSet)
        KeepIndex = np.where(Y['Time'][TrialOffSet]-Y['Time'][TrialOnSet]<=TimeToConsider)[0]
        TrialOnSet = TrialOnSet[KeepIndex]
        TrialOffSet = TrialOffSet[KeepIndex]
        
        if InOutAll=='In':
            TrialActivity_A = F_InterTrial_Activity_GUI(TrialOnSet,TrialOffSet,ActionCodeIndex_A)
            TrialActivity_B = F_InterTrial_Activity_GUI(TrialOnSet,TrialOffSet,ActionCodeIndex_B)
        
            OrderedActions = np.array([],
                                  dtype={'names':('Action A','Action B','Latency','Hour','Trial','Time A',
                                  'Time B','Index A','Index B','Bins_Unit'),
                                  'formats':(int,int,float,'S5',int,float,float,int,int,int)})
        else:
            TrialActivity_A = F_OutSideTrial_Activity_GUI(TrialOnSet,TrialOffSet,ActionCodeIndex_A)[1]
            TrialActivity_B = F_OutSideTrial_Activity_GUI(TrialOnSet,TrialOffSet,ActionCodeIndex_B)[1]
            
            OrderedActions = np.array([],
                                  dtype={'names':('Action A','Action B','Latency','Hour','Following Trial',
                                                  'Time A','Time B','Index A','Index B','Bins_Unit'),
                                  'formats':(int,int,float,'S5',int,float,float,int,int,int)})
            
                        
        for trialNum in range(len(TrialActivity_A)):

            if not (len(TrialActivity_B[trialNum]) and len(TrialActivity_A[trialNum])):
                continue
            
            TrialAction_A=np.array(TrialActivity_A[trialNum],dtype=int)
            TrialAction_B=np.array(TrialActivity_B[trialNum],dtype=int)
            
            
            if TrialAction_A[-1]>TrialAction_B[-1]:
                TrialAction_A = TrialAction_A[:-1]
            elif  TrialAction_A[0]>TrialAction_B[0]:
                TrialAction_B = TrialAction_B[1:]
            
            ActionCodeTime_A = Y['Time'][TrialAction_A]
            ActionCodeTime_B = Y['Time'][TrialAction_B]
            ActionCodeHour_A = F_TimeInterval_Trial_GUI(Y,TimeStamps,Start_exp,TimeInterval,TrialAction_A,0,'a',np.inf)[1]
            Latency = ActionCodeTime_B-ActionCodeTime_A 
            if InOutAll=='In':
                
                TmpOrderedActions = np.zeros(len(TrialAction_A),
                                  dtype={'names':('Action A','Action B','Latency','Hour','Trial','Time A',
                                  'Time B','Index A','Index B','Bins_Unit'),
                                  'formats':(int,int,float,'S5',int,float,float,int,int,int)})
            else:
                
                TmpOrderedActions = np.zeros(len(TrialAction_A),
                                  dtype={'names':('Action A','Action B','Latency','Hour','Following Trial',
                                                  'Time A','Time B','Index A','Index B','Bins_Unit'),
                                  'formats':(int,int,float,'S5',int,float,float,int,int,int)})
            TmpOrderedActions['Action A'] =  Action_A_Code
            TmpOrderedActions['Action B'] =  Action_B_Code
            TmpOrderedActions['Time A'] = ActionCodeTime_A
            TmpOrderedActions['Time B'] = ActionCodeTime_B
            TmpOrderedActions['Index A'] = TrialAction_A
            TmpOrderedActions['Index B'] = TrialAction_B
            TmpOrderedActions['Bins_Unit'] = ActionCodeHour_A
            TmpOrderedActions['Latency'] = Latency
            if InOutAll=='In':
                TmpOrderedActions['Trial'] = trialNum
            else:
                TmpOrderedActions['Following Trial'] = trialNum
            Hour=((TmpOrderedActions['Bins_Unit']*TimeInterval)//3600)%24
            Minute=((TmpOrderedActions['Bins_Unit']*TimeInterval)//60)%60
            for ind in range(len(Latency)):
                hour=Hour[ind]
                minute=Minute[ind]
                if minute<10:
                    string='%d:0%d'%(hour,minute)
                else:
                    string='%d:%d'%(hour,minute)
                TmpOrderedActions['Hour'][ind]=string
            OrderedActions = np.hstack((OrderedActions,TmpOrderedActions))
            
       
        
    return OrderedActions
    
def fit_sin_GUI(x,b1,b2,b3,b4):
    return b1*np.sin(2*np.pi*(1/b2)*x+b3)+b4
    
def FoodEaten_x_Day_GUI(Y,TimeStamps):
    """
    Function Target:    
        This Function calculates the number of pellet eaten each exp day.
        Must use scaled dataset!
    Input:
        -Y= nx2 dataset
        -FoodLeft/Right=scalar, the label of give pellet left/right
    Output:
        -TotDailyFood=vector, one element per day of experiment, 
            TotDailyFood[i]=tot food eaten the i-esim day
    """
    Start_exp = F_Start_exp_GUI(Y,TimeStamps)
    AllFoodLeft = np.where(Y['Action']==TimeStamps['Give Pellet Left'])[0]
    AllFoodRight = np.where(Y['Action']==TimeStamps['Give Pellet Right'])[0]
    AllFood=np.sort(np.hstack((AllFoodLeft,AllFoodRight)))
    HourFood = F_Hour_Trial_GUI(Y,TimeStamps,Start_exp,AllFood,0,'a',np.inf,24)[1]
    N_Day =int( max(HourFood) // 24  + 1)

    TotDailyFood=np.zeros(N_Day)
    for day in np.arange(N_Day,dtype=int):
        Ind0 = np.where(HourFood>=day*24)[0][0]
        Ind1 = np.where(HourFood<(day+1)*24)[0][-1]
        DailyFood = AllFood[Ind0:min(Ind1+1,len(AllFood))]
        TotDailyFood[day]=len(DailyFood)
    return TotDailyFood
    
def Food_X_TimeInterval_GUI(Y,TimeStamps,Start_exp,TimeInterval,Side='All'):
    """
    Function Target:
        This Function returns the food eaten per interval of time.
        
    """
    if Side == 'All':
        FoodRecieved=np.where(Y['Action']==TimeStamps['Give Pellet Left'])[0]
        FoodRecieved=np.sort(np.hstack((FoodRecieved,np.where(Y['Action']==TimeStamps['Give Pellet Right'])[0])))
    elif Side=='Left':
       FoodRecieved=np.where(Y['Action']==TimeStamps['Give Pellet Left'])[0] 
    elif Side=='Right':
        FoodRecieved=np.where(Y['Action']==TimeStamps['Give Pellet Right'])[0]
    
   
    FoodEatenInterval=F_TimeInterval_Trial(Y,Start_exp,TimeInterval,FoodRecieved,0,'a',np.inf)[1]
    FoodEatenPerTimeInterval=F_Activity_x_TimeInterval(FoodEatenInterval,TimeInterval)
    
    return FoodEatenPerTimeInterval

def F_Probe_Trials_GUI(Y, TimeStamps,Start_exp,End_Time,Probe_Side='r',Tend=np.inf,
                       TimeInterval = 3600, ProbesOn=None, ProbesOff=None):
    """
    Function Target:    This function calculates the time of nose poke in and
                        out in every probe trial of a specified side of the hopper.
                        
    Input:              -Y=nx2 dataset
                        -Start_exp = scalar, second from 00:00 of the first day
                        of experiment
                        -End_Time = last NP time (seconds from midnight of the first
                        day of experiment)
                        -Probe_Side = string, 'l'/'r' to specified the side of the
                        hopper we consider. l=left, r=right
                        -Tend = scalar, max duration of the trial. If the trial
                        last for more than Tend it's not considered
                        
    Output:             -Probes_Trial=5xn' matrix, contains np in and out times,
                        sec from start trial, the index and the hour
                        of the start of the trial and the number of each trial.
    """
    
#   With this function we calculate probes on and off in the specified hopper
    print('TEND in probes extract',Tend) 
    if not ProbesOn:
        ProbesOn,ProbesOff = F_Probes_x_TimeInterval_GUI(Y,TimeStamps,Start_exp,End_Time,Probe_Side,tend=Tend)
        print('MAX trial len', np.max(Y['Time'][ProbesOff]-Y['Time'][ProbesOn]))
#   Here we save the hour start for each trial
    Hour_Start_Trial = F_TimeInterval_Trial_GUI(Y, TimeStamps, Start_exp, 
                                                TimeInterval, ProbesOn, [],
                                                'a', Tend)[1]
    
#   Here we extract all activity:
    if Probe_Side=='l':
        NP_in = np.where(Y['Action']==23)[0]
        NP_out = np.where(Y['Action']==24)[0]
    elif Probe_Side=='r':
        NP_in = np.where(Y['Action']==27)[0]
        NP_out = np.where(Y['Action']==28)[0]
        
#   With this function I extract the inter trial activity of each probe trial
    Intertrial_In = F_InterTrial_Activity_GUI(ProbesOn,ProbesOff,NP_in,Vector=False)
    Intertrial_Out = F_InterTrial_Activity_GUI(ProbesOn,ProbesOff,NP_out,Vector=False)
    
    if (len(ProbesOn) != len(Intertrial_In)) or (len(ProbesOn)!=len(Intertrial_Out)):
        raise ValueError('ProbesOn,Intertrial_In and Intertrial_Out must have the same dimension')
    
#   Here we creatre a matrix that contains the second of the np in and out from
#   the start of the trial, the trial index and the hour of the trial   
    Probe_Trial = np.array([], dtype={'names':('In','Out','Index','Hour','Trial'),'formats':('f8','f8','int','int','int')})
        
    for i in range(len(ProbesOn)):
        
#   The Length of a trial activity is at most the lenght of np out. With incomplete
#   trials, that has one more np in than out, we consider last np out as the
#   last time stamp of the probe trial.
              
        Length_Trial=len(Intertrial_In[i])

        

        Temp = np.zeros(Length_Trial,dtype={'names':('In','Out','Index','Hour','Trial'),'formats':('f8','f8','int','int','int')})
        Temp['In'] = Y['Time'][Intertrial_In[i]]-Y['Time'][ProbesOn[i]]
        
        try:
            if Length_Trial>len(Intertrial_Out[i]):
                Index=np.hstack((Intertrial_Out[i],ProbesOff[i]))
                Temp['Out'] = Y['Time'][Index]-Y['Time'][ProbesOn[i]]
            elif Intertrial_Out[i][0]<Intertrial_In[i][0]:
                Intertrial_Out[i] = Intertrial_Out[i][1:]
            else:            
                Temp['Out'] = Y['Time'][Intertrial_Out[i]]-Y['Time'][ProbesOn[i]]
        except ValueError:
            return Intertrial_In[i],Intertrial_Out[i], ProbesOn[i]


        Temp['Index'] = ProbesOn[i]*np.ones(Length_Trial)
        Temp['Hour'] = Hour_Start_Trial[i]*np.ones(Length_Trial)
        Temp['Trial'] = i*np.ones(Length_Trial)
        Probe_Trial = np.hstack((Probe_Trial,Temp))
        
    return(Probe_Trial)

def F_binning_GUI(Probe_Trial,Delta,Fuat_Like=False):
    Maxtrial=Probe_Trial['Trial'][-1]
    Delta_Int=OrderedDict()
    for trial in range(Maxtrial+1):
        Delta_Int[trial]=[]
        Temp=Probe_Trial[np.where(Probe_Trial['Trial']==trial)[0]]
        for ind in range(len(Temp)):
            if not Fuat_Like:
                Delta_Int[trial]=Delta_Int[trial]+[np.hstack((np.arange(Temp['In'][ind],Temp['Out'][ind],Delta),Temp['Out'][ind]))]       
            else:
                Delta_Int[trial]=Delta_Int[trial]+[np.arange(Temp['In'][ind],Temp['Out'][ind],Delta)]
    return(Delta_Int)

def F_StartStop_Fuat_GUI(Delta_Int):
    Trials = list(Delta_Int.keys())
    Trial_Number = len(Trials)
    StartStop = np.zeros((Trial_Number,2))*np.nan
    for n in Trials:
        Temp_Data = np.hstack((0,np.hstack(Delta_Int[n])))
        print(n, len(Temp_Data))
        if len(Temp_Data)<=2:
            continue
        
        Differences = np.diff(Temp_Data)
        y = Differences-np.nanmean(Differences)
        Cum_y = np.cumsum(y)
        TmpCum=Cum_y
        try:
            Ind_Stop = np.argmin(Cum_y)+1
            Ind_Start = np.argmax(Cum_y[:Ind_Stop-1])+1
        except ValueError:
            continue
        StartStop[n,:] = [Temp_Data[Ind_Start],Temp_Data[Ind_Stop]]
    return(TmpCum,Ind_Start,Ind_Stop,StartStop)

def intConv(x):
    return int(x)

#def dateConvertion(dateString):
#    vectIntConv = np.vectorize(intConv)
#    Date = vectIntConv(dateString[:10].split('/'))[::-1]
#    Time = vectIntConv(dateString[11:].split(':'))
#    DateTime = np.hstack((Date, Time))
#    return datetime.datetime(*DateTime)

def vectDateConvertion(List):
    func = np.vectorize(dateConvertion)
    return func(List)

def F_PowerDensity_GUI(dataDict, Group_Dict, freqLim_Hz,
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
            normFactor = NormalizFactor_PowerDensity_GUI(Data,pw, pr, pnr)
            Power_Wake[ind,:] = np.nanmean(Data[pw],axis=0)  / normFactor
            Power_Rem[ind,:]  = np.nanmean(Data[pr],axis=0)  / normFactor
            Power_NRem[ind,:] = np.nanmean(Data[pnr],axis=0) / normFactor
    return (Power_Wake, Power_Rem, Power_NRem, FreqVect,
            IndexArray_dict, IndexGroup)

def NormalizFactor_PowerDensity_GUI(PowerSp, pw, pr, pnr):
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


def dateConvertion(dateString):
    vectIntConv = np.vectorize(intConv)
    Date = vectIntConv(dateString[:10].split('/'))[::-1]
    Time = vectIntConv(dateString[11:].split(':'))
    DateTime = np.hstack((Date, Time))
    return datetime.datetime(*DateTime)

def find_Hour_Light_Last_Hours(DayVect, Light_Start, Light_len):
    Hour_Dark, Hour_Light = Hour_Light_and_Dark_GUI((Light_Start+Light_len)%24,
                                                24-Light_len)
    Index0 = []
    Index1 = []
    IsLight = DayVect[0].hour in Hour_Light
    if IsLight:
        Index0 += [0]
    ind = 0
    for day in DayVect[1:]:
        if IsLight:
            IsLight = day.hour in Hour_Light
            if not IsLight:
                Index1 += [ind]
        else:
            IsLight = day.hour in Hour_Light
            if IsLight:
                Index0 += [ind]
        ind += 1
    if IsLight:
        Index1 += [ind]
    return Index0,Index1

def F_DeltaRebound(Baseline, Sleep_Deprivation, Recovery, FreeRunning = None,
                    Normalization_H = 4,  DeltaCol = 0,
                   Bin = 900, LightPhaseStart = 8, LightPhaseDur =12,
                   EpochDur = 4):
    """
        Function target:
        ================
            This function calculates delta rebound from an experiment of 
            4 phases: baseline, SD, recovery and freerunning
        
        Input:
        ======
            - Baseline : EEG_Data_Struct
                Baseline EEG data
            - Sleep_Deprivation : EEG_Data_Struct
                SD EEG data
            - Recovery : EEG_Data_Struct
                Recovery EEG data
            - Freerunning : EEG_Data_Struct
                Free running EEG data
            - Normalization_H : int
                Number of hours used for computing normalizing factor
            - DeltaCol : int
                Index of the column of delta frequencies
            - Bin : int
                Number of epochs used for computing each element of DeltaReb
            - LightPhaseDur : int                
                Duration of light phase in hours
            - LightPhaseStart : int                
                First hour of light phase
            - EpochDur : int
                Time duration of each epoch in seconds
        Output:
        =======
            - DeltaReb : dictionary
                keys = integer from 0 to N = number of light 
                phsases of baseline
                + DeltaReb[0] = delta rebound computed normalizing by the
                last 4 hours of last light phase of baseline
                + DeltaReb[1] = delta rebound computed normalizing by the
                last 4 hours of last 2 light phases of baseline...
            
    """
    DaysBaseline = Baseline.Timestamp
    if FreeRunning:
        Day, Delta, Epoch = F_CollectEpoch([Baseline, Sleep_Deprivation,
                                       Recovery, FreeRunning],
                                       DeltaCol = DeltaCol)
    else:
        Day, Delta, Epoch = F_CollectEpoch([Baseline, Sleep_Deprivation,
                                       Recovery],
                                       DeltaCol = DeltaCol, SD_Duration=6,
                                       EpochDur=4)
    DeltaNR = np.ones(len(Delta),dtype=float) * np.nan
    IndNR   = np.where(Epoch == 3)[0]
    DeltaNR[IndNR] = Delta[IndNR]
    NormalizFactor = NormalizationFactor_DeltaReb(DeltaNR, DaysBaseline,
                                         LightPhaseStart = LightPhaseStart,
                                         LightPhaseDur = LightPhaseDur,
                                         Normalization_H = Normalization_H,
                                         EpochDur = EpochDur)
    NumHour = int(np.ceil(len(Day)/float(Bin)))
    DeltaReb  = {}
    TimeStamp = np.zeros(NumHour, dtype='|S19')
    first = True
    for k in list(NormalizFactor.keys()):
        DeltaReb[k] = np.zeros(NumHour, dtype=float) * np.nan
        for h in range(NumHour):
            Tmp = np.nanmean(DeltaNR[h*Bin: (h+1)*Bin])
            if first:
                TimeStamp[h] = Day[h*Bin]
            if Tmp>0:
                DeltaReb[k][h] = Tmp / NormalizFactor[k]
        first = False
    try:
        Time_Limit = (Day[0],Day[(h+1)*Bin-1])
    except:
        Time_Limit = (Day[0],Day[-1])
    return DeltaReb,NormalizFactor,Time_Limit,TimeStamp

def F_DeltaRebound_Epoch_type(Baseline, Sleep_Deprivation, Recovery, FreeRunning = None,
                    Normalization_H = 4,  DeltaCol = 0,
                   Bin = 900, LightPhaseStart = 8, LightPhaseDur =12,
                   EpochDur = 4,epochType=[2,3]):
    """
        Function target:
        ================
            This function calculates delta rebound from an experiment of 
            4 phases: baseline, SD, recovery and freerunning
        
        Input:
        ======
            - Baseline : EEG_Data_Struct
                Baseline EEG data
            - Sleep_Deprivation : EEG_Data_Struct
                SD EEG data
            - Recovery : EEG_Data_Struct
                Recovery EEG data
            - Freerunning : EEG_Data_Struct
                Free running EEG data
            - Normalization_H : int
                Number of hours used for computing normalizing factor
            - DeltaCol : int
                Index of the column of delta frequencies
            - Bin : int
                Number of epochs used for computing each element of DeltaReb
            - LightPhaseDur : int                
                Duration of light phase in hours
            - LightPhaseStart : int                
                First hour of light phase
            - EpochDur : int
                Time duration of each epoch in seconds
        Output:
        =======
            - DeltaReb : dictionary
                keys = integer from 0 to N = number of light 
                phsases of baseline
                + DeltaReb[0] = delta rebound computed normalizing by the
                last 4 hours of last light phase of baseline
                + DeltaReb[1] = delta rebound computed normalizing by the
                last 4 hours of last 2 light phases of baseline...
            
    """
    DaysBaseline = Baseline.Timestamp
    if FreeRunning:
        Day, Delta, Epoch = F_CollectEpoch([Baseline, Sleep_Deprivation,
                                       Recovery, FreeRunning],
                                       DeltaCol = DeltaCol)
    else:
        Day, Delta, Epoch = F_CollectEpoch([Baseline, Sleep_Deprivation,
                                       Recovery],
                                       DeltaCol = DeltaCol, SD_Duration=6,
                                       EpochDur=4)
    DeltaNR = np.ones(len(Delta),dtype=float) * np.nan
    IndNR = []
    for t in epochType:
        IndNR   = np.hstack((IndNR,np.where(Epoch == t)[0]))
    IndNR = np.sort(np.array(IndNR,dtype=int))
    DeltaNR[IndNR] = Delta[IndNR]
    NormalizFactor = NormalizationFactor_DeltaReb(DeltaNR, DaysBaseline,
                                         LightPhaseStart = LightPhaseStart,
                                         LightPhaseDur = LightPhaseDur,
                                         Normalization_H = Normalization_H,
                                         EpochDur = EpochDur)
    NumHour = int(np.ceil(len(Day)/float(Bin)))
    DeltaReb  = {}
    TimeStamp = np.zeros(NumHour, dtype='|S19')
    first = True
    for k in list(NormalizFactor.keys()):
        DeltaReb[k] = np.zeros(NumHour, dtype=float) * np.nan
        for h in range(NumHour):
            Tmp = np.nanmean(DeltaNR[h*Bin: (h+1)*Bin])
            if first:
                TimeStamp[h] = Day[h*Bin]
            if Tmp>0:
                DeltaReb[k][h] = Tmp / NormalizFactor[k]
        first = False
    try:
        Time_Limit = (Day[0],Day[(h+1)*Bin-1])
    except:
        Time_Limit = (Day[0],Day[-1])
        print('modificato by edo')
    return DeltaReb,NormalizFactor,Time_Limit,TimeStamp

def EndsWithStar(Char):
    return Char.endswith('*')
    
def NormalizationFactor_DeltaReb(PowerFreq, Timestamp, LightPhaseStart = 7,
                        LightPhaseDur = 12, Normalization_H = 4,
                        EpochDur = 4):
    """
        Function Target:
        ================
            This function calculates the normalization factor for
            Delta Rebound. It takes as an input the power of delta freq.
            from the baseline dataset and gives as output several normalization
            factors: 
                - sum of all power of epochs in the last "Normalization_H"\
                hours of last light phase
                
                - sum of all power of epochs in the last "Normalization_H"\
                hours of the last 2 light phases
                
                            ...
                
                - sum of all power of epochs in the last "Normalization_H"\
                hours of all light phases
        Input:
        ======
        
            - PowerFreq : 1-dim numpy array (float)

            
                    Vector of delta frequencies of baseline dataset
                
            - Timestamp : 1-dim numpy array (datetime.datetime)

            
                    Vector containing date and hour of each epoch
            
            - LightPhaseStart : int
                
                First hour of light phase
            
            - LightPhaseDur : int
                
                Duration of light phase in hours
            
            - Normalization_H : int
            
                Number of hours used for computing normalizing factor
                
            - EpochDur : int

                Time duration of each epoch in seconds
        
        Output:
        =======
            - NormalizFactor : dictionary
            
                Dictionary's keys are integer:

                + NormalizFactor[1] = int, normalizing factor calculate\
                      considering last light phase
                      
                + NormalizFactor[2] = int, normalizing factor calucate\
                     considering last 2 light phases...
                     
    """
    LightStart, LightEnd = find_Hour_Light_Last_Hours(Timestamp,
                                                      LightPhaseStart,
                                                      LightPhaseDur)
    Index0 = []
    Index1 = []
    for ind in range(len(LightStart)):
        Delta_t = (Timestamp[LightEnd[ind]] -
            Timestamp[LightStart[ind]]).seconds
        if Delta_t > 3600 * Normalization_H:
            Index1 += [LightEnd[ind]]
            Index0 += [LightEnd[ind] - Normalization_H  * int(3600 / EpochDur)]
    Index0 = Index0[::-1]
    Index1 = Index1[::-1]
    Index  = np.array([], dtype=int)
    NormalizFactor = {}
    for k in range(len(Index0)):
        Index = np.hstack((Index, list(range(Index0[k],Index1[k]))))

        NormalizFactor[k]  = np.nanmean(PowerFreq[Index])
    return NormalizFactor

    
def F_CollectEpoch(DataList, DeltaCol=0, SD_Duration=6, EpochDur=4):
    """
        Function Target:
        ================
        
            This function is  returns a vector collecting al date and times
            of each epochnof all dataset in Datalist, a vector with all labeled
            epochs and a vector containinf the delta power of every epoch
            labeled without * and a NaN when the epoch is labeled with a *.
        
        Input:
        ======
            - DataList : list of EEG_Data_Struct
            - DeltaCol : int
                Index of the column of delta frequencies
        Output:
        =======
        
            - Day : numpy array
                Date and hour of every epoch
            - Delta : numpy array
                Delta frequancies of non * epochs
            - Epoch
                Labeled epochs
            
    """
    vectEndsWithStar = np.vectorize(EndsWithStar)
    Epoch = np.array([], dtype = int)
    Delta = np.array([], dtype = float)
    Day = np.array([],dtype = object)
    for Data in DataList:
        if Data is None:
            Epoch = np.hstack((Epoch, np.nan*np.ones(SD_Duration * 3600//EpochDur)))
            Delta = np.hstack((Delta, np.nan*np.ones(SD_Duration * 3600//EpochDur)))
            Day = np.hstack((Day, np.nan*np.ones(SD_Duration * 3600//EpochDur)))
            continue
        Index = np.where(vectEndsWithStar(Data.Stage) == True)[0]
        Epoch = np.hstack((Epoch, F_Epoch(Data.Stage)))
        tmpDelta = Data.PowerSp[:, DeltaCol]
        tmpDelta[Index] = np.nan
        Delta = np.hstack((Delta, tmpDelta))
        Day = np.hstack((Day, Data.Timestamp))
    return Day, Delta, Epoch

def F_Epoch(Data,Sleep_Diff=True):
    Epoch = np.zeros(len(Data),dtype=int)
    k = 1.0
    if Sleep_Diff:
        for epochStr in ['W','W*','R','R*','NR','NR*']:
            Epoch[np.where(Data==epochStr)[0]] = np.ceil(k/2)
            k += 1
            
    else:
        for epochStr in ['W','W*','R','R*','NR','NR*']:
            Epoch[np.where(Data==epochStr)[0]] = min(np.ceil(k/2),2)
            k += 1
    return Epoch
    
def EpocheTot_xTimebin(Epoch,Bin,Type=[3,2]):
    BoolVect=np.zeros(len(Epoch),dtype=int)
    for thisType in Type:
        BoolVect[np.where(Epoch==thisType)[0]]=1
    step = float(3600/4*Bin)
    iterate=np.arange(len(Epoch)//step)
    NEP=np.zeros(len(iterate))
    for t in iterate:
        NEP[t] = np.sum(BoolVect[t*step:(t+1)*step])
    return NEP
    
def EpisodsDurationXhour(Epoch, Bin, Type = [3,2]):
    BoolVect  = np.zeros(len(Epoch), dtype = int)
    NumEpisod = np.zeros(len(Epoch), dtype = int)
    for thisType in Type:
        BoolVect[np.where(Epoch==thisType)[0]] = 1
    Diff  = np.diff(BoolVect)
    Start = np.where(Diff > 0)[0]
    End   = np.where(Diff < 0)[0]
    NumEpisod[Start + 1] = 1
    step = int(3600/4*Bin)
    iterate=np.arange(len(Epoch)//step+1)
    NEP=np.zeros(len(iterate))
    for t in iterate:
        NEP[t] = np.sum(NumEpisod[1 + t*step:(t+1)*step])
    if Start[0] > End[0]:
        End = End[1:]
    if len(Start) > len(End):
        Start = Start[:-1]
    Duration = (End - Start) * 4.0 / 60.0
    DurEpisodes    = np.zeros(len(Epoch))
    DurEpisodes[:] = np.nan
    DurEpisodes[Start + 1] = Duration
    indE = np.where(DurEpisodes >= 60)[0]
    for t in range(len(indE)):
        k = step
        DurEpisodes[indE[t] + k] =\
            DurEpisodes[indE[t]] - 60
        DurEpisodes[indE[t]] = 60
        while DurEpisodes[indE[t]+k] >= 60:
            DurEpisodes[indE[t]+k+step] =\
                DurEpisodes[indE[t]+k]-60
            DurEpisodes[indE[t]+k] = 60
            k += step
    MeanDurEpisod = np.zeros(len(Epoch)//step)
    shorter = np.where(DurEpisodes <= 4.0/60)[0]
    DurEpisodes[shorter] = np.nan
    for t in range(len(MeanDurEpisod)):
        MeanDurEpisod[t] = np.nanmean(
            DurEpisodes[1 + t*step:(t+1)*step])
    return MeanDurEpisod, Duration

def Stat_Indexes_DeltaReb_GUI(DeltaReb_Dict, Group_Dict):
    """
        Function Target:
        ================
            This function comute mean, median and sem of delta rebound whithin
            each time bin and between groups specified by Group_Dict
        Input:
        ::::::
            - DeltaReb_Dict : dictionary, key = subject name
                Contains the Delta rebound for every subject that is the
                output of the function F_DeltaRebound
            - Group_Dict : dictionary, key = group name
                Group_Dict[group] : numpy array/list of subject names
        Output:
        :::::::
            - Mean, Median, SEM : numpy array
                Mean, Median and SEM of delta reb. whithin time and between
                subjects
            
    """
    GrSize = {}
    GroupDelta_Dict = {} 
    Mean   = {}
    Median = {}
    SEM    = {}
    for key in list(Group_Dict.keys()):
        Group = Group_Dict[key]
        GrSize[key] = len(Group)
        GroupDelta_Dict[key] = np.zeros((GrSize[key],
                                len(DeltaReb_Dict[Group[0]])))
        row = 0
        for subject in Group:
            GroupDelta_Dict[key][row,:] = DeltaReb_Dict[subject]
            row += 1
        Mean[key]   = np.zeros(GroupDelta_Dict[key].shape[1])
        Median[key] = np.zeros(GroupDelta_Dict[key].shape[1])
        SEM[key]    = np.zeros(GroupDelta_Dict[key].shape[1])
        for col in range(GroupDelta_Dict[key].shape[1]):
            Index = np.where(GroupDelta_Dict[key][:,col] != 0)[0]
            Mean[key][col]   = np.nanmean(GroupDelta_Dict[key][Index,col])
            Median[key][col] = np.nanmedian(GroupDelta_Dict[key][Index,col])
            SEM[key][col]    = np.nanstd(GroupDelta_Dict[key][Index,col])\
                               / np.sqrt(GrSize[key])
    return Mean, Median, SEM
            
def F_Reoder_SubjectiveTimes(timeVector,Hours,
                             ReturnArgSort=False):

    Ind = np.argsort(timeVector)
    if ReturnArgSort:
        return Ind
    Reordered = timeVector[Ind][Hours]
        
    return Reordered, Ind



def F_ExpGain_GUI(Short, Long, ProbeShort, Cond_SProbe, Cond_LProbe, 
                  MeanRange=(1, 9), CVRange=(0.05,0.5), Mesh=600):
    """
    Function Target: 
    ================
        This function calculates the expected gains of mice with
        different average time of switch latencies and different
        variation coefficient (CV) and the best mean switch latencies
        for every fixed CV.
                        
    
    Input:
    ======
        - Short/Long : float
            Duration of light signal in time for short and long trials
        - ProbeShort  : float
            Probability of short probe
        - Cond_SProbe : float
            Probability of short probe given a short trial
        - Cond_LProbe : float
            Probability of short probe given a Long trial
        - Mesh : int
            Dimension of explog matrix.
                        
    Output:
    =======
        -ExpLog : numpy array, shape = Mesh x Mesh
            Expected gain matrix, element (i,j) is the exp gain
            for Mean[j] and variance Cv[i]*Mean[j]
        - MaxRowl : numpy array, shape = Mesh x 1
            Max exp gain for every fixed mean, variating the Cv.
    """
    Cv = np.linspace(CVRange[0],CVRange[1],Mesh)
    Mean = np.linspace(MeanRange[0],MeanRange[1],Mesh)
    ExpLog = np.zeros((Mesh,Mesh),dtype=float)
    ProbeLong = 1-ProbeShort
    Matrix_Mean=np.zeros((Mesh,Mesh))
    Matrix_Std=np.zeros((Mesh,Mesh))

    for i in range(Mesh):
        Matrix_Mean[i,:]=Mean
        Matrix_Std[:,i]=Mean[i]*Cv

    PS = sts.norm.cdf(Short,Matrix_Mean,Matrix_Std)
    PL =  sts.norm.cdf(Long,Matrix_Mean,Matrix_Std)
    ExpLog = (ProbeShort*(1 - Cond_SProbe)) * (1 - PS) +\
        (ProbeLong * (1 - Cond_LProbe)) * PL
    ExpLog[np.isnan(ExpLog)] = np.nanmin(ExpLog)
    MaxRowl = np.nanargmax(ExpLog, axis=1)

    return(ExpLog, MaxRowl)

def stdMatrix_Group_Stat_Index_GUI(stdMatrix, Group_Dict):
    """
        Function Target:
        ================
            This function take in input a standard format structured numpy
            array that must have column names 'Subject', 'Time' and 'Mean'
            and returns a standard fromat structured array with means,
            median and SEM for each group in each time point indicated in 
            'Time'.
        Input:
        ======
            - stdMatrix : numpy array
                It is a structued array with columns 'Mean', 'Time' and 
                'Subject'. It contains mean values of subjective parameters
                collected for several days at different time points
            - Group_Dict : dictionary, keys = group names
                Value of the dictionary are lists of subject names,
                must be the same names found in stdMatrix['Subject']
        Output:
        =======
            - stdGroupMatrix : numpy array
                A strucured array containing statistical indexes of values
                in stdMatrix for every group at every time point
    """
    GroupList = list(Group_Dict.keys())
    subject   = Group_Dict[GroupList[0]][0].encode()
    HourList  = stdMatrix['Time'][np.where(stdMatrix['Subject'] == subject)[0]]
    timeStrLen = len(HourList[0])
    groupNameLen = []
    Len = len(HourList) * len(GroupList)
    for group in GroupList:
        groupNameLen += [len(group)]
    stdGroupMatrix = np.zeros(Len, dtype = {'names':('Group','Time','Mean',
                                                      'Median','SEM'),
                                         'formats':('|S%d'%max(groupNameLen),
                                                    '|S%d'%timeStrLen,
                                                    float, float ,float)})
    ind = 0
    for group in GroupList:
        SubjectList = Group_Dict[group]
        Shape = len(SubjectList), len(HourList)
        Matrix = np.zeros(Shape)
        row = 0
        for subject in Group_Dict[group]:
            SubInd        = np.where(stdMatrix['Subject'] == subject.encode())[0]
            Matrix[row,:] = stdMatrix['Mean'][SubInd]
            row += 1
        stdGroupMatrix['Mean'][ind : ind + len(HourList)] =\
            np.nanmean(Matrix, axis = 0)
        stdGroupMatrix['Median'][ind : ind + len(HourList)] =\
            np.nanmedian(Matrix, axis = 0)
        stdGroupMatrix['SEM'][ind : ind + len(HourList)] =\
            np.nanstd(Matrix, axis = 0)/np.sqrt(len(SubjectList))
        stdGroupMatrix['Time'][ind : ind + len(HourList)] = HourList
        stdGroupMatrix['Group'][ind : ind + len(HourList)] = group
        ind += len(HourList)
    
    return stdGroupMatrix
    
def StepWiseRegression_sse_forward(predictor, Observations, p_entrance=0.15,
                                   p_exit=0.15):
    """
        Function Target:
        ================
            This function computes a forward stepwise linear ls regression.
            Variable are selected via mutliple t-test. Every time the min
            p_value < p_entrance is kept. If no p_value are < than p_entrace
            the algorithm terminate.
        Input:
        ======
            - predictor : numpy array, shape = n_sample x (n_predictor + 1)
                Predictor matrix, first line must be of ones to add 
                an intercept. If it isn't the case the a line of ones is added.
            - Observations : numpy array, shape = n_sample x n_observation
            - p_entrance : float
                Entrance tolerance
            - p_exit : float
                Exit tolerance
        Output:
        =======
            - History : dictionary, keys = 'step %d'%(step num)
                - History['step %d'%(step num)] : dictionary
                    keys =
                        'Best Fit' --> best regression table results
                        'Regression Fits' --> dictionary with all the 
                            regressions performed at the given step
                        'Removed' --> List of removed variables at the
                            given step
                        'Added Predictor' --> the predictor added at the 
                            given step
            - insertedPredictor : list
                List of inserted predictors, values from 1 to n_predictor
    """
    if predictor.shape[0] != sum(predictor[:,0]):
        add_constant(predictor)
    NumPredictor  = predictor.shape[1] - 1
    insertedPredictor = []
    notInsertedPredictor = list(range(1, NumPredictor + 1))
    bestRegFit = None
    History = OrderedDict()
    stepList = []
    step = 0
    while True:
        History['step %d'%step] = {}
        History['step %d'%step]['Removed']   = []
        if len(insertedPredictor) > 1:
            remove = Remove_Predictor(bestRegFit, p_exit)
            for pred in remove:
                insertedPredictor.remove(pred)
                insort_left(notInsertedPredictor, pred)
            History['step %d'%step]['Removed'] = remove
        usePredictor  = OrderedDict()
        for pred in notInsertedPredictor:
            usePredictor[pred] = insertedPredictor + [pred]
            usePredictor[pred].sort()
        if notInsertedPredictor == []:
            History.pop('step %d'%step)
            break
        regFits =\
            Regression_Step(Observations, predictor, usePredictor)
        History['step %d'%step]['Regression Fits'] = regFits
        add, bestRegFit =\
            Add_Predictor(regFits, p_entrance)
        History['step %d'%step]['Added Predictor'] = add
        History['step %d'%step]['Best Fit']  = bestRegFit
        if add == None:
            break
        stepList += ['step %d'%step]
        notInsertedPredictor.remove(add)
        insort_left(insertedPredictor, add)
        insertedPredictor.sort()
        step += 1
    return History, insertedPredictor, stepList

def Regression_Step(Observations, predictor, usePredictor):
    """
        Function Target:
        ================
            This function perform a sequence of regressions using
            predictors indicated by usePredictor and returns regression 
            tables from each regression made.
        Input:
        ======
            - Observations : numpy array, shape = n_sample x n_observation
                Matrix containing all observations
            - predictor : numpy array, shape = n_sample x (n_predictor + 1)
                Predictor matrix, first line must be of ones to add 
                an intercept.
            - usePredictor : list
                Each element of the list is a list of indexes corrisponding
                to the predictors we will use for the regression fit
        Output:
        =======
            - regFits : dictionary, keys new predictor index
                Tabele of the regression from the model built adding the 
                predictor indicated by the dict key.
                
    """
    regFits = OrderedDict()
    for numPredictor in list(usePredictor.keys()):
        olsReg = OLS(Observations, predictor[:,[0] + usePredictor[numPredictor]])
        fit = olsReg.fit()
        regFits[numPredictor] = np.zeros(len(fit.params),
            dtype = {'names':('Predictor', 'params', 'std err','t',\
            'p_value','Conf. Int. 95% 0',
            'Conf. Int. 95% 1','Df model','Df resid','F stat','F p_value',
            'R-squared','R-squared adj'),
            'formats':(int,float,float,float,float,float,float,float,float,
                       float,float,float,float)})
        regFits[numPredictor]['Predictor'][0]   = 0
        regFits[numPredictor]['Predictor'][1:]  = usePredictor[numPredictor]
        regFits[numPredictor]['params']   = fit.params
        regFits[numPredictor]['std err']  = fit.bse
        regFits[numPredictor]['t']        = fit.tvalues
        regFits[numPredictor]['p_value']  = fit.pvalues
        regFits[numPredictor]['F stat'][0]   = fit.fvalue
        regFits[numPredictor]['F stat'][1:]  = np.nan
        regFits[numPredictor]['F p_value'][0]   = fit.f_pvalue
        regFits[numPredictor]['F p_value'][1:]  = np.nan
        regFits[numPredictor]['Conf. Int. 95% 0'] = fit.conf_int(0.05)[:,0]
        regFits[numPredictor]['Conf. Int. 95% 1'] = fit.conf_int(0.05)[:,1]
        regFits[numPredictor]['Df model'][0] = fit.df_model
        regFits[numPredictor]['Df model'][1:] = np.nan
        regFits[numPredictor]['Df resid'][0] = fit.df_resid
        regFits[numPredictor]['Df resid'][1:] = np.nan
        regFits[numPredictor]['R-squared'][0] = fit.rsquared
        regFits[numPredictor]['R-squared'][1:] = np.nan
        regFits[numPredictor]['R-squared adj'][0] = fit.rsquared_adj
        regFits[numPredictor]['R-squared adj'][1:] = np.nan
        
    return regFits

def Add_Predictor(regFits, p_entrance):
    """
        Function Target:
        ================
            This function check that which new predictor we need to add.
            We add the predictor with the min p_value stat if the p_value
            is lower than p_entrance.
    """
    newPredictor = list(regFits.keys())
    p_val = np.zeros(len(newPredictor), dtype={'names':('Predictor','p_value'),
                     'formats':(int,float)})
    index = 0
    for numPredictor in newPredictor:
        newPredictorRow = np.where(regFits[numPredictor]\
            ['Predictor'] == numPredictor)[0][0]
        p_val['p_value'][index] = regFits[numPredictor]\
            ['p_value'][newPredictorRow]
        p_val['Predictor'][index] = regFits[numPredictor]\
            ['Predictor'][newPredictorRow]
        index += 1
    argMin = np.argmin(p_val['p_value'])
    if p_val['p_value'][argMin] > p_entrance:
        return None, regFits[p_val['Predictor'][argMin]]
    return p_val['Predictor'][argMin], regFits[p_val['Predictor'][argMin]]

def Remove_Predictor(bestRegFit, p_exit):
    """
        Function Target:
        ================
            This function remove all predictors that in the new model has a
            p_value higher than p_exit.
    """
    notConstInd = np.where(bestRegFit['Predictor']!= 0)[0]
    indexRemove = np.where(bestRegFit['p_value'][notConstInd] > p_exit)[0]
    return bestRegFit['Predictor'][notConstInd][indexRemove]

def regression_Matrix(Datas, Group_Dict, predictor = True):
    """
        Function Target:
        ================
            This function build inputs for stepwise regression from a std 
            outputs of single subject analysis. 
            Each row of the output corrispond to a group average of a 
            behavioural/sleep score at a particular time of the day. It is not
            important that 
                Datas[name_j]['Time'][row,:] == Datas[name_k]['Time'][row,:]
            because an optimale time shift to align observation will be applied
            when performing the regression analysis.
        Input:
        ======
            - Datas : dictionary, keys = data name
                Dictionary of all collected observation/predictions
            - Group_Dict = dictionary, keys = data name
               - Group_Dict[key] : dictionary, keys = group names
                   List of subjects per group
            - predictor : bool
                If true a column of ones is prepended to the output matices
        Output:
        =======
            - regression_Dict : dictionary, keys = group names
                - regression_Dict[key] : numpy array
                    Input matrix for stepwise regression
        
    """
    regression_Dict = {}
    Hours = np.unique(Datas[list(Datas.keys())[0]]['Time'])
    numHours = len(Hours)
    for group in list(Group_Dict[list(Datas.keys())[0]].keys()):
        regression_Dict[group] = np.zeros((numHours,len(list(Datas.keys()))))
    predNum = 0
    for predict in list(Datas.keys()):
        DataArray = Datas[predict]
        for group in list(Group_Dict[predict].keys()):
            grList = Group_Dict[predict][group]
            matrix_sub = np.zeros((len(grList),len(Hours)))
            
            ind = 0
            for name in grList:
                matrix_sub[ind,:] = DataArray['Mean']\
                    [np.where(DataArray['Subject'] == name)[0]]
                matrix_sub[ind,:] = matrix_sub[ind,:] /\
                    np.nanmax(matrix_sub[ind,:])
                ind += 1
            regression_Dict[group][:,predNum] = np.nanmean(matrix_sub)
        predNum += 1
    if predictor:
        for group in list(Group_Dict[list(Datas.keys())[0]].keys()):
            regression_Dict[group] = add_constant(regression_Dict[group])
    return regression_Dict

def build_Rsquared_Matrix(regressionModels):
    ObsName = list(regressionModels.keys())
    lenObs = 0
    for name in ObsName:
        lenObs = max(lenObs, len(name))
    GroupName = list(regressionModels[ObsName[0]].keys())
    lenGr = 0
    for name in ObsName:
        lenGr = max(lenGr, len(name))
    lenCirca = 0
    lenSleep = 0
    CircaName = {}
    SleepName = {}
    selectedCirca = {}
    selectedSleep = {}
    for obs in ObsName:
        CircaName[obs] = {}
        selectedCirca[obs] = {}
        selectedSleep[obs] = {}
        SleepName[obs] = {}
        for group in GroupName:
            selectedCirca[obs][group] = {}
            selectedSleep[obs][group] = {}
            for predCirca in list(regressionModels[obs][group].keys()):
                selectedCirca[obs][group][predCirca] = {}
                selectedSleep[obs][group][predCirca] = {}
                for predSleep in list(regressionModels[obs][group][predCirca].keys()):
                    reg = regressionModels[obs][group][predCirca][predSleep]
                    lenCirca = max(lenCirca, len(reg.varaibleDict[1]))
                    if 'x1' in reg.model:
                        selectedCirca[obs][group][predCirca][predSleep] = True
                    else:
                        selectedCirca[obs][group][predCirca][predSleep] = False
                    if 'x2' in reg.model:
                        selectedSleep[obs][group][predCirca][predSleep] = True
                    else:
                        selectedSleep[obs][group][predCirca][predSleep] = False
                    lenSleep = max(lenSleep, len(reg.varaibleDict[2]))
    lenPredCirca = len(list(regressionModels[obs][group].keys()))
    lenPredSleep = len(list(regressionModels[obs][group][predCirca].keys()))
    Matrix = np.zeros(len(ObsName)*len(GroupName)*lenPredSleep*lenPredCirca,
                      dtype={'names':('Group','Observation', 'Circadian Predictor',
                                      'Sleep Predictor', 'R-squared',
                                      'Selected Circadian','Selected Sleep'),
                             'formats':('S%d'%lenGr,'S%d'%lenObs,
                             'S%d'%lenCirca,'S%d'%lenSleep,float,bool,bool)})
    ind = 0
    for obs in ObsName:
        for group in GroupName:
            for predCirca in list(regressionModels[obs][group].keys()):
                for predSleep in list(regressionModels[obs][group][predCirca].keys()):
                    Matrix['Group'][ind] = group
                    Matrix['Observation'][ind] = obs
                    Matrix['Circadian Predictor'][ind] = predCirca
                    Matrix['Sleep Predictor'][ind] = predSleep
                    Matrix['R-squared'][ind] =\
                        regressionModels[obs][group][predCirca]\
                            [predSleep].bestFit['R-squared'][0]
                    Matrix['Selected Circadian'][ind] =\
                        selectedCirca[obs][group][predCirca][predSleep]
                    Matrix['Selected Sleep'][ind] =\
                        selectedSleep[obs][group][predCirca][predSleep]
                    ind += 1
    return Matrix

class multiple_Regression(object):
    """
        multiple_Regression class:
        ==========================
            This class stores all informations regarding the best
            fit obtained with the multiple regression procedure
    """
    def __init__(self, bestFit, lagSleep, lagCircadian, selectedVariables,
                 varList, observationName, parent=None):
#   MODIFICA CRITICA, CAMBIO TIPO A BEST FIT PER TOGLIERE PANDAS
        self.bestFit = bestFit
#        self.bestFit = pd.DataFrame(bestFit)
        
        self.lagSleep = lagSleep
        self.lagCircadian = lagCircadian
        self.observationName = observationName
        self.model = 'y = 1'
        self.varaibleDict = {}

        try:
            self.selectedVariables =\
            np.array(varList)[np.array(selectedVariables)-1]
        except:
            self.selectedVariables = np.array([])
        for selected in selectedVariables:
            self.model += ' + x%d'%selected
        for k in range(len(varList)):
            self.varaibleDict[k + 1] = varList[k]

    def __repr__(self):
        string = 'Regression results:\n'
        string += '%s\n'%self.bestFit
        string += '\nOptimal sleep predictor lag: %s\n'%self.lagSleep
        string += 'Optimal circadian predictor lag: %s\n'%self.lagCircadian
        string += 'Selected model: %s\n'%self.model
        string += 'y = %s\n'%self.observationName
        for num in list(self.varaibleDict.keys()):
            string += 'x%d = %s\n'%(num, self.varaibleDict[num])
        return string

def find_BestLag(Group_Dict, Predictors, Observation, p_entrance=0.15,
                 p_exit=0.15):
    """
        Function Target:
        ================
            This function find best lag for every predictor and every group
            specified in Group_Dict
        Input:
        ======
            - Group_Dict : dictionary, key = input names (observations and 
                predictors)
                - Group_Dict[var] : dictionary, keys = genotype
                - Group_Dict[var][genotype] : list
                    It contains all mouse names of mice of the specified
                    genotype for the specified observation/predictor
            - Predictors : dictionary, key = predictor names
                Predictors[key] is a predictor matrix of the standard form;
                must contain columns 'Mean' and 'Subject'
            - Obeservation : dictionary, key = observation names
                Obeservation[key] is an observation matrix of the standard
                form; must contain columns 'Mean' and 'Subject'
            - p_entrance : float
                The maximum p value for a term to be added
            - p_exit : float
                The minumum p value for a term to be removed
        Output:
        =======
            - bestLag : dictionary, key = observation name
                - bestLag[obs] : dictionary, key = genotype name
                - bestLag[obs][gen] : dictionary, key = predictor name
                - bestLag[obs][gen][pred] : int
                    Index shift that maximizes the R-squared of the regression
            - R_squared : dictionary,key = observation name
                - R_squared[obs] : dictionary, key = genotype name
                - R_squared[obs][gen] : dictionary, key = predictor name
                - R_squared[obs][gen][pred] : list
                    List of R-squared, one for every possible time shift
                    of the predictor
    """
    predictorList = list(Predictors.keys())
    genotypeNameList = list(Group_Dict[list(Group_Dict.keys())[0]].keys())
    bestLag = {}
    R_squared = {}
    lagVect = {}
    for obsKey in list(Observation.keys()):
        bestLag[obsKey] = {}
        R_squared[obsKey] = {}
        lagVect[obsKey] = {}
        tmpObservation = {obsKey : Observation[obsKey]}
        tmpObservation = regression_Matrix(tmpObservation, Group_Dict, False)
        for genotype in genotypeNameList:
            bestLag[obsKey][genotype] = {}
            R_squared[obsKey][genotype] = {}
            lagVect[obsKey][genotype] = {}
            thisObservation = tmpObservation[genotype]
            for predictor in predictorList:
                thisPredictDict = {predictor : Predictors[predictor]}
                thisPredictMat = regression_Matrix(thisPredictDict, Group_Dict,
                                                   True)
                thisPredictMat = thisPredictMat[genotype]
                indexes = np.arange(thisPredictMat.shape[0], dtype=int)
                R_squared[obsKey][genotype][predictor] = []
                lagVect[obsKey][genotype][predictor] = indexes
                for lag in indexes:
                    shiftInd = (indexes + lag)%thisPredictMat.shape[0]
                    hist, tmp, steps = StepWiseRegression_sse_forward(
                        thisPredictMat[shiftInd, :], thisObservation,
                        p_entrance, p_exit)
                    try:
                        R_squared[obsKey][genotype][predictor] +=\
                            [hist[steps[-1]]['Best Fit']['R-squared'][0]]
                    except IndexError:
                        R_squared[obsKey][genotype][predictor] += [0]
                bestLag[obsKey][genotype][predictor] =\
                    np.argmax(R_squared[obsKey][genotype][predictor])
    return bestLag, R_squared, lagVect

def multipleRegressionProcedure(dict_Predictor_Circadian, dict_Predictor_Sleep,
                                dict_Observation, Group_dict, bestLagCircadian,
                                bestLagSleep, p_entrance=0.15,
                                p_exit=0.15):
    """
        Function Target:
        ================
            This function performs stepwise multiple regression for selecting
            best linear regression model for several observations and
            several couple of predictors
        Input:
        ======
            - dict_Predictor_Circadian : dictionary, key = predictor names
                dict_Predictor_Circadian[key] is a predictor matrix of the 
                standard form; must contain columns 'Mean' and 'Subject'
            - dict_Predictor_Sleep : predictor, key = observation names
                dict_Predictor_Sleep[key] is an observation matrix of the
                standard form; must contain columns 'Mean' and 'Subject'
            - dict_Observation : dictionary, keys = observation names
                dict_Observation[key] is an observation matrix of the standard
                form; must contain columns 'Mean' and 'Subject'
            - Group_dict : dictionary, key = input names (observations and 
                predictors)
                - Group_dict[var] : dictionary, keys = genotype
                - Group_dict[var][genotype] : list
                    It contains all mouse names of mice of the specified
                    genotype for the specified observation/predictor
            - bestLagCircadian : dictionary
                Output of the function "find_bestLag" for the circadian
                predictors
            - bestLagCircadian : dictionary
                Output of the function "find_bestLag" for the sleep
                predictors
            - p_entrance : float
                The maximum p value for a term to be added
            - p_exit : float
                The minumum p value for a term to be removed
        Output:
        =======
            - regressionModels : dictionary, keys = observation name
                - regressionModels[obs] : dictionary, keys = genotypes
                - regressionModels[obs][gen] : dictionary, keys = predictor
                    circadian
                - regressionModels[obs][gen][pred1] : dictionary, keys =
                    predictor sleep
                - regressionModels[obs][gen][pred1][pred2] : object, class
                    multiple_Regression
                    Contains informations abuout the best fit model of the
                    multiple regression procedure
    """
    regressionModels = {}
    for observation in list(bestLagSleep.keys()):
        regressionModels[observation] = {}
        tmpObservation = {observation : dict_Observation[observation]}
        for genotype in list(bestLagSleep[observation].keys()):
            regressionModels[observation][genotype] = {}
#==============================================================================
#   Create an observation matrix of the specified genotype
#==============================================================================
            obsMatrix = regression_Matrix(tmpObservation, Group_dict,
                                          False)[genotype]
#==============================================================================
#   indexes will be used for shifting the predictor vectors of the best
#   lag
#==============================================================================
            indexes = np.arange(obsMatrix.shape[0], dtype=int)
#==============================================================================
#   tmpPredictor wil be a dictionary with two keys that will be used for
#   generating the predictor matrix with 1 circadian predictor and one
#   sleep predictor.
#==============================================================================
            for circadian in list(dict_Predictor_Circadian.keys()):
                regressionModels[observation][genotype][circadian] = {}
                for sleep in list(dict_Predictor_Sleep.keys()):
                    tmpPredictor = {}
                    tmpPredictor[circadian] = dict_Predictor_Circadian\
                        [circadian]
                    tmpPredictor[sleep] = dict_Predictor_Sleep[sleep]
#==============================================================================
#   Creation of predictor matrix for the specified genotype
#==============================================================================
                    predMatrix = regression_Matrix(tmpPredictor, Group_dict,
                                                   True)[genotype]
#==============================================================================
#   Since preductors are added to the column matrix tmpPredictor in the same
#   order as predicotr names are returned by tmpPredictor.keys() we will
#   extract this information. Finally we add one because first column is
#   for the intercept
#==============================================================================
                    indCircadian = np.where(np.array(list(tmpPredictor.keys())) ==\
                        circadian)[0][0]
                    indSleep = (1 + indCircadian) % 2
                    indCircadian += 1
                    indSleep += 1
#==============================================================================
#   Calculate vector for shifting the predictor values and than shifting each
#   column of predMatrix
#==============================================================================
                    shiftCircadian =\
                        (indexes + bestLagCircadian[observation][genotype]\
                            [circadian]) % obsMatrix.shape[0]
                    predMatrix[:, indCircadian] = predMatrix[:, indCircadian]\
                        [shiftCircadian]
                    shiftSleep =\
                        (indexes + bestLagSleep[observation][genotype][sleep])\
                            % obsMatrix.shape[0]
                    predMatrix[:, indSleep] = predMatrix[:, indSleep]\
                        [shiftSleep]
#==============================================================================
#   Perform a stepwise regression
#==============================================================================
                    hist, selected, steps = StepWiseRegression_sse_forward(
                        predMatrix, obsMatrix,
                        p_entrance, p_exit)
                    varList = [0, 0]
                    varList[indCircadian - 1] = circadian
                    varList[indSleep - 1] = sleep
                    try:
                        regressionModels[observation][genotype]\
                            [circadian][sleep] = multiple_Regression(
                                hist[steps[-1]]['Best Fit'],
                                bestLagSleep[observation][genotype][sleep],
                                bestLagCircadian[observation][genotype]\
                                [circadian],
                                selected,
                                varList,
                                observation
                            )
                    except IndexError:
                        regressionModels[observation][genotype]\
                            [circadian][sleep] = multiple_Regression(
                                hist[list(hist.keys())[-1]]['Best Fit'],
                                bestLagSleep[observation][genotype][sleep],
                                bestLagCircadian[observation][genotype]\
                                [circadian],
                                selected,
                                varList,
                                observation
                            )
    return regressionModels
    
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
    
def std_Switch_Latency_GUI(Record_Switch, HSSwitch, DataGroup, Dark_start=20, Dark_length=12):
    Tot_Subjects = 0
    lenName = 0
    for name in list(Record_Switch.keys()):
        Tot_Subjects += 1
        lenName = max(lenName, len(name))
    for k in list(Record_Switch.keys()):
        print(k, len(Record_Switch[k]))
    Hour_Dark,Hour_Light = Hour_Light_and_Dark_GUI(Dark_start, Dark_length)
    Best_Model, Pdf, Cdf, EmCdf = F_Gr_Fit_GMM_GUI(Record_Switch, DataGroup,
                                              n_gauss=1)
    GMM_Fit = {'Best_Model' : Best_Model,
               'Pdf' : Pdf, 'Cdf' : Cdf,
               'EmCdf' : EmCdf}
    Median, Mean, Std = Subj_Median_Mean_Std_GUI(Record_Switch, HSSwitch)
    Hour_label = TimeUnit_to_Hours_GUI(np.hstack((Hour_Dark,Hour_Light)),3600)
    DataLen = len(Hour_label) * Tot_Subjects

    ind = 0
    std_Matrix = np.zeros(DataLen, dtype = {
        'names':('Subject', 'Time','Mean', 'Median', 'SEM'),
        'formats':('|U%d'%lenName, '|U5',float, float, float)})
    for name in list(Record_Switch.keys()):
        std_Matrix['Subject'][ind:len(Hour_label)+ind] = name
        std_Matrix['Mean'][ind:len(Hour_label)+ind] = Mean[name]
        std_Matrix['Median'][ind:len(Hour_label)+ind] = Median[name]
        std_Matrix['SEM'][ind:len(Hour_label)+ind] = Std[name]
        std_Matrix['Time'][ind:len(Hour_label)+ind] = Hour_label
        ind += len(Hour_label)

    return std_Matrix, GMM_Fit

def Exp_Gain_Matrix_GUI(GMM_Fit, Short, Long, Group_dict, ProbeShort, 
                        Cond_SProbe, Cond_LProbe):
    """
        Function Target:
        ================
            This function create a matrix of the std format for the GMM_Fit
            containing exp gain value for each subject as well as extimated
            parameters from the gaussian fit
        Input:
        ======
            - GMM_Fit : dictionary, keys = 'Pdf', 'Best_Model', 'Cdf', 'EmCdf'
                - GMM_Fit['Best_model'] : dictionary, keys = subject names
                    Objects of the class GMM with the best fit for each subject
            - Short : float
                Short signal duration
            - Long : float
                Long signal duration
            - Group_dict : dictionary, keys = group names
                Contains a list of subject for each group
            - ProbeShort : float, range = (0, 1)
                Probability of having a short problem
            - Cond_SProbe : int, range = (0, 1)
                Conditional probability of having a probe given that
                the signal is short
            - Cond_LProbe : int, range = (0, 1)
                Conditional probability of having a probe given that
                the signal is long
        Output:
        =======
            - std_Exp_Gain : numpy structured array
                Matrix containing information about the gaussian best fit for
                each mouse and the expected gain obtained from the fit value
                and the parameters used in the switch latency protocol
    """
    nameLen = 0
    for name in list(GMM_Fit['Best_Model'].keys()):
        nameLen = max(nameLen,len(name))
    groupLen = 0
    for group in list(Group_dict.keys()):
        groupLen = max(groupLen, len(group))
    ProbeLong = 1 - ProbeShort
    std_Exp_Gain =\
        np.zeros(len(list(GMM_Fit['Best_Model'].keys())),
                 dtype = {'names':('Group', 'Subject', 'Value', 'Fit Mean', 
                 'Fit CV'),'formats':('|S%d'%groupLen, '|S%d'%nameLen,
                 float, float, float)})
    ind = 0
    for group in list(Group_dict.keys()):
        for name in Group_dict[group]:
            m = GMM_Fit['Best_Model'][name].means_[0][0]
            var = GMM_Fit['Best_Model'][name].covariances_[0][0]
            CV = np.sqrt(var) / np.abs(m)
            PS = sts.norm.cdf(Short, m , var)
            PL =  sts.norm.cdf(Long, m, var)
            std_Exp_Gain['Group'][ind] = group
            std_Exp_Gain['Subject'][ind] = name
            std_Exp_Gain['Value'][ind] = (ProbeShort * (1 - Cond_SProbe)) *\
                (1 - PS) + (ProbeLong * (1 - Cond_LProbe)) * PL
            std_Exp_Gain['Fit Mean'][ind] = m
            std_Exp_Gain['Fit CV'][ind] = CV
            ind += 1
    return std_Exp_Gain

def std_Subjective_Error_Rate_GUI(Dataset_Dict, TimeStamps,
                                  DarkStart = 20, 
                                  DarkDuration = 12, tend = 30,
                                  TimeInterval = 3600):
    HBin = max(1, TimeInterval // 3600)
    if TimeInterval > 3600:
        TimeInterval = 3600
    NumSub = len(list(Dataset_Dict.keys()))
    LenSubName = []
    for key in list(Dataset_Dict.keys()):
        LenSubName += [len(key)]
    Hour_Dark,Hour_Light = Hour_Light_and_Dark_GUI(DarkStart, DarkDuration,
                                                 TimeInterval)
    first = True
    ind = 0
    for Datalabel in list(Dataset_Dict.keys()):
        Start_exp = Time_Details_GUI(Dataset_Dict[Datalabel],TimeStamps[Datalabel])[0]
        A, cr = F_Correct_Rate_New_GUI(Dataset_Dict[Datalabel],
                                TimeStamps[Datalabel],Start_exp,24,tend=tend,
                                TimeInterval=TimeInterval)
        
        ReorderIndex = np.hstack((Hour_Dark,Hour_Light))
        if HBin == 1:
            HLabel = TimeUnit_to_Hours_GUI(ReorderIndex,TimeInterval)
            if first:
                VectorError = np.zeros(len(HLabel) * NumSub, 
                        dtype={'names':('Subject','Time','Mean'),
                        'formats':('|S%d'%max(LenSubName),'|S5',float)})
                first = False
            VectorError['Time'][ind:ind + len(HLabel)] = HLabel
            VectorError['Mean'][ind:ind + len(HLabel)] = 1 - cr[ReorderIndex]
            VectorError['Subject'][ind:ind + len(HLabel)] = Datalabel
        else:
            Mean, Median, StdError, HLabel =\
                HourDark_And_Light_BinnedMean_GUI(cr, np.arange(24),
                                                  Hour_Dark,Hour_Light,
                                                  HBin,TimeUnit_Dur_Sec =
                                                  TimeInterval)
            if first:
                VectorError = np.zeros(len(HLabel) * NumSub, 
                        dtype={'names':('Subject','Time','Mean'),
                        'formats':('|S%d'%max(LenSubName),'|S5',float)})
                first = False
            VectorError['Time'][ind:ind + len(HLabel)] = HLabel
            VectorError['Mean'][ind:ind + len(HLabel)] = 1 - Mean
            VectorError['Subject'][ind:ind + len(HLabel)] = Datalabel
        ind += len(HLabel)
    return VectorError

def EpisodsDurationXhour_GUI(Epoch, Time, Bin, timeFirst, timeLast,
                             Type = [3,2], EpochDur=4, total_or_mean='Mean'):
    totEpochs = np.ceil(((timeLast - timeFirst).seconds +\
                (timeLast - timeFirst).days * 3600*24)/EpochDur) + 1
    initialVoidEpochs = ((Time[0]-timeFirst).seconds +\
        ((Time[0]-timeFirst).days * 3600 * 24))//EpochDur
    newTime = dateTimeArange(timeFirst, timeLast, sec=EpochDur)
    BoolVect  = np.zeros(np.int(totEpochs), dtype = int)
    NumEpisod = np.zeros(np.int(totEpochs), dtype = int)
    Epoch = Epoch[:np.int(totEpochs)]
    for thisType in Type:
        BoolVect[initialVoidEpochs:initialVoidEpochs + len(Epoch)]\
            [np.where(Epoch==thisType)[0]] = 1
    Diff  = np.diff(BoolVect)
    Start = np.where(Diff > 0)[0]
    End   = np.where(Diff < 0)[0]
    NumEpisod[Start + 1] = 1
    step = int(3600/EpochDur*Bin)
    iterate=np.arange(int(np.ceil(totEpochs/step)))
    NEP=np.zeros(len(iterate))
    for t in iterate:
        NEP[t] = np.sum(NumEpisod[1 + t*step:(t+1)*step])
    if Start[0] > End[0]:
        End = End[1:]
    if len(Start) > len(End):
        Start = Start[:-1]
    Duration = (End - Start) * EpochDur / 60.0
    DurEpisodes    = np.zeros(np.int(totEpochs))
    DurEpisodes[:] = np.nan
    DurEpisodes[Start + 1] = Duration
    indE = np.where(DurEpisodes >= Bin * 60)[0]
    for t in range(len(indE)):
        print(  '\n\nLOOONG EPISODES SPLITTING TO BE CORRECTED\n\n')
        k = step
        DurEpisodes[indE[t] + k] =\
            DurEpisodes[indE[t]] - 60 * Bin
        DurEpisodes[indE[t]] = (60*Bin)
        while DurEpisodes[indE[t]+k] >= 60 * Bin:
            DurEpisodes[indE[t]+k+step] =\
                DurEpisodes[indE[t]+k]-60*Bin
            DurEpisodes[indE[t]+k] = 60*Bin
            k += step
    NaN_ind = np.where(np.isnan(Epoch))[0]
    DurEpisodes[initialVoidEpochs:initialVoidEpochs + len(Epoch)][NaN_ind] = np.nan
    MeanDurEpisod = np.zeros(int(np.ceil(totEpochs/step)))
    ExtrTime      = np.zeros(int(np.ceil(totEpochs/step)), dtype = 'S19')
    shorter = np.where(DurEpisodes <= EpochDur/60)[0]
    DurEpisodes[shorter] = np.nan
    for t in range(len(MeanDurEpisod)):
        if total_or_mean == 'Mean':
            MeanDurEpisod[t] = np.nanmean(
                DurEpisodes[1 + t*step:(t+1)*step])
        else:
            MeanDurEpisod[t] = np.nansum(
                DurEpisodes[1 + t*step:(t+1)*step])
        ExtrTime[t] = newTime[t*step].isoformat()
    return MeanDurEpisod, Duration, ExtrTime

def F_DayAverage_GUI(Vector, Times, Hour_Dark,Hour_Light, Bin=3600):
    """
        Returns averages time bin by time bin
    """
    
    vectFunc = np.vectorize(TimeBin_From_TimeString)
    Times = Parse_TimeVect(Times)
    timeBinned = vectFunc(Times, Binning=Bin)
    Hours = np.hstack((Hour_Dark,Hour_Light))
    AverageVector = np.zeros(len(Hours))
    HourString = np.zeros(len(Hours),'|S19')
    if max(timeBinned) != max(Hours):
        raise ValueError('Need more than one day')
    k = 0
    for h in Hours:
        Ind = np.where(timeBinned==h)[0]
        AverageVector[k] = np.nanmean(Vector[Ind])
        HourString[k] = Times[Ind[0]].isoformat()
        k += 1
    return AverageVector, HourString

def std_Binned_TimeCourse_GUI(ValueDict, Time, rescaleBy=1):
    nameLen = 0
    for name in list(ValueDict.keys()):
        nameLen = max(nameLen, len(name))
    std_Matrix = np.zeros(len(Time[name]) * len(list(ValueDict.keys())),
                          dtype={'names':('Subject', 'Time', 'Value'),
                                 'formats':('|S%d'%nameLen, '|S19', float)})
    ind = 0
    for name in list(ValueDict.keys()):
        std_Matrix['Subject'][ind:ind + len(ValueDict[name])] = name
        std_Matrix['Time'][ind:ind + len(ValueDict[name])] = Time[name]
        std_Matrix['Value'][ind:ind + len(ValueDict[name])] =\
            ValueDict[name] * rescaleBy
        ind += len(ValueDict[name])
    return std_Matrix


def std_TimeCourse_Group_GUI(std_Matrix, Group_Dict):
    groupLen = 0
#    subjectVect = np.unique(std_Matrix['Subject'])
    for group in list(Group_Dict.keys()):
        groupLen = max(len(group), groupLen)
    if 'Mean' in std_Matrix.dtype.names:
        varName = 'Mean'
    elif 'Value' in std_Matrix.dtype.names:
        varName = 'Value'
    else:
        raise ValueError('Std Matrix must contain a colum \'Value\' or \'Mean\'')
    Time = np.unique(std_Matrix['Time'])
    timeLen = len(Time[0])
    std_Group_Matrix = np.zeros(len(list(Group_Dict.keys())) *\
        len(Time), dtype={'names':('Group','Time','Mean','Median','SEM','25 perc','75 perc'),
                          'formats':('|S%d'%groupLen, '|S%d'%timeLen, float,
                                     float, float,float,float)})
    
    ind = 0
    for group in list(Group_Dict.keys()):
        Matrix = np.zeros((len(Group_Dict[group]), len(Time))) * np.nan

        for k in range(len(Group_Dict[group])):
          
            
            Matrix[k, :] = std_Matrix[varName]\
                [np.where(std_Matrix['Subject'] == Group_Dict[group][k])[0]]
        std_Group_Matrix['Group'][ind:ind + len(Time)] = group
        std_Group_Matrix['Mean'][ind:ind + len(Time)] =\
            np.nanmean(Matrix, axis=0)
        std_Group_Matrix['Median'][ind:ind + len(Time)] =\
            np.nanmedian(Matrix, axis=0)
        std_Group_Matrix['SEM'][ind:ind + len(Time)] =\
            np.nanstd(Matrix, axis=0) / np.sqrt(len(Group_Dict[group]))
        std_Group_Matrix['25 perc'][ind:ind + len(Time)] =\
            np.nanpercentile(Matrix,25, axis=0)
        std_Group_Matrix['75 perc'][ind:ind + len(Time)] =\
            np.nanpercentile(Matrix,75, axis=0)
        std_Group_Matrix['Group'][ind:ind + len(Time)] = group
        std_Group_Matrix['Time'][ind:ind + len(Time)] = Time
        ind += len(Time)
    return std_Group_Matrix

def Return_Hour(timeVect):
    try:
        if len(timeVect) == 5:
            return timeVect
        else:
            if len(timeVect[11:16]) == 5:
                return timeVect[11:16]
            else:
                raise IndexError
    except TypeError:
        return '%d:%d'%(timeVect.hour,timeVect.minute)
            
def std_DailyAverage_SubjectiveTimeCourse_GUI(std_Matrix, Start_Dark=20):
    if 'Mean' in std_Matrix.dtype.names:
        varName = 'Mean'
    elif 'Value' in std_Matrix.dtype.names:
        varName = 'Value'
    else:
        raise ValueError('std_Matrix must contain column \'Value\' or \'Mean\'')
    func = np.vectorize(Return_Hour)
    Hour_and_Min = func(std_Matrix['Time'])
    Daily_hour = np.unique(Hour_and_Min)
    hind=0
    for h in Daily_hour:
        if int(h[:2]) >= Start_Dark:
            break
        hind += 1
    Daily_hour = Daily_hour[np.arange(hind, hind+len(Daily_hour))%\
        len(Daily_hour)]
    subjectVect = np.unique(std_Matrix['Subject'])
    subLen = 0
    for subject in subjectVect:
        subLen = max(len(subject), subLen)
    new_Matrix = np.zeros(len(Daily_hour)*len(subjectVect),
                          dtype={'names':('Subject', 'Time', 'Mean', 'Median',
                          'SEM','25 perc','75 perc'),'formats':('|S%d'%subLen, 'S5', float, float,
                          float,float,float)})
    ind = 0
    for subject in subjectVect:
        new_Matrix['Subject'][ind: ind+len(Daily_hour)] = subject
        new_Matrix['Time'][ind: ind+len(Daily_hour)] = Daily_hour
        SubIndex = np.where(std_Matrix['Subject'] == subject)[0]
        k = 0
        for h in Daily_hour:
            Index = np.where(Hour_and_Min[SubIndex] == h)[0]
            new_Matrix['Mean'][ind+k] = np.nanmean(std_Matrix[varName]\
                [SubIndex][Index])
            new_Matrix['Median'][ind+k] =\
                np.nanmedian(std_Matrix[varName][SubIndex][Index])
            new_Matrix['SEM'][ind+k] =\
                np.nanstd(std_Matrix[varName][SubIndex][Index])/\
                    np.sqrt(len(Index))
            new_Matrix['25 perc'][ind+k] =\
                np.nanpercentile(std_Matrix[varName][SubIndex][Index],25)
            new_Matrix['75 perc'][ind+k] =\
                np.nanpercentile(std_Matrix[varName][SubIndex][Index],75)
            k += 1
        ind += len(Daily_hour)
    return new_Matrix

def EpocheTot_xTimebin_GUI(Epoch, Time, Bin, timeFirst, timeLast,
                           EpochDur=4, Type=[3,2]):
    totEpochs = np.ceil(((timeLast - timeFirst).seconds +\
                (timeLast - timeFirst).days * 3600*24)/EpochDur) + 1

    initialVoidEpochs = ((Time[0]-timeFirst).seconds +\
        ((Time[0]-timeFirst).days * 3600 * 24))//EpochDur

    newTime = dateTimeArange(timeFirst, timeLast, sec=EpochDur)
    BoolVect = np.zeros(np.int(totEpochs),dtype=float)
    Epoch = Epoch[:np.int(totEpochs)]


    for thisType in Type:
        BoolVect[initialVoidEpochs:initialVoidEpochs + len(Epoch)]\
            [np.where(Epoch == thisType)[0]] = 1
    step = int(3600 / EpochDur*Bin)
    iterate = np.arange(int(np.ceil(totEpochs / step)))
    Index = np.where(np.diff(BoolVect) > 0)[0]
    NumEpisode = np.zeros(np.int(totEpochs), dtype=float)
    NumEpisode[Index + 1] = 1
    NaN_ind = np.where(np.isnan(Epoch))[0]
    NumEpisode[initialVoidEpochs:initialVoidEpochs + len(Epoch)][NaN_ind] = np.nan
    NEP = np.zeros(len(iterate))
    ExtrTime = np.zeros(len(iterate), dtype='S19')
    for t in iterate:
        NEP[t] = np.sum(NumEpisode[t*step:(t+1)*step])
        ExtrTime[t] = newTime[t*step].isoformat()
    return NEP, ExtrTime
    
def Time_To_Seconds(timeString):
    try:
       Sec = timeString.hour * 3600 + timeString.minute * 60
    except AttributeError:
        pass
    Sec = int(timeString.split(':')[0]) * 3600 +\
        int(timeString.split(':')[1]) * 60
    return Sec

def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N,mode='valid')[(N-1):]

def runningMean(x, N):
    if N%2 is 1:
        raise ValueError('N must be even')
    x_smooth = []
    for k in range(x.shape[0]):
        x_smooth += [np.mean(x[max(0,k-N//2):min(x.shape[0],k+N//2)])]
    return np.array(x_smooth)
    
    
def smooth_Peak_start_stop_Meck(Peak, bin_len_sec=5, time_len_sec=60):
    """
        Target: smoooth peak value
    """
    dI = int(Peak.shape[0] * bin_len_sec / time_len_sec)
    running_Mean_Peak = runningMean(Peak, dI)
    return running_Mean_Peak
    
def Meck_start_peak_stop(peak_smooth, time_len_sec=60):
    """
        Target:
        =======
        Meck start, peak, stop extracton
        Input:
        ======
            - peak_smooth:
                float array, smoothed 1D peak
            - time_len_sec:
                int, duration in sec
        Output:
        =======
            - start:
                float, start time
            - peak:
                float, peak time
            - stop:
                float, stop time
        
    """
    ARGMAX = np.argmax(peak_smooth)
    MAX = peak_smooth[ARGMAX]
    start_ind = int(np.where(peak_smooth[:ARGMAX] <= MAX * 0.5)[0][-1])
    stop_ind = int(ARGMAX + np.where(peak_smooth[ARGMAX:] <= MAX * 0.5)[0][0])
    dt = time_len_sec / float(peak_smooth.shape[0])
    start = dt * start_ind
    stop = dt * stop_ind
    peak = (start + stop) * 0.5
    return start, peak, stop
    
def compute_LDA(x,y):
    pca_res = PCA_mpl(x)
    X_norm = pca_res.a

    
    LDA = lda(n_components = 1)
#    lda_res = LDA.fit(X_norm, y, store_covariance=True)
    lda_res = LDA.fit(X_norm, y)

    y_pred = lda_res.predict(X_norm)

    score_list= lda_res.score(X_norm,y)
    prob_pred = lda_res.predict_proba(X_norm)



    params = lda_res.scalings_
    
    v = params / np.linalg.norm(params)
#    v[0] = -v[0]
    
    
    return(y_pred,prob_pred,score_list,v,X_norm,lda_res)

def compute_structure_matrix(y,X,X_norm,v):
    X_norm_1 = X_norm[:,[1,0]]
    Y = y.reshape((y.shape[0],1))
    
    S_11 = np.matrix((X_norm_1-np.mean(X_norm_1,axis=0))).T * np.matrix((X_norm_1-np.mean(X_norm_1,axis=0)))
    S_12 = np.matrix((X_norm_1-np.mean(X_norm_1,axis=0))).T * np.matrix((Y - np.mean(Y,axis=0)))
    S_21 = np.matrix((Y - np.mean(Y,axis=0))).T * np.matrix((X_norm_1-np.mean(X_norm_1,axis=0)))
    S_22 = np.matrix((Y - np.mean(Y,axis=0))).T * np.matrix((Y - np.mean(Y,axis=0)))
    
    Q_h = S_12 * np.linalg.inv(S_22) * S_21
    Q_t = S_11
    Q_e = Q_t - Q_h

    eig,eig_v = np.linalg.eig(np.linalg.inv(Q_e)*Q_h)
    
    v_ort = v[[1,0]]
    v_ort[0] = v_ort[0]*-1
    
    if (np.abs(eig_v[0,0]) - np.abs(v_ort[0][0])) < 10**-12 and (np.abs(eig_v[1,0]) - np.abs(v_ort[1][0])) < 10**-12:
       Index_for_color = 0
    else:
        Index_for_color = 1
    
    LAMBDA_2, A = np.linalg.eig( np.linalg.inv(S_11) * S_12 * np.linalg.inv(S_22) * S_21)
    
    if Index_for_color:
        LAMBDA_2 = LAMBDA_2[[1,0]]
    
    for k in range(A.shape[1]):
        A[:,k] = A[:,k] / np.sqrt(A[:,k] .T * Q_e * A[:,k])
   
    std_weights = np.diag(np.sqrt(np.diagonal(Q_e))) *A
    Struct_mat = np.linalg.inv(np.diag(np.sqrt(np.diagonal(Q_e)))) * Q_e * A
    
    if np.abs( eig_v[0,1]-eig_v[1,1] ) <10**(-12):
        explained_variance = LAMBDA_2[0]
    else:
        explained_variance = LAMBDA_2[0]
        
    return std_weights,Struct_mat,explained_variance,v_ort,Index_for_color

def rotazione(v_ort):
    angle = np.arctan2(-v_ort[0],v_ort[1])
    Rot = np.zeros((2,2))
    Rot[0,0] = np.cos(angle)
    Rot[1,1] = np.cos(angle)
    Rot[0,1] = -np.sin(angle)
    Rot[1,0] = np.sin(angle)

    Rot2 = np.zeros((2,2))
    Rot2[0,0] = np.cos(angle - np.pi*0.5)
    Rot2[1,1] = np.cos(angle-np.pi*0.5)
    Rot2[0,1] = -np.sin(angle-np.pi*0.5)
    Rot2[1,0] = np.sin(angle-np.pi*0.5)
    
    return Rot,Rot2  

def traslazione(v,par=3.5):
    transl = par*v
    if  v[1] < 0 and v[0]>0 and np.abs(v[0]) < np.abs(v[1]):
        transl = -transl
    elif v[1] < 0 and v[0]<0 :
        transl = -transl
        
    elif  v[0] < 0 and v[0]<0 and np.abs(v[0]) > np.abs(v[1]):
        transl = -transl
        
    return transl
    
def gaussian_fit(X_norm,v_ort,hd,hl):
    # per ruotare perpendicolamente devo passare v_ort
    v = v_ort[[1,0]]
    v[0] = -v[0]
    
    
    v_ort = v_ort / np.linalg.norm(v_ort)
    projected = np.dot(X_norm,v_ort)
#    projected = np.dot(X_norm[:,[1,0]],v_ort.T)
#    proj = np.zeros((x.shape[0],2))
#    proj[:,0] = res[:,0] * v[0]
#    proj[:,1] = res[:,0] * v[1]
#    projected = np.dot(X_norm[:,[1,0]],v_ort)
#    projected = projected.reshape((projected.shape[0],1))
    g_fit_Dark = mxt.GMM(1).fit(projected[hd])
    g_fit_Light = mxt.GMM(1).fit(projected[hl])
    gauss_dark = sts.norm(loc = g_fit_Dark.means_[0][0],scale = g_fit_Dark.covars_[0][0])
    gauss_light = sts.norm(loc = g_fit_Light.means_[0][0],scale = g_fit_Light.covars_[0][0])
    
    Rot,Rot2 = rotazione(v)
    transl = traslazione(v)
    transl = transl.reshape((transl.shape[0],1))

    x_light = np.linspace(gauss_light.ppf(0.01), gauss_light.ppf(0.99), 100)
    x_dark = np.linspace(gauss_dark.ppf(0.01), gauss_dark.ppf(0.99), 100)
    y_light = gauss_light.pdf(x_light)
    y_dark =  gauss_dark.pdf(x_dark)
    y_dark= y_dark / np.max([np.max(y_dark),np.max(y_light)])
    y_light = y_light / np.max([np.max(y_dark),np.max(y_light)])
    v_light = np.zeros((2,len(x_light)))
    v_light[0,:] = x_light
    v_light[1,:] = y_light
    v_dark = np.zeros((2,len(x_light)))
    v_dark[0,:] = x_dark
    v_dark[1,:] = y_dark
    
    line_v = np.zeros((2,2))
    line_v[1,0] = np.min((x_light[0],x_dark[0])) 
    line_v[1,1] = np.max((x_light[-1],x_dark[-1])) 
#    rot_line = np.dot(Rot2,line_v) + transl
    rot_v_light = np.dot(Rot,v_light) + transl
    rot_v_dark = np.dot(Rot,v_dark) + transl
    line_light = (rot_v_light[0,:] - transl [0]- np.mean(X_norm,axis=0)[0])/v_ort[0]*v_ort[1]+np.mean(X_norm,axis=0)[1]  +transl[1]
    line_dark =  (rot_v_dark[0,:] - transl [0]- np.mean(X_norm,axis=0)[0])/v_ort[0]*v_ort[1]+np.mean(X_norm,axis=0)[1]  +transl[1]
    return line_light,line_dark,rot_v_light,rot_v_dark


def computeReactionTime(Y,TimeStamps):
    onset = np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    offset = np.where(Y['Action']==TimeStamps['Start Intertrial Interval'])[0]
    if onset[0] > offset[0]:
        offset = offset[1:]
    if onset[-1] > offset[-1]:
        onset = onset[:-1]
    if onset.shape[0] != offset.shape[0]:
        raise ValueError('onset and offset must have same dimention')
    react_time = np.zeros(onset.shape[0]) * np.nan
    actionList = Y['Action'].tolist()
    for k in range(onset.shape[0]):
        i = onset[k]
        end = offset[k]
        try:
            left_in = actionList[i+1:end].index(TimeStamps['Left NP In'])
        except ValueError:
            left_in = np.inf
        try:
            right_in = actionList[i+1:end].index(TimeStamps['Right NP In'])
        except ValueError:
            right_in = np.inf
        if left_in > right_in:
            react_time[k] = Y['Time'][i+right_in] - Y['Time'][i]
        elif left_in < right_in:
            react_time[k] = Y['Time'][i+left_in] - Y['Time'][i]
        k += 1
    mask = True - np.isnan(react_time)
    react_time = react_time[mask]
    onset = onset[mask]
    Start_exp = F_Start_exp_GUI(Y,TimeStamps)
    trialHour=F_Hour_Trial_GUI(Y,TimeStamps,Start_exp, onset,None,'a',None,24)[1]
    return react_time,onset,trialHour

def computeSleepPerHrs(sleepData,epType ='NR'):
    epoch = sleepData.Stage
    if epType == 'S':
       epoch[np.where(epoch=='NR')[0]] = 'S'
       epoch[np.where(epoch=='NR*')[0]] = 'S'
       epoch[np.where(epoch=='R')[0]] = 'S'
       epoch[np.where(epoch=='R*')[0]] = 'S'
    else: 
        epoch[np.where(epoch == (epType+'*'))[0]] = epType
    time = sleepData.Timestamp
    func = lambda h : h.hour
    v_func = np.vectorize(func)
    hours = v_func(time)
    perc_vect = np.zeros(24) * np.nan
    for h in range(24):
        index = np.where(hours == h)[0]
        if index.shape[0] == 0:
            continue
        res = np.where(epoch[index] == epType)[0]
        perc = float(res.shape[0]) / index.shape[0] * 100
        perc_vect[h] = perc
    
    return perc_vect



def computeDailyScore(behaviorData, sleepData, TimeStamps, parBeh, parSleep):
    if parBeh == 'Reaction Time':
        behav_val, onset, trialHour = computeReactionTime(behaviorData,TimeStamps)
        dailyScore_beh = daily_Median_Mean_Std_GUI(behav_val,trialHour,HBin=3600)[1]
    elif parBeh == 'Error Rate':
        dailyScore_beh = F_Correct_Rate_GUI(behaviorData,24,TimeStamps)[1]
        dailyScore_beh = (1 - dailyScore_beh) * 100
        
    if parSleep == 'Sleep Total':
        dailyScore_sleep = computeSleepPerHrs(sleepData,'S')
    elif parSleep == 'NREM Total':
        dailyScore_sleep = computeSleepPerHrs(sleepData,'NR')
    elif parSleep == 'REM Total':
        dailyScore_sleep = computeSleepPerHrs(sleepData,'R')
    elif parSleep == 'Wake Total':
        dailyScore_sleep = computeSleepPerHrs(sleepData,'W')
    return dailyScore_beh,dailyScore_sleep

def performLDA_Analysis(behaviorData, sleepData, TimeStamps, parBeh, parSleep, dark_start,dark_len):
    hd,hl = Hour_Light_and_Dark_GUI(dark_start,dark_len,TimeInterval=3600)
    
    dailyScore_beh,dailyScore_sleep = computeDailyScore(behaviorData, sleepData, TimeStamps, parBeh, parSleep)
    
    print(dailyScore_beh)
    X = np.zeros((24,2))
    X[:,0] = dailyScore_beh
    X[:,1] = dailyScore_sleep
    
    y = np.ones(24)
    
    y[hl] = 0 # zeros mark light phase values
    y_pred,prob_pred,score_list,v,X_norm,lda_res = compute_LDA(X,y)
    std_weights,Struct_mat,explained_variance,v_ort,Index_for_color = compute_structure_matrix(y,X,X_norm,v)
    res = gaussian_fit(X_norm,v,hd,hl)
    
    return res,X_norm,Struct_mat,explained_variance,v_ort,v,y_pred,lda_res,Index_for_color,y