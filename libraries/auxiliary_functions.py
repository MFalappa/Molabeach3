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
from copy import deepcopy
from scipy.signal import filtfilt,ellip
from scipy.optimize import curve_fit
from PyQt5.QtWidgets import QInputDialog
from bisect import bisect_left
import scipy.stats as sts
import sklearn.mixture as mxt
import numpy as np
import datetime as dt
import warnings
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda
from matplotlib.mlab import PCA as PCA_mpl
#from sklearn.decomposition import PCA as PCA_mpl

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

def F_Correct_Rate_GUI(Y,Start_exp,period,TimeStamps,*tend,type_data='TSE'):
    
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

    if type_data == 'TSE':
        start_trial = 'Center Light On'
    elif 'AM-Microsystems':
        start_trial = 'ACT_START_TEST'

    TrialOnSet=np.where(Y['Action']==TimeStamps[start_trial])[0]
        
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

def computeReactionTime(Y,TimeStamps):
#    
#    try:
#        onset = np.where(Y['Action']==TimeStamps['ACT_START_TEST'])[0]
#    except:
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
    mask = True ^ np.isnan(react_time)
    react_time = react_time[mask]
    onset = onset[mask]
    Start_exp = F_Start_exp_GUI(Y,TimeStamps)
    trialHour=F_Hour_Trial_GUI(Y,TimeStamps,Start_exp, onset,None,'a',None,24)[1]
    return react_time,onset,trialHour

def performLDA_Analysis(behaviorData, sleepData, TimeStamps, parBeh, parSleep, dark_start,dark_len,type_data):
    hd,hl = Hour_Light_and_Dark_GUI(dark_start,dark_len,TimeInterval=3600)
    
    dailyScore_beh,dailyScore_sleep = computeDailyScore(behaviorData, sleepData, TimeStamps, parBeh, parSleep,type_data)
    
#    print(dailyScore_beh)
    X = np.zeros((24,2))
    X[:,0] = dailyScore_beh
    X[:,1] = dailyScore_sleep
    
    y = np.ones(24)
    
    y[hl] = 0 # zeros mark light phase values
    y_pred,prob_pred,score_list,v,X_norm,lda_res = compute_LDA(X,y)
    std_weights,Struct_mat,explained_variance,v_ort,Index_for_color = compute_structure_matrix(y,X,X_norm,v)
    res = gaussian_fit(X_norm,v,hd,hl)
    
    return res,X_norm,Struct_mat,explained_variance,v_ort,v,y_pred,lda_res,Index_for_color,y

def computeDailyScore(behaviorData, sleepData, TimeStamps, parBeh, parSleep,type_data):
    if parBeh == 'Reaction Time':
        behav_val, onset, trialHour = computeReactionTime(behaviorData,TimeStamps)
        dailyScore_beh = daily_Median_Mean_Std_GUI(behav_val,trialHour,HBin=3600)[1]
    elif parBeh == 'Error Rate':
        
        dailyScore_beh = F_Correct_Rate_GUI(behaviorData,0,24,TimeStamps,type_data=type_data)[1]
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
    g_fit_Dark = mxt.GaussianMixture(1).fit(projected[hd])
    g_fit_Light = mxt.GaussianMixture(1).fit(projected[hl])
    gauss_dark = sts.norm(loc = g_fit_Dark.means_[0][0],scale = g_fit_Dark.covariances_[0][0])
    gauss_light = sts.norm(loc = g_fit_Light.means_[0][0],scale = g_fit_Light.covariances_[0][0])
    
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
#    print(Sample.shape)
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
    
def std_Switch_Latency_GUI(Record_Switch, HSSwitch, DataGroup, Dark_start=20, Dark_length=12):
    Tot_Subjects = 0
    lenName = 0
    for name in list(Record_Switch.keys()):
        Tot_Subjects += 1
        lenName = max(lenName, len(name))
#    for k in list(Record_Switch.keys()):
#        print(k, len(Record_Switch[k]))
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

def createAbsoluteTime(Y,indexVect,Timestamps):
    day = Y['Time'][np.where(Y['Action']==Timestamps['Start Day'])[0][0]]
    month = Y['Time'][np.where(Y['Action']==Timestamps['Start Month'])[0][0]]
    year = Y['Time'][np.where(Y['Action']==Timestamps['Start Year'])[0][0]]
    
    hour = Y['Time'][np.where(Y['Action']==Timestamps['Start Hour'])[0][0]]
    minute = Y['Time'][np.where(Y['Action']==Timestamps['Start Minute'])[0][0]]
    second = Y['Time'][np.where(Y['Action']==Timestamps['Start Second'])[0][0]]
    
    secs = Y['Time'][indexVect]
    delta_sec = np.zeros(secs.shape[0],dtype=dt.timedelta)
    for k in range(secs.shape[0]):
        delta_sec[k] = dt.timedelta(0,secs[k])
    abstime = dt.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    func = lambda dti : abstime + dti
    vec_func = np.vectorize(func)
    return vec_func(delta_sec)

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

def getRewardTrialMED(Y,TimeStamps,start,stop):
    reward_start = []
    for k in range(start.shape[0]):
        if TimeStamps['Give Pellet Center'] in Y['Action'][start[k]:stop[k]]:
            reward_start += [start[k]]
    return np.array(reward_start)

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
    
def condition_check(table_row,type_tr):
    if type_tr == 'Long_Probe':
        return table_row['type'] == b'Long' and table_row['isProbe']
    elif type_tr == 'Long_reward':
        return table_row['type'] == b'Long' and table_row['isCorrect'] and not table_row['isProbe']
    elif type_tr == 'Long':
        return table_row['type'] == b'Long' and table_row['isCorrect']

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

                
                    idx = np.where(np_in[k][:,1] <= tl)[0]
                    if idx.shape[0] and np_out[k].shape[0] > idx[-1]:
#                        print(k)

                ## MODIFICA DA IN AD OUT
                #switch = np.concatenate((switch,[left_in[k][idx[-1],1]]))
                        switch = np.concatenate((switch,[np_out[k][idx[-1],1]]))
                        hrs_switch = np.concatenate((hrs_switch, [table[k]['absTime']]))
    return left,right,switch,hrs_switch

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
                     'formats':(dt.datetime,int,int,'S5',bool,bool)})
    table['absTime'] = times[:trial_type.shape[0]]
    table['start'] = start[:trial_type.shape[0]]
    table['stop'] = stop[:trial_type.shape[0]]
    ind_short = np.where(trial_type == 0)[0]
    table['type'] = 'Long'
    table['type'][ind_short] =  'Short'
    table['isCorrect'] = performance[:trial_type.shape[0]]
    table['isProbe'] = probe[:trial_type.shape[0]]
    
    return table,left_in,left_out,right_in,right_out,start,stop

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
    
def F_New_Gr_Switch_Latency_GUI(Datas,TimeStamps,Mouse_Name,H_By_H=False,ts=3,tl=6, type_tr='Long',scale=1,Tend=15,Long_Side='r',isMEDDict={}):


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
                reply = QInputDialog.getText(None,'Choose long location, Left (L) or Right (R)',name)
                if reply[1]:
                    if 'L' in reply[0].upper():
                        l_side = 'l'
                        cond_to_check = False
                    elif 'R' in reply[0].upper():
                        l_side = 'r'
                        cond_to_check = False                    
        #=============to be tested
            
#        Datas[name].Dataset = Rescale_Time_GUI(Datas[name].Dataset, TimeStamps, scale)
    
        table,left_in,left_out,right_in,right_out,start,stop = switch_analysis_gui(Datas[name].Dataset, 
                                                                                   TimeStamps, 
                                                                                   ts, 
                                                                                   tl,
                                                                                   long_side=l_side,
                                                                                   isMED=isMEDDict[name])
        
        left,right,switch,hrs_switch = compute_latency(table,left_in,left_out,right_in,right_out,start,stop,ts,tl,type_tr,long_side=l_side)
        switch_dict[name] = switch
        table_dict[name] = table
        left_dict[name] = left
        right_dict[name] = right
        hrs_switch_dict[name] = hrs_switch
    return(table_dict,left_dict,right_dict,switch_dict,hrs_switch_dict)

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
    p0 = np.hstack(([amplitude0, phase0, translation0] ))

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


    