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
import numpy as np
from Parser import parsing_Funct
import re
NO_INPUT_COMMANDS = ['START_TRIAL','END_TRIAL',
'LOOP_LOCAL_TRIAL','END_LOOP_LOCAL_TRIAL' ,'END_LOCAL_TRIAL','BLOCK_ELSE_IF',
'START_TRIAL_TIMER','RESET_TRIGGER','RGB_LEFT_OFF',
'RGB_MID_OFF','RGB_RIGHT_OFF','NOISE_LEFT_ON','NOISE_LEFT_OFF',
'NOISE_MID_ON','NOISE_MID_OFF','NOISE_RIGHT_ON','NOISE_RIGHT_OFF',
'EVENT_POKE_LEFT','EVENT_POKE_MID','EVENT_POKE_RIGHT','EVENT_TRIGGER_LEFT',
'EVENT_TRIGGER_MID','EVENT_TRIGGER_RIGHT',
'LOG_ITI_END','IS_RANDOM_MC',
'IS_TRIGGER_LEFT','IS_TRIGGER_MID','IS_TRIGGER_RIGHT','IS_PRESENCE_LEFT',
'IS_PRESENCE_MID','IS_PRESENCE_RIGHT','IS_LIGHT_LEFT','IS_LIGHT_MID',
'IS_LIGHT_RIGHT',
'IS_TIMEOUT_REACHED','RELEASE_PELLET_LEFT',
'RELEASE_PELLET_RIGHT','DUMMY_TEST','END_BLOCK_IF']

TWO_INPUT_COMMANDS = ['IS_COUNTER_GREATER','IS_COUNTER_LESSER',
                      'IS_COUNTER_EQUAL','COUNTER_INIT','ACTION_TTL']

ONE_INPUT_COMMANDS = ['RGB_LEFT_ON','RGB_MID_ON','RGB_RIGHT_ON','FIXED_DELAY',
                      'FIXED_DELAY_ITI','RANDOM_DELAY_ITI','COUNTER_INC','IS_RANDOM_MC_STEP']
def INT_INPUT_CHECK(inputs):
    for i in inputs:
        if not re.match('^[0-9]+$',i):
            return False, 'Non integer Input'
    return True, 'No errors'
    
def CO_set_MEAN_DISTRIBUTION_CHECK(inputs):
    if len(inputs) > 1:
        return False, 'Too many inputs'
    i = int(inputs[0])
    if i > 65535 or i < 0:
        return False, 'Input range between 0 and 65535'
    return True, 'No errors'
    
def CO_set_TRIAL_MAX_NUMBER_CHECK(inputs):
    if len(inputs) > 1:
        return False, 'Too many inputs'
    i = int(inputs[0])
    if i > 4294967295 or i <= 0:
        return False, 'Input range between 1 and 4294967295'
    return True, 'No errors'
    
def CO_set_TRIAL_TIMEOUT_CHECK(inputs):
    if len(inputs) > 1:
        return False, 'Too many inputs'
    i = int(inputs[0])
    if i > 4294967295 or i < 0:
        return False, 'Input range between 0 and 4294967295'
    return True, 'No errors'

def CO_set_PROBABILITY_ARRAY_CHECK(inputs):
    if not len(inputs) < 1:
        return False, 'Must insert at least one input'
    elif len(inputs) > 20:
        return False, 'Probability array as a maximum length of 20 values'
    i = int(inputs[0])
    if i < 0 or i > 100:
        return False, 'Input range between 0 and 100'
    return True, 'No errors'

def NO_INPUT_COMMAND_CHECK(command,inputs):
    if command in NO_INPUT_COMMANDS and len(inputs) > 1:
        return False, 'Too many inputs'
        

def check_prog(path_to_file):
    loop_local_num = 0
    block_if_num = 0
    command_sequence = []
    try:
        parsing_Funct(path_to_file,1)
    except ValueError, funcName:
        print 'Function %s not known'%funcName
        return False, 'Function %s not known'%funcName
    fh = open(path_to_file,'r')
#==============================================================================
#     Check CO_...
#==============================================================================
    line = fh.readline()
    while line.startswith('CO_'):
        line = line.rstrip('\n')
        for char in line:
            if char == '\t':
                line = line.lstrip('\t')
            elif char ==  ' ':
                line = line.lstrip(' ')
            else:
                break
            
        for char in line[::-1]:
            if char == '\t':
                line = line.rstrip('\t')
            elif char ==  ' ':
                line = line.rstrip(' ')
            else:
                break
        command = line.split(' ')[0].split('\t')[0]
        command_sequence += [command]
#        print '-%s-'%line
        inputs = line.split(' ')[1:]
        tof, error = INT_INPUT_CHECK(inputs)
        if not tof:
            fh.close()
            return tof, error
        if command == 'CO_set_MEAN_DISTRIBUTION':
            tof, error = CO_set_MEAN_DISTRIBUTION_CHECK(inputs)
        elif command == 'CO_set_TRIAL_MAX_NUMBER':
            tof, error = CO_set_TRIAL_MAX_NUMBER_CHECK(inputs)
        elif command == 'CO_set_PROBABILITY_ARRAY':
            tof, error = CO_set_PROBABILITY_ARRAY_CHECK(inputs)
        tof, error = INT_INPUT_CHECK(inputs)
        if not tof:
            fh.close()
            return tof, command + ': '+ error
        line = fh.readline()
        line = line.rstrip('\n')
#==============================================================================
#     Check START TRIAL
#==============================================================================
    print 'check start'
    while True:
        print '-%s-'%line
        for char in line:
            if char == '\t':
                line = line.lstrip('\t')
            elif char ==  ' ':
                line = line.lstrip(' ')
            else:
                break
        for char in line[::-1]:
            if char == '\t':
                line = line.rstrip('\t')
            elif char ==  ' ':
                line = line.rstrip(' ')
            else:
                break
        command = line.split(' ')[0].split('\t')[0]
        command_sequence += [command]
        inputs = line.split(' ')[1:]
        
        if command == 'START_TRIAL':
            break
        elif command == 'COUNTER_INIT':
            if len(inputs) != 2:
                return False, command + ': Two inputs required. %d given'%len(inputs)
        else:
            return False, command + ': Only initializations are allowed befeore START_TRIAL'
        line = fh.readline()
        line = line.rstrip('\n')
    if command != 'START_TRIAL':
        fh.close()
        return False, 'First command after COs must be START_TRIAL'
    if len(inputs) > 0:
        fh.close()
        return False, command + ': ' + 'Too many inputs'
    
#==============================================================================
#     RESET TRIGGER
#==============================================================================
    line = fh.readline()
    line = line.rstrip('\n')
    for char in line:
        if char == '\t':
            line = line.lstrip('\t')
        elif char ==  ' ':
            line = line.lstrip(' ')
        else:
            break
    for char in line[::-1]:
        if char == '\t':
            line = line.rstrip('\t')
        elif char ==  ' ':
            line = line.rstrip(' ')
        else:
            break
    command = line.split(' ')[0].split('\t')[0]
    command_sequence += [command]
    inputs = line.split(' ')[1:]
    if command != 'RESET_TRIGGER':
        fh.close()
        return False, 'Second command after COs must be RESET_TRIGGER'
    if len(inputs) > 0:
        return False, command + ': ' + 'Too many inputs'
#==============================================================================
#     Check all other commands
#==============================================================================
    line = fh.readline()
    while line:
        for char in line:
            if char == '\t':
                line = line.lstrip('\t')
            elif char ==  ' ':
                line = line.lstrip(' ')
            else:
                break
            for char in line[::-1]:
                if char == '\t':
                    line = line.rstrip('\t')
                elif char ==  ' ':
                    line = line.rstrip(' ')
                else:
                    break
        command = line.split(' ')[0].split('\t')[0]
        command_sequence += [command]
#        print 'riga',line,command, command_sequence
        inputs = line.split(' ')[1:]
        if command in NO_INPUT_COMMANDS and len(inputs) > 0:
            fh.close()
            return False, command + ': ' + 'Too many inputs'
        elif command in ONE_INPUT_COMMANDS and len(inputs) != 1:
            fh.close()
            return False, command + ': ' + 'One input required'
        elif command in TWO_INPUT_COMMANDS and len(inputs) != 2:
            fh.close()
            return False, command + ': ' + 'Two inputs required'
            
        if command.startswith('RGB') and command.endswith('ON'):
            if not int(inputs[0]) in range(8):
                fh.close()
                return False, command + ': ' + 'Input between 0 and 7' 
        elif command.startswith('FIXED_DELAY'):
            if int(inputs[0]) > 65535:
                fh.close()
                return False, command + ': ' + 'Input between lower then ' + inputs[0]
        elif command == 'RANDOM_DELAY_ITI':
            if not int(inputs[0]) in [1,2,3]:
                fh.close()
                return False, command + ': ' + 'Input must be 1 or 2 or 3'
        elif command.startswith('IS_'):
            block_if_num += 1

        elif command.startswith('END_BLOCK_IF'):
            block_if_num -= 1
        elif command == 'LOOP_LOCAL_TRIAL':
            loop_local_num += 1
        elif command == 'END_LOOP_LOCAL_TRIAL':
            loop_local_num -= 1

        line = fh.readline()
        line = line.rstrip('\n')
#    print '\n\n',command_sequence[-3:]
#    print block_if_num
    if command_sequence[-1] != 'END_TRIAL':
        return False, command_sequence[-1] + ': ' + 'Program must end with END_TRIAL'
    if block_if_num > 0:
        fh.close()
        return False, 'One or more \"IF\" not terminated'
    if block_if_num < 0:
        fh.close()
        return False, 'Too many \"END IF\"'
    if loop_local_num != 0:
        fh.close()
        return False, 'One or more \"LOOP_LOCAL_TRIAL\" not terminated'
    if block_if_num < 0:
        fh.close()
        return False, 'Too many \"END_LOOP_LOCAL_TRIAL\"'
    fh.close()
    return True, 'No errors encountered'
        
if __name__ == '__main__':
    path_to_file = 'C:\Users\ebalzani\IIT\Dottorato\Matte\Decision Making\\test_decision_making.prg'
    d = check_prog(path_to_file)
    print d