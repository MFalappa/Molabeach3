from analysis_functions import *

def function_Launcher(name,*myInput):
    if name == 'Power_Density':
        outputData, inputForPlots, info = Power_Density(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Sleep_Time_Course':
        outputData, inputForPlots, info = Sleep_Time_Course(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Group_Error_Rate':
        outputData, inputForPlots, info = Group_Error_Rate(*myInput)
        return outputData, inputForPlots, info
    elif name == 'error_rate':
        outputData, inputForPlots, info = error_rate(*myInput)
        return outputData, inputForPlots, info
    elif name == 'LDA':
        outputData, inputForPlots, info = LDA(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Switch_Latency':
        outputData, inputForPlots, info = Switch_Latency(*myInput)
        return outputData, inputForPlots, info
    elif name == 'delta_rebound':
        outputData, inputForPlots, info = delta_rebound(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Actograms':
        outputData, inputForPlots, info = Actograms(*myInput)
        return outputData, inputForPlots, info
    elif name == 'AIT':
        outputData, inputForPlots, info = AIT(*myInput)
        return outputData, inputForPlots, info
    elif name == 'raster_plot':
        outputData, inputForPlots, info = raster_plot(*myInput)
        return outputData, inputForPlots, info
    elif name == 'peak_procedure':
        outputData, inputForPlots, info = peak_procedure(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Attentional_analysis':
        outputData, inputForPlots, info = Attentional_analysis(*myInput)
        return outputData, inputForPlots, info
    elif name == 'sleep_fragmentation':
        outputData, inputForPlots, info = sleep_fragmentation(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Sleep_cycles':
        outputData, inputForPlots, info = Sleep_cycles(*myInput)
        return outputData, inputForPlots, info
    elif name == 'emg_normalized':
        outputData, inputForPlots, info = emg_normalized(*myInput)
        return outputData, inputForPlots, info
    elif name == 'Switch_Latency_TEST':
        outputData, inputForPlots, info = Switch_Latency_TEST(*myInput)
        return outputData, inputForPlots, info
