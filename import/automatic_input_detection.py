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
## TODO
## in check_analysis_function
## controllo che DataDict sia un doppio dizionario
## controllo che le prime chiavi di info siano tutte e sole le seconde di DataDict
## controllo che le seconde chiavi di info siano gli attributi di Dataset_GUI 

import os

def return_input_count(path):
    list_std_input = ['Combo','SpinBox','DoubleSpinBox','LineEdit',
                      'TimeSpinBox','Range','PhaseSel','TimeRange']
    dict_input = {}
    for key in list_std_input:
        dict_input[key] = 0
    num_lines = sum(1 for line in open(path,'U'))
    fh = open(path, 'U')
    i = 0
    flag_first = True
    while i < num_lines:
        line = fh.readline()
        i +=1
        while flag_first and i < num_lines and not (line.startswith(('def ','def\t'))):
            line = fh.readline()
            i +=1
        
        flag_first = False
        
        if line.lstrip().startswith('return '):
            break
        line_split = line.split('Input')
        if len(line_split) is 1:
            continue
        
        
#        elif line_split[0][-1] in [' ','\t']:
#            continue
#        
        if '\'' in line_split[1]:
            input_name = line_split[1].split('\'')[1].split('\'')[0]
        elif  '\"' in line_split[1]:
            input_name = line_split[1].split('\"')[1].split('\"')[0]
        else:
            continue
        if input_name not in list_std_input:
            raise NameError, 'Input must be choosen between (%s)'%(', '.join(list_std_input))
        else:
            dict_input[input_name] += 1
    fh.close()
    return dict_input
    
def check_analysis_function(path):
    check_data = False
    check_input = False
    check_data_group = False
    check_timestamps = False
    check_lock = False
    count_myinput = 0
    num_data_def = 0
    num_dplot_def = 0
    num_info_def = 0
    def_num = 0
    num_redef_info_key = {}
    num_dictPlot_key_def = {}
    num_DataDict_key_def = {}
    dict_inputs = {}
    key_datadict = []
    key_info = []
    infotypes_set = False
    num_lines = sum(1 for line in open(path,'U'))
    fh = open(path, 'U')
    i = 0
    flag_first = True
    while i < num_lines:
        line = fh.readline()
        i +=1
        while flag_first and i < num_lines and not (line.startswith(('def ','def\t'))):
            line = fh.readline()
            i +=1
        flag_first = False
        line_split = line.split('myInput')
        if line.startswith(('def ','def\t')):
            def_num += 1
            if def_num > 1:
                return False, 'Error in line %d. Too many function definition'%i
            if (not line_split[0].endswith('*')) or len(line_split)!= 2:
                return False, 'Error in line %d. Analysis function input must be \"*myInput\"'%i
            else:
                continue
        elif len(line_split) is 2:
            var = line_split[0].replace('\t','')
            var = var.replace(' ','')
            index = line_split[1].replace('\t','')
            index = index.replace(' ','')
            index = index.replace('\n','')
            if index == '[0]' and var != 'Datas=':
                return False, 'Error in line %d. myInput[0] must be assigned to Datas'%i
            elif index == '[0]' and var == 'Datas=':
                check_data = True
                count_myinput += 1
            elif index == '[1]' and var != 'Input=':
                return False, 'Error in line %d. myInput[1] must be assigned to Input'%i
            elif index == '[1]' and var == 'Input=':
                check_input = True
                count_myinput += 1
            elif index == '[2]' and var != 'DataGroup=':
                return False, 'Error in line %d. myInput[2] must be assigned to DataGroup'%i
            elif index == '[2]' and var == 'DataGroup=':
                check_data_group = True
                count_myinput += 1
            elif index == '[3]' and var != 'TimeStamps=':
                return False, 'Error in line %d. myInput[3] must be assigned to TimeStamps'%i
            elif index == '[3]' and var == 'TimeStamps=':
                check_timestamps = True
                count_myinput += 1
            elif index == '[4]' and var != 'lock=':
                return False, 'Error in line %d. myInput[4] must be assigned to lock'%i
            elif index == '[4]' and var == 'lock=':
                check_lock = True
                count_myinput += 1
            elif index == '[5]' and var != 'pairedGroups=':
                return False, 'Error in line %d. myInput[5] must be assigned to pairedGroups'%i
            elif index == '[6]' and var != 'Other=':
                return False, 'Error in line %d. myInput[5] must be assigned to Other'%i
            elif index[0] == '[' and index[-1]== ']' and index[1:-1].isdigit():
                continue
            else:
                return False, 'Error in line %d. line \"%s\" not understood'%(i,line)
        elif 'DataDict' in line:
            line_split = line.split('DataDict')
            no_space_after = line_split[1].replace(' ','')
            no_space_after = no_space_after.replace('\t','')
            no_space_after = no_space_after.replace('\n','')
            no_space_before = line_split[0].replace(' ','')
            no_space_before = no_space_before.replace('\t','')
            if no_space_before == '' and no_space_after == '={}':
                # controllo che datadict sia def come empty dict e una sola volta
                num_data_def += 1
                if num_data_def > 1:
                    return False, 'Error in line %d. Multiple definition of "DataDict" dictionary'%i
                continue
            if no_space_before == '' and  no_space_after.count('[') is 1:
                key1 = no_space_after.split(']')[0].split('[')[1]
                key1 = key1.rstrip('\'').lstrip('\'')
                key1 = key1.rstrip('\"').lstrip('\"')
                if ']=' in  no_space_after:
                    if key1 in num_DataDict_key_def.keys():
                        return False, 'Error in line %d. Multiple definition of DataDict[%s]'%(i,key1)
                    else:
                        num_DataDict_key_def[key1] = 0
                # controllo che datadict[key] sia def come un empty dict
                if no_space_after.split('=')[1] != '{}':
                    return False,'Error in line %d. DataDict[key] must be initialized as an empty dictionary'%i
            
            if no_space_before == '' and  no_space_after.count('[') is 2:
                # estraggo seconde chiavi di datadict
                key2 = line_split[1].split('[')[2].split(']')[0]
                key2 = key2.rstrip(' ').lstrip(' ').rstrip('\t').lstrip('\t').replace('\'','').replace('\"','')
                if not key2 in key_datadict:
                    key_datadict += [key2]
            if no_space_before == '' and not '[' in no_space_after:
                # controllo che Datadict sia sempre richiamato con una chiave
                return False,'Error in line %d. DataDict must be accessed with a key.'%i
            if no_space_before == 'return' and no_space_after != ',dictPlot,info':
                # controllo che ritorni gli output nell'ordine giusto
                return False, 'Error in line %d. Function must return \"DataDict,dictPlot,info\" in the correct order'%i
        elif 'dictPlot' in line:
            line_split = line.split('dictPlot')
            no_space_after = line_split[1].replace(' ','')
            no_space_after = no_space_after.replace('\t','')
            no_space_after = no_space_after.replace('\n','')
            no_space_before = line_split[0].replace(' ','')
            no_space_before = no_space_before.replace('\t','')
            if no_space_before == '' and no_space_after == '={}':
                num_dplot_def += 1
                if num_dplot_def > 1:
                    return False, 'Error in line %d. Multiple definition of "dictPlot" dictionary'%i
                continue
            if no_space_before == '' and not '[' in no_space_after:
                return False,'Error in line %d. dictPlot must be accessed with a key.'%i
            if no_space_before == '' and '[' in no_space_after:
                after = line_split[1]
                key1 = after.split(']')[0].split('[')[1]
                key1 = key1.lstrip().rstrip()
                key1 = key1.rstrip('\"')
                key1 = key1.lstrip('\'')
                key1 = key1.lstrip('\"')
                key1 = key1.rstrip('\'')
                if not key1 in dict_inputs.keys():
                    dict_inputs[key1] = []
                    num_dictPlot_key_def[key1] = 0
                if len(no_space_after.split(']')) is 3:
                    key2 = after.split(']')[-2].split('[')[1]
                    key2 = key2.lstrip().rstrip()
                    key2 = key2.rstrip('\'')
                    key2 = key2.rstrip('\"')
                    key2 = key2.lstrip('\'')
                    key2 = key2.lstrip('\"')
                    if not key2 in dict_inputs.keys():
                        dict_inputs[key1] += [key2]
                        
                elif no_space_after.count('[') is 1 and '={}' in no_space_after:
                    num_dictPlot_key_def[key1] += 1
                    if num_dictPlot_key_def[key1] > 1:
                        return False, 'Error in line %d. Multiple definition of dictPlot[\"%s\"]'%(i,key1)
                    
                    
        elif 'info' in line:
            line_split = line.split('info')
            no_space_after = line_split[1].replace(' ','')
            no_space_after = no_space_after.replace('\t','')
            no_space_after = no_space_after.replace('\n','')
            no_space_before = line_split[0].replace(' ','')
            no_space_before = no_space_before.replace('\t','')
            if no_space_before == '' and no_space_after == '={}':
                num_info_def += 1
                if num_info_def > 1:
                    return False, 'Error in line %d. Multiple definition of "info" dictionary'%i
                continue
            if no_space_before == '' and no_space_after.count('[') is 1:
                # controllo che datadict[key] sia def come un empty dict
                if no_space_after.split('=')[1] != '{}':
                    return False,'Error in line %d. info[key] must be initialized as an empty dictionary'%i
                else:
                    # colleziono tutte le chiavi di primo livello di info
                    key1 = line_split[1].split('[')[1].split(']')[0]
                    key1 = key1.rstrip('\t').rstrip(' ').lstrip('\t').lstrip(' ').replace('\'','').replace('\"','')
                    if key1 not in key_info:
                        key_info += [key1]
                        num_redef_info_key[key1] = 0
                    if '{}' in no_space_after:
                        num_redef_info_key[key1] += 1
                        if num_redef_info_key[key1] > 1:
                            return False,'Error in line %d. Multiple definition of info[%s] as an empty dictionary'%(i,key1)
            if no_space_before == '' and no_space_after.count('[') >= 2:
                key2 =  line_split[1].split('[')[2].split(']')[0]
                key2 = key2.rstrip('\t').rstrip(' ').lstrip('\t').lstrip(' ').replace('\'','').replace('\"','')
                if not key2 in ['Types', 'Factor']:
                    return False, 'Error in line %d. info[key].keys() must be between: [%s]'%(i,','.join(['Types', 'Factor']))
                elif key2 == 'Types' and no_space_after.count('[') == 3:
                    infotypes_set = True
                elif no_space_after.count('[') > 3:
                    return False, 'Error in line %d. info[key][\'Types\'] must be a list.'%i
            if no_space_before == '' and not '[' in no_space_after:
                return False,'Error in line %d. info must be accessed with a key.'%i
    if not check_data:
        return False, 'Error. Datas not assigned from myInput'
    if not check_input:
        return False, 'Error. Input not assigned from myInput'
    if not check_data_group:
        return False, 'Error. DataGroup not assigned from myInput'
    if not check_timestamps:
        return False, 'Error. TimeStamps not assigned from myInput'
    if not check_lock:
        return False, 'Error. lock not assigned from myInput'
    if num_data_def is 0:
        return False, 'Missing DataDict definition'
    if num_dplot_def is 0:
        return False, 'Missing dictPlot definition'
    if num_info_def is 0:
        return False, 'Missing info definition'
    for key in dict_inputs.keys():
        if len(dict_inputs[key]) is 0:
            return False, 'dictPlot must be a dicitonary that contains other non empty dictionaries'
    for key in  key_info:
        if not key in key_datadict:
            return False,'Error. info keys must be choosen between DataDict[key].keys()'
    if len(key_info) != len(key_datadict):
        return False,'Error. info keys must contain the union of DataDict[K].keys(), for K in DataDict.keys()'
    if not infotypes_set:
        return False, 'Error. info[key][\'Types\'] must be set for all output data'
    return True, 'Analysis function checked and ok!', dict_inputs

def check_plot_function(path,dict_inputs):
    i = 0
    def_num = 0
    num_myInput_used = 0
    num_lines = sum(1 for line in open(path,'U'))
    fh = open(path, 'U')
    flag_first = True
    while i < num_lines:
        line = fh.readline()
        i +=1
        while flag_first and i < num_lines and not (line.startswith(('def ','def\t'))):
            line = fh.readline()
            i +=1
        flag_first = False
        if line.startswith(('def ','def\t')):
            def_num += 1
            if def_num > 1:
                return False, 'Error in line %d. Too many function definition'%i
            line_split = line.split('myInput')
            if (not line_split[0].endswith('*')) or len(line_split)!= 2:
                return False, 'Error in line %d. Analysis function input must be \"*myInput\"'%i
            else:
                continue
        elif 'myInput' in line:
            after_str = line.split('myInput')[1]
            if after_str.count('[') == 3 and '].' in after_str:
                continue
            elif after_str.count('[') < 3 or after_str.count('[') < 3:
                return False, 'Error in line %d. myInput accessed using three arguments, an index and two dictionary keys'%i
            index = after_str.split(']')[0]
            index = index.split('[')[1]
            index = index.replace(' ','')
            index = index.replace('\t','')
            if index != '0':
                return False, 'Error in line %d. Input for plots must have index 0'%i
            key1 = after_str.split(']')[1].split('[')[1]
            key1 = key1.lstrip(' ')
            key1 = key1.lstrip('\t')
            key1 = key1.rstrip(' ')
            key1 = key1.rstrip('\t')
            key1 = key1.rstrip('\'')
            key1 = key1.rstrip('\"')
            key1 = key1.lstrip('\'')
            key1 = key1.lstrip('\"')
            if not key1  in dict_inputs.keys():
                print( 'Allowed keys:', dict_inputs.keys())
                return False,'Error in line %d. %s is not one of the keys of myInput detected from the analysis function'%(i,key1)
            key2 = after_str.split(']')[2].split('[')[1]
            key2 = key2.lstrip(' ')
            key2 = key2.lstrip('\t')
            key2 = key2.rstrip(' ')
            key2 = key2.rstrip('\t')
            key2 = key2.rstrip('\'')
            key2 = key2.rstrip('\"')
            key2 = key2.lstrip('\'')
            key2 = key2.lstrip('\"')
            if not key2 in dict_inputs[key1]:
                return False, 'Error in line %d. %s must be a key for myInput[%s]'%(i,key2,key1)
        elif 'figDict' in line:
            line_split = line.split('figDict')
            before = line_split[0].replace(' ','')
            before = before.replace('\t','')
            if before == '':
                if '={' in line_split[1].replace(' ','').replace('\t',''):
                    list_plt_keys = []
                    template = '={'
                    after = line_split[1].rstrip(' ').rstrip('\t').lstrip(' ').lstrip('\t')
                    i_ddot = after.find(':',0)
                    while i_ddot >= 0:
                        if after[i_ddot-1] == '\'':
                            key = after[after[:i_ddot-1].rfind('\''):i_ddot]
                        elif after[i_ddot-1] == '\"':
                            key = after[after[:i_ddot-1].rfind('\"'):i_ddot]
                        else:
                            i_ddot = after.find(':',i_ddot+1)
                            continue
                        template += key + ':{},'
                        list_plt_keys += [key[1:-1]]
                        i_ddot = after.find(':',i_ddot+1)
                    template = template[:-1]+'}'
                    if  template.replace(' ','').replace('\t','') != after.replace(' ','').replace('\t','').replace('\n',''):
                        return False, 'Error in line %d. figDict must be initialized in one line as a dictionary containing empty dictionaries'%i,template,after
                else:
                    after = line_split[1].rstrip(' ').rstrip('\t').lstrip(' ').lstrip('\t')
                    after = after.split('=')[0]
                    count = after.count('[')
                    if count != 2:
                        return False, 'Error in line %d. two keys are needed for assign a figure to dictPlot'%i
                    key1 = after.split('[')[1].split(']')[0].rstrip(' ').rstrip('\t').lstrip(' ').lstrip('\t')
                    if not key1[1:-1] in list_plt_keys:
                        return False, 'Error in line %d. \"%s\" must be a figDict key'%(i,key1[1:-1])
                    else:
                        num_myInput_used += 1
            elif 'return' in before:
                after = line.split('return')[1].replace(' ','').replace('\t','').replace('\n','')
                if after != 'figDict':
                    return False, 'Error in line %d. Plot function must return figDict'%i
    if  num_myInput_used is 0:
        return False, 'Error. Empty figDict output detected'
    
    return True, 'Plotting function checked, ok.'
if __name__ == '__main__':
    path = 'C:\Users\TucciLab\Documents\Software_Develompment\Phenopy\New_Analysis_Gui\Program upload\\TEST_tmp.py'
    res = check_analysis_function(path)
    inp = return_input_count(path)
#    print res
    print inp
    pathplt = 'C:\Users\TucciLab\Documents\Software_Develompment\Phenopy\New_Analysis_Gui\Program upload\\TEST_plt.py'
    if res[0]:
        res2=check_plot_function(pathplt,res[2])
        print res2
    