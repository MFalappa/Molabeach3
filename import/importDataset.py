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

import os,sys
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../..')),'libraries')
dlgAn_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../..')),'dialogsAndWidget','analysisDlg')
repo_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../..')),'actionDictionaries')

sys.path.append(dlgAn_dir)
sys.path.append(lib_dir)
import numpy as np
import h5py
from Modify_Dataset_GUI import (DetectDelimiter_GUI,Rescale_Time_GUI,Time_Details_GUI,
                                Terminate_Dataset_GUI,Dataset_GUI,EEG_Data_Struct)
import pyedflib
import pandas as pd
import nexfile
from input_Dlg_std import *

def loadTimeActionData_TSE(path):
    """
This porcedure allow to import file with two columns with time - code action data.
Possible delimiter are ['\t',';',','], with time in millisec.Time Stamps for
TSE system==TSE data
    """
    timestamps = np.load(os.path.join(repo_dir,'TSE.npy')).all()
    delimiter = DetectDelimiter_GUI(path)

    scale = 1000
    Scaled = (True,scale)
    Types =['TSE']
    fh = open(path,'U')
    header = 0
    line = fh.readline()
    while line:
        line.split(delimiter)
        try:
            float(line.split(delimiter)[0])
            break
        except:
            header += 1
            line = fh.readline()
    fh.close()
    Dataset = np.loadtxt(path,delimiter=delimiter,
                         dtype={'names':('Time','Action'),
                         'formats':('f8','f8')},skiprows=header)
    Dataset = Rescale_Time_GUI(Dataset, timestamps,scale,header=12,footer=3)
    End_Time = Time_Details_GUI(Dataset, timestamps)[2]
    Dataset = Terminate_Dataset_GUI(Dataset,End_Time,timestamps)
    ds = Dataset_GUI(Dataset, os.path.basename(path), Path=path, Types=Types, Scaled=Scaled,TimeStamps=timestamps)
    return ds
    
def load_TSE_edited_data(path):
    """
This porcedure allow to import file with two columns with time - code action data.
Possible delimiter are ['\t',';',','], with time in millisec.Time Stamps for
TSE system.
This function works ONLY for obsolete data edited from TSE.
In these file there is a footer (in the new version it has been deleted)==TSE data edited 
    """
    timestamps = np.load(os.path.join(repo_dir,'TSE.npy')).all()
    delimiter = DetectDelimiter_GUI(path)

    scale = 1000
    Scaled = (True,scale)
    Types =['TSE']
    fh = open(path,'U')
    header = 0
    line = fh.readline()
    while line:
        line.split(delimiter)
        try:
            float(line.split(delimiter)[0])
            break
        except:
            header += 1
            line = fh.readline()
    fh.close()
    Dataset = np.genfromtxt(path,delimiter=delimiter,
                         dtype={'names':('Time','Action'),
                         'formats':('f8','f8')},skip_header=header,skip_footer=3)
    Dataset = Rescale_Time_GUI(Dataset, timestamps,scale,header=12,footer=3)
    End_Time = Time_Details_GUI(Dataset, timestamps)[2]
    Dataset = Terminate_Dataset_GUI(Dataset,End_Time,timestamps)
    ds = Dataset_GUI(Dataset, os.path.basename(path), Path=path, Types=Types, Scaled=Scaled,TimeStamps=timestamps)
    return ds
    

def loadTimeActionData_AM_microsystems(path):
    """
This porcedure allow to import file with two columns with time - code action data.
Possible delimiter are ['\t',';',','], with time in millisec.Time Stamps for
am-microsystems==AM microsystems data 
    """
    timestamps = np.load(os.path.join(repo_dir,'AM-Microsystems.npy')).all()
    delimiter = DetectDelimiter_GUI(path)

    scale = 1000
    Scaled = (True,scale)
    Types = ['AM-Microsystems']
    fh = open(path,'U')
    header = 0
    line = fh.readline()
    while line:
        line.split(delimiter)
        try:
            float(line.split(delimiter)[0])
            break
        except:
            header += 1
            line = fh.readline()
    fh.close()
    Dataset = np.loadtxt(path,delimiter=delimiter,
                         dtype={'names':('Time','Action'),
                         'formats':('f8','f8')},skiprows=header)
    # remove bactery levels
    Dataset = Dataset[Dataset['Action'] != timestamps['Bactery Level']]
    Dataset = Rescale_Time_GUI(Dataset, timestamps,scale,header=11,footer=3)
    End_Time = Time_Details_GUI(Dataset, timestamps)[2]
    Dataset = Terminate_Dataset_GUI(Dataset,End_Time,timestamps)
    ds = Dataset_GUI(Dataset, os.path.basename(path), Path=path, Types=Types, Scaled=Scaled,TimeStamps=timestamps)
    return ds

def load_sleep_sign_export_text(path):
    """
This function imports dataset from sleep sign exported as text that can contain the
following columns:Times, Epoch, Stage and power spectrum or Delta,Theta,Gamma,...==Sleep data
    """
    delimiter = DetectDelimiter_GUI(path)
    num_header = 0
    fh = open(path,'U')
    flagBreak = False
    line = fh.readline()
    while line:
#        print(line)
        for head in ['EpochNo',	'Stage','Time',	'0.000000Hz']:
            if head in line:
                flagBreak = True
                break
        if flagBreak:
            break
        line = fh.readline()
        num_header += 1
    if len(line.split(delimiter)) < 10:
        Types = ['EEG Binned Frequencies']
    else:
        Types = ['EEG Full Power Spectrum']
    fh.close()
    data_sleep = EEG_Data_Struct(PathToFile=path, delimiter=delimiter,header=num_header+1)
    Scaled = (True,1)
    ds = Dataset_GUI(data_sleep, os.path.basename(path), Path=path, Types=Types, Scaled=Scaled,TimeStamps=None)    
    return ds

def load_excel(path):
    """
This function can import generic excel datasheet that can be parsed by 
Pandas library==Load excel without parsing
    """
    excel = pd.ExcelFile(path)
    Types = ['Unparsed Excel File']
    ds = Dataset_GUI(excel, os.path.basename(path), Path=path, Types=Types, Scaled=(True,1),TimeStamps=None)    
    return ds

def load_and_parse_excel(path):
    """
This function load and parse excel files via Pandas library==Load excel with parsing
    """
    excel = pd.ExcelFile(path)
    Types = ['Parsed Excel']
    dict_excel = {}
    for sheet in excel.sheet_names:
        dict_excel[sheet] = excel.parse(sheetname=sheet)
    ds = Dataset_GUI(dict_excel, os.path.basename(path), Path=path, Types=Types, Scaled=(True,1),TimeStamps=None)    
    return ds
    
def load_Spike_Data(path):
    """
This function can import a MatLab file with struct contains raw data and/or spike 
data extract from neural recording system==Spike data
    """
    data = h5py.File(path,'r')
    Types = ['single unit struct']
    ds = Dataset_GUI(data, os.path.basename(path), Path=path, Types=Types, Scaled=(True,1),TimeStamps=None)    
    return ds

def importNex_Nex(path):
    """
Import NeuroNexus ".nex" files  using the "nexfile.py" script 
from http//neuroexplorer.com/downloadspage==Nex files
    """
    reader = nexfile.Reader(useNumpy=True)
    fileData = reader.ReadNexFile(path)
    Types = ['nex_file']
    ds = Dataset_GUI(fileData, os.path.basename(path), Path=path, Types=Types, Scaled=(True,1),TimeStamps=None)    
    return ds

def create_laucher():
    fh = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'importDataset.py'))
    script = 'import numpy as np\nfrom importDataset import *\n\ndef launchLoadingFun(fhname,funName):\n'
    script += '\tprint(\'Importing function launchehd: \', funName)\n'
    line = fh.readline()
    while line:
        if line.startswith(('def ','def\t')):
            funName = (line[3:].replace(' ','')).replace('\t','')
            funName = funName.split('(')[0]
            if funName == 'main' or funName == 'create_laucher':
                line = fh.readline()
                continue
            script += '\tif funName == \'%s\':\n\t\treturn %s(fhname)\n\n'%(funName,funName)
        line = fh.readline()
    fh.close()
    dir_launcher = os.path.dirname(os.path.realpath(__file__))
    fh = open(os.path.join(dir_launcher,'importLauncher.py'),'w')
    fh.write(script)
    fh.close()
    
def loadTimeActionData_MED_SW(path):
    """
This method import data recorded from MED system configurated as follows:
the relative code were choosen arbitrary by the user programming MED software.
Apparatus:
#1 central hopper,
#2 left lever,
#3 right lever,
#4 .....==MED associates
    """
    timestamps = np.load(os.path.join(repo_dir,'MED_SW.npy')).all()
    scale = 1
    Scaled = (True,scale)
    Types =['MED_SW']
    
    raw = np.loadtxt(path)
    startDate = np.zeros(3)
    startDate[0] = int(raw[1]) # day
    startDate[1] = int(raw[0]) # month
    startDate[2] = int(raw[2]) # year
    
    endDate = np.zeros(3)
    endDate[0] = int(raw[4]) # day
    endDate[1] = int(raw[3]) # month
    endDate[2] = int(raw[5]) # year

    startRaw = raw.shape[0]-4

    findRaw = False

    while findRaw == False:
    
        if (raw[startRaw+2] == startDate[0]) and\
           (raw[startRaw+1] == startDate[1]) and\
           (raw[startRaw+3] == startDate[2]) and\
           (raw[startRaw-1] == startDate[0]) and\
           (raw[startRaw-2] == startDate[1]) and\
           (raw[startRaw] == startDate[2]):
        
            startRaw = startRaw -3
            findRaw = True
        else:
            startRaw = startRaw - 1  
            
    startH = int(raw[startRaw+11]) #hour
    startM = int(raw[startRaw+12]) #minutes
    startS = int(raw[startRaw+13]) #seconds

    endH = int(raw[startRaw+14]) #hour
    endM = int(raw[startRaw+15]) #minutes
    endS = int(raw[startRaw+16]) #seconds


    offSet = 21
    firstCode = 27
    nEvent = int(raw[startRaw+offSet])
    start = 19
    nameEvent = ['Start Trial','Stop Trial','Left Light On','Right Light On','Left Light Off','Right Light Off','House Light On','House Light Off','Left NP In','Right NP In','Center NP In','Center NP Out','Give Pellet Center','Start Intertrial Interval','End Intertrial Interval','Timeout Reached','null','null','Start experiment','Stop experiment','null','null','Short trial','Long trial','Short probe trial','Long probe trial','Water on','Water off']

    code = np.zeros((nEvent + 12),dtype = int)
    time = np.zeros((nEvent + 12),dtype = float)
    event = np.empty((nEvent + 12),dtype = "S35")
    
    code[0] = 29
    time[0] = startDate[0]
    event[0] = 'Start Day'
    code[1] = 30
    time[1] = startDate[1]
    event[1] = 'Start Month'
    code[2] = 31
    time[2] = startDate[2]
    event[2] = 'Start Year'
    
    
    code[3] = 32
    time[3] = startH
    event[3] = 'Start Hour'
    code[4] = 33
    time[4] = startM
    event[4] = 'Start Minute'
    code[5] = 34
    time[5] = startS
    event[5] = 'Start Second'
    
    code[6] = 35
    time[6] = endDate[0]
    event[6] = 'End Day'    
    code[7] = 36
    time[7] = endDate[1]
    event[7] = 'End Month'   
    code[8] = 37
    time[8] = endDate[2]
    event[8] = 'End Year'

    code[9] = 38
    time[9] = endH
    event[9] = 'End Hour'   
    code[10] = 39
    time[10] = endM
    event[10] = 'End Minute'    
    code[11] = 40
    time[11] = endS
    event[11] = 'End Second'
    
    
    
   
    

    if raw[startRaw+firstCode] == start:
        for kk in range(nEvent):
            code[kk + 12] = int(raw[startRaw+firstCode+kk])
            time[kk + 12] = raw[startRaw+firstCode+nEvent+kk]
            event[kk + 12] = nameEvent[int(code[kk + 12]-1)]
    
   
     
    Dataset = np.zeros(nEvent + 12,dtype={'names':('Time','Action','Event'), 'formats':(float,int,'S35')})
    Dataset['Time'] = time
    Dataset['Action'] = code
    Dataset['Event'] = event
   
    ds = Dataset_GUI(Dataset, os.path.basename(path), Path=path, Types=Types, Scaled=Scaled,TimeStamps=timestamps)
    return ds


def load_EDF_data(path):
    """
This porcedure allow to import file in the European Data Format (EDF).This function
import EEG, EMG, TEMPERATURE and motor ACTIVITY from DSI recordings==EDF data
    """
    timestamps = None

    scale = 1
    Scaled = (True,scale)
    Types =['EFT']
    f = pyedflib.EdfReader(path)
    START = f.getStartdatetime()
    EEG = f.readSignal(0)
    EMG = f.readSignal(2)
    TEMPERATURE = f.readSignal(5)
    ACTIVITY = f.readSignal(4)
    Dataset = {}
    Dataset['date'] = START
    Dataset['eeg'] = EEG
    Dataset['emg'] = EMG
    Dataset['temperature'] = TEMPERATURE
    Dataset['activity'] = ACTIVITY
    f._close()
    
    ds = Dataset_GUI(Dataset, os.path.basename(path), Path=path, Types=Types, Scaled=Scaled,TimeStamps=timestamps)
    return ds

create_laucher()

if __name__=='__main__':
#    s=loadTimeActionData_TSE('C:\Users\ebalzani\Desktop\TMP\\1.csv')
    pass
    
