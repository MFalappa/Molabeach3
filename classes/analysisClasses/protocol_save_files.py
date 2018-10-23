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

import sys,os
lib_fld = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
sys.path.append(lib_fld)
import numpy as np
from Modify_Dataset_GUI import *
import datetime as dt

def save_data_container(data_container, list_of_files, path_folder,fname=None):
    dc = DatasetContainer_GUI()
    for name in list_of_files:
        dc.add(data_container[name])
    if not fname:
        now = dt.datetime.now()
        time = now.year,now.month,now.day,now.hour,now.minute
        fname = os.path.join(path_folder,'workspace_%d-%d-%dT%d_%d'%time + '.phz')
    np.savez_compressed(fname ,**dc)
    os.rename(fname + '.npz', fname.split('.')[0] + '.phz')
    return

def load_npz(file_names,data_container):
    print 'load_npz',file_names
    dc = DatasetContainer_GUI()
    for name in file_names:
        loaded_data = np.load(name)
        for key in loaded_data.keys():
            dc.add(loaded_data[key].all())
        data_container.join(dc)
    return data_container


    
if __name__ == '__main__':
    dc = DatasetContainer_GUI()
    fpath =  'C:\Users\ebalzani\Dropbox\switch\\'
    for k in [1,2]:
        d=np.loadtxt(fpath+'%d.tmpcsv'%k,delimiter='\t')
        d = Dataset_GUI(d,'%d'%k,Types=['Unknown','Time_Action'],Path=fpath)
        dc.add(d)
    dc1 = DatasetContainer_GUI()
    for k in [2]:
        d=np.loadtxt(fpath+'%d.tmpcsv'%k,delimiter='\t')
        d = Dataset_GUI(d,'%d'%k,Types=['Unknown','Time_Action'],Path=fpath)
        dc1.add(d)
    dc.join(dc1)
    list_of_files=['1','2']
    path_folder = 'C:\Users\ebalzani\Desktop\TMP'
    save_data_container(dc,list_of_files,path_folder)
    
    load_dc = load_npz(['C:\Users\ebalzani\Desktop\TMP\\all.npz'],dc1)
