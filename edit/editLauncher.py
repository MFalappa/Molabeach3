import numpy as np
from editFunctions import *

def launchEditFun(phenopy,funName):
	if funName == 'TSE__Merge_Dataset':
		return TSE__Merge_Dataset(phenopy)

	if funName == 'AM_Microsystems__Merge_Dataset':
		return AM_Microsystems__Merge_Dataset(phenopy)

	if funName == 'EEG_Binned_Frequencies__Merge_Dataset':
		return EEG_Binned_Frequencies__Merge_Dataset(phenopy)

	if funName == 'EEG_Full_Power_Spectrum__Merge_Dataset':
		return EEG_Full_Power_Spectrum__Merge_Dataset(phenopy)

	if funName == 'TSE_Cut_Dataset':
		return TSE_Cut_Dataset(phenopy)

	if funName == 'AM_Microsystems__Cut_Dataset':
		return AM_Microsystems__Cut_Dataset(phenopy)

	if funName == 'EEG_Binned_Frequencies__Cut_Dataset':
		return EEG_Binned_Frequencies__Cut_Dataset(phenopy)

	if funName == 'EEG_Full_Power_Spectrum__Cut_Dataset':
		return EEG_Full_Power_Spectrum__Cut_Dataset(phenopy)

	if funName == 'TSE__Select_Interval':
		return TSE__Select_Interval(phenopy)

	if funName == 'AM_Microsystems__Select_Interval':
		return AM_Microsystems__Select_Interval(phenopy)

