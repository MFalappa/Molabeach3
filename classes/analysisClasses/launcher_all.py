from analysis_functions import *

def function_Launcher(name,*myInput):
    if name == 'Power_Density':
        outputData, inputForPlots, info = Power_Density(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Sleep_Time_Course':
        outputData, inputForPlots, info = Sleep_Time_Course(*myInput)
        return outputData, inputForPlots, info
    elif name == 'LDA':
        outputData, inputForPlots, info = LDA(*myInput)
        return outputData, inputForPlots, info
 
