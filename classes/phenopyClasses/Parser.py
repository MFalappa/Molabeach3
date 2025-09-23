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
from messageLib import (set_Mean_Distribution_ITI,set_Max_Trial_Num,
                        set_Probability_Array,program_Start_Trial,
                        set_Trial_Timeout_ms,program_Reset_Trigger,program_event_Trigger,
                        program_Start_Trial_Timer,program_if_Random_MC,program_Light_On,
                        program_Fix_Delay,program_Light_Off,program_Loop_Local_Trial,
                        program_If_Trigger,program_If_TimoutReached,
                        program_Release_Pellet,program_End_Local_Trial,
                        program_End_Block_If,program_Else_Block_If,
                        program_End_Loop_Local_Trial,program_Fixed_Delay_ITI,
                        program_Random_Delay_ITI,program_End_Trial,program_Counter_Init,
                        program_If_Light,program_If_Presence,program_Counter_Inc,
                        program_If_Counter,program_If_Random_Mc_Step,program_Dummy_Test,
                        program_Noise_On,program_Noise_Off,log_ITI_end_Msg,
                        program_event_Poke,program_manage_RGB,program_TTL,program_action,
                        program_init_Random_Mc_index,program_is_Random_Mc_index)

def parsing_Funct(pathToText,Id):
    """
        Parsing of the program written in in pseudo code.
    """
    messageList = []
    if not os.path.exists(pathToText):
        raise IOError('No such file \'%s\''%pathToText)
    num_lines = sum(1 for line in open(pathToText))
    fh = open(pathToText,'r')
    row = 0
    for fileRow in range(num_lines):
        line = fh.readline()
        line = line.rstrip('\n')
        for char in line:
            if char == '\t' or char == ' ':
                line = line.lstrip('\t')
                line = line.lstrip(' ')
            else:
                break

        for char in line[::-1]:
            
            if char == '\t' or char == ' ':
                line = line.rstrip('\t')
                line = line.rstrip(' ')
            else:
                break
        
        listLine = line.split(' ')
        programName = None
        parameters = []
        try:
           while True:
               listLine.remove(' ') 
        except ValueError:
            pass
        programName = listLine.pop(0)
        for param in listLine:
            parameters += [int(param)]
#        print 'line-%s-'%line, parameters
        if not programName or len(programName)==0 or programName in '\n':  
            continue
        elif programName == 'CO_set_MEAN_DISTRIBUTION':
            messageList += [set_Mean_Distribution_ITI(Id,parameters[0])]
        elif programName == 'CO_set_TRIAL_MAX_NUMBER':
            messageList += [set_Max_Trial_Num(Id,parameters[0])]
        elif programName == 'CO_set_TRIAL_TIMEOUT':
            messageList += [set_Trial_Timeout_ms(Id,parameters[0])]   
        elif programName == 'CO_set_PROBABILITY_ARRAY':
            messageList += set_Probability_Array(Id,parameters)  
        elif programName == 'START_TRIAL':
            messageList += [program_Start_Trial(Id,row)]
            row += 1
        elif programName == 'RESET_TRIGGER':
            messageList += [program_Reset_Trigger(Id,row)]
            row += 1
        elif programName == 'EVENT_TRIGGER_MID':
            messageList += [program_event_Trigger(Id,row,'M')]
            row += 1
        elif programName == 'EVENT_TRIGGER_LEFT':
            messageList += [program_event_Trigger(Id,row,'L')]
            row += 1
        elif programName == 'EVENT_TRIGGER_RIGHT':
            messageList += [program_event_Trigger(Id,row,'R')]
            row += 1
        elif programName == 'START_TRIAL_TIMER':
            messageList += [program_Start_Trial_Timer(Id,row)]
            row += 1
        elif programName == 'IS_RANDOM_MC':
            if len(parameters) == 1:
                messageList += [program_if_Random_MC(Id,row,parameters[0])]
            elif len(parameters) == 0:
                messageList += [program_if_Random_MC(Id,row,0)]
            else:
                raise ValueError('Too many parameters for function %s'%programName)
            row += 1
        elif programName == 'RGB_LEFT_ON':
            messageList += [program_Light_On(Id,row,'L',parameters[0])]
            row += 1
        elif programName == 'RGB_RIGHT_ON':
            messageList += [program_Light_On(Id,row,'R',parameters[0])]
            row += 1
        elif programName == 'RGB_MID_ON':
            messageList += [program_Light_On(Id,row,'M',parameters[0])]
            row += 1
        elif programName == 'FIXED_DELAY':
            messageList += [program_Fix_Delay(Id,row,parameters[0])]
            row += 1
        elif programName == 'FIXED_DELAY':
            messageList += [program_Fix_Delay(Id,row,parameters[0])]
            row += 1
        elif programName == 'RGB_LEFT_OFF':
            messageList += [program_Light_Off(Id,row,'L')]
            row += 1
        elif programName == 'RGB_MID_OFF':
            messageList += [program_Light_Off(Id,row,'M')]
            row += 1
        elif programName == 'RGB_RIGHT_OFF':
            messageList += [program_Light_Off(Id,row,'R')]
            row += 1
        elif programName == 'LOOP_LOCAL_TRIAL':
            messageList += [program_Loop_Local_Trial(Id,row)]
            row += 1
        elif programName == 'IS_TRIGGER_LEFT':
            messageList += [program_If_Trigger(Id,row,'L')]
            row += 1
        elif programName == 'IS_TRIGGER_MID':
            messageList += [program_If_Trigger(Id,row,'M')]
            row += 1
        elif programName == 'IS_TRIGGER_RIGHT':
            messageList += [program_If_Trigger(Id,row,'R')]
            row += 1
        elif programName == 'IS_TIMEOUT_REACHED':
            messageList += [program_If_TimoutReached(Id,row)]
            row += 1
        elif programName == 'RELEASE_PELLET_LEFT':
            messageList += [program_Release_Pellet(Id,row,'L')]
            row += 1
        elif programName == 'RELEASE_PELLET_RIGHT':
            messageList += [program_Release_Pellet(Id,row,'R')]
            row += 1
        elif programName == 'END_LOCAL_TRIAL':
            messageList += [program_End_Local_Trial(Id,row)]
            row += 1
        elif programName == 'END_BLOCK_IF':
            messageList += [program_End_Block_If(Id,row)]
            row += 1
        elif programName == 'END_LOOP_LOCAL_TRIAL':
            messageList += [program_End_Loop_Local_Trial(Id,row)]
            row += 1
        elif programName == 'ELSE_BLOCK_IF':
            messageList += [program_Else_Block_If(Id,row)]
            row += 1
        elif programName == 'BLOCK_ELSE_IF':
            messageList += [program_Else_Block_If(Id,row)]
            row += 1 
        elif programName == 'FIXED_DELAY_ITI':
            messageList += [program_Fixed_Delay_ITI(Id,row,parameters[0])]
            row += 1
        elif programName == 'RANDOM_DELAY_ITI':
            messageList += [program_Random_Delay_ITI(Id,row,parameters[0])]
            row += 1
        elif programName == 'END_TRIAL':
            messageList += [program_End_Trial(Id,row)]
            row += 1
        elif programName == 'COUNTER_INIT':
            if len(parameters) == 1:
                parameters += [0]
            messageList += [program_Counter_Init(Id,row,parameters[0],parameters[1])]
            row += 1
        elif programName == 'IS_LEFT_LIGHT':
            messageList += [program_If_Light(Id,row,'L')]
            row += 1
        elif programName == 'IS_MID_LIGHT':
            messageList += [program_If_Light(Id,row,'M')]
            row += 1
        elif programName == 'IS_RIGHT_LIGHT':
            messageList += [program_If_Light(Id,row,'M')]
            row += 1
        elif programName == 'COUNTER_INC':
            messageList += [program_Counter_Inc(Id,row,parameters[0])]
            row += 1
        elif programName == 'IS_PRESENCE_LEFT':
            messageList += [program_If_Presence(Id,row,'L')]
            row += 1
        elif programName == 'IS_PRESENCE_MID':
            messageList += [program_If_Presence(Id,row,'M')]
            row += 1
        elif programName == 'IS_PRESENCE_RIGHT':
            messageList += [program_If_Presence(Id,row,'R')]
            row += 1
        elif programName == 'IS_COUNTER_GREATER':
            messageList += [program_If_Counter(Id,row,'G',parameters[0],parameters[1])]
            row += 1
        elif programName == 'IS_COUNTER_LESSER':
            messageList += [program_If_Counter(Id,row,'L',parameters[0],parameters[1])]
            row += 1
        elif programName == 'IS_COUNTER_EQUAL':
            messageList += [program_If_Counter(Id,row,'E',parameters[0],parameters[1])]
            row += 1
        elif programName == 'IS_RANDOM_MC_STEP':
            messageList += [program_If_Random_Mc_Step(Id,row,parameters[0])]
            row += 1
        elif programName == 'DUMMY_TEST':
            messageList += [program_Dummy_Test(Id,row)]
            row += 1
        elif programName == 'NOISE_LEFT_ON':
            messageList += [program_Noise_On(Id, row, 1, 0, 0)]
            row += 1
        elif programName == 'NOISE_LEFT_OFF':
            messageList += [program_Noise_Off(Id,row,1,0,0)]
            row += 1
        elif programName == 'NOISE_RIGHT_ON':
            messageList += [program_Noise_On(Id,row,0,0,1)]
            row += 1
        elif programName == 'NOISE_RIGHT_OFF':
            messageList += [program_Noise_Off(Id,row,0,0,1)]
            row += 1
        elif programName == 'NOISE_MID_ON':
            messageList += [program_Noise_On(Id,row,0,1,0)]
            row += 1
        elif programName == 'NOISE_MID_OFF':
            messageList += [program_Noise_Off(Id,row,0,1,0)]
            row += 1
        elif programName == 'LOG_ITI_END':
            messageList += [log_ITI_end_Msg(Id,row)]
            row += 1

        elif programName == 'IS_PRESENCE_LEFT':
            messageList += [program_If_Presence(Id,row,'L')]
            row += 1
        elif programName == 'IS_PRESENCE_MID':
            messageList += [program_If_Presence(Id,row,'M')]
            row += 1
        elif programName == 'IS_PRESENCE_RIGHT':
            messageList += [program_If_Presence(Id,row,'R')]
            row += 1
        elif programName == 'EVENT_POKE_LEFT':
            messageList += [program_event_Poke(Id,row,'L')]
            row += 1
        elif programName == 'EVENT_POKE_MID':
            messageList += [program_event_Poke(Id,row,'M')]
            row += 1
        elif programName == 'EVENT_POKE_RIGHT':
            messageList += [program_event_Poke(Id,row,'R')]
            row += 1
        elif programName == 'RGB_MANAGE':
            messageList += [program_manage_RGB(Id,row,parameters[0],
                                               parameters[1],parameters[2])]
            row += 1
        elif programName == 'ACTION_TTL':
            messageList += [program_TTL(Id,row,parameters[0],
                                               parameters[1])]
            row += 1
        elif programName == 'MARK_ACTION':
            messageList += [program_action(Id,row,parameters[0])]
            row += 1
        
        elif programName == 'CO_INIT_RANDOM_MC_INDEX':
            messageList += [program_init_Random_Mc_index(Id,row)]
            row += 1
        
        elif programName == 'IS_RANDOM_MC_INDEX':
            messageList += [program_is_Random_Mc_index(Id,row,parameters[0])]
            row += 1
     
        else:
            raise ValueError(programName)
#        print(programName,' ',messageList[-1])
#              messageList[-1].dataAsHexStr()[2:4],
#              messageList[-1].dataAsHexStr()[4:8],
#              messageList[-1].dataAsHexStr()[8:10],
#              messageList[-1].dataAsHexStr()[10:12],
#              messageList[-1].dataAsHexStr()[12:14],
#              messageList[-1].dataAsHexStr()[14:16],
#              messageList[-1].dataAsHexStr()[16:18],
#              messageList[-1].dataAsHexStr()[20:22])
    return messageList

if __name__=='__main__':
    from time import clock
    import numpy as np
    t0=clock()
    command = parsing_Funct('/Users/Matte/Scuola/Dottorato/Projects/Tucci/switch colors/sw/preTraining_blu.txt',3)
    print(clock()-t0)
    data_matrix = np.zeros((len(command),9),dtype='S2')
    row = 0
    for msg in command:
        sting_data = msg.dataAsHexStr()
        k=0
        for ind in range(0,18,2):
            data_matrix[row,k] = sting_data[ind:ind+2]
            k += 1
        row+=1
    print(data_matrix)
    np.savetxt('/Users/Matte/Desktop/Program_switch.txt',data_matrix,fmt='%s')
