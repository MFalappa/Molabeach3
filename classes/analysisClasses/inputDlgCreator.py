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
def inputDlgCreator(analysisName,group_list=[]):
    dictInput = {}
#==============================================================================
#     Example of input dlg
#==============================================================================
   
    if analysisName == 'Power_Density':
        dictInput['Combo'] = [('Statistical index:',['Mean','Median'],['Mean','Median'],0),
                              ('Color wake:',['Blue','Green','Red','Cyan','Magenta','Yellow','Black','White'],['b','g','r','c','m','y','k','w'],0),
                              ('Color rem:',['Blue','Green','Red','Cyan','Magenta','Yellow','Black','White'],['b','g','r','c','m','y','k','w'],1),
                              ('Color nrem:',['Blue','Green','Red','Cyan','Magenta','Yellow','Black','White'],['b','g','r','c','m','y','k','w'],2)]
        dictInput['SpinBox'] = [('Title size:',(5,50),20),('Line width:',(0.2,10),2),('Legend size:',(5,50),15),('Axis label size:',(5,50),15),('Suptitle size',(5,100),25)]
        dictInput['DoubleSpinBox'] = [('Highest frequency:',(0.5,200),20)]
        return dictInput
    if analysisName == 'Group_Error_Rate':
        dictInput['Combo'] = [('Dark phase start:',
            ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00',
            '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00',
            '22:00', '23:00'],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
            14, 15, 16, 17, 18, 19, 20, 21, 22, 23],20),
            ('Dark phase duration (hours):',['0',' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',
            ' 9',' 10',' 11',' 12',' 13',' 14',' 15',' 16',' 17',' 18',' 19',
            ' 20',' 21',' 22',' 23',' 24'],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],12),
            ('Statistical index:',['Mean','Median'],['Mean','Median'],0),
            ('Time binning:',['10 min', '15 min', '20 min', '30 min', '1 h',
            '2 h', '3 h', '6 h', '12 h'],[600,900,1200,1800,3600,7200,
            10800,21600,43200],4),('Type',['Single subject','Group'],[0,1],1)]
        return dictInput
    if analysisName == 'Sleep_Time_Course':
#        print('Enterd sleep time course')
        dictInput['SpinBox'] = [('Time binning:',(1,24),1),
            ('Epoch duration:',(1,60),4),('Tick number:',(1,100),10),
            ('Dark phase start:',(0,23),20)]
#        print('spin ok')
        
        dictInput['Combo'] = [('Epoch type:',['Sleep','Rem','NRem','Wake'],
                  [[2,3],[2],[3],[1]],0),
                   ('Statistical index:',['Mean','Median'],['Mean','Median'],0),
                   ('Mean or total per time bin:',['Mean','Total'],
                    ['Mean','Total'], 1)]
        return dictInput
    if analysisName == 'Linear_Discriminant_Analysis':
        dictInput['SpinBox'] = [('Dark phase duration (hours):',(0,24),12),
                                ('Marker size:',(2,100),12)]
        dictInput['Combo'] = [('Dark start (behaviour exp.):',
                                ['0:00', '1:00', '2:00', '3:00', '4:00',
                                '5:00', '6:00', '7:00', '8:00',
                                '9:00', '10:00', '11:00', '12:00',
                                '13:00', '14:00', '15:00', '16:00',
                                '17:00', '18:00', '19:00', '20:00',
                                '21:00', '22:00', '23:00'],[0, 1, 2, 3, 4, 5,
                                6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                                19, 20, 21, 22, 23],20),
                                ('Dark start (EEG recording exp.):',['0:00',
                                '1:00', '2:00', '3:00', '4:00', '5:00', '6:00',
                                '7:00', '8:00', '9:00', '10:00', '11:00',
                                '12:00', '13:00', '14:00', '15:00', '16:00',
                                '17:00', '18:00', '19:00', '20:00', '21:00',
                                '22:00', '23:00'],[0, 1, 2, 3, 4, 5, 6, 7, 8,
                                9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                20, 21, 22, 23],20)]
        return dictInput
    
    if analysisName == 'Sleep_cycles':
        dictInput['Combo'] = [('Epoch type:',['Sleep','Rem','NRem','Wake'],
                  [[2,3],[2],[3],[1]],0),
                   ('Statistical index:',['Mean','Median'],['Mean','Median'],0),
                   ('Mean or total per time bin:',['Mean','Total'],
                    ['Mean','Total'], 1)]
                   
                   
        dictInput['Combo'] = [('Binning:',['1 min', '2 min', '3 min', '4 min','5 min'],
                  [1,2,3,4,5],2)]
        return dictInput
    if analysisName == 'Attentional_analysis':
        dictInput['Combo'] = [
                ('Type:',['Reaction time','Anticipation','Food','Error Rate'],
                  [[1],[2],[3],[4]],0),
                 ('Time binning:',['1 h','2 h', '3 h','6 h','12 h'],
                  [1,2,3,6,12],3),
            ('Dark phase start:',['0:00', '1:00', '2:00', '3:00', '4:00', '5:00',
                                  '6:00', '7:00','8:00', '9:00', '10:00', '11:00',
                                  '12:00', '13:00', '14:00','15:00', '16:00', 
                                  '17:00', '18:00', '19:00', '20:00', '21:00','22:00','23:00'],
                  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14, 15, 16, 17, 
                   18, 19, 20, 21, 22, 23],20),
            ('Dark phase duration (hours):',['0',' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',
            ' 9',' 10',' 11',' 12',' 13',' 14',' 15',' 16',' 17',' 18',' 19',
            ' 20',' 21',' 22',' 23',' 24'],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],12)]
        return dictInput
        
    if analysisName == 'LDA':
        dictInput['Combo'] = [('Dark start hour:',['0',' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9',' 10',' 11',' 12',' 13',' 14',' 15',' 16',' 17',' 18',' 19',' 20',' 21',' 22',' 23'],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],20),('Dark phase duration (hrs):',['0',' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9',' 10',' 11',' 12',' 13',' 14',' 15',' 16',' 17',' 18',' 19',' 20',' 21',' 22',' 23'],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],12),('Cognitive score:',['Error Rate','Reaction Time'],['Error Rate','Reaction Time'],0),('Sleep score:',['Sleep Total','NREM Total','REM Total','Wake Total'],['Sleep Total','NREM Total','REM Total','Wake Total'],0)]
        return dictInput
    if analysisName == 'Switch_Latency':
        dictInput['Range'] = [('Mean switch latency range (sec):',(0,400),1.000000,11.000000),('Coefficient of variation for switch latency:',(0.001,1.0),0.050000,0.500000)]
        dictInput['Combo'] = [('Dark start hour:',['0',' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9',' 10',' 11',' 12',' 13',' 14',' 15',' 16',' 17',' 18',' 19',' 20',' 21',' 22',' 23'],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],20),('Dark phase duration (hrs):',['0',' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9',' 10',' 11',' 12',' 13',' 14',' 15',' 16',' 17',' 18',' 19',' 20',' 21',' 22',' 23'],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],12),('Trail type:',["Long Probe","Long Reward","Long"],["Long_Probe","Long_reward","Long"],2),('Long location side:',["Left","Right","Mixed"],["l","r","m"],0)]
        dictInput['DoubleSpinBox'] = [('Duration of a trial (sec):',(2,100000),30.000000),('Short signal duration (sec):',(1,200),3.000000),('Long signal duration (sec):',(2,200),6.000000),('Probability of short trials:',(0,1),0.500000),('Conditional probability of short probe:',(0,1),0.200000),('Conditional probability of long probe:',(0,1),0.200000)]
        return dictInput
    if analysisName == 'delta_rebound':
        dictInput['PhaseSel'] = []
        dictInput['Combo'] = [('Time binning:',['10 min', '20 min','30 min','1 h', '2 h', '3 h', '6 h'],[600,1200,1800,3600,7200,10800,21600],3),('Frequency band:',["Delta","Theta"],[0,1],0),('Sleep stage:',["NRem","Rem","Wake","All"],["NR","R","W","All"],0)]
        return dictInput
    if analysisName == 'spikeStatistics':
        dictInput['DoubleSpinBox'] = [('Number of ISI histogram bars:',(10,999999),100.000000),('Binning in seconds for firing rate computing:',(0.1,999999),10.000000)]
        return dictInput
    if analysisName == 'emg_normalized':
        dictInput['LineEdit'] = ['Percentile to compute (separated by ,):']
        
        return dictInput
        
        
        
