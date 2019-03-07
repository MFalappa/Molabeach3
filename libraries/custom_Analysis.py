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

from Analyzing_GUI import *
from Plotting_GUI import *
from Modify_Dataset_GUI import *
import nexfile

def spikeStatistics(*myInput):
    Datas      = myInput[0]
    Input      = myInput[1]
    DataGroup  = myInput[2]
    TimeStamps = myInput[3]
    lock       = myInput[4]
    bins = int(Input[0]['DoubleSpinBox'][0])
    fr_bin_sec = Input[0]['DoubleSpinBox'][1]
    dictIsi = {}
    dictFR = {}
    outputTableFR = np.zeros(0, dtype={'names':('Subject','Neuron','Time(sec)','Firing Rate'),
                                       'formats':('S100','S30',float,float)})
    log2ISIoutput = np.zeros(0,dtype={'names':('Subject','Neuron','Edge 0','Edge 1','log2(ISI)'),
                                       'formats':('S100','S30',float,float,float)})
    for name in DataGroup:
        
        dictIsi[name] = {}
        dictFR[name] = {}
        try:
            lock.lockForRead()
            data_spk = deepcopy(Datas.takeDataset(name))
        finally:
            lock.unlock()
        num_vars = data_spk['FileHeader']['NumVars']
        ch_list = []
        num_ch = 0
        for ch in range(num_vars):
            if data_spk['Variables'][ch]['Header']['Type'] == 0: # if it is a spike train
                ch_list += [ch]
                num_ch += 1
        rec_dur = data_spk['FileHeader']['End']
        steps = int(rec_dur // fr_bin_sec)
        fr_mat = np.zeros((num_ch,steps))
        histisi_mat = np.zeros((num_ch,bins))
        edgeisi_mat = np.zeros((num_ch,bins+1))
        tmpOutputFR = np.zeros(num_ch*steps,dtype={'names':('Subject','Neuron','Time(sec)','Firing Rate'),
                                                'formats':('S100','S30',float,float)})
        tmpOutputFR['Subject'] = name
        tmplog2ISIoutput = np.zeros(num_ch*bins,dtype={'names':('Subject','Neuron','Edge 0','Edge 1','log2(ISI)'),
                                   'formats':('S100','S30',float,float,float)})
        tmplog2ISIoutput['Subject'] = name
        nameList = []
        ch_idx = 0
        for ch in ch_list:
            nameList += [name + '\n' + data_spk['Variables'][ch]['Header']['Name']]
            spk_ts = data_spk['Variables'][ch]['Timestamps']
            log2isi = np.log2(spk_ts[1:] - spk_ts[:-1])
            histisi, edgeisi = np.histogram(log2isi,bins=bins,normed=True)
            firingRate = np.zeros(steps)
            for k in range(steps):
                bl = (spk_ts >= k * fr_bin_sec) * (spk_ts < (k + 1) * fr_bin_sec)
                firingRate[k] = np.sum(bl) / fr_bin_sec
                k += 1
            fr_mat[ch_idx,:] = firingRate
            histisi_mat[ch_idx,:] = histisi
            edgeisi_mat[ch_idx,:] = edgeisi
            tmpOutputFR['Neuron'][ch_idx*firingRate.shape[0]: (ch_idx+1)*firingRate.shape[0]] = data_spk['Variables'][ch]['Header']['Name']
            tmpOutputFR['Firing Rate'][ch_idx*firingRate.shape[0]: (ch_idx+1)*firingRate.shape[0]] = firingRate
            tmpOutputFR['Time(sec)'][ch_idx*firingRate.shape[0]: (ch_idx+1)*firingRate.shape[0]] = np.arange(steps) * fr_bin_sec
            tmplog2ISIoutput['Neuron'][ch_idx*bins: (ch_idx+1)*bins] = data_spk['Variables'][ch]['Header']['Name']
            tmplog2ISIoutput['Edge 1'][ch_idx*bins: (ch_idx+1)*bins] = edgeisi[:-1]
            tmplog2ISIoutput['Edge 0'][ch_idx*bins: (ch_idx+1)*bins] = edgeisi[1:]
            tmplog2ISIoutput['log2(ISI)'][ch_idx*bins: (ch_idx+1)*bins] = histisi
            ch_idx += 1
        outputTableFR = np.hstack((outputTableFR,tmpOutputFR))
        log2ISIoutput = np.hstack((log2ISIoutput,tmplog2ISIoutput))
        dictIsi[name]['histISI'] = histisi_mat
        dictIsi[name]['edgeISI'] = edgeisi_mat
        dictIsi[name]['nameISI'] = nameList
        dictFR[name]['firingRate'] = fr_mat
        dictFR[name]['time(Sec)'] = np.arange(steps) * fr_bin_sec
        dictFR[name]['nameFR'] = nameList
    DataDict = {}
    DataDict['Spike Statistics'] = {}
    DataDict['Spike Statistics']['Firing Rate'] =  outputTableFR
    DataDict['Spike Statistics']['log2(ISI)'] = log2ISIoutput
    dictPlot = {}
    dictPlot['Fig:Spike Statistics'] = {}
    dictPlot['Fig:Spike Statistics']['Firing Rate'] = dictFR
    dictPlot['Fig:Spike Statistics']['ISI'] = dictIsi
    info = {}
    info['Firing Rate'] = {}
    info['Firing Rate']['Types']  = ['Binned Firing Rate']
    info['log2(ISI)'] = {}
    info['log2(ISI)']['Types']  = ['log2(ISI)']
    return DataDict,dictPlot,info
