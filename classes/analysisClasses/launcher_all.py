from analysis_functions import *

def function_Launcher(name,*myInput):
    if name == 'Power_Density':
        outputData, inputForPlots, info = Power_Density(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Sleep_Time_Course':
        outputData, inputForPlots, info = Sleep_Time_Course(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Linear_Discriminant_Analysis':
        outputData, inputForPlots, info = Linear_Discriminant_Analysis(*myInput)
        return outputData, inputForPlots, info
    elif name == 'LDA':
        outputData, inputForPlots, info = LDA(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Switch_Latency_TEST':
        outputData, inputForPlots, info = Switch_Latency_TEST(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Switch_Latency_TEST':
        outputData, inputForPlots, info = Switch_Latency_TEST(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Switch_Latency_TEST':
        outputData, inputForPlots, info = Switch_Latency_TEST(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Switch_Latency_TEST':
        outputData, inputForPlots, info = Switch_Latency_TEST(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Switch_Latency_TEST':
        outputData, inputForPlots, info = Switch_Latency_TEST(*myInput)
        return outputData, inputForPlots, info
