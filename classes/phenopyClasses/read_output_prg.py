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

import numpy as np

dict_input = { # chiave = codice funzione, valore = numero parametri
0:0,	# START_TRIAL
1:0,	# END_TRIAL
2:0,	# BLOCK_END_IF
3:0,	# LOOP_LOCAL_TRIAL
4:0,	# END_LOOP_LOCAL_TRIAL 
5:0,	# END_LOCAL_TRIAL
6:0,	# BLOCK_ELSE_IF
7:0,	# START_TRIAL_TIMER
8:0,	# RESET_TRIGGER
9:3,	# RGB_MANAGE
10:1,	# RGB_LEFT_ON
11:0,	# RGB_LEFT_OFF
12:1,   # RGB_MID_ON
13:0,	# RGB_MID_OFF
14:1,	# RGB_RIGHT_ON
15:0,	# RGB_RIGHT_OFF
16:0,	# NOISE_LEFT_ON
17:0,	# NOISE_LEFT_OFF
18:0,	# NOISE_MID_ON
19:0,	# NOISE_MID_OFF
20:0,	# NOISE_RIGHT_ON
21:0,	# NOISE_RIGHT_OFF
	
30:0,	# EVENT_POKE_LEFT
31:0,	# EVENT_POKE_MID
32:0,	# EVENT_POKE_RIGHT 
33:0,	# EVENT_TRIGGER_LEFT
34:0,	# EVENT_TRIGGER_MID
35:0,	# EVENT_TRIGGER_RIGHT
	
40:2,	# FIXED_DELAY
41:2,	# FIXED_DELAY_ITI
42:1,	# RANDOM_DELAY_ITI
43:0,	# LOG_ITI_END
	
50:0,	# IS_RANDOM_MC
52:0,	# IS_RANDOM_MC_STEP
	
57:0,	# IS_TRIGGER_LEFT
58:0,	# IS_TRIGGER_MID
59:0,	# IS_TRIGGER_RIGHT
60:0,	# IS_PRESENCE_LEFT
61:0,	# IS_PRESENCE_MID
62:0,	# IS_PRESENCE_RIGHT
63:0,	# IS_LIGHT_LEFT
64:0,	# IS_LIGHT_MID
65:0,	# IS_LIGHT_RIGHT
66:2,	# IS_COUNTER_GREATER
67:2,	# IS_COUNTER_LESSER
68:2,	# IS_COUNTER_EQUAL
69:0,	# IS_TIMEOUT_REACHED
70:2,	# COUNTER_INIT
71:1,	# COUNTER_INC
	
80:0,	# RELEASE_PELLET_LEFT
81:0,	# RELEASE_PELLET_RIGHT
82:0,	# DUMMY_TEST
83:2,	# ACTION_TTL
}

dict_function = { # chiave = codice funzione, valore = nome funzione
0:'START_TRIAL',
1:'END_TRIAL',
2:'BLOCK_END_IF',
3:'LOOP_LOCAL_TRIAL',
4:'END_LOOP_LOCAL_TRIAL' ,
5:'END_LOCAL_TRIAL',
6:'ELSE_BLOCK_IF',
7:'START_TRIAL_TIMER',
8:'RESET_TRIGGER',
9:'RGB_MANAGE',
10:'RGB_LEFT_ON',
11:'RGB_LEFT_OFF',
12:'RGB_MID_ON',
13:'RGB_MID_OFF',
14:'RGB_RIGHT_ON',
15:'RGB_RIGHT_OFF',
16:'NOISE_LEFT_ON',
17:'NOISE_LEFT_OFF',
18:'NOISE_MID_ON',
19:'NOISE_MID_OFF',
20:'NOISE_RIGHT_ON',
21:'NOISE_RIGHT_OFF',
	
30:'EVENT_POKE_LEFT',
31:'EVENT_POKE_MID',
32:'EVENT_POKE_RIGHT' ,
33:'EVENT_TRIGGER_LEFT',
34:'EVENT_TRIGGER_MID',
35:'EVENT_TRIGGER_RIGHT',
	
40:'FIXED_DELAY',
41:'FIXED_DELAY_ITI',
42:'RANDOM_DELAY_ITI',
43:'LOG_ITI_END',
	
50:'IS_RANDOM_MC',
52:'IS_RANDOM_MC_STEP',
	
57:'IS_TRIGGER_LEFT',
58:'IS_TRIGGER_MID',
59:'IS_TRIGGER_RIGHT',
60:'IS_PRESENCE_LEFT',
61:'IS_PRESENCE_MID',
62:'IS_PRESENCE_RIGHT',
63:'IS_LIGHT_LEFT',
64:'IS_LIGHT_MID',
65:'IS_LIGHT_RIGHT',
66:'IS_COUNTER_GREATER',
67:'IS_COUNTER_LESSER',
68:'IS_COUNTER_EQUAL',
69:'IS_TIMEOUT_REACHED',
70:'COUNTER_INIT',
71:'COUNTER_INC',
	
80:'RELEASE_PELLET_LEFT',
81:'RELEASE_PELLET_RIGHT',
82:'DUMMY_TEST',
83:'ACTION_TTL',
}


def hexString_to_int(hex_string_list):
    int_list = []
    for string in hex_string_list:
        int_list += [ int(string[2*5:2*5+2],16)]
        if len(int_list) <5:
            print string
    return int_list
    
def create_program(int_list):
    global dict_function, dict_input
    prog_str = ''
    k = 0
    while k < len(int_list):
        print k
        func_name = dict_function[int_list[k]]
        param_num = dict_input[int_list[k]]
        param_str = ''
        for j in xrange(param_num):
            k += 1
            param_str += ' %d'%int_list[k]
        if func_name == 'END_LOOP_LOCAL_TRIAL':
                k+= 1
        prog_str = prog_str + '%s'%func_name + param_str + '\n'
        k += 1
    return prog_str



if __name__ == '__main__':
    list_hex = np.loadtxt('C:\Users\ebalzani\IIT\myPython\\canusb_project\Programmi\\Prog_Peak_Uploaded.txt',
                          dtype='S100')
    new_list_hex = []
    for a in list_hex:
        new_list_hex += [''.join(a)]
    int_list = hexString_to_int(new_list_hex)
    program_transl = create_program(int_list)
#    fh = open('C:\Users\ebalzani\IIT\Dottorato\Matte\Color Preference\Data\\27-6 to 28-6\\change_color_prog_transl.txt','w')
#    fh.write(program_transl)
#    fh.close()