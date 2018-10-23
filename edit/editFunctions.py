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
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../..")),'libraries')
anDlg_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../..")),'dialogsAndWidget','analysisDlg')
phenopy_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../..")),'mainScripts')
sys.path.append(lib_dir)
sys.path.append(anDlg_dir)
sys.path.append(phenopy_dir)
from Modify_Dataset_GUI import *
from MergeDlg import MergeDlg
from mainAnalysis import *
from PyQt4.QtGui import QApplication
from CreateGroupsDlg import CreateGroupsDlg
from Input_Dlg_std import inputDialog
import datetime as DT
import numpy as np

def TSE__Merge_Dataset(phenopy, selType='TSE'): 
    """
        Merge two dataset of the TSE type
    """
    DatasetContainer = phenopy.Dataset
    dialog = MergeDlg( SelectedType = selType,DataContainer=DatasetContainer)
    if not dialog.exec_():
        return
    mergeDict = dialog.mergeDict
    for key in mergeDict.keys():
        datalist = mergeDict[key]
        data_dict = {}
        try:
            phenopy.lock.lockForRead()
            for dataName in datalist:
                data_dict[dataName] = DatasetContainer.takeDataset(dataName)
            Merged = Merge_N_Dataset_GUI(data_dict,datalist,DatasetContainer[dataName].TimeStamps)
        finally:
            phenopy.lock.unlock()
        try:
            phenopy.lock.lockForWrite()
            data = Dataset_GUI(Merged, key, Path=None,Types=[selType],Scaled=(True,1000.),
                               TimeStamps=DatasetContainer[dataName].TimeStamps)
            phenopy.Dataset.pop(key)                
            phenopy.Dataset.add(data)
            message = 'Merged data %s'%key
            phenopy.listWidgetRight.addItem(message)
        except Exception, e:
            phenopy.listWidgetRight.addItem(e)
        finally:
            phenopy.lock.unlock()
    
def AM_Microsystems__Merge_Dataset(phenopy):
    TSE__Merge_Dataset(phenopy, selType='AM-Microsystems')
          
def EEG_Binned_Frequencies__Merge_Dataset(phenopy, selType='EEG Binned Frequencies'): 
    """
        Merge two dataset of the sleepSign FFT export type.
    """
    DatasetContainer = phenopy.Dataset
    dialog = MergeDlg(SelectedType = selType,DataContainer=DatasetContainer)
    if not dialog.exec_():
        return
    mergeDict = dialog.mergeDict
    for key in mergeDict.keys():
        datalist = mergeDict[key]
        try:
            phenopy.lock.lockForWrite()
            Data = DatasetContainer.takeDataset(datalist[0])
            for dataName in datalist[1:]:
                tmpData = DatasetContainer.takeDataset(dataName)
                if len(np.where(tmpData.freqTuple != Data.freqTuple)[0]) != 0:
                    raise ValueError
                    
                Data.PowerSp = np.vstack((Data.PowerSp, tmpData.PowerSp))
                DeltaDay = Data.Timestamp[-1] - tmpData.Timestamp[0]
                tmpData.Timestamp = vectAddDays(tmpData.Timestamp,
                    daynum=DeltaDay.days)
                if tmpData.Timestamp[0] <= Data.Timestamp[-1]:
                    tmpData.Timestamp = vectAddDays(tmpData.Timestamp, daynum=1)
                Data.Timestamp = np.hstack((Data.Timestamp, tmpData.Timestamp))
                Data.Stage = np.hstack((Data.Stage, tmpData.Stage))
            
            data = Dataset_GUI(Data, key, Path=None,Types=[selType],Scaled=(True,1))
            phenopy.Dataset.pop(key)                
            phenopy.Dataset.add(data)
            message = 'Merged data %s'%key
            phenopy.listWidgetRight.addItem(message)
#        except Exception, e:
#            phenopy.listWidgetRight.addItem(e.message)
        finally:
            phenopy.lock.unlock()

def EEG_Full_Power_Spectrum__Merge_Dataset(phenopy):
    """
        Merge dataset of the sleepSign export type
    """
    EEG_Binned_Frequencies__Merge_Dataset(phenopy,selType='EEG Full Power Spectrum')
    
def TSE_Cut_Dataset(phenopy, selType='TSE'):
    """
        Cut dataset of TSE type keeping only a range of experimental days
    """
    dataContainer = phenopy.Dataset
    Groupdialog = CreateGroupsDlg(1,dataContainer.keys(),DataContainer=dataContainer,
                                  TypeList=[selType],parent=phenopy)
    if not Groupdialog.exec_():
        return
    datadict = Groupdialog.returnSelectedNames()
    datalist = datadict[datadict.keys()[0]]
    IsFirst = True
    for dataName in datalist:
        Start_exp,Start_Time,End_Time = Time_Details_GUI(dataContainer.takeDataset(dataName),
                                                        dataContainer[dataName].TimeStamps)   
        N_Day=int(np.ceil((End_Time[0]-Start_exp[0])/(3600*24)))
        Days=[ '%s'%d for d in xrange(1,N_Day+2) ]
        DaysValue = range(1,N_Day+2)
        if IsFirst:
            comboBox = [(u'Starting Day:',Days,DaysValue,0),
                        (u'Ending Day:',Days, DaysValue, len(Days)-1)]
            timeSpinBox = [None,('Starting Time:',0, 0),
                           ('Ending Time',23,59),None]
            IsFirst = False
        else:
            comboBox = [(u'Starting Day:', Days,DaysValue, dialog.ComboBox[0].currentIndex()),
                        (u'Ending Day:', Days, DaysValue, min(dialog.ComboBox[1].currentIndex(),len(Days)))]
            timeSpinBox = [None,('Starting Time:',dialog.HourSpinBox[1].value(), dialog.MinuteSpinbox[1].value()),
                           ('Ending Time',dialog.HourSpinBox[2].value(),dialog.MinuteSpinbox[2].value()),None]
        lineEdit = ['Dataset name:']
        dialog = inputDialog(dataName, comboBox, timeSpinBox, None, lineEdit, parent=phenopy)
        if not dialog.exec_():
            continue
        try:
            stdOutput = dialog.createStdOutput()
            dayStart = stdOutput['Combo'][0]
            dayEnd = stdOutput['Combo'][1]
            hourStart = stdOutput['TimeSpinBox'][0][0] * 3600 + stdOutput['TimeSpinBox'][0][1] * 60
            hourEnd = stdOutput['TimeSpinBox'][1][0] * 3600 + stdOutput['TimeSpinBox'][1][1] * 60
            secStart = (dayStart - 1)*3600*24+hourStart
            secEnd = (dayEnd - 1)*3600*24+hourEnd
            phenopy.lock.lockForWrite()
            print secStart,secEnd
            Dataset = Cut_Dataset_GUI(dataContainer.takeDataset(dataName),secStart,secEnd,
                                      dataContainer[dataName].TimeStamps, DayOrSec='Sec')
            
            message = 'Cutted Dataset %s'%dataName
            newName = stdOutput['LineEdit'][0]
            if newName:
                dataContainer.pop(newName)
            else:
                newName = copy(dataName)
            while newName in dataContainer.keys():
                newName = newName.split('.')[0] + '_Cut.csv'
                    
            data = Dataset_GUI(Dataset, newName,
                               Path=None,Types=dataContainer[dataName].Types,
                               Scaled=dataContainer[dataName].Scaled,
                               TimeStamps=dataContainer[dataName].TimeStamps)
            dataContainer.add(data)
            phenopy.listWidgetRight.addItem(message)
        except IndexError, e:
            message = 'Failed to cut Dataset %s with exception'%(dataName,e.message)
            phenopy.listWidgetRight.addItem(message)
        finally:
            phenopy.lock.unlock()

def AM_Microsystems__Cut_Dataset(phenopy):
    """
        Cut dataset of AM-Microsystems type keeping only a range of 
        experimental days
    """
    TSE_Cut_Dataset(phenopy, selType='AM-Microsystems')

def EEG_Binned_Frequencies__Cut_Dataset(phenopy,selType='EEG Binned Frequencies'):
    """
        Cut sleepSign dataset of the form EEG Binned Frequencies
    """
    print selType
    dataContainer = phenopy.Dataset
    Groupdialog = CreateGroupsDlg(1,dataContainer.keys(),DataContainer=dataContainer,
                                  TypeList=[selType],parent=phenopy)
    if not Groupdialog.exec_():
        return
    datadict = Groupdialog.returnSelectedNames()
    datalist = datadict[datadict.keys()[0]]
    IsFirst = True
    for dataName in datalist:
        try:
            phenopy.lock.lockForRead()
            Dataset = copy(phenopy.Dataset.takeDataset(dataName))
            d0 = DT.date(Dataset.Timestamp[0].year, Dataset.Timestamp[0].month,
                         Dataset.Timestamp[0].day)
            d1 = DT.date(Dataset.Timestamp[-1].year, Dataset.Timestamp[-1].month,
                         Dataset.Timestamp[-1].day)
            N_Day = (d1 - d0).days + 1
            Days=[u'%s'%d for d in xrange(1,N_Day+2)]
            DaysValue = range(1,N_Day+2)
            if IsFirst:
                comboBox = [(u'Starting Day:', Days, DaysValue,0),
                            (u'Ending Day:', Days, DaysValue, len(Days)-1)]
                timeSpinBox = [None,('Starting Time:',0,0),
                             ('Ending Time',23,59),None]
            else:
                comboBox = [(u'Starting Day:', Days,DaysValue,dialog.ComboBox[0].currentIndex()),
                            (u'Ending Day:', Days, DaysValue, min(dialog.ComboBox[1].currentIndex(),len(Days)-1))]
                timeSpinBox = [None,('Starting Time:',dialog.HourSpinBox[1].value(),dialog.MinuteSpinBox[1].value()),
                             ('Ending Time',dialog.HourSpinBox[2].value(),dialog.MinuteSpinBox[2].value()),None]
            lineEdit = ['Dataset name:']
            dialog = inputDialog(dataName,comboBox,timeSpinBox,None,
                                 lineEdit,parent=phenopy)
            if not dialog.exec_():
                return
            stdOutput = dialog.createStdOutput()
            dayStart = stdOutput['Combo'][0]
            dayEnd = stdOutput['Combo'][1]
            if stdOutput['TimeSpinBox'][1][0] == 24:
                hour_end = DT.time(23, 59, 59)
            else:
                hour_end = DT.time(stdOutput['TimeSpinBox'][1][0],
                                   stdOutput['TimeSpinBox'][1][1],0)
            if stdOutput['TimeSpinBox'][0][0] == 24:
                hour_start = DT.time(23, 59, 59)
            else:
                hour_start = DT.time(stdOutput['TimeSpinBox'][0][0],
                                     stdOutput['TimeSpinBox'][0][1],0)
        
            date_0 = Dataset.Timestamp[0]
            date_0 = date_0 + DT.timedelta(dayStart - 1)
            date_0 = date_0.replace(hour=hour_start.hour,
                                    minute=hour_start.minute,
                                    second=hour_start.second)
            date_1 = copy(date_0)
            date_1 = date_1 + DT.timedelta(dayEnd - dayStart)
            date_1 = date_1.replace(hour=hour_end.hour, minute=hour_end.minute,
                                    second=hour_end.second)
            ind_0 = np.where(Dataset.Timestamp >= date_0)[0][0]
            ind_1 = np.where(Dataset.Timestamp <= date_1)[0][-1]
            Dataset.PowerSp = Dataset.PowerSp[ind_0:ind_1]
            Dataset.Timestamp = Dataset.Timestamp[ind_0:ind_1]
            Dataset.Stage = Dataset.Stage[ind_0:ind_1]
            message = 'Cutted Dataset %s'%dataName
            newName = stdOutput['LineEdit'][0]
            if newName:
                dataContainer.pop(newName)
            else:
                newName = copy(dataName)
            while newName in dataContainer.keys():
                newName = newName.split('.')[0] + '_Cut.csv'
                    
            data = Dataset_GUI(Dataset, newName,
                               Path=None,Types=dataContainer[dataName].Types,
                               Scaled=dataContainer[dataName].Scaled,
                               TimeStamps=dataContainer[dataName].TimeStamps)
            dataContainer.add(data)
            phenopy.listWidgetRight.addItem(message)
        except Exception, e:
            message = 'Unable to cut dataset with the exception: %s'%e.message
            phenopy.listWidgetRight.addItem(message)
        finally:
            phenopy.lock.unlock()
    
def EEG_Full_Power_Spectrum__Cut_Dataset(phenopy):
    """
        Cut sleepSign dataset of the form EEG Binned Frequencies
    """
    EEG_Binned_Frequencies__Cut_Dataset(phenopy,selType='EEG Full Power Spectrum')

def TSE__Select_Interval(phenopy, selType='TSE'):
    """
        Select a subset of hours from TSE data across the whole experiment
    """
    dataContainer = phenopy.Dataset
    Groupdialog = CreateGroupsDlg(1,dataContainer.keys(),DataContainer=dataContainer,
                                  TypeList=[selType],parent=phenopy)
    if not Groupdialog.exec_():
        return
    datadict = Groupdialog.returnSelectedNames()
    datalist = datadict[datadict.keys()[0]]
    comboBox=[(u'Keep time interval:', ['Inside','Outside'],['Inside','Outside'], 0)]
    timeSpinBox = [('Day Time 0:', 0, 0),('Day Time 1:', 24, 0),None]
    Datalist=u''
    for dataName in datalist:
        Datalist+=unicode(dataName)+u'<br>'
    Datalist=Datalist[:-4]
    dialog = inputDialog(Datalist,comboBox,timeSpinBox,None,NewDataLineEdit=True,
                                 DatasetNum=Groupdialog.groupListWidget[0].count(),
                                 parent=phenopy)
    if not dialog.exec_():
        return
                
    secStart = dialog.HourSpinBox[0].value()*3600 + dialog.MinuteSpinbox[0].value()*60
    secEnd = dialog.HourSpinBox[1].value()*3600 + dialog.MinuteSpinbox[1].value()*60
    InOrOut = dialog.ComboBox[0].currentText()
    newName=None
    if len(dialog.NewDataLineEdit.text())>0:
        newName = dialog.NewDataLineEdit.text().split(';')
                                    
    if InOrOut==u'Inside':
        InOrOut = 'In'
    else:
        InOrOut = 'Out'

    for DataLabel in datalist:
        try:
            phenopy.lock.lockForRead()
            
            Dataset = copy(phenopy.Dataset.takeDataset(DataLabel))
            Start_exp,Start_Time,End_Time = Time_Details_GUI(Dataset,
                                            phenopy.Dataset[DataLabel].TimeStamps)
            Types = phenopy.Dataset.dataType(DataLabel)
            Dataset = Select_Interval_GUI(Dataset, secStart, secEnd,
                                          phenopy.Dataset[DataLabel].TimeStamps,
                                          InOrOut=InOrOut)
            Scaled = phenopy.Dataset.scaled(DataLabel)
            message = 'Selected interval from Dataset %s'%DataLabel
            if newName:
                phenopy.Dataset.pop(newName)
            else:
                newName = copy(DataLabel)
            while newName in dataContainer.keys():
                newName = newName.split('.')[0] + '_SelectedInterval.csv' 
            data = Dataset_GUI(Dataset,newName,
                               Path=None,Types=Types, Scaled=Scaled)
            phenopy.Dataset.add(data)
            phenopy.listWidgetRight.addItem(message)
        except IndexError, e:
            message = 'Failed to select interval from data %s\nwith the exception %s'%(DataLabel,e.message)
            phenopy.listWidgetRight.addItem(message)
        finally:
            phenopy.lock.unlock()
def AM_Microsystems__Select_Interval(phenopy):
    """
        Select a subset of hours from AM-Microsystems data across the whole experiment
    """
    TSE__Select_Interval(phenopy, selType='TSE')
        
def create_laucher():
    fh = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'editFunctions.py'),'U')
    script = 'import numpy as np\nfrom editFunctions import *\n\ndef launchEditFun(phenopy,funName):\n'
    line = fh.readline()
    
    while line:
        if line.startswith(('def ','def\t')):
            funName = (line[3:].replace(' ','')).replace('\t','')
            funName = funName.split('(')[0]
            if funName == 'main' or funName == 'create_laucher':
                line = fh.readline()
                continue
            script += '\tif funName == \'%s\':\n\t\treturn %s(phenopy)\n\n'%(funName,funName)
        line = fh.readline()
    fh.close()
    edt_dir = os.path.dirname(os.path.realpath(__file__))
    fh = open(os.path.join(edt_dir,'editLauncher.py'),'w')
    fh.write(script)
    fh.close()

create_laucher()


def main():
    app=QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()