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

import numpy as np
import matplotlib.pylab as plt


def detection(aboveTh, neo, fs, maxDur = 4, refPeriod = 1, signal = None ):
    """
        Detects as a peak the maximum obtained by neo transform of the\\
        singnal in each interval in which the neo is above threshold.\\
        It discards spikes that are close than refPeriod and that lasts\\
        for more than maxDur
    """

    samples = fs * maxDur *10**-3
    stop = 0
    
    change = np.diff(aboveTh)
        
    start = np.where(change == 1)[0]+1
    stop = np.where(change == -1)[0]+1
    
    if not start.shape[0]:
        return np.array([])
        
    if aboveTh[0]:
        start = np.hstack(([0],start))
        
    if aboveTh[-1]:
        stop = np.hstack((stop,aboveTh.shape[0]))
        
    if start.shape[0] != stop.shape[0]:
        raise IndexError, 'start and stop have different dimension'
    else:
        spikeIdx = np.ones(start.shape[0],dtype=int)*-1
    
    abs_y = np.abs(signal[1:-1])    
    
    for kk in xrange(start.shape[0]):
        if (stop[kk] - start[kk]) > samples:
            continue
        else:
            spikeIdx[kk] = int(np.argmax(abs_y[start[kk]:stop[kk]])+start[kk])
    
    spikeIdx = spikeIdx[spikeIdx >= 0]
    if spikeIdx.shape[0]<=2:
        return spikeIdx
        
    samplesRef = fs * refPeriod * 10**-3


#==============================================================================
#     DELETE SPIKES WITH bilateral WINDOW
#==============================================================================
    boolean = ((spikeIdx[1:-1] - spikeIdx[:-2]) >= samplesRef) * ((spikeIdx[2:] - spikeIdx[1:-1]) >= samplesRef)
    
    filtered = []
    
    if spikeIdx[1] - spikeIdx[0] >= samplesRef:
        filtered += [spikeIdx[0]]
        
    filtered = np.hstack((filtered, spikeIdx[1:-1][boolean]))
    
    if spikeIdx[-1]-spikeIdx[-2] >= samplesRef:
        filtered = np.hstack((filtered, [spikeIdx[-1]]))
    
    return filtered
            
if __name__ == '__main__':
    
    aboveTh = np.array([True]+[True]+[False]*3 + [True]*4 + [False]*6 + [True]*8,dtype = int)
    fs = 10**3
    neo = np.random.rand(aboveTh.shape[0])
    
    idx = detection(aboveTh, neo, fs, refPeriod = 7)
    print(idx)
    