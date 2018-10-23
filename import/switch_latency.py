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

import sys
sys.path.append('C:\Users\MFalappa\Documents\Phenopy\MyPython_Lib')
import numpy as np
import scipy.stats as sts
from Modify_Dataset_GUI import *
import sklearn.mixture as mxt
import sklearn.lda as lda
from scipy.optimize import curve_fit
import datetime
from sklearn.utils import weight_vector
from sklearn.decomposition import PCA, FastICA
from sklearn.utils.sparsetools import _graph_validation,_graph_tools
from sklearn.utils import lgamma,weight_vector
from sklearn.neighbors import typedefs
from statsmodels.api import add_constant, OLS
from time import clock
from bisect import bisect_left

def F_New_Gr_Switch_Latency_GUI(Datas, TimeStamps, Mouse_Name, H_By_H=False, ts=3,
                            tl=6, type_tr='Long', scale=1000, Tend=15,
                            Long_Side='r'):


    for name in Mouse_Name:
        if type(Long_Side) is dict:
            l_side = Long_Side[name]
        else:
            l_side = Long_Side
            
        Datas[name] = Rescale_Time_GUI(Datas[name], TimeStamps[name], scale)
        x = Time_Details_GUI(Datas[name], TimeStamps[name])
    
        table,left_in,left_out,right_in,right_out,start,stop = switch_analysis_gui(Datas[name], TimeStamps[name], ts, tl)
        
        left,right,switch = compute_latency(table,left_in,left_out,right_in,right_out,start,stop,tl,type_tr)
        
    return(table,left,right,switch)

def condition_check(table_row,type_tr):
    if type_tr == 'Long_Probe':
        return table_row[2] == 'Long' and table_row[4]
    elif type_tr == 'Long_Reward':
        return table_row[2] == 'Long' and table_row['isCorrect'] and not table_row['isProbe']
    elif type_tr == 'Long':
        return table_row[2] == 'Long' and table_row['isCorrect']
        
def compute_latency(table,left_in,left_out,right_in,right_out,start,stop,tl,type_tr):
    left = []
    right = []
    switch = []
    
    for k in range(table.shape[0]):
        if condition_check(table[k],type_tr):
            left = np.concatenate((left,left_in[k][:,1]))
            right = np.concatenate((right,right_in[k][:,1]))
            idx = np.where( left_in[k][:,1] <= tl)[0]
            if idx.shape[0]:
                ## MODIFICA DA IN AD OUT
                #switch = np.concatenate((switch,[left_in[k][idx[-1],1]]))
                switch = np.concatenate((switch,[left_out[k][idx[-1],1]]))
            
    return left,right,switch
            
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
    
def switch_analysis_gui(Y,TimeStamps,ts,tl):
    
    left_in,left_out,right_in,right_out,start,stop = create_np_activity(Y,TimeStamps)
    rewarded_start = getRewardedTrial(Y, TimeStamps)
    trial_type = switch_type_trial(Y,TimeStamps,ts,tl)
    performance = switch_performance(trial_type,left_in,right_in,ts,tl)
    probe = switch_probe_check(start, performance, rewarded_start)
    table = np.zeros(trial_type.shape[0], dtype = {'names':('start','stop','type','isCorrect','isProbe'),
                     'formats':(int,int,'S5',bool,bool)})
    table['start'] = start
    table['stop'] = stop
    ind_short = np.where(trial_type == 0)[0]
    table['type'] = 'Long'
    table['type'][ind_short] =  'Short'
    table['isCorrect'] = performance
    table['isProbe'] = probe
    
    return table,left_in,left_out,right_in,right_out,start,stop
    

def switch_probe_check(start, performance, rewarded_start):
    correct = np.where(performance)[0]
    probe = np.zeros(performance.shape[0],dtype=bool)
  
    for k in correct:
        if not (start[k] in rewarded_start):
            probe[k] = True
      
    return probe
    
def switch_performance(trial_type,left_in,right_in,ts,tl):
    
    performance = np.zeros(trial_type.shape[0],dtype = bool)
    
    for k in range(trial_type.shape[0]):
        if  k == 3701:
            pass
        # ceck short location
        if trial_type[k]==0: 
            try:
                tmp_left = np.where( left_in[k][:,1] >= ts)[0][0]
            except IndexError:
                continue
            
            try:
                tmp_right = np.where( right_in[k][:,1] >= ts)[0][0]
                if tmp_right > tmp_left:
                    performance[k] = True
            except IndexError:
                performance[k] = True
                continue
            
        else:
            #Check long location
     
            try:
               tmp_right = np.where( right_in[k][:,1] >= tl)[0][0]
            except IndexError:
                continue
            
            try:
                tmp_left = np.where( left_in[k][:,1] >= tl)[0][0]
                if tmp_right < tmp_left:
                    performance[k] = True
            except IndexError:
                performance[k] = True
                continue
            
    return(performance)
    
    
def switch_type_trial(Y,TimeStamps,ts,tl):
    
    light_on = np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    light_off = np.where(Y['Action']==TimeStamps['Center Light Off'])[0]  
    start_trial = np.where(Y['Action']==TimeStamps['Center Light On'])[0]
  
    light_on = Y['Time'][light_on]
    light_off =  Y['Time'][light_off]
    
    duration = light_off - light_on
    tmp = np.zeros((2,duration.shape[0]))
    
    tmp[0,:] = np.abs(duration-ts)
    tmp[1,:] = np.abs(duration-tl)
    # 0, short 1, long
    trial_type = np.argmin(tmp,axis = 0)
    
    return(trial_type)
    
    
def create_np_activity(Y,TimeStamps):
    
    Left_NP_in=np.where(Y['Action']==TimeStamps['Left NP In'])[0]
    Left_NP_out=np.where(Y['Action']==TimeStamps['Left NP Out'])[0]
    Right_NP_in=np.where(Y['Action']==TimeStamps['Right NP In'])[0]
    Right_NP_out=np.where(Y['Action']==TimeStamps['Right NP Out'])[0]
    
    start_trial = np.where(Y['Action']==TimeStamps['Center Light On'])[0]
    end_trial = np.where(Y['Action']==TimeStamps['Start Intertrial Interval'])[0]
    
    left_in = {}
    left_out = {}
    right_in = {}
    right_out = {}
    
    stop = np.zeros(start_trial.shape[0],dtype = int)
    start = np.zeros(start_trial.shape[0],dtype = int)
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
    return(left_in,left_out,right_in,right_out,start,stop)
    

    
if __name__ == '__main__' : 
    Y = np.genfromtxt('C:\Users\MFalappa\Desktop\\prova.csv',
                      delimiter='\t', dtype={'names':('Time','Action'),'formats':(float,float)})
    TimeStamps = np.load('C:\Users\MFalappa\Documents\Phenopy\Timestamps_repo\TSE.npy').all()
    t0 = clock()
    Y = Y[:np.where(Y['Action']==36)[0][-1]+1]
    d = {'ciccio':Y}
    td = {'ciccio':TimeStamps}
    res=F_New_Gr_Switch_Latency_GUI(d,td,['ciccio'],ts=3,tl=6)
    import matplotlib.pylab as plt
    plt.close('all')
    plt.figure()
#    plt.hist()