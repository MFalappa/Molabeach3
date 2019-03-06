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
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import string
import scipy.stats as sts
import bisect
from copy import copy
from Analyzing_GUI import Normalize_Action_x_Interval_GUI
from Modify_Dataset_GUI import TimeUnit_to_Hours_GUI

def plotLDARes_Dict(X_norm_d, y_d, lda_res_d, gauss_light_d, gauss_dark_d,line_light_d,line_dark_d, Index_for_color_d, Struct_mat_d, v_ort_d ,hl, hd,title_d,xlabel,ylabel):
    figDict = {}
    for name in  list(X_norm_d.keys()):
        X_norm = X_norm_d[name]
        y = y_d[name]
        lda_res = lda_res_d[name]
        gauss_light = gauss_light_d[name]
        gauss_dark = gauss_dark_d[name]
        line_light = line_light_d[name]
        line_dark = line_dark_d[name]
        Index_for_color = Index_for_color_d[name]
        Struct_mat = Struct_mat_d[name]
        v_ort = v_ort_d[name]
        title = title_d[name]
        fig = plotLDARes(X_norm, y, lda_res, gauss_light, gauss_dark,line_light,line_dark, Index_for_color, Struct_mat, v_ort ,hl, hd,
               title,xlabel,ylabel)
        figDict['Scatter %s'%name] = fig
    return figDict
    
def plotLDARes(X_norm, y, lda_res, gauss_light, gauss_dark,line_light,line_dark, Index_for_color, Struct_mat, v_ort ,hl, hd,
               title,xlabel,ylabel):

    fig = plt.figure()
    plt.hold(1)
    plt.title(title, fontsize=20,)
    plt.fill_betweenx([-4,4],[-4,4],[4,-4],color='k',alpha=np.abs(Struct_mat[1,Index_for_color]))
    plt.fill_between([-4,4],[-4,4],[4,-4],color='k',alpha=np.abs(Struct_mat[0,Index_for_color]))
    plt.scatter(X_norm[hd,0],X_norm[hd,1],color='g',s=40)
    plt.scatter(X_norm[hl,0],X_norm[hl,1],color='r',s=40)
    
    m = lda_res.coef_[0][0]/lda_res.coef_[0][1]
    m=-1/m
    q = lda_res.intercept_
    
    x = np.linspace(-4,4,100)
    f_x = m*x+q
    plt.plot(f_x,x,color=(218./255,165./255,32./255),lw=2 ) 
    
    plt.fill_between(gauss_light[0,:],line_light,gauss_light[1,:],alpha=0.85,facecolor='r',edgecolor=None)
    plt.fill_between(gauss_dark[0,:],line_dark,gauss_dark[1,:],alpha=0.85,facecolor='g',edgecolor=None)

    plt.xlim(-4,4)
    plt.ylim(-4,4)
    
    plt.plot(gauss_light[0,:],gauss_light[1,:],'r')
    plt.plot(gauss_dark[0,:],gauss_dark[1,:],'g')
    plt.xlabel(xlabel,fontsize=15)
    plt.ylabel(ylabel,fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    return fig

def Gr_SwitchLAtency_PLT_GUI(*myinput):
    fig1 = Gr_BoxPlot_LD_GUI(myInput[:4])
    fig2    = CDF_Gr_Plot_GUI(myInput[4:])
    fig2[max(fig2.keys())+1] = fig1
    return fig2
    
def Print_Actogram_GUI(Action_x_Interval,N_Day,interval,returnFig = False, *other, **kwargs):
    """

    Function Targets:   Print an actogram
    Input:              -Action_x_Interval=vector containing number of NP per time interval
                        -N_Day=numbers of day of the acogram
                        -interval=fraction of an hour in seconds
                        -other=tuple, the periodicity of the activity we consider in hour 
                        and/or the string specify how to normalize the actogram bars. 
                        -kwargs=dictionary, key='Start_Hour','Norm'
                            -kwargs['Norm']=boolean, true if data are normalized 
                            false if not
    Output:             -Actogram = the actogram graph
    
    """
    
    print('retfig',returnFig)
    if len(other)==0:
        period=24
        string='All'
    elif len(other)==1:
        if type(other[0])==int:
            period=other[0]
            string='All'
        else:
            string=other[0]
            period=24
    elif len(other)==2:
        if type(other[0])==int:
            period=other[0]
            string=other[1]
        else:
            string=other[0]
            period=other[1]
    elif len(other)>2:
        print('Warning! Too many input argumet...')
        return()
    
    if 3600%interval!=0:
        print('Warning! The interval you choose is not a fraction of an hour')
        return()
    if 'Start_Hour' in kwargs:
        Start_Hour=int(kwargs['Start_Hour'])
    else:
        Start_Hour=0
    if 'Norm' in kwargs:
        Norm=kwargs['Norm']
    else:
        Norm = False
#    print 'Start_Hour',Start_Hour
    Hour_Fraction=int(3600/interval)
    period=int(period)
    N_Day=int(N_Day)
    #print Norm
#   We keep only the NP that occured in the N_Day days of trials
    if not Norm:
        Norm_Action_x_Interval=Normalize_Action_x_Interval_GUI(Action_x_Interval,period,Hour_Fraction,N_Day,string)
    else:
        Norm_Action_x_Interval=Action_x_Interval
    
#   Actogram's total raw number = number of days minus one
#   x_axis is a vector like [1,2,3,..,period*4-1,period*4,1,2,3,...,period*4-1,period*4,1,2...,period*4]
#   repeting N_day-1 times the arange(1,period*4+1).
    if string=='FullData':
        
        x_axis=np.array(np.ones((N_Day,1))*np.arange(1,Hour_Fraction*2*period+1)).reshape(-1,)
                    
        Norm_Action_x_Interval=np.hstack((Norm_Action_x_Interval,np.zeros((N_Day+1)*Hour_Fraction*period-len(Norm_Action_x_Interval))))
    #   We create a matrix in with every raw contains the actions of an entire day
        
        Daily_Actions=np.array(Norm_Action_x_Interval.reshape((N_Day+1,Hour_Fraction*period)))
    
    #   We double from the second raw to the last but one
    
        Double=np.hstack((Daily_Actions[1:-1],Daily_Actions[1:-1])).reshape(-1,)
        
        y_axis=np.hstack((Norm_Action_x_Interval[0:Hour_Fraction*period],Double,Norm_Action_x_Interval[-Hour_Fraction*period:]))
    
        Bottom_y=(np.arange(1,N_Day+1).reshape((N_Day,1))*np.ones(2*period*Hour_Fraction)).reshape(-1,)    
    
    else:
        x_axis=np.array(np.ones((N_Day-1,1))*np.arange(1,Hour_Fraction*2*period+1)).reshape(-1,)
       
    #   We create a matrix in with every raw contains the actions of an entire day
    
        Daily_Actions=np.array(Norm_Action_x_Interval.reshape((N_Day,Hour_Fraction*period)))
    
    #   We double from the second raw to the last but one
    
        Double=np.hstack((Daily_Actions[1:-1],Daily_Actions[1:-1])).reshape(-1,)
        
        y_axis=np.hstack((Norm_Action_x_Interval[0:Hour_Fraction*period],Double,Norm_Action_x_Interval[-Hour_Fraction*period:]))
    
        Bottom_y=(np.arange(1,N_Day).reshape((N_Day-1,1))*np.ones(2*period*Hour_Fraction)).reshape(-1,)
    Bottom_y=Bottom_y[::-1]
    x_axis=x_axis*interval/3600
    FIG = plt.figure(figsize=(5.5*3.13,3.5*3.13))
    if 'title' in kwargs:
        plt.title(kwargs['title'])
    Actogram = plt.bar(x_axis,y_axis,bottom=Bottom_y,align='center',width=interval/3600.0,color='b',lw=0.)
     
    if N_Day>=2 and string=='FullData':
        label=[]
        for i in range(N_Day):
            label=label+['%d-%d' % (N_Day-i,N_Day-i+1)]
        plt.yticks(np.arange(1,N_Day+1),label)
        ymax=N_Day+1
    elif N_Day>=2 and string!='FullData':
        label=[]
        for i in range(N_Day-1):
            label=label+['%d-%d' % (N_Day-(i+1),N_Day-i)]
        plt.yticks(np.arange(1,N_Day),label)
        ymax=N_Day
    else:
        label=['1-2']
        plt.yticks([1],label)
        ymax=1
   
    plt.xlabel('Time(hours)')
    plt.ylabel('Days')
    if 'Title' in kwargs:
        title=kwargs['Title']
    else:
        title='Actogram'
    plt.title(title)
    if 'Suptitle' in kwargs:
        plt.suptitle(kwargs['Suptitle'],fontsize='large')
    
    plt.ylim(1,ymax)
    #plt.xticks(np.arange(0,2*period+1,6),np.arange(Start_Hour,Start_Hour+2*period+1,6)%(period))
    plt.xticks(np.arange(0,2*period+1,1),np.arange(Start_Hour,Start_Hour+2*period+1,1)%(period))
    plt.hold(1)
    
    plt.xlim((-0.5,2*period))
    
    if returnFig:
        return(FIG)
        
    return(Actogram)


    
def F_Errorbar_Plt_LD_GUI(Mean_error,std_error,group_name,Hour_Dark,
                      Hour_Light,period=24,H_bin=1,Ylabel='Error Rate',Title=None):
    """
    Function Targets:       This function prints an errorbar plot
    
    Input:                  -Mean_error=dictionary, keys:group names
                            values: mean error rate, starting 
                            from the first H_bin hours of Dark phase following
                            the dark phase
                            -period= the period you're considering, default =24 h
                            -H_bin=integer, number of hour bins default=1
                            
    Output:                 -Error bar graph
    """


  
#   Length_Light=number of light phase hour bins
#   Length_Dark=number of dark phase hour bins


    x_axis=np.arange(len(Mean_error[group_name[0]]))
    
    L_H_bin_Mean=int(np.ceil(float(period)/(2*H_bin)))

#   Here we create x label
    label_dark=[]
    label_light=[]
    for i in np.arange(L_H_bin_Mean):
        hour_first=Hour_Dark[i*H_bin:(i+1)*H_bin][0]
        hour_last=Hour_Dark[i*H_bin:(i+1)*H_bin][-1]
        if hour_first==hour_last:
            label_dark=label_dark+['%d'%hour_first]
        else:
            label_dark=label_dark+['%d-%d'%(hour_first,hour_last)]
        hour_first=Hour_Light[i*H_bin:(i+1)*H_bin][0]
        hour_last=Hour_Light[i*H_bin:(i+1)*H_bin][-1]

        if hour_first==hour_last:
            label_light=label_light+['%d'%hour_first]
        else:
            label_light=label_light+['%d-%d'%(hour_first,hour_last)]
        
    label_ticks=label_dark+label_light

    label_legend=group_name
    plt.figure(figsize=(5.5*3.13,3.5*3.13))
    plt.hold(1)
    plt.xticks(x_axis,label_ticks)
    plt.xlabel('Circadian time interval')
    plt.ylabel(Ylabel)
    plt.xlim((-1,x_axis[-1]+1))
    plt.axvspan(-1,len(label_dark)-0.5 ,color='b', alpha=0.3)
    if Title:
        plt.title(Title)
    for group in group_name:        
        plt.errorbar(x_axis,Mean_error[group],yerr=std_error[group])

    plt.legend(label_legend)
    plt.hold(0)
    return()

def LD_ErrorBar_plt_GUI(AllMeans,AllStdErrors,Label,Title=None,Ylim=None,
                    rotation=0,color='r',alpha=0.3,ecolor='r',Ticks=True,
                    HourFrac=1,DarkStart=20,Xlabel=None,lw=0.0,figSize=None,
                    Dark_Len=None):
    """
    Function target:
    ----------------
        This function prints an errror bar plot. The difference with the previuous
        function is that the dark phase blu rectangle is drawn using information 
        contained in label.
    Input:
    ------
        - AllMeans = array, contains the y_axis values
        - AllStdError = array, contains the error bar length
        - Label = list of str, each str can be 'Light'/'L' indicating that
             the corrisponding point is in light  phase, 'Dark'/'D' if it is in
             Dark phase.
        - Ticks = True for using Label for the ticks. (usually this option
            is for a L/D graph over the days). If Ticks is False than the ticks
            will be the hour from DarkStart to the end
        - DarkStart = int, hour in which dark phase starts. It will corrispond to the
            hour indicated for the first ticks. (it is supposed that you reordered the dict
            with the dark before and than the light)
        - HourFraction = int, if you are plotting daily averages indicates the time
            bin used for the time binning. 
            example:
                If each value corrispond to a 15min mean you will have to put HourFrac=4
                If each value corrispond to a 30min mean you will have to put HourFrac=2
                If each value corrispond to a 60min mean you will have to put HourFrac=1
            
        
            
    """
    if figSize:
        plt.figure(figsize=figSize)
    plt.hold(1)
    if AllStdErrors==None:
        if color:
            p1,=plt.plot(list(range(len(Label))),AllMeans,'%s'%color)
        else:
            p1,=plt.plot(list(range(len(Label))),AllMeans)
    else:
        if color and ecolor:
            p1=plt.errorbar(list(range(len(Label))),AllMeans,yerr=AllStdErrors,elinewidth=2,color=color,ecolor=ecolor)    
        elif color:
            p1=plt.errorbar(list(range(len(Label))),AllMeans,yerr=AllStdErrors,elinewidth=2,color=color)
        elif ecolor:
            p1=plt.errorbar(list(range(len(Label))),AllMeans,yerr=AllStdErrors,elinewidth=2,ecolor=ecolor)
        else:
            p1=plt.errorbar(list(range(len(Label))),AllMeans,yerr=AllStdErrors,elinewidth=2)
    if Ylim is None:
        plt.ylim(0,1)
    else:
        plt.ylim(Ylim)
    plt.ylabel('Mean')
    if Ticks:
        plt.xticks(list(range(len(Label))),Label,rotation=rotation)
    else:
        ticks,labels=plt.xticks()
        
        if 0 in ticks:
            #print('ciao')
            fracTicks=(np.array(ticks)+DarkStart*HourFrac)%(24*HourFrac)
            hourTicks=np.array(fracTicks/HourFrac,dtype=int)
            minTicks=np.mod(np.array(ticks),HourFrac)*(60/HourFrac)
            LabelTicks=[]
            for k in range(len(ticks)):
                if minTicks[k]<10:
                    minT='0'+str(int(minTicks[k]))
                else:
                    minT=str(int(minTicks[k]))
                LabelTicks+=['%d:%s'%(hourTicks[k],minT)]
            plt.xticks(ticks,LabelTicks)
    plt.xlim(-0.5,len(Label)-0.5)     
    if Dark_Len:
        plt.axvspan(-0.5,Dark_Len-0.5,alpha=alpha,lw=lw)
    else:
        for i in range(len(Label)):
            if Label[i]=='D' or Label[i]=='Dark':
                plt.axvspan(i-0.5,i+0.5,alpha=alpha,lw=lw)
            
            
    if Title:
        plt.title(Title)
    if Xlabel:
       plt.xlabel(Xlabel) 
            
    plt.hold(0)   
    return p1
    
def F_Error_Rate_plt_GUI(Correct_Rate):

    """
    Function target:    This function prints the error rate bar for each hour.
                        You can also specify the type of error rate to print.

    Input:              -Correct_Rate=vector, element i of this vector contains
                        the correct rate of hour i.
  .

    Output:             -Error Rate bar graph.
                        
    """      
    xaxis=list(range(24))
    yaxis=1-Correct_Rate
    Mean=sum(yaxis)/24
    x=[-0.50,23.5]
    y=[Mean,Mean]
    plt.figure(figsize=(5.5*3.13,3.5*3.13))
    plt.hold(1)
    plt.plot(x,y,'--r')
    plt.bar(xaxis,yaxis,align='center')
    plt.xlabel('Hour')
    plt.legend(['Mean'])
    plt.title('All Trials Error Rate' )
        
    plt.xticks(np.arange(0,24,1),np.arange(0,24,1))
    plt.axis([-0.5,23.5,0,1])
    plt.hold(0)
    return()

def F_Error_Rate_New_plt_GUI(Correct_Rate,Ticks,color='b',meanColor='r',LenDark=12,
                             alpha=0.3,Title=None,correctRate=True):
    xaxis=list(range(len(Correct_Rate)))
    if correctRate:
        yaxis=1-Correct_Rate
    else:
        yaxis=Correct_Rate
    xEndDark=LenDark
    xStartDark=-0.5
    
    Ticks=np.array(Ticks)
    Mean=np.mean(yaxis)
    x=[-0.5,len(Correct_Rate)-0.5]
    y=[Mean,Mean]
    fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
    plt.hold(1)
    plt.plot(x,y,'--%s'%meanColor)
    plt.plot(xaxis,yaxis,'-o%s'%color)
    plt.xlabel('Time')
    plt.legend(['Mean'])
    if not Title:
        plt.title('All Trials Error Rate' )
    else:
        plt.title(Title)
    if len(Correct_Rate)>=10:
        xTicks = np.array(np.floor(np.arange(0,len(Correct_Rate),len(Correct_Rate)//10)),dtype=int  )
    else:
        xTicks = list(range(len(Ticks)))
    plt.xticks(xTicks,Ticks[xTicks])
    plt.axis([-0.5,len(Correct_Rate)-0.5,0,1])
    plt.grid()
    plt.axvspan(xStartDark,xEndDark,0,1,alpha=alpha)
    plt.hold(0)
    
    return(fig)

def F_Error_Bar_New_plt_GUI(yaxis,yerr,Ticks,color='b',meanColor='r',LenDark=12,
                             alpha=0.3,Title=None,yLabel=None,yLim=None):
    
    xaxis=list(range(len(yaxis)))
 
    xEndDark=LenDark-0.5
    xStartDark=-0.5
    
    Ticks=np.array(Ticks)
    Mean=np.nanmean(yaxis)
    x=[-0.5,len(yaxis)-0.5]
    y=[Mean,Mean]
    fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
    plt.hold(1)
    plt.plot(x,y,'--%s'%meanColor)
    plt.errorbar(xaxis,yaxis,yerr=yerr)
    plt.xlabel('Time')
    plt.legend(['Mean'])
    if not Title:
        plt.title('All Trials Error Rate' )
    else:
        plt.title(Title)
    if len(yaxis)>=10:
        xTicks = np.array(np.floor(np.arange(0,len(yaxis),len(yaxis)//10)),dtype=int  )
    else:
        xTicks = list(range(len(Ticks)))
    plt.xticks(xTicks,Ticks[xTicks])
    if not yLim:
        plt.xlim(-0.5,len(yaxis)-0.5)
    else:
        plt.axis([-0.5,len(yaxis)-0.5,yLim[0],yLim[1]])
    if yLabel:
        plt.ylabel(yLabel)
    plt.grid()
    plt.axvspan(xStartDark,xEndDark,0,1,alpha=alpha)
    plt.hold(0)
    
    return(fig)

def F_PeakProbes_plt_GUI(Peak,tend,t0,l_s,Title=None,*t_first_last):
    """
    Function Targets:   It prints a Peak distribution, red if long probes are
                        analyzed blue if short
                        
    Input:              -Peak =  vector containing the Peak precisure value
                        -tend = scalar, max time end of a trial
                        -t0 = scalar, target time
                        -l_s = string, 's' or 'l' to specify if short or long
                        trial are analyzed
                        -t_first_last = time interval we consider (we analyse
                        probe trial containedo in (t_first,t_last))
                        
    Output:             -Normalized peak precisure plot
                        
    """
    
    
    x_axis=np.arange(0,tend,1/100.0)
    if len(t_first_last)==2:
        Hstart=int(np.floor(t_first_last[0]/3600))
        Mstart=int(np.floor((t_first_last[0]-Hstart*3600)/60))
        
        Hend=int(np.floor(t_first_last[1]/3600))
        Mend=int(np.floor((t_first_last[1]-Hend*3600)/60))
        
        TimeSt='%d.%d' % (Hstart,Mstart)
        TimeEnd='%d.%d' % (Hend,Mend)
    else:
        TimeSt='0.00'
        TimeEnd='24.00'
    
    Iend=string.find(TimeEnd,'.')
    Istart=string.find(TimeSt,'.')
    
    if len(TimeEnd[Iend:])==2:
        TimeEnd=TimeEnd+'0'
    if len(TimeSt[Istart:])==2:
        TimeSt=TimeSt+'0'
    
    N_Peak=np.array(Peak,dtype=float)/np.max(Peak)
    if l_s=='s':  
        label='Short'
        color='r'
    elif l_s=='l':
        label='Long'
        color='b'
        
    opt_y=[0,1]
    opt_x=[t0,t0]
    fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
    if t0!=-1:
        plt.plot(x_axis,N_Peak,color,opt_x,opt_y,'k--')
    else:
        plt.plot(x_axis,N_Peak,color)
    plt.ylim(0,1)
    plt.xlabel('Time(sec)')
    plt.ylabel('Normalized Response Rate')
    if Title is  None:
        plt.title('%s Peak Distr.' % label)
    else:
        plt.title(Title)
    plt.text(23*tend/30,0.85,'Trials analized from %s to %s' % (TimeSt,TimeEnd),)
    plt.show()
    return(fig)
    
def F_Raster_Plt_GUI(Raster,strn,scale,*other):
    """
    Function Targets:           This function prints a raster plots from a raster
                                plt matrix.
                                
    Input:                      -Raster = matrix n'xtend*100 containing raster plot
                                -strn = string, 'l' or 's', to specify which location
                                (long/short) you're consiering
                                -scale = scalar, factor for rescaling time stamps
                                
    Output:                     -Raster plot graph
    """
    print(( 'len other: ', len(other)))
    if len(other) == 3:
        RR = [Raster, other[0]]
        strings = [strn, other[1]]
        scales = [scale, other[2]]
        fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
        plt.hold(1)
        XMIN,XMAX,YMIN,YMAX = np.inf, 0, np.inf, 0
        for k in [0, 1]:
            print(('k:',k))
            Raster = RR[k]
            strn = strings[k]
            scale = scales[k]
            end=Raster-np.hstack((Raster[:,1:],np.zeros((np.size(Raster,axis=0),1))))
            Ind=np.where(end==-1)
            Ind=(Ind[0],Ind[1]+1)
            v0=np.zeros((np.size(Raster,axis=0),np.size(Raster,axis=1)))
            v0[Ind]=1
            
            Ind=np.where(end==1)
            v1=np.zeros((np.size(Raster,axis=0),np.size(Raster,axis=1)))
            v1[Ind]=1
            
            I0=np.where(v0==1)
            I1=np.where(v1==1)
            scale=scale/10
            
            if strn=='l':
                string='long'
                color1='r'
                color2='or'
                label = 'NP right'
            else:
                string='short'
                color1='b'
                color2='ob'
                label = 'NP left'
            End_point=plt.plot(I1[1]/float(scale),I1[0]+1,'ow')
            St_point=plt.plot(I0[1]/float(scale),I0[0]+1,color2)
            Lines=plt.hlines(I0[0]+1,I0[1]/float(scale),I1[1]/float(scale),color1,label=label)
            xmin,xmax = plt.xlim()
            ymin,ymax = plt.ylim()
            XMIN = min(XMIN,xmin)
            XMAX = max(XMAX,xmax)
            YMIN = min(YMIN,ymin)
            YMAX = max(YMAX,ymax)
        plt.xlim(XMIN,XMAX)
        plt.ylim(YMIN,YMAX)
        if len(strings) == 2:
            string = 'left and right location'
        Title=plt.title('Raster plot: %s' % string)
        plt.legend()
        YLabel=plt.ylabel('Trial number')
        XLabel=plt.xlabel('Time(sec)')
    else:
        end=Raster-np.hstack((Raster[:,1:],np.zeros((np.size(Raster,axis=0),1))))
        Ind=np.where(end==-1)
        Ind=(Ind[0],Ind[1]+1)
        v0=np.zeros((np.size(Raster,axis=0),np.size(Raster,axis=1)))
        v0[Ind]=1
        I0=np.where(v0==1)
        Ind=np.where(end==1)
        
        v1=v0*0.
        v1[Ind]=1
        
        I0=np.where(v0==1)
        I1=np.where(v1==1)
        del v0,v1,Raster
        scale=scale/10
        
        if strn=='l':
            string='right location'
            color1='r'
            color2='or'
            
        else:
            string='left location'
            color1='b'
            color2='ob'
        fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
        End_point=plt.plot(I1[1]/float(scale),I1[0]+1,'ow')
        St_point=plt.plot(I0[1]/float(scale),I0[0]+1,color2)
        Lines=plt.hlines(I0[0]+1,I0[1]/float(scale),I1[1]/float(scale),color1)
    
        Title=plt.title('Raster plot: %s' % string)
        YLabel=plt.ylabel('Trial number')
        XLabel=plt.xlabel('Time(sec)')
        #plt.show()
        
    return(fig)

def Gr_BoxPlot_LD_GUI(Means,Hour_Light,Hour_Dark,Group_Name):
    """
    Function Target:    This function prints boxplots divided by light and dark phase 
                        of the vectors Means[name], for every group name.
                        
    Input:              -Means=dicitionary, Means[name]=vector,length 24, contains the vector
                        that we want to print as a boxplot, the i value corrisponds to a mean 
                        relative to hour i.
                        -Hour_Light/Dark=vector, contains the Light/Dark hours
                        -Group_Name=vector of strings, contains the name of each
                        group
                        
    Output:             -Box0= subplot of boxplot, one plot per group, divided by 
                        light and dark phase
                        -Box1/Box2=boxplot,  for dark/light phase
                        containing the boxplots of every group
    """
    
    n_row=len(Group_Name)/2+len(Group_Name)%2
    
    Ymin=np.min(list(Means.values()))*0.95
    Ymax=np.max(list(Means.values()))*1.05
    figDict = {}
    i=0
    if len(Group_Name)!=1:
        for i in range(len(Group_Name)):
            figDict[i] = plt.figure()
            
            plt.subplot(n_row,2,i+1)
            Box0=plt.boxplot([Means[Group_Name[i]][Hour_Dark], Means[Group_Name[i]][Hour_Light]])
            ticks,tmp=plt.xticks()
            plt.xticks(ticks,['Dark','Light'])
            plt.title(Group_Name[i])
            plt.ylim(Ymin,Ymax)
            
    else:
        figDict[i] = plt.figure()
        print('GR boxplot', Means[Group_Name[0]])
        plt.boxplot([Means[Group_Name[0]][Hour_Dark], Means[Group_Name[0]][Hour_Light]])
        ticks,tmp=plt.xticks()
        plt.xticks(ticks,['Dark','Light'])
        plt.ylim(Ymin,Ymax)
        plt.title(Group_Name[0])
    
    figDict[i+1] = plt.figure()
    Mean_Light=[[]]*len(Group_Name)
    Mean_Dark=[[]]*len(Group_Name)
    for i in range(len(Group_Name)):
        Mean_Light[i]=Means[Group_Name[i]][Hour_Light]
        Mean_Dark[i]=Means[Group_Name[i]][Hour_Dark]
    plt.subplot(1,2,1)
    
    plt.boxplot(Mean_Dark)
    ticks,tmp=plt.xticks()
    plt.xticks(ticks,Group_Name)
    plt.title('Dark')
    plt.ylim(Ymin,Ymax)
    
    plt.subplot(1,2,2)
    
    plt.boxplot(Mean_Light)
    ticks,tmp=plt.xticks()
    plt.xticks(ticks,Group_Name)
    plt.title('Light')
    plt.ylim(Ymin,Ymax)
    plt.show()
    return(figDict)

def Plt_RawPowerDensity_GUI(Freq, y_axis_list, color_list = ['r'],
                           linewidth = 2, legend_list = ['Wake'],
                           title = 'Power Density', title_size = 20, 
                           axis_label_size = 15,
                           legend_size = 15,ylim=None):
    """
        Function Target: 
        ================
            Plot the power density from input dataset
        Input:
        ======
            - Freq : numpy array
                x_axis vector
            - y_axis_list : list of numpy arrays
                each element of the list is a y_axis for delta power
        Output:
        =======
            - fig : matplotlib.figure.Figure
                The power density figure
    """
    fig = plt.figure(figsize=(4.5*3.13,3.5*3.13))
    plt.hold(1)        
    for k in range(len(y_axis_list)):
        plt.plot(Freq, y_axis_list[k], color = color_list[k],
                 linewidth = linewidth, label = legend_list[k])
    plt.title(title, fontsize = title_size)
    plt.xlabel('Frequency (Hz)', fontsize = axis_label_size)
    plt.ylabel('Power Density', fontsize = axis_label_size)
    plt.legend(fontsize = legend_size)
    plt.xlim(0,max(Freq))
    if type(ylim) is tuple:
        plt.ylim(ylim)
    plt.hold(0)
    return fig

def Plt_RawPowerDensity_Loop_GUI(Freq,Power_Wake,Power_Rem,Power_NRem,IndexGroup,
                             color_list = ['r','y','g'],linewidth = 2, 
                             legend_list = ['Wake','Rem','NRem'],
                             title_size = 20, axis_label_size = 15,
                             legend_size = 15):
    figDict = {}
    maxList = []
    for group in list(IndexGroup.keys()):
        for subject in list(IndexGroup[group].keys()):
            row = IndexGroup[group][subject]
            maxList += [np.max([np.max(Power_Wake[row]),np.max(Power_Rem[row]),
                                np.max(Power_NRem[row])])]
    ylim = (0,np.max(maxList)*1.05)
    for group in list(IndexGroup.keys()):
        for subject in list(IndexGroup[group].keys()):
            noext = subject.split('.')[0]
            title = 'Power Density\n%s (%s)'%(noext,group)
            row = IndexGroup[group][subject]
            y_axis_list = [Power_Wake[row],Power_Rem[row],Power_NRem[row]]
            figDict[subject] =\
                Plt_RawPowerDensity_GUI(Freq, y_axis_list,
                                        color_list = color_list,
                                        linewidth = linewidth,
                                        legend_list = legend_list,
                                        title = title,
                                        title_size = title_size, 
                                        axis_label_size = axis_label_size,
                                        legend_size = legend_size,ylim=ylim)
    return figDict

def Plt_MedianPowerDensity_GUI(Freq, PowerW_matrix, PowerR_matrix,
                               PowerNR_matrix, IndexArray_dict, 
                               color_list = ['k', 'r', 'b'],
                               linewidth = 2, legend_list = ['Wake', 'Rem',
                               'NRem'], suptitle = 'Power Density',
                               suptitle_size = 25, axis_label_size = 10,
                               legend_size = 15,title_size=15,
                               MeanOrMedian = 'Mean'):
    fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
    nrow = len(list(IndexArray_dict.keys()))
    ind = 1
    plt.hold(1)
    MAX_list = []
    for key in list(IndexArray_dict.keys()):
        Index   = IndexArray_dict[key]
        if MeanOrMedian == 'Median':
            PowerW  = np.nanmedian(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmedian(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmedian(PowerNR_matrix[Index],axis=0)

        else:
            PowerW  = np.nanmean(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmean(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmean(PowerNR_matrix[Index],axis=0)
            
        MAX_list += [np.max([np.max(PowerW),np.max(PowerNR),np.max(PowerR)])]
    ylim = (0,1.05*np.max(MAX_list))
    genotype_mean = {}
    gen_yer = {}
    for key in list(IndexArray_dict.keys()):
        plt.subplot(nrow,1,ind)
        Index   = IndexArray_dict[key]
        if MeanOrMedian == 'Median':
            PowerW  = np.nanmedian(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmedian(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmedian(PowerNR_matrix[Index],axis=0)
            
            PowerWs = np.percentile(PowerW_matrix[Index], 75, axis=0)
            PowerRs = np.percentile(PowerR_matrix[Index], 75, axis=0)
            PowerNRs = np.percentile(PowerNR_matrix[Index], 75, axis=0)
            
            error_high = np.array([PowerWs,PowerRs,PowerNRs])
            
            PowerWs = np.percentile(PowerW_matrix[Index], 25, axis=0)
            PowerRs = np.percentile(PowerR_matrix[Index], 25, axis=0)
            PowerNRs = np.percentile(PowerNR_matrix[Index], 25, axis=0)
            
            error_low = np.array([PowerWs,PowerRs,PowerNRs])
            gen_yer[key] = {'high':error_high,'low':error_low}
            genotype_mean[key] = [PowerW,PowerR,PowerNR]
            
        else:
            PowerW  = np.nanmean(PowerW_matrix[Index],axis=0)
            PowerR  = np.nanmean(PowerR_matrix[Index],axis=0)
            PowerNR = np.nanmean(PowerNR_matrix[Index],axis=0)
            
            PowerWs = sts.sem(PowerW_matrix[Index],axis=0)
            PowerRs = sts.sem(PowerR_matrix[Index],axis=0)
            PowerNRs = sts.sem(PowerNR_matrix[Index],axis=0)
            genotype_mean[key] = [PowerW,PowerR,PowerNR]
#        yVal = np.array([PowerW,PowerR,PowerNR])
            yErr = np.array([PowerWs,PowerRs,PowerNRs])
            gen_yer[key] = yErr
        plt.title('Genotype: %s'%key, fontsize = title_size)
        plt.xlabel('Frequency (Hz)', fontsize = axis_label_size)
        plt.ylabel('Power Density', fontsize = axis_label_size)
        PP = [PowerW,PowerR,PowerNR]
        legend_list = []
        for k in range(3):
#            plt.plot(Freq, PP[k], color = color_list[k],
#                 linewidth = linewidth, label = legend_list[k])
            if MeanOrMedian == 'Median':
                legend_list += [plt.errorbar(Freq, PP[k],yerr=np.vstack([error_low[k,:], error_high[k,:]]),color = color_list[k])]
            else:
                legend_list += [plt.errorbar(Freq, PP[k],yerr=yErr[k,:],color = color_list[k])]
        plt.legend(legend_list,['Wake','REM','NREM'],fontsize = legend_size)
        ind += 1
        plt.ylim(ylim)  
        plt.xlim(0,max(Freq))
    plt.suptitle(suptitle, fontsize = suptitle_size)
    plt.hold(0)
    plt.hold(1)
    list_title = ['Power Wake','Power REM','Power NREM']
    tuple_fig = ()
    color_list = ['k', 'r', 'b','g','y',(125./255,)*3,'m','c']
    for k in range(3):
        tuple_fig += (plt.figure(figsize=(5.5*3.13,3.5*3.13)),)
        legend_list = []
        legend_lab = []
        plt.title(list_title[k],fontsize=20)
        i = 0
        for key in list(IndexArray_dict.keys()):
            if type(gen_yer[key]) is dict:
                legend_list += [plt.errorbar(Freq, genotype_mean[key][k],yerr=np.vstack([gen_yer[key]['low'][k,:], gen_yer[key]['high'][k,:]]),color=color_list[i%len(color_list)])]
            else:
                legend_list += [plt.errorbar(Freq, genotype_mean[key][k],yerr=gen_yer[key][k],color=color_list[i%len(color_list)])]
            legend_lab += [key]
            i += 1
        plt.xlabel('Frequency (Hz)', fontsize = axis_label_size)
        plt.ylabel('Power Density', fontsize = axis_label_size)
        plt.legend(legend_list,legend_lab,fontsize = legend_size)
    plt.hold(0)
    return (fig,) + tuple_fig
def CDF_average_plot_GUI(Cdf,EmCdf,Group_Name,Mouse_Grouped,t0=3,t1=6):
    
   
    x = np.linspace(0,t0+t1,1000)
    
    fig=plt.figure('CDF average')
    
    Num_Group=len(Group_Name)
    Row_Num=np.ceil(Num_Group/2.)
    i=1

    plt.hold(1)
    print('\n\n%s\n=========\n\n'%Group_Name,Row_Num)

    for group in Group_Name:
        mn = np.zeros((Mouse_Grouped[group].__len__()),dtype = float)*np.nan
        cv = np.zeros((Mouse_Grouped[group].__len__()),dtype = float)*np.nan
        kk = 0
        for name in Mouse_Grouped[group]:
            mn[kk] = np.nanmean(Cdf[name]['x'])
            cv[kk] = np.cov(Cdf[name]['x'])
            kk += 1
            
        avg = sts.norm(np.mean(mn),np.sum(cv**0.5)/10.)
        plt.plot(x,avg.cdf(x),linewidth=2,label = group)
        plt.ylim(0,1)
        plt.plot([t0,t0],[0,1],'--k')
        plt.plot([t1,t1],[0,1],'--k')
        plt.title('Group switch latency')
        plt.xlabel('Switch Latency(sec)')
        plt.ylabel('Cumulative Probability')
        plt.legend()
        i+=1
    
    plt.hold(0)
    plt.show()
    return(fig)
    
def CDF_Gr_Plot_GUI(Cdf,EmCdf,Group_Name,Mouse_Grouped,t0=3,t1=6):
    """
    Function Target:    This function prints the cdf theo and empirical.
    
    Input:              -Cdf=dictionary, keys=mouse name
                            -Cdf[name]=Cdf theorical of the GMM relative to mouse name
                        -EmCdf=dictionary, keys=mouse name
                            -EmCdf[name]=vector, empirical cdf relative to mouse name
                        -Group_Name=list of group names
                        -Mouse_Grouped=dictionary, keys=group name
                            -Mouse_Grouped[group]=list of mouse name in the group
                        -t0/t1=sec of the switch
                        
    Output:             -fig=Empirical and theorical cdfs graph
    """
    Num_Group=len(Group_Name)
    Row_Num=np.ceil(Num_Group/2.)
    i=1
    fig=plt.figure('CDF')
    plt.hold(1)
    print('\n\n%s\n=========\n\n'%Group_Name,Row_Num)
    if Num_Group == 1:
        col = 1
    else:
        col = 2
    for group in Group_Name:
        plt.subplot(Row_Num,col,i)
        for name in Mouse_Grouped[group]:
            plt.plot(Cdf[name]['x'],Cdf[name]['y'],'b')
            plt.plot(EmCdf[name]['x'],EmCdf[name]['y'],'r')
            plt.legend(['GMM Fit','Raw'])
        plt.ylim(0,1)
        plt.plot([t0,t0],[0,1],'--k')
        plt.plot([t1,t1],[0,1],'--k')
        plt.title(group)
        plt.xlabel('Switch Latency(sec)')
        plt.ylabel('Cumulative Probability')
        i+=1
    plt.hold(0)
    plt.show()
    return(fig)

def Plt_ErrorBar_Gr_DeltaReb(Mean, SEM, TimeLim, Colors = None,
                             GroupLabel = ['Wt','Mut'],
                             TimeBin_Sec = 3600, NumTicks = 10,
                             linewidth = 2, elinewidth=2.5, ticksize=12,
                             titlesize = 20, labelsize = 15):
    fig = plt.figure()
    plt.hold(1)
    for key in list(Mean.keys()):
        if not key in GroupLabel:
            raise ValueError('GroupLabel must be a list containing keys of\
                                Mean dicitonary')
    ind = 0
    for key in GroupLabel:
        Sec_0 = TimeLim[0].second + TimeLim[0].minute * 60\
                + TimeLim[0].hour * 3600
        TimeBinVect = (np.arange(len(Mean[key]))*TimeBin_Sec) + Sec_0
        print((type(Colors)))
        if Colors is None:
            plt.errorbar(TimeBinVect , Mean[key], yerr = SEM[key],
                         elinewidth = elinewidth, linewidth = linewidth, 
                         label = key)
        else:
            plt.errorbar(TimeBinVect , Mean[key], yerr = SEM[key],
                         elinewidth = elinewidth, linewidth = linewidth, 
                         label = key, color = Colors[ind],
                         ecolor = Colors[ind])
            
            ind += 1
    StepTicks   = int(np.ceil(len(TimeBinVect)/float((NumTicks))))
    TickLabel_x =  np.hstack((TimeBinVect[::StepTicks][:-1],
                                  TimeBinVect[-1]))
    TickLabel = TimeUnit_to_Hours_GUI(TickLabel_x, 1)
    plt.xticks(TickLabel_x,TickLabel,fontsize = ticksize)
    plt.xlim(TimeBinVect[0]*0.95,
             TimeBinVect[-1] + TimeBinVect[0]*0.05)
    plt.title('Delta rebound', fontsize = titlesize)
    plt.xlabel('Time', fontsize = labelsize)
    plt.ylabel('EEG Delta Power', fontsize = labelsize)
    plt.legend()
    plt.hold(0)
    return fig

def plot_LDA_GUI(lda, X, y, y_pred,titlelabel='Linear Discriminant Analysis',
                 labelHourDark = None, labelHourLight = None,
                 x_label = 'Sleep episod duration', x_label_size = 15,
                 y_label = 'Error rate', y_label_size = 15,
                 title_size = 20, color=False, markersize=12,
                 phaseLabel=['Dark phase','Light phase']):
    
    fig = plt.figure(figsize=(4.*3.13,3*3.13))
    plt.hold(1)
    plt.title(titlelabel, fontsize = title_size)
#    plt.ylabel('Data with fixed covariance')
    
    tp = (y == y_pred)  # True Positive
    tp0, tp1 = tp[y == 0], tp[y == 1]
    X0, X1 = X[y == 0], X[y == 1]
    X0_tp, X0_fp = X0[tp0], X0[~tp0]
    X1_tp, X1_fp = X1[tp1], X1[~tp1]


    # class 0: dots
    plt.plot(X0_tp[:, 0], X0_tp[:, 1], 'o', color='blue',
             markersize=markersize,label = phaseLabel[0])
    plt.plot(X0_fp[:, 0], X0_fp[:, 1], 's', color='#000099',
             markersize=markersize)  # dark red

    # class 1: dots
    plt.plot(X1_tp[:, 0], X1_tp[:, 1], 'o', color='red',markersize=markersize,
             label=phaseLabel[1])
    plt.plot(X1_fp[:, 0], X1_fp[:, 1], 's', color='#990000',
             markersize=markersize)  # dark blue
    plt.legend()
    # class 0 and 1 : areas
    nx, ny = 200, 100
    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()
    
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, nx),
                         np.linspace(y_min, y_max, ny))
    Z = lda.predict_proba(np.c_[xx.ravel(), yy.ravel()])
    Z = Z[:, 1].reshape(xx.shape)
    if color:
        cm = plt.pcolormesh(xx, yy, Z, cmap='red_blue_classes',
                   norm=colors.Normalize(0., 1.))
        cbar = plt.colorbar(cm)
        cbar.ax.set_ylabel('Posterior classicication probability',fontsize=15)
    plt.contour(xx, yy, Z, [0.5], linewidths=2., colors='k')
    
    if not (labelHourDark is None):
        Dy = (y_max - y_min)*0.02
        for t in range(len(X0)):
            plt.text(X0[t,0],X0[t,1] + Dy, labelHourDark[t],fontsize = 12)
            plt.text(X1[t,0],X1[t,1] + Dy, labelHourLight[t],fontsize = 12)
    plt.xlabel(x_label,fontsize = x_label_size)
    plt.ylabel(y_label,fontsize = y_label_size)
    plt.hold(0)
    return fig

def plot_LDA_Group_GUI(lda_dict, X_dict, y_dict, y_pred_dict,color_dict,
                       titlelabel='Linear Discriminant Analysis',
                       labelHourDark = None, labelHourLight = None,
                       x_label = 'Sleep episod duration', x_label_size = 15,
                       y_label = 'Error rate', y_label_size = 15,
                       title_size = 20, color=False, markersize=12,
                       phaseLabel=['Dark phase','Light phase'],
                       markerface=['k','y'],newfig=True):
    if newfig:
        fig = plt.figure(figsize=(4.*3.13,3*3.13))
    plt.hold(1)
    for key in list(lda_dict.keys()):
#        lda = lda_dict[key]
        X = X_dict[key]
        y = y_dict[key]
        y_pred = y_pred_dict[key]
        plt.title(titlelabel, fontsize = title_size)
#    plt.ylabel('Data with fixed covariance')
    
        tp = (y == y_pred)  # True Positive
        tp0, tp1 = tp[y == 0], tp[y == 1]
        X0, X1 = X[y == 0], X[y == 1]
        X0_tp, X0_fp = X0[tp0], X0[~tp0]
        X1_tp, X1_fp = X1[tp1], X1[~tp1]
    
    
        # class 0: dots
#        print(color_dict) 
        plt.plot(X0_tp[:, 0], X0_tp[:, 1], linestyle=' ',
                 marker='o', markeredgecolor=color_dict[key],markeredgewidth=2,
                 markerfacecolor=markerface[0],
                 markersize=markersize,label='%s: %s'%(key,phaseLabel[1]))
        plt.plot(X0_fp[:, 0], X0_fp[:, 1], linestyle=' ',
                 marker='s', markeredgecolor=color_dict[key],markeredgewidth=2,
                 markerfacecolor=markerface[1],
                 markersize=markersize)  
    
        # class 1: dots
        plt.plot(X1_tp[:, 0], X1_tp[:, 1], linestyle=' ',
                 marker='o', markeredgecolor=color_dict[key],markeredgewidth=2,
                 markerfacecolor=markerface[1],
                 markersize=markersize,label='%s: %s'%(key,phaseLabel[0]))
        plt.plot(X1_fp[:, 0], X1_fp[:, 1], linestyle=' ',
                 marker='s', markeredgecolor=color_dict[key],markeredgewidth=2,
                 markerfacecolor=markerface[1],
                 markersize=markersize)
        # class 0 and 1 : areas
#        nx, ny = 200, 100
        x_min, x_max = plt.xlim()
        y_min, y_max = plt.ylim()
        
#        xx, yy = np.meshgrid(np.linspace(x_min, x_max, nx),
#                             np.linspace(y_min, y_max, ny))
#        Z = lda.predict_proba(np.c_[xx.ravel(), yy.ravel()])
#        Z = Z[:, 1].reshape(xx.shape)
#        if color:
#            cm = plt.pcolormesh(xx, yy, Z, cmap='red_blue_classes',
#                       norm=colors.Normalize(0., 1.))
#            cbar = plt.colorbar(cm)
#            cbar.ax.set_ylabel('Posterior classicication probability',fontsize=15)
#        coefAng = lda[key].coef_[0]/lda[key].coef_[1]
#        intercept = lda[key].intercept_[0]/lda[key].coef_[1]
#        plt.contour(xx, yy, Z, [0.5], linewidths=2., colors=color_dict[key])
        
        if not (labelHourDark is None):
            Dy = (y_max - y_min)*0.02
            for t in range(len(X0)):
                plt.text(X0[t,0],X0[t,1] + Dy, labelHourDark[t],fontsize = 12)
                plt.text(X1[t,0],X1[t,1] + Dy, labelHourLight[t],fontsize = 12)
        plt.xlabel(x_label,fontsize = x_label_size)
        plt.ylabel(y_label,fontsize = y_label_size)
    
    plt.legend()

    plt.hold(0)
    if not newfig:
        return
    return fig

def plot_Standard_Input_Error_Bar_GUI(stdGroupMatrix, Dark_length,
                                  TimeInterval, title, x_label,
                                  y_label, title_size = 20, 
                                  label_size = 15, tick_size = 12,
                                  legend_size = 15,
                                  hold_on = True, stat_ind = 'Mean',
                                  linewidth = 1.5, elinewidth = 2,
                                  tick_every = 4, alpha = 0.4):
    if 3600 % TimeInterval != 0  and TimeInterval % 3600 != 0:
        raise ValueError('TimeInterval must divide or be a multiple of 3600!')
    Num_Hour_Dark  = int(np.ceil(Dark_length * (3600.0 / TimeInterval)))
    GroupList = np.unique(stdGroupMatrix['Group'])
    if not hold_on:
        fig = {}
    else:
        fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
        plt.hold(True)
    for group in GroupList:
        y_axis = stdGroupMatrix[stat_ind]\
            [np.where(stdGroupMatrix['Group']==group)[0]]
        y_err = stdGroupMatrix['SEM']\
            [np.where(stdGroupMatrix['Group']==group)[0]]
        ticks = stdGroupMatrix['Time']\
            [np.where(stdGroupMatrix['Group']==group)[0]]
        if (not hold_on):
            fig[group] = plt.figure(figsize=(5.5*3.13,3.5*3.13))
        x_axis = list(range(len(y_axis)))
        plt.errorbar(x_axis, y_axis, yerr= y_err,
                     linewidth = linewidth, elinewidth = elinewidth,
                     label = group)
        plt.legend(fontsize = label_size)
        plt.xticks(x_axis[::tick_every], ticks[::tick_every], fontsize = tick_size)
        plt.title(title, fontsize = title_size)
        plt.ylabel(y_label, fontsize = label_size)
        plt.xlabel(x_label, fontsize = label_size)
        if not hold_on:
            ymin, ymax = plt.ylim()
            plt.axvspan(-0.5, Num_Hour_Dark - 0.5, ymin, ymax, alpha = alpha)
    if hold_on:
        ymin, ymax = plt.ylim()
        plt.axvspan(-0.5, Num_Hour_Dark - 0.5, ymin - 100, ymax + 100,
                    alpha = alpha)
    xmax = plt.xlim()[1]
    plt.xlim(-0.5, xmax + 0.5)
    plt.ylim(ymin, ymax)
    return fig

def plot_Standard_Input_Error_Rate_GUI(stdGroupMatrix, Dark_length,
                                  TimeInterval, title, x_label,
                                  y_label, title_size = 20, 
                                  label_size = 15, tick_size = 12,
                                  legend_size = 15,
                                  hold_on = True, stat_ind = 'Mean',
                                  linewidth = 1.5, elinewidth = 2,
                                  tick_every = 4, alpha = 0.4):
    if 3600 % TimeInterval != 0  and TimeInterval % 3600 != 0:
        raise ValueError('TimeInterval must divide or be a multiple of 3600!')
    Num_Hour_Dark  = int(np.ceil(Dark_length * (3600.0 / TimeInterval)))
    GroupList = np.unique(stdGroupMatrix['Group'])
    if not hold_on:
        fig = {}
    else:
        fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
        plt.hold(True)
    colorList = []
    for group in GroupList:
        y_axis = stdGroupMatrix[stat_ind]\
            [np.where(stdGroupMatrix['Group']==group)[0]]
        y_err = stdGroupMatrix['SEM']\
            [np.where(stdGroupMatrix['Group']==group)[0]]
        ticks = stdGroupMatrix['Time']\
            [np.where(stdGroupMatrix['Group']==group)[0]]
        if (not hold_on):
            fig[group] = plt.figure(figsize=(5.5*3.13,3.5*3.13))
        x_axis = list(range(len(y_axis)))
        p=plt.errorbar(x_axis, y_axis, yerr= y_err,
                     linewidth = linewidth, elinewidth = elinewidth,
                     label = group)
        colorList += [p.lines[0].get_color()]
        plt.legend(fontsize = label_size)
        plt.xticks(x_axis[::tick_every], ticks[::tick_every], fontsize = tick_size)
        plt.title(title, fontsize = title_size)
        plt.ylabel(y_label, fontsize = label_size)
        plt.xlabel(x_label, fontsize = label_size)
        if not hold_on:
            ymin, ymax = plt.ylim()
            plt.axvspan(-0.5, Num_Hour_Dark - 0.5, ymin, ymax, alpha = alpha)
    if hold_on:
        ymin, ymax = plt.ylim()
        plt.axvspan(-0.5, Num_Hour_Dark - 0.5, ymin - 100, ymax + 100,
                    alpha = alpha)
    xmax = plt.xlim()[1]
    plt.xlim(-0.5, xmax + 0.5)
#    plt.ylim(ymin, ymax)
    plt.ylim(0, 1)

    fig1 = plt.figure()
    plt.hold(True)
    x_axis = []
    y_axis = []
    ind = 0
    plt.suptitle('Error Rate',fontsize='xx-large')
    for phase in ['Light','Dark']:
        plt.subplot(1,2,ind + 1)
        plt.title(phase,fontsize='large')
        x_axis = list(range(len(GroupList)))
        y_axis = []
        y_err = []
        for group in GroupList:
            if phase == 'Dark':
                y_axis += [np.nanmean(stdGroupMatrix[stat_ind]\
                    [np.where(stdGroupMatrix['Group']==group)[0]]\
                    [:Num_Hour_Dark])]
            
                y_err += [np.nanmean(stdGroupMatrix['SEM']\
                    [np.where(stdGroupMatrix['Group']==group)[0]]\
                    [:Num_Hour_Dark])]
            else:
                y_axis += [np.nanmean(stdGroupMatrix[stat_ind]\
                    [np.where(stdGroupMatrix['Group']==group)[0]]\
                    [Num_Hour_Dark:])]
            
                y_err += [np.nanmean(stdGroupMatrix['SEM']\
                    [np.where(stdGroupMatrix['Group']==group)[0]]\
                    [Num_Hour_Dark:])]
        ticks = GroupList
        
        plt.bar(x_axis , y_axis, 0.4,
                align='center', color=colorList, ecolor='r')
        for kk in range(len(y_axis)):
            plt.errorbar([x_axis[kk]] , [y_axis[kk]], yerr=[y_err[kk]],fmt=None,
                align='center', ecolor=colorList[kk], elinewidth=1.5)
        plt.xticks(x_axis,ticks,fontsize='medium')
        Argmax = np.argmax(y_axis)
        y_max = max(1, y_axis[Argmax]+y_err[Argmax])
        plt.ylim(0,y_max)
        plt.xlim(-0.5,len(x_axis)-0.5)
        ind += 1
    return fig,fig1

#def std_Bar_Plot(std_Matrix, title, title_size=20, linewidth=1, elinewidth=3,
#                 rescaleBy=1.0, treshold=0.95, y_label='', label_size=12,
#                 tick_size=15):
#    """
#        Function Target:
#        ================
#            This function plots a bar graph with std_Matrix values
#            averaged group by group. It normalizes all values by the factor
#            rescaleBy
#        Input:
#        ======
#            - std_Matrix : numpy structured array
#                Matrix containing values we want to plot: must have a column
#                'Value' or a column 'Mean' and a clumn 'Group'.
#            - title : string
#                Title of the plot
#        Output:
#        =======
#            - Average bar graph with sem
#    """
#    Groups = np.unique(std_Matrix['Group'])
#    if 'Mean' in std_Matrix.dtype.names:
#        varName = 'Mean'
#    elif 'Value' in std_Matrix.dtype.names:
#        varName = 'Value'
#    else:
#        raise ValueError('stdMatrix must have column \'Mean\' or \'Value\'')
#    std_Matrix[varName] = std_Matrix[varName] / rescaleBy
#    Mean = []
#    SEM = []
#    for group in Groups:
#        grIndex = np.where(std_Matrix['Group'] == group)[0]
#        Mean += [np.nanmean(std_Matrix[varName][grIndex])]
#        SEM += [np.nanstd(std_Matrix[varName][grIndex])/np.sqrt(len(grIndex))]
#    x_axis = range(len(Mean))
#    fig = plt.figure(figsize=(5.5*3.13,3.5*3.13))
#    plt.hold(1)
#    colorList = ('b', 'g', 'c', 'y', 'm', 'k')
#    for k in x_axis:
#        plt.bar([k], [Mean[k]], yerr=[SEM[k]], align='center',
#                color=colorList[k],
#                linewidth=linewidth, width=0.3,
#                error_kw={'elinewidth' : elinewidth, 'ecolor' : 'r'})
#    plt.xticks(x_axis, Groups, fontsize=tick_size)
#    plt.ylabel(y_label, fontsize=label_size)
#    plt.xlim(-0.5, len(Groups) - 0.5)
#    plt.ylim(0, 1.2)
#    if 0 <= treshold <= 1:
#        plt.plot([-0.5, len(Groups) - 0.5], [treshold, treshold], '--r')
#        ticks = list(plt.yticks()[0])
#        bisect.insort_right(ticks, treshold)
#        plt.yticks(ticks,ticks)
#    plt.title(title, fontsize=title_size)
#    plt.hold(0)
#    return fig

def plt_Best_Period(Period_Array, Best_Fit_Param, subject=''):
    fig = plt.figure()
    plt.hold(1)
    plt.plot(Best_Fit_Param['Period'], Best_Fit_Param['Pearson corr'],
             'or')
    plt.plot(Period_Array['Period'], Period_Array['Pearson corr'],
             linewidth = 2)
    xticks,tmp = plt.xticks()
    xticks = list(xticks)
    bisect.insort_left(xticks,Best_Fit_Param['Period'])
    tickList = []
    for k in xticks:
        tickList += ['%.2f'%k]
        if tickList[-1].endswith('.00'):
            tickList[-1] = tickList[-1][:-3]
    try:
        tickList.remove('24')
        xticks.remove(24.)
    except ValueError as inst:
        print(inst.message)
        
    plt.xticks(xticks,tickList,fontsize='large')
    plt.yticks(fontsize='large')
    plt.plot([Best_Fit_Param['Period']]*2,[0,1],'--r')
    plt.title('Periodicity extraction: best fit\n' + subject, fontsize=20)
    plt.xlabel('Periodicity(h)',fontsize='x-large')
    plt.ylabel('Correlation',fontsize='x-large')
    ymax = max(0.7, Best_Fit_Param['Pearson corr'] + 0.1)
    plt.ylim(0,ymax)
    return fig

def std_Bar_Plot_GUI(std_Matrix_input, title, title_size=20, linewidth=1,
                     elinewidth=3, rescaleBy=1.0, treshold=0.95, y_label='',
                     label_size=12, tick_size=15):
    """
        Function Target:
        ================
            This function plots a bar graph with std_Matrix values
            averaged group by group. It normalizes all values by the factor
            rescaleBy
        Input:
        ======
            - std_Matrix : numpy structured array
                Matrix containing values we want to plot: must have a column
                'Value' or a column 'Mean' and a clumn 'Group'.
            - title : string
                Title of the plot
        Output:
        =======
            - Average bar graph with sem
    """
    std_Matrix = copy(std_Matrix_input)
    Groups = np.unique(std_Matrix['Group'])
    if 'Mean' in std_Matrix.dtype.names:
        varName = 'Mean'
    elif 'Value' in std_Matrix.dtype.names:
        varName = 'Value'
    else:
        raise ValueError('stdMatrix must have column \'Mean\' or \'Value\'')
    std_Matrix[varName] = std_Matrix[varName] / rescaleBy
    Mean = []
    SEM = []
    for group in Groups:
        grIndex = np.where(std_Matrix['Group'] == group)[0]
        Mean += [np.nanmean(std_Matrix[varName][grIndex])]
        SEM += [np.nanstd(std_Matrix[varName][grIndex])/np.sqrt(len(grIndex))]
    x_axis = list(range(len(Mean)))
    fig = plt.figure(figsize=(4.5*3.13,3.5*3.13))
    plt.hold(1)
    colorList = ('b', 'g', 'c', 'y', 'm', 'k',(1,69/255.,0/255.),'r')
    for k in x_axis:
        plt.bar([k], [Mean[k]], yerr=[SEM[k]], align='center',
                color=colorList[k],
                linewidth=linewidth, width=0.3,
                error_kw={'elinewidth' : elinewidth, 'ecolor' : 'r'})
    plt.xticks(x_axis, Groups, fontsize=tick_size)
    plt.ylabel(y_label, fontsize=label_size)
    plt.xlim(-0.5, len(Groups) - 0.5)
    plt.ylim(0, 1.2)
    if 0 <= treshold <= 1:
        plt.plot([-0.5, len(Groups) - 0.5], [treshold, treshold], '--r')
        ticks = list(plt.yticks()[0])
        bisect.insort_right(ticks, treshold)
        plt.yticks(ticks,ticks)
    plt.title(title, fontsize=title_size)
    plt.hold(0)
    return fig

def lineFunc(x, m, q):
    return m * x + q

def F_ExpGain_Plt_GUI(ExpLog, MaxRowl, Mean_minmax=(1, 9),
                      Cv_minmax=(0.05, 0.5), std_Exp_Gain=None,
                      marker_size=15, legend_size=12,color_std=None,
                      new_fig=True,color_bar=False):
    """
    Function Target:
    ================
        This function print an image of the expected gain for different average 
        switch time and Coeff. of variation (Cv) and also a plot a graph of best
        average switch time as a function of Cv.
                        
    Input:
    ======
        - ExpLog : numpy array, shape = n x n
            ExpLog[i,j] = exp. gain for mean switch time of i sec and Cv of j.
        - MaxRowl : numpy array, shape = n x 1
            Max exp gain over all Cv values for every fixed mean switch time 
        - Mean_minmax : tuple
            2 elements, extreme values of the mean switch time.
            Default min is 1 sec and default max is 9 sec
        - Cv_minmax : tuple
            2 elements, extreme values of CV. Default min is 0.05, 
            default max is 0.5
                        
    Output:
    =======
        - fig : figure representing the expected gain
    """
    Mesh = len(ExpLog[:,0])
    Norm_ExpLog = np.zeros((Mesh,len(ExpLog[0,:])))
    for i in range(Mesh):
        Norm_ExpLog[i,:] = ExpLog[i,:] / max(ExpLog[i,:])
    fig = plt.figure()
    plt.hold(1)
    ax = plt.subplot(111)
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    plt.title('Expected Gain', fontsize='large')
    img = plt.imshow(Norm_ExpLog, cmap = plt.cm.Greys_r)
    plt.plot(MaxRowl, list(range(Mesh)), color = 'r')
    plt.gca().invert_yaxis()
    if color_bar:
        plt.colorbar(img)
    plt.xlim(0, Mesh)
    plt.ylim(0, Mesh)
    
    
    y, tmp = plt.yticks()
    YTicks = np.linspace(Cv_minmax[0], Cv_minmax[1], len(y))
    plt.yticks(y, YTicks)
    xmin, xMax = plt.xlim()
    ymin, yMax = plt.ylim()
    m_resc_x = (xMax - xmin) / (Mean_minmax[1] -Mean_minmax[0])
    q_resc_x = xmin -  Mean_minmax[0] * m_resc_x
    m_resc_y = (yMax - ymin) / (Cv_minmax[1] -  Cv_minmax[0])
    q_resc_y = ymin -  Cv_minmax[0] * m_resc_y
    if not (std_Exp_Gain is None):
        color = ['b', 'g', 'c', 'y', 'm', 'k',(1,69/255.,0/255.),'r']
        Groups = np.unique(std_Exp_Gain['Group'])
        ind = 0
        for group in Groups:
            IndGr = np.where(std_Exp_Gain['Group'] == group)[0]
            xnew = lineFunc(std_Exp_Gain['Fit Mean'][IndGr], m_resc_x,
                            q_resc_x)
            ynew = lineFunc(std_Exp_Gain['Fit CV'][IndGr], m_resc_y,
                            q_resc_y)
            if not color_std is None:
                plt.scatter(xnew, ynew, c=color_std,
                       s=marker_size, label=group)
            else:
                plt.scatter(xnew, ynew, c=color[ind%len(color)],
                       s=marker_size, label=group)
            ind += 1
        plt.legend(fontsize=legend_size)
    x = np.linspace(xmin, xMax, Mean_minmax[1])
    plt.xticks(x, np.arange(Mean_minmax[0],Mean_minmax[1]+1))
    plt.xlabel('Mean')
    plt.ylabel('Coefficient of Variation (CV)')
    plt.hold(0)
    return(fig)

def std_ErrorBar_Plt_TimeCourse_GUI(std_Matrix_Group, title, x_label,
                                y_label, hold_on=True, 
                                stat_index='Mean', elinewidth=1.5,
                                title_size=20, tick_size=12, label_size=15,
                                tick_Num=10):
    Groups = np.unique(std_Matrix_Group['Group'])
    vectTime = np.unique(std_Matrix_Group['Time'])
    if len(vectTime[0]) == 19:
        ind = 0
        for t in vectTime:
            vectTime[ind] = '%d:'%int(t[-8:-6]) + t[-5:-3]
            ind += 1
    if hold_on:
        fig = plt.figure()
        plt.hold(True)
    else:
        fig = {}
    for group in Groups:
        if not hold_on:
            fig[group] = plt.figure()
        y_axis = std_Matrix_Group[stat_index][np.where(std_Matrix_Group['Group'] == group)[0]]
        if stat_index == 'Mean':
            y_err = std_Matrix_Group['SEM'][np.where(std_Matrix_Group['Group'] == group)[0]]
        elif stat_index == 'Median':
            y_err = [std_Matrix_Group['25 perc'][np.where(std_Matrix_Group['Group'] == group)[0]],
                     std_Matrix_Group['75 perc'][np.where(std_Matrix_Group['Group'] == group)[0]]]
        x_axis = np.arange(len(y_axis))
        plt.errorbar(x_axis, y_axis, yerr=y_err, label=group,
                     elinewidth=elinewidth)
        plt.xlabel(x_label, fontsize=label_size)
        plt.ylabel(y_label, fontsize=label_size)
        tick = vectTime[::len(vectTime)//tick_Num]
        xtick = x_axis[::len(vectTime)//tick_Num]
        plt.xticks(xtick, tick, fontsize=tick_size)
        if not hold_on:
            plt.title(title+'\n%s'%group, fontsize=title_size)
        else:
            plt.title(title, fontsize=title_size)
    if hold_on:
        plt.legend()
    xmin,xmax = plt.xlim()
    delta = (xmax-xmin) * 0.02
    plt.xlim(xmin - delta, xmax + delta)
    return fig

def plot_Rsquared_Grid_GUI(regressionModels, title='Predictor comparison',
                           x_label='Observation', y_label='Predictor sleep',
                           label_size=10, title_size=20, rotation=0,
                           reorderObs=None, reorderPred=None,vmin=-1,
                           vmax=1):
    """
        Function Target:
        ================
            This function deslplay an heat map of the R-quared extracted by
            the 'multipleRegressionProcedure' function
        Input:
        ======
            - regressionModels : dictionary, keys = observation name
                - regressionModels[obs] : dictionary, keys = genotypes
                - regressionModels[obs][gen] : dictionary, keys = predictor
                    circadian
                - regressionModels[obs][gen][pred1] : dictionary, keys =
                    predictor sleep
                - regressionModels[obs][gen][pred1][pred2] : object, class
                    multiple_Regression
                    Contains informations abuout the best fit model of the
                    multiple regression procedure
            - title : string
                Title string
            - x_label/y_label : string
                x label/y label string
            - label_size : int
                Font size of the labels
            - title_size : int
                Fontsize for the title
            - rotation : int
                Rotation of the ticks (angle)
            - reorderObs : list
                List of integer that will be used to reorder observation names
                that are returned by regressionModels.keys()
            - reorderPred : list
                List of integer that will be used to reorder predictors
        Output:
            - fig : dictionary, keys= genotype
                - fig[key] : figure
                    Heat map for R-squared of best fit
    """
#    print title, x_label,y_label,label_size
    observationList = list(regressionModels.keys())
    if reorderObs != None:
        observationList = np.array(observationList)[reorderObs]
    else:
        observationList.sort()
    genotypeList = list(regressionModels[observationList[0]].keys())
    predictorCircadian = list(regressionModels[observationList[0]]\
        [genotypeList[0]].keys())[0]
    predictorSleepList = list(regressionModels[observationList[0]]\
        [genotypeList[0]][predictorCircadian].keys())
    if reorderPred != None:
        predictorSleepList = np.array(predictorSleepList)[reorderPred][::-1]
    else:
        predictorSleepList.sort()
    genotypeList.sort()
    signedRsquared = {}
    figdict = {}
    ticksPos = np.linspace(-1, 1, 9)
    ticks = list(np.array(ticksPos, dtype='S5'))
    ticks[-1] = 'Sleep'
    ticks[0] = 'Circadian'
    xtickList = []
    for obs in observationList:
        xtickList += [obs.split('.')[0]]
    ytickList = []
    for sleep in predictorSleepList:
        ytickList += [sleep.split('.')[0]]
    for genotype in genotypeList:
        R_squared = np.zeros((len(predictorSleepList), len(observationList)))
        for j in range(len(observationList)):
            for k in range(len(predictorSleepList)):
                reg = regressionModels[observationList[j]][genotype]\
                    [predictorCircadian][predictorSleepList[k]]
#                print reg
                try:
                    if 'x1' in reg.model and 'x2' in reg.model:
                        minInd = np.argmin(reg.bestFit['p_value'][1:])
                        if reg.selectedVariables[minInd - 1]==predictorCircadian:
                            R_squared[k, j] = -1 * reg.bestFit['R-squared'][0]
                        else:
                            R_squared[k, j] = reg.bestFit['R-squared'][0]
                    elif reg.selectedVariables[0]==predictorCircadian:#'x1' in reg.model:
                        R_squared[k, j] = -1 * reg.bestFit['R-squared'][0]
                    elif reg.selectedVariables[0]==predictorSleepList[k]:#'x2' in reg.model:
                        R_squared[k, j] = reg.bestFit['R-squared'][0]
                    else:
                        R_squared[k, j] = 0
                except IndexError:
                    R_squared[k, j] = 0
#                print genotype,observationList[j],predictorCircadian,predictorSleepList[k]
#                print R_squared[k, j],reg.selectedVariables
#                print raw_input('...')
        signedRsquared[genotype] = R_squared
        figdict[genotype] = plt.figure(figsize=(5.5 * 3.13, 3.5 * 3.13))
#        plt.imshow(R_squared, interpolation='none')
        plt.pcolor(R_squared, vmin=vmin, vmax=vmax)
        plt.title(title + '\nGenotype: %s'%genotype, fontsize=title_size)
        plt.ylabel(y_label, fontsize=label_size)
        plt.xlabel(x_label, fontsize=label_size)
#        posx = plt.xticks()[0]
#        posy = plt.yticks()[0][1]
#        print(plt.yticks()[0])
        posy_all = 0.5 + np.arange(0,len(ytickList))
        plt.xticks(np.arange(len(xtickList))+0.5, xtickList, fontsize='x-small',
                   rotation=rotation)
        plt.yticks(posy_all, ytickList, fontsize='x-small',
                   rotation=rotation)
        plt.colorbar()
#        plt.xlim(-0.5, len(observationList) -0.5)
#        plt.ylim(-0.5, len(predictorSleepList) - 0.5)
    return figdict, signedRsquared

def plot_R_Squared_vs_Lag_GUI(lagVect, R_squared):
    fig = {}
    for obs in list(lagVect.keys()):
        gen = list(lagVect[obs].keys())[0]
        for predictor in list(lagVect[obs][gen].keys()):
            obsLabel = obs.split('.')[0]
            predLabel = predictor.split('.')[0]
            fig['Lag_%s_%s'%(obsLabel,predLabel)] =\
                plt.figure(figsize=(6.5*3.13,3.5*3.13))
            for genotype in list(lagVect[obs].keys()):
                plt.plot(lagVect[obs][genotype][predictor],
                         R_squared[obs][genotype][predictor], label=genotype,
                         linewidth=1.5)
                plt.legend()
            title = 'Lag\nObservation: %s\nPredictor: %s'%(obsLabel,predLabel)
            plt.ylabel('R-squared')
            plt.xlabel('Lag (hours)')
            plt.title(title)
            
    return fig