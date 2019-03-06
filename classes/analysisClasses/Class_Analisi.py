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

from inputDlgCreator import inputDlgCreator

def createComboTuple(string, label, intTuple,listValues, value):
    comboList = ((('%d ' + '%s;'%string)*len(intTuple))%intTuple).split(';')[:-1]
    return (label,comboList,listValues,value)

class inputDict_Creator(object):
    """
        Classe che contiene dizionario con input. Prima chiave è il numero 
        di dialoghi di input che un'analisi richiede, la seconda chiave è il
        tipo di QWidget che deve contenere l'inputDialog. Ha un metodo
        per ritornare gli input date le due chiavi
    """
    def __init__(self):
        self.refresh()
    def refresh(self):
        self.inputDict = {}
        self._input_ind = 0
        self.inputDict[0]={}
        
    def addNewDlg(self):
        self._input_ind += 1
        self.inputDict[self._input_ind]={}
    def addNewInput(self,inputName,inputData):
        self.inputDict[self._input_ind][inputName] = inputData
    def returnListDlg(self):
        return list(self.inputDict.keys())
    def returnInput(self, keyDlg, keyInput):
        if keyInput in list(self.inputDict[keyDlg].keys()):
            return self.inputDict[keyDlg][keyInput]
        else:
            return None
       
class Analysis_Single_GUI(object):
    """
        Questa classe crea un oggetto input creator a seconda dell'analisi.
        Siccome è stata creata prima della standardizzazione delle analisi
        crea gli input delle funzioni "vecchie" in un modo, e invece utilizza
        lo standard di inputDlgCreator se la funzione è nuova
    """
    def __init__(self, analysisName, parent = None):
        self.inputCreator = inputDict_Creator()
        if not analysisName is None:
            self.getInput(analysisName)
        
    def getInput(self,analysisName):
        self.inputCreator.refresh()
        if analysisName == 'Actogram':
            comboInput = [createComboTuple('min','Time binning:',\
                (10,15,20,30,60),[10,15,20,30,60],1)]
            Hours = []
            for h in range(24):
                Hours += ['%d:00'%h]
            comboInput += [('Light phase start:', Hours, list(range(24)),7)]
            self.inputCreator.addNewInput('Combo', comboInput)
            Range = [('Periodicity range:',(0.5,100),22,27)]
            self.inputCreator.addNewInput('Range', Range)
            self.inputCreator.addNewInput('SpinBox', [('Period linspace num:',
                                                       (10,10000),100)])
            self.inputCreator.addNewInput('SavingDetails',True)
            
            
        elif analysisName in ['Error_Rate', 'AIT']:
#            doubleInput = [('Trial duration (sec):', (0,100000), 30)]
#            self.inputCreator.addNewInput('DoubleSpinBox', doubleInput)
#            listCombo = [u'Daily means', u'Hour by hour rate']
#            comboInput = [(u'Output format:', listCombo, listCombo, 0)]
#            self.inputCreator.addNewInput('Combo', comboInput)
#            self.inputCreator.addNewDlg()
            Hours, Hours1 = [], []
            valueHours = list(range(24))
            valueHours1 = list(range(25))
            labels = (('%d min;'*3)%(10,15,30) + ('%d h;'*6)%(1,2,3,4,6,12)).split(';')[:-1]
            value_Labels = [600, 900, 1800, 3600, 7200, 10800, 14400,\
                              21600, 43200]
            for h in range(24):
                Hours += ['%d:00'%h]
                Hours1 += ['%d h'%h]
            Hours1 += ['24 h']
            comboBox=[('Time binning:', labels, value_Labels, 3),
                      ('Dark Phase Start:', Hours, valueHours, 20),
                      ('Dark Phase Duration:', Hours1, valueHours1, 12)]
            self.inputCreator.addNewInput('Combo', comboBox)
            if analysisName == 'Error_Rate':              
                doubleList = [('Trial duration (sec):', (1,100000), 30)]
                self.inputCreator.addNewInput('DoubleSpinBox',doubleList)
            self.inputCreator.addNewInput('SavingDetails',True)
            
        elif analysisName in ['Peak_Procedure', 'Raster_Plot']:
            comboBox = [('Trial type:',['All','Probe left','Probe right'],
                         ['All','Probe Left','Probe Right'],0),
                        ('Print location:', ['Both', 'Left','Right'],
                         ['Both', 'Left','Right'], 0),
                         ]
            if analysisName == 'Peak_Procedure':
                comboBox = [('Trial type:',['All','Probe left','Probe right'],
                         ['All','Probe Left','Probe Right'],0),
                        ('Print location:', ['Left','Right'],
                         ['Left','Right'], 0),
                         ]
                doubleList = [('Light signal:', (0, 1000), 3),
                              ('Trial duration (sec):', (15,10000), 30)]
                
            else:
                doubleList = [('Trial duration (sec):', (15,100000), 30)]
            self.inputCreator.addNewInput('DoubleSpinBox',doubleList)

            self.inputCreator.addNewInput('Combo', comboBox)         
            timeSpinBox=[None,('Start time:',0,0),('End time',24,0),None]
            self.inputCreator.addNewInput('TimeSpinBox',timeSpinBox)
            self.inputCreator.addNewInput('SavingDetails',True)

        else:
            try:
                dictInput = inputDlgCreator(analysisName)
                for key in list(dictInput.keys()):
                    self.inputCreator.addNewInput(key,dictInput[key])
                    self.inputCreator.addNewInput('SavingDetails',True)
            except:
                raise KeyError('No single subject analysis named %s'%analysisName)    

class Analysis_Group_GUI(object):
    """ Questa classe crea un oggetto input creator a seconda dell'analisi.
        Utilizza lo standard di inputDlgCreator che per ogni analisi ritorna un
        dizionario
    """
    def __init__(self, analysisName, group_list=[], parent=None):
        self.inputCreator = inputDict_Creator()
        if not analysisName is None:
            self.getInput(analysisName, group_list)
        
    def getInput(self,analysisName, group_list):
        print('Gr List:',group_list)
        self.inputCreator.refresh()
        try:
            dictInput = inputDlgCreator(analysisName, group_list)
            for key in list(dictInput.keys()):
                self.inputCreator.addNewInput(key,dictInput[key])
                self.inputCreator.addNewInput('SavingDetails',True)
        except:
            raise KeyError('No single subject analysis named %s'%analysisName)    

if __name__ == '__main__':
    an=Analysis_Single_GUI('AIT').inputCreator
    print('list dlg: ', an.returnListDlg())
    print('combo: ', an.returnInput(0,'Combo'))
    print('DoubleSpinBox: ',an.returnInput(0,'DoubleSpinBox'))
    if an.returnListDlg() ==  [0,1]:
        print('combo: ', an.returnInput(1,'Combo'))
    anGr=Analysis_Group_GUI('Group_Error_Rate').inputCreator
    print(anGr.inputDict)