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
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'libraries')
sys.path.append(lib_dir)
from PyQt4.QtCore import (SIGNAL, QThread)
from Analyzing_GUI import *
from Plotting_GUI import *
from Modify_Dataset_GUI import OrderedDict
from copy import copy
import matplotlib
from launcher import function_Launcher
matplotlib.use('qt4agg')

class analysisSingle_thread(QThread):
    def __init__(self, Datas, lock, parent = None):
        super(analysisSingle_thread, self).__init__(parent)
        self.lock = lock
        self.Datas = Datas
        self.inputForPlots = OrderedDict()
        self.outputData = OrderedDict()
        self.info = OrderedDict()
        
    def initialize(self, Input, analysisName, DataDict , TimeStamps, pairedGroups):
        print 'start initialize'
        self.Input = Input
        self.analysisName = analysisName
        print 'DataDict',DataDict
        self.DataList = DataDict.values()[0]
        self.TimeStamps = copy(TimeStamps)
        self.pairedGroups = pairedGroups
        flag = True
        for key in Input.keys():
            if Input[key].has_key('SavingDetails'):
                self.savingDetails = Input[key]['SavingDetails']
                flag = False
                break
        if flag:
            self.savingDetails = False
        print 'end initialize ',self.savingDetails
    def run(self):
        self.outputData, self.inputForPlots, self.info =\
            self.analyze(self.analysisName)
        self.emit(SIGNAL('threadFinished()'))
        
    def setInput(self, Input, DataList):
        self.Input = Input
        self.DataList = DataList
    
    def analyze(self, analysisName):
        print 'analyze called',':',analysisName
        try:
            if analysisName == 'Actogram':
                return Actogram(self.Datas, self.Input, 
                                self.DataList, self.TimeStamps, self.lock)
            elif analysisName == 'AIT':
                return AIT(self.Datas, self.Input, 
                                self.DataList, self.TimeStamps, self.lock)
            elif analysisName == 'Error_Rate':
                return Error_Rate(self.Datas, self.Input, 
                                self.DataList, self.TimeStamps, self.lock)
            elif analysisName == 'Raster_Plot':
                return Raster_Plot(self.Datas, self.Input, 
                                self.DataList, self.TimeStamps, self.lock)
            elif analysisName == 'Peak_Procedure':
                return Peak_Procedure(self.Datas, self.Input, 
                                self.DataList, self.TimeStamps, self.lock)
            else:
                return function_Launcher(analysisName,self.Datas,
                                               self.Input,self.DataList,
                                               self.TimeStamps, self.lock,
                                               self.pairedGroups)
        except Exception,e:# as inst:
            #print(type(inst))    # the exception instance
            #print(inst.args)     # arguments stored in .args
            #print(inst)
            #x = inst.args     # unpack args
            #print('x =', x)
            print e
            outputData, inputForPlot, info = None, None, None
            
        return outputData, inputForPlot, info

def Actogram(Datas, Input, DataList, TimeStamps, lock):
    """
        Actogram from std input dlg
    """
    interval = Input[0]['Combo'][0] * 60
    print 'interval ',interval
    step_num = Input[0]['SpinBox'][0]
    p_min = Input[0]['Range'][0][0]
    p_max = Input[0]['Range'][0][1]
    Light_start = Input[0]['Combo'][1]
    print 'Input extracted'
    inputForPlots, dataDict = OrderedDict(),OrderedDict()
    outputData = OrderedDict()
    lenName = 0
    print 'DL',DataList
    for name in DataList:
        lenName = max(lenName, len(name))
    dtypeDict = {'names':('Subject', 'Period', 'Phase', 'Amplitude',
                          'Translation', 'Pearson corr', 'p_value'),
                 'formats':('|S%d'%lenName, float, float, float, float, float,
                            float)}
    std_SinFit = np.zeros(len(DataList), dtype=dtypeDict)
    ind = 0
    print DataList
    for dataName in DataList:
        try:
            lock.lockForRead()
            data = copy(Datas.takeDataset(dataName))
            ##################### DA INSERIRE OVUNQUE
            if Datas.getTimeStamps(dataName):
                TimeStamps = Datas.getTimeStamps(dataName)
            ##############################################
        finally:
            lock.unlock()
        print 'data exported'
        print TimeStamps
        Start_exp, Start_Time, End_Time = Time_Details_GUI(data,TimeStamps)
        Start_H = (Start_exp)//3600
        Actogram, N_Day = F_Actogram_GUI(data, Start_exp, End_Time,\
                                             interval, TimeStamps, 24)
        Ms,Ds,Ys = StartDate_GUI(data, TimeStamps)
        Me,De,Ye = EndDate_GUI(data, TimeStamps)
        title = u'Actogram %s\nFrom: %d/%d/%d\nTo: %d/%d/%d'\
                %(dataName,Ms,Ds,Ys,Me,De,Ye)
        kwargs = {'Start_Hour': Start_H,'Title' : title}
        inputForPlots[dataName] = {}
        inputForPlots[dataName]['Fig_Actogram'] = (Actogram, N_Day, interval,True,
                                   'FullData', 24, kwargs)
        minutes = np.ones(len(Actogram)) * 60.0 * (interval / 3600.0)
        minutes[0] = 0
        minutes=np.cumsum(minutes)
        dataDict[dataName] = np.zeros(len(Actogram),dtype={'names':
                        ('Activity','Minutes'),
                         'formats':(float,int)})
        dataDict[dataName]['Activity'] = Actogram
        dataDict[dataName]['Minutes']  = minutes
        Period_Array, Best_Fit_Param, Best_Fit =\
        Fit_Sin_BestPeriod(Actogram,p_min,p_max,Start_H, 
                           step_num = step_num,
                           Light_start = Light_start,
                           interval = interval)
        std_SinFit[ind]['Subject'] = dataName
        std_SinFit[ind]['Period'] = Best_Fit_Param['Period']
        std_SinFit[ind]['Phase'] = Best_Fit_Param['Phase']
        std_SinFit[ind]['Amplitude'] = Best_Fit_Param['Amplitude']
        std_SinFit[ind]['Translation'] = Best_Fit_Param['Translation']
        std_SinFit[ind]['Pearson corr'] = Best_Fit_Param['Pearson corr']
        std_SinFit[ind]['p_value'] = Best_Fit_Param['p_value']
        inputForPlots[dataName]['Fig Sinfit'] = (Period_Array, Best_Fit_Param,
                                                 dataName.split('.')[0])
        ind += 1
    
    DataDict = {}
    DataDict['Single Subject Actogram'] = {}
    DataDict['Single Subject Actogram']['Actogram'] = create_OutputData_GUI(dataDict)
    DataDict['Single Subject Actogram']['Sinfit'] = std_SinFit
    
    info = {}
    info['Actogram'] = {}
    info['Actogram']['Types']  = ['Actogram', 'Single Subject']
    info['Actogram']['Factor'] = [0,2]
    info['Sinfit'] = {}
    info['Sinfit']['Types'] = ['SinFit','Single Subject']
    info['Sinfit']['Factor'] = []
    return DataDict, inputForPlots, info

def AIT(Datas, Input, DataList, TimeStamps, lock):
    """
        Ait computation from std input dlg
    """
    TimeInterval  = Input[0]['Combo'][0]
    Dark_start    = Input[0]['Combo'][1]
    Dark_length   = Input[0]['Combo'][2]
    inputForPlots = {}
    dataDict      = {}
   
    for dataName in DataList:
        try:
            lock.lockForRead()
            data = copy(Datas.takeDataset(dataName))
            ##################### DA INSERIRE OVUNQUE
            if Datas.getTimeStamps(dataName):
                TimeStamps = Datas.getTimeStamps(dataName)
            ##############################################
        finally:
            lock.unlock()
        print 'Dato estratto'
        OrdMedian,OrdMean,OrdStd,perc25,perc75,\
            Hour_Dark,Hour_Light,HourStart_AIT = AITComputation_GUI(
                data, Dark_start,
                TimeStamps, Dark_length,
                TimeInterval=TimeInterval)
        Hours=np.hstack((Hour_Dark,Hour_Light))
        dark_bin = (((Dark_start-12) * 3600.)%(3600.*24))/TimeInterval
        Hlabel = TimeUnit_to_Hours_GUI(Hours+dark_bin,TimeInterval)
        LenDark = Hour_Dark.shape[0]

        AITVector=np.zeros(len(Hlabel),dtype={'names':('Mean','Median','Standard Error','Perc 25','Perc 75','Time'),'formats':(float,float,float,float,float,'|S5')})
        AITVector['Mean']=OrdMean
        AITVector['Median']=OrdMedian
        AITVector['Standard Error']=OrdStd
        AITVector['Perc 25']=perc25
        AITVector['Perc 75']=perc75
        AITVector['Time']=Hlabel
        print 'AITVector created'
        inputForPlots[dataName] = {}
        inputForPlots[dataName]['Fig_AIT'] = (OrdMean, OrdStd,
                                          Hlabel, 'b', 'r', LenDark, 0.3,
                                         'Actual Inter Trial\n%s'\
                                         %dataName, 
                                         'AIT Duration (min)',None,OrdMedian,perc25,perc75)
        print 'inputForPlots created'
        dataDict[dataName] = AITVector
        print 'dataDict created'
    
    DataDict = {}
    DataDict['Single Subject AIT'] = {}
    DataDict['Single Subject AIT']['AIT'] = create_OutputData_GUI(dataDict)
    
    info = {}
    info['AIT'] = {}
    info['AIT']['Types']  = ['AIT', 'Single Subject']
    info['AIT']['Factor'] = [0,5]
    
    return DataDict, inputForPlots, info

def Error_Rate(Datas, Input, DataList, TimeStamps, lock):
    dataDict, inputForPlots = {},{}
    outputData   = {}
    
    TimeInterval = Input[0]['Combo'][0]
    Dark_start   = Input[0]['Combo'][1]
    Dark_length  = Input[0]['Combo'][2]
    tend = Input[0]['DoubleSpinBox'][0]
    if TimeInterval <= 3600:
        HBin = 1
    else:
        HBin = int(TimeInterval/3600)
        TimeInterval = 3600
    Hour_Dark,Hour_Light=Hour_Light_and_Dark_GUI(Dark_start,Dark_length,
                                                 TimeInterval)
    LenDark=len(Hour_Dark)
    for dataLabel in DataList:
        inputForPlots[dataLabel] = {}
        try:
            lock.lockForRead()
            data = copy(Datas.takeDataset(dataLabel))
            ##################### DA INSERIRE OVUNQUE
            if Datas.getTimeStamps(dataLabel):
                TimeStamps = Datas.getTimeStamps(dataLabel)
            ##############################################
        finally:
            lock.unlock()
        title = 'Error Rate\n%s'%dataLabel.split('.')[0]
        Start_exp,Start_Time,End_Time = Time_Details_GUI(data,TimeStamps)
        
        
        try:
            A,cr=F_Correct_Rate_New_GUI(data,
                                    TimeStamps,Start_exp,24,tend=tend,
                                    TimeInterval=TimeInterval)
        except:
            print 'unable to extract correct rate'
            return
        ReorderIndex = np.hstack((Hour_Dark,Hour_Light))
        if HBin==1:
            HLabel = TimeUnit_to_Hours_GUI(ReorderIndex,TimeInterval)
            VectorError=np.zeros(len(HLabel),dtype={'names':('Mean','Time'),'formats':(float,'|S5')})
            VectorError['Time']=HLabel
            VectorError['Mean']=1-cr[ReorderIndex]
            inputForPlots[dataLabel]['Fig_Error_Rate_Daily_Average'] =\
                                cr[ReorderIndex],HLabel,'b','r',\
                                LenDark-0.5, 0.3, title, True
        else:
            Mean,Median,StdError,HLabel =\
                HourDark_And_Light_BinnedMean_GUI(cr,np.arange(24),
                Hour_Dark,Hour_Light,
                HBin,TimeUnit_Dur_Sec = TimeInterval)
            LenDark = len(Hour_Dark[::HBin])-0.5
            inputForPlots[dataLabel]['Fig_Error_Rate_Daily_Average'] =\
                                Mean,HLabel,'b','r',LenDark,\
                                0.3,title,True
            VectorError = np.zeros(len(HLabel),
                                   dtype={'names':('Mean','Time'),
                                   'formats':(float,'|S5')})
            VectorError['Time'] = HLabel
            VectorError['Mean'] = 1-Mean
        dataDict[dataLabel] = VectorError
        outputData['Error Rate'] = create_OutputData_GUI(dataDict)
        
    DataDict = {}
    DataDict['Single Subject Error Rate'] = {}
    DataDict['Single Subject Error Rate']['Error Rate'] = outputData['Error Rate']
    
    info = {}
    info['Error Rate'] = {}
    info['Error Rate']['Types']  = ['Error Rate', 'Single Subject']
    info['Error Rate']['Factor'] = [0]
    return DataDict, inputForPlots, info

def Raster_Plot(Datas, Input, DataList, TimeStamps, lock):
    inputForPlots = {}
    
    if Input[0]['Combo'][0] == 'Probe Left':
        HopperSide = 'l'
    elif Input[0]['Combo'][0] == 'Probe Right':
        HopperSide = 'r'
    
    if Input[0]['Combo'][1] == 'Left':
        loc_for_Pk = 'l'
        Location = 's'
        LocName  = 'Left'
    elif Input[0]['Combo'][1] == 'Right':
        Location = 'l'
        LocName  = 'Right'
        loc_for_Pk = 'r'
    else:
        Location = 's'
        Location1 = 'l'
        LocName = 'Both'
    t_first = Input[0]['TimeSpinBox'][0][0]*3600 +\
              Input[0]['TimeSpinBox'][0][1]*60
    t_last  = Input[0]['TimeSpinBox'][1][0]*3600 +\
              Input[0]['TimeSpinBox'][1][1]*60
    tend    = Input[0]['DoubleSpinBox'][0]
    if Input[0]['Combo'][1] == 'Both':
        printBoth = True
        loc_for_Pk = 'l'
        loc_for_Pk1 = 'r'
    else:
        printBoth = False
    for dataName in DataList:
        try:
            lock.lockForRead()
            data   = copy(Datas.takeDataset(dataName))
            ##################### DA INSERIRE OVUNQUE
            if Datas.getTimeStamps(dataName):
                TimeStamps = Datas.getTimeStamps(dataName)
            ##############################################
            scale  = copy(Datas.scaled(dataName)[1])
        finally:
            lock.unlock()
        print 'data copied'
        Start_exp,Start_Time,End_Time = Time_Details_GUI(data,
                                                         TimeStamps)
        print 'time details extracted'
        if Input[0]['Combo'][0] == 'All':
            TrialOnset = np.where(data['Action']==TimeStamps['Center Light On'])[0]
            TrialOffset = np.where(data['Action']==TimeStamps['End Intertrial Interval'])[0]
            TrialOnset = F_OnSet_GUI(TrialOffset,TrialOnset)
            TrialOffset = F_OffSet_GUI(TrialOnset,TrialOffset)
            if len(TrialOnset)>len(TrialOffset):
                TrialOnset=TrialOnset[:-1]
            index = np.where((data['Time'][TrialOnset] + Start_exp)%24 <= t_last)[0] 
            index_2 = np.where((data['Time'][TrialOnset][index] + Start_exp)%24 >= t_first)[0]
            TrialOnset = TrialOnset[index][index_2]
            TrialOffset = TrialOffset[index][index_2]
            Pks = TrialOnset,TrialOffset
            Pk = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,
                                  loc_for_Pk)
            if printBoth:
                
                
                Pk1 = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,
                                       loc_for_Pk1)
                inputForPlots[dataName] = {}
                inputForPlots[dataName]['Fig_Raster_%s'%LocName] =\
                    Pk[0], Location, scale,\
                    Pk1[0], Location1, scale
            else:
                inputForPlots[dataName] = {}
                inputForPlots[dataName]['Fig_Raster_%s'%LocName] =\
                        Pk[0], Location, scale
                
        else:
            Pks_0,Pks_1,indTrOn,trNum = F_Probes_x_TimeInterval_GUI(data, 
                                              TimeStamps, Start_exp,
                                              End_Time, HopperSide, tend = tend,
                                              Floor=True,  t_first = t_first, 
                                              t_last = t_last,
                                              return_IndProbe=True)
            Pks = (Pks_0,Pks_1)
            Pk = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,
                                  loc_for_Pk,trial_num=trNum,trial_ind=indTrOn)
            if printBoth:
                print 'HS: ',HopperSide
                Pk1 = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,
                                       loc_for_Pk1,trial_num=trNum,
                                       trial_ind=indTrOn)
                inputForPlots[dataName] = {}
                inputForPlots[dataName]['Fig_Raster_%s'%LocName] =\
                    Pk[0], Location, scale,\
                    Pk1[0], Location1, scale
            else:
                inputForPlots[dataName] = {}
                inputForPlots[dataName]['Fig_Raster_%s'%LocName] =\
                        Pk[0], Location, scale
        print 'Raster Plot Extracted'
        

        
    return {}, inputForPlots, {}

def Peak_Procedure(Datas, Input, DataList, TimeStamps, lock):
    outputData, dataDict, inputForPlots = {}, {}, {}
    t = Input[0]['DoubleSpinBox'][0]
    
    
    if Input[0]['Combo'][0] == 'Probe Left':
        HopperSide = 'l'
    elif Input[0]['Combo'][0] == 'Probe Right':
        HopperSide = 'r'   
    if Input[0]['Combo'][1] == 'Left':
        Location = 'l'
        LocName  = 'left hopper'
        loc_for_Pk = 'l'
    else:
        Location = 's'
        LocName  = 'right hopper'
        loc_for_Pk = 'r'

    t_first = Input[0]['TimeSpinBox'][0][0]*3600 +\
              Input[0]['TimeSpinBox'][0][1]*60
    t_last  = Input[0]['TimeSpinBox'][1][0]*3600 +\
              Input[0]['TimeSpinBox'][1][1]*60
    tend    = Input[0]['DoubleSpinBox'][1]
    centiSec = np.arange(0,tend,0.01)
    for dataName in DataList:
        dataDict[dataName], inputForPlots[dataName] = OrderedDict(),\
                                                      OrderedDict()
        try:
            lock.lockForRead()
            data   = copy(Datas.takeDataset(dataName))
            ##################### DA INSERIRE OVUNQUE
            if Datas.getTimeStamps(dataName):
                TimeStamps = Datas.getTimeStamps(dataName)
            ##############################################
#            scale  = copy(Datas.scaled(dataName)[1])
        finally:
            lock.unlock()
        print 'data copied'
        
        Start_exp,Start_Time,End_Time = Time_Details_GUI(data,
                                                         TimeStamps)
        print 'time details extracted'
        ## Probe trial on and off
        if Input[0]['Combo'][0] == 'All':
            TrialOnset = np.where(data['Action']==TimeStamps['Center Light On'])[0]
            TrialOffset = np.where(data['Action']==TimeStamps['End Intertrial Interval'])[0]
            TrialOnset = F_OnSet_GUI(TrialOffset,TrialOnset)
            TrialOffset = F_OffSet_GUI(TrialOnset,TrialOffset)
            if len(TrialOnset)>len(TrialOffset):
                TrialOnset=TrialOnset[:-1]
            index = np.where((data['Time'][TrialOnset] + Start_exp)%24 <= t_last)[0] 
            index_2 = np.where((data['Time'][TrialOnset][index] + Start_exp)%24 >= t_first)[0]
            TrialOnset = TrialOnset[index][index_2]
            TrialOffset = TrialOffset[index][index_2]
            Pks = TrialOnset,TrialOffset
            
        else:
            Pks = F_Probes_x_TimeInterval_GUI(data, TimeStamps, Start_exp,
                                          End_Time, HopperSide, tend = tend,
                                          Floor=True,  t_first = t_first, 
                                          t_last = t_last)
        print 'Pks computed'
        print '\n\nLen pks: ',len(Pks[0])
        print dataName
        Pk = F_PeakProbes_GUI(data, TimeStamps, Pks[0], Pks[1], tend,
                              loc_for_Pk)
        print 'Pk computed'
        if Input[0]['Combo'][0] == 'All':
            title = 'All trials, %s'%LocName
        else:
            title = '%s trials, %s'%(Input[0]['Combo'][0],LocName)
        print np.max(Pk[1])
        inputForPlots[dataName]['Fig_Peak_%s'%LocName] =\
                Pk[1], tend, t, Location, 'Peak Procedure\n%s\n%s'%(dataName,
                title),\
                t_first, t_last
        dataDict[dataName] = np.zeros(len(Pk[1]),dtype = {'names':
                                                    ('Value',
                                                     'Centisec'),
                                                     'formats':
                                                     (float,float)})
        dataDict[dataName]['Value']    = Pk[1]
        dataDict[dataName]['Centisec'] = centiSec
    outputData['Peak_%s'%LocName] = create_OutputData_GUI(dataDict)
     
    DataDict = {}
    DataDict['Single Subject Peak'] = {}
    DataDict['Single Subject Peak']['Peak_%s'%LocName] = outputData['Peak_%s'%LocName]
    
    info = {}
    info['Peak_%s'%LocName] = {}
    info['Peak_%s'%LocName]['Types']  = ['Peak Procedure', 'Single Subject']
    info['Peak_%s'%LocName]['Factor'] = [0,2]

    return DataDict, inputForPlots, info

if __name__== '__main__':
#    data = np.loadtxt('C:\Users\ebalzani\IIT\myPython\E_Pycodes\Dataset\IIT_Cage_8_N.csv')
    Input = {}
    Input['Combo'] = 900
    