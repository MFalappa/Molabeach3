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
"""

import sys
sys.path.append('/Users/Matte/Python_script/Phenopy/libraries')
import numpy as np
import matplotlib.pylab as plt
import h5py
import os
import dill
import datetime as dt

from scipy.signal import filtfilt,butter,ellip
from scipy.stats import signaltonoise
from time import clock
from multiprocessing import Pool
from copy import deepcopy

from detectionParametrized import *
from Modify_Dataset_GUI import *
from create_spike_func import *

plt.close('all')



fld = '/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/raw'
fld_RMS = '/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/rms'
path_save = '/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/detected'
scored = '/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/sleep'
figFld = '//Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/figure'
carPath = '/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/car'
lfp_fld = '/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/lfp'

if not ( os.path.exists(fld) * os.path.exists(path_save) * os.path.exists(fld_RMS)):
    raise ValueError, "One of the path (fld, fld_RMS, path_save) do not exist!"

convolveSec = 0.0 # number of sec used for convolution (value taken from "Falling-Edge, Variable Threshold (FEVT) Method for the Automated Detection of Gastric Slow Wave Events in High-Resolution Serosal Electrode Recordings")
nDet = 30         # number of stddev for threshold (value taken from "Falling-Edge, Variable Threshold (FEVT) Method for the Automated Detection of Gastric Slow Wave Events in High-Resolution Serosal Electrode Recordings")
nArt = 50
refracMs = 2.     # refractory period in ms
pre = 25          # number of pre-peak time points
post = 30         # number of post-peak time points
numProcesses = 8  # select number of parallel processes
corrTh = 0.8

maxDur = 4.5
totChann = 16

def vectorizedRowCorr(A,B):
    N = A.shape[1]
    sA = A.sum(axis=1)
    sB = B.sum(axis=1)
    p1 = N*np.einsum('ij,ij->i',A,B)
    p2 = sA * sB
    p3 = N * np.sum(np.power(B, 2), axis=1) - np.power(sB, 2)
    p4 = N * np.sum(np.power(A, 2), axis=1) - np.power(sA, 2)
    return (p1 - p2) / np.sqrt(p3*p4)

def extractWf(data, pre, post, ch, totchan = np.arange(16)):
    wf = np.zeros((pre.shape[0], post[0] - pre[0]), dtype=np.float32)
    for k in xrange(pre.shape[0]):
        wf[k,:] = data[pre[k]: post[k]]
    return wf
    
    
def ellip_bandpass(lowcut, highcut, fs, order=3, rp=0.1, rs=40):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = ellip(order, rp, rs, [low, high], btype='bandpass')
    return b, a

def ellip_bandpass_filter(data, lowcut, highcut, fs, order=5, rp=0.1, rs=40):
    b, a = ellip_bandpass(lowcut, highcut, fs, order=order, rp=rp, rs=rs)
    y = filtfilt(b, a, data)
    return y

def extractor(variable):
    path, chann = variable

    fh = h5py.File(path,'r')
    y = fh['data']['streams']['wave'][chann,:]
    
    fs = fh['data']['streams']['fs'].value[0][0] 
    
    if fs > 7000:
        HF = 5000
    else:
        HF = 3000
        
    d = ellip_bandpass_filter(y, 300, HF, fs)
 
    fh.close()
    return d
    
def get_sleep_name_detection(path):
    sbj_spk = os.path.basename(path)
    sbj = sbj_spk.split('_')[0]
    list_file = os.listdir(scored)
    sub_list = []
    for sName in list_file:
        if not sName.endswith('.txt'):
            continue
        if not sbj in sName:
            continue
        sub_list += [sName]
    phase = sbj_spk.split('_')[2].upper()
    phase_list = []
    for sName in sub_list:
        if phase in sName.upper():
           phase_list += [sName]
    hour = sbj_spk.split('_')[3].upper()
    for sName in phase_list:
        if hour in sName.upper():
            return sName
            
def extractWS(path,scored):
    
    fh = h5py.File(path,'r')
    tm = fh['data']['info']['starttime']
    fs = fh['data']['streams']['fs'].value[0][0]
    
    time = ''
    for kk in range(tm.shape[0]):
        time += str(unichr(tm[kk]))
        
    tm = fh['data']['info']['date']
    date = ''
    for kk in range(tm.shape[0]):
        date += str(unichr(tm[kk]))
    
    fh.close()
    
    sleepName = get_sleep_name_detection(path)

    sleep_data = EEG_Data_Struct(PathToFile = os.path.join(scored,sleepName),delimiter = '\t',header = 19)
    
    tmp = extract_epi(sleep_data,epoch='W',merge_if=1,min_epi_len=0)    
    w = (np.array((tmp['Start'],tmp['End']),dtype = int))*4
    tmp = extract_epi(sleep_data,epoch='R',merge_if=1,min_epi_len=0)    
    r = (np.array((tmp['Start'],tmp['End']),dtype = int))*4
    tmp = extract_epi(sleep_data,epoch='NR',merge_if=1,min_epi_len=0)    
    nr = (np.array((tmp['Start'],tmp['End']),dtype = int))*4
    

    startSU = dt.datetime.strptime(date+'T'+time,'%Y-%b-%dT%H:%M:%S')
    startSL = sleep_data.Timestamp[0]
    delta = startSL - startSU
    
    if delta < dt.timedelta(0):
        delta =  startSU - startSL
        ct = -(delta.seconds + 3600*24*delta.days)
    else:
        ct = (delta.seconds + 3600*24*delta.days)
  
    ct = int(ct*fs)
    w = np.array((w*fs),dtype = int) + ct
    r = np.array((r*fs),dtype = int) + ct
    nr = np.array((nr*fs),dtype = int) + ct
    # filter for positive vals
    w = w[:, (w[0,:] > 0) * (w[1,:] > 0) > 0]
    r = r[:, (r[0,:] > 0) * (r[1,:] > 0) > 0]
    nr = nr[:, (nr[0,:] > 0) * (nr[1,:] > 0) > 0]
    return w,r,nr,fs
    
def thresholding(carPath,fs,stage,keepChan,nDet,convolveSec,saveFig=False,
                 stageType='Wake',recName='',fldSave='.'):
    
    th = np.zeros((1,len(keepChan)))*np.nan
    
    for ch in keepChan:

        fCar = h5py.File(os.path.join(carPath,recName.replace('raw','car')),'r')
        carSig = fCar['ch_%d'%ch]
        
        y = []
        for ii in range(stage.shape[1]):
            y = np.hstack((y,carSig[stage[0,ii]:stage[1,ii]]))

        yNEO = y[1:-1] * y[1:-1] - y[2:]*y[:-2]
        # smooth signal if needed    
        if convolveSec > 0:
            yNEO = np.convolve(yNEO, np.ones(convolveNum)/convolveNum, mode='same')

        fCar.close()
        threshold = nDet * np.nanmedian(np.abs(yNEO - np.nanmedian(yNEO))) / 0.6745 
        
        th[0,ch] = threshold  
        if saveFig:
            plt.figure()
            samples = int(min(119*fs,yNEO.shape[0]))
            x_axis = np.linspace(0,samples/fs,samples)
            plt.plot(x_axis, yNEO[:samples])
            plt.plot(x_axis[[0,-1]],[threshold]*2, '--r')
            plt.xlim(x_axis[0],x_axis[-1])
            plt.title(recName + ' '+ stageType)
            plt.xlabel('time(sec)')
            plt.ylabel('NEO')
            plt.savefig(os.path.join(fldSave,recName.split('.')[0] + '_' + stageType + '_channel_%d' %ch + '.png'))
            plt.close()
       
    return th
    
    
def no_sleep_thresholding(carPath,fs,keepChan,nDet,convolveSec,recName=''):

    thr = np.zeros(len(keepChan))*np.nan
    
    for ch in keepChan:
        
        fCar = h5py.File(os.path.join(carPath,recName.replace('raw','car')),'r')
        y = fCar['ch_%d'%ch]
    
        yNEO = y[1:-1] * y[1:-1] - y[2:]*y[:-2]
        # smooth signal if needed    
        if convolveSec > 0:
            yNEO = np.convolve(yNEO, np.ones(convolveNum)/convolveNum, mode='same')
        
        fCar.close()
        threshold = nDet * np.nanmedian(np.abs(yNEO - np.nanmedian(yNEO))) / 0.6745 
        
        thr[ch] = threshold  
        
    return thr

if __name__ == '__main__':
    dirFh = os.listdir(fld)
    list_done = os.listdir(path_save)
    for fname in dirFh:

        if not fname.endswith('.mat'):
            continue
        if fname.startswith('.'):
            continue
        path = os.path.join(fld,fname)
        if (os.path.basename(path).split('raw')[0] + 'detected.mat') in list_done:
            print 'skipped %s'%os.path.basename(path)
            continue
        print 'Detection %s'%os.path.basename(path)
        
            
        # name of the RMS dict
        nameRMS = os.path.basename(path).split('raw')[0] + 'RMS.npy'
        try:
            keepChan = np.array(np.load(os.path.join(fld_RMS,nameRMS)).all()['keepChann'])
        except:
             keepChan = range(16)   
        
        th_M = np.zeros((1,totChann))*np.nan
        
#        th_nr = np.zeros(totChann)*np.nan
#        th_r = np.zeros(totChann)*np.nan
#        th_w = np.zeros(totChann)*np.nan

#==============================================================================        
        subSpkInd = np.array([],dtype=np.int32)
        subWf = np.zeros((0,pre+post),dtype=np.float32)
        subTs = np.array([],dtype=np.float32)
        subCh = np.array([],dtype=np.int32)
        
#        if not os.path.exists(os.path.join(lfp_fld,fname.replace('raw','lfp'))):
#            fl = h5py.File(os.path.join(lfp_fld,fname.replace('raw','lfp')),'w')
#            
#            t0=clock()
#            print 'Computing Local Field Potential'
#            ff = h5py.File(path,'r')
#            streams = ff['data']['streams']
#            wave = streams['wave']
#            fs = streams['fs'].value[0][0]
#            
#            ch = wave.shape[0]
#            
#            for kk in range(ch):
#                lfp = ellip_bandpass_filter(wave[kk,:], 0.1, 300, fs)
#                fl.create_dataset('lfp_%d'%kk, data = lfp, compression = 'gzip' ,compression_opts=9)
#            
#            fl.close()
#            ff.close()
#            print 'LFP completed in %f min'%((clock()-t0)/60)

        #decommentare da qui#
        if not os.path.exists(os.path.join(carPath,fname.replace('raw','car'))):
            fCar = h5py.File(os.path.join(carPath,fname.replace('raw','car')),'w')
            t0 = clock()
            for ch in keepChan:
                print 'CAR computing for channel %d'%ch
                fh = h5py.File(path,'r')
                dat = fh['data']
                streams = dat['streams']
                fs = streams['fs'].value[0][0]
                convolveNum = int(np.ceil(convolveSec * fs))
                chStream = streams['wave'][ch,:]
    
                mean_vec = np.zeros(chStream.shape[0],dtype=np.float32)
                # use 4 cores in parallel async mode
                            
                k = 0

                # index of other channels
                idx = keepChan[keepChan != ch]#range(0,ch)+range(ch+1,16)
                fh.close()

                while k<len(idx):
                    pool = Pool(processes=numProcesses)
                    try:
                        chs = idx[k:min(k+numProcesses,len(idx))]
                        variable = []
                        for i in chs:
                            variable += [(path,i)]
                        mean_vec = mean_vec + np.sum(np.vstack((pool.map(extractor, variable))),axis=0)
                        print chs
                        k += numProcesses
                    finally:
                        pool.terminate()
                # finalize the mean
                mean_vec = mean_vec / idx.shape[0]
                # Remove common noise by referencing to CAR (common averarage reference)
                chRaw = np.array(chStream - mean_vec, dtype=np.float32)
                fCar.create_dataset('ch_%d'%ch, data = chRaw, compression = 'gzip' ,compression_opts=9)
            print 'CAR completed in %f sec'%(clock()-t0)
            fCar.close()
             
            # CAR COMPLETED
        
        t0 = clock()     
        print 'Threshold extracting'
        
        pp = h5py.File(path,'r')
        fs = pp['data']['streams']['fs'].value[0][0]
        pp.close()
        
        th = no_sleep_thresholding(carPath,fs,keepChan,nDet,convolveSec,recName=fname)

        
#        try:
#            w,r,nr,fs = extractWS(path,scored)
#    
#            th_nr = thresholding(carPath,fs,nr,keepChan,nDet,convolveSec,
#                                 saveFig=True,stageType='NRem',recName=fname,fldSave=figFld)
#            th_r = thresholding(carPath,fs,r,keepChan,nDet,convolveSec,
#                                 saveFig=True,stageType='Rem',recName=fname,fldSave=figFld)
#            th_w = thresholding(carPath,fs,w,keepChan,nDet,convolveSec,
#                                 saveFig=True,stageType='Wake',recName=fname,fldSave=figFld)
#             
#            tt = np.vstack((th_w,th_r))
#            tt = np.vstack((tt,th_nr))
#            th = np.nanmax(tt,axis=0)
#            
#            sleep_th = True
#            print 'Threshold computed with sleep steges in %f min'%((clock()-t0)/60)
#        except:
#            th = no_sleep_thresholding(carPath,fs,keepChan,nDet,convolveSec,recName=fname)
#            sleep_th = False
        print 'Threshold computed without sleep steges in %f min'%((clock()-t0)/60)

             
        # cycle only in keepChan
        for ch in keepChan:
            fCar = h5py.File(os.path.join(carPath,fname.replace('raw','car')),'r')
            y = fCar['ch_%d'%ch]
            
            fh = h5py.File(path,'r')
            fs = fh['data']['streams']['fs'].value[0][0]
            fh.close()
            
            # Compute NEO, Kim and Kim 2000 "Neural Spike Sorting Under Nearly 0-dB Signal-to-Noise Ratio Using Nonlinear Energy Operator and Artificial Neural-Network Classifier"
            yNEO = y[1:-1] * y[1:-1] - y[2:]*y[:-2]
            # smooth signal if needed    
            if convolveSec > 0:
                convolveNum = int(np.ceil(convolveSec * fs))
                yNEO = np.convolve(yNEO, np.ones(convolveNum)/convolveNum, mode='same')
            
            # Compute detection threshold
            
            # Extract spike indices
            t0 = clock()
            print 'computing detection'
            aboveTh = np.array(yNEO > th[ch],dtype = np.int8)
           
    

            spkIdx = detection(aboveTh, yNEO, fs,maxDur, refracMs, signal = y)
            print 'detection computed %f second'%(clock()-t0)
            spkIdx = np.array(spkIdx, dtype=int)
            print 'Computing artefact threshold'
            t0 = clock()
            thMax = nArt * np.nanmedian(np.abs(y - np.nanmedian(y))) / 0.6745
            th_M[0,ch] = thMax
            print 'Artefact threshold completed in %f sec'%(clock()-t0)     
            #==============================================================================
            #   ARTEFACT REMOVAL            
            #==============================================================================
                   
            k = 0
            print 'Artefact Removal for channel %d'%ch
            t0 = clock()
            
            spkIdx = spkIdx[spkIdx - pre > 0]
            spkIdx = spkIdx[spkIdx + post < y[1:-1].shape[0]]
            other_idx = np.where(keepChan != ch)[0]
            wf = extractWf(y[1:-1], spkIdx-pre, spkIdx+post, ch, totchan=keepChan)
            corrVect = np.ones((spkIdx.shape[0],1),dtype=np.float32) * -1
            
            carWf = np.zeros((spkIdx.shape[0],post+pre),dtype = np.float32)
                
            for other_ch in other_idx:
                for kk in range(spkIdx.shape[0]):
                    carWf[kk,:] = fCar['ch_%d'%other_ch][spkIdx[kk]-pre:spkIdx[kk]+post]
                newCorr = vectorizedRowCorr(carWf, wf).reshape(corrVect.shape)
                corrVect = np.max(np.c_[corrVect,newCorr],axis=1).reshape(newCorr.shape)
            
            boolean = (corrVect[:,0] < corrTh) * (np.max(wf,axis=1)-np.min(wf,axis=1) < thMax) > 0
            
            print 'Artefact removal completed in %f sec'%(clock()-t0)
            fCar.close()

            spkIdx = spkIdx[boolean]
            wf = wf[boolean,:]
           
            subCh = np.hstack((subCh, np.array([ch]*spkIdx.shape[0],dtype=np.int32)))
            subWf = np.vstack((subWf, np.array(wf,dtype=np.float32)))
            subTs = np.hstack((subTs, np.array(spkIdx / fs,dtype=np.float32)))
            subSpkInd = np.hstack((subSpkInd, np.array(1+spkIdx,dtype=np.int32)))
      

        fh = h5py.File(os.path.join(path_save,os.path.basename(path).split('raw')[0] + 'detected.mat'),'w')
        fh['ts'] = subTs
        fh['waveforms'] = subWf
        fh['chann'] = subCh
        fh['spkIndex'] = subSpkInd
        fh['neo_th'] = th
        fh['art_th'] = th_M
#        if sleep_th:
#            fh['th_w'] = th_w
#            fh['th_r'] = th_r
#            fh['th_nr'] = th_nr

        fh.close()