#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:35:01 2019

@author: Matte
"""
#TSE
#AM-Microsystems
#EEG Binned Frequencies
#EEG Full Power Spectrum
#Unparsed Excel File
#Parsed Excel
#MED_SW
#EDF

import numpy as np


DD = np.load('/Users/edoardo/Work/Code/phenopy/mainScripts/Analysis.npy').all()
new_dict = {}
keys = list(DD.keys())
for an_func in keys:
        tmpdict = DD.pop(an_func)
        alias = tmpdict.pop('label')
        new_dict[alias] = tmpdict
        new_dict[alias]['analysis_function'] = an_func
new_dict['SL']['plot_function'] = 'plotSwitchLatency_TEST'

np.save('/Users/edoardo/Work/Code/phenopy/mainScripts/Analysis.npy',new_dict)








        
  