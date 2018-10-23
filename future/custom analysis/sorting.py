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

from scipy.io import loadmat
import numpy as np
#import scipy.signal as signal
import matplotlib.pylab as plt
import os
from check_opt_sorting import *
import h5py
import dill                            #pip install dill --user
import shutil

working_folder = '/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit/detected'
save_folder = os.path.join('/Users/Matte/Scuola/Dottorato/Projects/Pace/Single unit','sorted')

if not os.path.exists(save_folder):
    os.mkdir(save_folder)

wf_key = 'waveforms'
ch_key = 'chann'

for fileName in os.listdir(working_folder):
    if not fileName.endswith('.mat'):
        continue
    
    print 'Data: ',fileName
    # open and extract
    fname = os.path.join(working_folder, fileName)
    
    name_save = fileName.replace('detected','sorted')
    if name_save in os.listdir(save_folder):
        print 'file already sorted'
        continue
    
    
    fh = h5py.File(fname,'r')
    f_sorted = h5py.File(os.path.join(save_folder,name_save),'w')
    
    for kk in fh.keys():
        f_sorted.create_dataset(kk, data = fh[kk])
    
    fh.close()
    f_sorted.close()
    
    
    
    f_sorted = h5py.File(os.path.join(save_folder,name_save),'r+')
    wf = f_sorted[wf_key].value
    channel = f_sorted[ch_key].value
    
    # create new container for labels initialised at -1
    if 'unit' in  f_sorted.keys():
        f_sorted.pop('unit')
    try:
        f_sorted['unit'] = np.ones((1,channel.shape[1]), dtype=int) * np.nan
    except:
        f_sorted['unit'] = np.ones((1,channel.shape[0]), dtype=int) * np.nan

    idx = 0    
    # loop over channels
    for ch in np.unique(channel):  
        print 'channel ',ch
        # filter selected channel
        ch_filter = channel.flatten() == ch
        try:
            wf_ch = wf[ch_filter,:]
#            wf_ch = wf.T[ch_filter,:]
        except:
            wf_ch = wf[ch_filter,:]
        # normalize waveforms
        Nwf = sts.zscore(wf_ch,axis=1)
        
        # optimal K
        K,Lfinal,_ = selectK(Nwf,20,10,15, 250,200,2,10**-4,excludeFun=excludeMaxDistFromCentroids,Klim=4)
        f_sorted['unit'][0,idx:idx+Lfinal.shape[0]] = Lfinal
        idx += Lfinal.shape[0]
        
    f_sorted.close()
