import numpy as np
from importDataset import *

def launchLoadingFun(fhname,funName):
	print 'Importing function launchehd: ', funName
	if funName == 'loadTimeActionData_TSE':
		return loadTimeActionData_TSE(fhname)

	if funName == 'load_TSE_edited_data':
		return load_TSE_edited_data(fhname)

	if funName == 'loadTimeActionData_AM_microsystems':
		return loadTimeActionData_AM_microsystems(fhname)

	if funName == 'load_sleep_sign_export_text':
		return load_sleep_sign_export_text(fhname)

	if funName == 'load_excel':
		return load_excel(fhname)

	if funName == 'load_and_parse_excel':
		return load_and_parse_excel(fhname)

	if funName == 'load_Spike_Data':
		return load_Spike_Data(fhname)

	if funName == 'importNex_Nex':
		return importNex_Nex(fhname)

	if funName == 'loadTimeActionData_MED_SW':
		return loadTimeActionData_MED_SW(fhname)

