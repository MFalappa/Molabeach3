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
WE WILL INTRODUCE IN THE NEXT RELEASE OF PHENOPY AFTER A HARD DEBUF AND 
GENERALIZATION

*******************************************************************************
SPIKE MATRIX MUST BE ALLIGNED SUCH THAT THE TIMESTAMP 0 IS RELATIVE TO 
THE FIRST TIME OF THE SLEEP SCORING
*******************************************************************************
"""

import numpy as np
import os,sys
sys.path.append('/Users/Matte/Python_script/Phenopy/libraries')
from sleep_analysis import *
from scipy.io import loadmat
from Modify_Dataset_GUI import *
from Analyzing_GUI import *
from copy import copy
import scipy.stats as sts
from scipy.signal import savgol_filter
from statsmodels.sandbox.stats.multicomp import multipletests
import h5py
plt.close('all')


epoch_dur = 4
pre_dur = 20
after_dur = 20
sec_hist = 1

def reformat_data(single_unit,spkKey,unitKey,chKey,noiseCode):
    chann = single_unit[chKey].value.flatten()
    unit = single_unit[unitKey].value.flatten()
    
    spike = single_unit[spkKey].value.flatten()
    uniqueCh = np.unique(chann)
    unitIndex = np.zeros((2,0),dtype=int)
    maxTS = 0
    dictCU = {}
    for ch in uniqueCh:
        idx_ch = chann == ch
        unch = unit[idx_ch]
        spikeCh = spike[idx_ch]
        uniqueUn = np.unique(unch)
        numNoise = 0
        for un in uniqueUn:
            if un in noiseCode:
                numNoise += 1
        tmpUI = np.zeros((2,uniqueUn.shape[0]-numNoise))
        k = 0
        for un in uniqueUn:
            if un in noiseCode:
                continue
            tmpUI[:,k] = [ch,un]
            dictCU['%d_%d'%(ch,un)] = spikeCh[unch==un]
            maxTS = max(maxTS,len(dictCU['%d_%d'%(ch,un)]))
            k+=1
        unitIndex = np.hstack((unitIndex,tmpUI))
    spike_time = np.zeros((maxTS,unitIndex.shape[1]))*np.nan
    k = 0
    for ch,un in unitIndex.T:
        spike_time[:dictCU['%d_%d'%(ch,un)].shape[0],k] = dictCU['%d_%d'%(ch,un)] 
        k+=1
    return spike_time,unitIndex
    
class transition_psth(object):
    def __init__(self,matrix,edge,type_trans):
        self.dict = {}
        self.dict.__setitem__('hist',matrix)
        self.dict.__setitem__('edge',edge)
        self.dict.__setitem__('transition',type_trans)
    
    def psth_trans(self,trans):
        return self.dict.__getitem__('hist')[self.dict['transition'] == trans,:,:] / (self.dict['edge'][1] - self.dict['edge'][0])
        
    def psth_trans_ch(self,trans,ch):
        return self.dict.__getitem__('hist')[self.dict['transition'] == trans,:,ch] / (self.dict['edge'][1] - self.dict['edge'][0])
    
    def __getitem__(self,key):
        return self.dict[key]
    
    def keys(self):
        return self.dict.keys()
    
    
    def shape(self):
        return self.dict['hist'].shape
    
    def plotMeanHist(self,trans,ch):
        psth = self.psth_trans_ch(trans,ch)
        mean_psth = np.nanmean(psth,axis=0)
        fig = plt.figure()
        dedge = self.dict['edge'][1] - self.dict['edge'][0]
        plt.bar(self.dict['edge'][:-1],mean_psth,width=dedge)
        plt.title('psth %s'%trans,fontsize=20)
        plt.xlabel('Time(sec)')
        plt.ylabel('spike/sec')
        return fig

def compute_all_epi(sleep_data,merge_if=1):
    for epoch in ['W*','R*','NR*']:
        sleep_data.Stage[sleep_data.Stage == epoch] = epoch[:-1]
    epi_nr = extract_epi(sleep_data,epoch='NR',merge_if=0,min_epi_len=1)
    epi_r = extract_epi(sleep_data,epoch='R',merge_if=0,min_epi_len=1)
    epi_w = extract_epi(sleep_data,epoch='W',merge_if=0,min_epi_len=1)
    
    epi_all = np.zeros(epi_nr.shape[0]+epi_r.shape[0]+epi_w.shape[0],
                       dtype = {'names':('Start','End','Stage'),'formats':(int,int,'S2')})
    
    n_nr = epi_nr.shape[0]
    n_r = epi_r.shape[0]
    n_w = epi_w.shape[0]
    epi_all[:n_nr]['Start'] = epi_nr['Start']
    epi_all[:n_nr]['End'] = epi_nr['End']
    epi_all[:n_nr]['Stage'] = 'NR'
    epi_all[n_nr:n_nr+n_r]['Start'] = epi_r['Start']
    epi_all[n_nr:n_nr+n_r]['End'] = epi_r['End']
    epi_all[n_nr:n_nr+n_r]['Stage'] = 'R'
    epi_all[-n_w:]['Start'] = epi_w['Start']
    epi_all[-n_w:]['End'] = epi_w['End']
    epi_all[-n_w:]['Stage'] = 'W'
    
    epi_all.sort(order = 'Start')
    epi_all.sort(order = 'End')
    
    epi_all =  merge_epi(copy(epi_all),merge_if=merge_if)
    epi_all['Start'] = epi_all['Start'] * epoch_dur
    epi_all['End'] = epi_all['End'] * epoch_dur     
    return epi_all
    
def psth_transtion(spike_time, sleep_data, pre_dur, after_dur, sec_hist,
                   epoch_dur):
        
    for epoch in ['W*','R*','NR*']:
        sleep_data.Stage[sleep_data.Stage == epoch] = epoch[:-1]
    epi_all = compute_all_epi(sleep_data,merge_if = 1)
    sum_dur = after_dur+pre_dur
    if (sum_dur) % sec_hist:
        sum_dur = (sum_dur) - (sum_dur) % sec_hist + sec_hist
    
    matrix_psth = np.zeros((epi_all.shape[0]-2,(sum_dur)//sec_hist,spike_time.shape[1])) * np.nan
    trans_type_v = np.zeros(epi_all.shape[0]-2,dtype='S8')
    for k in xrange(1,epi_all.shape[0]-1):
        trans_type = epi_all['Stage'][k-1] + '-' + epi_all['Stage'][k]
        trans_type_v[k-1] = trans_type
        dur_bef = epi_all['End'][k-1] - epi_all['Start'][k-1]
        dur_aft = epi_all['End'][k] - epi_all['Start'][k]
        t0 = epi_all['End'][k-1]
        if dur_aft < after_dur or dur_bef < pre_dur:
            print 'Skip k',k-1
            continue
        for ch in xrange(29):
            spike_ch = spike_time[:,ch]    
            spike_ch = spike_ch[spike_ch > t0 - pre_dur]
            tmp_spike = spike_ch[spike_ch <= t0 + after_dur] - t0
            if not tmp_spike.shape[0]:
                continue
            hist, edge = np.histogram(tmp_spike,range=(-pre_dur,after_dur), bins=(sum_dur)//sec_hist)
            
            matrix_psth[k-1,:,ch] = hist 
    psth = transition_psth(matrix_psth,edge,trans_type_v)
    return psth,epi_all

class subject_handling(object):
    def __init__(self):
        self.subject_dict = {}
        self.recording_dict = {}
        self.subject_recording = {}
    
    def load_subject(self,path_sleep,path_spike,genotype,subject,rec_label,spikeKey ='timeStamps',unitKey='unitIndex',chKey=None,noiseCode=[-1]):
        delim = DetectDelimiter_GUI(path_sleep)
        num_header = 0
        fh = open(path_sleep,'U')
        flagBreak = False
        line = fh.readline()
        while line:
            print line
            for head in ['EpochNo',	'Stage','Time',	'0.000000Hz']:
                if head in line:
                    flagBreak = True
                    break
            if flagBreak:
                break
            line = fh.readline()
            num_header += 1
        fh.close()
        num_header += 1
        sleep_data = EEG_Data_Struct(freqLim_Hz = 20.5,PathToFile=path_sleep,
                                     delimiter=delim, header=num_header)
        single_unit = h5py.File(path_spike, 'r')
#        single_unit = loadmat(path_spike)
        if 'cut' in single_unit.keys():
            sleep_data.Stage[single_unit['cut'].value.flatten()] = 'M'
#        print single_unit.keys()
        if chKey is None:
            spike_time = single_unit[spikeKey].value.T
            unit_and_ch = single_unit[unitKey].value.T
        else:
            spike_time, unit_and_ch = reformat_data(single_unit,spikeKey, unitKey,chKey,noiseCode)

        if subject in self.recording_dict.keys():
            
            self.recording_dict[subject][rec_label] = recording_characterization(spike_time,sleep_data,unit_and_ch,rec_label)
        else:
            self.recording_dict[subject] = {}
            self.recording_dict[subject][rec_label] = recording_characterization(spike_time,sleep_data,unit_and_ch,rec_label)
        self.subject_dict[subject] = genotype
        if subject in self.subject_recording.keys():
            if rec_label in self.subject_recording[subject]: 
                self.subject_recording[subject].remove(rec_label)
            self.subject_recording[subject].append(rec_label)
        else:
            self.subject_recording[subject] = [rec_label]
        
    def return_tuple_types(self,table):
        fmt = []
        for name in table.dtype.names:
            fmt += [table.dtype.fields[name][0]]
        return tuple(fmt)
    
    def add_field_to_table(self,table,fieldName,fieldValue,side='left',rec_type='S100'):
        types = self.return_tuple_types(table)
        names = table.dtype.names
#        rec_type = 'S100'
        if side == 'left':
            new_table = np.zeros(table.shape[0],dtype={'names':(fieldName,)+names,'formats':(rec_type,)+types})
        else:
            new_table = np.zeros(table.shape[0],dtype={'names':names+(fieldName,),'formats':types+(rec_type,)})
        for name in names:
            new_table[name] = table[name]
        new_table[fieldName] = fieldValue
        return new_table
    
    def firing_rate_x_stage_per_subject(self,subject):
        rec_dict = self.recording_dict[subject]
        first_phase = True
        for phase in self.subject_recording[subject]:
            rec = rec_dict[phase]
            if first_phase:
                table = rec.all_unit_firing_rate_x_stage()
                first_phase = False
            else:
                table = np.hstack((table,rec.all_unit_firing_rate_x_stage()))
        return table
    
    
    def isi_x_stage_per_subject(self,subject):
        rec_dict = self.recording_dict[subject]
        first_phase = True
        for phase in self.subject_recording[subject]:
            rec = rec_dict[phase]
            if first_phase:
                table = rec.all_unit_isi_x_stage()
                first_phase = False
            else:
                table = np.hstack((table,rec.all_unit_isi_x_stage()))
        return table
    
    def firing_rate_x_stage(self,sub_list):
        first = True
        for sub in sub_list:
            for phase in self.subject_recording[sub]:
                rec = self.recording_dict[sub][phase]
                if first:
                    first = False
                    table = rec.all_unit_firing_rate_x_stage()
                    new_table = self.add_field_to_table(table,'Subject',sub)
                    new_table = self.add_field_to_table(new_table,'Genotype',self.subject_dict[sub])
                else:
                    table = rec.all_unit_firing_rate_x_stage()
                    table = self.add_field_to_table(table,'Subject',sub)
                    table = self.add_field_to_table(table,'Genotype',self.subject_dict[sub])
                    new_table = np.hstack((new_table,table))
                    
        return new_table
    
    def isi_x_stage(self,sub_list):
        first = True
        for sub in sub_list:
            for phase in self.subject_recording[sub]:
                rec = self.recording_dict[sub][phase]
                if first:
                    first = False
                    table = rec.all_unit_isi_x_stage()
                    new_table = self.add_field_to_table(table,'Subject',sub)
                    new_table = self.add_field_to_table(new_table,'Genotype',self.subject_dict[sub])
                else:
                    table = rec.all_unit_isi_x_stage()
                    table = self.add_field_to_table(table,'Subject',sub)
                    new_table = np.hstack((new_table,self.add_field_to_table(table,'Genotype',self.subject_dict[sub])))
        return new_table
    
    def cmp_class_firing_rate(self,sub_list):
        table = self.firing_rate_x_stage(sub_list)
        dict_class = {21:'NR > R > W',15:'R > NR > W',19:'NR > W > R',
                      11:'R > W > NR',7:'W > NR > R',5:'W > R > NR'}
        classe = []
        for row in xrange(table.shape[0]):
            w = table[row]['Wake(spike/sec)']
            r = table[row]['REM(spike/sec)']
            nr = table[row]['NREM(spike/sec)']
            cl = np.sum( np.argsort([w,r,nr]) * np.array([1,3,9]))
            classe += [dict_class[cl]]
        new_table = self.add_field_to_table(table,'Class',classe)
        return new_table
    
    def pop(self,subject,rec,ch,unit):
        return self.recording_dict[subject][rec].pop(ch,unit)
    
    def save(self,path):
        np.save(path,self)
        
    def plot_rate_x_subject(self,subject,recording):
        rec = self.recording_dict[subject][recording]
        table = rec.all_unit_firing_rate_x_stage()
        matrix = np.zeros((table.shape[0],3))
        matrix[:,0] = table['Wake(spike/sec)']
        matrix[:,1] = table['NREM(spike/sec)']
        matrix[:,2] = table['REM(spike/sec)']
        x_axis = np.ones((table.shape[0],3))
        x_axis = np.dot(x_axis,np.diag([1,2,3]))
        fig = plt.figure()
        plt.plot(x_axis.T,matrix.T,color='b')
        plt.xticks([1,2,3],['W','NREM','REM'])
        plt.title('Firing Rate - %s phase: %s'%(subject,recording))
        plt.ylabel('Spike/sec')
        plt.xlim(0.5,3.5)
        return fig
    
    def plot_isi_x_subject(self,subject,recording,new_fig=True):
        rec = self.recording_dict[subject][recording]
        table = rec.all_unit_isi_x_stage()
        matrix = np.zeros((table.shape[0],3))
        matrix[:,0] = table['Wake(sec)']
        matrix[:,1] = table['NREM(sec)']
        matrix[:,2] = table['REM(sec)']
        x_axis = np.ones((table.shape[0],3))
        x_axis = np.dot(x_axis,np.diag([1,2,3]))
        if new_fig:
            fig = plt.figure()
        else:
            fn = plt.get_fignums()
            if len(fn):
                fig = plt.figure(fn[-1])
            else:
                fig = plt.figure()
        plt.plot(x_axis.T,matrix.T,color='b')
        plt.xticks([1,2,3],['W','NREM','REM'])
        plt.title('Firing Rate - %s phase: %s'%(subject,recording))
        plt.ylabel('sec')
        plt.xlim(0.5,3.5)
        return fig
    
    def plot_rate_x_subject_over_list(self,subject,rec_list,new_fig=True):
        k = 1
        tk = []
        tk_lab = []
        for recording in rec_list:
            rec = self.recording_dict[subject][recording]
            table = rec.all_unit_firing_rate_x_stage()
            matrix = np.zeros((table.shape[0],3))
            matrix[:,0] = table['Wake(spike/sec)']
            matrix[:,1] = table['NREM(spike/sec)']
            matrix[:,2] = table['REM(spike/sec)']
            x_axis = np.ones((table.shape[0],3))
            x_axis = np.dot(x_axis,np.diag([k,1+k,2+k]))
            if k == 1:
                fig = plt.figure()
            plt.plot(x_axis.T,matrix.T,color='b')
            tk += [k,1+k,2+k]
            tk_lab += ['W','NREM\n%s'%recording,'REM']
            k += 3
            
        plt.xticks(tk,tk_lab)
        plt.title('Firing Rate - %s'%(subject))
        plt.ylabel('Spike/sec')
        plt.xlim(0.5, x_axis[0,2]+0.5)
        return fig
    
    def plot_isi_x_subject_over_list(self,subject,rec_list,new_fig=True):
        k = 1
        tk = []
        tk_lab = []
        for recording in rec_list:
            rec = self.recording_dict[subject][recording]
            table = rec.all_unit_isi_x_stage()
            matrix = np.zeros((table.shape[0],3))
            matrix[:,0] = table['Wake(sec)']
            matrix[:,1] = table['NREM(sec)']
            matrix[:,2] = table['REM(sec)']
            x_axis = np.ones((table.shape[0],3))
            x_axis = np.dot(x_axis,np.diag([k,1+k,2+k]))
            plt.plot(x_axis.T,matrix.T,color='b')
            if k == 1:
                fig = plt.figure()
            tk += [k,1+k,2+k]
            tk_lab += ['W','NREM\n%s'%recording,'REM']
            k += 3
        plt.xticks(tk,tk_lab)
        plt.title('Firing Rate - %s'%(subject))
        plt.ylabel('sec')
        plt.xlim(0.5, x_axis[0,2]+0.5)
        return fig
    
    def plot_rate_per_class_over_list(self,fr_type,sub_list):
        
        for subject in sub_list:
            table = self.cmp_class_firing_rate([subject])
            table = table[table['Class'] == fr_type]
            rec_list = self.subject_recording[subject]
            k = 1
            tk = []
            tk_lab = []
            for recording in rec_list:
                rec_table = table[table['Recording']==recording]
                matrix = np.zeros((rec_table.shape[0],3))
                matrix[:,0] = rec_table['Wake(spike/sec)']
                matrix[:,1] = rec_table['NREM(spike/sec)']
                matrix[:,2] = rec_table['REM(spike/sec)']
                x_axis = np.ones((rec_table.shape[0],3))
                x_axis = np.dot(x_axis,np.diag([k,1+k,2+k]))
                if k==1:
                    plt.figure(figsize=[ 10.,  5.95])
                plt.plot(x_axis.T,matrix.T,color='b')
                tk += [k,1+k,2+k]
                tk_lab += ['W','NREM\n%s N=%d'%(recording,rec_table.shape[0]),'REM']
                k += 3
            
            plt.xticks(tk,tk_lab)
            plt.title('Firing Rate - %s\nN cell = %d\tClass type %s'%(subject,table.shape[0],fr_type))
            plt.ylabel('Spike/sec')
#            plt.xlim(0.5, x_axis[0,2]+0.5)
        return
    
    def stat_per_stage(self,sub_list, method='bonferroni',threshold=0.01):
        table = self.cmp_class_firing_rate(sub_list)
        anova = []
        anova_sg = []
        post_wr = []
        post_wr_sg = []
        post_wnr = []
        post_wnr_sg = []
        post_nrr = []
        post_nrr_sg = []
        tot_ep_w = []
        tot_ep_r = []
        tot_ep_nr = []
        
        for row in xrange(table.shape[0]):
            sub = table[row]['Subject']
            rec_label = table[row]['Recording']
            rec = self.recording_dict[sub][rec_label]
            ch,unit = table[row]['Channel'],table[row]['Unit']
            fr_x_epoch = rec.get_firning_rate_x_epoch_dict(ch,unit)
            tot_ep_w += [fr_x_epoch['W'].shape[0]]
            tot_ep_nr += [fr_x_epoch['NR'].shape[0]]
            tot_ep_r += [fr_x_epoch['R'].shape[0]]
            if fr_x_epoch['W'].shape[0] * fr_x_epoch['R'].shape[0] * fr_x_epoch['NR'].shape[0]:
                
                f,p_gl = sts.f_oneway(fr_x_epoch['W'],fr_x_epoch['R'],fr_x_epoch['NR'])
                t,pwr = sts.ttest_ind(fr_x_epoch['W'],fr_x_epoch['R'])
                t,pwnr = sts.ttest_ind(fr_x_epoch['W'],fr_x_epoch['NR'])
                t,pnrr = sts.ttest_ind(fr_x_epoch['NR'],fr_x_epoch['R'])
                rej,padj,alphaS,alphaB = multipletests([pwr,pwnr,pnrr],method=method)
                anova += [p_gl]
                anova_sg += [p_gl<threshold]
                post_wr += [padj[0]]
                post_wnr += [padj[1]]
                post_nrr += [padj[2]]
                
                post_wr_sg += [padj[0]<threshold]
                post_wnr_sg += [padj[1]<threshold]
                post_nrr_sg += [padj[2]<threshold]
            
            elif fr_x_epoch['W'].shape[0] * fr_x_epoch['R'].shape[0]:
                f,p_gl = sts.ttest_ind(fr_x_epoch['W'],fr_x_epoch['R'])
                anova += [p_gl]
                anova_sg += [p_gl<threshold]
                post_wr += [p_gl]
                post_wr_sg += [p_gl<threshold]
                post_wnr += [np.nan]
                post_nrr += [np.nan]
                post_wnr_sg += [False]
                post_nrr_sg += [False]
            
            elif fr_x_epoch['W'].shape[0] * fr_x_epoch['NR'].shape[0]:
                f,p_gl = sts.ttest_ind(fr_x_epoch['W'],fr_x_epoch['NR'])
                anova += [p_gl]
                anova_sg += [p_gl<threshold]
                post_wnr += [p_gl]
                post_wnr_sg += [p_gl<threshold]
                post_wr += [np.nan]
                post_nrr += [np.nan]
                post_wr_sg += [False]
                post_nrr_sg += [False]
            
            elif fr_x_epoch['R'].shape[0] * fr_x_epoch['NR'].shape[0]:
                f,p_gl = sts.ttest_ind(fr_x_epoch['R'],fr_x_epoch['NR'])
                anova += [p_gl]
                anova_sg += [p_gl<threshold]
                post_nrr += [p_gl]
                post_nrr_sg += [p_gl<threshold]
                post_wr += [np.nan]
                post_wnr += [np.nan]
                post_wr_sg += [False]
                post_wnr_sg += [False]
            else:
                anova += [np.nan]
                anova_sg += [False]
                post_nrr += [np.nan]
                post_nrr_sg += [False]
                post_wr += [np.nan]
                post_wnr += [np.nan]
                post_wr_sg += [False]
                post_wnr_sg += [False]
        table = self.add_field_to_table(table,'Num Wake Epoch',tot_ep_w,side='right')
        table = self.add_field_to_table(table,'Num REM Epoch',tot_ep_r,side='right')
        table = self.add_field_to_table(table,'Num NREM Epoch',tot_ep_nr,side='right')
        table = self.add_field_to_table(table,'Anova',anova,side='right')
        table = self.add_field_to_table(table,'Anova Sign',anova_sg,side='right')
        table = self.add_field_to_table(table,'Post-hoc W-R (%s)'%method,post_wr,side='right')
        table = self.add_field_to_table(table,'Post-hoc W-R Sign',post_wr_sg,side='right')
        table = self.add_field_to_table(table,'Post-hoc W-NR (%s)'%method,post_wnr,side='right')
        table = self.add_field_to_table(table,'Post-hoc W-NR Sign',post_wnr_sg,side='right')
        table = self.add_field_to_table(table,'Post-hoc NR-R (%s)'%method,post_nrr,side='right')
        table = self.add_field_to_table(table,'Post-hoc NR-R Sign',post_nrr_sg,side='right')
        return table
        
        
class recording_characterization(object):
    def __init__(self,spike,sleep_data,unit_and_ch,rec_label,perc_x_polyfit=0.1,epoch_dur_sec = 4):
        self.all_episodes = compute_all_epi(sleep_data,merge_if=0)
        self.dict_unit = {}
        n = 0
        for ch,unit in unit_and_ch.T:
#            print 'Loading ch %s, unit %s...'%(ch,unit)
            noNan = spike[True-np.isnan(spike[:,n]),n]
            self.dict_unit['%d-%d'%(ch,unit)] = channel_characterization_sleep_SU(ch,unit,sleep_data,noNan,self.all_episodes,perc_x_polyfit=perc_x_polyfit,epoch_dur_sec=epoch_dur_sec)
            n += 1
        self.unit_and_ch = unit_and_ch
        self.perc_x_polyfit = perc_x_polyfit
        self.rec_label = rec_label
        
    
    def __getitem__(self,chun):
        if type(chun) != tuple:
            raise TypeError, '__getitem__ method needsa a tuple with two elements'
        if len(chun) != 2:
            raise TypeError, '__getitem__ method needsa a tuple with two elements'
        return self.dict_unit['%d-%d'%chun]
    
    def __iter__(self):
        for ch,unit in self.unit_and_ch.T:
            yield ch,unit,self.dict_unit['%d-%d'%(ch,unit)]
        
    def keys(self):
        return self.dict_unit.keys()
    
    def pop(self,ch,unit):
        if ch == 6 and unit == 2:
            pass
        idx = np.prod(self.unit_and_ch == [[ch],[unit]],axis=0)
        if np.sum(idx) < 1:
            raise IndexError, 'No channel %d, unit %d recorded!'%(ch,unit)
        elif np.sum(idx) > 1:
            raise IndexError, 'More than one %d, unit %d recorded!'%(ch,unit)
        idx = True - np.array(idx,dtype=bool)
        self.unit_and_ch[:, True - idx]
        return self.dict_unit.pop('%d-%d'%(ch,unit))
    
    def get_isi_x_stage(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.isi_x_stage
    
    def get_num_spike_x_stage(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.num_spike_x_stage
    
    def get_isi_dict(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.isi_dict
    
    def get_fit_logIsiH(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.fit_logIsiH
    
    def get_firing_rate_x_stage(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.firing_rate_x_stage
    
    def get_firing_rate_x_epoch(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.rate_x_epoch
    
    def get_firning_rate_x_epoch_dict(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.rate_x_epoch_dict
    
    def get_isi_x_epoch(self,ch,unit):
        channel_decr = self.dict_unit['%d-%d'%(ch,unit)]
        return channel_decr.isi_x_epoch
    
    def all_unit_firing_rate_x_stage(self):
        keys = self.dict_unit.keys()
        mat_rate = np.zeros(len(keys),dtype={'names':('Recording','Channel','Unit','Wake(spike/sec)','REM(spike/sec)','NREM(spike/sec)','All(spike/sec)'),
                                             'formats':('S100',int,int,float,float,float,float)})
        mat_rate['Recording'] = self.rec_label
        row = 0
        
        ttttt = 0
        for key in keys:
            ch = int(key.split('-')[0])        
            unit = int(key.split('-')[1])
            fr = self.get_firing_rate_x_stage(ch,unit)
            mat_rate[row]['Channel'] = ch
            mat_rate[row]['Unit'] = unit
            mat_rate[row]['Wake(spike/sec)'] = fr['firing rate'][fr['Stage']=='W']
            mat_rate[row]['REM(spike/sec)'] = fr['firing rate'][fr['Stage']=='R']
            mat_rate[row]['NREM(spike/sec)'] = fr['firing rate'][fr['Stage']=='NR']
            mat_rate[row]['All(spike/sec)'] = fr['firing rate'][fr['Stage']=='All']
            row += 1
        return mat_rate
    
    def all_unit_isi_x_stage(self,mean_median = 'mean'):
        keys = self.dict_unit.keys()
        mat_isi = np.zeros(len(keys),dtype={'names':('Recording','Channel','Unit','Wake(sec)','REM(sec)','NREM(sec)','All(sec)'),
                                             'formats':('S100',int,int,float,float,float,float)})
        mat_isi['Recording'] = self.rec_label
        row = 0
        for key in keys:
            ch = int(key.split('-')[0])
            unit = int(key.split('-')[1])
            isi = self.get_isi_x_stage(ch,unit)
            mat_isi[row]['Channel'] = ch
            mat_isi[row]['Unit'] = unit
            mat_isi[row]['Wake(sec)'] = isi['%s isi'%mean_median][isi['Stage']=='W']
            mat_isi[row]['REM(sec)'] = isi['%s isi'%mean_median][isi['Stage']=='R']
            mat_isi[row]['NREM(sec)'] = isi['%s isi'%mean_median][isi['Stage']=='NR']
            mat_isi[row]['All(sec)'] = isi['%s isi'%mean_median][isi['Stage']=='All']
            row += 1
        return mat_isi
        
    def all_unit_numSpike_x_stage(self):
        keys = self.dict_unit.keys()
        mat_num_spike = np.zeros(len(keys),dtype={'names':('Recording','Channel','Unit','Wake Num Spike','REM Num Spike','NREM Num Spike','All Num Spike','Wake Duration','REM Duration','NREM Duration','All Duration'),
                                             'formats':('S100',int,int,float,float,float,float)+(float,)*4})
        mat_num_spike['Recording'] = self.rec_label
        row = 0
        for key in keys:
            ch = int(key.split('-')[0])
            unit = int(key.split('-')[1])
            ns = self.get_num_spike_x_stage(ch,unit)
            mat_num_spike[row]['Channel'] = ch
            mat_num_spike[row]['Unit'] = unit
            mat_num_spike[row]['Wake Num Spike'] = ns['Num spike'][ns['Stage']=='W']
            mat_num_spike[row]['REM Num Spike'] = ns['Num spike'][ns['Stage']=='R']
            mat_num_spike[row]['NREM Num Spike'] = ns['Num spike'][ns['Stage']=='NR']
            mat_num_spike[row]['All Num Spike'] = ns['Num spike'][ns['Stage']=='All']
            mat_num_spike[row]['Wake Duration'] = ns['Duration'][ns['Stage']=='W']
            mat_num_spike[row]['REM Duration'] = ns['Duration'][ns['Stage']=='R']
            mat_num_spike[row]['NREM Duration'] = ns['Duration'][ns['Stage']=='NR']
            mat_num_spike[row]['All Duration'] = ns['Duration'][ns['Stage']=='All']
            row += 1
        return mat_num_spike
    
    def save(self,path):
        np.save(path,self)
            

class channel_characterization_sleep_SU(object):
    def __init__(self,channel,unit,sleep_data,spike,all_episodes,perc_x_polyfit=0.1,epoch_dur_sec = 4):
        super(channel_characterization_sleep_SU,self).__init__()
        self.all_episodes = all_episodes
        self.sleep_data = sleep_data
        self.sleep_stage = sleep_data.Stage
        self.epoch_dur = epoch_dur_sec
        self.spike = spike
        self.channel = channel
        self.unit = unit
        self.perc_x_polyfit = perc_x_polyfit
        self.update()
        
    def update(self):
        self.sleep_stage_NoStar = self._remove_star()
        self.rate_x_epoch,self.rate_x_epoch_dict = self._compute_firing_rate_x_epoch()
        self.isi_x_epoch = self._compute_isi_x_epoch()
        self.firing_rate_x_stage = self._compute_firing_rate_x_stage()
        self.isi_x_stage, self.isi_dict = self._compute_isi_x_stage()
        self.fit_logIsiH = self._compute_loghist_and_local_polyfit()
        self.num_spike_x_stage = self._compute_num_spike_x_stage()
    
    def _remove_star(self):
        stage_NoStar = self.sleep_stage
        for star in ['W*','NR*','R*']:
            stage_NoStar[self.sleep_stage == star] = star[:-1]
        return stage_NoStar
        
    def _compute_firing_rate_x_epoch(self):
        rate_x_epoch = np.zeros(self.sleep_stage.shape[0])
        rate_x_epoch_dict = {'W':np.array([]),'R':np.array([]),'NR':np.array([])}
        for k in xrange(self.sleep_stage.shape[0]):
            tot_spike = np.sum((self.spike >= k*self.epoch_dur) * (self.spike < (k+1)*self.epoch_dur),dtype=float)
            rate_x_epoch[k] = tot_spike / self.epoch_dur
            if not self.sleep_stage_NoStar[k] in ['M','Non']:
                rate_x_epoch_dict[self.sleep_stage_NoStar[k]] = np.hstack((rate_x_epoch_dict[self.sleep_stage_NoStar[k]],[rate_x_epoch[k]]))
        return rate_x_epoch,rate_x_epoch_dict
           
    def _compute_isi_x_epoch(self):
        isi_x_epoch = np.zeros(self.sleep_stage.shape[0])
        for k in xrange(self.sleep_stage.shape[0]):
            index = (self.spike >= k*self.epoch_dur) * (self.spike < (k+1)*self.epoch_dur)
            isi_x_epoch[k] = np.nanmean(np.diff(self.spike[index]))
        return isi_x_epoch
    
    def _compute_firing_rate_x_stage(self):
        spike = {'W':0,'R':0,'NR':0}
        duration = {'W':0.,'R':0.,'NR':0.}
        firing_rate = np.zeros(4,dtype={'names':('firing rate','Stage'),'formats':(float,'S3')})
        for k in xrange(self.all_episodes.shape[0]):
            start = self.all_episodes['Start'][k]
            end = self.all_episodes['End'][k]
            tmp_duration = (end-start)
            tmp_spike = np.sum((self.spike >= start) * (self.spike < end),dtype=float)
            spike[self.all_episodes['Stage'][k]] += tmp_spike
            duration[self.all_episodes['Stage'][k]] += tmp_duration
        stage = ['W','NR','R']
        for k in xrange(3):
            if duration[stage[k]] > 0:
                firing_rate[k]['firing rate'] = spike[stage[k]] / duration[stage[k]]
            else:
                firing_rate[k]['firing rate'] = np.nan
            firing_rate[k]['Stage'] = stage[k]
        firing_rate[3]['Stage'] = 'All'
        if self.spike.shape[0]:
            firing_rate[3]['firing rate'] = (spike['W']+spike['R']+spike['NR'])/np.max(self.spike)
        else:
            firing_rate[3]['firing rate'] = np.nan
        return firing_rate
    
    def _compute_num_spike_x_stage(self):
        spike = {'W':0,'R':0,'NR':0}
        duration = {'W':0.,'R':0.,'NR':0.}
        num_spike = np.zeros(4,dtype={'names':('Num spike','Duration','Stage'),'formats':(int,float,'S3')})
        for k in xrange(self.all_episodes.shape[0]):
            start = self.all_episodes['Start'][k]
            end = self.all_episodes['End'][k]
            tmp_duration = (end-start)
            tmp_spike = np.sum((self.spike >= start) * (self.spike < end),dtype=float)
            spike[self.all_episodes['Stage'][k]] += tmp_spike
            duration[self.all_episodes['Stage'][k]] += tmp_duration
        stage = ['W','NR','R']
        for k in xrange(3):
            num_spike[k]['Num spike'] = spike[stage[k]] 
            num_spike[k]['Duration'] = duration[stage[k]]
            num_spike[k]['Stage'] = stage[k]
        num_spike[3]['Stage'] = 'All'
        num_spike[3]['Num spike'] = (spike['W']+spike['R']+spike['NR'])
        num_spike[3]['Duration'] = (duration['W']+duration['R']+duration['NR'])
        return num_spike
    
    def _compute_isi_x_stage(self):
        isi = {'W':[],'R':[],'NR':[]}   
        isi_mat = np.zeros(4,dtype={'names':('mean isi','std isi','median isi','25 perc','75 perc','Stage'),'formats':(float,)*5+('S3',)})
#        test = 0 
        for k in xrange(self.all_episodes.shape[0]):
            start = self.all_episodes['Start'][k]
            end = self.all_episodes['End'][k]
            index = (self.spike >= start) * (self.spike < end)
            isi[self.all_episodes['Stage'][k]] = np.hstack((isi[self.all_episodes['Stage'][k]] ,np.diff(self.spike[index])))
#            test += np.sum(index)
#        if test != len(self.spike):
#            print test,len(self.spike),self.all_episodes
#            raise ValueError,'NOT ALL SPIKES CONSIDERED'
        isi['All'] = np.diff(self.spike)
        stage = ['W','NR','R','All']
        for k in xrange(4):
            isi_mat['mean isi'][k] = np.nanmean(isi[stage[k]])
            isi_mat['median isi'][k] = np.nanmedian(isi[stage[k]])
            isi_mat['std isi'][k] = np.nanstd(isi[stage[k]])
            mask = True - np.isnan(isi[stage[k]])
            try:
                isi_mat['25 perc'][k] = np.nanpercentile(isi[stage[k]][mask],25)
                isi_mat['75 perc'][k] = np.nanpercentile(isi[stage[k]][mask],75)
            except:
                isi_mat['25 perc'][k] = np.nan
                isi_mat['75 perc'][k] = np.nan
            isi_mat['Stage'][k] = stage[k]
        return isi_mat, isi
        
    def _compute_loghist_and_local_polyfit(self):
        hd = self.compute_logIsi_histogram()
        dict_logHist = {}
        for stage in ['W','R','NR','All']:
            if hd[stage].shape[1]:
                logHist = np.zeros(hd[stage].shape[1],dtype={'names':('edge','hist','width','polyfit'),'formats':(float,)*4})
                wl = hd[stage].shape[1] * self.perc_x_polyfit
                
                if np.ceil(wl) % 2:
                    wl = int(np.ceil(wl))
                else:
                    wl = int(np.float(wl))
                wl = max(wl,3)
                polyfit = savgol_filter(hd[stage][1,:]/np.sum(hd[stage][1,:]), wl, 1, deriv=0, delta=1.0, axis=-1, mode='interp', cval=0.0)
                logHist['edge'] = hd[stage][0,:]
                logHist['hist'] = hd[stage][1,:]
                logHist['width'] = hd[stage][2,:]
                logHist['polyfit'] = polyfit
                dict_logHist[stage] = logHist
            else:
                dict_logHist[stage] = []
        return dict_logHist
        
    def compute_isi_histogram(self,bins=None,isi_range=None):
        if not bins:
            bins = 50
        hist_dict = {}
        for stage in ['W','NR','R','All']:
            hist_mat = np.zeros((3,bins))
            hist,edge = np.histogram(self.isi_dict[stage]*1000.,bins=bins,range=isi_range)
            hist_mat[1,:] = hist
            hist_mat[2,:] = np.diff(edge)
            hist_mat[0,:] = edge[:-1]
            hist_dict[stage] = hist_mat
        return hist_dict
    
    def compute_logIsi_histogram(self,isi_range=None):
        
        hist_dict = {}
        for stage in ['W','NR','R','All']:
            isi_vect = np.array(self.isi_dict[stage],dtype=float)*1000.
            try:
                if not isi_range:
                    isi_range = (0,np.ceil(np.max(isi_vect)))
    #            print stage,'MAX ISIVECT', isi_vect
                num = np.ceil(np.log10(np.max(isi_vect)))
                bins = np.logspace(0,num,num*10.)
                hist,edge = np.histogram(isi_vect,bins=bins,range=isi_range)
                hist_mat = np.zeros((3,hist.shape[0]))
                hist_mat[1,:] = hist
                hist_mat[2,:] = np.diff(edge)
                hist_mat[0,:] = edge[:-1]#np.power(10,edge[:-1])
            except:
                hist_mat = np.array([[]])
            hist_dict[stage] = hist_mat
        return hist_dict
        
    def plot_isi(self,stage,close_figs=True,bins=None,isi_range=None,toPlot='isiH'):
        if close_figs:
            plt.close('all')
        fig = plt.figure()
        if toPlot == 'isiH':
            hd = self.compute_isi_histogram(bins=bins,isi_range=isi_range)
        else:
            hd = self.compute_logIsi_histogram(isi_range=isi_range)
        plt.bar(hd[stage][0,:],hd[stage][1,:]/np.sum(hd[stage][1,:]),width=hd[stage][2,:],alpha=0.5)
        plt.xlabel('Time(ms)')
        plt.ylabel('Normalized counts')
        plt.title('ISI Histogram - channel %s unit %s'%(self.channel,self.unit))
        return fig
    
    def plot_log_isi(self,stage,close_figs=True,bins=None,isi_range=None):
        fig = self.plot_isi(stage,close_figs=close_figs,bins=bins,isi_range=isi_range,toPlot='logISIH')
        plt.gca().set_xscale("log")
        return fig
    
    def plot_polyfit_res(self,stage,close_figs=True,new_fig=False):
        if close_figs:
            plt.close('all')
        if new_fig:
            plt.figure()
        logISI = self.fit_logIsiH[stage]
        col = {'W':'b','R':'r','NR':'g','All':'k'}
        label = {'W':'Wake','R':'REM','NR':'NREM','All':'All'}
        plt.bar(logISI['edge'],logISI['hist']/np.sum(logISI['hist']),width=logISI['width'],alpha=0.5,color=col[stage])
        plt.plot(logISI['edge'],logISI['polyfit'],lw=1.,color=col[stage],label=label[stage])
        plt.legend(frameon=False)
        plt.gca().set_xscale("log")
    

