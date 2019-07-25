from custom_Analysis_Gr import *

def function_Launcher_Gr(name,*myInput):
    if name == 'Power_Density':
        outputData, inputForPlots, info = Power_Density(*myInput)
        return outputData, inputForPlots, info
    if name == 'Sleep_Time_Course':
        outputData, inputForPlots, info = Sleep_Time_Course(*myInput)
        return outputData, inputForPlots, info
    if name == 'Linear_Discriminant_Analysis':
        outputData, inputForPlots, info = Linear_Discriminant_Analysis(*myInput)
        return outputData, inputForPlots, info
    if name == 'LDA':
        outputData, inputForPlots, info = LDA(*myInput)
        return outputData, inputForPlots, info
    if name == 'Switch_Latency_TEST':
        outputData, inputForPlots, info = Switch_Latency_TEST(*myInput)
        return outputData, inputForPlots, info
